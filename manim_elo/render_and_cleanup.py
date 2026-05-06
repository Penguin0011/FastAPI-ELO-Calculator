import os
import glob
import subprocess
import shutil

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    media_dir = os.path.join(base_dir, "media", "videos")
    
    print("Starting master render for Parts 1, 2, and 3 (1080p60)...")
    print("This will take a significant amount of time.")
    
    # Run the existing script in HQ with parts-only filter
    subprocess.run(["python", "render_all_scenes.py", "--hq", "--parts-only"], cwd=base_dir)
    
    print("\nRendering complete. Running cleanup/replacement phase...")
    
    # Now find all 1080p60 generated mp4s
    hq_pattern = os.path.join(media_dir, "**", "1080p60", "*.mp4")
    hq_videos = glob.glob(hq_pattern, recursive=True)
    
    count_replaced = 0
    
    for hq_vid in hq_videos:
        # Example hq_vid: .../media/videos/s01_introduction/1080p60/Scene1_1_TitleHook.mp4
        scene_name = os.path.basename(hq_vid)
        dir_name = os.path.dirname(hq_vid)
        module_dir = os.path.dirname(dir_name) # e.g. s01_introduction
        
        # Look for older quality versions, like 480p15, and delete them
        # Walk the module_dir and find any other mp4s with the exact same scene_name
        # that are NOT in 1080p60
        for root, dirs, files in os.walk(module_dir):
            if os.path.basename(root) == "1080p60":
                continue
            if scene_name in files:
                old_file = os.path.join(root, scene_name)
                try:
                    os.remove(old_file)
                    print(f"Replaced/Removed older version: {old_file}")
                    count_replaced += 1
                except Exception as e:
                    print(f"Failed to remove {old_file}: {e}")
                    
        # Also clean up partial movie files for this scene specifically
        partial_dir = os.path.join(module_dir, "480p15", "partial_movie_files", os.path.splitext(scene_name)[0])
        if os.path.exists(partial_dir):
            try:
                shutil.rmtree(partial_dir)
                print(f"Removed partial cache: {partial_dir}")
            except Exception as e:
                print(f"Failed to remove partials {partial_dir}: {e}")
                
    print(f"\nCleanup finished! Replaced {count_replaced} older videos with their 1080p counterparts.")
    print("Animations that were not re-generated have been left alone.")

if __name__ == "__main__":
    main()
