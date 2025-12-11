# **Crypto Price Equilibrium Simulator**

<p align="center">
  <img src="https://img.shields.io/badge/Project-Crypto%20Equilibrium%20Simulator-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Category-Market%20Modeling-4CAF50?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Theory-Equilibrium%20Forces-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Framework-Streamlit-red?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/Engine-Force%20Decomposition-9C27B0?style=for-the-badge" />

</p>

---

# **Overview**

**Crypto markets are not predictable, but they are explainable.**
Instead of treating price as something to forecast, this project treats price as something to **interpret** through equilibrium theory.

The **Crypto Price Equilibrium Simulator** models cryptocurrencies as systems governed by **forces**:

* **Demand** (inflow, momentum)
* **Supply** (scarcity, dilution)
* **Volatility** (risk, instability)
* **Liquidity** (depth, participation)
* **Speculation** (hype, short-term behavioral pressure)

These forces interact continuously, pushing prices upward or downward.
Instead of estimating a single target price, the model produces:

* **Equilibrium Center**, where the market *wants* the price to stabilize
* **Equilibrium Band**, acceptable price volatility range
* **Equilibrium Shift (%)**, deviation between market and equilibrium
* **Tension Score**, instability of the market environment
* **Force Decomposition**, transparent breakdown of upward/downward pressures

The goal is **interpretability**, giving traders, analysts, and researchers a way to *see* how crypto markets negotiate price.

This project includes:

* A **full modeling engine**
* A **CLI for data preparation & force inspection**
* A **Streamlit dashboard** with interactive simulation tools
* A complete **market equilibrium map** of 1000+ cryptocurrencies

---

# **Dataset**

This project uses the **Top 1000 Cryptocurrencies Real-Time Data (2025)** dataset
by **Mihika Ajay Jadhav** on Kaggle:

