# ============================================================
# SKYGRAF — app.py
# Aplikasi Streamlit visualisasi jaringan penerbangan
# Asia Tenggara berbasis Weighted Directed Graph + Dijkstra
# ============================================================

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Circle
import networkx as nx
import streamlit as st

from graf import (
    GrafBandara, KELAS_KURSI, KELAS_LABEL, KELAS_IKON,
    MODE_CARI, MODE_LABEL, HARI_MINGGU, MASKAPAI_LIST,
    buat_graf_asean,
)

# ── KONFIGURASI HALAMAN ──────────────────────────────────────

st.set_page_config(
    page_title="SkyGraf — Jaringan Penerbangan Asia Tenggara",
    page_icon="✈️",
    layout="wide",
)

# ── WARNA PER NEGARA ─────────────────────────────────────────

WARNA_NEGARA = {
    "Indonesia": "#e53935", "Singapura": "#ffd600",
    "Malaysia":  "#1565c0", "Thailand":  "#6a1b9a",
    "Filipina":  "#0277bd", "Vietnam":   "#2e7d32",
    "Myanmar":   "#4e342e",
}

# ── SESSION STATE ────────────────────────────────────────────

if "graf" not in st.session_state:
    st.session_state.graf = buat_graf_asean()

sky = st.session_state.graf

# ── HELPER ───────────────────────────────────────────────────

