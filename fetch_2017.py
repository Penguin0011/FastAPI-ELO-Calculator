import fastf1
import pandas as pd

def get_2017_standings():
    fastf1.Cache.enable_cache('fastf1_cache')
    print("Fetching 2017 Calendar...")
    schedule = fastf1.get_event_schedule(2017)
    
    driver_points = {}
    
    # We can iterate races, but that takes time.
    # Faster: Get the LAST race of 2017 and check "SeasonStandings" if available?
    # FastF1 session results often have 'Points' for the race, not season.
    # However, `session.results` has `GridPosition`, `Position`, `Points`.
    
    # Let's simple iterate. 20 races roughly.
    races = schedule[schedule['EventFormat'] == 'conventional'] # Skip unknown?
    
    print(f"Processing {len(races)} races...")
    
    for i, race in races.iterrows():
        try:
            session = fastf1.get_session(2017, race['RoundNumber'], 'R')
            session.load(laps=False, telemetry=False, messages=False, weather=False)
            results = session.results
            
            for _, row in results.iterrows():
                driver = row['Abbreviation'] # Use Code like 'HAM', 'VET'
                points = row['Points']
                driver_points[driver] = driver_points.get(driver, 0) + points
        except Exception as e:
            print(f"Skipping round {race['RoundNumber']}: {e}")
            
    # Sort
    standings = sorted(driver_points.items(), key=lambda x: x[1], reverse=True)
    
    print("\n2017 Final Standings:")
    for rank, (drv, pts) in enumerate(standings, 1):
        print(f"{rank}. {drv}: {pts}")
        
    return standings

if __name__ == "__main__":
    get_2017_standings()
