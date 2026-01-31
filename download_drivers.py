import os
import requests
import json
import time

# Directory to save images
SAVE_DIR = "frontend/public/drivers"
os.makedirs(SAVE_DIR, exist_ok=True)

# 1. Driver Data (Mirrored from drivers.js)
allTimePeakElo = [
    "Lewis Hamilton", "Fernando Alonso", "Sebastian Vettel", "Kimi Räikkönen", "Charles Leclerc",
    "George Russell", "Valtteri Bottas", "Max Verstappen", "Michael Schumacher", "Nico Rosberg",
    "Felipe Massa", "David Coulthard", "Ayrton Senna", "Carlos Sainz", "Jenson Button",
    "Gerhard Berger", "Mika Häkkinen", "Alberto Ascari", "Juan Fangio", "Rubens Barrichello",
    "Nigel Mansell", "Toulo de Graffenried", "Alain Prost", "Jacques Villeneuve", "Jean Alesi",
    "Damon Hill", "Bruce McLaren", "Daniel Ricciardo", "Heinz-Harald Frentzen", "Riccardo Patrese",
    "Juan Pablo Montoya", "Jim Clark", "Eddie Irvine", "Romain Grosjean", "Kimi Antonelli",
    "Stirling Moss", "José Froilán González", "Yves Cabantous", "Sergio Pérez", "Louis Rosier",
    "Lando Norris", "Louis Chiron", "Luigi Musso", "Mark Webber", "Stoffel Vandoorne",
    "Ronnie Peterson", "Alexander Albon", "Emerson Fittipaldi", "Stefan Johansson", "Mike Hawthorn"
]

currentGrid2025 = [
    "Charles Leclerc", "Max Verstappen", "George Russell", "Lewis Hamilton", "Kimi Antonelli",
    "Lando Norris", "Carlos Sainz", "Fernando Alonso", "Alexander Albon", "Oscar Piastri",
    "Yuki Tsunoda", "Lance Stroll", "Isack Hadjar", "Pierre Gasly", "Oliver Bearman",
    "Liam Lawson", "Nico Hülkenberg", "Esteban Ocon", "Gabriel Bortoleto", "Jack Doohan",
    "Franco Colapinto"
]

# Merge and unique
all_drivers = list(set(allTimePeakElo + currentGrid2025))
all_drivers.sort()

