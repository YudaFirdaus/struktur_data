# ============================================================
# SKYGRAF — graf.py
# Struktur data graf penerbangan Asia Tenggara
# Tanpa networkx — semua struktur data dibuat manual
# ============================================================

# ============================================================
# KONSTANTA GLOBAL
# ============================================================

KELAS_KURSI = ["ECO", "BIS", "FIR"]

KELAS_LABEL = {
    "ECO": "Ekonomi",
    "BIS": "Bisnis",
    "FIR": "First Class",
}

KELAS_IKON = {
    "ECO": "💺",
    "BIS": "🛋️",
    "FIR": "👑",
}

MODE_CARI = ["harga", "durasi", "jarak"]

MODE_LABEL = {
    "harga":  "💰 Harga Termurah",
    "durasi": "⏱️ Waktu Tercepat",
    "jarak":  "📏 Jarak Terpendek",
}

TIPE_BANDARA = ["hub", "spoke"]

HARI_MINGGU = [
    "Senin", "Selasa", "Rabu", "Kamis",
    "Jumat", "Sabtu", "Minggu",
]

# Daftar maskapai yang dipakai dalam data preset
MASKAPAI_LIST = [
    "Garuda Indonesia",
    "Lion Air",
    "AirAsia",
    "Citilink",
    "Batik Air",
    "Singapore Airlines",
    "Malaysia Airlines",
    "Thai Airways",
    "Philippine Airlines",
    "Vietnam Airlines",
]

# Daftar tipe pesawat
PESAWAT_LIST = [
    "Boeing 737-800",
    "Boeing 737 MAX",
    "Boeing 777-300ER",
    "Airbus A320",
    "Airbus A320neo",
    "Airbus A330-300",
    "Airbus A380",
    "ATR 72-600",
]


# ============================================================
# CLASS BANDARA — Merepresentasikan satu bandara (Vertex)
# ============================================================

class Bandara:
    """
    Satu node dalam graf — merepresentasikan sebuah bandara.

    Atribut:
        iata       (str): Kode IATA 3 huruf, unik. Contoh: "CGK"
        nama       (str): Nama lengkap bandara.
        kota       (str): Kota lokasi bandara.
        negara     (str): Negara lokasi bandara.
        zona_waktu (str): Zona waktu UTC. Contoh: "UTC+7"
        terminal   (int): Jumlah terminal aktif.
        tipe       (str): "hub" (bandara utama) atau "spoke" (kecil).
    """

    def __init__(self, iata, nama, kota, negara,
                 zona_waktu="UTC+7", terminal=1, tipe="spoke"):
        self.iata       = iata.upper()
        self.nama       = nama
        self.kota       = kota
        self.negara     = negara
        self.zona_waktu = zona_waktu
        self.terminal   = terminal
        self.tipe       = tipe

    def __repr__(self):
        return f"Bandara({self.iata} — {self.kota}, {self.negara})"

    def to_dict(self):
        """Ubah ke dict untuk ekspor JSON."""
        return {
            "iata":       self.iata,
            "nama":       self.nama,
            "kota":       self.kota,
            "negara":     self.negara,
            "zona_waktu": self.zona_waktu,
            "terminal":   self.terminal,
            "tipe":       self.tipe,
        }


# ============================================================
# CLASS PENERBANGAN — Merepresentasikan satu rute (Edge)
# ============================================================

