from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_RAW = BASE_DIR / "data" / "raw" / "crypto_top1000_dataset.csv"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_METRICS_DIR = REPORTS_DIR / "metrics"
REPORTS_FIGURES_DIR = REPORTS_DIR / "figures"

# Dataset column names (from the Kaggle crypto_top1000 dataset)
COL_ID = "id"
COL_SYMBOL = "symbol"
COL_NAME = "name"
COL_MARKET_CAP_RANK = "market_cap_rank"
COL_CURRENT_PRICE = "current_price"
COL_MARKET_CAP = "market_cap"
COL_FULLY_DILUTED_VALUATION = "fully_diluted_valuation"
COL_TOTAL_VOLUME = "total_volume"
COL_HIGH_24H = "high_24h"
COL_LOW_24H = "low_24h"
COL_CIRC_SUPPLY = "circulating_supply"
COL_TOTAL_SUPPLY = "total_supply"
COL_MAX_SUPPLY = "max_supply"
COL_ATH = "ath"
COL_ATH_CHANGE_PCT = "ath_change_percentage"
COL_ATH_DATE = "ath_date"
COL_ATL = "atl"
COL_ATL_CHANGE_PCT = "atl_change_percentage"
COL_ATL_DATE = "atl_date"
COL_PRICE_CHANGE_24H = "price_change_24h"
COL_PCT_CHANGE_24H = "price_change_percentage_24h"
COL_PCT_CHANGE_1H = "price_change_percentage_1h"
COL_PCT_CHANGE_7D = "price_change_percentage_7d"
COL_PCT_CHANGE_30D = "price_change_percentage_30d"
COL_PCT_CHANGE_1Y = "price_change_percentage_1y"
COL_MARKET_CAP_CHANGE_24H = "market_cap_change_24h"
COL_MARKET_CAP_PCT_CHANGE_24H = "market_cap_change_percentage_24h"
COL_LAST_UPDATED = "last_updated"
COL_IMAGE = "image"
COL_SUPPLY_UTILIZATION = "supply_utilization"

# Engineered feature names
COL_LIQUIDITY_RATIO = "liquidity_ratio"
COL_VOLATILITY_24H = "volatility_24h"
COL_VOLATILITY_7D = "volatility_7d"
COL_SPECULATION_INDEX = "speculation_index"

# Force columns
COL_FORCE_DEMAND = "force_demand"
COL_FORCE_SUPPLY = "force_supply"
COL_FORCE_VOLATILITY = "force_volatility"
COL_FORCE_LIQUIDITY = "force_liquidity"
COL_FORCE_SPECULATION = "force_speculation"

# Equilibrium outputs
COL_EQ_SHIFT = "equilibrium_shift"
COL_EQ_CENTER = "equilibrium_center"
COL_EQ_LOWER = "equilibrium_lower"
COL_EQ_UPPER = "equilibrium_upper"
COL_TENSION_SCORE = "tension_score"
