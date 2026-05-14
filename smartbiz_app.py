"""
SmartBiz Analytics Surakarta v2.0
Platform Analisis & Rekomendasi Peluang Bisnis UMKM – Kota Surakarta
"""

import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SmartBiz Analytics – Surakarta",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
:root {
    --electric-blue : #3ABEF9;
    --neon-mint     : #A7FF83;
    --coral-red     : #FF6B6B;
    --deep-charcoal : #1E1E2E;
    --surface       : #181825;
    --card-bg       : #24273A;
    --text-primary  : #CDD6F4;
    --text-muted    : #7F849C;
    --border        : #313244;
    --amber         : #FFD700;
    --purple        : #C678DD;
}
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--surface);
    color: var(--text-primary);
}
section[data-testid="stSidebar"] {
    background-color: var(--deep-charcoal) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text-primary) !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stRadio label {
    font-size: 0.8rem; font-weight: 700; letter-spacing: 0.05em;
    text-transform: uppercase; color: var(--electric-blue) !important;
}
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background-color: #2A2A3E !important; border: 1px solid var(--border) !important;
    border-radius: 8px !important; color: var(--text-primary) !important;
}
.main .block-container { background-color: var(--surface); padding-top: 1.5rem; max-width: 100%; }

.metric-card {
    background: var(--card-bg); border: 1px solid var(--border);
    border-radius: 16px; padding: 1.25rem 1.5rem;
    text-align: center; position: relative; overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover { transform: translateY(-3px); box-shadow: 0 8px 30px rgba(58,190,249,0.15); }
.metric-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--electric-blue), var(--neon-mint));
    border-radius: 16px 16px 0 0;
}
.metric-card .label { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.4rem; }
.metric-card .value { font-size: 1.8rem; font-weight: 900; line-height: 1.1; }
.metric-card .sub { font-size: 0.72rem; color: var(--text-muted); margin-top: 0.3rem; }
.metric-card .hint { font-size: 0.68rem; color: #5a5f7a; margin-top: 0.5rem;
    background: rgba(49,50,68,0.5); border-radius: 6px; padding: 0.2rem 0.5rem; }
.value-blue  { color: var(--electric-blue); }
.value-mint  { color: var(--neon-mint); }
.value-coral { color: var(--coral-red); }
.value-amber { color: var(--amber); }

.section-header {
    font-size: 0.8rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--electric-blue);
    margin: 1.5rem 0 0.75rem; display: flex; align-items: center; gap: 0.5rem;
}
.section-header::after { content: ''; flex: 1; height: 1px; background: var(--border); }

.hero-banner {
    background: linear-gradient(135deg, #1E1E2E 0%, #181836 50%, #1E2E24 100%);
    border: 1px solid var(--border); border-radius: 20px;
    padding: 1.75rem 2.5rem; margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
}
.hero-banner h1 {
    font-size: 1.8rem; font-weight: 900;
    background: linear-gradient(135deg, var(--electric-blue), var(--neon-mint));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;
}
.hero-banner p { color: var(--text-muted); margin: 0.4rem 0 0; font-size: 0.88rem; }
.hero-glow {
    position: absolute; width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(58,190,249,0.08) 0%, transparent 70%);
    top: -80px; right: -80px; border-radius: 50%;
}

