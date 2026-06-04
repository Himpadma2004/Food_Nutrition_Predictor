import os
import time
import random
import hashlib
import requests

from io import BytesIO
from PIL import Image
from tqdm import tqdm
from ddgs import DDGS

# ==================================================
# PROJECT PATHS
# ==================================================

BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
DATASET_FOLDER = os.path.join(BASE_DIR, "food_dataset")
os.makedirs(DATASET_FOLDER, exist_ok=True)

# ==================================================
# EXACTLY WHICH CLASSES TO TOP UP & THEIR TARGETS
# ==================================================

TARGET_COUNT = 200   # bring every class up to this

TOPUP_CLASSES = {
    "chaat"            : 200,
    "fafda"            : 200,
    "undhiyu"          : 200,
    "dhokla"           : 200,
    "khaman"           : 200,
    "thepla"           : 200,
    "appam"            : 200,
    "khakhra"          : 200,
    "pongal"           : 200,
    "gujarati_thali"   : 200,
    "kathiyawadi_thali": 200,
    "handvo"           : 200,
    "sev_tameta"       : 200,
    "dal_dhokli"       : 200,
    "khichu"           : 200,
    "patra"            : 200,
}

# ==================================================
# CONFIG
# ==================================================

MIN_WIDTH        = 200
MIN_HEIGHT       = 200
REQUEST_TIMEOUT  = 8
USER_AGENT       = "Mozilla/5.0"
DDGS_RESULTS_PER_QUERY = 60
DDGS_RETRIES     = 3

# ==================================================
# RICH QUERY BUILDER
# (more specific queries = better quality images)
# ==================================================

EXTRA_QUERIES = {
    "chaat"            : ["chaat street food india", "chaat plate close up"],
    "fafda"            : ["fafda gujarati snack", "fafda jalebi breakfast"],
    "undhiyu"          : ["undhiyu gujarati dish", "surti undhiyu"],
    "dhokla"           : ["dhokla steamed gujarati", "soft dhokla plate"],
    "khaman"           : ["khaman dhokla gujarati", "yellow khaman soft"],
    "thepla"           : ["thepla gujarati flatbread", "methi thepla"],
    "appam"            : ["appam kerala breakfast", "appam with stew"],
    "khakhra"          : ["khakhra gujarati crispy", "khakhra snack"],
    "pongal"           : ["pongal south indian breakfast", "ven pongal dish"],
    "gujarati_thali"   : ["gujarati thali full meal", "gujarati thali plate"],
    "kathiyawadi_thali": ["kathiyawadi thali saurashtra", "kathiyawadi food plate"],
    "handvo"           : ["handvo gujarati cake", "handvo baked snack"],
    "sev_tameta"       : ["sev tameta gujarati curry", "sev tomato sabji"],
    "dal_dhokli"       : ["dal dhokli gujarati", "dal dhokli recipe plate"],
    "khichu"           : ["khichu gujarati rice flour", "papdi no lot khichu"],
    "patra"            : ["patra gujarati arbi leaves", "alu vadi patra"],
}

def build_queries(food_name, folder_name):
    base = [
        f"{food_name} Indian food",
        f"{food_name} dish close up",
        f"{food_name} plate meal",
        f"{food_name} homemade",
        f"{food_name} hd image",
        f"{food_name} restaurant",
        f"{food_name} traditional",
        f"{food_name} authentic recipe",
        f"{food_name} food photography",
        f"{food_name} Indian cuisine",
    ]
    extra = EXTRA_QUERIES.get(folder_name, [])
    return list(set(base + extra))

# ==================================================
# DDGS SEARCH
# ==================================================

def ddgs_search(query):
    for attempt in range(DDGS_RETRIES):
        try:
            with DDGS() as ddgs:
                results = ddgs.images(query=query,
                                    max_results=DDGS_RESULTS_PER_QUERY)
                return [item["image"] for item in results if item.get("image")]
        except Exception:
            print(f"  ⚠️ DDGS retry {attempt+1}/{DDGS_RETRIES}")
            time.sleep(random.uniform(5, 10))
    return []

# ==================================================
# IMAGE VALIDATION
# ==================================================

def validate_image(content):
    try:
        img = Image.open(BytesIO(content))
        img.verify()
        img = Image.open(BytesIO(content)).convert("RGB")
        if img.size[0] < MIN_WIDTH or img.size[1] < MIN_HEIGHT:
            return None
        return img
    except Exception:
        return None

# ==================================================
# SCRAPER — only fills up to target, skips if done
# ==================================================

def scrape_food(food_name, folder_name, target):
    save_folder = os.path.join(DATASET_FOLDER, folder_name)
    os.makedirs(save_folder, exist_ok=True)

    existing = [f for f in os.listdir(save_folder)
                if os.path.splitext(f)[1].lower() in
                {'.jpg','.jpeg','.png','.webp','.bmp'}]
    already  = len(existing)

    if already >= target:
        print(f"  ⏭️  {food_name} already has {already} images — skipping")
        return

    needed = target - already
    print(f"\n{'='*52}")
    print(f"  🍛 {food_name}")
    print(f"  Have: {already}  |  Need: {needed} more  |  Target: {target}")
    print(f"{'='*52}")

    queries  = build_queries(food_name, folder_name)
    all_urls = set()

    for q in queries:
        urls = ddgs_search(q)
        all_urls.update(urls)
        time.sleep(random.uniform(1, 2))

    print(f"  🔗 Unique URLs found: {len(all_urls)}")

    saved = already
    hashes = set()
    t0 = time.time()

    for url in tqdm(all_urls, desc=f"  Downloading {food_name}"):
        if saved >= target:
            break
        try:
            r = requests.get(url, timeout=REQUEST_TIMEOUT,
                            headers={"User-Agent": USER_AGENT})
            if r.status_code != 200:
                continue
            img = validate_image(r.content)
            if img is None:
                continue
            h = hashlib.md5(r.content).hexdigest()
            if h in hashes:
                continue
            hashes.add(h)
            img.save(os.path.join(save_folder,
                    f"{folder_name}_scraped_{saved}.jpg"),
                    "JPEG", quality=95)
            saved += 1
            time.sleep(random.uniform(0.05, 0.15))
        except Exception:
            continue

    mins = (time.time() - t0) / 60
    print(f"  ✅ Done: {saved}/{target} images  ({mins:.1f} min)")

# ==================================================
# MAIN
# ==================================================

def main():
    print(f"\n🚀 Topping up {len(TOPUP_CLASSES)} underfilled classes")
    print(f"   Target per class: {TARGET_COUNT} images\n")

    for folder_name, target in TOPUP_CLASSES.items():
        # Convert folder_name back to display name for queries
        food_name = folder_name.replace("_", " ").title()
        scrape_food(food_name, folder_name, target)
        cooldown = random.uniform(4, 8)
        print(f"  ⏳ Cooldown {cooldown:.1f}s")
        time.sleep(cooldown)

    print("\n🎉 All classes topped up!")

    # Final summary
    print("\n📊 Final image counts:")
    for folder_name in TOPUP_CLASSES:
        folder = os.path.join(DATASET_FOLDER, folder_name)
        count  = len([f for f in os.listdir(folder)
                    if os.path.splitext(f)[1].lower() in
                    {'.jpg','.jpeg','.png','.webp','.bmp'}])
        status = "✅" if count >= TARGET_COUNT else "⚠️"
        print(f"  {status} {folder_name:25s}: {count}")


if __name__ == "__main__":
    main()