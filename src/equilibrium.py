from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd

from . import config


def _safe_divide(a: pd.Series, b: pd.Series) -> pd.Series:
    """Safe division with protection against zero and NaN."""
    return a / b.replace(0, np.nan)


def _rank_to_unit(s: pd.Series, ascending: bool = True) -> pd.Series:
    """Map a series to [-1, 1] based on rank.

    - ascending=True: low values -> -1, high values -> +1
    - ascending=False: high values -> -1, low values -> +1
    """
    s = s.astype(float)
    # Handle constant or all-NaN columns gracefully
    if s.nunique(dropna=True) <= 1:
        return pd.Series(0.0, index=s.index)

    ranks = s.rank(pct=True, method="average")
    if not ascending:
        ranks = 1.0 - ranks
    return 2.0 * (ranks - 0.5)


def compute_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute liquidity, volatility, and speculation helper columns."""
    df = df.copy()

    # Liquidity ratio: how much volume relative to market cap
    df[config.COL_LIQUIDITY_RATIO] = _safe_divide(
        df[config.COL_TOTAL_VOLUME], df[config.COL_MARKET_CAP]
    )

    # Volatility measures based on percentage price changes
    df[config.COL_VOLATILITY_24H] = df[config.COL_PCT_CHANGE_24H].abs()
    df[config.COL_VOLATILITY_7D] = df[config.COL_PCT_CHANGE_7D].abs()

    # Speculation index: amplified short-term swings weighted by liquidity
    df[config.COL_SPECULATION_INDEX] = (
        df[config.COL_VOLATILITY_24H].fillna(0.0)
        + df[config.COL_VOLATILITY_7D].fillna(0.0)
    ) * df[config.COL_LIQUIDITY_RATIO].fillna(0.0)

    # Supply utilization: if not provided or constant, approximate from circs/max
    if (
        config.COL_SUPPLY_UTILIZATION in df.columns
        and df[config.COL_SUPPLY_UTILIZATION].notna().any()
        and df[config.COL_SUPPLY_UTILIZATION].nunique(dropna=True) > 1
    ):
        # Already usable
        pass
    else:
        util = _safe_divide(df[config.COL_CIRC_SUPPLY], df[config.COL_MAX_SUPPLY])
        df[config.COL_SUPPLY_UTILIZATION] = util.clip(lower=0.0, upper=1.0)

    return df


def compute_equilibrium(df: pd.DataFrame) -> pd.DataFrame:
    """Compute forces and equilibrium band for each asset.

    The idea:

    - Demand force: driven by volume and recent positive momentum
    - Supply force: driven by supply utilization (scarcity)
    - Volatility force: driven by recent volatility (acts as destabiliser)
    - Liquidity force: driven by liquidity ratio (stabiliser when high)
    - Speculation force: driven by speculation index (short-term hype)

    These forces are combined into a raw equilibrium shift, which is then
    scaled and applied to current_price to obtain center / band.
    """
    df = df.copy()

    # --- Demand force: high volume and strong 7d positive momentum -> positive ---
    vol = df[config.COL_TOTAL_VOLUME].fillna(0.0)
    mom_7d = df[config.COL_PCT_CHANGE_7D].fillna(0.0)
    demand_score = 0.6 * _rank_to_unit(vol, ascending=True) + 0.4 * _rank_to_unit(
        mom_7d, ascending=True
    )
    df[config.COL_FORCE_DEMAND] = demand_score.clip(-1.0, 1.0)

    # --- Supply force: higher utilization -> more scarcity -> positive ---
    supply_util = df[config.COL_SUPPLY_UTILIZATION].fillna(0.0)
    supply_force = _rank_to_unit(supply_util, ascending=True)
    df[config.COL_FORCE_SUPPLY] = supply_force.clip(-1.0, 1.0)

    # --- Volatility force: more volatility -> more instability (negative towards equilibrium) ---
    vol_7d = df[config.COL_VOLATILITY_7D].fillna(0.0)
    volatility_force = _rank_to_unit(vol_7d, ascending=False)
    # Here: high volatility -> more negative
    df[config.COL_FORCE_VOLATILITY] = volatility_force.clip(-1.0, 1.0)

    # --- Liquidity force: high liquidity ratio -> stabilising positive force ---
    liq_ratio = df[config.COL_LIQUIDITY_RATIO].fillna(0.0)
    liquidity_force = _rank_to_unit(liq_ratio, ascending=True)
    df[config.COL_FORCE_LIQUIDITY] = liquidity_force.clip(-1.0, 1.0)

    # --- Speculation force: short-term hype, can push price away from fundamentals ---
    spec_idx = df[config.COL_SPECULATION_INDEX].fillna(0.0)
    speculation_force = _rank_to_unit(spec_idx, ascending=True)
    df[config.COL_FORCE_SPECULATION] = speculation_force.clip(-1.0, 1.0)

    # --- Combine forces into equilibrium shift ---
    # Weights are deliberately simple and interpretable
    w_demand = 0.35
    w_supply = 0.20
    w_volatility = -0.20  # more volatility pulls away from stable equilibrium
    w_liquidity = 0.15
    w_speculation = 0.30

    raw_shift = (
        w_demand * df[config.COL_FORCE_DEMAND]
        + w_supply * df[config.COL_FORCE_SUPPLY]
        + w_volatility * df[config.COL_FORCE_VOLATILITY]
        + w_liquidity * df[config.COL_FORCE_LIQUIDITY]
        + w_speculation * df[config.COL_FORCE_SPECULATION]
    )

    # Limit the raw shift to a reasonable range
    raw_shift = raw_shift.clip(-1.0, 1.0)

    # Scale: we interpret raw_shift as a multiplier within a band, e.g. +/- 15%
    shift_scale = 0.15
    equilibrium_shift = shift_scale * raw_shift

    df[config.COL_EQ_SHIFT] = equilibrium_shift

    # Compute equilibrium center & band around the *current* price
    price = df[config.COL_CURRENT_PRICE].astype(float)
    center = price * (1.0 + equilibrium_shift)

    # Band width grows with volatility and speculation
    base_band_width = 0.05  # 5%
    extra_from_volatility = 0.10 * (
        (df[config.COL_FORCE_VOLATILITY] * -1.0 + 1.0) / 2.0
    )  # higher volatility -> wider band
    extra_from_speculation = 0.05 * (
        (df[config.COL_FORCE_SPECULATION] + 1.0) / 2.0
    )
    band_width = base_band_width + extra_from_volatility + extra_from_speculation
    band_width = band_width.clip(0.05, 0.25)

    lower = center * (1.0 - band_width)
    upper = center * (1.0 + band_width)

    df[config.COL_EQ_CENTER] = center
    df[config.COL_EQ_LOWER] = lower
    df[config.COL_EQ_UPPER] = upper

    # Tension score: magnitude of raw shift plus volatility contribution
    tension = raw_shift.abs() + (df[config.COL_FORCE_VOLATILITY] * -1.0 + 1.0) / 2.0
    df[config.COL_TENSION_SCORE] = tension

    return df
