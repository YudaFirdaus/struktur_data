# ============================================================
# SKYGRAF — app.py
# Aplikasi Streamlit visualisasi jaringan penerbangan
# Asia Tenggara berbasis Weighted Directed Graph
# ============================================================

import json
import os

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Circle, FancyBboxPatch
import networkx as nx
import numpy as np
import streamlit as st

from graf import (
    GrafBandara,
    KELAS_KURSI, KELAS_LABEL, KELAS_IKON,
    MODE_CARI, MODE_LABEL,
    HARI_MINGGU, MASKAPAI_LIST,
    buat_graf_asean,
)

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================

st.set_page_config(
    page_title="SkyGraf — Jaringan Penerbangan Asia Tenggara",
    page_icon="✈️",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main .block-container {
    background-color: #0a0f1e !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

h1,h2,h3,h4 {
    font-family: 'Space Mono', monospace !important;
    color: #e2e8f0 !important;
    letter-spacing: -0.5px;
}

p, span, label, div, li,
.stMarkdown, .stText,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {
    color: #e2e8f0 !important;
}

/* Sidebar */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
section[data-testid="stSidebar"] {
    background-color: #0d1425 !important;
    border-right: 1px solid #1e2d4a !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #e2e8f0 !important;
}

/* Input */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background-color: #111827 !important;
    color: #e2e8f0 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 8px !important;
}
.stTextInput label, .stTextArea label,
.stNumberInput label, .stSelectbox label,
.stMultiSelect label, .stRadio label,
.stCheckbox label {
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Selectbox */
.stSelectbox > div > div,
[data-baseweb="select"] > div {
    background-color: #111827 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}
[data-baseweb="select"] span,
[data-baseweb="select"] div { color: #e2e8f0 !important; background: transparent !important; }
[data-baseweb="popover"] ul, [data-baseweb="menu"] {
    background-color: #111827 !important;
    border: 1px solid #1e3a5f !important;
}
[data-baseweb="menu"] li, [data-baseweb="option"] {
    color: #e2e8f0 !important; background-color: #111827 !important;
}
[data-baseweb="menu"] li:hover { background-color: #1e2d4a !important; }

/* Tombol */
.stButton > button {
    background: linear-gradient(135deg, #1e3a5f, #0f2447) !important;
    color: #60a5fa !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb, #1e40af) !important;
    color: #ffffff !important;
    border-color: #2563eb !important;
}
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background-color: #0d1425 !important;
    border-bottom: 1px solid #1e2d4a !important;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.78rem !important;
    color: #64748b !important;
    background-color: transparent !important;
    border-radius: 6px 6px 0 0 !important;
    padding: 8px 16px !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em;
}
.stTabs [aria-selected="true"] {
    background-color: #1e2d4a !important;
    color: #60a5fa !important;
    border-bottom: 2px solid #3b82f6 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background-color: #0a0f1e !important;
    padding: 16px 0;
}

/* Metric */
[data-testid="metric-container"] {
    background: #0d1425 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 10px !important;
    padding: 14px !important;
}
[data-testid="stMetricValue"] {
    color: #60a5fa !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
}
[data-testid="stMetricLabel"] { color: #64748b !important; }

/* Expander */
div[data-testid="stExpander"] {
    border: 1px solid #1e2d4a !important;
    border-radius: 10px !important;
    background: #0d1425 !important;
}
div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] summary span,
div[data-testid="stExpander"] p { color: #e2e8f0 !important; }

/* Divider */
hr { border-color: #1e2d4a !important; }

/* Alert */
.stSuccess { background-color: #052e16 !important; color: #86efac !important; border-color: #166534 !important; }
.stWarning { background-color: #1c1407 !important; color: #fde68a !important; }
.stError   { background-color: #1f0a0a !important; color: #fca5a5 !important; }
.stInfo    { background-color: #0c1a2e !important; color: #93c5fd !important; }

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: #0d1425 !important;
    border: 1px dashed #1e3a5f !important;
    border-radius: 10px !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0a0f1e; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 3px; }

/* Header */
header[data-testid="stHeader"], .stAppHeader {
    background-color: #0d1425 !important;
    border-bottom: 1px solid #1e2d4a !important;
}
[data-testid="stDecoration"], .stDecoration {
    background: linear-gradient(90deg, #1d4ed8, #2563eb, #3b82f6) !important;
    height: 3px !important;
}

/* DataFrame */
[data-testid="stDataFrame"] th {
    background-color: #1e2d4a !important;
    color: #60a5fa !important;
    font-family: 'Space Mono', monospace !important;
}
[data-testid="stDataFrame"] td {
    color: #e2e8f0 !important;
    background-color: #0d1425 !important;
}

/* Radio */
.stRadio label span { color: #e2e8f0 !important; }

/* Custom */
.sky-title {
    font-family: 'Space Mono', monospace !important;
    font-size: 2.4rem;
    font-weight: 700;
    color: #ffffff !important;
    letter-spacing: -1px;
    line-height: 1.1;
}
.sky-title span { color: #3b82f6 !important; }
.sky-sub {
    color: #64748b !important;
    font-size: 0.9rem;
    margin-top: 4px;
    margin-bottom: 20px;
    font-family: 'DM Sans', sans-serif !important;
}
.route-card {
    background: #0d1425;
    border: 1px solid #1e2d4a;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
}
.route-card:hover { border-color: #2563eb; }
.kelas-eco { color: #86efac; }
.kelas-bis { color: #93c5fd; }
.kelas-fir { color: #fde68a; }
.tag {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 99px;
    font-size: 11px;
    font-weight: 600;
    margin: 2px;
    font-family: 'Space Mono', monospace;
}
.tag-blue  { background: #1e3a5f; color: #93c5fd; }
.tag-green { background: #052e16; color: #86efac; }
.tag-amber { background: #1c1407; color: #fde68a; }
.tag-red   { background: #1f0a0a; color: #fca5a5; }
.tag-gray  { background: #1e2d4a; color: #94a3b8;  }
</style>
""", unsafe_allow_html=True)

# ============================================================
# KONSTANTA UI
# ============================================================

WARNA_NEGARA = {
    "Indonesia":  "#e53935",
    "Singapura":  "#ffd600",
    "Malaysia":   "#1565c0",
    "Thailand":   "#6a1b9a",
    "Filipina":   "#0277bd",
    "Vietnam":    "#2e7d32",
    "Myanmar":    "#4e342e",
    "Kamboja":    "#558b2f",
    "Laos":       "#00838f",
    "Brunei":     "#f57f17",
}

FILE_SIMPAN = "data_skygraf.json"

# ============================================================
# SESSION STATE
# ============================================================

if "graf" not in st.session_state:
    if os.path.exists(FILE_SIMPAN):
        with open(FILE_SIMPAN) as f:
            st.session_state.graf = GrafBandara.impor_json(json.load(f))
    else:
        st.session_state.graf = buat_graf_asean()

sky = st.session_state.graf


# ============================================================
# FUNGSI HELPER
# ============================================================

def simpan_data():
    with open(FILE_SIMPAN, "w") as f:
        json.dump(sky.ekspor_json(), f, indent=2, ensure_ascii=False)


def format_harga(angka):
    """Rp 1.350.000"""
    return f"Rp {angka:,.0f}".replace(",", ".")


def format_durasi(mnt):
    """125 → '2j 5m'"""
    return f"{mnt//60}j {mnt%60}m" if mnt % 60 else f"{mnt//60}j"


def gambar_peta(highlight_path=None, mode=None):
    """
    Menggambar peta jaringan penerbangan.
    highlight_path: list kode IATA rute yang disorot.
    """
    G = nx.DiGraph()
    for b in sky.get_semua_bandara_detail():
        G.add_node(b["iata"], **b)
    for r in sky.get_semua_rute():
        # Hindari duplikat edge (bisa ada 2 maskapai di rute sama)
        if not G.has_edge(r["dari"], r["ke"]):
            G.add_edge(r["dari"], r["ke"],
                       jarak=r["jarak_km"],
                       maskapai=r["maskapai"])

    if len(G.nodes) == 0:
        st.warning("Belum ada data bandara.")
        return

    fig, ax = plt.subplots(figsize=(13, 7))
    fig.patch.set_facecolor("#0a0f1e")
    ax.set_facecolor("#0a0f1e")

    # Layout
    pos = nx.spring_layout(G, seed=7, k=2.5)

    # Pisahkan edge
    edge_hl, edge_normal = [], []
    if highlight_path and len(highlight_path) > 1:
        pasangan = list(zip(highlight_path, highlight_path[1:]))
        for u, v in G.edges():
            if (u, v) in pasangan:
                edge_hl.append((u, v))
            else:
                edge_normal.append((u, v))
    else:
        edge_normal = list(G.edges())

    # Edge normal
    nx.draw_networkx_edges(
        G, pos, edgelist=edge_normal,
        edge_color="#1e2d4a", width=1.0,
        alpha=0.7, ax=ax,
        arrows=True, arrowsize=8,
        connectionstyle="arc3,rad=0.1",
    )

    # Edge highlight (rute terpilih)
    if edge_hl:
        nx.draw_networkx_edges(
            G, pos, edgelist=edge_hl,
            edge_color="#fbbf24", width=3.5,
            ax=ax, arrows=True, arrowsize=16,
            connectionstyle="arc3,rad=0.1",
        )
        # Glow
        nx.draw_networkx_edges(
            G, pos, edgelist=edge_hl,
            edge_color="#fbbf2440", width=10,
            ax=ax, arrows=False,
            connectionstyle="arc3,rad=0.1",
        )

    # Node
    for node in G.nodes():
        x, y = pos[node]
        negara = G.nodes[node].get("negara", "")
        warna  = WARNA_NEGARA.get(negara, "#64748b")
        in_hl  = highlight_path and node in highlight_path
        tipe   = G.nodes[node].get("tipe", "spoke")

        # Glow untuk node di jalur
        if in_hl:
            glow = Circle((x, y), 0.10,
                           facecolor="#fbbf2420", edgecolor="none",
                           zorder=10)
            ax.add_patch(glow)

        # Ring luar
        r_outer = 0.075 if tipe == "hub" else 0.058
        ax.add_patch(Circle((x, y), r_outer,
                             facecolor="#0d1425",
                             edgecolor="#fbbf24" if in_hl else warna,
                             linewidth=2.5 if in_hl else 1.5,
                             zorder=11))
        # Titik dalam
        r_inner = 0.042 if tipe == "hub" else 0.030
        ax.add_patch(Circle((x, y), r_inner,
                             facecolor="#fbbf24" if in_hl else warna,
                             edgecolor="none", zorder=12))

    # Label
    for node, (x, y) in pos.items():
        in_hl = highlight_path and node in highlight_path
        color = "#fbbf24" if in_hl else "#e2e8f0"
        txt = ax.text(x, y - 0.11, node,
                      fontsize=7.5, ha="center", va="top",
                      fontweight="bold", color=color,
                      fontfamily="monospace", zorder=15)
        txt.set_path_effects([
            pe.withStroke(linewidth=2.5, foreground="#0a0f1e")
        ])
        # Nama kota kecil
        kota = G.nodes[node].get("kota", "")
        ax.text(x, y - 0.175, kota,
                fontsize=5.5, ha="center", va="top",
                color="#64748b", zorder=15)

    # Legenda negara
    from matplotlib.lines import Line2D
    neg_unik = set(G.nodes[n].get("negara","") for n in G.nodes())
    handles  = [
        Line2D([0],[0], marker="o", color="w",
               markerfacecolor=WARNA_NEGARA.get(neg,"#64748b"),
               markersize=7, label=neg)
        for neg in sorted(neg_unik) if neg
    ]
    leg = ax.legend(handles=handles, loc="lower left",
                    fontsize=7, facecolor="#0d1425",
                    edgecolor="#1e2d4a", framealpha=0.9,
                    labelcolor="#e2e8f0", title="Negara",
                    title_fontsize=7)
    leg.get_title().set_color("#64748b")

    # Info rute disorot
    if highlight_path:
        label = " → ".join(highlight_path)
        ax.set_title(f"RUTE: {label}",
                     fontsize=10, color="#fbbf24",
                     fontfamily="monospace",
                     fontweight="bold", pad=10)
    else:
        ax.set_title("JARINGAN PENERBANGAN ASIA TENGGARA",
                     fontsize=10, color="#60a5fa",
                     fontfamily="monospace",
                     fontweight="bold", pad=10)

    ax.set_axis_off()
    fig.tight_layout(pad=0.5)
    st.pyplot(fig)
    plt.close(fig)


# ============================================================
# HEADER
# ============================================================

col_logo, col_stats = st.columns([2, 3])

with col_logo:
    st.markdown(
        '<div class="sky-title">Sky<span>Graf</span></div>'
        '<div class="sky-sub">✈️ Jaringan Penerbangan Asia Tenggara — '
        'Weighted Directed Graph + Dijkstra</div>',
        unsafe_allow_html=True,
    )

ring = sky.ringkasan()
with col_stats:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("✈️ Bandara",  ring["total_bandara"])
    c2.metric("🛫 Rute",     ring["total_rute"])
    c3.metric("🏢 Maskapai", ring["total_maskapai"])
    c4.metric("🌏 Negara",   ring["total_negara"])

st.divider()

# ============================================================
# SIDEBAR — Manajemen Data
# ============================================================

with st.sidebar:
    st.markdown("### ✈️ SkyGraf")
    st.caption("Manajemen Jaringan Penerbangan")
    st.divider()

    menu = st.radio("Menu:", [
        "🗺️ Lihat Peta",
        "🏢 Tambah Bandara",
        "🛫 Tambah Rute",
        "🗑️ Hapus Data",
        "💾 Simpan & Muat",
    ], label_visibility="collapsed")

    st.divider()

    # ── LIHAT PETA ──
    if menu == "🗺️ Lihat Peta":
        st.subheader("🌏 Info Bandara")
        semua = sky.get_semua_bandara()
        if semua:
            pilih = st.selectbox("Pilih Bandara:", semua,
                                 format_func=lambda x:
                                 f"{x} — {sky.get_detail_bandara(x)['kota']}")
            detail = sky.get_detail_bandara(pilih)
            if detail:
                st.markdown(
                    f"**{detail['nama']}**  \n"
                    f"📍 {detail['kota']}, {detail['negara']}  \n"
                    f"🕐 {detail['zona_waktu']}  \n"
                    f"🏗️ {detail['terminal']} Terminal  \n"
                    f"🔵 Tipe: `{detail['tipe'].upper()}`"
                )
                rute_keluar = sky.get_rute_dari(pilih)
                st.caption(f"{len(rute_keluar)} rute keluar dari {pilih}")

    # ── TAMBAH BANDARA ──
    elif menu == "🏢 Tambah Bandara":
        st.subheader("🏢 Tambah Bandara")
        with st.form("form_bandara"):
            iata     = st.text_input("Kode IATA (3 huruf):")
            nama     = st.text_input("Nama Bandara:")
            kota     = st.text_input("Kota:")
            negara   = st.text_input("Negara:")
            utc      = st.selectbox("Zona Waktu:", [
                "UTC+6.5","UTC+7","UTC+8","UTC+9"
            ])
            terminal = st.number_input("Jumlah Terminal:", 1, 10, 1)
            tipe     = st.selectbox("Tipe:", ["hub","spoke"])
            sub      = st.form_submit_button("➕ Tambah Bandara",
                                             use_container_width=True)
            if sub:
                if not iata.strip() or len(iata.strip()) != 3:
                    st.error("Kode IATA harus 3 huruf.")
                elif sky.tambah_bandara(iata.strip().upper(), nama,
                                        kota, negara, utc,
                                        terminal, tipe):
                    st.success(f"✅ {iata.upper()} ditambahkan!")
                    st.rerun()
                else:
                    st.warning("⚠️ Kode IATA sudah terdaftar.")

    # ── TAMBAH RUTE ──
    elif menu == "🛫 Tambah Rute":
        st.subheader("🛫 Tambah Rute Baru")
        semua = sky.get_semua_bandara()
        if len(semua) < 2:
            st.info("Tambahkan minimal 2 bandara.")
        else:
            with st.form("form_rute"):
                col1, col2 = st.columns(2)
                with col1: dari_b = st.selectbox("Dari:", semua)
                with col2: ke_b   = st.selectbox("Ke:",   semua)
                kode     = st.text_input("Kode Penerbangan (cth: GA830):")
                maskapai = st.selectbox("Maskapai:", MASKAPAI_LIST)
                pesawat  = st.text_input("Tipe Pesawat:", "Boeing 737-800")
                col3, col4 = st.columns(2)
                with col3: jarak   = st.number_input("Jarak (KM):", 1.0, 15000.0, 500.0)
                with col4: durasi  = st.number_input("Durasi (menit):", 10, 1440, 90)
                jadwal_input = st.text_input(
                    "Jadwal (pisah koma, cth: 06:00,10:30,15:00):",
                    "06:00,12:00,18:00"
                )
                hari_input = st.multiselect(
                    "Hari Operasi:",
                    ["Setiap Hari"] + HARI_MINGGU,
                    default=["Setiap Hari"],
                )
                st.markdown("**Kelas Kursi:**")
                col_e, col_b, col_f = st.columns(3)
                with col_e:
                    st.markdown("💺 **Ekonomi**")
                    eco_kap  = st.number_input("Kapasitas ECO:", 50, 400, 150, key="eco_k")
                    eco_hrg  = st.number_input("Harga ECO (Rp):", 100000, 50000000, 1000000, step=50000, key="eco_h")
                with col_b:
                    st.markdown("🛋️ **Bisnis**")
                    bis_kap  = st.number_input("Kapasitas BIS:", 4, 100, 24, key="bis_k")
                    bis_hrg  = st.number_input("Harga BIS (Rp):", 500000, 100000000, 3500000, step=100000, key="bis_h")
                with col_f:
                    st.markdown("👑 **First** (opsional)")
                    ada_fir  = st.checkbox("Tersedia First Class")
                    fir_kap  = st.number_input("Kapasitas FIR:", 2, 20, 8, key="fir_k") if ada_fir else 0
                    fir_hrg  = st.number_input("Harga FIR (Rp):", 1000000, 200000000, 10000000, step=500000, key="fir_h") if ada_fir else 0

                sub = st.form_submit_button("➕ Tambah Rute", use_container_width=True)
                if sub:
                    if dari_b == ke_b:
                        st.error("Asal dan tujuan tidak boleh sama.")
                    else:
                        jadwal_list = [j.strip() for j in jadwal_input.split(",") if j.strip()]
                        kursi = {
                            "ECO": {"kapasitas": eco_kap, "tersedia": eco_kap, "harga": eco_hrg},
                            "BIS": {"kapasitas": bis_kap, "tersedia": bis_kap, "harga": bis_hrg},
                        }
                        if ada_fir:
                            kursi["FIR"] = {"kapasitas": fir_kap, "tersedia": fir_kap, "harga": fir_hrg}
                        if sky.tambah_rute(
                            dari_b, ke_b, kode, maskapai, pesawat,
                            jarak, durasi, jadwal_list, hari_input, kursi
                        ):
                            st.success(f"✅ Rute {dari_b}→{ke_b} ditambahkan!")
                            st.rerun()
                        else:
                            st.error("❌ Gagal. Periksa data kembali.")

    # ── HAPUS ──
    elif menu == "🗑️ Hapus Data":
        st.subheader("🗑️ Hapus Data")
        semua = sky.get_semua_bandara()
        st.markdown("**Hapus Bandara**")
        if semua:
            hapus_b = st.selectbox("Pilih:", semua, key="hapus_bdr",
                                   format_func=lambda x:
                                   f"{x} — {sky.get_detail_bandara(x)['kota']}")
            if st.button("🗑️ Hapus Bandara", use_container_width=True):
                sky.hapus_bandara(hapus_b)
                st.success(f"✅ {hapus_b} dihapus."); st.rerun()
        st.divider()
        st.markdown("**Hapus Rute**")
        semua_rute = sky.get_semua_rute()
        if semua_rute:
            opsi = [f"{r['kode_penerbangan']}: {r['dari']}→{r['ke']} ({r['maskapai']})"
                    for r in semua_rute]
            pilih_r = st.selectbox("Pilih rute:", opsi, key="hapus_rte")
            if st.button("🗑️ Hapus Rute", use_container_width=True):
                idx = opsi.index(pilih_r)
                t   = semua_rute[idx]
                sky.hapus_rute(t["dari"], t["ke"], t["kode_penerbangan"])
                st.success("✅ Rute dihapus."); st.rerun()
        else:
            st.info("Belum ada rute.")

    # ── SIMPAN & MUAT ──
    elif menu == "💾 Simpan & Muat":
        st.subheader("💾 Simpan & Muat")
        if st.button("💾 Simpan Sekarang", use_container_width=True):
            simpan_data(); st.success("✅ Data disimpan.")
        st.divider()
        uploaded = st.file_uploader("📂 Muat dari JSON:", type="json")
        if uploaded:
            try:
                data = json.load(uploaded)
                st.session_state.graf = GrafBandara.impor_json(data)
                st.success("✅ Data dimuat!"); st.rerun()
            except Exception as e:
                st.error(f"❌ Gagal: {e}")
        st.divider()
        data_json = json.dumps(sky.ekspor_json(), indent=2, ensure_ascii=False)
        st.download_button("⬇️ Unduh JSON", data=data_json,
                           file_name="skygraf_data.json",
                           mime="application/json",
                           use_container_width=True)


# ============================================================
# TABS UTAMA
# ============================================================

tab_peta, tab_cari, tab_jadwal, tab_bandara, tab_debug = st.tabs([
    "🌐 Peta Rute",
    "🔍 Cari Penerbangan",
    "📅 Jadwal & Maskapai",
    "🏢 Data Bandara",
    "🔧 Debug & Struktur Data",
])


# ─────────────────────────────────────────────────────────────
# TAB 1: PETA RUTE
# ─────────────────────────────────────────────────────────────
with tab_peta:
    st.subheader("🌐 Peta Jaringan Penerbangan Asia Tenggara")
    st.caption("Setiap titik = bandara. Setiap garis = rute penerbangan langsung.")

    hub_list = sky.hub_tersibuk(3)
    if hub_list:
        cols_hub = st.columns(3)
        for i, (iata, jml) in enumerate(hub_list):
            detail = sky.get_detail_bandara(iata)
            nama_k = detail["kota"] if detail else iata
            cols_hub[i].metric(f"🏆 Hub #{i+1}", iata,
                               help=f"{nama_k} — {jml} rute keluar")

    gambar_peta()

    st.divider()
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        rt = sky.rute_terpanjang()
        if rt:
            st.markdown(
                f"**✈️ Rute Terpanjang:**  \n"
                f"`{rt.dari}` → `{rt.ke}` — "
                f"**{rt.jarak_km:,.0f} KM** ({rt.durasi_format()})  \n"
                f"_{rt.maskapai}_"
            )
    with col_stat2:
        rp = sky.rute_terpendek_jarak()
        if rp:
            st.markdown(
                f"**✈️ Rute Terpendek:**  \n"
                f"`{rp.dari}` → `{rp.ke}` — "
                f"**{rp.jarak_km:,.0f} KM** ({rp.durasi_format()})  \n"
                f"_{rp.maskapai}_"
            )


# ─────────────────────────────────────────────────────────────
# TAB 2: CARI PENERBANGAN
# ─────────────────────────────────────────────────────────────
with tab_cari:
    st.subheader("🔍 Cari Penerbangan Optimal")

    semua_b = sky.get_semua_bandara()
    if len(semua_b) < 2:
        st.info("Tambahkan minimal 2 bandara terlebih dahulu.")
    else:
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            asal = st.selectbox("🛫 Asal:", semua_b,
                                format_func=lambda x:
                                f"{x} — {sky.get_detail_bandara(x)['kota']}")
        with col_b:
            tujuan = st.selectbox("🛬 Tujuan:", semua_b,
                                  format_func=lambda x:
                                  f"{x} — {sky.get_detail_bandara(x)['kota']}")
        with col_c:
            mode = st.selectbox("⚖️ Prioritas:",
                                MODE_CARI,
                                format_func=lambda x: MODE_LABEL[x])
        with col_d:
            kelas = st.selectbox("💺 Kelas:",
                                 KELAS_KURSI,
                                 format_func=lambda x:
                                 f"{KELAS_IKON[x]} {KELAS_LABEL[x]}")

        if st.button("🔍 CARI RUTE OPTIMAL", use_container_width=True):
            if asal == tujuan:
                st.warning("⚠️ Asal dan tujuan tidak boleh sama.")
            else:
                path, total, details = sky.cari_rute(asal, tujuan, mode, kelas)

                if path:
                    st.success(f"✅ Rute ditemukan! {MODE_LABEL[mode]}")

                    # Metric hasil
                    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                    if mode == "harga":
                        col_m1.metric("💰 Total Harga", format_harga(total))
                    elif mode == "durasi":
                        col_m1.metric("⏱️ Total Durasi", format_durasi(int(total)))
                    else:
                        col_m1.metric("📏 Total Jarak", f"{total:,.0f} KM")
                    col_m2.metric("✈️ Kota Disinggahi", len(path))
                    col_m3.metric("🔄 Jumlah Transit", len(path) - 2 if len(path) > 2 else 0)
                    col_m4.metric("💺 Kelas", f"{KELAS_IKON[kelas]} {KELAS_LABEL[kelas]}")

                    # Jalur rute
                    st.markdown("**Jalur Penerbangan:**")
                    rute_html = " &nbsp;<span style='color:#3b82f6'>→</span>&nbsp; ".join(
                        f"<code style='background:#1e2d4a;color:#60a5fa;padding:2px 8px;"
                        f"border-radius:4px;font-family:monospace'>{n}</code>"
                        for n in path
                    )
                    st.markdown(rute_html, unsafe_allow_html=True)

                    # Detail tiap segmen
                    st.markdown("**Detail Segmen:**")
                    for i, p in enumerate(details):
                        harga_kelas = p.kursi.get(kelas, {}).get("harga", 0)
                        tersedia    = p.kursi.get(kelas, {}).get("tersedia", 0)
                        with st.expander(
                            f"Segmen {i+1}: {p.dari} → {p.ke} "
                            f"| {p.kode_penerbangan} | {p.maskapai}"
                        ):
                            col_d1, col_d2, col_d3 = st.columns(3)
                            col_d1.markdown(
                                f"**Pesawat:** {p.pesawat}  \n"
                                f"**Jarak:** {p.jarak_km:,.0f} KM  \n"
                                f"**Durasi:** {p.durasi_format()}"
                            )
                            col_d2.markdown(
                                f"**Jadwal:** {', '.join(p.jadwal)}  \n"
                                f"**Hari:** {', '.join(p.hari_operasi)}"
                            )
                            col_d3.markdown(
                                f"**Kelas:** {KELAS_IKON[kelas]} {KELAS_LABEL[kelas]}  \n"
                                f"**Harga:** {format_harga(harga_kelas)}  \n"
                                f"**Kursi Tersedia:** {tersedia}"
                            )

                            # Tabel semua kelas
                            st.markdown("**Semua Kelas Kursi:**")
                            for kls in KELAS_KURSI:
                                if kls in p.kursi:
                                    k_data = p.kursi[kls]
                                    cls_color = {
                                        "ECO":"kelas-eco",
                                        "BIS":"kelas-bis",
                                        "FIR":"kelas-fir"
                                    }[kls]
                                    st.markdown(
                                        f"<span class='{cls_color}'>"
                                        f"{KELAS_IKON[kls]} **{KELAS_LABEL[kls]}**</span> — "
                                        f"{format_harga(k_data['harga'])} | "
                                        f"Tersedia: {k_data['tersedia']}/{k_data['kapasitas']}",
                                        unsafe_allow_html=True,
                                    )

                    # Peta rute disorot
                    st.markdown("**Peta Rute:**")
                    gambar_peta(highlight_path=path, mode=mode)

                else:
                    st.error(
                        f"❌ Tidak ada rute dari **{asal}** ke **{tujuan}** "
                        f"untuk kelas {KELAS_LABEL[kelas]}. "
                        f"Coba mode atau kelas lain."
                    )

        # Bandingkan semua mode
        st.divider()
        st.markdown("**🔄 Bandingkan Ketiga Mode Sekaligus:**")
        if st.button("Bandingkan Harga vs Durasi vs Jarak",
                     use_container_width=True):
            if asal == tujuan:
                st.warning("Asal dan tujuan tidak boleh sama.")
            else:
                semua_mode = sky.cari_semua_mode(asal, tujuan, kelas)
                cols_mode  = st.columns(3)
                icons = {"harga":"💰","durasi":"⏱️","jarak":"📏"}
                for i, (m, (p, t, d)) in enumerate(semua_mode.items()):
                    with cols_mode[i]:
                        st.markdown(f"### {MODE_LABEL[m]}")
                        if p:
                            if m == "harga":
                                val = format_harga(t)
                            elif m == "durasi":
                                val = format_durasi(int(t))
                            else:
                                val = f"{t:,.0f} KM"
                            st.metric("Nilai Optimal", val)
                            st.caption(" → ".join(p))
                            if len(p) > 2:
                                transit = ", ".join(p[1:-1])
                                st.markdown(
                                    f"<span class='tag tag-amber'>Transit: {transit}</span>",
                                    unsafe_allow_html=True)
                            else:
                                st.markdown(
                                    "<span class='tag tag-green'>Langsung</span>",
                                    unsafe_allow_html=True)
                        else:
                            st.error("Tidak ada rute")


# ─────────────────────────────────────────────────────────────
# TAB 3: JADWAL & MASKAPAI
# ─────────────────────────────────────────────────────────────
with tab_jadwal:
    st.subheader("📅 Jadwal Penerbangan & Filter Maskapai")

    col_j1, col_j2 = st.columns(2)

    with col_j1:
        st.markdown("#### 🕐 Jadwal Per Rute & Hari")
        semua_b = sky.get_semua_bandara()
        if len(semua_b) >= 2:
            j_dari = st.selectbox("Dari:", semua_b, key="jd_dari",
                                  format_func=lambda x:
                                  f"{x} — {sky.get_detail_bandara(x)['kota']}")
            j_ke   = st.selectbox("Ke:",   semua_b, key="jd_ke",
                                  format_func=lambda x:
                                  f"{x} — {sky.get_detail_bandara(x)['kota']}")
            j_hari = st.selectbox("Hari:", ["Semua Hari"] + HARI_MINGGU)

            if j_dari != j_ke:
                if j_hari == "Semua Hari":
                    rute_list = sky.get_rute_antara(j_dari, j_ke)
                else:
                    rute_list = sky.jadwal_tersedia(j_dari, j_ke, j_hari)

                if rute_list:
                    for p in rute_list:
                        with st.expander(
                            f"✈️ {p.kode_penerbangan} — {p.maskapai}"
                        ):
                            st.markdown(
                                f"**Pesawat:** {p.pesawat}  \n"
                                f"**Durasi:** {p.durasi_format()} | "
                                f"**Jarak:** {p.jarak_km:,.0f} KM  \n"
                                f"**Hari Operasi:** {', '.join(p.hari_operasi)}"
                            )
                            st.markdown("**Jadwal Keberangkatan → Perkiraan Tiba:**")
                            cols_jadwal = st.columns(4)
                            for idx, jam in enumerate(p.jadwal):
                                tiba = p.hitung_tiba(jam)
                                cols_jadwal[idx % 4].markdown(
                                    f"<div style='background:#0d1425;border:1px solid #1e2d4a;"
                                    f"border-radius:8px;padding:8px;text-align:center;"
                                    f"margin:2px'>"
                                    f"<div style='color:#60a5fa;font-family:monospace;"
                                    f"font-weight:bold'>{jam}</div>"
                                    f"<div style='color:#64748b;font-size:10px'>↓</div>"
                                    f"<div style='color:#86efac;font-family:monospace'>{tiba}</div>"
                                    f"</div>",
                                    unsafe_allow_html=True,
                                )
                            st.markdown("**Ketersediaan Kursi:**")
                            for kls in KELAS_KURSI:
                                if kls in p.kursi:
                                    k_d = p.kursi[kls]
                                    pct = int(k_d["tersedia"] / k_d["kapasitas"] * 100)
                                    bar_w = pct
                                    bar_c = "#22c55e" if pct > 50 else "#f59e0b" if pct > 20 else "#ef4444"
                                    st.markdown(
                                        f"{KELAS_IKON[kls]} **{KELAS_LABEL[kls]}** — "
                                        f"{format_harga(k_d['harga'])} | "
                                        f"{k_d['tersedia']}/{k_d['kapasitas']} kursi  \n"
                                        f"<div style='background:#1e2d4a;border-radius:4px;"
                                        f"height:6px;margin:4px 0 8px'>"
                                        f"<div style='background:{bar_c};width:{bar_w}%;"
                                        f"height:6px;border-radius:4px'></div></div>",
                                        unsafe_allow_html=True,
                                    )
                else:
                    txt = f"pada hari {j_hari}" if j_hari != "Semua Hari" else ""
                    st.info(f"Tidak ada penerbangan {j_dari}→{j_ke} {txt}.")

    with col_j2:
        st.markdown("#### 🏢 Filter per Maskapai")
        maskapai_ada = list(set(
            r["maskapai"] for r in sky.get_semua_rute()
        ))
        if maskapai_ada:
            pilih_m = st.selectbox("Pilih Maskapai:", sorted(maskapai_ada))
            rute_m  = sky.filter_maskapai(pilih_m)
            st.metric("Total Rute", len(rute_m))
            if rute_m:
                for r in rute_m:
                    dari_d  = sky.get_detail_bandara(r["dari"])
                    ke_d    = sky.get_detail_bandara(r["ke"])
                    dari_nm = dari_d["kota"] if dari_d else r["dari"]
                    ke_nm   = ke_d["kota"]   if ke_d   else r["ke"]
                    eco_h   = r["kursi"].get("ECO",{}).get("harga", 0)
                    st.markdown(
                        f"<div class='route-card'>"
                        f"<b style='font-family:monospace;color:#60a5fa'>"
                        f"{r['kode_penerbangan']}</b> &nbsp;"
                        f"<span class='tag tag-gray'>{r['pesawat']}</span><br>"
                        f"<b>{r['dari']}</b> {dari_nm} → "
                        f"<b>{r['ke']}</b> {ke_nm}<br>"
                        f"<span style='color:#64748b;font-size:12px'>"
                        f"{r['jarak_km']:,.0f} KM | {format_durasi(r['durasi_mnt'])} | "
                        f"ab {format_harga(eco_h)}</span>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
        else:
            st.info("Belum ada data rute.")


# ─────────────────────────────────────────────────────────────
# TAB 4: DATA BANDARA
# ─────────────────────────────────────────────────────────────
with tab_bandara:
    st.subheader("🏢 Data Bandara Asia Tenggara")

    semua_detail = sky.get_semua_bandara_detail()

    # Kelompokkan per negara
    per_negara = {}
    for b in semua_detail:
        neg = b["negara"]
        if neg not in per_negara:
            per_negara[neg] = []
        per_negara[neg].append(b)

    for negara, list_b in sorted(per_negara.items()):
        warna_n = WARNA_NEGARA.get(negara, "#64748b")
        st.markdown(
            f"<h4 style='color:{warna_n};font-family:monospace;"
            f"border-left:3px solid {warna_n};padding-left:10px;"
            f"margin:16px 0 8px'>🌏 {negara}</h4>",
            unsafe_allow_html=True,
        )
        cols_b = st.columns(min(len(list_b), 4))
        for i, b in enumerate(list_b):
            rute_k = len(sky.get_rute_dari(b["iata"]))
            with cols_b[i % 4]:
                tipe_tag = "tag-blue" if b["tipe"] == "hub" else "tag-gray"
                st.markdown(
                    f"<div class='route-card'>"
                    f"<div style='font-family:monospace;font-size:1.3rem;"
                    f"font-weight:700;color:{warna_n}'>{b['iata']}</div>"
                    f"<div style='font-size:11px;color:#e2e8f0;margin:2px 0'>"
                    f"{b['nama']}</div>"
                    f"<div style='font-size:11px;color:#64748b'>"
                    f"📍 {b['kota']} | {b['zona_waktu']}</div>"
                    f"<div style='margin-top:6px'>"
                    f"<span class='tag {tipe_tag}'>{b['tipe'].upper()}</span>"
                    f"<span class='tag tag-gray'>{b['terminal']} terminal</span>"
                    f"<span class='tag tag-blue'>{rute_k} rute</span>"
                    f"</div></div>",
                    unsafe_allow_html=True,
                )

    st.divider()
    st.markdown("#### 📊 BFS & DFS dari Bandara")
    col_t1, col_t2 = st.columns(2)
    semua_b = sky.get_semua_bandara()
    with col_t1:
        st.markdown("**BFS (Breadth-First Search)**")
        st.caption("Telusuri bandara lapis per lapis dari titik awal.")
        if semua_b:
            bfs_start = st.selectbox("Mulai dari:", semua_b, key="bfs_s")
            if st.button("▶ Jalankan BFS"):
                hasil_bfs = sky.bfs(bfs_start)
                st.markdown(" → ".join(
                    f"`{x}`" for x in hasil_bfs
                ))
                st.caption(f"Total {len(hasil_bfs)} bandara terjangkau.")
    with col_t2:
        st.markdown("**DFS (Depth-First Search)**")
        st.caption("Telusuri sedalam mungkin sebelum kembali.")
        if semua_b:
            dfs_start = st.selectbox("Mulai dari:", semua_b, key="dfs_s")
            if st.button("▶ Jalankan DFS"):
                hasil_dfs = sky.dfs(dfs_start)
                st.markdown(" → ".join(
                    f"`{x}`" for x in hasil_dfs
                ))
                st.caption(f"Total {len(hasil_dfs)} bandara terjangkau.")


# ─────────────────────────────────────────────────────────────
# TAB 5: DEBUG & STRUKTUR DATA
# ─────────────────────────────────────────────────────────────
with tab_debug:
    st.subheader("🔧 Struktur Data Internal")
    st.markdown(
        "> Tab ini menampilkan isi **adjacency list manual** dari class `GrafBandara` — "
        "berguna untuk debugging dan demonstrasi ke dosen bahwa struktur data "
        "dibangun sendiri tanpa library."
    )
    st.divider()

    st.markdown("#### 📋 Adjacency List")
    adj = sky.adjacency_list
    rows = []
    for dari_k, tujuan_dict in adj.items():
        for ke_k, attr in tujuan_dict.items():
            rows.append({
                "Dari": dari_k,
                "Ke":   ke_k,
                "Kode": attr.get("kode",""),
                "Maskapai": attr.get("maskapai",""),
                "Jarak (KM)": attr.get("jarak_km",""),
                "Durasi": attr.get("durasi",""),
                "Jadwal": ", ".join(attr.get("jadwal",[])),
            })
    if rows:
        import pandas as pd
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada data.")

    st.divider()
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown("**Daftar Vertex (Bandara):**")
        for b in sky.get_semua_bandara_detail():
            rute_k = len(sky.get_rute_dari(b["iata"]))
            st.markdown(
                f"- **{b['iata']}** `{b['kota']}, {b['negara']}` "
                f"— {rute_k} rute keluar"
            )
    with col_d2:
        st.markdown("**Hub Tersibuk (Derajat Tertinggi):**")
        for iata, jml in sky.hub_tersibuk(10):
            d = sky.get_detail_bandara(iata)
            kota = d["kota"] if d else ""
            st.markdown(f"- **{iata}** {kota} — {jml} rute")

    st.divider()
    st.markdown("#### 📦 Ekspor JSON")
    data_str = json.dumps(sky.ekspor_json(), indent=2, ensure_ascii=False)
    st.markdown(
        f'<pre style="background:#0d1425;border:1px solid #1e2d4a;'
        f'border-radius:10px;padding:16px;color:#e2e8f0;'
        f'font-size:0.75rem;max-height:300px;overflow-y:auto;">'
        f'{data_str[:3000]}{"..." if len(data_str)>3000 else ""}</pre>',
        unsafe_allow_html=True,
    )
    st.download_button(
        "⬇️ Download JSON Lengkap",
        data=data_str,
        file_name="skygraf_export.json",
        mime="application/json",
        use_container_width=True,
    )