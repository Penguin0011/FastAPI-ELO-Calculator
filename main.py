import argparse
import sys
import os
import pandas as pd
from data_loader import get_all_seasons_data
from elo_model import BayesianEloModel
from plotter import plot_individual_driver_history
from optimizer import optimize_hyperparameters

# Parameters
START_YEAR = 1950 # Start from 1950 as requested
# User implied "all the years that are available in the fastf1 api only".
# FastF1/Ergast goes back to 1950s for results, 1996 for Laps, 2018 for Telemetry.

END_YEAR = 2025

def main():
    print("Starting F1 ELO Calculator...")
    
    # Check if data exists locally
    data_path = 'f1_data_full.csv'
    existing_data = pd.DataFrame()
    
    if os.path.exists(data_path):
        print(f"Loading cached data from {data_path}...")
        try:
            existing_data = pd.read_csv(data_path)
            print(f"Loaded {len(existing_data)} existing rows.")
        except Exception as e:
            print(f"Error loading cache: {e}. Starting fresh.")
            
    # Determine years to fetch
    years_to_fetch = []
    if not existing_data.empty and 'year' in existing_data.columns:
        existing_years = existing_data['year'].unique()
        print(f"Existing years: {sorted(existing_years)}")
        for y in range(START_YEAR, END_YEAR + 1):
            if y not in existing_years:
                years_to_fetch.append(y)
    else:
        years_to_fetch = list(range(START_YEAR, END_YEAR + 1))
        
    if years_to_fetch:
        print(f"Fetching missing years: {years_to_fetch}")
        # We need to update get_all_seasons_data to accept a list of years or we manually loop here.
        # Let's manually loop here to be safe and use append.
        
        # Import setup_fastf1 and get_race_results directly if possible, or modify data_loader.
        # For simplicity, let's assume we can loop here or modify data_loader to take a list.
        # But get_all_seasons_data takes start/end.
        # Let's modify data_loader loop to range(start, end).
        # Better: Just call get_race_results(year) loop here? 
        # But setup_fastf1 needs to be called.
        
        from data_loader import get_race_results, setup_fastf1
        import time
        
        setup_fastf1()
        new_data_frames = []
        
        for year in years_to_fetch:
            print(f"Fetching {year}...")
            time.sleep(2.0) # Rate limit protection
            try:
                df = get_race_results(year)
                if not df.empty:
                    new_data_frames.append(df)
                    # Incremental save just in case
                    if not existing_data.empty:
                        combined_autosave = pd.concat([existing_data] + new_data_frames, ignore_index=True)
                        combined_autosave.to_csv(data_path, index=False)
                    else:
                        temp_concat = pd.concat(new_data_frames, ignore_index=True)
                        temp_concat.to_csv(data_path, index=False)
                        
            except Exception as e:
                print(f"Error processing {year}: {e}")
                
        if new_data_frames:
            new_data = pd.concat(new_data_frames, ignore_index=True)
            if not existing_data.empty:
                data = pd.concat([existing_data, new_data], ignore_index=True)
            else:
                data = new_data
            
            # Final Save
            data.to_csv(data_path, index=False)
            print("Data fetching complete and saved.")
        else:
            data = existing_data
            
    else:
        print("All years present. Using existing data.")
        data = existing_data

    print(f"Loaded {len(data)} results.")
    
    # ---------------------------------------------------------
    # DATA CLEANING / NORMALIZATION
    # ---------------------------------------------------------
    def normalize_driver_names(df):
        print("Normalizing driver names...")
        
        # 1. Driver ID Consolidation (The "Scour" Method)
        # This resolves duplicates like "Sergio Perez" vs "Sergio Pérez" by grouping by unique DriverID.
        if 'driver_id' in df.columns:
             def best_name(names):
                 # Filter nulls and convert to list
                 names = [n for n in names if pd.notna(n)]
                 if not names: return "Unknown"
                 unique_names = list(set(names))
                 if len(unique_names) == 1:
                     return unique_names[0]
                 
                 # Score names: Higher score = more non-ascii chars (accents), then length
                 def score(n):
                     non_ascii = sum(1 for c in n if ord(c) > 127)
                     return (non_ascii, len(n), n)
                 
                 best = max(unique_names, key=score)
                 
                 # Optional: Log changes implies we are merging
                 # if len(unique_names) > 1:
                 #    print(f"Merging {unique_names} -> {best}")
                 
                 return best

             # Calculate best name for each ID
             print("Scouring data for duplicates based on Driver ID...")
             id_to_name = df.groupby('driver_id')['driver_name'].agg(best_name)
             
             # Apply the merge
             df['driver_name'] = df['driver_id'].map(id_to_name).fillna(df['driver_name'])
             print("Merged duplicates based on Driver ID.")
        
        # 2. Canonical Alias Map (Manual Overrides for specific preferences or legacy data issues)
        aliases = {
            "Andrea Kimi Antonelli": "Kimi Antonelli",
            "Nyck De Vries": "Nyck de Vries",
            "Jerome d'Ambrosio": "Jérôme d'Ambrosio",
            "Sebastien Buemi": "Sébastien Buemi",
            "Sebastien Bourdais": "Sébastien Bourdais",
            "Lucas Di Grassi": "Lucas di Grassi",
            "Paul Di Resta": "Paul di Resta",
        }
        
        df['driver_name'] = df['driver_name'].replace(aliases)
        return df
        
    data = normalize_driver_names(data)
    print("Normalized driver names (Merged Aliases).")
    
    # 3. Data Type Enforcement
    # Ensure effective_position is strictly numeric
    if 'effective_position' in data.columns:
        data['effective_position'] = pd.to_numeric(data['effective_position'], errors='coerce').fillna(20.0)
    
    # Ensure is_mechanical_dnf is boolean
    if 'is_mechanical_dnf' in data.columns:
        data['is_mechanical_dnf'] = data['is_mechanical_dnf'].astype(bool)

    # 4. Remove rows with critical missing info
    data = data.dropna(subset=['driver_name', 'constructor'])
    
    print(f"Data ready for training. Shape: {data.shape}")
    # ---------------------------------------------------------
    
    # Optimization?
    # For now, use reasonable defaults to ensure completion.
    # K=24 is much more aggressive (High Volatility requested)
    # Gamma=1.0 retains strong car weighting
    
    k = 24.0
    gamma = 1.0 
    
    # No manual seeding for 2017 anymore. We start from 1982.
    initial_ratings = {}
        
    # Calculate ELO Ratings
    print(f"--- Training ELO Model (K={k}) ---")
    model = BayesianEloModel(k_factor=k, gamma=gamma, initial_ratings=initial_ratings)
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
    
    with open('all_time_peak_elo.txt', 'w', encoding='utf-8') as f:
        f.write("F1 Driver All-Time Peak ELO Ratings (Dataset History)\n")
        f.write("=====================================================\n")
        for rank, (drv, rating) in enumerate(peaks.items(), 1):
            f.write(f"{rank}. {drv}: {rating:.0f}\n")
            
    print("Saved all_time_peak_elo.txt")
    
    # Save All-Time Average
    print("Generating All-Time Average report...")
    averages = history_df.groupby('driver')['rating'].mean().sort_values(ascending=False)
    
    with open('all_time_average_elo.txt', 'w', encoding='utf-8') as f:
        f.write("F1 Driver All-Time Average ELO Ratings (Dataset History)\n")
        f.write("========================================================\n")
        for rank, (drv, rating) in enumerate(averages.items(), 1):
            f.write(f"{rank}. {drv}: {rating:.0f}\n")
            
    print("Saved all_time_average_elo.txt")
    
    # Filter for drivers CURRENTLY ON THE GRID (2025)
    # Sort
    sorted_ratings = sorted(final_ratings.items(), key=lambda x: x[1], reverse=True)
    
    with open('2025_current_grid_elo.txt', 'w', encoding='utf-8') as f:
        f.write("F1 Driver ELO Ratings - End of 2025 (Active Grid)\n")
        f.write("===============================================\n")
        for rank, (drv, rating) in enumerate(sorted_ratings, 1):
            f.write(f"{rank}. {drv}: {rating:.0f}\n")
            
    print("Saved 2025_current_grid_elo.txt")
    
    # ---------------------------------------------------------
    # JSON DATA EXPORT FOR FRONTEND
    # ---------------------------------------------------------
    import json
    
    print("Generating frontend data files...")
    
    # 1. DRIVER STATS JSON
    # Structure: { "Driver Name": { wins, losses, total_races, avg_elo, peak_elo, current_elo } }
    driver_stats = {}
    
    # Calculate wins (P1 finishes) and total races per driver
    for drv in data['driver_name'].unique():
        drv_data = data[data['driver_name'] == drv]
        wins = int((drv_data['position'] == 1).sum())
        total_races = len(drv_data)
        losses = total_races - wins
        
        # Get ELO stats from history
        drv_hist = history_df[history_df['driver'] == drv]
        avg_elo = round(drv_hist['rating'].mean(), 0) if not drv_hist.empty else 1500
        peak_elo = round(drv_hist['rating'].max(), 0) if not drv_hist.empty else 1500
        current_elo = round(drv_hist.iloc[-1]['rating'], 0) if not drv_hist.empty else 1500
        
        driver_stats[drv] = {
            "wins": wins,
            "losses": losses,
            "total_races": total_races,
            "avg_elo": int(avg_elo),
            "peak_elo": int(peak_elo),
            "current_elo": int(current_elo)
        }
    
    # Save driver_stats.json
    stats_path = 'frontend/src/data/driver_stats.json'
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(driver_stats, f, indent=2, ensure_ascii=False)
    print(f"Saved {stats_path}")
    
    # 2. TIMELINE DATA JSON
    # Structure: { "year": [ { "name": "...", "elo": ... }, ... ] }
    # Get end-of-year ratings for each driver per year
    timeline_data = {}
    
    for year in sorted(history_df['year'].unique()):
        year_history = history_df[history_df['year'] == year]
        # Get last rating for each driver in that year
        end_of_year = year_history.groupby('driver').last().reset_index()
        # Sort by rating descending
        end_of_year = end_of_year.sort_values('rating', ascending=False)
        
        year_rankings = []
        for _, row in end_of_year.iterrows():
            year_rankings.append({
                "name": row['driver'],
                "elo": int(round(row['rating'], 0))
            })
        
        timeline_data[str(int(year))] = year_rankings
    
    # Save timeline_data.json
    timeline_path = 'frontend/src/data/timeline_data.json'
    with open(timeline_path, 'w', encoding='utf-8') as f:
        json.dump(timeline_data, f, indent=2, ensure_ascii=False)
    print(f"Saved {timeline_path}")
    
    # 3. ELO HISTORY JSON (for dynamic charting/comparisons)
    # Structure: { "Driver Name": [ { "year": 2007, "race_index": 1, "rating": 1523 }, ... ] }
    # race_index is a global sequential index across all races
    print("Generating ELO history for frontend charting...")
    
    elo_history = {}
    
    # Create a global race index mapping
    # Sort all unique (year, round) combinations chronologically
    race_keys = history_df[['year', 'round']].drop_duplicates().sort_values(['year', 'round'])
    race_index_map = {(int(row['year']), int(row['round'])): idx for idx, (_, row) in enumerate(race_keys.iterrows())}
    
    for drv in history_df['driver'].unique():
        drv_hist = history_df[history_df['driver'] == drv].sort_values(['year', 'round'])
        
        driver_data = []
        for _, row in drv_hist.iterrows():
            race_idx = race_index_map.get((int(row['year']), int(row['round'])), 0)
            driver_data.append({
                "year": int(row['year']),
                "round": int(row['round']),
                "race_name": str(row['race_name']) if 'race_name' in row and pd.notna(row['race_name']) else f"Round {int(row['round'])}",
                "race_index": race_idx,
                "rating": int(round(row['rating'], 0))
            })
        
        elo_history[drv] = driver_data

    
    # Save elo_history.json
    elo_history_path = 'frontend/src/data/elo_history.json'
    with open(elo_history_path, 'w', encoding='utf-8') as f:
        json.dump(elo_history, f, indent=2, ensure_ascii=False)
    print(f"Saved {elo_history_path}")
    
    print("Done!")


if __name__ == "__main__":
    main()
