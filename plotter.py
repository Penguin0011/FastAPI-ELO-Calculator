import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

def plot_individual_driver_history(history_df: pd.DataFrame, output_dir: str):
    """
    Plots the ELO history for every single driver individually.
    """
    if history_df.empty:
        print("No history to plot.")
        return

    # Create directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all drivers
    drivers = history_df['driver'].unique()
    
    # Pre-calculate race index for continuous X axis
    races = history_df[['year', 'round', 'race_name', 'date']].drop_duplicates().sort_values(['year', 'round'])
    races['race_index'] = range(len(races))
    
    # Create readable labels: "Year Country"
    # FastF1 'race_name' is like "Bahrain Grand Prix". Extraction: "Bahrain"
    def get_short_name(full_name):
        return full_name.replace(" Grand Prix", "").replace("Gp", "")
        
    races['label'] = races['year'].astype(str) + " " + races['race_name'].apply(get_short_name)
    
    merged = history_df.merge(races, on=['year', 'round']) # Note: race_name might differ in history if we didn't store it consistent.
    # Check history_df content. It assumes 'year', 'round' match.
    # We might need to handle if 'race_name' wasn't in history_df?
    # history_df was built from race_data which had 'race_name'.
    # But wait, history_df only has ['year', 'round', 'driver', 'rating'].
    # We need to re-fetch race names or rely on the fact that we can get them from unique (year, round) tuples.
    # The 'races' dataframe above dedupes from history_df but history_df might NOT have race_name if get_history_df didn't save it!
    # Let's check elo_model.py
    
    plt.style.use('dark_background')
    
    print(f"Generating plots for {len(drivers)} drivers...")
    
    for drv in drivers:
        drv_data = merged[merged['driver'] == drv]
        
        fig, ax = plt.subplots(figsize=(14, 7)) # Wider for labels
        
        # Plot the line
        ax.plot(drv_data['race_index'], drv_data['rating'], label=drv, color='#FF1E00', linewidth=2.5) # F1 Red
        
        ax.set_title(f"{drv} - ELO History", fontsize=18, color='white', pad=20)
        ax.set_ylabel("ELO Rating", fontsize=12)
        
        # Configure X-Axis
        # We can't show every label if there are 100+ races.
        # Show ~20 ticks max.
        n_races = len(drv_data)
        if n_races > 20:
            step = n_races // 20
        else:
            step = 1
            
        tick_indices = drv_data['race_index'].iloc[::step]
        
        # We need to map back to labels from the MAIN 'races' df to ensure global consistency?
        # Or just local labels.
        # Ideally, X-axis represents time.
        # If a driver didn't race in a round, the line skips?
        # Matplotlib plot(x,y) connects points.
        
        # Let's use the actual indices from the global 'races' DF so gaps show up as gaps (or straight lines across missing years).
        # drv_data['race_index'] is correct global index.
        
        # Ticks: show ticks for the points we have, or global timeline?
        # Let's show global timeline ticks for context (e.g. Years).
        
        # Find indices where year changes?
        # Or just spacing.
        
        # Let's use the driver's own timeline for ticks to identify their specific races.
        tick_labels = races.loc[races['race_index'].isin(tick_indices), 'label']
        
        ax.set_xticks(tick_indices)
        ax.set_xticklabels(tick_labels, rotation=45, ha='right', fontsize=9)
        
        ax.legend(loc='upper left')
        ax.grid(True, linestyle='--', alpha=0.2)
        
        # Save
        safe_name = "".join([c for c in drv if c.isalpha() or c.isdigit() or c==' ']).strip().replace(' ', '_')
        path = os.path.join(output_dir, f"{safe_name}.png")
        
        plt.tight_layout()
        plt.savefig(path, dpi=150)
        plt.close(fig)
        
    print(f"Saved {len(drivers)} plots to {output_dir}")
