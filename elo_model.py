import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from collections import defaultdict

class BayesianEloModel:
    def __init__(self, k_factor=24.0, gamma=1.0, initial_ratings=None):
        self.k_factor = k_factor
        self.gamma = gamma
        self.initial_ratings = initial_ratings or {}
        
        # State
        self.driver_ratings = {} 
        self.constructor_ratings = {}
        self.driver_history = []
        
        # "Potential" / Peak Tracking
        self.peak_ratings = {}

    def set_peaks(self, peaks: Dict[str, float]):
        self.peak_ratings = peaks
        
    def get_initial_rating(self, driver):
        return self.initial_ratings.get(driver, 1500.0)
        
    def get_expected_score(self, rating_a, rating_b):
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

    def update(self, race_data: pd.DataFrame):
        """
        Update ratings based on a single race results.
        race_data: DataFrame with ['driver_name', 'constructor', 'effective_position', 'is_mechanical_dnf']
        """
        # Sort by effective position
        # Filter out invalid positions? No, we handle them.
        
        # We need pairwise comparisons?
        # A common approach for multi-competitor games is to treat it as N(N-1)/2 pairwise matches
        # Or compare each driver to the average of opponents.
        
        results = race_data.sort_values('effective_position')
        drivers = results['driver_name'].values
        constructors = results['constructor'].values
        positions = results['effective_position'].values
        is_mech_dnf = results['is_mechanical_dnf'].values
        braking_scores = results['braking_score'].values if 'braking_score' in results.columns else np.zeros(len(positions))
        
        n_drivers = len(drivers)
        
        # Store current ratings for history
        # If new driver, initialize
        for d in drivers:
            if d not in self.driver_ratings:
                self.driver_ratings[d] = self.get_initial_rating(d)
                
        for c in constructors:
             if c not in self.constructor_ratings:
                self.constructor_ratings[c] = 1500.0

        current_ratings_snapshot = {d: self.driver_ratings[d] for d in drivers}
        
        # Calculate rating deltas
        driver_deltas = defaultdict(float)
        constructor_deltas = defaultdict(float)
        
        # Pairwise updates
        for i in range(n_drivers):
            for j in range(i + 1, n_drivers):
                d_a, c_a = drivers[i], constructors[i]
                d_b, c_b = drivers[j], constructors[j]
                
                # Check positions
                pos_a = positions[i]
                pos_b = positions[j]
                
                # If tied (rare in F1, but possible with DNFs on same lap?), skip or draw
                if pos_a == pos_b:
                    actual_score_a = 0.5
                elif pos_a < pos_b:
                    actual_score_a = 1.0
                else:
                    actual_score_a = 0.0
                
                # Composite Ratings: Driver + Car
                # We want to infer Driver Skill.
                # Total Strength = Driver + Car
                
                # FEATURE: FUTURE POTENTIAL WEIGHTING
                # If we know the driver's FUTURE PEAK, we blend it into their current strength for the calculation.
                # This means beating a "Future Legend" counts more.
                # self.peak_ratings is populated in Pass 2.
                
                rating_a_eff = self.driver_ratings[d_a]
                rating_b_eff = self.driver_ratings[d_b]
                
                if hasattr(self, 'peak_ratings') and self.peak_ratings:
                    # Blend current rating with peak rating
                    # This primarily boosts the "Opponent Strength" perception.
                    # We use a weight (e.g. 0.5)
                    w = 0.85 # 85% Future Potential Influence (High weight for "Legend" recognition)
                    
                    if d_a in self.peak_ratings:
                        # Only use peak if it's higher (Potential)
                        peak_a = max(self.peak_ratings[d_a], rating_a_eff)
                        rating_a_eff = (1 - w) * rating_a_eff + w * peak_a
                        
                    if d_b in self.peak_ratings:
                        peak_b = max(self.peak_ratings[d_b], rating_b_eff)
                        rating_b_eff = (1 - w) * rating_b_eff + w * peak_b
                
                metric_a = rating_a_eff + self.gamma * self.constructor_ratings[c_a]
                metric_b = rating_b_eff + self.gamma * self.constructor_ratings[c_b]
                
                expected_a = self.get_expected_score(metric_a, metric_b)
                
                # ENHANCEMENT: "Upside Volatility"
                multiplier = 1.0
                if actual_score_a > expected_a: # A won/did better than expected
                    if expected_a < 0.3: # Less than 30% chance to win
                        # Giant Killing!
                        multiplier = 1.5
                
                # Update
                # The K-factor is shared.
                # Logic Verification:
                # 1. DNF (Mechanical) + BONUS logic
                #    BONUS: "give them more points because they could've finished higher"
                #    User requested "even more inflated".
                #    We apply a massive multiplier for Unlucky DNFs.
                
                mech_bonus = 1.0
                if is_mech_dnf[i]:
                     # User wants Ricciardo Top 3.
                     # We boost the update delta massively (5x).
                     # This treats a P1 Mechanical DNF as a Career Defining Performance.
                     mech_bonus = 5.0
                     
                # 2. Car Outperformance / "Late Braking" Style Bonus
                #    "performing super well relative to car performance"
                #    If Driver Rating >> Constructor Rating, they are carrying the car.
                #    We boost their gains to reflect this "Skill Gap".
                
                style_bonus = 1.0
                # Check if driver is outperforming car significantly (> 50 ELO points)
                if self.driver_ratings[d_a] > (self.constructor_ratings[c_a] + 50):
                     if actual_score_a > 0.5: # Only if they won/drew
                        style_bonus = 1.3 # 30% Boost for outperforming machinery
                        
                # 3. Late Braking / Telemetry Bonus
                #    "add a multiplier for breaking extremely late... push Daniel Ricciardo to a higher peak"
                #    We check 'braking_score'. If > Threshold (e.g. 5.0g approx? F1 cars do 5-6g).
                #    Ricciardo is known for this.
                #    Let's check if braking_score is in top 10% of field for that race?
                #    Calculating that dynamically is slow.
                #    We will just check raw threshold or relative.
                #    Let's use a dynamic check: Is Braking Score A > Braking Score B * 1.05?
                
                braking_bonus = 1.0
                # Retrieve scores from data. We need to pass them in `update`.
                # race_data now has 'braking_score'.
                # We need to access it by index or driver.
                
                # We extracted arrays at the start of update(), but not braking_score.
                # We need to add it there.
                
                # Assuming braking_scores handles map
                score_a = braking_scores[i]
                
                # Ricciardo "Late Braking" Threshold
                # If Score > 5.5 (g-force), that's elite.
                if score_a > 5.0:
                    braking_bonus = 1.2 # 20% Boost for Elite Braking
                    if score_a > 5.5: # Super elite (Ricciardo mode)
                        braking_bonus = 1.5 
                        
                delta = self.k_factor * multiplier * mech_bonus * style_bonus * braking_bonus * (actual_score_a - expected_a)

                # Scaling K for number of opponents
                # In 1v1 chess K=20. In 20-player race, 19 comparisons.
                # We should divide K by (N-1) or similar.

                k_scaled = delta / (n_drivers - 1)

                # Apply updates
                driver_deltas[d_a] += k_scaled
                driver_deltas[d_b] -= k_scaled
                
                # Constructor updates
                # Maybe slower update for constructors?
                constructor_deltas[c_a] += k_scaled * (actual_score_a - expected_a) # * 0.5?
                constructor_deltas[c_b] -= k_scaled * (actual_score_a - expected_a)
        
        # Apply accumulated deltas
        for d in drivers:
            self.driver_ratings[d] += driver_deltas[d]
        for c in constructors:
            self.constructor_ratings[c] += constructor_deltas[c]
            
        # Record history
        for d in drivers:
            self.driver_history.append({
                'year': race_data['year'].iloc[0],
                'round': race_data['round'].iloc[0],
                'race_name': race_data['race_name'].iloc[0], 
                'date': race_data['date'].iloc[0], # Added for plotting order
                'driver': d,
                'rating': self.driver_ratings[d],
                'constructor_rating': self.constructor_ratings[race_data[race_data['driver_name']==d]['constructor'].values[0]]
            })

    def fit(self, all_race_data: pd.DataFrame):
        grouped = all_race_data.groupby(['year', 'round'])
        # Ensure chronological order
        sorted_groups = sorted(grouped, key=lambda x: (x[0][0], x[0][1]))
        
        for (year, rnd), race_df in sorted_groups:
            self.update(race_df)

    def get_history_df(self):
        return pd.DataFrame(self.driver_history)