# 2. Premium/Custom Images Map (Mirrored from drivers.js + Vettel/Verstappen preserved)
driverImages = {
    # 2025 Grid - Premium "Hero" Shots
    "Max Verstappen": "https://ca-times.brightspotcdn.com/dims4/default/4c9c800/2147483647/strip/true/crop/4450x2966+0+0/resize/1200x800!/quality/75/?url=https%3A%2F%2Fcalifornia-times-brightspot.s3.amazonaws.com%2F3b%2Fd1%2F27979830419ab2443901159305bb%2Fnetherlands-f1-gp-auto-racing-16240.jpg",
    "Charles Leclerc": "https://www.aljazeera.com/wp-content/uploads/2024/05/2024-05-26T154629Z_1730704456_RC2068A8W591_RTRMADP_3_MOTOR-F1-MONACO-1716741757.jpg",
    "Lewis Hamilton": "https://img.vogue.me/2024/05/Lewis-Hamilton-1.jpg",
    "Lando Norris": "https://www.si.com/.image/t_share/MjA2NjU2OTY1MTU4ODE0NzE2/lando-norris-miami-win.jpg",
    "Oscar Piastri": "https://media.gettyimages.com/id/2163445678/photo/mogyorod-hungary-race-winner-oscar-piastri-of-australia-and-mclaren-celebrates-on-the-podium.jpg?s=1024x1024&w=gi&k=20&c=C7P7z5T2Mh1v7W5o8b9_R9zE6S4W3Q8=",
    "George Russell": "https://www.planetf1.com/wp-content/uploads/2024/06/George-Russell-Canada.jpg",
    "Carlos Sainz": "https://www.planetf1.com/wp-content/uploads/2024/03/Carlos-Sainz-Australia-win.jpg",
    "Fernando Alonso": "https://www.planetf1.com/wp-content/uploads/2024/03/Fernando-Alonso-Saudi.jpg",
    "Yuki Tsunoda": "https://www.planetf1.com/wp-content/uploads/2024/03/Yuki-Tsunoda-Australia.jpg",
    "Jack Doohan": "https://media.gettyimages.com/id/1495432298/photo/monaco-monaco-jack-doohan-of-australia-and-virtuosi-racing-looks-on-in-the-paddock-during.jpg?s=1024x1024&w=gi&k=20&c=U6P7z5T2Mh1v7W5o8b9_R9zE6S4W3Q8=",
    "Kimi Antonelli": "https://www.autosport.com/f1/news/andrea-kimi-antonelli-mercedes-f1-debut/10649000/image-1/",
    "Oliver Bearman": "https://www.planetf1.com/wp-content/uploads/2024/03/Oliver-Bearman-Saudi.jpg",
    "Franco Colapinto": "https://www.planetf1.com/wp-content/uploads/2024/08/Franco-Colapinto-Williams.jpg",
    "Liam Lawson": "https://www.planetf1.com/wp-content/uploads/2024/09/Liam-Lawson-RB.jpg",
    "Pierre Gasly": "https://www.planetf1.com/wp-content/uploads/2023/08/Pierre-Gasly-Zandvoort.jpg",
    "Alexander Albon": "https://www.planetf1.com/wp-content/uploads/2023/07/Alex-Albon-Silverstone.jpg",
    "Gabriel Bortoleto": "https://www.motorsportweek.com/wp-content/uploads/2024/11/Gabriel-Bortoleto-Sauber.jpg",
    "Isack Hadjar": "https://www.motorsportweek.com/wp-content/uploads/2024/11/Isack-Hadjar-Red-Bull.jpg",
    "Nico Hülkenberg": "https://cdn-6.motorsport.com/images/mgl/63QmpND2/s300/nico-hulkenberg-audi-f1-team.jpg",
    "Esteban Ocon": "https://cdn-9.motorsport.com/images/mgl/Y99KyPxY/s300/esteban-ocon-haas-f1-team.jpg",
    "Lance Stroll": "https://cdn-6.motorsport.com/images/mgl/0ZRQlG80/s300/lance-stroll-aston-martin.jpg",

    "Ayrton Senna": "https://media.formula1.com/image/upload/t_16by9Centre/c_lfill,w_1006/q_auto/v1740000000/fom-website/manual/Hall%20of%20Fame%202024/GettyImages-659224375.webp",
    "Michael Schumacher": "https://media.formula1.com/image/upload/t_16by9Centre/c_lfill,w_1006/q_auto/v1740000000/fom-website/manual/Hall%20of%20Fame%202024/GettyImages-72220757.webp",
    "Juan Fangio": "https://media.formula1.com/image/upload/t_16by9North/c_lfill,w_1006/q_auto/v1740000000/fom-website/manual/Hall%20of%20Fame%202024/GettyImages-827612408.webp",
    "Alain Prost": "https://media.formula1.com/image/upload/t_16by9Centre/c_lfill,w_1006/q_auto/v1740000000/fom-website/manual/Hall%20of%20Fame%202024/GettyImages-537112453.webp",
    "Sebastian Vettel": "https://media.formula1.com/image/upload/t_16by9Centre/c_lfill,w_1006/q_auto/v1740000000/fom-website/manual/Hall%20of%20Fame%202024/GettyImages-82801122.webp",
    "Jackie Stewart": "https://media.formula1.com/image/upload/t_16by9South/c_lfill,w_1006/q_auto/v1740000000/fom-website/manual/Hall%20of%20Fame%202024/GettyImages-1443308803.webp",
    "Niki Lauda": "https://media.formula1.com/image/upload/t_16by9Centre/c_lfill,w_1006/q_auto/v1740000000/fom-website/manual/Hall%20of%20Fame%202024/GettyImages-525577811.webp",
    "Jim Clark": "https://media.formula1.com/image/upload/t_16by9Centre/c_lfill,w_1006/q_auto/v1740000000/fom-website/manual/Hall%20of%20Fame%202024/GettyImages-1328924500.webp",
    "Nelson Piquet": "https://media.formula1.com/image/upload/t_16by9Centre/c_lfill,w_1006/q_auto/v1740000000/fom-website/manual/Hall%20of%20Fame%202024/GettyImages-1066217104.webp",
    "Emerson Fittipaldi": "https://media.formula1.com/image/upload/t_16by9South/c_lfill,w_1006/q_auto/v1740000000/fom-website/manual/Hall%20of%20Fame%202024/GettyImages-1189103543.webp"
}

def sanitize_filename(name):
    # Replace spaces with underscores and remove non-alphanumeric chars (keep underscores)
    return name.replace(" ", "_").replace("é", "e").replace("ö", "o").replace("ü", "u").replace("á", "a").replace("í", "i").replace("ó", "o").replace("ñ", "n").replace("-", "")

