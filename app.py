import streamlit as st
import torch
import torch.nn as nn
import torch.nn.functional as F
import timm
import numpy as np
import pickle
import json
import matplotlib.pyplot as plt
from PIL import Image
import albumentations as A
from albumentations.pytorch import ToTensorV2
from pathlib import Path

from nutrition_data import (
    get_nutrition, scale_nutrition,
    get_daily_pct, get_health_tags, ICMR_RDA
)

# ─────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title = "🍛 Indian Food Nutrition Predictor",
    page_icon  = "🍛",
    layout     = "wide",
    initial_sidebar_state = "expanded",
)

st.markdown("""
<style>
    /* ── Base ─────────────────────────────────────────── */
    .main  { background-color: #0e1117; }
    .stApp { background-color: #0e1117; }

    /* ── Hero banner ─────────────────────────────────── */
    .hero {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 50%, #ffcd3c 100%);
        padding: 32px 36px; border-radius: 20px;
        margin-bottom: 10px; text-align: center;
        box-shadow: 0 8px 32px #ff6b3540;
    }
    .hero h1 {
        color: white; font-size: 2.6rem;
        font-weight: 800; margin: 0; letter-spacing: -0.5px;
    }
    .hero p {
        color: #fff5e6; font-size: 1.05rem;
        margin: 8px 0 0 0; opacity: 0.9;
    }
    .hero .badges {
        margin-top: 14px;
    }
    .hero-badge {
        display: inline-block; background: #ffffff22;
        color: white; font-size: 0.8rem; font-weight: 600;
        padding: 4px 14px; border-radius: 20px;
        margin: 3px 4px; border: 1px solid #ffffff33;
    }

    /* ── Disclaimer banner ───────────────────────────── */
    .disclaimer {
        background: linear-gradient(135deg, #1a1200, #2a1f00);
        border: 1.5px solid #f7931e66;
        border-left: 5px solid #f7931e;
        border-radius: 12px; padding: 16px 20px;
        margin: 14px 0 20px 0;
    }
    .disclaimer .disc-title {
        color: #f7931e; font-size: 1rem;
        font-weight: 700; margin-bottom: 6px;
    }
    .disclaimer p {
        color: #ccc; font-size: 0.87rem;
        margin: 0; line-height: 1.6;
    }
    .disclaimer .disc-note {
        color: #f7931e; font-weight: 600;
    }

    /* ── Input tabs ──────────────────────────────────── */
    .input-section {
        background: #1e2130; border-radius: 16px;
        padding: 24px; margin-bottom: 20px;
    }
    .input-section h3 {
        color: #f7931e; margin: 0 0 16px 0;
        font-size: 1.1rem; font-weight: 700;
    }

    /* ── Prediction card ─────────────────────────────── */
    .pred-card {
        background: linear-gradient(135deg, #1a2e1a, #1e2e1e);
        border-radius: 14px; padding: 20px 24px;
        border-left: 5px solid #2ecc71; margin-bottom: 16px;
        box-shadow: 0 4px 16px #2ecc7120;
    }
    .pred-label {
        font-size: 1.8rem; font-weight: 800;
        color: #2ecc71; letter-spacing: -0.3px;
    }
    .pred-conf {
        font-size: 1rem; color: #aaa; margin-top: 5px;
    }
    .conf-bar-wrap {
        background: #2a2d3a; border-radius: 8px;
        height: 8px; margin-top: 10px; overflow: hidden;
    }
    .conf-bar-fill {
        height: 8px; border-radius: 8px;
        background: linear-gradient(90deg, #2ecc71, #27ae60);
    }

    /* ── Nutrition cards ─────────────────────────────── */
    .nutr-card {
        background: #1e2130; border-radius: 14px;
        padding: 20px 22px; margin-bottom: 16px;
        border: 1px solid #2a2d3a;
    }
    .nutr-title {
        font-size: 1.05rem; font-weight: 700;
        color: #f7931e; margin-bottom: 14px;
        border-bottom: 1px solid #2a2d3a; padding-bottom: 8px;
    }

    /* ── Fact rows ───────────────────────────────────── */
    .fact-row {
        display: flex; justify-content: space-between;
        align-items: center; padding: 7px 0;
        border-bottom: 1px solid #23263a; font-size: 0.93rem;
    }
    .fact-row:last-child { border-bottom: none; }
    .fact-key  { color: #bbb; }
    .fact-val  { color: white; font-weight: 700; font-size: 1rem; }
    .fact-pct  { color: #666; font-size: 0.78rem; margin-left: 6px; }

    /* ── Tag pills ───────────────────────────────────── */
    .tag-pill {
        display: inline-block; padding: 5px 13px;
        border-radius: 20px; font-size: 0.78rem;
        font-weight: 600; margin: 4px 4px 4px 0;
        letter-spacing: 0.2px;
    }

    /* ── Section heading ─────────────────────────────── */
    .section-head {
        font-size: 1.3rem; font-weight: 800;
        color: #f7931e; margin: 28px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #f7931e33;
    }

    /* ── Info box ────────────────────────────────────── */
    .info-box {
        background: #1a1d2a; border-radius: 10px;
        padding: 13px 16px; margin-top: 12px;
        font-size: 0.83rem; color: #777;
        border: 1px solid #2a2d3a;
    }

    /* ── Landing card ────────────────────────────────── */
    .landing-card {
        background: #1e2130; border-radius: 16px;
        padding: 32px; text-align: center;
        border: 2px dashed #2a2d3a;
        margin-top: 20px;
    }
    .landing-card .lc-icon {
        font-size: 4rem; margin-bottom: 12px;
    }
    .landing-card h3 { color: #f7931e; margin: 0 0 8px 0; }
    .landing-card p  { color: #888; font-size: 0.95rem; }

    /* ── Footer ──────────────────────────────────────── */
    .footer {
        text-align: center; color: #444;
        font-size: 0.78rem; padding: 24px 0 8px 0;
        border-top: 1px solid #1e2130;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# PATHS & CONSTANTS
# ─────────────────────────────────────────────────────────
CHECKPOINT_DIR = Path('./checkpoints')
MODEL_PATH     = CHECKPOINT_DIR / 'best_model.pth'
MAPPING_PATH   = CHECKPOINT_DIR / 'class_mapping.json'
NAMES_PKL      = CHECKPOINT_DIR / 'class_names.pkl'

IMG_SIZE = 256
TTA_N    = 6
TOP_K    = 5
DEVICE   = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# ─────────────────────────────────────────────────────────
# LOAD CLASS NAMES
# ─────────────────────────────────────────────────────────
@st.cache_resource
def load_class_names():
    if NAMES_PKL.exists():
        with open(NAMES_PKL, 'rb') as f:
            return pickle.load(f)
    if MAPPING_PATH.exists():
        with open(MAPPING_PATH) as f:
            d = json.load(f)
        idx_to_class = d.get('idx_to_class', {})
        return [idx_to_class[str(i)] for i in range(len(idx_to_class))]
    st.error("❌ class_names.pkl not found in ./checkpoints/")
    st.stop()


# ─────────────────────────────────────────────────────────
# MODEL
# ─────────────────────────────────────────────────────────
class FoodClassifier(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.backbone = timm.create_model(
            'tf_efficientnetv2_s', pretrained=False,
            num_classes=0, global_pool='avg',
            drop_rate=0.3, drop_path_rate=0.2,
        )
        feat = self.backbone.num_features
        self.head = nn.Sequential(
            nn.Linear(feat, 512), nn.BatchNorm1d(512),
            nn.GELU(), nn.Dropout(0.4),
            nn.Linear(512, num_classes),
        )

    def forward(self, x):
        return self.head(self.backbone(x))


@st.cache_resource
def load_model(num_classes):
    if not MODEL_PATH.exists():
        st.error(f"❌ Model not found: {MODEL_PATH}")
        st.stop()
    model = FoodClassifier(num_classes).to(DEVICE)
    ckpt  = torch.load(MODEL_PATH, map_location=DEVICE)
    model.load_state_dict(ckpt['model_state'])
    model.eval()
    return model


# ─────────────────────────────────────────────────────────
# TRANSFORMS
# ─────────────────────────────────────────────────────────
tta_transform = A.Compose([
    A.RandomResizedCrop(size=(IMG_SIZE, IMG_SIZE), scale=(0.85, 1.0), p=1.0),
    A.HorizontalFlip(p=0.5),
    A.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, p=0.4),
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ToTensorV2(),
])


# ─────────────────────────────────────────────────────────
# PREDICTION
# ─────────────────────────────────────────────────────────
@torch.no_grad()
def predict(pil_image, model, class_names, n_tta=TTA_N, top_k=TOP_K):
    img   = np.array(pil_image.convert('RGB'))
    views = torch.stack(
        [tta_transform(image=img)['image'] for _ in range(n_tta)]
    ).to(DEVICE).float()
    with torch.amp.autocast('cuda', enabled=DEVICE.type == 'cuda'):
        logits = model(views)
    probs          = F.softmax(logits, dim=1).mean(0)
    topk_p, topk_i = probs.topk(top_k)
    return [
        {'label': class_names[i.item()], 'confidence': p.item() * 100}
        for i, p in zip(topk_i, topk_p)
    ]


# ─────────────────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────────────────
def make_pred_chart(results):
    names  = [r['label']      for r in results]
    scores = [r['confidence'] for r in results]
    colors = ['#2ecc71'] + ['#3498db'] * (len(names) - 1)
    fig, ax = plt.subplots(figsize=(7, 3.5))
    fig.patch.set_facecolor('#1e2130')
    ax.set_facecolor('#1e2130')
    ax.barh(names[::-1], scores[::-1], color=colors[::-1],
            height=0.55, edgecolor='none')
    for i, (n, s) in enumerate(zip(names[::-1], scores[::-1])):
        ax.text(s + 0.8, i, f'{s:.1f}%', va='center',
                ha='left', fontsize=10, color='white', fontweight='bold')
    ax.set_xlim(0, 115)
    ax.set_xlabel('Confidence (%)', color='#aaa', fontsize=10)
    ax.set_title('Top Predictions', color='white', fontsize=13, pad=10)
    ax.tick_params(colors='#ccc', labelsize=10)
    ax.spines[:].set_visible(False)
    plt.tight_layout()
    return fig


def make_macro_donut(nutr):
    carbs, protein, fat = nutr['carbs'], nutr['protein'], nutr['fat']
    if (carbs + protein + fat) == 0:
        return None
    fig, ax = plt.subplots(figsize=(4, 4))
    fig.patch.set_facecolor('#1e2130')
    ax.set_facecolor('#1e2130')
    ax.pie(
        [carbs, protein, fat],
        labels=[f'Carbs\n{carbs}g', f'Protein\n{protein}g', f'Fat\n{fat}g'],
        colors=['#3498db', '#2ecc71', '#e74c3c'],
        startangle=90,
        wedgeprops=dict(width=0.5, edgecolor='#1e2130', linewidth=2),
        textprops=dict(color='white', fontsize=9),
    )
    ax.text(0, 0, f'{int(nutr["calories"])}\nkcal',
            ha='center', va='center', fontsize=14,
            color='white', fontweight='bold')
    ax.set_title('Macro Breakdown', color='white', fontsize=12, pad=10)
    plt.tight_layout()
    return fig


def make_daily_pct_chart(pct_dict):
    labels = list(pct_dict.keys())
    values = [min(v, 120) for v in pct_dict.values()]
    colors = ['#e74c3c' if v > 80 else '#f39c12' if v > 40 else '#2ecc71'
              for v in values]
    fig, ax = plt.subplots(figsize=(6, 3.8))
    fig.patch.set_facecolor('#1e2130')
    ax.set_facecolor('#1e2130')
    ax.barh(labels[::-1], values[::-1],
            color=colors[::-1], height=0.55, edgecolor='none')
    ax.axvline(100, color='#aaa', linestyle='--', linewidth=1, alpha=0.5)
    for i, lbl in enumerate(labels[::-1]):
        ax.text(values[len(values)-1-i] + 1, i,
                f'{pct_dict[lbl]:.0f}%',
                va='center', ha='left', fontsize=9,
                color='white', fontweight='bold')
    ax.set_xlim(0, 135)
    ax.set_xlabel('% of ICMR Daily Value', color='#aaa', fontsize=9)
    ax.set_title('% Daily Value (ICMR RDA)', color='white', fontsize=11, pad=8)
    ax.tick_params(colors='#ccc', labelsize=9)
    ax.spines[:].set_visible(False)
    plt.tight_layout()
    return fig


def make_calorie_gauge(calories, daily=2000):
    pct = min(calories / daily, 1.0)
    fill_color = '#2ecc71' if pct < 0.3 else '#f39c12' if pct < 0.6 else '#e74c3c'
    fig, ax = plt.subplots(figsize=(6, 1.8))
    fig.patch.set_facecolor('#1e2130')
    ax.set_facecolor('#1e2130')
    ax.barh([0], [daily],    color='#2a2d3a',  height=0.5, edgecolor='none')
    ax.barh([0], [calories], color=fill_color, height=0.5, edgecolor='none')
    ax.text(daily / 2, 0.55,
            f'{calories:.0f} kcal  —  {pct*100:.1f}% of daily 2000 kcal',
            ha='center', va='bottom', color='white',
            fontsize=10, fontweight='bold')
    ax.set_xlim(0, daily * 1.05)
    ax.set_ylim(-0.6, 1.1)
    ax.axis('off')
    ax.set_title('🔥 Calorie Gauge', color='white', fontsize=11, pad=6)
    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────
# NUTRITION RENDERER
# ─────────────────────────────────────────────────────────
def render_nutrition(food_key, grams):
    raw = get_nutrition(food_key)
    if raw is None:
        st.warning(f"⚠️ Nutrition data not available for **{food_key}**.")
        return

    nutr = scale_nutrition(raw, grams)
    pct  = get_daily_pct(raw, grams)
    tags = get_health_tags(raw, grams)

    st.markdown('<div class="section-head">🥗 Nutrition Information</div>',
                unsafe_allow_html=True)

    # Calorie gauge — full width
    fig_g = make_calorie_gauge(nutr['calories'])
    st.pyplot(fig_g, use_container_width=True)
    plt.close(fig_g)

    # Donut | Daily% bars
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        fig_d = make_macro_donut(nutr)
        if fig_d:
            st.pyplot(fig_d, use_container_width=True)
            plt.close(fig_d)
    with c2:
        fig_p = make_daily_pct_chart(pct)
        st.pyplot(fig_p, use_container_width=True)
        plt.close(fig_p)

    # Facts card | Tags
    c3, c4 = st.columns(2, gap="medium")
    with c3:
        st.markdown('<div class="nutr-card"><div class="nutr-title">📋 Nutrition Facts</div>',
                    unsafe_allow_html=True)
        DISPLAY = [
            ('🔥 Calories', 'calories', 'kcal'),
            ('🍞 Carbs',    'carbs',    'g'),
            ('💪 Protein',  'protein',  'g'),
            ('🧈 Fat',      'fat',      'g'),
            ('🌾 Fiber',    'fiber',    'g'),
            ('🍬 Sugar',    'sugar',    'g'),
            ('🧂 Sodium',   'sodium',   'mg'),
        ]
        rows = ''
        for label, key, unit in DISPLAY:
            rows += f"""<div class="fact-row">
                <span class="fact-key">{label}</span>
                <span>
                  <span class="fact-val">{nutr[key]}{unit}</span>
                  <span class="fact-pct">{pct[key]:.0f}% DV</span>
                </span></div>"""
        st.markdown(rows, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="nutr-card"><div class="nutr-title">🏷️ Health Tags</div>',
                    unsafe_allow_html=True)
        if tags:
            tag_html = ''
            for t in tags:
                bg = t['color'] + '28'
                tag_html += (
                    f'<span class="tag-pill" style="background:{bg};'
                    f'color:{t["color"]};border:1px solid {t["color"]}44;">'
                    f'{t["emoji"]} {t["label"]}</span>'
                )
            st.markdown(tag_html, unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:#666;font-size:0.88rem;">No special flags for this dish.</p>',
                        unsafe_allow_html=True)
        st.markdown('<br>', unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        m1.metric('Carbs',   f'{nutr["carbs"]}g')
        m2.metric('Protein', f'{nutr["protein"]}g')
        m3.metric('Fat',     f'{nutr["fat"]}g')
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="info-box">📌 All values shown for <b>{grams}g</b> serving · '
        f'Based on ICMR RDA for a sedentary Indian adult · '
        f'Actual nutritional values vary by recipe, cooking method, and ingredients used.</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────
# LOAD RESOURCES
# ─────────────────────────────────────────────────────────
class_names = load_class_names()
NUM_CLASSES = len(class_names)
model       = load_model(NUM_CLASSES)


# ─────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    n_tta = st.slider("TTA passes",       min_value=1, max_value=10, value=TTA_N,
                      help="More passes = slightly more accurate but slower")
    top_k = st.slider("Top-K results",    min_value=3, max_value=10, value=TOP_K)
    grams = st.slider("Serving size (g)", min_value=50, max_value=500,
                      value=100, step=25,
                      help="All nutrition values scale automatically")

    st.markdown("---")
    st.markdown("### 📊 Model Info")
    st.markdown(f"- **Classes :** {NUM_CLASSES}")
    st.markdown(f"- **Backbone:** EfficientNetV2-S")
    st.markdown(f"- **Input   :** {IMG_SIZE}×{IMG_SIZE}px")
    st.markdown(f"- **Device  :** `{DEVICE}`")

    st.markdown("---")
    st.markdown("### ⚠️ Quick Disclaimer")
    st.markdown("""
    <div style='background:#1a1200;border-left:3px solid #f7931e;
                padding:10px 12px;border-radius:6px;font-size:0.8rem;color:#ccc;'>
    Nutrition values are <b>fixed estimates</b>.
    Not for medical or dietary decisions.
    Consult a qualified nutritionist.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🍽️ Supported Foods")
    st.dataframe({"Food": sorted(class_names)},
                 use_container_width=True, height=260)


# ─────────────────────────────────────────────────────────
# MAIN PAGE
# ─────────────────────────────────────────────────────────

# ── Hero ──────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <h1>🍛 Indian Food Nutrition Predictor</h1>
  <p>Snap or upload a photo of Indian food · Identify the dish · Get a full nutrition breakdown</p>
  <div class="badges">
    <span class="hero-badge">🤖 AI Powered</span>
    <span class="hero-badge">📸 Camera Support</span>
    <span class="hero-badge">🥗 {NUM_CLASSES} Food Classes</span>
    <span class="hero-badge">🇮🇳 Indian Cuisine</span>
    <span class="hero-badge">📊 ICMR RDA Based</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Disclaimer banner ─────────────────────────────────────
st.markdown("""
<div class="disclaimer">
  <div class="disc-title">⚠️ Important Notice — Please Read</div>
  <p>
    This is an <span class="disc-note">early-stage research prototype</span>.
    The nutrition values displayed are <span class="disc-note">fixed estimates per 100g</span>
    sourced from standard food composition databases — they are <b>not calculated from your
    specific dish or portion</b>. Our model identifies food products based on their visual
    appearance from images, which may not always be accurate.<br><br>
    🚫 <span class="disc-note">Do not use this information for diet, health, or medical decisions.</span>
    Actual nutritional content varies significantly based on recipe, cooking method, ingredients,
    and portion size. Always consult a <b>qualified nutritionist or dietitian</b> for
    personalised dietary guidance. We are not nutrition or health experts.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Image Input — Upload or Camera ───────────────────────
st.markdown('<div class="input-section"><h3>📸 Provide a Food Image</h3>', unsafe_allow_html=True)

input_mode = st.radio(
    "Choose input method",
    ["📁 Upload Image", "📷 Use Camera"],
    horizontal=True,
    label_visibility="collapsed",
)

pil_img = None

if input_mode == "📁 Upload Image":
    uploaded = st.file_uploader(
        "Upload a food image",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
    )
    if uploaded:
        pil_img = Image.open(uploaded).convert('RGB')

else:  # Camera
    st.markdown(
        '<p style="color:#888;font-size:0.85rem;margin-bottom:8px;">'
        '📱 Allow camera access when prompted · Works best with a clear, single-dish photo</p>',
        unsafe_allow_html=True,
    )
    camera_img = st.camera_input("Take a photo of your food")
    if camera_img:
        pil_img = Image.open(camera_img).convert('RGB')

st.markdown('</div>', unsafe_allow_html=True)

# ── Results ───────────────────────────────────────────────
if pil_img is not None:

    col_img, col_res = st.columns([1, 1], gap="large")

    with col_img:
        st.markdown("#### 📷 Input Image")
        st.image(pil_img, use_container_width=True)

    with st.spinner("🔍 Analysing image..."):
        results = predict(pil_img, model, class_names, n_tta=n_tta, top_k=top_k)

    top1 = results[0]
    conf = top1['confidence']

    with col_res:
        st.markdown("#### 🏆 Prediction")

        # Confidence-based colour
        badge_color = '#2ecc71' if conf >= 70 else '#f39c12' if conf >= 40 else '#e74c3c'
        conf_label  = 'High Confidence' if conf >= 70 else 'Medium Confidence' if conf >= 40 else 'Low Confidence'

        st.markdown(f"""
        <div class="pred-card" style="border-left-color:{badge_color};">
            <div class="pred-label" style="color:{badge_color};">
                {top1['label'].replace('_', ' ').title()}
            </div>
            <div class="pred-conf">
                {conf:.1f}% confidence &nbsp;·&nbsp;
                <span style="color:{badge_color};font-weight:600;">{conf_label}</span>
            </div>
            <div class="conf-bar-wrap">
                <div class="conf-bar-fill"
                     style="width:{min(conf,100):.0f}%;
                            background:linear-gradient(90deg,{badge_color},{badge_color}aa);">
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Low-confidence warning
        if conf < 40:
            st.markdown("""
            <div style='background:#1a0a00;border:1px solid #e74c3c55;
                        border-radius:8px;padding:10px 14px;font-size:0.83rem;color:#e07050;
                        margin-bottom:10px;'>
            ⚠️ <b>Low confidence prediction.</b> The model is not certain about this dish.
            Try a clearer photo with better lighting and a single dish in frame.
            </div>
            """, unsafe_allow_html=True)

        fig = make_pred_chart(results[:top_k])
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    # Top-K medals
    st.markdown("---")
    st.markdown("#### 📋 Top Predictions")
    medals = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
    cols   = st.columns(min(top_k, 5))
    for i, (col, r) in enumerate(zip(cols, results[:top_k])):
        col.metric(
            label = f"{medals[i]} {r['label'].replace('_',' ').title()}",
            value = f"{r['confidence']:.1f}%",
        )

    st.markdown("---")

    # Nutrition section
    render_nutrition(top1['label'], grams)

else:
    # Landing state
    st.markdown("""
    <div class="landing-card">
        <div class="lc-icon">🍽️</div>
        <h3>Upload or snap a photo to get started</h3>
        <p>
            Use the <b>Upload Image</b> option to select a file from your device,<br>
            or use <b>Use Camera</b> to take a live photo directly.<br><br>
            The AI will identify the dish and show a complete nutrition breakdown instantly.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
    🍛 Indian Food Nutrition Predictor &nbsp;·&nbsp; v1.0 Beta &nbsp;·&nbsp;
    Built with EfficientNetV2-S · {NUM_CLASSES} classes · ICMR RDA based nutrition<br>
    ⚠️ For educational and research purposes only · Not a substitute for professional nutritional advice
</div>
""", unsafe_allow_html=True)