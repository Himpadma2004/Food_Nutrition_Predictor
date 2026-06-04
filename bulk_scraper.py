import os
import time
import random
import hashlib
import requests

from io import BytesIO
from PIL import Image
from tqdm import tqdm
from ddgs import DDGS
import time

# ==================================================
# PROJECT PATHS
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATASET_FOLDER = os.path.join(
    BASE_DIR,
    "food_dataset"
)

TXT_PATH = os.path.join(
    BASE_DIR,
    "food_categories.txt"
)

os.makedirs(
    DATASET_FOLDER,
    exist_ok=True
)


# ==================================================
# CONFIG
# ==================================================

POPULAR_TARGET = 200
REGIONAL_TARGET = 120
RARE_TARGET = 80
THALI_TARGET = 100

MIN_WIDTH = 200
MIN_HEIGHT = 200

REQUEST_TIMEOUT = 8

USER_AGENT = (
    "Mozilla/5.0"
)

DDGS_RESULTS_PER_QUERY = 60
DDGS_RETRIES = 3


# ==================================================
# CATEGORY TYPES
# ==================================================

THALI_KEYWORDS = [
    "thali",
    "sadya",
    "wazwan",
    "dham"
]

RARE_FOODS = [
    "Khichu",
    "Patra",
    "Dal Dhokli",
    "Handvo",
    "Sev Tameta",
    "Gujarati Kadhi"
]

REGIONAL_FOODS = [
    "Dhokla",
    "Khaman",
    "Thepla",
    "Undhiyu",
    "Khakhra",
    "Fafda",
    "Appam",
    "Pongal"
]


# ==================================================
# TARGET IMAGE COUNT
# ==================================================

def get_target_count(food_name):

    lower_name = food_name.lower()

    if any(
        x in lower_name
        for x in THALI_KEYWORDS
    ):
        return THALI_TARGET

    if food_name in RARE_FOODS:
        return RARE_TARGET

    if food_name in REGIONAL_FOODS:
        return REGIONAL_TARGET

    return POPULAR_TARGET


# ==================================================
# SMART QUERY EXPANSION
# ==================================================

def build_queries(food_name):

    food_lower = food_name.lower()

    queries = [

        f"{food_name} Indian food",

        f"{food_name} dish",

        f"{food_name} plate",

        f"{food_name} meal",

        f"{food_name} homemade",

        f"{food_name} close up",

        f"{food_name} hd image",

        f"{food_name} restaurant",

        f"{food_name} traditional food",

        f"{food_name} authentic"
    ]

    # Extra queries for breads
    if any(
        x in food_lower
        for x in [
            "roti",
            "naan",
            "paratha",
            "kulcha",
            "bhature"
        ]
    ):

        queries.extend([

            f"{food_name} Indian bread",

            f"{food_name} close shot",

            f"{food_name} homemade Indian"
        ])

    # Extra queries for sweets
    if any(
        x in food_lower
        for x in [
            "jalebi",
            "rasgulla",
            "gulab jamun",
            "rasmalai",
            "barfi",
            "halwa"
        ]
    ):

        queries.extend([

            f"{food_name} Indian sweet",

            f"{food_name} dessert",

            f"{food_name} mithai"
        ])

    # Extra queries for thalis
    if "thali" in food_lower:

        queries.extend([

            f"{food_name} Indian platter",

            f"{food_name} full meal",

            f"{food_name} traditional thali"
        ])

    return list(set(queries))


# ==================================================
# DDGS SEARCH
# ==================================================

def ddgs_search(query):

    for attempt in range(
        DDGS_RETRIES
    ):

        try:

            with DDGS() as ddgs:

                results = ddgs.images(
                    query=query,
                    max_results=
                    DDGS_RESULTS_PER_QUERY
                )

                urls = []

                for item in results:

                    image_url = item.get(
                        "image"
                    )

                    if image_url:
                        urls.append(
                            image_url
                        )

                return urls

        except Exception as e:

            print(
                f"⚠️ DDGS retry "
                f"{attempt + 1}/"
                f"{DDGS_RETRIES}"
            )

            time.sleep(
                random.uniform(
                    5,
                    10
                )
            )

    return []