.recommend-box {
    border-radius: 16px; padding: 1.5rem 2rem; margin-top: 1rem; border: 1px solid;
    position: relative;
}
.recommend-box.high {
    background: linear-gradient(135deg, rgba(167,255,131,0.06), rgba(58,190,249,0.06));
    border-color: var(--neon-mint);
}
.recommend-box.medium {
    background: linear-gradient(135deg, rgba(58,190,249,0.06), rgba(30,30,46,0.8));
    border-color: var(--electric-blue);
}
.recommend-box.low {
    background: linear-gradient(135deg, rgba(255,107,107,0.06), rgba(30,30,46,0.8));
    border-color: var(--coral-red);
}
.recommend-box .badge {
    display: inline-block; font-size: 0.65rem; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    padding: 0.25rem 0.75rem; border-radius: 100px; margin-bottom: 0.75rem;
}
.recommend-box.high .badge  { background: var(--neon-mint);     color: #1E1E2E; }
.recommend-box.medium .badge{ background: var(--electric-blue); color: #1E1E2E; }
.recommend-box.low .badge   { background: var(--coral-red);     color: #fff; }
.recommend-box p { margin: 0.3rem 0; font-size: 0.9rem; line-height: 1.7; color: var(--text-primary); }
.recommend-box strong { color: var(--neon-mint); }

.biz-card {
    background: var(--card-bg); border: 1px solid var(--border); border-radius: 14px;
    padding: 1.2rem 1.5rem; margin-bottom: 0.75rem; transition: all 0.2s;
}
.biz-card:hover { border-color: var(--electric-blue); transform: translateX(3px); }
.biz-card .rank { font-size: 1.5rem; font-weight: 900; color: var(--electric-blue); }
.biz-card .kel-name { font-size: 1rem; font-weight: 700; color: var(--text-primary); }
.biz-card .kec-name { font-size: 0.75rem; color: var(--text-muted); }
.biz-card .stats { font-size: 0.8rem; color: var(--text-muted); margin-top: 0.3rem; }
.biz-card .gmaps-btn {
    display: inline-block; font-size: 0.7rem; font-weight: 700;
    background: linear-gradient(135deg, #34A853, #0F9D58);
    color: #fff !important; padding: 0.2rem 0.6rem; border-radius: 6px;
    text-decoration: none; margin-top: 0.4rem;
}

.guide-box {
    background: rgba(58,190,249,0.04); border: 1px solid rgba(58,190,249,0.2);
    border-radius: 14px; padding: 1.25rem 1.75rem;
}
.guide-box h4 { color: var(--electric-blue); font-size: 0.85rem; margin-top: 0.8rem; margin-bottom: 0.3rem; }
.guide-box p, .guide-box li { font-size: 0.82rem; color: var(--text-muted); line-height: 1.7; }

div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--electric-blue), #1E8FCC) !important;
    color: #0D0D1A !important; font-weight: 700 !important;
    font-size: 0.85rem !important; letter-spacing: 0.06em !important;
    text-transform: uppercase !important; border: none !important;
    border-radius: 10px !important; padding: 0.65rem 1.5rem !important;
    width: 100% !important; transition: all 0.25s !important;
    box-shadow: 0 4px 20px rgba(58,190,249,0.35) !important; cursor: pointer !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(58,190,249,0.55) !important;
}
.sidebar-logo {
    text-align: center; padding: 1rem 0 1.5rem;
    border-bottom: 1px solid #313244; margin-bottom: 1.5rem;
}
.sidebar-logo h2 {
    font-size: 1.1rem; font-weight: 900;
    background: linear-gradient(135deg, #3ABEF9, #A7FF83);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0.5rem 0 0.25rem;
}
.sidebar-logo p { font-size: 0.7rem; color: #7F849C; margin: 0; letter-spacing: 0.08em; }
.map-wrapper { border-radius: 16px; overflow: hidden; border: 1px solid var(--border); }

.legend-item { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; font-size: 0.8rem; }
.legend-dot  { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }
.legend-sq   { width: 12px; height: 12px; flex-shrink: 0; }

.opportunity-bar { height: 8px; border-radius: 4px; margin: 4px 0; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
DATA_PATHS = [
    os.path.join(os.path.dirname(__file__), "SmartBiz_Surakarta_With_Coords.csv"),
    "SmartBiz_Surakarta_With_Coords.csv",
    "/mnt/user-data/uploads/SmartBiz_Surakarta_With_Coords.csv",
]

@st.cache_data(show_spinner=False)
def load_data():
    for path in DATA_PATHS:
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                df["Total_UMKM"] = (
                    df["Jumlah_UMKM_Kuliner"]
                    + df["Jumlah_UMKM_Jasa"]
                    + df["Jumlah_UMKM_Retail"]
                )
                df["Skor_Peluang"] = (
                    df["Jumlah_Penduduk"] / (df["Total_UMKM"] + 1)
                ).round(2)
                return df
            except Exception as e:
                st.error(f"Gagal membaca data: {e}")
    return None

df_raw = load_data()

if df_raw is None:
    st.error("⚠️ File data tidak ditemukan. Pastikan `SmartBiz_Surakarta_With_Coords.csv` ada di direktori yang sama.")
    st.stop()

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────

# Institusi pendidikan di Surakarta — universitas & sekolah
EDU_MARKERS = [
    # ── Perguruan Tinggi ──
    {"name": "UNS – Univ. Sebelas Maret",           "lat": -7.5589, "lon": 110.8561, "type": "universitas", "color": "#3ABEF9"},
    {"name": "UMS – Univ. Muhammadiyah Surakarta",  "lat": -7.5527, "lon": 110.7719, "type": "universitas", "color": "#A7FF83"},
    {"name": "UIN Raden Mas Said Surakarta",         "lat": -7.5606, "lon": 110.7735, "type": "universitas", "color": "#FFD700"},
    {"name": "UNISRI Surakarta",                     "lat": -7.5671, "lon": 110.8310, "type": "universitas", "color": "#C678DD"},
    {"name": "ISI Surakarta",                        "lat": -7.5528, "lon": 110.8480, "type": "universitas", "color": "#FF8C42"},
    {"name": "Univ. Tunas Pembangunan (UTP)",        "lat": -7.5490, "lon": 110.8050, "type": "universitas", "color": "#F7768E"},
    # ── SMA / SMK ──
    {"name": "SMA Negeri 1 Surakarta",               "lat": -7.5632, "lon": 110.8185, "type": "sekolah", "color": "#89DCEB"},
    {"name": "SMA Negeri 2 Surakarta",               "lat": -7.5660, "lon": 110.8280, "type": "sekolah", "color": "#89DCEB"},
    {"name": "SMA Negeri 3 Surakarta",               "lat": -7.5582, "lon": 110.8215, "type": "sekolah", "color": "#89DCEB"},
    {"name": "SMA Negeri 4 Surakarta",               "lat": -7.5598, "lon": 110.8302, "type": "sekolah", "color": "#89DCEB"},
    {"name": "SMA Negeri 5 Surakarta",               "lat": -7.5495, "lon": 110.8115, "type": "sekolah", "color": "#89DCEB"},
    {"name": "SMA Batik 1 Surakarta",                "lat": -7.5738, "lon": 110.8185, "type": "sekolah", "color": "#89DCEB"},
    {"name": "SMK Negeri 2 Surakarta",               "lat": -7.5669, "lon": 110.8254, "type": "sekolah", "color": "#89DCEB"},
    {"name": "SMK Warga Surakarta",                  "lat": -7.5607, "lon": 110.8330, "type": "sekolah", "color": "#89DCEB"},
    {"name": "SMA MTA Surakarta",                    "lat": -7.5488, "lon": 110.8178, "type": "sekolah", "color": "#89DCEB"},
]

SKENARIO_COLORS = {
    "Normal":      "#3ABEF9",
    "High Growth": "#A7FF83",
    "Low Growth":  "#FF6B6B",
}

BUSINESS_INFO = {
    "☕ Coffee Shop": {
        "col":    "Jumlah_Coffee_Shop",
        "icon":   "☕",
        "color":  "#B5885B",
        "label":  "Coffee Shop",
        "desc":   "Kedai kopi, minuman kekinian, boba, dll.",
        "target": "Pelajar & mahasiswa, pekerja muda, komunitas kreatif",
        "modal":  "Rp 15 jt – 50 jt",
        "tips":   [
            "Lokasi dekat kampus atau SMA sangat menguntungkan",
            "Cari kelurahan dengan jumlah Coffee Shop sedikit tapi kepadatan tinggi",
            "Lalu lintas tinggi → potensi pelanggan impulsif lebih besar",
        ],
    },
    "🧺 Laundry": {
        "col":    "Jumlah_Laundry",
        "icon":   "🧺",
        "color":  "#7DCFFF",
        "label":  "Laundry",
        "desc":   "Laundry kiloan, express, antar-jemput.",
        "target": "Mahasiswa kos, keluarga muda, pekerja",
        "modal":  "Rp 10 jt – 25 jt",
        "tips":   [
            "Ideal di dekat kawasan kos-kosan & kampus",
            "Kelurahan padat penduduk dengan laundry sedikit = peluang emas",
            "Servis antar-jemput memberi keunggulan kompetitif",
        ],
    },
    "🍜 Kuliner / Warung Makan": {
        "col":    "Jumlah_UMKM_Kuliner",
        "icon":   "🍜",
        "color":  "#FF9E64",
        "label":  "Kuliner",
        "desc":   "Warung makan, restoran, katering, jajanan.",
        "target": "Semua kalangan, karyawan, mahasiswa, keluarga",
        "modal":  "Rp 5 jt – 30 jt",
        "tips":   [
            "Volume lalu lintas harian = indikator potensi pelanggan",
            "Area perkantoran, sekolah, & kampus sangat potensial",
            "Diferensiasi menu dari kompetitor adalah kunci",
        ],
    },
    "🛒 Retail / Toko": {
        "col":    "Jumlah_UMKM_Retail",
        "icon":   "🛒",
        "color":  "#9ECE6A",
        "label":  "Retail",
        "desc":   "Toko kelontong, minimarket, toko fashion, aksesoris.",
        "target": "Warga sekitar, ibu rumah tangga, pelajar",
        "modal":  "Rp 10 jt – 100 jt",
        "tips":   [
            "Aksesibilitas jalan & kepadatan penduduk sangat menentukan",
            "Spesialisasi produk membantu bersaing dengan minimarket besar",
            "Perhatikan indeks harga properti untuk menilai biaya sewa",
        ],
    },
    "🔧 Jasa (Salon/Bengkel/dll)": {
        "col":    "Jumlah_UMKM_Jasa",
        "icon":   "🔧",
        "color":  "#BB9AF7",
        "label":  "Jasa",
        "desc":   "Bengkel, salon, fotografi, laundry, service elektronik.",
        "target": "Komunitas lokal, profesional, rumah tangga",
        "modal":  "Rp 5 jt – 50 jt",
        "tips":   [
            "Cari niche/spesialisasi yang belum banyak di area tersebut",
            "Area residensial padat cocok untuk jasa harian (salon, bengkel)",
            "Tingkat pendapatan rata-rata mempengaruhi daya beli jasa",
        ],
    },
}

SECTOR_LABELS = {
    "Coffee Shop": "Jumlah_Coffee_Shop",
    "Laundry":     "Jumlah_Laundry",
    "Kuliner":     "Jumlah_UMKM_Kuliner",
    "Jasa":        "Jumlah_UMKM_Jasa",
    "Retail":      "Jumlah_UMKM_Retail",
}
SECTOR_COLORS = ["#B5885B", "#7DCFFF", "#FF9E64", "#BB9AF7", "#9ECE6A"]

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size:2rem;">🏙️</div>
        <h2>SmartBiz Analytics</h2>
        <p>SURAKARTA · UMKM INTELLIGENCE</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Filter Jenis Usaha (NEW FEATURE) ──
    st.markdown("### 🏪 Jenis Usaha yang Ingin Dibuka")
    selected_biz = st.selectbox(
        "Pilih jenis usaha:",
        list(BUSINESS_INFO.keys()),
        help="Pilih jenis usaha yang ingin Anda buka untuk mendapatkan rekomendasi lokasi terbaik.",
    )
    biz_info = BUSINESS_INFO[selected_biz]

    st.markdown("### 📍 Filter Wilayah")
    kecamatan_list = sorted(df_raw["Kecamatan"].dropna().unique().tolist())
    selected_kec   = st.selectbox("Kecamatan", kecamatan_list, index=0)

    kelurahan_list = sorted(
        df_raw.loc[df_raw["Kecamatan"] == selected_kec, "Kelurahan"].dropna().unique().tolist()
    )
    selected_kel = st.selectbox("Kelurahan (opsional)", kelurahan_list, index=0)

    st.markdown("### 📈 Skenario Ekonomi")
    skenario_idx = st.select_slider(
        "Pilih Skenario",
        options=["High Growth", "Normal", "Low Growth"],
        value="Normal",
        help="Normal: kondisi ekonomi rata-rata. High Growth: pertumbuhan tinggi. Low Growth: pertumbuhan lambat.",
    )

    st.markdown("### 📅 Tahun Data")
    tahun_opts    = sorted(df_raw["Tahun"].unique().tolist())
    selected_tahun = st.selectbox("Tahun", tahun_opts, index=len(tahun_opts)-1)

    st.markdown("---")

    # Tombol analisis
    run_analysis = st.button("⚡ Analisis & Rekomendasi")

    # Legenda peta di sidebar
    st.markdown("---")
    st.markdown("**🗺️ Legenda Peta**")
    st.markdown("""
    <div style="font-size:0.75rem;color:#7F849C;line-height:1.9;">
    <div class="legend-item"><div class="legend-dot" style="background:#A7FF83;"></div> Peluang Tinggi (Skor ≥ 100)</div>
    <div class="legend-item"><div class="legend-dot" style="background:#3ABEF9;"></div> Peluang Sedang (Skor 50–99)</div>
    <div class="legend-item"><div class="legend-dot" style="background:#FF6B6B;"></div> Area Padat Kompetitor (< 50)</div>
    <div class="legend-item"><div style="font-size:14px;">🎓</div> Perguruan Tinggi</div>
    <div class="legend-item"><div style="font-size:14px;">🏫</div> SMA / SMK</div>
    <div class="legend-item"><div style="font-size:14px;">🔥</div> Heatmap Kepadatan Populasi</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────
df_kec = df_raw[
    (df_raw["Kecamatan"] == selected_kec) &
    (df_raw["Skenario_Ekonomi"] == skenario_idx) &
    (df_raw["Tahun"] == selected_tahun)
].copy()

df_kel = df_kec[df_kec["Kelurahan"] == selected_kel].copy()

df_map = df_raw[
    (df_raw["Skenario_Ekonomi"] == skenario_idx) &
    (df_raw["Tahun"] == selected_tahun)
].copy()

# Hitung skor peluang SPESIFIK untuk jenis usaha yang dipilih
biz_col = biz_info["col"]
df_map["Skor_Bisnis"] = (df_map["Jumlah_Penduduk"] / (df_map[biz_col] + 1)).round(2)
df_kec["Skor_Bisnis"] = (df_kec["Jumlah_Penduduk"] / (df_kec[biz_col] + 1)).round(2)

# ─────────────────────────────────────────────
# HERO BANNER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-glow"></div>
    <h1>🏙️ SmartBiz Analytics Surakarta</h1>
    <p>Platform Prediksi Peluang Bisnis UMKM berbasis data spasial · Temukan lokasi terbaik untuk usaha Anda di Kota Solo</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PANDUAN MEMBACA DASHBOARD (collapsible)
# ─────────────────────────────────────────────
with st.expander("📖 Panduan Membaca Dashboard — Klik untuk membuka", expanded=False):
    st.markdown("""
    <div class="guide-box">
    <h4>🎯 Apa itu SmartBiz Analytics?</h4>
    <p>Platform ini membantu Anda menemukan <b>lokasi terbaik</b> untuk membuka usaha UMKM di Kota Surakarta,
    berdasarkan data populasi, kepadatan kompetitor, aksesibilitas, dan potensi pasar.</p>

    <h4>📊 Cara Membaca Metrik Utama</h4>
    <ul>
    <li><b>👥 Total Penduduk</b> — Jumlah warga di kelurahan tersebut. Makin banyak = pasar potensial lebih besar.</li>
    <li><b>💰 Rata-Rata Pendapatan</b> — Pendapatan per kapita warga. Makin tinggi = daya beli lebih kuat.</li>
    <li><b>🏪 Total UMKM</b> — Jumlah usaha yang sudah ada. Tinggi = persaingan ketat, perlu diferensiasi.</li>
    <li><b>⭐ Skor Peluang Bisnis</b> — Rasio Penduduk ÷ Jumlah Usaha. <b>Makin tinggi = persaingan makin rendah = peluang lebih terbuka.</b>
    Skor ≥ 100 (Hijau🟢), 50–99 (Biru🔵), di bawah 50 (Merah🔴).</li>
    </ul>

    <h4>🗺️ Cara Membaca Peta</h4>
    <ul>
    <li><b>Lingkaran berwarna</b> = lokasi kelurahan, warna menunjukkan tingkat peluang bisnis.</li>
    <li><b>🎓 Ikon wisuda</b> = perguruan tinggi (universitas). <b>🏫 Ikon sekolah</b> = SMA/SMK terdekat.</li>
    <li><b>Heatmap merah-kuning</b> = area dengan kepadatan penduduk tinggi.</li>
    <li>Klik lingkaran untuk melihat detail kelurahan + link Google Maps.</li>
    </ul>

    <h4>📈 Cara Membaca Chart</h4>
    <ul>
    <li><b>Bar Chart Sektor</b> — Membandingkan jumlah usaha per sektor di kecamatan yang dipilih.</li>
    <li><b>Radar Profil</b> — Gambaran keunggulan/kelemahan kelurahan dari 5 dimensi: kepadatan, pendapatan, usia produktif, aksesibilitas, dan lalu lintas.</li>
    <li><b>Trend Tahunan</b> — Pertumbuhan jumlah usaha dari 2023–2026 berdasarkan skenario ekonomi.</li>
    </ul>

    <h4>🤖 Cara Membaca Rekomendasi</h4>
    <ul>
    <li>Rekomendasi dihasilkan otomatis berdasarkan data. Pilih <b>jenis usaha</b> di sidebar, lalu klik <b>⚡ Analisis</b>.</li>
    <li>Top 5 Kelurahan terbaik untuk jenis usaha yang dipilih akan ditampilkan beserta link Google Maps.</li>
    </ul>

    <h4>⚙️ Skenario Ekonomi</h4>
    <ul>
    <li><b>High Growth</b> — Skenario optimis, ekonomi tumbuh pesat, daya beli meningkat.</li>
    <li><b>Normal</b> — Kondisi ekonomi rata-rata, pertumbuhan stabil.</li>
    <li><b>Low Growth</b> — Skenario hati-hati, pertumbuhan lambat, persaingan lebih ketat.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INFO JENIS USAHA YANG DIPILIH
# ─────────────────────────────────────────────
st.markdown(f'<div class="section-header">{biz_info["icon"]} Jenis Usaha yang Dipilih: {biz_info["label"]}</div>', unsafe_allow_html=True)

col_biz1, col_biz2, col_biz3 = st.columns([2, 2, 3])
with col_biz1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">📋 Deskripsi Usaha</div>
        <div style="font-size:0.9rem;color:#CDD6F4;margin-top:0.5rem;">{biz_info["desc"]}</div>
        <div class="hint">💰 Estimasi Modal Awal: <b>{biz_info["modal"]}</b></div>
    </div>""", unsafe_allow_html=True)
with col_biz2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">🎯 Target Pelanggan</div>
        <div style="font-size:0.85rem;color:#CDD6F4;margin-top:0.5rem;line-height:1.5;">{biz_info["target"]}</div>
    </div>""", unsafe_allow_html=True)
with col_biz3:
    tips_html = "".join([f"<li>{t}</li>" for t in biz_info["tips"]])
    st.markdown(f"""
    <div class="metric-card" style="text-align:left;">
        <div class="label">💡 Tips Memilih Lokasi</div>
        <ul style="font-size:0.8rem;color:#7F849C;margin-top:0.5rem;padding-left:1.2rem;line-height:1.7;">
        {tips_html}
        </ul>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# METRIC CARDS
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">📊 Ringkasan Metrik Wilayah Terpilih</div>', unsafe_allow_html=True)

if df_kel.empty:
    st.warning(f"⚠️ Data untuk Kelurahan **{selected_kel}** pada skenario **{skenario_idx}** tidak tersedia.")
    total_pop = avg_income = total_umkm = opp_score = kepadatan = usia_prod = 0
    biz_count = biz_skor = 0
else:
    total_pop   = int(df_kel["Jumlah_Penduduk"].mean())
    avg_income  = float(df_kel["Rata_Rata_Pendapatan"].mean())
    total_umkm  = int(df_kel["Total_UMKM"].mean())
    opp_score   = float(df_kel["Skor_Peluang"].mean())
    kepadatan   = int(df_kel["Kepadatan_Penduduk"].mean())
    usia_prod   = float(df_kel["Persentase_Usia_Produktif"].mean())
    biz_count   = int(df_kel[biz_col].mean())
    # Cek dulu apakah kolomnya ada
if "Skor_Bisnis" in df_kel.columns:
    biz_skor = float(df_kel["Skor_Bisnis"].mean())
else:
    print("Kolom Skor_Bisnis tidak ditemukan! Kolom yang ada adalah:", df_kel.columns.tolist())
    biz_skor = 0.0  # Nilai default jika kolom tidak ada

if opp_score >= 100:
    score_class, score_icon = "value-mint",  "🔥"
elif opp_score >= 50:
    score_class, score_icon = "value-blue",  "✅"
else:
    score_class, score_icon = "value-coral", "⚠️"

if biz_skor >= 500:
    biz_class = "value-mint"
elif biz_skor >= 200:
    biz_class = "value-blue"
else:
    biz_class = "value-coral"

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">👥 Total Penduduk</div>
        <div class="value value-blue">{total_pop:,}</div>
        <div class="sub">jiwa</div>
        <div class="hint">Potensi calon pelanggan di wilayah ini</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">💰 Rata-Rata Pendapatan</div>
        <div class="value value-mint">Rp {avg_income/1_000_000:.1f}jt</div>
        <div class="sub">per bulan / kapita</div>
        <div class="hint">Indikator daya beli masyarakat</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">🏪 Total UMKM Aktif</div>
        <div class="value value-coral">{total_umkm:,}</div>
        <div class="sub">unit usaha</div>
        <div class="hint">Makin tinggi = persaingan makin ketat</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">{score_icon} Skor Peluang Umum</div>
        <div class="value {score_class}">{opp_score:.1f}</div>
        <div class="sub">Penduduk ÷ (UMKM+1)</div>
        <div class="hint">≥100🟢 Tinggi | 50–99🔵 Sedang | &lt;50🔴 Padat</div>
    </div>""", unsafe_allow_html=True)
with c5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">{biz_info["icon"]} Pesaing {biz_info["label"]}</div>
        <div class="value {biz_class}">{biz_count}</div>
        <div class="sub">unit di kelurahan ini</div>
        <div class="hint">Skor khusus: {biz_skor:.0f} — makin tinggi = lebih sedikit pesaing</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PETA
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">🗺️ Peta Spasial UMKM, Pendidikan & Peluang Bisnis</div>', unsafe_allow_html=True)

# Keterangan peta
st.caption(
    "💡 **Cara baca peta:** Lingkaran berwarna = kelurahan (hijau=peluang tinggi, biru=sedang, merah=padat). "
    "🎓 = Perguruan Tinggi. 🏫 = SMA/SMK. 🔥 Heatmap = kepadatan penduduk. "
    "**Klik marker untuk detail & link Google Maps.**"
)

def haversine_km(lat1, lon1, lat2, lon2):
    """Hitung jarak (km) antara dua titik koordinat."""
    R = 6371
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
    return R * 2 * np.arcsin(np.sqrt(a))

def nearest_edu(lat: float, lon: float, edu_type: str = None):
    """Cari institusi pendidikan terdekat."""
    markers = [m for m in EDU_MARKERS if (edu_type is None or m["type"] == edu_type)]
    if not markers:
        return None, None
    dists = [(haversine_km(lat, lon, m["lat"], m["lon"]), m) for m in markers]
    dists.sort(key=lambda x: x[0])
    return dists[0][1]["name"], round(dists[0][0], 2)

def build_map(df_map_data: pd.DataFrame, highlight_kel: str, biz_col_name: str) -> folium.Map:
    center_lat = df_map_data["Latitude"].mean()
    center_lon = df_map_data["Longitude"].mean()

    m = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles=None)

    # Tile layers
    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        attr="CartoDB", name="🌑 Mode Gelap", control=True
    ).add_to(m)
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google Satellite', name='🛰️ Google Satelit', control=True
    ).add_to(m)
    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        attr="CartoDB", name="☀️ Mode Terang", control=True
    ).add_to(m)

    # Heatmap kepadatan penduduk
    heat_data = df_map_data[["Latitude", "Longitude", "Kepadatan_Penduduk"]].dropna()
    if not heat_data.empty:
        HeatMap(
            heat_data.values.tolist(),
            name="🔥 Heatmap Kepadatan Penduduk",
            radius=30, blur=25,
            gradient={0.2: "#3ABEF9", 0.5: "#A7FF83", 0.8: "#FFD700", 1.0: "#FF6B6B"},
        ).add_to(m)

    # Cluster UMKM
    cluster = MarkerCluster(name="🏪 Titik Kelurahan (Klik untuk detail)").add_to(m)
    for _, row in df_map_data.iterrows():
        if pd.isna(row["Latitude"]) or pd.isna(row["Longitude"]):
            continue

        skor      = row.get("Skor_Peluang", 50)
        biz_score = row.get("Skor_Bisnis", 50)
        umkm      = row.get("Total_UMKM", 0)
        kompetitor = int(row.get(biz_col_name, 0))
        is_kel    = row["Kelurahan"] == highlight_kel
        lat, lon  = row["Latitude"], row["Longitude"]

        color = "#A7FF83" if skor >= 100 else ("#3ABEF9" if skor >= 50 else "#FF6B6B")
        radius = 12 if is_kel else 7
        weight = 3  if is_kel else 1

        # Cari universitas & sekolah terdekat
        univ_name, univ_km = nearest_edu(lat, lon, "universitas")
        sch_name, sch_km   = nearest_edu(lat, lon, "sekolah")
        univ_info = f"{univ_name} ({univ_km} km)" if univ_name else "—"
        sch_info  = f"{sch_name} ({sch_km} km)" if sch_name else "—"

        gmaps_url = f"https://www.google.com/maps?q={lat},{lon}"
        gmaps_search = f"https://maps.google.com/?q=Kelurahan+{row['Kelurahan']}+{row['Kecamatan']}+Surakarta"

        # Badge skor
        if skor >= 100:
            badge_col, badge_txt = "#A7FF83", "🔥 Peluang Tinggi"
        elif skor >= 50:
            badge_col, badge_txt = "#3ABEF9", "✅ Peluang Sedang"
        else:
            badge_col, badge_txt = "#FF6B6B", "⚠️ Padat Kompetitor"

        popup_html = f"""
        <div style="font-family:'Segoe UI',sans-serif;min-width:240px;background:#1E1E2E;
                    color:#CDD6F4;padding:14px;border-radius:12px;font-size:12px;line-height:1.7;">
            <b style="color:#3ABEF9;font-size:14px;">{row['Kelurahan']}</b><br>
            <span style="color:#7F849C;font-size:11px;">{row['Kecamatan']} · {row.get('Tahun','')}</span>
            <span style="background:{badge_col};color:#1E1E2E;font-size:10px;font-weight:700;
                  padding:1px 7px;border-radius:10px;margin-left:6px;">{badge_txt}</span>
            <hr style="border-color:#313244;margin:8px 0">
            👥 <b>Penduduk:</b> {int(row['Jumlah_Penduduk']):,} jiwa<br>
            💰 <b>Pendapatan:</b> Rp {int(row['Rata_Rata_Pendapatan'])/1e6:.1f} jt/bln<br>
            🏪 <b>Total UMKM:</b> {int(umkm):,} unit<br>
            {biz_info["icon"]} <b>Pesaing {biz_info["label"]}:</b> <span style="color:#FF9E64">{kompetitor}</span><br>
            ⭐ <b>Skor Peluang:</b> <span style="color:#A7FF83">{skor:.1f}</span>
            &nbsp;&nbsp;|&nbsp;&nbsp;
            🎯 <b>Skor {biz_info["label"]}:</b> <span style="color:#FFD700">{biz_score:.0f}</span>
            <hr style="border-color:#313244;margin:8px 0">
            🎓 <b>Univ. Terdekat:</b> {univ_info}<br>
            🏫 <b>SMA Terdekat:</b> {sch_info}
            <hr style="border-color:#313244;margin:8px 0">
            <a href="{gmaps_url}" target="_blank"
               style="background:#34A853;color:#fff;font-weight:700;font-size:11px;
                      padding:4px 10px;border-radius:6px;text-decoration:none;margin-right:5px;">
               📍 Buka di Maps (Koordinat)
            </a>
            <a href="{gmaps_search}" target="_blank"
               style="background:#4285F4;color:#fff;font-weight:700;font-size:11px;
                      padding:4px 10px;border-radius:6px;text-decoration:none;">
               🔍 Cari di Maps
            </a>
        </div>"""

        folium.CircleMarker(
            location=[lat, lon],
            radius=radius, color=color, fill=True,
            fill_color=color, fill_opacity=0.85, weight=weight,
            popup=folium.Popup(popup_html, max_width=280),
            tooltip=f"{'⭐ ' if is_kel else ''}{row['Kelurahan']} | Skor: {skor:.1f} | {biz_info['icon']}: {kompetitor} unit",
        ).add_to(cluster)

    # Institusi Pendidikan
    univ_group = folium.FeatureGroup(name="🎓 Perguruan Tinggi")
    school_group = folium.FeatureGroup(name="🏫 SMA / SMK")

    for edu in EDU_MARKERS:
        gmaps_edu = f"https://www.google.com/maps/search/{edu['name'].replace(' ', '+')}"

        if edu["type"] == "universitas":
            icon_html = f"""
            <div style="background:{edu['color']};width:34px;height:34px;border-radius:50%;
                        display:flex;align-items:center;justify-content:center;
                        font-size:16px;border:2px solid #fff;box-shadow:0 3px 10px rgba(0,0,0,0.5);">🎓</div>"""
            popup_html = f"""
            <div style="font-family:'Segoe UI',sans-serif;background:#1E1E2E;color:#CDD6F4;
                        padding:12px;border-radius:10px;font-size:12px;min-width:200px;">
                <b style="color:{edu['color']};font-size:13px;">🎓 {edu['name']}</b><br>
                <span style="color:#7F849C">Perguruan Tinggi · Surakarta</span><br>
                <hr style="border-color:#313244;margin:7px 0">
                <a href="{gmaps_edu}" target="_blank"
                   style="background:#34A853;color:#fff;font-weight:700;font-size:11px;
                          padding:3px 9px;border-radius:6px;text-decoration:none;">
                   📍 Lihat di Google Maps
                </a>
            </div>"""
            folium.Marker(
                location=[edu["lat"], edu["lon"]],
                popup=folium.Popup(popup_html, max_width=240),
                tooltip=f"🎓 {edu['name']}",
                icon=folium.DivIcon(html=icon_html, icon_size=(34, 34), icon_anchor=(17, 17)),
            ).add_to(univ_group)
        else:
            icon_html = f"""
            <div style="background:#89DCEB;width:28px;height:28px;border-radius:6px;
                        display:flex;align-items:center;justify-content:center;
                        font-size:14px;border:2px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,0.4);">🏫</div>"""
            popup_html = f"""
            <div style="font-family:'Segoe UI',sans-serif;background:#1E1E2E;color:#CDD6F4;
                        padding:12px;border-radius:10px;font-size:12px;min-width:190px;">
                <b style="color:#89DCEB;font-size:13px;">🏫 {edu['name']}</b><br>
                <span style="color:#7F849C">SMA / SMK · Surakarta</span><br>
                <hr style="border-color:#313244;margin:7px 0">
                <a href="{gmaps_edu}" target="_blank"
                   style="background:#34A853;color:#fff;font-weight:700;font-size:11px;
                          padding:3px 9px;border-radius:6px;text-decoration:none;">
                   📍 Lihat di Google Maps
                </a>
            </div>"""
            folium.Marker(
                location=[edu["lat"], edu["lon"]],
                popup=folium.Popup(popup_html, max_width=230),
                tooltip=f"🏫 {edu['name']}",
                icon=folium.DivIcon(html=icon_html, icon_size=(28, 28), icon_anchor=(14, 14)),
            ).add_to(school_group)

    univ_group.add_to(m)
    school_group.add_to(m)
    folium.LayerControl(position="topright", collapsed=False).add_to(m)
    return m

with st.container():
    st.markdown('<div class="map-wrapper">', unsafe_allow_html=True)
    fmap = build_map(df_map, selected_kel, biz_col)
    st_folium(fmap, width="100%", height=500, returned_objects=[])
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">📈 Analisis Sektor & Profil Demografi</div>', unsafe_allow_html=True)

col_bar, col_radar = st.columns([1, 1], gap="large")

with col_bar:
    st.markdown(f"#### 🏪 Jumlah UMKM per Sektor — Kec. {selected_kec}")
    st.caption("Bar ini menunjukkan total unit usaha per sektor di kecamatan yang dipilih. Sektor dengan bar **lebih pendek** = persaingan lebih sedikit = **lebih terbuka untuk usaha baru**.")

    if df_kec.empty:
        st.info("Data kecamatan tidak tersedia.")
    else:
        sector_means = {label: int(df_kec[col].sum()) for label, col in SECTOR_LABELS.items()}
        # Highlight bar sektor yang dipilih
        bar_colors = []
        for label in sector_means.keys():
            if label == biz_info["label"]:
                bar_colors.append(biz_info["color"])
            else:
                bar_colors.append("#4A4E69")

        bar_fig = go.Figure(go.Bar(
            x=list(sector_means.keys()),
            y=list(sector_means.values()),
            marker=dict(color=bar_colors, line=dict(color="rgba(0,0,0,0)", width=0)),
            text=[f"{v:,}" for v in sector_means.values()],
            textposition="outside",
            textfont=dict(color="#CDD6F4", size=11),
        ))
        bar_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#CDD6F4"),
            xaxis=dict(gridcolor="#313244", tickfont=dict(size=11)),
            yaxis=dict(gridcolor="#313244", tickfont=dict(size=11), title="Jumlah Unit"),
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False, height=300,
            annotations=[dict(
                text=f"← Bar berwarna = sektor {biz_info['label']} yang Anda pilih",
                xref="paper", yref="paper", x=0.5, y=1.05,
                showarrow=False, font=dict(size=10, color="#7F849C"), xanchor="center"
            )]
        )
        st.plotly_chart(bar_fig, use_container_width=True, config={"displayModeBar": False})

