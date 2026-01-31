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
        
        # Grid Meta-Data
        self.champions_set = set() # Set of drivers who have won a WDC *before* the current race
        
        # Historical Champion Tracking
        # Updated to include full history from 1950-2025 using Full Names
        # This aligns with the driver_name normalization which prefers accents/full names.
        
        self.wdc_history = {
            1950: "Giuseppe Farina", 1951: "Juan Manuel Fangio", 1952: "Alberto Ascari", 1953: "Alberto Ascari",
            1954: "Juan Manuel Fangio", 1955: "Juan Manuel Fangio", 1956: "Juan Manuel Fangio", 1957: "Juan Manuel Fangio",
            1958: "Mike Hawthorn", 1959: "Jack Brabham", 1960: "Jack Brabham", 1961: "Phil Hill",
            1962: "Graham Hill", 1963: "Jim Clark", 1964: "John Surtees", 1965: "Jim Clark",
            1966: "Jack Brabham", 1967: "Denny Hulme", 1968: "Graham Hill", 1969: "Jackie Stewart",
            1970: "Jochen Rindt", 1971: "Jackie Stewart", 1972: "Emerson Fittipaldi", 1973: "Jackie Stewart",
            1974: "Emerson Fittipaldi", 1975: "Niki Lauda", 1976: "James Hunt", 1977: "Niki Lauda",
            1978: "Mario Andretti", 1979: "Jody Scheckter", 1980: "Alan Jones", 1981: "Nelson Piquet",
            1982: "Keke Rosberg", 1983: "Nelson Piquet", 1984: "Niki Lauda", 1985: "Alain Prost",
            1986: "Alain Prost", 1987: "Nelson Piquet", 1988: "Ayrton Senna", 1989: "Alain Prost",
            1990: "Ayrton Senna", 1991: "Ayrton Senna", 1992: "Nigel Mansell", 1993: "Alain Prost",
            1994: "Michael Schumacher", 1995: "Michael Schumacher", 1996: "Damon Hill", 1997: "Jacques Villeneuve",
            1998: "Mika Häkkinen", 1999: "Mika Häkkinen", 2000: "Michael Schumacher", 2001: "Michael Schumacher",
            2002: "Michael Schumacher", 2003: "Michael Schumacher", 2004: "Michael Schumacher", 2005: "Fernando Alonso",
            2006: "Fernando Alonso", 2007: "Kimi Räikkönen", 2008: "Lewis Hamilton", 2009: "Jenson Button",
            2010: "Sebastian Vettel", 2011: "Sebastian Vettel", 2012: "Sebastian Vettel", 2013: "Sebastian Vettel",
            2014: "Lewis Hamilton", 2015: "Lewis Hamilton", 2016: "Nico Rosberg", 2017: "Lewis Hamilton",
            2018: "Lewis Hamilton", 2019: "Lewis Hamilton", 2020: "Lewis Hamilton", 2021: "Max Verstappen",
            2022: "Max Verstappen", 2023: "Max Verstappen", 2024: "Max Verstappen", 2025: "Lando Norris"
        }



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
        
        # Calculate Grid Competitiveness (Champion Density)
        # Count how many drivers in current race are in self.champions_set
        # We need to map driver names/codes. Assuming 'drivers' array contains compatible IDs.
        # Check against self.champions_set.
        # Note: self.champions_set needs to handle the ID format (TLA like 'HAM' or Name).
        # We'll try matching TLA first.
        
        active_champs = 0
        for d in drivers:
            if d in self.champions_set:
                active_champs += 1
                
        # Grid Multiplier: 5% boost per champion on grid
        # e.g. 2012 (6 champs) -> 1.3x multiplier
        prior_champs_bonus = 1.0 + (active_champs * 0.05)
        
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
                
                rating_a_eff = self.driver_ratings[d_a]
                rating_b_eff = self.driver_ratings[d_b]
                
                # Removed individual logic, focusing on competitiveness now.
                
                metric_a = rating_a_eff + self.gamma * self.constructor_ratings[c_a]
                metric_b = rating_b_eff + self.gamma * self.constructor_ratings[c_b]
                
                expected_a = self.get_expected_score(metric_a, metric_b)
                
                # ENHANCEMENT: "Upside Volatility"
                multiplier = 1.0
                if actual_score_a > expected_a: # A won/did better than expected
                    if expected_a < 0.3: # Less than 30% chance to win
                        # Giant Killing!
                        multiplier = 1.5
                
                # Teammate Battle Boost
                # User Request: "50% based on intra-team battles and 50% based on inter-team battles"
                # In a grid of N drivers, you have 1 teammate and (N-2) other opponents.
                # To make the teammate match equal in weight to the SUM of all other matches:
                # Weight_Teammate = Sum(Weight_Others)
                # Weight_Teammate = (N-2) * 1.0
                # So Multiplier = (n_drivers - 2).
                
                teammate_multiplier = 1.0
                if c_a == c_b:
                    # Dynamic balancing
                    if n_drivers > 2:
                        teammate_multiplier = float(n_drivers - 2)
                    else:
                        teammate_multiplier = 1.0 # 1v1 duel

                
                # Update
                # The K-factor is shared.
                # Global K * Grid Competitiveness * Teammate Boost * Volatility
                
                # SEASON LENGTH NORMALIZATION
                # User Request: "deal with... shorter with less races... inflated amount of recent years"
                # We normalize K based on a reference season length (e.g. 20 races).
                # If season has 16 races, each race is worth MORE (20/16 = 1.25x).
                # If season has 24 races, each race is worth LESS (20/24 = 0.83x).
                
                season_scaling = 1.0
                current_year = race_data['year'].iloc[0]
                if hasattr(self, 'races_per_season') and current_year in self.races_per_season:
                    n_races = self.races_per_season[current_year]
                    if n_races > 0:
                        season_scaling = 20.0 / n_races
                
                match_k = self.k_factor * prior_champs_bonus * teammate_multiplier * multiplier * season_scaling
                
                # Logic Verification:
                # 1. DNF (Mechanical) + BONUS logic
                #    BONUS: "give them more points because they could've finished higher"
                #    User requested "even more inflated".
                #    We apply a massive multiplier for Unlucky DNFs.
                
                mech_bonus = 1.0
                if d_a in is_mech_dnf and is_mech_dnf[i]: 
                     # User wants Ricciardo Top 3.
                     # We boost the update delta massively (5x).
                     # This treats a P1 Mechanical DNF as a Career Defining Performance.
                     mech_bonus = 5.0 
                     
                # 2. Car Outperformance (Relative to Teammate/Grid)
                #    Revised: Continuous "Carry" Bonus.
                #    If Driver > Car, they get a multiplier on positive results.
                #    Formula: Bonus = 1.0 + (Diff * 0.001) for Diff > 0.
                #    Example: Driver 1600, Car 1400. Diff=200. Bonus = 1.2x.
                #    This scales gracefully.
                
                style_bonus = 1.0
                rating_diff = self.driver_ratings[d_a] - self.constructor_ratings[c_a]
                
                if rating_diff > 0 and actual_score_a > 0.5:
                     # Only reward if they outperform AND get a result (Win/Draw)
                     # Cap at reasonable max (e.g. 1.5x for +500 gap)
                     raw_bonus = rating_diff * 0.001
                     style_bonus = 1.0 + min(0.5, raw_bonus)
                        
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
                        
                delta = match_k * mech_bonus * style_bonus * braking_bonus * (actual_score_a - expected_a)
                
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
        
        # TEAM SIZE CAP LOGIC
        # Rule: If a constructor has > 2 drivers, only the highest finisher (lowest effective_position)
        # is allowed to have a POSITIVE delta. Others are capped at max(delta, 0) -> No, min(delta, 0) -> No gain.
        
        # 1. Group by constructor to find team sizes and best finisher
        team_performances = defaultdict(list)
        for i, d in enumerate(drivers):
            constr = constructors[i]
            pos = positions[i] # effective_position
            team_performances[constr].append( (d, pos) )
            
        capped_drivers = set()
        for constr, members in team_performances.items():
            if len(members) > 2:
                # Large team!
                # Identify best finisher
                # Sort by position (ascending)
                members.sort(key=lambda x: x[1])
                best_driver = members[0][0]
                
                # All others are capped
                for m_driver, m_pos in members:
                    if m_driver != best_driver:
                        capped_drivers.add(m_driver)
                        
        # Apply accumulated deltas with clamping
        for d in drivers:
            delta = driver_deltas[d]
            
            # Apply Cap
            if d in capped_drivers and delta > 0:
                delta = 0.0 # Clamp to 0 if positive
                
            self.driver_ratings[d] += delta
            
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
        # Calculate Season Lengths for Normalization
        self.races_per_season = all_race_data.groupby('year')['round'].nunique().to_dict()
        
        # We need to process year-by-year to update Champions Set dynamically
        years = sorted(all_race_data['year'].unique())
        
        for year in years:
            # Get all races for this year
            year_data = all_race_data[all_race_data['year'] == year]
            grouped = year_data.groupby('round')
            sorted_rounds = sorted(grouped, key=lambda x: x[0])
            
            for rnd, race_df in sorted_rounds:
                self.update(race_df)
            
            # End of Year: Add new Champion to history
            # In real life, champ is decided when points impossible to catch.
            # Approximating: Add to set at end of season.
            if year in self.wdc_history:
                champ_code = self.wdc_history[year]
                # print(f"End of {year}: Crowning {champ_code}")
                # We need to handle Name vs Code matching.
                # Our manual set used Names for pre-1982. 
                # Our wdc_history uses TLA codes (e.g. "VER").
                # The `update` logic checks `d in self.champions_set`.
                # If race_data has "Max Verstappen" but we add "VER", it fails.
                # However, fastf1 `driver_name` is typically TLA in recent years? 
                # No, standard is usually "VER" in 'driver' column (TLA).
                # Wait, data_loader.py:
                # result['driver_name'] = driver['code'] if driver['code'] else driver['familyName']
                # So we are using TLA (3 letters) mostly.
                # Our Pre-1982 seeds were Full Names ("Niki Lauda").
                # We should update them to TLA codes if possible or support both.
                # For safety, I will add the code to the set.
                self.champions_set.add(champ_code)

    def get_history_df(self):
        return pd.DataFrame(self.driver_history)