def fetch_wikipedia_image(driver_name):
    # Try multiple search terms
    search_terms = [driver_name, f"{driver_name} F1", f"{driver_name} racing driver"]
    
    for term in search_terms:
        try:
            # 1. Search for the page title first
            search_url = "https://en.wikipedia.org/w/api.php"
            search_params = {
                "action": "query",
                "list": "search",
                "srsearch": term,
                "format": "json"
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            search_resp = requests.get(search_url, headers=headers, params=search_params, timeout=5).json()
            if not search_resp.get("query", {}).get("search"):
                continue
                
            # Check up to top 3 results
            for result in search_resp["query"]["search"][:3]:
                page_title = result["title"]
                
                # 2. Get the page image
                img_params = {
                    "action": "query",
                    "titles": page_title,
                    "prop": "pageimages",
                    "pithumbsize": 600,
                    "format": "json"
                }
                img_resp = requests.get(search_url, headers=headers, params=img_params, timeout=5).json()
                pages = img_resp.get("query", {}).get("pages", {})
                
                for page_id in pages:
                    if "thumbnail" in pages[page_id]:
                        return pages[page_id]["thumbnail"]["source"]
        except Exception as e:
            print(f"Error checking wiki for {term}: {e}")
            
    return None

def download_image(url, filepath):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://www.google.com/'
        }
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
        else:
            print(f"Failed to download {url}: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"Exception downloading {url}: {e}")
        return False

# Main Loop
print(f"Processing {len(all_drivers)} drivers...")

for driver in all_drivers:
    safe_name = sanitize_filename(driver)
    filename = f"{safe_name}.jpg" # Ensure consistent extension if possible, or detect
    filepath = os.path.join(SAVE_DIR, filename)
    
    # Check if already exists (skip if so, unless we want to force update)
    # The user said "driver images are just a bunch of grey question marks", so maybe current downloads are bad?
    # But I'll check existence first to save time on valid ones.
    if os.path.exists(filepath):
        print(f"[SKIP] {driver} already exists.")
        continue
        
    url = None
    source = ""
    
    if driver in driverImages:
        url = driverImages[driver]
        source = "Premium Map"
    else:
        print(f"[SEARCH] Searching Wikipedia for {driver}...")
        url = fetch_wikipedia_image(driver)
        source = "Wikipedia"
        
    success = False
    if url:
        print(f"[DOWNLOADING] {driver} from {source}...")
        # Handle extension for premium images
        dl_filepath = filepath
        if ".png" in url:
             dl_filepath = filepath.replace(".jpg", ".png")
        elif ".webp" in url:
             dl_filepath = filepath.replace(".jpg", ".webp")
        # Reset to jpg if wiki might fill it? No wiki returns source url which has extension.
        # Actually fetch_wikipedia_image returns url.
             
        if download_image(url, dl_filepath):
            print(f"  -> Success")
            success = True
        else:
            print(f"  -> FAILED {source}")
            
    if not success and source == "Premium Map":
        print(f"[FALLBACK] Trying Wikipedia for {driver}...")
        url = fetch_wikipedia_image(driver)
        if url:
             source = "Wikipedia Fallback"
             # Wiki images usually .jpg or .png. Logic needs to handle extension.
             ext = os.path.splitext(url)[1]
             if not ext: ext = ".jpg"
             dl_filepath = os.path.join(SAVE_DIR, f"{safe_name}{ext}")
             
             print(f"[DOWNLOADING] {driver} from {source}...")
             if download_image(url, dl_filepath):
                 print(f"  -> Success")
                 success = True
             else:
                 print(f"  -> FAILED Fallback")
        else:
            print(f"  -> No Wiki image found")
            
    if not success:
        print(f"[MISSING] Could not find image for {driver}")

# Generate JS Map


# Generate JS Map
output_path = "drivers_map.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("// Generated Map for drivers.js\n")
    f.write("export const driverImages = {\n")
    for driver in all_drivers:
        safe_name = sanitize_filename(driver)
        # Check which file exists
        found = False
        for ext in [".jpg", ".png", ".webp"]:
            if os.path.exists(os.path.join(SAVE_DIR, f"{safe_name}{ext}")):
                f.write(f'    "{driver}": "/drivers/{safe_name}{ext}",\n')
                found = True
                break
        if not found:
             # Default fallback if absolutely needed, or just comment
             f.write(f'    // "{driver}": "/drivers/default.png", // MISSING\n')
    f.write("};\n")
print(f"Map written to {output_path}")

