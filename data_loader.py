import fastf1
import pandas as pd
import numpy as np
import os
import logging
from typing import List, Dict, Optional, Tuple
from feature_engineering import calculate_pace_metrics, get_speed_trap_data, determine_mechanical_dnf, calculate_braking_aggression
import time
import requests
import random

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CACHE_DIR = os.path.join(os.getcwd(), 'fastf1_cache')

def setup_fastf1():
    """Configures FastF1 cache and settings."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    fastf1.Cache.enable_cache(CACHE_DIR)
    logger.info(f"FastF1 cache enabled at: {CACHE_DIR}")

def get_race_results(year: int) -> pd.DataFrame:
    """
    Fetches race results for a given year.
    Returns a DataFrame with columns: [round, race_name, date, driver, constructor, position, status, points]
    """
    try:
        # Add delay before fetching schedule to respect rate limits
        time.sleep(1.0) 
        schedule = fastf1.get_event_schedule(year)
    except Exception as e:
        logger.error(f"Failed to load schedule for {year}: {e}")
        return pd.DataFrame() # Return empty df on failure
        
    all_results = []
    
    # Filter for official races only
    races = schedule[schedule['EventFormat'] == 'conventional'] # Mostly conventional, handling sprints might be needed separately or treated as sub-events
    # Actually, let's just iterate all rounds that have a Race session
    
    for i, row in schedule.iterrows():
        # Skip testing or upcoming if not available
        try:
            # Check if event has happened
            if row['EventDate'] > pd.Timestamp.now():
                continue
                
            if row['EventDate'] > pd.Timestamp.now():
                continue

            # Retry logic for session loading
            max_retries = 5
            base_delay = 2.0
            session = None
            
            for attempt in range(max_retries):
                try:
                    # Small delay between races
                    time.sleep(1.5)
                    
                    session = fastf1.get_session(year, row['RoundNumber'], 'R')
                    # Load only laps (telemetry=False saves huge time/bandwidth)
                    # We only need lap times and SpeedST which are in Laps object
                    session.load(laps=True, telemetry=False, weather=False, messages=False)
                    break # Success
                except Exception as e:
                    if "429" in str(e) or "rate limit" in str(e).lower():
                        sleep_time = base_delay * (2 ** attempt) + random.uniform(0, 1)
                        logger.warning(f"Rate limit hit for {year} R{row['RoundNumber']}. Retrying in {sleep_time:.1f}s...")
                        time.sleep(sleep_time)
                    else:
                        logger.error(f"Error loading session {year} R{row['RoundNumber']}: {e}")
                        # For other errors, maybe skip?
                        # If it's a network error unrelated to 429, we might want to retry too.
                        # But for now, let's just log and continue/break if critical.
                        # If session failed to load, we can't proceed.
                        if attempt == max_retries - 1:
                            logger.error(f"Failed to load session after {max_retries} attempts.")
                        break

            if session is None or not hasattr(session, 'results'):
                continue
            
            results = session.results
            if results.empty:
                continue
                
            # We need laps for feature engineering later, but for now let's just get high level results
            # actually, maybe we should return a richer object or save per-race extraction
            
            # Get teammates map
            teammates = {}
            for drv in session.drivers:
                t = session.get_driver(drv)['TeamName']
                if t not in teammates:
                    teammates[t] = []
                teammates[t].append(drv)


            for drv in session.drivers:
                try:
                    drv_result = results.loc[drv]
                    driver_obj = session.get_driver(drv)
                    
                    # Basic info
                    status = drv_result['Status']
                    position = drv_result['Position']
                    classified_pos = drv_result['ClassifiedPosition'] # Official classification
                    grid = drv_result['GridPosition']
                    
                    # DNF Handling
                    is_mechanical_dnf = determine_mechanical_dnf(status)
                    effective_position = position
                    if is_mechanical_dnf:
                        # Constructive position at time of failure
                        # Optimization: Sometimes "lap times suddenly get a lot slower" before retirement.
                        # We should check max(1, dnf_pos) to ensure we don't accidentally get -1.
                        
                        dnf_pos = get_position_at_dnf(session, drv, status)
                        if dnf_pos > 0:
                            effective_position = dnf_pos
                        else:
                             # If we can't find exact pos, default to classified or 
                             # better yet, assuming they were likely verified as mechanical,
                             # we might assume they were doing okay? No, that's unsafe.
                             # But usually get_position_at_dnf works.
                             pass
                             
                        # Force update: If mechanical failure, assume they "beat" everyone below their failure point.
                        # This allows the model to treat P(DNF@P1) > P(P2 Finished).
                        pass
                        
                    # Features
                    teammate = None
                    team = driver_obj['TeamName']
                    if team in teammates:
                        for tm in teammates[team]:
                            if tm != drv:
                                teammate = tm
                                break
                    
                    # Calculate telemetry features if enough data
                    # Note: This is slow. For a full history run, it will take hours.
                    # We might want to safeguard or allow simplified mode.
                    # Given the "most accurate ever" request, we do it.
                    
                    pace_metrics = calculate_pace_metrics(session, drv, teammate)
                    max_speed = get_speed_trap_data(session, drv)
                    
                    # Append result
                    all_results.append({
                        'year': year,
                        'round': row['RoundNumber'],
                        'race_name': row['EventName'],
                        'date': row['EventDate'],
                        'driver_code': drv_result['Abbreviation'],
                        'driver_name': driver_obj['FullName'], # Use driver_obj for full name stability
                        'constructor': team,
                        'position': position,
                        'classified_position': classified_pos,
                        'grid': grid,
                        'status': status,
                        'points': drv_result['Points'],
                        'is_mechanical_dnf': is_mechanical_dnf,
                        'effective_position': effective_position,
                        'pace_delta': pace_metrics.get('pace_delta', 0.0), # vs session median (approx)
                        'pace_teammate_delta': pace_metrics.get('teammate_delta', 0.0),
                        'consistency': pace_metrics.get('consistency', 0.0),
                        'max_speed': max_speed
                    })
                except Exception as e:
                    logger.warning(f"Skipping driver {drv} in {year} R{row['RoundNumber']}: {e}")

        except Exception as e:
            logger.error(f"Error loading {year} round {row['RoundNumber']}: {e}")
            
    return pd.DataFrame(all_results)

def get_position_at_dnf(session, driver_code, status):
    """
    Finds the position of the driver at the moment of failure using telemetry/laps.
    Logic:
    1. Look at laps.
    2. If last lap is extremely slow (>110% of median), it's likely the failure lap.
    3. We want the position they were in *before* that failure.
    4. If last lap is normal (instant failure), use position of that lap.
    """
    try:
        laps = session.laps.pick_driver(driver_code)
        if laps.empty:
            return 0
            
        # Filter valid laps
        clean_laps = laps.pick_quicklaps()
        if clean_laps.empty:
            return 0
            
        median_pace = clean_laps['LapTime'].median()
        last_lap = laps.iloc[-1]
        
        # Check if last lap was "The Failure" (slow)
        # Using 1.15 threshold (15% slower)
        is_slow_failure = False
        if not pd.isnull(last_lap['LapTime']) and last_lap['LapTime'] > median_pace * 1.15:
            is_slow_failure = True
            
        # Target lap index
        # If slow failure, we want the lap BEFORE this one.
        # If sudden failure (crash/instant engine off), we want THIS lap's position (or previous if incomplete).
        
        # 'LapNumber' is 1-indexed.
        dnf_lap_number = int(last_lap['LapNumber'])
        
        if is_slow_failure:
            target_lap = dnf_lap_number - 1
        else:
            target_lap = dnf_lap_number
            
        if target_lap < 1:
            return 0 # Failed on lap 1
            
        # Find position at that lap
        # We need to know where everyone was at 'target_lap'
        # This is expensive to do for everyone.
        # Approximation: Use 'Position' column if available in Laps?
        # FastF1 Laps data usually contains 'Position' at end of lap.
        
        if 'Position' in laps.columns:
            # Get position at target lap
            pos_rec = laps[laps['LapNumber'] == target_lap]
            if not pos_rec.empty:
                return int(pos_rec.iloc[0]['Position'])
                
        # Fallback to driver result position if valid
        return 0
        
    except Exception as e:
        logger.warning(f"Could not determine DNF pos for {driver_code}: {e}")
        return 0

def get_all_seasons_data(start_year: int, end_year: int) -> pd.DataFrame:
    """Loads and aggregates data from multiple seasons."""
    setup_fastf1()
    all_seasons = []
    current_year = pd.Timestamp.now().year
    
    for year in range(start_year, end_year + 1):
        if year > current_year:
            break
        
        # Add significant delay between seasons
        logger.info(f"Processing season {year}...")
        time.sleep(2.0)
        
        df = get_race_results(year)
        if not df.empty:
            all_seasons.append(df)
            
    if not all_seasons:
        return pd.DataFrame()
        
    return pd.concat(all_seasons, ignore_index=True)

if __name__ == "__main__":
    # Test run
    setup_fastf1()
    # Loading just one recent race to verify
    try:
        session = fastf1.get_session(2024, 1, 'R')
        session.load(laps=False, telemetry=False)
        print(f"Successfully loaded {session.event['EventName']}")
    except Exception as e:
        print(f"Failed setup test: {e}")