def format_harga(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

def format_durasi(mnt):
    return f"{mnt//60}j {mnt%60}m" if mnt % 60 else f"{mnt//60}j"

def gambar_peta(highlight_path=None):
    """Gambar peta jaringan penerbangan, opsional sorot rute."""
    G = nx.DiGraph()
    for b in sky.get_semua_bandara_detail():
        G.add_node(b["iata"], **b)
    for r in sky.get_semua_rute():
        if not G.has_edge(r["dari"], r["ke"]):
            G.add_edge(r["dari"], r["ke"])

    if not G.nodes:
        st.warning("Belum ada data bandara.")
        return

    fig, ax = plt.subplots(figsize=(13, 7))
    fig.patch.set_facecolor("#0a0f1e")
    ax.set_facecolor("#0a0f1e")
    pos = nx.spring_layout(G, seed=7, k=2.5)

    # Pisahkan edge normal vs highlight
    edge_hl, edge_normal = [], []
    if highlight_path and len(highlight_path) > 1:
        pasangan = list(zip(highlight_path, highlight_path[1:]))
        for u, v in G.edges():
            (edge_hl if (u, v) in pasangan else edge_normal).append((u, v))
    else:
        edge_normal = list(G.edges())

    nx.draw_networkx_edges(G, pos, edgelist=edge_normal,
        edge_color="#1e2d4a", width=1.0, alpha=0.7, ax=ax,
        arrows=True, arrowsize=8, connectionstyle="arc3,rad=0.1")

    if edge_hl:
        nx.draw_networkx_edges(G, pos, edgelist=edge_hl,
            edge_color="#fbbf24", width=3.5, ax=ax,
            arrows=True, arrowsize=16, connectionstyle="arc3,rad=0.1")
        nx.draw_networkx_edges(G, pos, edgelist=edge_hl,
            edge_color="#fbbf2440", width=10, ax=ax,
            arrows=False, connectionstyle="arc3,rad=0.1")

    for node in G.nodes():
        x, y    = pos[node]
        negara  = G.nodes[node].get("negara", "")
        warna   = WARNA_NEGARA.get(negara, "#64748b")
        in_hl   = highlight_path and node in highlight_path
        is_hub  = G.nodes[node].get("tipe", "spoke") == "hub"

        if in_hl:
            ax.add_patch(Circle((x,y), 0.10,
                facecolor="#fbbf2420", edgecolor="none", zorder=10))
        ax.add_patch(Circle((x,y), 0.075 if is_hub else 0.058,
            facecolor="#0d1425",
            edgecolor="#fbbf24" if in_hl else warna,
            linewidth=2.5 if in_hl else 1.5, zorder=11))
        ax.add_patch(Circle((x,y), 0.042 if is_hub else 0.030,
            facecolor="#fbbf24" if in_hl else warna,
            edgecolor="none", zorder=12))

    for node, (x, y) in pos.items():
        in_hl = highlight_path and node in highlight_path
        txt = ax.text(x, y-0.11, node, fontsize=7.5, ha="center", va="top",
                      fontweight="bold", color="#fbbf24" if in_hl else "#e2e8f0",
                      fontfamily="monospace", zorder=15)
        txt.set_path_effects([pe.withStroke(linewidth=2.5, foreground="#0a0f1e")])
        ax.text(x, y-0.175, G.nodes[node].get("kota",""),
                fontsize=5.5, ha="center", va="top", color="#64748b", zorder=15)

    from matplotlib.lines import Line2D
    neg_unik = {G.nodes[n].get("negara","") for n in G.nodes()}
    handles = [
        Line2D([0],[0], marker="o", color="w",
               markerfacecolor=WARNA_NEGARA.get(neg,"#64748b"),
               markersize=7, label=neg)
        for neg in sorted(neg_unik) if neg
    ]
    leg = ax.legend(handles=handles, loc="lower left", fontsize=7,
                    facecolor="#0d1425", edgecolor="#1e2d4a",
                    labelcolor="#e2e8f0", title="Negara", title_fontsize=7)
    leg.get_title().set_color("#64748b")

    judul = f"RUTE: {' → '.join(highlight_path)}" if highlight_path \
            else "JARINGAN PENERBANGAN ASIA TENGGARA"
    ax.set_title(judul, fontsize=10,
                 color="#fbbf24" if highlight_path else "#60a5fa",
                 fontfamily="monospace", fontweight="bold", pad=10)
    ax.set_axis_off()
    fig.tight_layout(pad=0.5)
    st.pyplot(fig)
    plt.close(fig)


# ── HEADER ───────────────────────────────────────────────────

col_logo, col_stats = st.columns([2, 3])
with col_logo:
    st.title("✈️ SkyGraf")
    st.caption("Jaringan Penerbangan Asia Tenggara — Weighted Directed Graph + Dijkstra")

ring = sky.ringkasan()
with col_stats:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("✈️ Bandara",  ring["total_bandara"])
    c2.metric("🛫 Rute",     ring["total_rute"])
    c3.metric("🏢 Maskapai", ring["total_maskapai"])
    c4.metric("🌏 Negara",   ring["total_negara"])

st.divider()

# ── SIDEBAR — Manajemen Data ─────────────────────────────────

with st.sidebar:
    st.markdown("### ✈️ SkyGraf")
    st.caption("Manajemen Jaringan Penerbangan")
    st.divider()

    menu = st.radio("Menu:", [
        "🗺️ Lihat Peta",
        "🏢 Tambah Bandara",
        "🛫 Tambah Rute",
        "🗑️ Hapus Data",
    ], label_visibility="collapsed")

    st.divider()

    if menu == "🗺️ Lihat Peta":
        st.subheader("🌏 Info Bandara")
        semua = sky.get_semua_bandara()
        if semua:
            pilih = st.selectbox("Pilih Bandara:", semua,
                                 format_func=lambda x:
                                 f"{x} — {sky.get_detail_bandara(x)['kota']}")
            d = sky.get_detail_bandara(pilih)
            if d:
                st.markdown(
                    f"**{d['nama']}**  \n"
                    f"📍 {d['kota']}, {d['negara']}  \n"
                    f"🕐 {d['zona_waktu']} | 🏗️ {d['terminal']} Terminal  \n"
                    f"🔵 Tipe: `{d['tipe'].upper()}`"
                )
                st.caption(f"{len(sky.get_rute_dari(pilih))} rute keluar dari {pilih}")

    elif menu == "🏢 Tambah Bandara":
        st.subheader("🏢 Tambah Bandara")
        with st.form("form_bandara"):
            iata     = st.text_input("Kode IATA (3 huruf):")
            nama     = st.text_input("Nama Bandara:")
            kota     = st.text_input("Kota:")
            negara   = st.text_input("Negara:")
            utc      = st.selectbox("Zona Waktu:", ["UTC+6.5","UTC+7","UTC+8","UTC+9"])
            terminal = st.number_input("Jumlah Terminal:", 1, 10, 1)
            tipe     = st.selectbox("Tipe:", ["hub","spoke"])
            if st.form_submit_button("➕ Tambah Bandara", use_container_width=True):
                if len(iata.strip()) != 3:
                    st.error("Kode IATA harus 3 huruf.")
                elif sky.tambah_bandara(iata.strip().upper(), nama, kota,
                                        negara, utc, terminal, tipe):
                    st.success(f"✅ {iata.upper()} ditambahkan!")
                    st.rerun()
                else:
                    st.warning("⚠️ Kode IATA sudah terdaftar.")

    elif menu == "🛫 Tambah Rute":
        st.subheader("🛫 Tambah Rute Baru")
        semua = sky.get_semua_bandara()
        if len(semua) < 2:
            st.info("Tambahkan minimal 2 bandara.")
        else:
            with st.form("form_rute"):
                c1, c2 = st.columns(2)
                dari_b = c1.selectbox("Dari:", semua)
                ke_b   = c2.selectbox("Ke:", semua)
                kode     = st.text_input("Kode Penerbangan (cth: GA830):")
                maskapai = st.selectbox("Maskapai:", MASKAPAI_LIST)
                pesawat  = st.text_input("Tipe Pesawat:", "Boeing 737-800")
                c3, c4   = st.columns(2)
                jarak    = c3.number_input("Jarak (KM):", 1.0, 15000.0, 500.0)
                durasi   = c4.number_input("Durasi (menit):", 10, 1440, 90)
                jadwal_input = st.text_input("Jadwal (pisah koma):", "06:00,12:00,18:00")
                hari_input   = st.multiselect("Hari Operasi:",
                                              ["Setiap Hari"]+HARI_MINGGU,
                                              default=["Setiap Hari"])
                eco_h = st.number_input("Harga Ekonomi (Rp):", 100_000, 50_000_000, 1_000_000, 50_000)
                bis_h = st.number_input("Harga Bisnis (Rp):",  500_000,100_000_000, 3_500_000,100_000)

                if st.form_submit_button("➕ Tambah Rute", use_container_width=True):
                    if dari_b == ke_b:
                        st.error("Asal dan tujuan tidak boleh sama.")
                    else:
                        kursi = {
                            "ECO": {"kapasitas":150,"tersedia":134,"harga":eco_h},
                            "BIS": {"kapasitas": 24,"tersedia": 20,"harga":bis_h},
                        }
                        jadwal_list = [j.strip() for j in jadwal_input.split(",") if j.strip()]
                        if sky.tambah_rute(dari_b, ke_b, kode, maskapai, pesawat,
                                           jarak, durasi, jadwal_list, hari_input, kursi):
                            st.success(f"✅ Rute {dari_b}→{ke_b} ditambahkan!")
                            st.rerun()
                        else:
                            st.error("❌ Gagal. Periksa data kembali.")

    elif menu == "🗑️ Hapus Data":
        st.subheader("🗑️ Hapus Data")
        semua = sky.get_semua_bandara()
        st.markdown("**Hapus Bandara**")
        if semua:
            hapus_b = st.selectbox("Pilih Bandara:", semua, key="hapus_bdr",
                                   format_func=lambda x:
                                   f"{x} — {sky.get_detail_bandara(x)['kota']}")
            if st.button("🗑️ Hapus Bandara", use_container_width=True):
                sky.hapus_bandara(hapus_b)
                st.success(f"✅ {hapus_b} dihapus.")
                st.rerun()
        st.divider()
        st.markdown("**Hapus Rute**")
        semua_rute = sky.get_semua_rute()
        if semua_rute:
            opsi = [f"{r['kode_penerbangan']}: {r['dari']}→{r['ke']} ({r['maskapai']})"
                    for r in semua_rute]
            pilih_r = st.selectbox("Pilih rute:", opsi, key="hapus_rte")
            if st.button("🗑️ Hapus Rute", use_container_width=True):
                idx = opsi.index(pilih_r)
                t = semua_rute[idx]
                sky.hapus_rute(t["dari"], t["ke"], t["kode_penerbangan"])
                st.success("✅ Rute dihapus.")
                st.rerun()
        else:
            st.info("Belum ada rute.")


# ── TABS UTAMA ───────────────────────────────────────────────

tab_peta, tab_cari, tab_jadwal, tab_bandara = st.tabs([
    "🌐 Peta Rute",
    "🔍 Cari Penerbangan",
    "📅 Jadwal & Maskapai",
    "🏢 Data Bandara",
])


# ─────────────────────────────────────────────────────────────
# TAB 1 — PETA RUTE
# ─────────────────────────────────────────────────────────────
with tab_peta:
    st.subheader("🌐 Peta Jaringan Penerbangan Asia Tenggara")
    st.caption("Setiap titik = bandara. Setiap garis = rute penerbangan langsung.")

    hub_list = sky.hub_tersibuk(3)
    if hub_list:
        cols = st.columns(3)
        for i, (iata, jml) in enumerate(hub_list):
            d = sky.get_detail_bandara(iata)
            cols[i].metric(f"🏆 Hub #{i+1}", iata,
                           help=f"{d['kota']} — {jml} rute keluar")

    gambar_peta()

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        rt = sky.rute_terpanjang()
        if rt:
            st.markdown(f"**✈️ Rute Terpanjang:**  \n"
                        f"`{rt.dari}` → `{rt.ke}` — **{rt.jarak_km:,.0f} KM** "
                        f"({rt.durasi_format()})  \n_{rt.maskapai}_")
    with col2:
        rp = sky.rute_terpendek_jarak()
        if rp:
            st.markdown(f"**✈️ Rute Terpendek:**  \n"
                        f"`{rp.dari}` → `{rp.ke}` — **{rp.jarak_km:,.0f} KM** "
                        f"({rp.durasi_format()})  \n_{rp.maskapai}_")


# ─────────────────────────────────────────────────────────────
# TAB 2 — CARI PENERBANGAN
# ─────────────────────────────────────────────────────────────
with tab_cari:
    st.subheader("🔍 Cari Penerbangan Optimal (Dijkstra)")

    semua_b = sky.get_semua_bandara()
    if len(semua_b) < 2:
        st.info("Tambahkan minimal 2 bandara terlebih dahulu.")
    else:
        ca, cb, cc, cd = st.columns(4)
        asal   = ca.selectbox("🛫 Asal:", semua_b,
                              format_func=lambda x:
                              f"{x} — {sky.get_detail_bandara(x)['kota']}")
        tujuan = cb.selectbox("🛬 Tujuan:", semua_b,
                              format_func=lambda x:
                              f"{x} — {sky.get_detail_bandara(x)['kota']}")
        mode   = cc.selectbox("⚖️ Prioritas:", MODE_CARI,
                              format_func=lambda x: MODE_LABEL[x])
        kelas  = cd.selectbox("💺 Kelas:", KELAS_KURSI,
                              format_func=lambda x:
                              f"{KELAS_IKON[x]} {KELAS_LABEL[x]}")

        if st.button("🔍 CARI RUTE OPTIMAL", use_container_width=True):
            if asal == tujuan:
                st.warning("⚠️ Asal dan tujuan tidak boleh sama.")
            else:
                path, total, details = sky.cari_rute(asal, tujuan, mode, kelas)

                if path:
                    st.success(f"✅ Rute ditemukan! {MODE_LABEL[mode]}")

                    m1, m2, m3, m4 = st.columns(4)
                    if mode == "harga":
                        m1.metric("💰 Total Harga", format_harga(total))
                    elif mode == "durasi":
                        m1.metric("⏱️ Total Durasi", format_durasi(int(total)))
                    else:
                        m1.metric("📏 Total Jarak", f"{total:,.0f} KM")
                    m2.metric("✈️ Kota Disinggahi", len(path))
                    m3.metric("🔄 Transit", max(0, len(path)-2))
                    m4.metric("💺 Kelas", f"{KELAS_IKON[kelas]} {KELAS_LABEL[kelas]}")

                    st.markdown("**Jalur:** " + " → ".join(f"`{n}`" for n in path))

                    for i, p in enumerate(details):
                        with st.expander(f"Segmen {i+1}: {p.dari} → {p.ke} | {p.kode_penerbangan} | {p.maskapai}"):
                            d1, d2, d3 = st.columns(3)
                            d1.markdown(f"**Pesawat:** {p.pesawat}  \n"
                                        f"**Jarak:** {p.jarak_km:,.0f} KM  \n"
                                        f"**Durasi:** {p.durasi_format()}")
                            d2.markdown(f"**Jadwal:** {', '.join(p.jadwal)}  \n"
                                        f"**Hari:** {', '.join(p.hari_operasi)}")
                            harga_kelas = p.kursi.get(kelas, {}).get("harga", 0)
                            tersedia    = p.kursi.get(kelas, {}).get("tersedia", 0)
                            d3.markdown(f"**Kelas:** {KELAS_IKON[kelas]} {KELAS_LABEL[kelas]}  \n"
                                        f"**Harga:** {format_harga(harga_kelas)}  \n"
                                        f"**Kursi:** {tersedia} tersedia")

                    gambar_peta(highlight_path=path)
                else:
                    st.error(f"❌ Tidak ada rute dari **{asal}** ke **{tujuan}** "
                             f"untuk kelas {KELAS_LABEL[kelas]}.")

        # Bandingkan semua mode
        st.divider()
        if st.button("🔄 Bandingkan Harga vs Durasi vs Jarak", use_container_width=True):
            if asal == tujuan:
                st.warning("Asal dan tujuan tidak boleh sama.")
            else:
                hasil = sky.cari_semua_mode(asal, tujuan, kelas)
                cols  = st.columns(3)
                for i, (m, (p, t, _)) in enumerate(hasil.items()):
                    with cols[i]:
                        st.markdown(f"### {MODE_LABEL[m]}")
                        if p:
                            val = format_harga(t) if m=="harga" else \
                                  format_durasi(int(t)) if m=="durasi" else \
                                  f"{t:,.0f} KM"
                            st.metric("Nilai Optimal", val)
                            st.caption(" → ".join(p))
                        else:
                            st.error("Tidak ada rute")


# ─────────────────────────────────────────────────────────────
# TAB 3 — JADWAL & MASKAPAI
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
            j_ke   = st.selectbox("Ke:", semua_b, key="jd_ke",
                                  format_func=lambda x:
                                  f"{x} — {sky.get_detail_bandara(x)['kota']}")
            j_hari = st.selectbox("Hari:", ["Semua Hari"] + HARI_MINGGU)

            if j_dari != j_ke:
                rute_list = sky.get_rute_antara(j_dari, j_ke) \
                            if j_hari == "Semua Hari" \
                            else sky.jadwal_tersedia(j_dari, j_ke, j_hari)

                if rute_list:
                    for p in rute_list:
                        with st.expander(f"✈️ {p.kode_penerbangan} — {p.maskapai}"):
                            st.markdown(f"**Pesawat:** {p.pesawat}  \n"
                                        f"**Durasi:** {p.durasi_format()} | "
                                        f"**Jarak:** {p.jarak_km:,.0f} KM  \n"
                                        f"**Hari:** {', '.join(p.hari_operasi)}")
                            st.markdown("**Jadwal Berangkat → Tiba:**")
                            cols_j = st.columns(4)
                            for idx, jam in enumerate(p.jadwal):
                                tiba = p.hitung_tiba(jam)
                                cols_j[idx%4].markdown(f"🕐 **{jam}** → {tiba}")
                            st.markdown("**Harga:**")
                            for kls in KELAS_KURSI:
                                if kls in p.kursi:
                                    k_d = p.kursi[kls]
                                    st.markdown(
                                        f"{KELAS_IKON[kls]} **{KELAS_LABEL[kls]}**: "
                                        f"{format_harga(k_d['harga'])} | "
                                        f"Kursi: {k_d['tersedia']}/{k_d['kapasitas']}"
                                    )
                else:
                    st.info(f"Tidak ada penerbangan {j_dari}→{j_ke}"
                            + (f" pada {j_hari}" if j_hari != "Semua Hari" else "") + ".")

    with col_j2:
        st.markdown("#### 🏢 Filter per Maskapai")
        maskapai_ada = sorted({r["maskapai"] for r in sky.get_semua_rute()})
        if maskapai_ada:
            pilih_m = st.selectbox("Pilih Maskapai:", maskapai_ada)
            rute_m  = sky.filter_maskapai(pilih_m)
            st.metric("Total Rute", len(rute_m))
            for r in rute_m:
                dari_d = sky.get_detail_bandara(r["dari"])
                ke_d   = sky.get_detail_bandara(r["ke"])
                eco_h  = r["kursi"].get("ECO",{}).get("harga", 0)
                st.markdown(
                    f"**{r['kode_penerbangan']}** — {r['dari']} ({dari_d['kota']}) → "
                    f"{r['ke']} ({ke_d['kota']})  \n"
                    f"_{r['pesawat']} | {r['jarak_km']:,.0f} KM | "
                    f"ab {format_harga(eco_h)}_"
                )
        else:
            st.info("Belum ada data rute.")


# ─────────────────────────────────────────────────────────────
# TAB 4 — DATA BANDARA + BFS/DFS
# ─────────────────────────────────────────────────────────────
with tab_bandara:
    st.subheader("🏢 Data Bandara Asia Tenggara")

    semua_detail = sky.get_semua_bandara_detail()
    per_negara   = {}
    for b in semua_detail:
        per_negara.setdefault(b["negara"], []).append(b)

    for negara, list_b in sorted(per_negara.items()):
        warna_n = WARNA_NEGARA.get(negara, "#64748b")
        st.markdown(f"#### 🌏 {negara}")
        cols_b = st.columns(min(len(list_b), 4))
        for i, b in enumerate(list_b):
            rute_k = len(sky.get_rute_dari(b["iata"]))
            with cols_b[i % 4]:
                st.markdown(
                    f"**{b['iata']}** — {b['nama']}  \n"
                    f"📍 {b['kota']} | {b['zona_waktu']}  \n"
                    f"Tipe: `{b['tipe'].upper()}` | {b['terminal']} terminal | {rute_k} rute"
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
                hasil = sky.bfs(bfs_start)
                st.markdown(" → ".join(f"`{x}`" for x in hasil))
                st.caption(f"Total {len(hasil)} bandara terjangkau.")

    with col_t2:
        st.markdown("**DFS (Depth-First Search)**")
        st.caption("Telusuri sedalam mungkin sebelum kembali.")
        if semua_b:
            dfs_start = st.selectbox("Mulai dari:", semua_b, key="dfs_s")
            if st.button("▶ Jalankan DFS"):
                hasil = sky.dfs(dfs_start)
                st.markdown(" → ".join(f"`{x}`" for x in hasil))
                st.caption(f"Total {len(hasil)} bandara terjangkau.")

    st.divider()
    st.markdown("#### 📋 Adjacency List")
    st.caption("Representasi internal graf sebagai dictionary Python.")
    adj = sky.adjacency_list
    for dari_k, tujuan_dict in adj.items():
        if tujuan_dict:
            st.markdown(f"**{dari_k}** → " +
                        ", ".join(f"`{ke}` ({info['kode']})"
                                  for ke, info in tujuan_dict.items()))
