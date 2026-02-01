import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# =============================================================================
# GLOBAL FIXED AXIS CONFIGURATION FOR OVERLAY COMPARISON SYSTEM
# =============================================================================
# All plots use IDENTICAL axis ranges so they can be overlaid via CSS
GLOBAL_X_MIN = 0        # Will be set to min race_index
GLOBAL_X_MAX = None     # Will be set to max race_index (dynamic)
GLOBAL_Y_MIN = 1000     # Minimum ELO axis
GLOBAL_Y_MAX = 2500     # Maximum ELO axis (top of graph)
PLOT_TRANSPARENT = True # Enable transparent background for overlay

def plot_individual_driver_history(history_df: pd.DataFrame, output_dir: str):
    """
    Plots the ELO history for every single driver individually.
    
    NEW FEATURES (for Static Overlay Comparison):
    - Fixed Y-Axis limits (1000-2500) across ALL plots
    - Fixed X-Axis limits (0 to max_race_index) across ALL plots
    - Transparent backgrounds (PNG with alpha channel)
    - Consistent styling enables visual comparison via CSS image stacking
    """
    global GLOBAL_X_MAX
    
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
    
    # Set global X max based on total races
    GLOBAL_X_MAX = len(races) - 1
    
    # Create readable labels: "Year Country"
    def get_short_name(full_name):
        return full_name.replace(" Grand Prix", "").replace("Gp", "")
        
    races['label'] = races['year'].astype(str) + " " + races['race_name'].apply(get_short_name)
    
    merged = history_df.merge(races, on=['year', 'round'])
    
    plt.style.use('dark_background')
    
    print(f"Generating plots for {len(drivers)} drivers with FIXED AXIS (Overlay Mode)...")
    
    for drv in drivers:
        drv_data = merged[merged['driver'] == drv]
        
        # Create figure with transparent background for overlay capability
        fig, ax = plt.subplots(figsize=(14, 7))
        
        if PLOT_TRANSPARENT:
            fig.patch.set_alpha(0.0)  # Figure transparent
            ax.patch.set_alpha(0.0)   # Axes transparent
        
        # Plot the line
        ax.plot(drv_data['race_index'], drv_data['rating'], label=drv, color='#FF1E00', linewidth=2.5)
        
        ax.set_title(f"{drv} - ELO History", fontsize=18, color='white', pad=20)
        ax.set_ylabel("ELO Rating", fontsize=12)
        
        # =================================================================
        # FIXED AXIS LIMITS (Critical for Static Overlay Comparison)
        # =================================================================
        ax.set_xlim(GLOBAL_X_MIN, GLOBAL_X_MAX)
        ax.set_ylim(GLOBAL_Y_MIN, GLOBAL_Y_MAX)
        
        # Configure X-Axis Labels (spaced to avoid clutter)
        # Use global race indices for ticks
        total_races = GLOBAL_X_MAX + 1
        num_ticks = min(20, total_races)
        tick_step = max(1, total_races // num_ticks)
        selected_indices = range(0, total_races, tick_step)
        
        tick_data = races[races['race_index'].isin(selected_indices)].sort_values('race_index')
        tick_indices = tick_data['race_index'].values
        tick_labels = tick_data['label'].values
        
        ax.set_xticks(tick_indices)
        ax.set_xticklabels(tick_labels, rotation=45, ha='right', fontsize=9)
        
        ax.legend(loc='upper left')
        ax.grid(True, linestyle='--', alpha=0.2)
        
        # Save with transparency
        safe_name = "".join([c for c in drv if c.isalpha() or c.isdigit() or c==' ']).strip().replace(' ', '_')
        path = os.path.join(output_dir, f"{safe_name}.png")
        
        plt.tight_layout()
        plt.savefig(path, dpi=150, transparent=PLOT_TRANSPARENT)
        plt.close(fig)
        
    print(f"Saved {len(drivers)} plots to {output_dir}")

