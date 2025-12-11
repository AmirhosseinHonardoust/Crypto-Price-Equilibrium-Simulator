from __future__ import annotations

import pandas as pd

from . import config, equilibrium


def load_raw() -> pd.DataFrame:
    """Load the raw crypto dataset from CSV."""
    path = config.DATA_RAW
    if not path.exists():
        raise FileNotFoundError(f"Raw data not found at: {path}")
    df = pd.read_csv(path)
    return df


def clean_and_engineer(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning and feature engineering.

    - Ensures numeric types where appropriate
    - Computes liquidity, volatility, and speculation indices
    - Computes equilibrium forces and outputs
    """
    df = df.copy()

    # Ensure numeric for key columns (coerce errors to NaN)
    numeric_cols = [
        config.COL_MARKET_CAP_RANK,
        config.COL_CURRENT_PRICE,
        config.COL_MARKET_CAP,
        config.COL_FULLY_DILUTED_VALUATION,
        config.COL_TOTAL_VOLUME,
        config.COL_HIGH_24H,
        config.COL_LOW_24H,
        config.COL_CIRC_SUPPLY,
        config.COL_TOTAL_SUPPLY,
        config.COL_MAX_SUPPLY,
        config.COL_ATH,
        config.COL_ATH_CHANGE_PCT,
        config.COL_ATL,
        config.COL_ATL_CHANGE_PCT,
        config.COL_PRICE_CHANGE_24H,
        config.COL_PCT_CHANGE_24H,
        config.COL_PCT_CHANGE_1H,
        config.COL_PCT_CHANGE_7D,
        config.COL_PCT_CHANGE_30D,
        config.COL_PCT_CHANGE_1Y,
        config.COL_MARKET_CAP_CHANGE_24H,
        config.COL_MARKET_CAP_PCT_CHANGE_24H,
        config.COL_SUPPLY_UTILIZATION,
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows missing critical price or market cap info
    required = [
        config.COL_SYMBOL,
        config.COL_CURRENT_PRICE,
        config.COL_MARKET_CAP,
        config.COL_TOTAL_VOLUME,
    ]
    existing_required = [c for c in required if c in df.columns]
    df = df.dropna(subset=existing_required)

    # Compute engineered metrics & equilibrium
    df = equilibrium.compute_engineered_features(df)
    df = equilibrium.compute_equilibrium(df)

    return df


def load_processed() -> pd.DataFrame:
    """Load processed data, computing and caching it if needed."""
    config.DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    processed_path = config.DATA_PROCESSED_DIR / "crypto_equilibrium.parquet"

    if processed_path.exists():
        return pd.read_parquet(processed_path)

    df_raw = load_raw()
    df_proc = clean_and_engineer(df_raw)
    df_proc.to_parquet(processed_path, index=False)
    return df_proc
