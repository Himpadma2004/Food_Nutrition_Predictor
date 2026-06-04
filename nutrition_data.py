# ─────────────────────────────────────────────────────────────────────────────
# nutrition_data.py
# Per-100g nutrition values for all 77 Indian food classes
# Sources: IFCT 2017 (Indian Food Composition Tables), USDA FoodData Central,
#          Nutritionix, NIN Hyderabad database
# All values are approximate for a standard preparation of each dish
# ─────────────────────────────────────────────────────────────────────────────

# ICMR RDA (Recommended Dietary Allowance) for a sedentary Indian adult
ICMR_RDA = {
    'calories'    : 2000,   # kcal/day
    'protein'     : 60,     # g/day
    'carbs'       : 300,    # g/day
    'fat'         : 60,     # g/day
    'fiber'       : 40,     # g/day
    'sugar'       : 50,     # g/day  (added sugars limit)
    'sodium'      : 2000,   # mg/day
}

# ─────────────────────────────────────────────────────────────────────────────
# NUTRITION DATA  (per 100g unless stated)
# keys: calories(kcal), protein(g), carbs(g), fat(g), fiber(g), sugar(g), sodium(mg)
# ─────────────────────────────────────────────────────────────────────────────
NUTRITION = {

    # ── Rice Dishes ──────────────────────────────────────────────────────────
    'biryani': {
        'calories': 200, 'protein': 8.5, 'carbs': 28.0,
        'fat': 6.5, 'fiber': 1.2, 'sugar': 1.5, 'sodium': 420,
    },
    'pulao': {
        'calories': 172, 'protein': 4.2, 'carbs': 30.5,
        'fat': 4.0, 'fiber': 1.0, 'sugar': 1.0, 'sodium': 310,
    },
    'khichdi': {
        'calories': 130, 'protein': 5.5, 'carbs': 22.0,
        'fat': 2.8, 'fiber': 2.5, 'sugar': 0.8, 'sodium': 280,
    },
    'fried_rice': {
        'calories': 185, 'protein': 5.0, 'carbs': 28.0,
        'fat': 6.0, 'fiber': 1.5, 'sugar': 2.0, 'sodium': 480,
    },
    'rasam': {
        'calories':  38, 'protein': 1.8, 'carbs':  6.5,
        'fat': 0.8, 'fiber': 1.0, 'sugar': 2.0, 'sodium': 390,
    },
    'idli': {
        'calories':  58, 'protein': 2.1, 'carbs': 11.2,
        'fat': 0.4, 'fiber': 0.5, 'sugar': 0.3, 'sodium': 180,
    },
    'pongal': {
        'calories': 148, 'protein': 4.5, 'carbs': 24.5,
        'fat': 4.2, 'fiber': 1.8, 'sugar': 0.5, 'sodium': 260,
    },

    # ── Breads / Flatbreads ───────────────────────────────────────────────────
    'roti': {
        'calories': 120, 'protein': 3.5, 'carbs': 22.0,
        'fat': 2.0, 'fiber': 2.8, 'sugar': 0.3, 'sodium': 160,
    },
    'paratha': {
        'calories': 260, 'protein': 5.5, 'carbs': 34.0,
        'fat': 11.0, 'fiber': 2.5, 'sugar': 0.5, 'sodium': 320,
    },
    'naan': {
        'calories': 280, 'protein': 8.0, 'carbs': 50.0,
        'fat': 5.5, 'fiber': 1.8, 'sugar': 2.5, 'sodium': 480,
    },
    'poori': {
        'calories': 330, 'protein': 6.0, 'carbs': 40.0,
        'fat': 16.0, 'fiber': 2.0, 'sugar': 0.5, 'sodium': 290,
    },
    'chole_bhature': {
        'calories': 310, 'protein': 9.5, 'carbs': 42.0,
        'fat': 12.0, 'fiber': 5.0, 'sugar': 2.0, 'sodium': 520,
    },
    'uttapam': {
        'calories': 118, 'protein': 3.8, 'carbs': 19.5,
        'fat': 3.0, 'fiber': 1.5, 'sugar': 1.2, 'sodium': 220,
    },
    'appam': {
        'calories': 110, 'protein': 2.5, 'carbs': 22.0,
        'fat': 1.5, 'fiber': 0.8, 'sugar': 1.5, 'sodium': 150,
    },
    'dosa': {
        'calories': 133, 'protein': 3.5, 'carbs': 21.5,
        'fat': 4.0, 'fiber': 1.2, 'sugar': 0.8, 'sodium': 240,
    },

    # ── Curries & Gravies ─────────────────────────────────────────────────────
    'dal_makhani': {
        'calories': 145, 'protein': 7.5, 'carbs': 18.0,
        'fat': 5.0, 'fiber': 4.5, 'sugar': 2.0, 'sodium': 380,
    },
    'palak_paneer': {
        'calories': 165, 'protein': 8.5, 'carbs': 8.0,
        'fat': 11.5, 'fiber': 3.0, 'sugar': 2.5, 'sodium': 350,
    },
    'paneer_butter_masala': {
        'calories': 198, 'protein': 9.0, 'carbs': 10.5,
        'fat': 14.5, 'fiber': 2.0, 'sugar': 4.5, 'sodium': 420,
    },
    'butter_chicken': {
        'calories': 175, 'protein': 14.5, 'carbs': 7.5,
        'fat': 10.5, 'fiber': 1.5, 'sugar': 4.0, 'sodium': 480,
    },
    'chicken_curry': {
        'calories': 155, 'protein': 15.0, 'carbs': 5.5,
        'fat': 8.5, 'fiber': 1.0, 'sugar': 2.5, 'sodium': 450,
    },
    'mutton_curry': {
        'calories': 190, 'protein': 17.5, 'carbs': 4.5,
        'fat': 12.0, 'fiber': 0.8, 'sugar': 1.5, 'sodium': 510,
    },
    'malai_kofta': {
        'calories': 220, 'protein': 7.5, 'carbs': 18.0,
        'fat': 14.0, 'fiber': 2.5, 'sugar': 5.0, 'sodium': 390,
    },
    'shahi_paneer': {
        'calories': 210, 'protein': 8.5, 'carbs': 12.0,
        'fat': 15.0, 'fiber': 1.5, 'sugar': 5.5, 'sodium': 360,
    },
    'kadai_paneer': {
        'calories': 185, 'protein': 9.0, 'carbs': 9.5,
        'fat': 13.0, 'fiber': 2.5, 'sugar': 4.0, 'sodium': 380,
    },
    'paneer_tikka_masala': {
        'calories': 195, 'protein': 9.5, 'carbs': 10.0,
        'fat': 14.0, 'fiber': 2.0, 'sugar': 4.5, 'sodium': 410,
    },
    'aloo_gobi': {
        'calories':  95, 'protein': 2.8, 'carbs': 15.0,
        'fat': 3.2, 'fiber': 3.5, 'sugar': 3.0, 'sodium': 280,
    },
    'mixed_veg_curry': {
        'calories':  88, 'protein': 2.5, 'carbs': 12.5,
        'fat': 3.5, 'fiber': 3.8, 'sugar': 3.5, 'sodium': 310,
    },
    'kadhi': {
        'calories':  72, 'protein': 3.5, 'carbs': 8.5,
        'fat': 3.0, 'fiber': 0.8, 'sugar': 3.5, 'sodium': 350,
    },
    'rajma_chawal': {
        'calories': 158, 'protein': 7.5, 'carbs': 26.5,
        'fat': 3.0, 'fiber': 5.5, 'sugar': 1.5, 'sodium': 320,
    },
    'halwa': {
        'calories': 310, 'protein': 4.5, 'carbs': 48.0,
        'fat': 12.0, 'fiber': 1.5, 'sugar': 32.0, 'sodium': 120,
    },

    # ── Street Foods / Snacks ─────────────────────────────────────────────────
    'samosa': {
        'calories': 262, 'protein': 5.0, 'carbs': 32.0,
        'fat': 13.0, 'fiber': 2.5, 'sugar': 1.5, 'sodium': 380,
    },
    'pakora': {
        'calories': 285, 'protein': 6.5, 'carbs': 28.0,
        'fat': 16.5, 'fiber': 2.0, 'sugar': 1.0, 'sodium': 420,
    },
    'bread_pakora': {
        'calories': 295, 'protein': 7.0, 'carbs': 35.0,
        'fat': 14.5, 'fiber': 1.8, 'sugar': 1.5, 'sodium': 460,
    },
    'vada_pav': {
        'calories': 290, 'protein': 6.5, 'carbs': 42.0,
        'fat': 11.0, 'fiber': 3.0, 'sugar': 2.5, 'sodium': 510,
    },
    'pav_bhaji': {
        'calories': 185, 'protein': 5.5, 'carbs': 28.5,
        'fat': 6.5, 'fiber': 4.0, 'sugar': 5.0, 'sodium': 480,
    },
    'pani_puri': {
        'calories': 180, 'protein': 3.5, 'carbs': 28.0,
        'fat': 6.5, 'fiber': 2.5, 'sugar': 3.0, 'sodium': 540,
    },
    'bhel_puri': {
        'calories': 150, 'protein': 4.0, 'carbs': 25.0,
        'fat': 4.5, 'fiber': 2.5, 'sugar': 4.0, 'sodium': 490,
    },
    'sev_puri': {
        'calories': 195, 'protein': 4.5, 'carbs': 26.0,
        'fat': 8.5, 'fiber': 2.0, 'sugar': 4.5, 'sodium': 530,
    },
    'chaat': {
        'calories': 160, 'protein': 4.0, 'carbs': 24.0,
        'fat': 5.5, 'fiber': 3.0, 'sugar': 5.5, 'sodium': 500,
    },
    'kachori': {
        'calories': 400, 'protein': 7.5, 'carbs': 45.0,
        'fat': 22.0, 'fiber': 3.5, 'sugar': 1.5, 'sodium': 360,
    },
    'aloo_tikki': {
        'calories': 195, 'protein': 3.5, 'carbs': 28.0,
        'fat': 8.0, 'fiber': 2.5, 'sugar': 1.5, 'sodium': 380,
    },
    'medu_vada': {
        'calories': 225, 'protein': 7.5, 'carbs': 22.0,
        'fat': 12.0, 'fiber': 2.8, 'sugar': 0.5, 'sodium': 320,
    },
    'dabeli': {
        'calories': 250, 'protein': 6.0, 'carbs': 38.0,
        'fat': 9.0, 'fiber': 3.0, 'sugar': 6.0, 'sodium': 490,
    },
    'frankie_roll': {
        'calories': 220, 'protein': 8.5, 'carbs': 30.0,
        'fat': 8.0, 'fiber': 2.5, 'sugar': 3.0, 'sodium': 450,
    },
    'misal_pav': {
        'calories': 210, 'protein': 8.5, 'carbs': 32.0,
        'fat': 6.0, 'fiber': 5.5, 'sugar': 2.5, 'sodium': 480,
    },
    'momos': {
        'calories': 155, 'protein': 9.5, 'carbs': 20.0,
        'fat': 4.0, 'fiber': 1.5, 'sugar': 1.5, 'sodium': 390,
    },
    'sandwich': {
        'calories': 230, 'protein': 8.0, 'carbs': 32.0,
        'fat': 8.5, 'fiber': 2.5, 'sugar': 4.0, 'sodium': 520,
    },

    # ── Sweets / Desserts ─────────────────────────────────────────────────────
    'jalebi': {
        'calories': 358, 'protein': 2.5, 'carbs': 65.0,
        'fat': 10.0, 'fiber': 0.5, 'sugar': 52.0, 'sodium':  80,
    },
    'gulab_jamun': {
        'calories': 380, 'protein': 5.5, 'carbs': 58.0,
        'fat': 14.5, 'fiber': 0.5, 'sugar': 45.0, 'sodium': 120,
    },
    'rasgulla': {
        'calories': 186, 'protein': 5.0, 'carbs': 34.5,
        'fat': 3.5, 'fiber': 0.2, 'sugar': 32.0, 'sodium':  90,
    },
    'rasmalai': {
        'calories': 215, 'protein': 6.5, 'carbs': 28.0,
        'fat': 8.5, 'fiber': 0.3, 'sugar': 26.0, 'sodium': 110,
    },
    'barfi': {
        'calories': 410, 'protein': 8.5, 'carbs': 58.0,
        'fat': 16.5, 'fiber': 0.8, 'sugar': 50.0, 'sodium': 100,
    },
    'kaju_katli': {
        'calories': 485, 'protein': 10.5, 'carbs': 62.0,
        'fat': 22.5, 'fiber': 1.5, 'sugar': 55.0, 'sodium':  80,
    },
    'ladoo': {
        'calories': 440, 'protein': 6.5, 'carbs': 65.0,
        'fat': 18.0, 'fiber': 2.0, 'sugar': 45.0, 'sodium': 120,
    },
    'modak': {
        'calories': 320, 'protein': 5.0, 'carbs': 52.0,
        'fat': 10.5, 'fiber': 2.5, 'sugar': 30.0, 'sodium':  90,
    },
    'mysore_pak': {
        'calories': 520, 'protein': 6.5, 'carbs': 60.0,
        'fat': 30.0, 'fiber': 1.0, 'sugar': 48.0, 'sodium': 150,
    },
    'peda': {
        'calories': 390, 'protein': 8.5, 'carbs': 58.0,
        'fat': 13.5, 'fiber': 0.5, 'sugar': 50.0, 'sodium': 130,
    },
    'shrikhand': {
        'calories': 245, 'protein': 7.5, 'carbs': 38.0,
        'fat': 7.5, 'fiber': 0.2, 'sugar': 36.0, 'sodium': 100,
    },
    'rabri': {
        'calories': 280, 'protein': 8.0, 'carbs': 38.0,
        'fat': 11.0, 'fiber': 0.3, 'sugar': 35.0, 'sodium': 120,
    },
    'kulfi': {
        'calories': 218, 'protein': 5.5, 'carbs': 28.0,
        'fat': 9.5, 'fiber': 0.3, 'sugar': 25.0, 'sodium': 110,
    },

    # ── Gujarati Specialties ──────────────────────────────────────────────────
    'dhokla': {
        'calories': 160, 'protein': 5.5, 'carbs': 25.0,
        'fat': 4.5, 'fiber': 2.0, 'sugar': 3.5, 'sodium': 380,
    },
    'khaman': {
        'calories': 155, 'protein': 5.8, 'carbs': 24.5,
        'fat': 4.0, 'fiber': 2.2, 'sugar': 3.8, 'sodium': 360,
    },
    'thepla': {
        'calories': 195, 'protein': 5.5, 'carbs': 28.0,
        'fat': 7.0, 'fiber': 3.5, 'sugar': 1.0, 'sodium': 290,
    },
    'khakhra': {
        'calories': 385, 'protein': 11.0, 'carbs': 62.0,
        'fat': 10.5, 'fiber': 5.5, 'sugar': 1.5, 'sodium': 420,
    },
    'fafda': {
        'calories': 450, 'protein': 9.0, 'carbs': 55.0,
        'fat': 22.0, 'fiber': 3.5, 'sugar': 1.0, 'sodium': 480,
    },
    'undhiyu': {
        'calories': 145, 'protein': 5.5, 'carbs': 18.0,
        'fat': 6.0, 'fiber': 6.5, 'sugar': 3.5, 'sodium': 310,
    },
    'handvo': {
        'calories': 185, 'protein': 7.5, 'carbs': 26.0,
        'fat': 6.0, 'fiber': 3.5, 'sugar': 2.0, 'sodium': 380,
    },
    'sev_tameta': {
        'calories': 120, 'protein': 3.5, 'carbs': 14.5,
        'fat': 5.5, 'fiber': 2.5, 'sugar': 4.5, 'sodium': 350,
    },
    'dal_dhokli': {
        'calories': 165, 'protein': 6.5, 'carbs': 26.5,
        'fat': 4.5, 'fiber': 4.0, 'sugar': 2.5, 'sodium': 380,
    },
    'khichu': {
        'calories': 148, 'protein': 2.5, 'carbs': 30.5,
        'fat': 2.0, 'fiber': 1.5, 'sugar': 0.5, 'sodium': 290,
    },
    'patra': {
        'calories': 180, 'protein': 4.5, 'carbs': 25.0,
        'fat': 7.0, 'fiber': 3.5, 'sugar': 3.0, 'sodium': 340,
    },

    # ── Thalis ────────────────────────────────────────────────────────────────
    'gujarati_thali': {
        'calories': 180, 'protein': 6.5, 'carbs': 28.0,
        'fat': 5.5, 'fiber': 4.0, 'sugar': 5.0, 'sodium': 420,
    },
    'kathiyawadi_thali': {
        'calories': 210, 'protein': 7.0, 'carbs': 30.0,
        'fat': 7.5, 'fiber': 5.0, 'sugar': 4.0, 'sodium': 480,
    },

    # ── Non-Indian (kept in dataset) ──────────────────────────────────────────
    'pizza': {
        'calories': 266, 'protein': 11.0, 'carbs': 33.0,
        'fat': 10.0, 'fiber': 2.3, 'sugar': 3.6, 'sodium': 598,
    },
    'burger': {
        'calories': 295, 'protein': 14.5, 'carbs': 28.0,
        'fat': 14.0, 'fiber': 1.5, 'sugar': 5.5, 'sodium': 520,
    },
    'pasta': {
        'calories': 220, 'protein': 8.0, 'carbs': 38.0,
        'fat': 4.5, 'fiber': 2.5, 'sugar': 3.5, 'sodium': 340,
    },
    'sandwich': {
        'calories': 230, 'protein': 8.0, 'carbs': 32.0,
        'fat': 8.5, 'fiber': 2.5, 'sugar': 4.0, 'sodium': 520,
    },
    'taco': {
        'calories': 218, 'protein': 9.5, 'carbs': 20.0,
        'fat': 11.5, 'fiber': 2.5, 'sugar': 2.0, 'sodium': 480,
    },
}