class Penerbangan:
    """
    Satu edge dalam graf — merepresentasikan rute penerbangan.

    Atribut:
        dari             (str)  : Kode IATA asal.
        ke               (str)  : Kode IATA tujuan.
        kode_penerbangan (str)  : Nomor penerbangan. Contoh: "GA830"
        maskapai         (str)  : Nama maskapai.
        pesawat          (str)  : Tipe pesawat.
        jarak_km         (float): Jarak geografis dalam KM.
        durasi_mnt       (int)  : Durasi terbang dalam menit.
        jadwal           (list) : Jam keberangkatan. ["06:00","10:30"]
        hari_operasi     (list) : Hari terbang. ["Setiap Hari"] atau
                                  ["Senin","Rabu","Jumat"]
        kursi            (dict) : Data kelas kursi.
                                  Format:
                                  {
                                    "ECO": {
                                      "kapasitas": 150,
                                      "tersedia":  134,
                                      "harga":     1_350_000
                                    },
                                    "BIS": { ... },
                                    "FIR": { ... },  # opsional
                                  }
    """

    def __init__(self, dari, ke, kode_penerbangan, maskapai, pesawat,
                 jarak_km, durasi_mnt, jadwal, hari_operasi, kursi):
        self.dari             = dari.upper()
        self.ke               = ke.upper()
        self.kode_penerbangan = kode_penerbangan
        self.maskapai         = maskapai
        self.pesawat          = pesawat
        self.jarak_km         = float(jarak_km)
        self.durasi_mnt       = int(durasi_mnt)
        self.jadwal           = jadwal           # list of "HH:MM"
        self.hari_operasi     = hari_operasi     # list of str
        self.kursi            = kursi            # dict

    def __repr__(self):
        return (f"Penerbangan({self.kode_penerbangan}: "
                f"{self.dari}→{self.ke}, {self.durasi_mnt}mnt)")

    def get_bobot(self, mode="harga", kelas="ECO"):
        """
        Mengembalikan nilai bobot sesuai mode pencarian dan kelas.

        Parameter:
            mode  (str): "harga" | "durasi" | "jarak"
            kelas (str): "ECO"   | "BIS"    | "FIR"

        Return:
            float — nilai bobot untuk Dijkstra.
            float("inf") jika kelas tidak tersedia di penerbangan ini.
        """
        if mode == "durasi":
            return float(self.durasi_mnt)
        if mode == "jarak":
            return float(self.jarak_km)
        # mode == "harga"
        if kelas not in self.kursi:
            return float("inf")   # kelas tidak tersedia
        return float(self.kursi[kelas]["harga"])

    def kursi_tersedia(self, kelas="ECO"):
        """Cek apakah masih ada kursi kosong untuk kelas tertentu."""
        if kelas not in self.kursi:
            return False
        return self.kursi[kelas]["tersedia"] > 0

    def hitung_tiba(self, jam_berangkat):
        """
        Menghitung jam tiba dari jam keberangkatan.

        Parameter:
            jam_berangkat (str): Format "HH:MM". Contoh: "06:00"

        Return:
            str — jam tiba dalam format "HH:MM".
        """
        h, m = map(int, jam_berangkat.split(":"))
        total = h * 60 + m + self.durasi_mnt
        tiba_h = (total // 60) % 24
        tiba_m = total % 60
        return f"{tiba_h:02d}:{tiba_m:02d}"

    def operasi_pada_hari(self, hari):
        """
        Cek apakah penerbangan beroperasi pada hari tertentu.

        Parameter:
            hari (str): Nama hari. Contoh: "Senin"

        Return:
            True jika beroperasi, False jika tidak.
        """
        if "Setiap Hari" in self.hari_operasi:
            return True
        return hari in self.hari_operasi

    def durasi_format(self):
        """Mengembalikan durasi dalam format '2j 5m'."""
        jam = self.durasi_mnt // 60
        mnt = self.durasi_mnt % 60
        return f"{jam}j {mnt}m" if mnt else f"{jam}j"

    def to_dict(self):
        """Ubah ke dict untuk ekspor JSON."""
        return {
            "dari":             self.dari,
            "ke":               self.ke,
            "kode_penerbangan": self.kode_penerbangan,
            "maskapai":         self.maskapai,
            "pesawat":          self.pesawat,
            "jarak_km":         self.jarak_km,
            "durasi_mnt":       self.durasi_mnt,
            "jadwal":           self.jadwal,
            "hari_operasi":     self.hari_operasi,
            "kursi":            self.kursi,
        }


# ============================================================
# CLASS GRAFBANDARA — Struktur data utama (Adjacency List Manual)
# ============================================================

class GrafBandara:
    """
    Graf berarah berbobot untuk jaringan penerbangan.

    Menggunakan adjacency list manual (dict Python).
    networkx TIDAK dipakai di sini — hanya di app.py untuk gambar peta.

    Struktur internal:
        _bandara : dict { iata_str → Bandara }
        _adj     : dict { iata_str → [Penerbangan, ...] }

    Graf ini BERARAH — rute CGK→SIN ≠ SIN→CGK karena harga
    dan jadwal bisa berbeda di tiap arah.
    """

    def __init__(self):
        self._bandara = {}   # { iata: Bandara }
        self._adj     = {}   # { iata: [Penerbangan] }

    # ----------------------------------------------------------
    # BAGIAN 1: MANAJEMEN BANDARA (VERTEX)
    # ----------------------------------------------------------

    def tambah_bandara(self, iata, nama, kota, negara,
                       zona_waktu="UTC+7", terminal=1, tipe="spoke"):
        """
        Menambah bandara baru ke dalam graf.

        Return:
            True  → berhasil.
            False → kode IATA sudah terdaftar.
        """
        iata = iata.upper()
        if iata in self._bandara:
            return False

        self._bandara[iata] = Bandara(
            iata, nama, kota, negara, zona_waktu, terminal, tipe
        )
        self._adj[iata] = []
        return True

    def hapus_bandara(self, iata):
        """
        Menghapus bandara dan semua rute yang berhubungan.

        Return:
            True / False
        """
        iata = iata.upper()
        if iata not in self._bandara:
            return False

        del self._bandara[iata]
        del self._adj[iata]

        # Hapus semua edge yang menuju bandara ini
        for kode in self._adj:
            self._adj[kode] = [
                p for p in self._adj[kode] if p.ke != iata
            ]
        return True

    def get_semua_bandara(self):
        """Mengembalikan list kode IATA semua bandara."""
        return list(self._bandara.keys())

    def get_detail_bandara(self, iata):
        """
        Mengembalikan dict atribut sebuah bandara.
        Return None jika tidak ditemukan.
        """
        iata = iata.upper()
        if iata not in self._bandara:
            return None
        return self._bandara[iata].to_dict()

    def get_semua_bandara_detail(self):
        """Mengembalikan list dict semua bandara."""
        return [b.to_dict() for b in self._bandara.values()]

    def _bandara_ada(self, iata):
        """Helper: cek apakah bandara terdaftar."""
        return iata.upper() in self._bandara

    # ----------------------------------------------------------
    # BAGIAN 2: MANAJEMEN PENERBANGAN (EDGE)
    # ----------------------------------------------------------

    def tambah_rute(self, dari, ke, kode_penerbangan, maskapai,
                    pesawat, jarak_km, durasi_mnt, jadwal,
                    hari_operasi, kursi):
        """
        Menambah rute penerbangan (edge berarah: dari → ke).

        Return:
            True  → berhasil.
            False → salah satu bandara tidak ada, atau jarak/durasi <= 0.
        """
        dari = dari.upper()
        ke   = ke.upper()

        if not self._bandara_ada(dari) or not self._bandara_ada(ke):
            return False
        if jarak_km <= 0 or durasi_mnt <= 0:
            return False

        p = Penerbangan(
            dari, ke, kode_penerbangan, maskapai, pesawat,
            jarak_km, durasi_mnt, jadwal, hari_operasi, kursi
        )
        self._adj[dari].append(p)
        return True

    def hapus_rute(self, dari, ke, kode_penerbangan=None):
        """
        Menghapus rute penerbangan.

        Jika kode_penerbangan diberikan, hanya hapus penerbangan
        dengan kode tersebut. Jika None, hapus semua rute dari→ke.

        Return:
            True / False
        """
        dari = dari.upper()
        ke   = ke.upper()

        if dari not in self._adj:
            return False

        sebelum = len(self._adj[dari])
        if kode_penerbangan:
            self._adj[dari] = [
                p for p in self._adj[dari]
                if not (p.ke == ke and
                        p.kode_penerbangan == kode_penerbangan)
            ]
        else:
            self._adj[dari] = [
                p for p in self._adj[dari] if p.ke != ke
            ]

        return len(self._adj[dari]) < sebelum

    def get_semua_rute(self):
        """
        Mengembalikan semua rute sebagai list of dict.
        Karena graf berarah, CGK→SIN dan SIN→CGK keduanya muncul.
        """
        hasil = []
        for penerbangan_list in self._adj.values():
            for p in penerbangan_list:
                hasil.append(p.to_dict())
        return hasil

    def get_rute_dari(self, iata):
        """
        Mengembalikan list Penerbangan yang berangkat dari bandara ini.
        Dipakai saat traversal dan Dijkstra.
        """
        return self._adj.get(iata.upper(), [])

    def get_rute_antara(self, dari, ke):
        """
        Mengembalikan semua penerbangan dari → ke.
        Bisa lebih dari satu (beda maskapai/jadwal).
        """
        dari = dari.upper()
        ke   = ke.upper()
        return [p for p in self._adj.get(dari, []) if p.ke == ke]

    def filter_maskapai(self, nama_maskapai):
        """
        Mengembalikan semua rute dari maskapai tertentu.
        """
        hasil = []
        for penerbangan_list in self._adj.values():
            for p in penerbangan_list:
                if p.maskapai == nama_maskapai:
                    hasil.append(p.to_dict())
        return hasil

    def jadwal_tersedia(self, dari, ke, hari):
        """
        Mengembalikan penerbangan yang beroperasi pada hari tertentu.

        Parameter:
            dari (str): Kode IATA asal.
            ke   (str): Kode IATA tujuan.
            hari (str): Nama hari. Contoh: "Senin"

        Return:
            list of Penerbangan.
        """
        return [
            p for p in self.get_rute_antara(dari, ke)
            if p.operasi_pada_hari(hari)
        ]

    # ----------------------------------------------------------
    # BAGIAN 3: TRAVERSAL MANUAL
    # ----------------------------------------------------------

    def bfs(self, mulai):
        """
        Breadth-First Search — telusuri semua bandara yang
        terhubung dari titik awal (lapis per lapis).

        Return:
            list kode IATA dalam urutan BFS.
        """
        mulai = mulai.upper()
        if not self._bandara_ada(mulai):
            return []

        dikunjungi = []
        antrian    = [mulai]
        sudah      = {mulai}

        while antrian:
            sekarang = antrian.pop(0)   # FIFO
            dikunjungi.append(sekarang)

            for penerbangan in self._adj[sekarang]:
                if penerbangan.ke not in sudah:
                    sudah.add(penerbangan.ke)
                    antrian.append(penerbangan.ke)

        return dikunjungi

    def dfs(self, mulai, _sudah=None):
        """
        Depth-First Search — telusuri sedalam mungkin (rekursif).

        Return:
            list kode IATA dalam urutan DFS.
        """
        mulai = mulai.upper()
        if not self._bandara_ada(mulai):
            return []

        if _sudah is None:
            _sudah = set()

        _sudah.add(mulai)
        hasil = [mulai]

        for penerbangan in self._adj[mulai]:
            if penerbangan.ke not in _sudah:
                hasil.extend(self.dfs(penerbangan.ke, _sudah))

        return hasil

    def terhubung(self, dari, ke):
        """
        Cek apakah ada jalur (langsung maupun transit)
        dari bandara 'dari' ke bandara 'ke'.
        """
        return ke.upper() in self.bfs(dari)

    # ----------------------------------------------------------
    # BAGIAN 4: DIJKSTRA MANUAL + MULTI-BOBOT
    # ----------------------------------------------------------

    def _dijkstra(self, dari, ke, mode="harga", kelas="ECO"):
        """
        Implementasi Dijkstra manual dengan multi-bobot.

        Cara kerja:
          1. Inisialisasi semua jarak = ∞, kecuali titik awal = 0.
          2. Pilih vertex dengan jarak terkecil dari set 'belum'.
          3. Untuk setiap rute keluar dari vertex tersebut:
             - Lewati jika kelas tidak tersedia di penerbangan itu.
             - Hitung jarak alternatif: jarak_sekarang + bobot_edge.
             - Jika lebih kecil, perbarui jarak dan catat path.
          4. Ulangi sampai vertex tujuan diproses.
          5. Rekonstruksi jalur dari dict 'sebelum'.

        Parameter:
            dari  (str): Kode IATA asal.
            ke    (str): Kode IATA tujuan.
            mode  (str): "harga" | "durasi" | "jarak"
            kelas (str): "ECO"   | "BIS"    | "FIR"

        Return:
            (path, total_bobot, detail_penerbangan)
            path               → list kode IATA yang dilalui.
            total_bobot        → total nilai bobot (harga/durasi/jarak).
            detail_penerbangan → list Penerbangan yang digunakan.
            Jika tidak ada rute: (None, 0, []).
        """
        dari = dari.upper()
        ke   = ke.upper()

        if not self._bandara_ada(dari) or not self._bandara_ada(ke):
            return None, 0, []

        INF     = float("inf")
        jarak   = {v: INF for v in self._bandara}
        sebelum = {v: None for v in self._bandara}
        edge_via= {v: None for v in self._bandara}  # simpan edge yang dipakai
        belum   = set(self._bandara.keys())
        jarak[dari] = 0

        while belum:
            # Pilih vertex belum dikunjungi dengan jarak terkecil
            sekarang = min(belum, key=lambda v: jarak[v])

            if jarak[sekarang] == INF:
                break   # tidak ada lagi yang terhubung
            if sekarang == ke:
                break   # sudah sampai tujuan

            belum.remove(sekarang)

            for penerbangan in self._adj[sekarang]:
                tujuan = penerbangan.ke
                if tujuan not in belum:
                    continue

                # Lewati jika mode harga dan kelas tidak tersedia
                if mode == "harga" and not penerbangan.kursi_tersedia(kelas):
                    continue

                bobot     = penerbangan.get_bobot(mode, kelas)
                jarak_alt = jarak[sekarang] + bobot

                if jarak_alt < jarak[tujuan]:
                    jarak[tujuan]    = jarak_alt
                    sebelum[tujuan]  = sekarang
                    edge_via[tujuan] = penerbangan

        # Cek apakah tujuan bisa dicapai
        if jarak[ke] == INF:
            return None, 0, []

        # Rekonstruksi jalur
        path    = []
        details = []
        langkah = ke
        while langkah is not None:
            path.append(langkah)
            if edge_via[langkah]:
                details.append(edge_via[langkah])
            langkah = sebelum[langkah]

        path.reverse()
        details.reverse()

        return path, round(jarak[ke], 2), details

    def cari_rute(self, dari, ke, mode="harga", kelas="ECO"):
        """
        Mencari rute optimal dari bandara asal ke tujuan.

        Parameter:
            dari  (str): Kode IATA asal.
            ke    (str): Kode IATA tujuan.
            mode  (str): "harga" | "durasi" | "jarak"
            kelas (str): "ECO"   | "BIS"    | "FIR"

        Return:
            (path, total, details) — lihat _dijkstra().
        """
        if mode not in MODE_CARI:
            return None, 0, []
        if mode == "harga" and kelas not in KELAS_KURSI:
            return None, 0, []
        return self._dijkstra(dari, ke, mode, kelas)

    def cari_semua_mode(self, dari, ke, kelas="ECO"):
        """
        Mencari rute optimal untuk ketiga mode sekaligus.

        Return:
            dict {
                "harga":  (path, total, details),
                "durasi": (path, total, details),
                "jarak":  (path, total, details),
            }
        """
        return {
            mode: self.cari_rute(dari, ke, mode, kelas)
            for mode in MODE_CARI
        }

    # ----------------------------------------------------------
    # BAGIAN 5: ANALITIK & UTILITAS
    # ----------------------------------------------------------

    def hub_tersibuk(self, top=5):
        """
        Mengembalikan bandara dengan rute terbanyak (derajat tertinggi).

        Return:
            list of tuple [(iata, jumlah_rute), ...] urut descending.
        """
        derajat = {
            iata: len(rute_list)
            for iata, rute_list in self._adj.items()
        }
        return sorted(derajat.items(), key=lambda x: x[1], reverse=True)[:top]

    def rute_terpanjang(self):
        """
        Mengembalikan penerbangan dengan jarak_km terbesar.

        Return:
            Penerbangan atau None.
        """
        semua = [
            p for rute_list in self._adj.values()
            for p in rute_list
        ]
        if not semua:
            return None
        return max(semua, key=lambda p: p.jarak_km)

    def rute_terpendek_jarak(self):
        """
        Mengembalikan penerbangan dengan jarak_km terkecil.
        """
        semua = [
            p for rute_list in self._adj.values()
            for p in rute_list
        ]
        if not semua:
            return None
        return min(semua, key=lambda p: p.jarak_km)

    def ringkasan(self):
        """Mengembalikan statistik singkat graf."""
        semua_rute = self.get_semua_rute()
        maskapai   = set(r["maskapai"] for r in semua_rute)
        negara     = set(
            b.negara for b in self._bandara.values()
        )
        return {
            "total_bandara": len(self._bandara),
            "total_rute":    len(semua_rute),
            "total_maskapai":len(maskapai),
            "total_negara":  len(negara),
            "bandara_hub":   [
                iata for iata, b in self._bandara.items()
                if b.tipe == "hub"
            ],
        }

    @property
    def adjacency_list(self):
        """
        Adjacency list dalam format dict yang mudah dibaca.
        Format: { "CGK": { "SIN": {"kode":..., "jarak":...} } }
        """
        hasil = {}
        for iata, penerbangan_list in self._adj.items():
            hasil[iata] = {}
            for p in penerbangan_list:
                hasil[iata][p.ke] = {
                    "kode":     p.kode_penerbangan,
                    "maskapai": p.maskapai,
                    "jarak_km": p.jarak_km,
                    "durasi":   p.durasi_format(),
                    "jadwal":   p.jadwal,
                }
        return hasil

    # ----------------------------------------------------------
    # BAGIAN 6: EKSPOR & IMPOR JSON
    # ----------------------------------------------------------

    def ekspor_json(self):
        """Ekspor seluruh data ke dict siap disimpan ke file JSON."""
        return {
            "bandara": self.get_semua_bandara_detail(),
            "rute":    self.get_semua_rute(),
        }

    @classmethod
    def impor_json(cls, data):
        """
        Buat objek GrafBandara dari dict hasil baca file JSON.

        Parameter:
            data (dict): Hasil dari ekspor_json().

        Return:
            Objek GrafBandara yang sudah terisi.
        """
        g = cls()

        for b in data.get("bandara", []):
            g.tambah_bandara(
                iata=b["iata"], nama=b["nama"],
                kota=b["kota"], negara=b["negara"],
                zona_waktu=b.get("zona_waktu", "UTC+7"),
                terminal=b.get("terminal", 1),
                tipe=b.get("tipe", "spoke"),
            )

        for r in data.get("rute", []):
            g.tambah_rute(
                dari=r["dari"], ke=r["ke"],
                kode_penerbangan=r["kode_penerbangan"],
                maskapai=r["maskapai"], pesawat=r["pesawat"],
                jarak_km=r["jarak_km"], durasi_mnt=r["durasi_mnt"],
                jadwal=r["jadwal"], hari_operasi=r["hari_operasi"],
                kursi=r["kursi"],
            )

        return g


# ============================================================
# DATA PRESET — Jaringan Penerbangan Asia Tenggara
# ============================================================

def buat_graf_asean():
    """
    Membuat GrafBandara dengan data preset bandara
    dan rute penerbangan Asia Tenggara.

    Return:
        Objek GrafBandara siap pakai.
    """
    g = GrafBandara()

    # ---- BANDARA ----
    bandara_data = [
        # IATA,  Nama,                              Kota,          Negara,       UTC,      Term, Tipe
        ("CGK", "Soekarno-Hatta International",    "Jakarta",     "Indonesia",  "UTC+7",  3, "hub"),
        ("SUB", "Juanda International",             "Surabaya",    "Indonesia",  "UTC+7",  2, "hub"),
        ("DPS", "Ngurah Rai International",         "Denpasar",    "Indonesia",  "UTC+8",  2, "hub"),
        ("UPG", "Sultan Hasanuddin International",  "Makassar",    "Indonesia",  "UTC+8",  2, "spoke"),
        ("BTH", "Hang Nadim International",         "Batam",       "Indonesia",  "UTC+7",  1, "spoke"),
        ("SIN", "Changi Airport",                   "Singapura",   "Singapura",  "UTC+8",  4, "hub"),
        ("KUL", "Kuala Lumpur International",       "Kuala Lumpur","Malaysia",   "UTC+8",  2, "hub"),
        ("BKK", "Suvarnabhumi Airport",             "Bangkok",     "Thailand",   "UTC+7",  1, "hub"),
        ("DMK", "Don Mueang International",         "Bangkok",     "Thailand",   "UTC+7",  2, "spoke"),
        ("HKT", "Phuket International",             "Phuket",      "Thailand",   "UTC+7",  1, "spoke"),
        ("MNL", "Ninoy Aquino International",       "Manila",      "Filipina",   "UTC+8",  4, "hub"),
        ("HAN", "Noi Bai International",            "Hanoi",       "Vietnam",    "UTC+7",  2, "hub"),
        ("SGN", "Tan Son Nhat International",       "Ho Chi Minh", "Vietnam",    "UTC+7",  2, "hub"),
        ("RGN", "Yangon International",             "Yangon",      "Myanmar",    "UTC+6.5",1, "spoke"),
        ("PNH", "Phnom Penh International",         "Phnom Penh",  "Kamboja",    "UTC+7",  1, "spoke"),
        ("VTE", "Wattay International",             "Vientiane",   "Laos",       "UTC+7",  1, "spoke"),
        ("BWN", "Brunei International",             "Bandar Seri Begawan","Brunei","UTC+8",1, "spoke"),
    ]

    for row in bandara_data:
        g.tambah_bandara(*row)

    # ---- RUTE PENERBANGAN ----
    # Format: tambah_rute(dari, ke, kode, maskapai, pesawat,
    #                     jarak_km, durasi_mnt, jadwal, hari_operasi, kursi)

    def kursi_full(eco_h, bis_h, fir_h=None,
                   eco_k=150, bis_k=24, fir_k=8):
        """Helper buat dict kursi."""
        k = {
            "ECO": {"kapasitas": eco_k, "tersedia": eco_k - 16, "harga": eco_h},
            "BIS": {"kapasitas": bis_k, "tersedia": bis_k - 4,  "harga": bis_h},
        }
        if fir_h:
            k["FIR"] = {"kapasitas": fir_k, "tersedia": fir_k - 1, "harga": fir_h}
        return k

    def kursi_budget(eco_h, bis_h, eco_k=180, bis_k=12):
        """Helper buat dict kursi maskapai budget (tanpa First)."""
        return {
            "ECO": {"kapasitas": eco_k, "tersedia": eco_k - 20, "harga": eco_h},
            "BIS": {"kapasitas": bis_k, "tersedia": bis_k - 2,  "harga": bis_h},
        }

    rute_data = [
        # ── CGK (Jakarta) ──────────────────────────────────────
        ("CGK","SIN","GA830","Garuda Indonesia","Boeing 737-800",
         1410,125,["06:00","10:30","15:00","19:45"],["Setiap Hari"],
         kursi_full(1_350_000, 4_200_000, 12_500_000)),

        ("CGK","SIN","QZ8074","AirAsia","Airbus A320",
         1410,125,["07:30","13:00","20:00"],["Setiap Hari"],
         kursi_budget(850_000, 2_800_000)),

        ("CGK","KUL","GA716","Garuda Indonesia","Boeing 737-800",
         1160,115,["08:00","14:00","20:30"],["Setiap Hari"],
         kursi_full(1_100_000, 3_800_000, 11_000_000)),

        ("CGK","KUL","AK391","AirAsia","Airbus A320neo",
         1160,115,["06:30","11:00","16:30","22:00"],["Setiap Hari"],
         kursi_budget(700_000, 2_500_000)),

        ("CGK","BKK","GA866","Garuda Indonesia","Airbus A330-300",
         2250,210,["08:30","22:00"],["Setiap Hari"],
         kursi_full(2_100_000, 6_500_000, 18_000_000)),

        ("CGK","SUB","GA306","Garuda Indonesia","Boeing 737-800",
         664, 70, ["06:00","08:00","10:00","12:00","14:00","16:00","18:00","20:00"],
         ["Setiap Hari"], kursi_budget(450_000, 1_500_000)),

        ("CGK","DPS","GA406","Garuda Indonesia","Boeing 737-800",
         950, 95, ["06:00","09:00","12:00","15:00","18:00","21:00"],
         ["Setiap Hari"], kursi_budget(650_000, 2_100_000)),

        ("CGK","MNL","GA880","Garuda Indonesia","Airbus A330-300",
         2790,240,["09:00","21:00"],["Setiap Hari"],
         kursi_full(2_800_000, 8_500_000, 22_000_000)),

        ("CGK","BTH","GA162","Garuda Indonesia","ATR 72-600",
         880, 85, ["06:30","11:30","16:00"],["Setiap Hari"],
         kursi_budget(600_000, 1_800_000, 120, 8)),

        # ── SIN (Singapura) ────────────────────────────────────
        ("SIN","CGK","GA831","Garuda Indonesia","Boeing 737-800",
         1410,130,["09:30","14:00","18:30","23:00"],["Setiap Hari"],
         kursi_full(1_450_000, 4_500_000, 13_000_000)),

        ("SIN","KUL","SQ118","Singapore Airlines","Airbus A320",
         350, 50, ["06:00","08:00","10:00","12:00","14:00","16:00","18:00","20:00","22:00"],
         ["Setiap Hari"], kursi_full(900_000, 3_200_000)),

        ("SIN","BKK","SQ708","Singapore Airlines","Airbus A330-300",
         1430,145,["07:00","12:00","18:00","23:00"],["Setiap Hari"],
         kursi_full(1_600_000, 5_200_000, 16_000_000)),

        ("SIN","MNL","SQ922","Singapore Airlines","Boeing 777-300ER",
         2390,210,["08:30","14:00","20:30"],["Setiap Hari"],
         kursi_full(2_200_000, 7_000_000, 20_000_000)),

        ("SIN","HAN","SQ172","Singapore Airlines","Airbus A320",
         1680,155,["09:00","15:00","21:00"],["Setiap Hari"],
         kursi_full(1_500_000, 5_000_000)),

        ("SIN","SGN","SQ186","Singapore Airlines","Airbus A320",
         1170,115,["07:30","11:30","15:30","20:00"],["Setiap Hari"],
         kursi_full(1_200_000, 4_000_000)),

        ("SIN","BTH","SQ5416","Singapore Airlines","ATR 72-600",
         180, 30, ["07:00","10:00","13:00","16:00","19:00"],["Setiap Hari"],
         kursi_budget(400_000, 1_200_000, 120, 8)),

        # ── KUL (Kuala Lumpur) ─────────────────────────────────
        ("KUL","CGK","MH714","Malaysia Airlines","Boeing 737-800",
         1160,120,["08:30","14:30","21:00"],["Setiap Hari"],
         kursi_full(1_200_000, 4_000_000, 11_500_000)),

        ("KUL","SIN","AK701","AirAsia","Airbus A320",
         350, 55, ["05:30","07:30","09:30","11:30","13:30","15:30","17:30","19:30","21:30"],
         ["Setiap Hari"], kursi_budget(550_000, 1_800_000)),

        ("KUL","BKK","AK880","AirAsia","Airbus A320neo",
         1550,155,["06:30","11:00","16:00","21:00"],["Setiap Hari"],
         kursi_budget(900_000, 2_800_000)),

        ("KUL","HKT","AK838","AirAsia","Airbus A320",
         850, 90, ["07:00","13:00","19:00"],["Setiap Hari"],
         kursi_budget(700_000, 2_200_000)),

        ("KUL","RGN","MH740","Malaysia Airlines","Boeing 737-800",
         2050,185,["09:00","22:30"],["Setiap Hari"],
         kursi_full(1_800_000, 5_500_000)),

        ("KUL","DPS","AK368","AirAsia","Airbus A320",
         1970,185,["08:00","22:00"],["Setiap Hari"],
         kursi_budget(1_100_000, 3_200_000)),

        # ── BKK (Bangkok) ──────────────────────────────────────
        ("BKK","CGK","TG433","Thai Airways","Airbus A330-300",
         2250,220,["10:00","23:30"],["Setiap Hari"],
         kursi_full(2_300_000, 7_000_000, 19_000_000)),

        ("BKK","SIN","TG401","Thai Airways","Airbus A330-300",
         1430,150,["08:00","14:00","20:30"],["Setiap Hari"],
         kursi_full(1_700_000, 5_500_000, 17_000_000)),

        ("BKK","HAN","TG560","Thai Airways","Airbus A320",
         1290,130,["09:30","16:00"],["Setiap Hari"],
         kursi_full(1_300_000, 4_200_000)),

        ("BKK","RGN","PG701","Bangkok Airways","ATR 72-600",
         750, 75, ["07:30","12:30","17:00"],
         ["Senin","Rabu","Jumat","Sabtu","Minggu"],
         kursi_budget(900_000, 2_500_000, 120, 8)),

        ("BKK","HKT","PG101","Bangkok Airways","ATR 72-600",
         600, 65, ["06:30","08:30","10:30","12:30","14:30","16:30","18:30"],
         ["Setiap Hari"], kursi_budget(600_000, 1_800_000, 120, 8)),

        # ── DPS (Bali) ─────────────────────────────────────────
        ("DPS","CGK","JT804","Lion Air","Boeing 737-800",
         950, 95, ["06:00","08:00","10:00","12:00","14:00","16:00","18:00","20:00"],
         ["Setiap Hari"], kursi_budget(550_000, 1_700_000)),

        ("DPS","SIN","GA348","Garuda Indonesia","Boeing 737-800",
         1940,180,["08:30","18:00"],["Setiap Hari"],
         kursi_full(1_800_000, 5_500_000)),

        ("DPS","SUB","JT568","Lion Air","Boeing 737-800",
         550, 60, ["06:30","10:00","14:00","18:30"],["Setiap Hari"],
         kursi_budget(380_000, 1_200_000)),

        # ── SUB (Surabaya) ─────────────────────────────────────
        ("SUB","CGK","GA307","Garuda Indonesia","Boeing 737-800",
         664, 70, ["05:30","07:30","09:30","11:30","13:30","15:30","17:30","19:30"],
         ["Setiap Hari"], kursi_budget(450_000, 1_500_000)),

        ("SUB","SIN","GA346","Garuda Indonesia","Boeing 737-800",
         1870,170,["08:00","20:00"],["Setiap Hari"],
         kursi_full(1_700_000, 5_200_000)),

        # ── MNL (Manila) ───────────────────────────────────────
        ("MNL","CGK","PR502","Philippine Airlines","Airbus A330-300",
         2790,245,["08:00","22:00"],["Setiap Hari"],
         kursi_full(3_000_000, 9_000_000, 23_000_000)),

        ("MNL","SIN","PR500","Philippine Airlines","Airbus A320",
         2390,215,["07:30","13:00","20:00"],["Setiap Hari"],
         kursi_full(2_300_000, 7_200_000)),

        ("MNL","BKK","PR730","Philippine Airlines","Airbus A320",
         2200,195,["09:00","20:30"],["Setiap Hari"],
         kursi_full(2_100_000, 6_500_000)),

        # ── SGN (Ho Chi Minh) ──────────────────────────────────
        ("SGN","SIN","VN601","Vietnam Airlines","Airbus A320",
         1170,120,["07:00","11:00","15:00","20:00"],["Setiap Hari"],
         kursi_full(1_300_000, 4_200_000)),

        ("SGN","HAN","VN215","Vietnam Airlines","Airbus A320",
         1140,115,["06:00","08:00","10:00","12:00","14:00","16:00","18:00","20:00"],
         ["Setiap Hari"], kursi_budget(500_000, 1_600_000)),

        ("SGN","BKK","VN601","Vietnam Airlines","Airbus A320",
         1000,100,["09:00","16:00"],["Setiap Hari"],
         kursi_full(1_100_000, 3_500_000)),

        ("SGN","PNH","VN831","Vietnam Airlines","ATR 72-600",
         240, 40, ["07:00","12:00","17:00"],
         ["Senin","Selasa","Kamis","Sabtu"],
         kursi_budget(450_000, 1_400_000, 120, 8)),

        # ── HAN (Hanoi) ────────────────────────────────────────
        ("HAN","SIN","VN631","Vietnam Airlines","Airbus A320",
         1680,160,["08:00","14:30","21:00"],["Setiap Hari"],
         kursi_full(1_600_000, 5_000_000)),

        ("HAN","BKK","VN610","Vietnam Airlines","Airbus A320",
         1290,135,["10:00","17:00"],["Setiap Hari"],
         kursi_full(1_400_000, 4_500_000)),
    ]

    for row in rute_data:
        g.tambah_rute(*row)

    return g