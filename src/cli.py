from __future__ import annotations

import argparse
from typing import Optional

from . import config, data_prep


def cmd_prepare_data(args: argparse.Namespace) -> None:
    df = data_prep.load_processed()
    print(f"Prepared processed dataset with {len(df)} rows.")
    print("Columns available:")
    print(", ".join(df.columns))


def _select_row(index: Optional[int], symbol: Optional[str]):
    df = data_prep.load_processed()
    if symbol is not None:
        mask = df[config.COL_SYMBOL].str.upper() == symbol.upper()
        if not mask.any():
            raise ValueError(f"Symbol {symbol} not found in processed dataset.")
        row = df[mask].iloc[0]
    else:
        if index is None:
            raise ValueError("Either --index or --symbol must be provided.")
        if index < 0 or index >= len(df):
            raise IndexError(f"Index {index} out of range for dataset of size {len(df)}.")
        row = df.iloc[index]
    return row


def cmd_show_equilibrium(args: argparse.Namespace) -> None:
    row = _select_row(args.index, args.symbol)

    print("Asset:")
    for col in [config.COL_SYMBOL, config.COL_NAME, config.COL_MARKET_CAP_RANK]:
        if col in row.index:
            print(f"- {col}: {row[col]}")

    print("\nCurrent state:")
    for col in [config.COL_CURRENT_PRICE, config.COL_MARKET_CAP, config.COL_TOTAL_VOLUME]:
        if col in row.index:
            print(f"- {col}: {row[col]}")

    print("\nForces:")
    for col in [
        config.COL_FORCE_DEMAND,
        config.COL_FORCE_SUPPLY,
        config.COL_FORCE_VOLATILITY,
        config.COL_FORCE_LIQUIDITY,
        config.COL_FORCE_SPECULATION,
    ]:
        if col in row.index:
            print(f"- {col}: {row[col]:+.3f}")

    print("\nEquilibrium:")
    for col in [
        config.COL_EQ_SHIFT,
        config.COL_EQ_CENTER,
        config.COL_EQ_LOWER,
        config.COL_EQ_UPPER,
        config.COL_TENSION_SCORE,
    ]:
        if col in row.index:
            print(f"- {col}: {row[col]:.6f}")


def cmd_export_equilibrium(args: argparse.Namespace) -> None:
    df = data_prep.load_processed()
    out_path = args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Exported equilibrium snapshot to {out_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Crypto Price Equilibrium Simulator CLI"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_prepare = subparsers.add_parser(
        "prepare-data", help="Clean, engineer features, and compute equilibrium."
    )
    p_prepare.set_defaults(func=cmd_prepare_data)

    p_show = subparsers.add_parser(
        "show-equilibrium", help="Show equilibrium details for a single asset."
    )
    p_show.add_argument(
        "--index",
        type=int,
        default=None,
        help="Row index in the processed dataset.",
    )
    p_show.add_argument(
        "--symbol",
        type=str,
        default=None,
        help="Asset symbol (e.g. BTC, ETH). Overrides --index if provided.",
    )
    p_show.set_defaults(func=cmd_show_equilibrium)

    p_export = subparsers.add_parser(
        "export-equilibrium",
        help="Export full equilibrium snapshot to CSV.",
    )
    p_export.add_argument(
        "--out",
        type=lambda p: config.REPORTS_METRICS_DIR / p,
        default=config.REPORTS_METRICS_DIR / "equilibrium_snapshot.csv",
        help="Output CSV path (relative to project root reports/metrics).",    )
    p_export.set_defaults(func=cmd_export_equilibrium)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
