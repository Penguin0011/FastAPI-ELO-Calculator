# The Bayesian F1 Engine

A FastAPI-based ELO calculator that pulls data from fastf1.dev and calculates driver ELO ratings using Bayesian inference to separate driver skill from car performance.

## Repository Info
- Repo: theaakashb/FastAPI-ELO-Calculator
- Language composition: Python (100%)

## Quick Start

### Getting Started
1. Create and activate a virtual environment
   - macOS/Linux:
     ```
     python -m venv .venv
     source .venv/bin/activate
     ```
   - Windows (PowerShell):
     ```
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the FastAPI app (example):
   ```
   uvicorn app.main:app --reload
   ```
   Adjust the module path to match your project layout.

### Data Sources and Networking
To allow FastF1 to retrieve data, ensure your firewall permits outbound HTTPS access to:
- https://livetiming.formula1.com (primary for live timing/telemetry)

Depending on your usage for schedules/results, you may also need:
- https://ergast.com
- https://api.jolpica-f1.com

### Configuration
- Set any environment variables required for FastF1 caching or API behavior.
- Configure ELO calculation parameters (e.g., K-factor, weighting for quali vs race, DNFs, penalties) in your application settings.

### Endpoints (examples)
- `GET /elo/{driver}`: Retrieve the current ELO for a driver
- `POST /elo/recalculate`: Trigger recalculation for a session or season
- `GET /sessions/{year}`: List sessions available for a given year

Note: Actual endpoints depend on how your FastAPI app is structured.

---

## The Methodology: Why Bayesian?

This project explores why standard ranking systems fail in the chaotic environment of Formula 1 and how a **Bayesian Inference** approach solves the "Man vs. Machine" paradox. By the end of this section, you will understand:
*   Why "Points Exchange" models (like standard Elo) cannot handle F1's hardware asymmetry.
*   What "Bayesian Inference" actually is (without the jargon).
*   How we mathematically isolate **Driver Skill** from **Car Performance** using telemetry physics and probability theory.

---

## 1. The Standard Elo: A Model of Symmetry

The Elo rating system was invented by Arpad Elo for Chess, a game of perfect information and symmetry.
In Chess:
1.  **Symmetry:** Both players use the same pieces.
2.  **Zero-Sum:** If I win, you lose.
3.  **Isolation:** It is 1 vs 1.

The math is simple: *Probability of Winning* is a function of the difference in ratings. If a Grandmaster beats a Novice, the system says "I expected that," and ratings barely change. If a Novice beats a Grandmaster, the system says "Surprise!" and points are transferred heavily.

### The F1 Paradox
Why does this fail in Formula 1?
Because Formula 1 is **asymmetric**.

> **Think about it:** If Max Verstappen (World Champion) is driving a Haas, and Logan Sargeant (Rookie) is driving a Red Bull, who wins?

Likely Logan.
A standard Elo model would see Logan beating Max and conclude: *"Logan is better than Max."*
We know this is false. The *Car* won, not the driver. Standard Elo has no variable for "The Machine," so it blindly conflates Car Performance with Driver Skill. To fix this, we need a smarter statistical framework.

---

## 2. A Primer: What is a Bayesian Model?

Before diving into our formulas, let's understand the philosophy.
**Bayesian Inference** is not about counting wins and losses. It is about **Updating Beliefs**.

It follows a cycle:
1.  **Prior Belief:** What did we think *before* the race started?
    *   *Example:* "We believe Max is an 1800-rated driver."
2.  **Likelihood (The Evidence):** The race happens.
    *   *Example:* Max enters a race. He finishes P1.
3.  **Posterior Update:** How does this evidence change our belief?
    *   *The Twist:* We check *how probable* that P1 result was given his Car.
    *   If he was in a Rocket Ship, P1 was 99% probable. The "Evidence" is weak. Our belief (rating) barely changes.
    *   If he was in a Tractor, P1 was 1% probable. The "Evidence" is massive. Our belief shifts drastically.

**In F1 terms:**
We treat every race not as a "Match," but as a **Noisy Experiment**. The result (Position) is the signal, but the Car is the Noise. Bayesian methods allow us to mathematically "subtract" the noise to find the true signal (Driver Skill).

---

## 3. Inner Workings: The Equations of Isolation

Now that we understand the *Why*, let's look at the *How*.
This engine implements a custom high-dimensional model to calculate **Composite Effective Strength**.

### 3.1 Separating Man from Machine
We posit that the "Strength" displayed on track is the sum of two latent variables:
$$R_{effective} = R_{driver} + R_{car}$$

When calculating the probability of Driver A beating Driver B, we don't compare their skills. We compare their **Total Packages**:

$$P(A > B) = \frac{1}{1 + 10^{\frac{(R_{driver\_B} + R_{car\_B}) - (R_{driver\_A} + R_{car\_A})}{400}}}$$

**What does this mean effectively?**
It acts as a **Handicap**.
*   If you are in a dominant car ($R_{car} = High$), you start the math with a massive advantage.
*   To gain rating points, you must outperform that advantage. Merely winning isn't enough; you must win *more convincingly* than the car predicts.

---

## 4. Modeling Volatility: The "K-Factor" Dynamics

How fast should a rating change? In our model, this is dynamic. We use four context-aware vectors to determine the volatility ($K$) of any given result.

### 4.1 Teammate Isolation (The Control Group)
This is the most critical component.
The only strictly fair comparison in F1 is your teammate. They are the "Control Group" for the car variable.
We mathematically enforce that **50% of your rating** is derived from your battle with your teammate.

$$Weight_{teammate} = N_{drivers} - 2$$
$$Weight_{others} = 1$$

In a grid of 20, your 1 teammate is weighted x18 stronger than any other individual rival. Beating your teammate is the only way to prove *pure* skill separate from the car.

### 4.2 The "Golden Era" Multiplier
Not all grids are equal. A win in 2012 (6 World Champions on the grid) is harder than a win in a depleted year.
We count the number of Champions ($N_{WDC}$) and scale the points:
$$K_{grid} = 1 + (0.05 \cdot N_{WDC})$$

### 4.3 Season Normalization
Modern seasons (24 races) are longer than classic seasons (16 races). To prevent "recency bias" where modern drivers accumulate stats faster, we normalize all volatility to a 20-race standard. A race in the 80s is fundamentally worth more rating points than a race today.

---

## 5. Physics-Based Features

Results tell us *what* happened. Telemetry tells us *how* it happened.
We ingest lap-by-lap telemetry data to calculate style-based bonuses.

### 5.1 Braking Aggression Logic
Late braking is a high-risk, high-skill trait. We measure it by analyzing the **Deceleration Gradient** ($g$-force) from the car's speed traces.

$$a(t) = \frac{\Delta v}{\Delta t}$$

We extract the **95th percentile peak deceleration**.
*   Standard Braking: ~4.0g
*   Elite Braking: >5.0g
*   **"Honey Badger" Zone:** >5.5g

Drivers who consistently register in the "Honey Badger" zone (braking later and harder than physics suggests is safe) receive a **1.5x Volatility Bonus**. This allows the model to reward "Aggressive Elo" even if the driver finishes P5.

### 5.2 The "Carry Job" Gradient
What happens when a driver simply outperforms their machinery?
If $R_{driver} > R_{car}$, we apply a continuous reward gradient.
$$Bonus = 1 + \left( \frac{R_{driver} - R_{car}}{1000} \right)$$
The bigger the gap between Driver Skill and Car Performance, the more points the driver gets for a positive result. This mathematically rewards the "underdog" performance.

---

## 6. Asymmetry: The "Robbery" Prevention

Finally, we address the biggest flaw in standard stats: **Mechanical Failure (DNF).**
In most models, a DNF is a Loss.
In our model, a Mechanical DNF is **Information Loss**.

### 6.1 The "Stolen Win" Logic
If a driver suffers a mechanical failure (Engine, Hydraulics, Brakes) while running in a points-paying position, the model triggers the **Robbery Protocol**:
1.  **Voiding:** All comparisons against drivers below them are voided (you didn't lose to them, you vanished).
2.  **Compensation:** For the comparisons that *did* happen (e.g., losing the lead), we apply a **500% Volatility Multiplier** ($K=5.0$) to the assumption that they *would* have maintained their pace.

This ensures that reliability issues do not disguise a driver's peak capability. A driver who leads every lap and breaks down on the final corner will effectively "keep" the rating they would have earned, protecting their Peak Elo.

---

## Final Thoughts
By combining **Bayesian Probability**, **Physics Telemetry**, and **Context-Aware Volatility**, this engine does what the Championship Standings cannot: it predicts who would win if everyone drove the same car.

---

## Development Notes
- FastF1 benefits from a local cache to avoid repeated downloads; ensure the cache directory is writable.
- When running behind a firewall, verify the allowed domains above are reachable.
- This project uses the FastF1 library to retrieve Formula 1 timing and telemetry data, then computes ELO ratings for drivers based on configurable factors.

## License
Add your chosen license here.