# ==================================================
# IMAGE VALIDATION
# ==================================================

def validate_image(content):

    try:

        image = Image.open(
            BytesIO(content)
        )

        image.verify()

        image = Image.open(
            BytesIO(content)
        )

        image = image.convert(
            "RGB"
        )

        width, height = image.size

        if (
            width < MIN_WIDTH
            or
            height < MIN_HEIGHT
        ):
            return None

        return image

    except Exception:

        return None


# ==================================================
# FOOD SCRAPER
# ==================================================

def scrape_food(food_name):

    target_count = (
        get_target_count(
            food_name
        )
    )

    folder_name = (
        food_name
        .replace(" ", "_")
        .lower()
    )

    save_folder = os.path.join(
        DATASET_FOLDER,
        folder_name
    )

    os.makedirs(
        save_folder,
        exist_ok=True
    )

    existing_images = os.listdir(
        save_folder
    )

    if (
        len(existing_images)
        >= target_count
    ):

        print(
            f"⏭️ "
            f"{food_name} "
            f"already complete"
        )

        return

    print(
        f"\n🍛 Processing: "
        f"{food_name}"
    )
    scrape_start = time.time()

    print(
        f"🎯 Target: "
        f"{target_count}"
    )

    all_urls = set()

    queries = build_queries(
        food_name
    )

    print(
        f"🔍 Running "
        f"{len(queries)} "
        f"queries..."
    )

    for query in queries:

        print(
            f"   → {query}"
        )

        urls = ddgs_search(
            query
        )

        all_urls.update(
            urls
        )

        time.sleep(
            random.uniform(
                1,
                2
            )
        )

    print(
        f"🔗 URLs found: "
        f"{len(all_urls)}"
    )

    saved_count = len(
        existing_images
    )

    hashes = set()

    for url in tqdm(
        all_urls
    ):

        if (
            saved_count
            >= target_count
        ):
            break

        try:

            response = (
                requests.get(
                    url,
                    timeout=
                    REQUEST_TIMEOUT,
                    headers={
                        "User-Agent":
                        USER_AGENT
                    }
                )
            )

            if (
                response.status_code
                != 200
            ):
                continue

            image = (
                validate_image(
                    response.content
                )
            )

            if image is None:
                continue

            image_hash = (
                hashlib.md5(
                    response.content
                )
                .hexdigest()
            )

            if (
                image_hash
                in hashes
            ):
                continue

            hashes.add(
                image_hash
            )

            file_path = (
                os.path.join(
                    save_folder,
                    f"{folder_name}_"
                    f"{saved_count}.jpg"
                )
            )

            image.save(
                file_path,
                "JPEG",
                quality=95
            )

            saved_count += 1

            time.sleep(
                random.uniform(
                    0.05,
                    0.15
                )
            )

        except Exception:
            continue

    scrape_end = time.time()
    total_seconds = (scrape_end - scrape_start)
    minutes = (total_seconds // 60)
    print(f"✅ Finished {food_name}: {saved_count}/{target_count}")
    print(f"⏱️ Scraping Time: {minutes:.2f} minutes")
    
# ==================================================
# MAIN
# ==================================================

def main():

    if not os.path.exists(
        TXT_PATH
    ):

        print(
            "❌ "
            "food_categories.txt "
            "not found!"
        )

        return

    with open(
        TXT_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        foods = [

            line.strip()

            for line in f

            if line.strip()
        ]

    print(
        f"\n🚀 Starting "
        f"{len(foods)} "
        f"categories"
    )

    for food in foods:

        scrape_food(food)

        cooldown = (
            random.uniform(
                4,
                8
            )
        )

        print(
            f"⏳ Cooling "
            f"{cooldown:.1f}s"
        )

        time.sleep(
            cooldown
        )

    print(
        "\n🎉 DATASET "
        "COMPLETED!"
    )


if __name__ == "__main__":
    main()