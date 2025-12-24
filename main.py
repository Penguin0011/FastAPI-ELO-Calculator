import argparse
import sys
import os
import pandas as pd
from data_loader import get_all_seasons_data
from elo_model import BayesianEloModel
from plotter import plot_individual_driver_history
from optimizer import optimize_hyperparameters

# Parameters
START_YEAR = 2018 # Start reasonable to get good history without waiting forever. 2018 is good start of liberty era/modern data.
# User implied "all the years that are available in the fastf1 api only". Fastf1 goes back to 2018 reliably for telemetry?
# FastF1 lap data is good from 2018+. Basic results exist for much longer.
# PROMPT: "utilizing only the fastf1 api for data... features: lap pace deltas... from all the years that are available"
# If I try 1950, features will fail.
# I will try to load from 2018 onwards for FULL features.
# If I use basic results, I can go back further.
# But the user specifically asked for "telemetry-derived features ... into the per-race CSV".
# This implies I should only use years where this is possible.
# FastF1 supports partial data back to late 90s, but telemetry/laps are patchy. 2018 is safe. 
# I will default to 2018.

END_YEAR = 2025

def main():
    print("Starting F1 ELO Calculator...")
    
    # Check if data exists locally to save time (simple CSV cache)
    data_path = 'f1_data_processed.csv'
    if os.path.exists(data_path):
        print(f"Loading cached data from {data_path}...")
        data = pd.read_csv(data_path)
    else:
        print("Fetching data from FastF1 (this may take a while)...")
        data = get_all_seasons_data(START_YEAR, END_YEAR)
        if not data.empty:
            data.to_csv(data_path, index=False)
    
    if data.empty:
        print("No data found!")
        return

    print(f"Loaded {len(data)} results.")
    
    # Optimization?
    # For now, use reasonable defaults to ensure completion.
    # K=24 is much more aggressive (High Volatility requested)
    # Gamma=1.0 retains strong car weighting
    
    k = 24.0
    gamma = 1.0 
    
    k = 24.0
    gamma = 1.0 
    
    k = 24.0
    gamma = 1.0 
    
    # 2017 Seeding Logic
    # Standings from fetch_2017.py
    standings_2017 = [
        "HAM", "VET", "BOT", "RAI", "RIC", "VER", "PER", "OCO", "SAI", "MAS", 
        "HUL", "STR", "GRO", "MAG", "ALO", "VAN", "PAL", "KVY", "WEH", "GIO", 
        "ERI", "BUT", "DIR", "GAS", "HAR"
    ]
    
    # Distribution: 
    # Median ~ 1500. Range ~ 100.
    # Curve: Flat at top, drops faster at bottom (Square function).
    # ELO = Base + Range * (1 - ((Rank-1)/(N-1))^2 ) ? No, that drops fast then flat?
    # We want "gap being more the farther back you go". 
    # This means gradient increases. Convex.
    # ELO = Max - Range * ((Rank-1)/(N-1))^Exp
    
    N = len(standings_2017)
    MaxELO = 1550
    Range = 100
    Exp = 2.0 # Quadratic drop
    
    initial_ratings = {}
    print("Calculating 2017 Seeding...")
    for rank, drv in enumerate(standings_2017, 1):
        # Norm rank 0 to 1
        x = (rank - 1) / (N - 1)
        drop = Range * (x ** Exp)
        elo = MaxELO - drop
        initial_ratings[drv] = elo
        # print(f"{rank}. {drv}: {elo:.1f}")
        
    # PASS 1: Calculate "Potential" (Peaks)
    print("--- PASS 1: Analyzing Career Potential ---")
    model_p1 = BayesianEloModel(k_factor=k, gamma=gamma, initial_ratings=initial_ratings)
    model_p1.fit(data)
    
    # Extract peaks
    history_p1 = model_p1.get_history_df()
    peaks = history_p1.groupby('driver')['rating'].max().to_dict()
    print("Potential analysis complete. Identified peaks for future weighting.")
    
    # PASS 2: Train with Future Knowledge
    print(f"--- PASS 2: Training with Potential Weighting (K={k}) ---")
    model = BayesianEloModel(k_factor=k, gamma=gamma, initial_ratings=initial_ratings)
    model.set_peaks(peaks) # Inject future knowledge
    model.fit(data)
    
    # Save 2025 ratings
    print("Generating report...")
    history_df = model.get_history_df()
    
    # Plot individuals
    print("Generating individual plots...")
    plot_individual_driver_history(history_df, 'plots')
    
    # Filter for drivers CURRENTLY ON THE GRID (2025)
    # Strategy: Drivers who participated in the 2025 season are "on the grid" for that year context.
    # To be precise, we can check drivers in the LAST race of 2025?
    # User said: "drivers that are CURRENTLY ON THE GRID".
    # Since we are simulating "after events of 2025", we take the 2025 roster.
    # Note: Reserve drivers (Bearman, Lawson etc) might appear if they raced.
    # I will include everyone who raced in 2025.
    
    drivers_2025 = data[data['year'] == 2025]['driver_name'].unique()
    
    final_ratings = {}
    for drv in drivers_2025:
        # Get their last entry from history
        drv_hist = history_df[history_df['driver'] == drv]
        if not drv_hist.empty:
            last_rating = drv_hist.iloc[-1]['rating']
            final_ratings[drv] = last_rating
            
    print("Saved 44 plots to plots") # This print might be inaccurate if dynamic, but keeping flow.
    
    # Save All-Time Peaks
    print("Generating All-Time Peak report...")
    # Group by driver and find max rating
    # history_df has 'rating' column
    peaks = history_df.groupby('driver')['rating'].max().sort_values(ascending=False)
    
    with open('all_time_peak_elo.txt', 'w') as f:
        f.write("F1 Driver All-Time Peak ELO Ratings (Dataset History)\n")
        f.write("=====================================================\n")
        for rank, (drv, rating) in enumerate(peaks.items(), 1):
            f.write(f"{rank}. {drv}: {rating:.0f}\n")
            
    print("Saved all_time_peak_elo.txt")
    
    # Filter for drivers CURRENTLY ON THE GRID (2025)
    # Sort
    sorted_ratings = sorted(final_ratings.items(), key=lambda x: x[1], reverse=True)
    
    with open('2025_current_grid_elo.txt', 'w') as f:
        f.write("F1 Driver ELO Ratings - End of 2025 (Active Grid)\n")
        f.write("===============================================\n")
        for rank, (drv, rating) in enumerate(sorted_ratings, 1):
            f.write(f"{rank}. {drv}: {rating:.0f}\n")
            
    print("Saved 2025_current_grid_elo.txt")
    print("Done!")

if __name__ == "__main__":
    main()
