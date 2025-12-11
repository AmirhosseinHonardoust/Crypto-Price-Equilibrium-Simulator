import sys
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

# Make src importable
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src import config, data_prep, equilibrium


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load processed data (cached)."""
    return data_prep.load_processed()


def main() -> None:
    st.set_page_config(
        page_title="Crypto Price Equilibrium Simulator",
        layout="wide",
    )
    st.title("Crypto Price Equilibrium Simulator")

    df = load_data()

    # Reusable config for force plots
    force_cols = [
        config.COL_FORCE_DEMAND,
        config.COL_FORCE_SUPPLY,
        config.COL_FORCE_VOLATILITY,
        config.COL_FORCE_LIQUIDITY,
        config.COL_FORCE_SPECULATION,
    ]
    force_labels = ["Demand", "Supply", "Volatility", "Liquidity", "Speculation"]

    tab_single, tab_scenarios, tab_market = st.tabs(
        ["Single Coin", "Scenario Simulator", "Market Map"]
    )

    # ---------------------- Single Coin ----------------------
    with tab_single:
        st.subheader("Single Coin Equilibrium View")

        symbols = sorted(df[config.COL_SYMBOL].unique().tolist())
        if not symbols:
            st.error("No symbols found in processed data.")
            return

        symbol = st.selectbox("Symbol", symbols, index=0)
        row = df[df[config.COL_SYMBOL] == symbol].iloc[0]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Price", f"{row[config.COL_CURRENT_PRICE]:.6f}")
            if config.COL_MARKET_CAP_RANK in row.index:
                st.metric("Market Cap Rank", int(row[config.COL_MARKET_CAP_RANK]))

        with col2:
            st.metric("Equilibrium Center", f"{row[config.COL_EQ_CENTER]:.6f}")
            st.metric(
                "Equilibrium Shift",
                f"{row[config.COL_EQ_SHIFT] * 100:+.2f}%",
                help="Relative shift applied to current price to estimate equilibrium center.",
            )

        with col3:
            st.metric(
                "Equilibrium Band",
                f"[{row[config.COL_EQ_LOWER]:.6f}, {row[config.COL_EQ_UPPER]:.6f}]",
            )
            st.metric(
                "Tension Score",
                f"{row[config.COL_TENSION_SCORE]:.3f}",
                help="Higher tension implies more unstable equilibrium (forces pulling hard).",
            )

        st.markdown("### Force Decomposition")

        force_values = [row.get(c, np.nan) for c in force_cols]
        force_df = pd.DataFrame(
            {"force": force_labels, "value": force_values}
        ).set_index("force")
        st.bar_chart(force_df)

        with st.expander("Raw row (debug / inspection)"):
            st.json(
                {
                    k: (
                        float(row[k])
                        if isinstance(row[k], (int, float, np.floating))
                        else row[k]
                    )
                    for k in row.index
                }
            )

    # ---------------------- Scenario Simulator ----------------------
    with tab_scenarios:
        st.subheader("Scenario Simulator (What-If Analysis)")

        symbols = sorted(df[config.COL_SYMBOL].unique().tolist())
        symbol = st.selectbox(
            "Symbol for Scenario", symbols, index=0, key="scenario_symbol"
        )
        base_row = df[df[config.COL_SYMBOL] == symbol].iloc[0]

        st.markdown("Adjust hypothetical changes to see how equilibrium responds.")

        col1, col2, col3 = st.columns(3)
        with col1:
            vol_mult = st.slider(
                "Volume multiplier",
                min_value=0.1,
                max_value=5.0,
                value=1.0,
                step=0.1,
                help="Scale the total_volume for scenario.",
            )
        with col2:
            vol24_mult = st.slider(
                "24h volatility multiplier",
                min_value=0.1,
                max_value=5.0,
                value=1.0,
                step=0.1,
                help="Scale the 24h and 7d percent change magnitude.",
            )
        with col3:
            util_shift = st.slider(
                "Supply utilization shift (absolute)",
                min_value=-0.5,
                max_value=0.5,
                value=0.0,
                step=0.05,
                help="Adjust supply utilization (scarcity) up/down.",
            )

        if st.button("Run Scenario"):
            # Start from the base row
            sim_row = base_row.copy()

            # Apply scenario transformations
            sim_row[config.COL_TOTAL_VOLUME] = max(
                0.0, base_row[config.COL_TOTAL_VOLUME] * vol_mult
            )
            sim_row[config.COL_PCT_CHANGE_24H] = (
                base_row[config.COL_PCT_CHANGE_24H] * vol24_mult
            )
            sim_row[config.COL_PCT_CHANGE_7D] = (
                base_row[config.COL_PCT_CHANGE_7D] * vol24_mult
            )

            # Adjust supply utilization in [0, 1]
            current_util = float(base_row.get(config.COL_SUPPLY_UTILIZATION, 0.0))
            new_util = float(np.clip(current_util + util_shift, 0.0, 1.0))
            sim_row[config.COL_SUPPLY_UTILIZATION] = new_util

            # Use full market for ranking-based forces
            df_all = df.copy()
            mask = df_all[config.COL_SYMBOL] == symbol
            df_all.loc[mask, sim_row.index] = sim_row.values

            df_all = equilibrium.compute_engineered_features(df_all)
            df_all = equilibrium.compute_equilibrium(df_all)
            sim = df_all[mask].iloc[0]

            st.markdown("### Scenario Results")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Price", f"{sim[config.COL_CURRENT_PRICE]:.6f}")
            with col2:
                st.metric("Equilibrium Center", f"{sim[config.COL_EQ_CENTER]:.6f}")
                st.metric(
                    "Equilibrium Shift",
                    f"{sim[config.COL_EQ_SHIFT] * 100:+.2f}%",
                )
            with col3:
                st.metric(
                    "Equilibrium Band",
                    f"[{sim[config.COL_EQ_LOWER]:.6f}, {sim[config.COL_EQ_UPPER]:.6f}]",
                )
                st.metric("Tension Score", f"{sim[config.COL_TENSION_SCORE]:.3f}")

            st.markdown("### Scenario Force Decomposition")
            scenario_force_values = [sim.get(c, np.nan) for c in force_cols]
            scenario_force_df = pd.DataFrame(
                {"force": force_labels, "value": scenario_force_values}
            ).set_index("force")
            st.bar_chart(scenario_force_df)

            with st.expander("Scenario raw row"):
                st.json(
                    {
                        k: (
                            float(sim[k])
                            if isinstance(sim[k], (int, float, np.floating))
                            else sim[k]
                        )
                        for k in sim.index
                    }
                )

    # ---------------------- Market Map ----------------------
    with tab_market:
        st.subheader("Market Equilibrium Map")

        st.markdown(
            (
                "This view plots each asset by its **equilibrium shift** and "
                "**tension score**.\n\n"
                "- Assets with high positive shift may be pulled upward by forces.\n"
                "- Assets with high negative shift may be stretched high vs equilibrium.\n"
                "- High tension means the configuration is unstable."
            )
        )

        plot_df = df.copy()
        plot_df = plot_df[
            [
                config.COL_SYMBOL,
                config.COL_EQ_SHIFT,
                config.COL_TENSION_SCORE,
                config.COL_VOLATILITY_7D,
                config.COL_MARKET_CAP_RANK,
            ]
        ].dropna()

        st.scatter_chart(
            plot_df,
            x=config.COL_EQ_SHIFT,
            y=config.COL_TENSION_SCORE,
        )

        with st.expander("Sample of market data used in the map"):
            st.dataframe(plot_df.head(50))


if __name__ == "__main__":
    main()