def get_nutrition(food_key: str) -> dict | None:
    """
    Return nutrition dict for a food key (class name).
    Returns None if food not found in database.
    """
    return NUTRITION.get(food_key, None)


def scale_nutrition(nutrition: dict, grams: float) -> dict:
    """
    Scale nutrition values from per-100g to given gram amount.
    """
    factor = grams / 100.0
    return {k: round(v * factor, 1) for k, v in nutrition.items()}


def get_daily_pct(nutrition: dict, grams: float = 100) -> dict:
    """
    Return each nutrient as % of ICMR RDA for given gram amount.
    """
    scaled = scale_nutrition(nutrition, grams)
    return {
        k: round((scaled[k] / ICMR_RDA[k]) * 100, 1)
        for k in ICMR_RDA
    }


def get_health_tags(nutrition: dict, grams: float = 100) -> list[dict]:
    """
    Return auto-generated health tags based on per-serving values.
    Each tag: {'label': str, 'color': str, 'emoji': str}
    """
    n = scale_nutrition(nutrition, grams)
    tags = []

    # Calories
    if n['calories'] < 100:
        tags.append({'label': 'Low Calorie',  'color': '#2ecc71', 'emoji': '🟢'})
    elif n['calories'] > 350:
        tags.append({'label': 'High Calorie', 'color': '#e74c3c', 'emoji': '🔴'})

    # Protein
    if n['protein'] > 15:
        tags.append({'label': 'High Protein', 'color': '#2ecc71', 'emoji': '🟢'})
    elif n['protein'] < 3:
        tags.append({'label': 'Low Protein',  'color': '#f39c12', 'emoji': '🟡'})

    # Fat
    if n['fat'] < 3:
        tags.append({'label': 'Low Fat',      'color': '#2ecc71', 'emoji': '🟢'})
    elif n['fat'] > 20:
        tags.append({'label': 'High Fat',     'color': '#e74c3c', 'emoji': '🔴'})

    # Fiber
    if n['fiber'] > 5:
        tags.append({'label': 'High Fiber',   'color': '#2ecc71', 'emoji': '🟢'})

    # Sugar
    if n['sugar'] > 30:
        tags.append({'label': 'High Sugar',   'color': '#e74c3c', 'emoji': '🔴'})
    elif n['sugar'] < 5:
        tags.append({'label': 'Low Sugar',    'color': '#2ecc71', 'emoji': '🟢'})

    # Sodium
    if n['sodium'] > 500:
        tags.append({'label': 'High Sodium',  'color': '#e74c3c', 'emoji': '🔴'})
    elif n['sodium'] < 150:
        tags.append({'label': 'Low Sodium',   'color': '#2ecc71', 'emoji': '🟢'})

    return tags
