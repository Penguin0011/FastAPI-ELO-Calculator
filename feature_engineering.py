import numpy as np
import pandas as pd
import fastf1

def calculate_pace_metrics(session, driver_code, teammate=None):
    """
    Calculates pace relative to the field and teammate.
    Returns a dictionary of metrics.
    """
    try:
        laps = session.laps.pick_driver(driver_code).pick_quicklaps()
        if laps.empty:
            return {'pace_delta': 0.0, 'teammate_delta': 0.0, 'consistency': 0.0}
        
        # Session median
        all_laps = session.laps.pick_quicklaps()
        if all_laps.empty:
            return {'pace_delta': 0.0, 'teammate_delta': 0.0, 'consistency': 0.0}
            
        session_median = all_laps['LapTime'].median()
        driver_median = laps['LapTime'].median()
        
        # Consistency: Std Dev of lap times (lower is better)
        consistency = laps['LapTime'].std().total_seconds() if len(laps) > 1 else 0.0
        
        pace_delta = 0.0
        if not pd.isna(session_median) and not pd.isna(driver_median):
            pace_delta = (driver_median - session_median) / session_median
            
        # Teammate Delta
        teammate_delta = 0.0
        if teammate:
            tm_laps = session.laps.pick_driver(teammate).pick_quicklaps()
            if not tm_laps.empty:
                tm_median = tm_laps['LapTime'].median()
                if not pd.isna(tm_median) and not pd.isna(driver_median):
                     teammate_delta = (driver_median - tm_median) / tm_median

        return {
            'pace_delta': pace_delta,
            'teammate_delta': teammate_delta,
            'consistency': consistency
        }
        
    except Exception as e:
        return {'pace_delta': 0.0, 'teammate_delta': 0.0, 'consistency': 0.0}

def get_speed_trap_data(session, driver_code):
    """
    Get max speed.
    """
    try:
        laps = session.laps.pick_driver(driver_code).pick_quicklaps()
        if laps.empty:
            return 0.0
        # Check SpeedTrap_0 or similar? 
        # FastF1 'ST' column in laps?
        if 'ST' in laps.columns:
            return laps['ST'].max()
        return 0.0
    except:
        return 0.0

def determine_mechanical_dnf(status: str) -> bool:
    """
    Heuristic for mechanical DNF.
    """
    mech_keywords = ['Engine', 'Gearbox', 'Brakes', 'Clutch', 'Hydraulics', 'Electrical', 'Power Unit', 'Transmission', 'Exhaust', 'Turbo', 'MGU', 'Electronics', 'Pump', 'Oil', 'Water', 'Cooling']
    status_lower = str(status).lower()
    
    # Check if mechanical
    for kw in mech_keywords:
        if kw.lower() in status_lower:
            return True
            
    # Explicit exclusions (Accidents)
    accident_keywords = ['accident', 'collision', 'crash', 'spun', 'tyre', 'puncture', 'damage', 'retired', 'withdrew', 'illness']
    for kw in accident_keywords:
        if kw in status_lower:
            return False
            
    return False

def calculate_braking_aggression(session, driver_code) -> float:
    """
    Calculates a 'Braking Aggression' score based on peak deceleration.
    Late brakers typically decelerate harder and for shorter duration.
    
    Returns:
        float: 95th percentile of deceleration (g-force proxy, roughly).
        Higher is more aggressive.
    """
    try:
        # Get fastest lap telemetry
        laps = session.laps.pick_driver(driver_code).pick_quicklaps()
        if laps.empty:
            return 0.0
            
        fastest_lap = laps.pick_fastest()
        if fastest_lap is None or pd.isna(fastest_lap['LapTime']):
            return 0.0
            
        try:
            telemetry = fastest_lap.get_telemetry()
        except:
            return 0.0 # No data
            
        if 'Speed' not in telemetry.columns or 'Time' not in telemetry.columns:
            return 0.0
            
        # Calculate Deceleration
        # Speed is km/h. Convert to m/s: / 3.6
        # dv/dt
        
        speed_ms = telemetry['Speed'] / 3.6
        time_s = telemetry['Time'].dt.total_seconds()
        
        # Gradient
        accel = np.gradient(speed_ms, time_s)
        
        # We want Deceleration (Negative Accel)
        decel = -accel
        
        # Filter for braking zones (Decel > 2 m/s^2 roughly)
        braking_events = decel[decel > 2.0]
        
        if len(braking_events) < 10:
            return 0.0
            
        # Metric: 95th percentile of deceleration (Peak Braking Power)
        # Late brakers push the limit of tire friction -> higher peak decel.
        metric = np.percentile(braking_events, 95)
        
        return float(metric)
        
    except Exception as e:
        return 0.0
