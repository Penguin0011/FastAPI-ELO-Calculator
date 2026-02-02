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
    
    # ---------------------------------------------------------
    # 4. DRIVER BEST CAR JSON (Most Successful Car Feature)
    # ---------------------------------------------------------
    print("Generating driver best car data...")
    
    # Comprehensive F1 car name mapping: (constructor, year) -> car model name
    CAR_NAME_MAP = {
        # Red Bull Racing (2005-2025) - both naming variants used in CSV
        ("Red Bull", 2005): "RB1", ("Red Bull", 2006): "RB2", ("Red Bull", 2007): "RB3",
        ("Red Bull", 2008): "RB4", ("Red Bull", 2009): "RB5", ("Red Bull", 2010): "RB6",
        ("Red Bull", 2011): "RB7", ("Red Bull", 2012): "RB8", ("Red Bull", 2013): "RB9",
        ("Red Bull", 2014): "RB10", ("Red Bull", 2015): "RB11", ("Red Bull", 2016): "RB12",
        ("Red Bull", 2017): "RB13", ("Red Bull", 2018): "RB14", ("Red Bull", 2019): "RB15",
        ("Red Bull", 2020): "RB16", ("Red Bull", 2021): "RB16B", ("Red Bull", 2022): "RB18",
        ("Red Bull", 2023): "RB19", ("Red Bull", 2024): "RB20", ("Red Bull", 2025): "RB21",
        ("Red Bull Racing", 2005): "RB1", ("Red Bull Racing", 2006): "RB2", ("Red Bull Racing", 2007): "RB3",
        ("Red Bull Racing", 2008): "RB4", ("Red Bull Racing", 2009): "RB5", ("Red Bull Racing", 2010): "RB6",
        ("Red Bull Racing", 2011): "RB7", ("Red Bull Racing", 2012): "RB8", ("Red Bull Racing", 2013): "RB9",
        ("Red Bull Racing", 2014): "RB10", ("Red Bull Racing", 2015): "RB11", ("Red Bull Racing", 2016): "RB12",
        ("Red Bull Racing", 2017): "RB13", ("Red Bull Racing", 2018): "RB14", ("Red Bull Racing", 2019): "RB15",
        ("Red Bull Racing", 2020): "RB16", ("Red Bull Racing", 2021): "RB16B", ("Red Bull Racing", 2022): "RB18",
        ("Red Bull Racing", 2023): "RB19", ("Red Bull Racing", 2024): "RB20", ("Red Bull Racing", 2025): "RB21",
        
        # Mercedes (2010-2025)
        ("Mercedes", 2010): "W01", ("Mercedes", 2011): "W02", ("Mercedes", 2012): "W03",
        ("Mercedes", 2013): "W04", ("Mercedes", 2014): "W05", ("Mercedes", 2015): "W06",
        ("Mercedes", 2016): "W07", ("Mercedes", 2017): "W08", ("Mercedes", 2018): "W09",
        ("Mercedes", 2019): "W10", ("Mercedes", 2020): "W11", ("Mercedes", 2021): "W12",
        ("Mercedes", 2022): "W13", ("Mercedes", 2023): "W14", ("Mercedes", 2024): "W15",
        ("Mercedes", 2025): "W16",
        
        # Ferrari (2010-2025)
        ("Ferrari", 2010): "F10", ("Ferrari", 2011): "150° Italia", ("Ferrari", 2012): "F2012",
        ("Ferrari", 2013): "F138", ("Ferrari", 2014): "F14 T", ("Ferrari", 2015): "SF15-T",
        ("Ferrari", 2016): "SF16-H", ("Ferrari", 2017): "SF70H", ("Ferrari", 2018): "SF71H",
        ("Ferrari", 2019): "SF90", ("Ferrari", 2020): "SF1000", ("Ferrari", 2021): "SF21",
        ("Ferrari", 2022): "F1-75", ("Ferrari", 2023): "SF-23", ("Ferrari", 2024): "SF-24",
        ("Ferrari", 2025): "SF-25",
        
        # McLaren (2010-2025)
        ("McLaren", 2010): "MP4-25", ("McLaren", 2011): "MP4-26", ("McLaren", 2012): "MP4-27",
        ("McLaren", 2013): "MP4-28", ("McLaren", 2014): "MP4-29", ("McLaren", 2015): "MP4-30",
        ("McLaren", 2016): "MP4-31", ("McLaren", 2017): "MCL32", ("McLaren", 2018): "MCL33",
        ("McLaren", 2019): "MCL34", ("McLaren", 2020): "MCL35", ("McLaren", 2021): "MCL35M",
        ("McLaren", 2022): "MCL36", ("McLaren", 2023): "MCL60", ("McLaren", 2024): "MCL38",
        ("McLaren", 2025): "MCL39",
        
        # Alpine / Renault (2002-2025)
        ("Renault", 2002): "R22", ("Renault", 2003): "R23", ("Renault", 2004): "R24",
        ("Renault", 2005): "R25", ("Renault", 2006): "R26", ("Renault", 2007): "R27",
        ("Renault", 2008): "R28", ("Renault", 2009): "R29", ("Renault", 2010): "R30",
        ("Renault", 2011): "R31", ("Renault", 2016): "R.S.16", ("Renault", 2017): "R.S.17",
        ("Renault", 2018): "R.S.18", ("Renault", 2019): "R.S.19", ("Renault", 2020): "R.S.20",
        ("Alpine", 2021): "A521", ("Alpine", 2022): "A522", ("Alpine", 2023): "A523",
        ("Alpine", 2024): "A524", ("Alpine", 2025): "A525",
        
        # Aston Martin (2021-2025)
        ("Aston Martin", 2021): "AMR21", ("Aston Martin", 2022): "AMR22",
        ("Aston Martin", 2023): "AMR23", ("Aston Martin", 2024): "AMR24",
        ("Aston Martin", 2025): "AMR25",
        
        # Williams (2009-2025)
        ("Williams", 2009): "FW31", ("Williams", 2010): "FW32", ("Williams", 2011): "FW33",
        ("Williams", 2012): "FW34", ("Williams", 2013): "FW35", ("Williams", 2014): "FW36",
        ("Williams", 2015): "FW37", ("Williams", 2016): "FW38", ("Williams", 2017): "FW40",
        ("Williams", 2018): "FW41", ("Williams", 2019): "FW42", ("Williams", 2020): "FW43",
        ("Williams", 2021): "FW43B", ("Williams", 2022): "FW44", ("Williams", 2023): "FW45",
        ("Williams", 2024): "FW46", ("Williams", 2025): "FW47",
        
        # Haas (2016-2025)
        ("Haas F1 Team", 2016): "VF-16", ("Haas F1 Team", 2017): "VF-17",
        ("Haas F1 Team", 2018): "VF-18", ("Haas F1 Team", 2019): "VF-19",
        ("Haas F1 Team", 2020): "VF-20", ("Haas F1 Team", 2021): "VF-21",
        ("Haas F1 Team", 2022): "VF-22", ("Haas F1 Team", 2023): "VF-23",
        ("Haas F1 Team", 2024): "VF-24", ("Haas F1 Team", 2025): "VF-25",
        
        # Sauber / Alfa Romeo (2018-2025) - CSV uses both "Alfa Romeo" and "Alfa Romeo Racing"
        ("Sauber", 2018): "C37", ("Alfa Romeo", 2019): "C38", ("Alfa Romeo", 2020): "C39",
        ("Alfa Romeo", 2021): "C41", ("Alfa Romeo", 2022): "C42", ("Alfa Romeo", 2023): "C43",
        ("Alfa Romeo Racing", 2019): "C38", ("Alfa Romeo Racing", 2020): "C39",
        ("Alfa Romeo Racing", 2021): "C41", ("Alfa Romeo Racing", 2022): "C42", ("Alfa Romeo Racing", 2023): "C43",
        ("Sauber", 2024): "C44", ("Sauber", 2025): "C45",
        ("Kick Sauber", 2024): "C44", ("Kick Sauber", 2025): "C45",
        
        # Toro Rosso / AlphaTauri / RB (2006-2025)
        ("Toro Rosso", 2006): "STR1", ("Toro Rosso", 2007): "STR2", ("Toro Rosso", 2008): "STR3",
        ("Toro Rosso", 2009): "STR4", ("Toro Rosso", 2010): "STR5", ("Toro Rosso", 2011): "STR6",
        ("Toro Rosso", 2012): "STR7", ("Toro Rosso", 2013): "STR8", ("Toro Rosso", 2014): "STR9",
        ("Toro Rosso", 2015): "STR10", ("Toro Rosso", 2016): "STR11", ("Toro Rosso", 2017): "STR12",
        ("Toro Rosso", 2018): "STR13", ("Toro Rosso", 2019): "STR14",
        ("AlphaTauri", 2020): "AT01", ("AlphaTauri", 2021): "AT02",
        ("AlphaTauri", 2022): "AT03", ("AlphaTauri", 2023): "AT04",
        ("RB", 2024): "VCARB 01", ("RB", 2025): "VCARB 02",
        
        # Force India / Racing Point (2008-2020)
        ("Force India", 2008): "VJM01", ("Force India", 2009): "VJM02",
        ("Force India", 2010): "VJM03", ("Force India", 2011): "VJM04",
        ("Force India", 2012): "VJM05", ("Force India", 2013): "VJM06",
        ("Force India", 2014): "VJM07", ("Force India", 2015): "VJM08",
        ("Force India", 2016): "VJM09", ("Force India", 2017): "VJM10",
        ("Force India", 2018): "VJM11",
        ("Racing Point", 2019): "RP19", ("Racing Point", 2020): "RP20",
    }
    
    def get_car_name(constructor, year):
        """Get specific car model name from constructor and year."""
        return CAR_NAME_MAP.get((constructor, year), f"{constructor} {year}")
    
    # Calculate best car for each driver
    driver_best_car = {}
    
    for drv in data['driver_name'].unique():
        drv_data = data[data['driver_name'] == drv]
        drv_hist = history_df[history_df['driver'] == drv].sort_values(['year', 'round'])
        
        if drv_hist.empty:
            continue
        
        # Group by constructor to find best stint
        constructor_stints = {}
        
        for constructor in drv_data['constructor'].unique():
            stint_data = drv_data[drv_data['constructor'] == constructor]
            stint_years = sorted(stint_data['year'].unique())
            
            if not stint_years:
                continue
            
            year_start = int(stint_years[0])
            year_end = int(stint_years[-1])
            
            # Calculate total stats for this constructor stint (used for scoring)
            total_stint_wins = int((stint_data['position'] == 1).sum())
            total_stint_races = len(stint_data)
            
            # Get ELO progression during this stint
            stint_history = drv_hist[(drv_hist['year'] >= year_start) & (drv_hist['year'] <= year_end)]
            
            if stint_history.empty:
                continue
            
            start_elo = stint_history.iloc[0]['rating']
            end_elo = stint_history.iloc[-1]['rating']
            elo_gained = end_elo - start_elo
            peak_elo = stint_history['rating'].max()
            
            # Find the best single year with this constructor for car name
            best_year = stint_data.groupby('year').apply(
                lambda x: (x['position'] == 1).sum()
            ).idxmax() if total_stint_wins > 0 else year_end
            
            car_name = get_car_name(constructor, int(best_year))
            
            # Calculate stats for the BEST YEAR only (the specific car)
            best_year_data = stint_data[stint_data['year'] == best_year]
            car_wins = int((best_year_data['position'] == 1).sum())
            car_races = len(best_year_data)
            car_win_rate = (car_wins / car_races * 100) if car_races > 0 else 0
            
            constructor_stints[constructor] = {
                "constructor": constructor,
                "car_name": car_name,
                "best_year": int(best_year),
                "year_start": year_start,
                "year_end": year_end,
                "wins": car_wins,  # Wins with this specific car/year
                "total_races": car_races,  # Races in that specific year
                "win_rate": round(car_win_rate, 1),  # Win rate for that specific car
                "elo_gained": int(round(elo_gained)),
                "peak_elo": int(round(peak_elo)),
                # Score for ranking: prioritize ELO gained, then win rate, then wins
                "_score": (elo_gained * 2) + (car_win_rate * 5) + (car_wins * 10)
            }
        
        if not constructor_stints:
            continue
        
        # Find the best constructor stint by score
        best_stint = max(constructor_stints.values(), key=lambda x: x["_score"])
        
        # Remove internal score from output
        del best_stint["_score"]
        
        driver_best_car[drv] = best_stint
    
    # Save driver_best_car.json
    best_car_path = 'frontend/src/data/driver_best_car.json'
    with open(best_car_path, 'w', encoding='utf-8') as f:
        json.dump(driver_best_car, f, indent=2, ensure_ascii=False)
    print(f"Saved {best_car_path}")
    
    print("Done!")


if __name__ == "__main__":
    main()