[https://www.kaggle.com/datasets/mihikaajayjadhav/top-1000-cryptocurrencies-real-time-data-2025](https://www.kaggle.com/datasets/mihikaajayjadhav/top-1000-cryptocurrencies-real-time-data-2025)

It includes:

* Prices, volumes, and market caps
* 1h / 24h / 7d / 30d / 1y price % changes
* Circulating, total, and max supply
* ATH / ATL metrics
* Rank, symbol, and name

This information is rich enough to build a **force-based equilibrium model** without requiring historic price series.

---

# **Theoretical Foundation**

## Why Prediction Fails in Crypto

Crypto markets are:

* Extremely volatile
* Highly speculative
* Behaviorally driven
* Influenced by liquidity shocks and circulation dynamics
* Not governed by stable fundamentals

Predicting exact prices is nearly impossible.

But **understanding forces** is feasible.

---

## Price as a Negotiated Outcome

We treat price as:

> **a temporary agreement between opposing forces.**

Just like particles in physics, assets in markets sit at the intersection of:

* upward pressure
* downward pressure
* internal instability

When forces balance, the asset is in **equilibrium**.
When forces diverge, the asset exhibits **tension**.

---

## Force-Based Modeling

Each crypto asset is transformed into a 5-dimensional force vector:

| Force           | Meaning                  | Interpretation                    |                     |
| --------------- | ------------------------ | --------------------------------- | ------------------- |
| **Demand**      | Market appetite          | High interest → upward pull       |                     |
| **Supply**      | Scarcity / cap structure | Scarce → upward                   | Diluting → downward |
| **Volatility**  | Risk environment         | High → downward pressure          |                     |
| **Liquidity**   | Stability of trading     | High → stabilizes equilibrium     |                     |
| **Speculation** | Short-term hype          | Can strongly push up or pull down |                     |

These forces are normalized to a standard scale **[-1, 1]** to expose their relative strength.

---

## Equilibrium Shift

The model computes:

```
raw_shift =
    0.35 * demand
  + 0.20 * supply
  - 0.20 * volatility
  + 0.15 * liquidity
  + 0.30 * speculation
```

Then scales it:

```
equilibrium_shift = 0.15 * raw_shift
```

Meaning:

* Positive shift → equilibrium is higher than current price
* Negative shift → price may be stretched above equilibrium

---

## Equilibrium Band

The band widens when:

* volatility is high
* speculation is high
* liquidity is low

Because instability expands the uncertainty region.

---

## Tension Score

Tension measures:

* how strongly forces disagree
* how volatile the environment is
* how fragile price becomes

High tension assets are “fragile equilibria.”

---

# Project Structure

```
Crypto-Price-Equilibrium-Simulator/
│
├── src/
│   ├── config.py
│   ├── data_prep.py
│   ├── equilibrium.py
│   └── cli.py
│
├── app/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── reports/
│   └── metrics/
│
└── README.md
```

---

# **Streamlit Application**

The UI has three main panels.

---

# **1. Single Coin Equilibrium View**

<img width="1274" height="600" alt="Screenshot 2025-12-11 at 17-45-50 Crypto Price Equilibrium Simulator" src="https://github.com/user-attachments/assets/e3b3d98e-7561-4d4e-b7ce-664c50e7adaf" />

This view focuses on one asset at a time, breaking down:

* Current price
* Market forces
* Equilibrium center
* Equilibrium shift
* Lower/upper bands
* Tension score

### Equilibrium Center

Represents the modeled “fair price” given the interacting forces:

* If demand + speculation dominate → equilibrium above current price
* If volatility + supply dominate → equilibrium below current price

### Equilibrium Shift (%)

A concise summary of price misalignment:

* **Positive** → market forces push the asset higher
* **Negative** → market forces push it lower
* **Near zero** → asset is price-aligned with equilibrium

### Equilibrium Band

Represents the realistic price range considering instability.
A wide band = chaotic environment.
A narrow band = stable market conditions.

### Tension Score

High tension means:

* forces are in conflict
* volatility is elevated
* equilibrium is unstable

This score is extremely valuable for risk assessment.

### Force Decomposition

This is the heart of interpretability.

**Demand** up?
→ buyers dominate.

**Supply** down?
→ supply oversaturation.

**Speculation** up?
→ hype or fear dominating fundamentals.

**Liquidity** weak?
→ market depth insufficient.

**Volatility** strong negative?
→ environment too unstable for price convergence.

This visualization explains **why** the equilibrium shifted.

---

# **2. Scenario Simulator (What-If Analysis)**

<img width="1302" height="646" alt="Screenshot 2025-12-11 at 18-04-19 Crypto Price Equilibrium Simulator" src="https://github.com/user-attachments/assets/e50a8f36-710c-4af4-b8c5-4c253c187236" />

This section lets you simulate **hypothetical market conditions**.

It is essentially a **market physics sandbox**, allowing analysts to ask:

* What if volatility doubled?
* What if liquidity surged?
* What if supply shocks occurred?
* What if market demand collapsed?

### Sliders:

**Volume multiplier**
Simulates inflow/outflow shocks.

**Volatility multiplier**
Simulates stress events, flash crashes, or stabilization.

**Supply utilization shift**
Simulates scarcity changes (burns, unlocks, halvings).

---

### Scenario Output Explanation

The screenshot demonstrates:

* Equilibrium center rising from **3114 → 3291**
* Equilibrium shift **+5.68%**
* Band width reflects a mix of volatility (widening) and liquidity (tightening)
* Tension score **1.023** suggesting instability

---

### Scenario Force Decomposition

This chart answers the question:

> “How did the forces change under my hypothetical environment?”

* **Demand force** increases dramatically if volume increases
* **Supply force** changes with utilization shifts
* **Volatility force** becomes more negative when volatility spikes
* **Speculation force** grows when volatility × liquidity intensifies

This section transforms the app into a **decision-support platform** for analysts.

---

# **3. Market Equilibrium Map**

<img width="1244" height="617" alt="Screenshot 2025-12-11 at 18-04-52 Crypto Price Equilibrium Simulator" src="https://github.com/user-attachments/assets/811ffaad-6a87-45f2-a724-a5292dd4e8a3" />

This map visualizes every cryptocurrency as a point in a **force-driven equilibrium space**.

### X-Axis: Equilibrium Shift

Shows whether an asset is:

* pulled upward (right side)
* pulled downward (left side)
* or stable (center)

### Y-Axis: Tension Score

Shows how violently the market forces interact:

* low tension → stable equilibrium
* high tension → fragile equilibrium

---

### How to Interpret the Screenshot

The screenshot shows:

* A rising curve: higher equilibrium shift often correlates with higher tension
* Clusters of assets: groups behaving similarly under market stress
* Outliers: assets with extreme disequilibrium, often highly speculative
* Calm zone around (0, 0.3–0.6): assets near equilibrium and low risk
* Unstable zone in upper-right corner: high shift + high tension → speculative bubbles

This map becomes a **market-wide diagnostic tool**.

---

# CLI Usage

All commands should be run from the project root directory.

### Prepare processed data

```bash
python -m src.cli prepare-data
```

This will:

* read `data/raw/crypto_top1000_dataset.csv`
* clean and engineer features
* compute forces & equilibrium values
* cache the result in `data/processed/crypto_equilibrium.parquet`

---

### Inspect equilibrium for a single asset

You can select an asset by **index** (row number in the processed dataset):

```bash
python -m src.cli show-equilibrium --index 0
```

Or by **symbol**:

```bash
python -m src.cli show-equilibrium --symbol ETH
```

The CLI prints:

* basic asset metadata (symbol, name, rank)
* current price, market cap, and volume
* all five forces (demand, supply, volatility, liquidity, speculation)
* equilibrium shift, center, band, and tension score

---

### Export a full equilibrium snapshot

```bash
python -m src.cli export-equilibrium --out equilibrium_snapshot.csv
```

Output is saved under:

```text
reports/metrics/equilibrium_snapshot.csv
```

You can open this in a notebook, Excel, or any BI tool to do more custom analysis.

---

## Streamlit Dashboard

Run the dashboard with:

```bash
streamlit run app/app.py
```

The UI has three tabs:

1. **Single Coin**
2. **Scenario Simulator**
3. **Market Map**

---

# Limitations

This model is **interpretative**, not predictive.

* Uses snapshot data
* Does not incorporate order book depth
* No historical volatility estimation
* No causal modeling
* Scenario results are directional, not exact

Still, it reveals deep market structure invisible in raw prices.

---

# Future Improvements

* Time-series equilibrium drift
* Order-book-informed demand pressure
* Automated equilibrium regime detection
* ML-generated force weights
* Narrative-driven scenario templates