with col_radar:
    st.markdown(f"#### 🎯 Radar Profil — Kel. {selected_kel}")
    st.caption("Grafik radar menampilkan 5 dimensi lokasi (0–100). **Nilai makin luar = makin baik** untuk membuka usaha di dimensi tersebut.")

    if df_kel.empty:
        st.info("Data kelurahan tidak tersedia.")
    else:
        radar_row = df_kel.iloc[0]

        def normalize(val, lo, hi):
            if hi == lo: return 50.0
            return max(0.0, min(100.0, (val - lo) / (hi - lo) * 100))

        cats = ["Kepadatan\nPenduduk", "Daya\nBeli", "Usia\nProduktif", "Aksesibilitas", "Lalu\nLintas"]
        vals_raw = [
            radar_row.get("Kepadatan_Penduduk", 0),
            radar_row.get("Rata_Rata_Pendapatan", 0),
            radar_row.get("Persentase_Usia_Produktif", 0),
            radar_row.get("Skor_Aksesibilitas", 0),
            radar_row.get("Volume_Lalu_Lintas_Harian", 0),
        ]
        ref_lo = [0,       1_000_000, 50,    0,  0]
        ref_hi = [50_000, 10_000_000, 85, 100, 60_000]
        vals_norm = [normalize(v, lo, hi) for v, lo, hi in zip(vals_raw, ref_lo, ref_hi)]
        vals_norm.append(vals_norm[0])
        cats_plot = cats + [cats[0]]

        radar_fig = go.Figure()
        radar_fig.add_trace(go.Scatterpolar(
            r=vals_norm, theta=cats_plot, fill="toself",
            fillcolor="rgba(58,190,249,0.15)",
            line=dict(color="#3ABEF9", width=2),
            marker=dict(color="#A7FF83", size=7),
            name="Profil Kelurahan"
        ))
        # Reference line 50
        radar_fig.add_trace(go.Scatterpolar(
            r=[50]*6, theta=cats_plot, mode="lines",
            line=dict(color="#313244", width=1, dash="dot"),
            name="Garis Referensi (50)"
        ))
        radar_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#CDD6F4", size=11),
            polar=dict(
                bgcolor="rgba(30,30,46,0.5)",
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="#313244",
                               linecolor="#313244", tickfont=dict(size=9, color="#7F849C"),
                               tickvals=[25, 50, 75, 100]),
                angularaxis=dict(gridcolor="#313244", linecolor="#313244", tickfont=dict(size=10)),
            ),
            margin=dict(l=40, r=40, t=40, b=40), height=300,
            showlegend=True,
            legend=dict(font=dict(size=9, color="#7F849C"), bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(radar_fig, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
# TREND CHART
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">📅 Tren Pertumbuhan UMKM (2023–2026)</div>', unsafe_allow_html=True)
st.caption(f"Grafik ini menampilkan proyeksi pertumbuhan jumlah usaha **{biz_info['label']}** di Kecamatan {selected_kec} berdasarkan 3 skenario ekonomi. Digunakan untuk menilai apakah persaingan akan makin ketat atau tidak.")

df_trend = df_raw[df_raw["Kecamatan"] == selected_kec].groupby(
    ["Tahun", "Skenario_Ekonomi"]
)[biz_col].sum().reset_index()

trend_fig = go.Figure()
for skenario, color in SKENARIO_COLORS.items():
    d = df_trend[df_trend["Skenario_Ekonomi"] == skenario]
    trend_fig.add_trace(go.Scatter(
        x=d["Tahun"], y=d[biz_col],
        mode="lines+markers+text",
        name=skenario,
        line=dict(color=color, width=2),
        marker=dict(size=7, color=color),
        text=[str(v) for v in d[biz_col]],
        textposition="top center",
        textfont=dict(size=10, color=color),
    ))
trend_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#CDD6F4"),
    xaxis=dict(title="Tahun", gridcolor="#313244", tickvals=tahun_opts),
    yaxis=dict(title=f"Total {biz_info['label']}", gridcolor="#313244"),
    legend=dict(
        title="Skenario Ekonomi",
        bgcolor="rgba(36,39,58,0.8)",
        bordercolor="#313244", borderwidth=1,
        font=dict(size=11)
    ),
    margin=dict(l=20, r=20, t=30, b=20), height=260,
    hovermode="x unified",
    annotations=[dict(
        text=f"💡 Garis naik = persaingan makin ketat. Perhatikan skenario yang Anda pilih.",
        xref="paper", yref="paper", x=0.5, y=1.08,
        showarrow=False, font=dict(size=10, color="#7F849C"), xanchor="center"
    )]
)
st.plotly_chart(trend_fig, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
# TOP 5 REKOMENDASI LOKASI
# ─────────────────────────────────────────────
st.markdown(f'<div class="section-header">🏆 Top 5 Kelurahan Terbaik untuk {biz_info["icon"]} {biz_info["label"]}</div>', unsafe_allow_html=True)
st.caption(
    f"Peringkat ini dihitung dari rasio **Penduduk ÷ (Jumlah {biz_info['label']} + 1)** "
    f"— semakin tinggi = semakin sedikit kompetitor per potensi pelanggan. "
    f"Skenario: **{skenario_idx}** · Tahun: **{selected_tahun}**"
)

top5_df = df_map.nlargest(5, "Skor_Bisnis")[
    ["Kelurahan", "Kecamatan", "Jumlah_Penduduk", biz_col, "Skor_Bisnis", "Skor_Peluang",
     "Rata_Rata_Pendapatan", "Jumlah_Sekolah_Kampus", "Latitude", "Longitude"]
].reset_index(drop=True)

max_skor = top5_df["Skor_Bisnis"].max()

col_r1, col_r2 = st.columns(2, gap="large")

for i, (_, row) in enumerate(top5_df.iterrows()):
    pct = int(row["Skor_Bisnis"] / max_skor * 100)
    rank_emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i]
    bar_color  = ["#FFD700","#C0C0C0","#CD7F32","#3ABEF9","#7F849C"][i]
    gmaps_url  = f"https://www.google.com/maps?q={row['Latitude']},{row['Longitude']}"
    gmaps_search = (
        f"https://maps.google.com/?q=Kelurahan+{row['Kelurahan']}+"
        f"{row['Kecamatan']}+Surakarta"
    )

    # Cari sekolah/univ terdekat
    univ_n, univ_d = nearest_edu(row["Latitude"], row["Longitude"], "universitas")
    sch_n, sch_d   = nearest_edu(row["Latitude"], row["Longitude"], "sekolah")
    univ_str = f"{univ_n} ({univ_d} km)" if univ_n else "—"
    sch_str  = f"{sch_n} ({sch_d} km)" if sch_n else "—"

    card_html = f"""
    <div class="biz-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div>
                <span class="rank">{rank_emoji}</span>
                <span class="kel-name"> {row['Kelurahan']}</span><br>
                <span class="kec-name">📍 Kec. {row['Kecamatan']}</span>
            </div>
            <div style="text-align:right;">
                <div style="font-size:1.3rem;font-weight:900;color:#A7FF83;">{row['Skor_Bisnis']:.0f}</div>
                <div style="font-size:0.65rem;color:#7F849C;">Skor {biz_info['label']}</div>
            </div>
        </div>
        <div style="background:#313244;border-radius:4px;height:6px;margin:8px 0;">
            <div style="background:{bar_color};width:{pct}%;height:6px;border-radius:4px;"></div>
        </div>
        <div class="stats">
            👥 {int(row['Jumlah_Penduduk']):,} jiwa &nbsp;|&nbsp;
            {biz_info['icon']} {int(row[biz_col])} pesaing &nbsp;|&nbsp;
            💰 Rp {row['Rata_Rata_Pendapatan']/1e6:.1f}jt<br>
            🎓 {univ_str}<br>
            🏫 {sch_str}
        </div>
        <a class="gmaps-btn" href="{gmaps_url}" target="_blank">📍 Google Maps (Koordinat)</a>
        &nbsp;
        <a class="gmaps-btn" href="{gmaps_search}" target="_blank"
           style="background:linear-gradient(135deg,#4285F4,#1A73E8);">🔍 Cari di Maps</a>
    </div>"""

    if i % 2 == 0:
        with col_r1:
            st.markdown(card_html, unsafe_allow_html=True)
    else:
        with col_r2:
            st.markdown(card_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# REKOMENDASI UTAMA
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">🤖 Rekomendasi SmartBiz untuk Kelurahan yang Dipilih</div>', unsafe_allow_html=True)

def get_best_sector(row: pd.Series) -> str:
    sector_cols = {
        "Coffee Shop": row.get("Jumlah_Coffee_Shop", 0),
        "Laundry":     row.get("Jumlah_Laundry", 0),
        "Kuliner":     row.get("Jumlah_UMKM_Kuliner", 0),
        "Retail":      row.get("Jumlah_UMKM_Retail", 0),
        "Jasa":        row.get("Jumlah_UMKM_Jasa", 0),
    }
    pop = row.get("Jumlah_Penduduk", 1)
    return max({k: pop / (v + 1) for k, v in sector_cols.items()}, key=lambda x: pop / (sector_cols[x] + 1))

if not df_kel.empty:
    row0       = df_kel.iloc[0]
    best_sec   = get_best_sector(row0)
    skor_val   = float(row0.get("Skor_Peluang", 0))
    biz_skor_v = float(row0.get("Skor_Bisnis", 0))
    kompetitor = int(row0.get(biz_col, 0))
    lat0, lon0 = row0.get("Latitude", -7.56), row0.get("Longitude", 110.82)

    univ_n, univ_d = nearest_edu(lat0, lon0, "universitas")
    sch_n, sch_d   = nearest_edu(lat0, lon0, "sekolah")
    univ_str = f"{univ_n} (~{univ_d} km)" if univ_n else "—"
    sch_str  = f"{sch_n} (~{sch_d} km)" if sch_n else "—"

    gmaps_kel = f"https://www.google.com/maps?q={lat0},{lon0}"
    gmaps_search_kel = f"https://maps.google.com/?q=Kelurahan+{selected_kel}+{selected_kec}+Surakarta"

    if skor_val >= 100:
        box_class = "high"; badge_txt = "🔥 Peluang Sangat Tinggi"
    elif skor_val >= 50:
        box_class = "medium"; badge_txt = "✅ Peluang Moderat"
    else:
        box_class = "low"; badge_txt = "⚠️ Area Padat Kompetitor"

    # Pesan khusus untuk jenis usaha yang dipilih
    if biz_skor_v >= 500:
        biz_msg = (f"Secara khusus untuk <strong>{biz_info['label']}</strong>, "
                   f"kelurahan ini sangat menjanjikan dengan hanya <strong>{kompetitor} unit pesaing</strong> "
                   f"dan skor peluang khusus <strong>{biz_skor_v:.0f}</strong>.")
    elif biz_skor_v >= 200:
        biz_msg = (f"Untuk <strong>{biz_info['label']}</strong>, persaingan di sini tergolong moderat "
                   f"(<strong>{kompetitor} unit</strong>). Masih ada ruang untuk masuk "
                   f"dengan diferensiasi yang tepat.")
    else:
        biz_msg = (f"Untuk <strong>{biz_info['label']}</strong>, persaingan di sini cukup ketat "
                   f"(<strong>{kompetitor} unit</strong>). "
                   f"Pertimbangkan strategi diferensiasi yang kuat atau lokasi lain di atas.")

    recommend_content = f"""
    <div class="recommend-box {box_class}">
        <span class="badge">{badge_txt}</span>
        <p>
        Kelurahan <strong>{selected_kel}</strong>, Kecamatan <strong>{selected_kec}</strong>
        memiliki skor peluang umum <strong>{skor_val:.1f}</strong> dalam skenario
        <strong>{skenario_idx}</strong> tahun <strong>{selected_tahun}</strong>.
        </p>
        <p>{biz_msg}</p>
        <p>
        📍 Lokasi ini berjarak <strong>{univ_d} km dari {univ_n}</strong> dan
        <strong>{sch_d} km dari {sch_n}</strong> — faktor strategis untuk usaha {biz_info['label']}.
        </p>
        <p>
        💡 Sektor dengan peluang terbuka paling lebar secara umum di wilayah ini:
        <strong>{best_sec}</strong>.
        </p>
        <div style="margin-top:1rem;display:flex;gap:10px;flex-wrap:wrap;">
            <a href="{gmaps_kel}" target="_blank"
               style="background:linear-gradient(135deg,#34A853,#0F9D58);color:#fff;
                      font-weight:700;font-size:0.75rem;padding:6px 14px;border-radius:8px;
                      text-decoration:none;">📍 Buka Google Maps (Koordinat)</a>
            <a href="{gmaps_search_kel}" target="_blank"
               style="background:linear-gradient(135deg,#4285F4,#1A73E8);color:#fff;
                      font-weight:700;font-size:0.75rem;padding:6px 14px;border-radius:8px;
                      text-decoration:none;">🔍 Cari Kelurahan di Maps</a>
        </div>
    </div>"""

    if run_analysis:
        st.markdown(
            f'<p style="color:#7F849C;font-size:0.8rem;">🤖 Analisis diperbarui untuk '
            f'<b>{selected_kel}</b> · {selected_kec} · {skenario_idx} · {selected_tahun}</p>',
            unsafe_allow_html=True
        )
    st.markdown(recommend_content, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="recommend-box medium">
        <span class="badge">⚠️ Data Tidak Tersedia</span>
        <p>Data untuk kelurahan yang dipilih tidak tersedia pada skenario dan tahun yang dipilih.
        Silakan ubah filter di sidebar.</p>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PELUANG USAHA SPESIFIK
# ─────────────────────────────────────────────
if run_analysis and not df_kel.empty:
    st.markdown('<div class="section-header">💼 Ide Peluang Usaha Berdasarkan Data</div>', unsafe_allow_html=True)

    row0 = df_kel.iloc[0]
    lalu_lintas = int(row0.get("Volume_Lalu_Lintas_Harian", 0))
    pendapatan  = float(row0.get("Rata_Rata_Pendapatan", 0))
    usia_prod_v = float(row0.get("Persentase_Usia_Produktif", 0))
    aksesibilitas = float(row0.get("Skor_Aksesibilitas", 0))
    jumlah_kes  = int(row0.get("Jumlah_Fasilitas_Kesehatan", 0))
    jumlah_bank = int(row0.get("Jumlah_Bank_ATM", 0))

    ide_list = []

    if biz_info["label"] == "Coffee Shop":
        if univ_d and univ_d < 3:
            ide_list.append(f"☕ **Kedai Kopi Belajar** — Dekat kampus ({univ_str}), buka area co-working untuk mahasiswa.")
        if lalu_lintas > 10000:
            ide_list.append(f"☕ **Drive-Thru Kopi** — Lalu lintas {lalu_lintas:,} kendaraan/hari sangat ideal untuk konsep grab-and-go.")
        if pendapatan > 5_000_000:
            ide_list.append(f"☕ **Specialty Coffee** — Daya beli Rp {pendapatan/1e6:.1f}jt/bln mendukung segmen premium.")
        ide_list.append("☕ **Kopi & Snack Kekinian** — Kombinasi menu minuman + makanan ringan memperluas segmen pelanggan.")

    elif biz_info["label"] == "Laundry":
        if univ_d and univ_d < 2:
            ide_list.append(f"🧺 **Laundry Kiloan Mahasiswa** — Kawasan dekat kampus ({univ_str}) = pasar kos-kosan stabil.")
        ide_list.append("🧺 **Laundry Express + Antar-Jemput** — Layanan cepat 3–4 jam + delivery meningkatkan harga jual.")
        ide_list.append("🧺 **Laundry Sepatu & Tas** — Niche yang belum banyak, margin lebih tinggi dari kiloan biasa.")
        if jumlah_kes > 5:
            ide_list.append("🧺 **Laundry Linen RS/Klinik** — Banyak fasilitas kesehatan di area ini = potensi kemitraan B2B.")

    elif biz_info["label"] == "Kuliner":
        if lalu_lintas > 15000:
            ide_list.append(f"🍜 **Warung Pinggir Jalan** — Lalu lintas {lalu_lintas:,}/hari = potensi besar pelanggan spontan.")
        if sch_d and sch_d < 1.5:
            ide_list.append(f"🍜 **Kantin / Warteg Pelajar** — Dekat {sch_str}, target pelajar dengan harga terjangkau.")
        ide_list.append("🍜 **Katering Harian / Nasi Kotak** — Layanan langganan harian untuk karyawan & mahasiswa.")
        if pendapatan > 6_000_000:
            ide_list.append("🍜 **Restoran Casual Dining** — Daya beli memadai untuk konsep makan bersama keluarga.")

    elif biz_info["label"] == "Retail":
        ide_list.append("🛒 **Toko Kebutuhan Harian** — Stok produk habis pakai (sembako, toiletries) = frekuensi beli tinggi.")
        if univ_d and univ_d < 3:
            ide_list.append(f"🛒 **Toko Alat Tulis & Fotokopi** — Dekat kampus ({univ_str}), kebutuhan akademik stabil.")
        if lalu_lintas > 10000:
            ide_list.append("🛒 **Toko Oleh-Oleh / Souvenir Solo** — Arus kendaraan tinggi cocok untuk toko impulsif.")
        ide_list.append("🛒 **Toko Online + Pickup Point** — Modal lebih rendah, kombinasi online-offline mengurangi risiko.")

    elif biz_info["label"] == "Jasa":
        ide_list.append("🔧 **Jasa Servis Elektronik** — Niche spesifik (HP, laptop) dengan margin perbaikan yang baik.")
        if usia_prod_v > 65:
            ide_list.append(f"💆 **Salon & Perawatan Tubuh** — {usia_prod_v:.1f}% penduduk usia produktif = pasar aktif untuk grooming.")
        if jumlah_bank > 5:
            ide_list.append("📸 **Jasa Fotografi & Printing** — Banyak bank/ATM di sekitar = area komersial aktif.")
        ide_list.append("🔧 **Jasa Kebersihan Rumah** — Layanan cleaning berbasis aplikasi semakin diminati keluarga muda.")

    if ide_list:
        cols_ide = st.columns(min(len(ide_list), 2))
        for j, ide in enumerate(ide_list[:4]):
            with cols_ide[j % 2]:
                st.markdown(f"""
                <div class="metric-card" style="text-align:left;padding:1rem 1.25rem;">
                    <div style="font-size:0.88rem;color:#CDD6F4;line-height:1.6;">{ide}</div>
                </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABEL DATA LENGKAP (expandable)
# ─────────────────────────────────────────────
with st.expander("📋 Lihat Tabel Data Lengkap — Klik untuk membuka", expanded=False):
    st.caption(
        "Tabel ini menampilkan semua data kelurahan yang tersedia sesuai filter yang dipilih. "
        "Anda dapat mengurutkan kolom dengan mengklik header kolom."
    )
    display_cols = [
        "Kelurahan", "Kecamatan", "Jumlah_Penduduk", "Rata_Rata_Pendapatan",
        "Total_UMKM", biz_col, "Skor_Bisnis", "Skor_Peluang",
        "Jumlah_Sekolah_Kampus", "Skor_Aksesibilitas", "Volume_Lalu_Lintas_Harian"
    ]
    existing_cols = [c for c in display_cols if c in df_map.columns]
    df_show = df_map[existing_cols].sort_values("Skor_Bisnis", ascending=False).reset_index(drop=True)
    df_show.index = df_show.index + 1

    col_rename = {
        "Jumlah_Penduduk": "Penduduk",
        "Rata_Rata_Pendapatan": "Pendapatan (Rp)",
        "Total_UMKM": "Total UMKM",
        biz_col: f"Pesaing {biz_info['label']}",
        "Skor_Bisnis": f"Skor {biz_info['label']}",
        "Skor_Peluang": "Skor Umum",
        "Jumlah_Sekolah_Kampus": "Sekolah/Kampus",
        "Skor_Aksesibilitas": "Aksesibilitas",
        "Volume_Lalu_Lintas_Harian": "Lalu Lintas/Hari",
    }
    st.dataframe(
        df_show.rename(columns=col_rename),
        use_container_width=True, height=350
    )

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2.5rem 0 1rem;color:#313244;font-size:0.72rem;
            letter-spacing:0.08em;border-top:1px solid #313244;margin-top:2rem;">
    SmartBiz Analytics Surakarta v2.0 &nbsp;·&nbsp; Built with Streamlit &amp; Spatial Intelligence
    &nbsp;·&nbsp; Data: UMKM Surakarta 2023–2026
    &nbsp;·&nbsp; 🗺️ Peta terintegrasi Google Maps
</div>
""", unsafe_allow_html=True)