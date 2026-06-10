# ============================================================
# SKYGRAF — graf.py
# Struktur data graf penerbangan Asia Tenggara
# Tanpa networkx — semua struktur data dibuat manual
# ============================================================

# ============================================================
# KONSTANTA GLOBAL
# ============================================================

KELAS_KURSI = ["ECO", "BIS", "FIR"]
KELAS_LABEL = {"ECO": "Ekonomi", "BIS": "Bisnis", "FIR": "First Class"}
KELAS_IKON  = {"ECO": "💺", "BIS": "🛋️", "FIR": "👑"}

MODE_CARI  = ["harga", "durasi", "jarak"]
MODE_LABEL = {
    "harga":  "💰 Harga Termurah",
    "durasi": "⏱️ Waktu Tercepat",
    "jarak":  "📏 Jarak Terpendek",
}

HARI_MINGGU  = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"]
MASKAPAI_LIST = [
    "Garuda Indonesia","Lion Air","AirAsia","Citilink","Batik Air",
    "Singapore Airlines","Malaysia Airlines","Thai Airways",
    "Philippine Airlines","Vietnam Airlines",
]


# ============================================================
# CLASS BANDARA — Node/Vertex dalam graf
# ============================================================

class Bandara:
    """Merepresentasikan satu bandara (vertex dalam graf)."""

    def __init__(self, iata, nama, kota, negara,
                 zona_waktu="UTC+7", terminal=1, tipe="spoke"):
        self.iata       = iata.upper()
        self.nama       = nama
        self.kota       = kota
        self.negara     = negara
        self.zona_waktu = zona_waktu
        self.terminal   = terminal
        self.tipe       = tipe   # "hub" atau "spoke"

    def __repr__(self):
        return f"Bandara({self.iata} — {self.kota}, {self.negara})"

    def to_dict(self):
        return {
            "iata": self.iata, "nama": self.nama, "kota": self.kota,
            "negara": self.negara, "zona_waktu": self.zona_waktu,
            "terminal": self.terminal, "tipe": self.tipe,
        }


# ============================================================
# CLASS PENERBANGAN — Edge dalam graf
# ============================================================

class Penerbangan:
    """
    Merepresentasikan satu rute penerbangan (edge berarah berbobot).

    kursi: dict format {
        "ECO": {"kapasitas": 150, "tersedia": 134, "harga": 1_350_000},
        "BIS": {...},
        "FIR": {...},  # opsional
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
        self.jadwal           = jadwal        # list "HH:MM"
        self.hari_operasi     = hari_operasi  # list str
        self.kursi            = kursi         # dict

    def __repr__(self):
        return f"Penerbangan({self.kode_penerbangan}: {self.dari}→{self.ke})"

    def get_bobot(self, mode="harga", kelas="ECO"):
        """Nilai bobot untuk Dijkstra sesuai mode & kelas."""
        if mode == "durasi":
            return float(self.durasi_mnt)
        if mode == "jarak":
            return float(self.jarak_km)
        # mode == "harga"
        if kelas not in self.kursi:
            return float("inf")
        return float(self.kursi[kelas]["harga"])

    def kursi_tersedia(self, kelas="ECO"):
        """Cek apakah masih ada kursi kosong untuk kelas ini."""
        return kelas in self.kursi and self.kursi[kelas]["tersedia"] > 0

    def operasi_pada_hari(self, hari):
        """True jika penerbangan beroperasi pada hari tersebut."""
        return "Setiap Hari" in self.hari_operasi or hari in self.hari_operasi

    def hitung_tiba(self, jam_berangkat):
        """Hitung jam tiba dari jam keberangkatan (format HH:MM)."""
        h, m = map(int, jam_berangkat.split(":"))
        total = h * 60 + m + self.durasi_mnt
        return f"{(total//60)%24:02d}:{total%60:02d}"

    def durasi_format(self):
        """Durasi dalam format '2j 5m'."""
        j, m = self.durasi_mnt // 60, self.durasi_mnt % 60
        return f"{j}j {m}m" if m else f"{j}j"

    def to_dict(self):
        return {
            "dari": self.dari, "ke": self.ke,
            "kode_penerbangan": self.kode_penerbangan,
            "maskapai": self.maskapai, "pesawat": self.pesawat,
            "jarak_km": self.jarak_km, "durasi_mnt": self.durasi_mnt,
            "jadwal": self.jadwal, "hari_operasi": self.hari_operasi,
            "kursi": self.kursi,
        }


# ============================================================
# CLASS GRAFBANDARA — Struktur data utama (Adjacency List Manual)
# ============================================================

class GrafBandara:
    """
    Graf berarah berbobot untuk jaringan penerbangan.
    Menggunakan adjacency list manual (dict Python).

    _bandara : { iata → Bandara }
    _adj     : { iata → [Penerbangan, ...] }
    """

    def __init__(self):
        self._bandara = {}
        self._adj     = {}

    # ── MANAJEMEN BANDARA (VERTEX) ──────────────────────────

    def tambah_bandara(self, iata, nama, kota, negara,
                       zona_waktu="UTC+7", terminal=1, tipe="spoke"):
        """Tambah bandara. Return True jika berhasil, False jika sudah ada."""
        iata = iata.upper()
        if iata in self._bandara:
            return False
        self._bandara[iata] = Bandara(iata, nama, kota, negara,
                                      zona_waktu, terminal, tipe)
        self._adj[iata] = []
        return True

    def hapus_bandara(self, iata):
        """Hapus bandara beserta semua rute yang terhubung."""
        iata = iata.upper()
        if iata not in self._bandara:
            return False
        del self._bandara[iata]
        del self._adj[iata]
        for k in self._adj:
            self._adj[k] = [p for p in self._adj[k] if p.ke != iata]
        return True

    def get_semua_bandara(self):
        return list(self._bandara.keys())

    def get_detail_bandara(self, iata):
        b = self._bandara.get(iata.upper())
        return b.to_dict() if b else None

    def get_semua_bandara_detail(self):
        return [b.to_dict() for b in self._bandara.values()]

    def _bandara_ada(self, iata):
        return iata.upper() in self._bandara

    # ── MANAJEMEN RUTE (EDGE) ───────────────────────────────

    def tambah_rute(self, dari, ke, kode_penerbangan, maskapai,
                    pesawat, jarak_km, durasi_mnt, jadwal,
                    hari_operasi, kursi):
        """Tambah rute (edge berarah dari→ke). Return True/False."""
        dari, ke = dari.upper(), ke.upper()
        if not self._bandara_ada(dari) or not self._bandara_ada(ke):
            return False
        if jarak_km <= 0 or durasi_mnt <= 0:
            return False
        self._adj[dari].append(Penerbangan(
            dari, ke, kode_penerbangan, maskapai, pesawat,
            jarak_km, durasi_mnt, jadwal, hari_operasi, kursi
        ))
        return True

    def hapus_rute(self, dari, ke, kode_penerbangan=None):
        """Hapus rute. Jika kode diberikan, hapus hanya yang cocok."""
        dari, ke = dari.upper(), ke.upper()
        if dari not in self._adj:
            return False
        sebelum = len(self._adj[dari])
        if kode_penerbangan:
            self._adj[dari] = [
                p for p in self._adj[dari]
                if not (p.ke == ke and p.kode_penerbangan == kode_penerbangan)
            ]
        else:
            self._adj[dari] = [p for p in self._adj[dari] if p.ke != ke]
        return len(self._adj[dari]) < sebelum

    def get_semua_rute(self):
        return [p.to_dict() for lst in self._adj.values() for p in lst]

    def get_rute_dari(self, iata):
        return self._adj.get(iata.upper(), [])

    def get_rute_antara(self, dari, ke):
        return [p for p in self._adj.get(dari.upper(), [])
                if p.ke == ke.upper()]

    def filter_maskapai(self, nama_maskapai):
        return [p.to_dict() for lst in self._adj.values()
                for p in lst if p.maskapai == nama_maskapai]

    def jadwal_tersedia(self, dari, ke, hari):
        """Penerbangan dari→ke yang beroperasi pada hari tertentu."""
        return [p for p in self.get_rute_antara(dari, ke)
                if p.operasi_pada_hari(hari)]

    # ── TRAVERSAL: BFS & DFS ────────────────────────────────

    def bfs(self, mulai):
        """Breadth-First Search — kunjungi bandara lapis per lapis."""
        mulai = mulai.upper()
        if not self._bandara_ada(mulai):
            return []
        dikunjungi, antrian, sudah = [], [mulai], {mulai}
        while antrian:
            sekarang = antrian.pop(0)     # FIFO
            dikunjungi.append(sekarang)
            for p in self._adj[sekarang]:
                if p.ke not in sudah:
                    sudah.add(p.ke)
                    antrian.append(p.ke)
        return dikunjungi

    def dfs(self, mulai, _sudah=None):
        """Depth-First Search — telusuri sedalam mungkin (rekursif)."""
        mulai = mulai.upper()
        if not self._bandara_ada(mulai):
            return []
        if _sudah is None:
            _sudah = set()
        _sudah.add(mulai)
        hasil = [mulai]
        for p in self._adj[mulai]:
            if p.ke not in _sudah:
                hasil.extend(self.dfs(p.ke, _sudah))
        return hasil

    # ── DIJKSTRA ────────────────────────────────────────────

    def _dijkstra(self, dari, ke, mode="harga", kelas="ECO"):
        """
        Algoritma Dijkstra manual dengan multi-bobot.

        1. Inisialisasi semua jarak = ∞, asal = 0.
        2. Pilih vertex dengan jarak terkecil dari set 'belum'.
        3. Perbarui jarak tetangga jika ditemukan jalur lebih pendek.
        4. Rekonstruksi jalur dari dict 'sebelum'.

        Return: (path, total_bobot, detail_penerbangan)
        """
        dari, ke = dari.upper(), ke.upper()
        if not self._bandara_ada(dari) or not self._bandara_ada(ke):
            return None, 0, []

        INF      = float("inf")
        jarak    = {v: INF for v in self._bandara}
        sebelum  = {v: None for v in self._bandara}
        edge_via = {v: None for v in self._bandara}
        belum    = set(self._bandara.keys())
        jarak[dari] = 0

        while belum:
            sekarang = min(belum, key=lambda v: jarak[v])
            if jarak[sekarang] == INF or sekarang == ke:
                break
            belum.remove(sekarang)

            for p in self._adj[sekarang]:
                if p.ke not in belum:
                    continue
                if mode == "harga" and not p.kursi_tersedia(kelas):
                    continue
                bobot     = p.get_bobot(mode, kelas)
                jarak_alt = jarak[sekarang] + bobot
                if jarak_alt < jarak[p.ke]:
                    jarak[p.ke]    = jarak_alt
                    sebelum[p.ke]  = sekarang
                    edge_via[p.ke] = p

        if jarak[ke] == INF:
            return None, 0, []

        # Rekonstruksi jalur
        path, details, langkah = [], [], ke
        while langkah is not None:
            path.append(langkah)
            if edge_via[langkah]:
                details.append(edge_via[langkah])
            langkah = sebelum[langkah]
        path.reverse(); details.reverse()
        return path, round(jarak[ke], 2), details

    def cari_rute(self, dari, ke, mode="harga", kelas="ECO"):
        """Cari rute optimal. Return (path, total, details)."""
        if mode not in MODE_CARI:
            return None, 0, []
        return self._dijkstra(dari, ke, mode, kelas)

    def cari_semua_mode(self, dari, ke, kelas="ECO"):
        """Cari rute untuk ketiga mode sekaligus."""
        return {m: self.cari_rute(dari, ke, m, kelas) for m in MODE_CARI}

    # ── ANALITIK ────────────────────────────────────────────

    def hub_tersibuk(self, top=5):
        """Bandara dengan rute terbanyak (derajat keluar tertinggi)."""
        derajat = {iata: len(lst) for iata, lst in self._adj.items()}
        return sorted(derajat.items(), key=lambda x: x[1], reverse=True)[:top]

    def rute_terpanjang(self):
        semua = [p for lst in self._adj.values() for p in lst]
        return max(semua, key=lambda p: p.jarak_km) if semua else None

    def rute_terpendek_jarak(self):
        semua = [p for lst in self._adj.values() for p in lst]
        return min(semua, key=lambda p: p.jarak_km) if semua else None

    def ringkasan(self):
        semua_rute = self.get_semua_rute()
        return {
            "total_bandara":  len(self._bandara),
            "total_rute":     len(semua_rute),
            "total_maskapai": len({r["maskapai"] for r in semua_rute}),
            "total_negara":   len({b.negara for b in self._bandara.values()}),
        }

    @property
    def adjacency_list(self):
        """Adjacency list dalam format dict yang mudah dibaca."""
        return {
            iata: {
                p.ke: {"kode": p.kode_penerbangan, "maskapai": p.maskapai,
                       "jarak_km": p.jarak_km, "durasi": p.durasi_format()}
                for p in lst
            }
            for iata, lst in self._adj.items()
        }

    # ── EKSPOR & IMPOR JSON ─────────────────────────────────

    def ekspor_json(self):
        return {"bandara": self.get_semua_bandara_detail(),
                "rute":    self.get_semua_rute()}

    @classmethod
    def impor_json(cls, data):
        g = cls()
        for b in data.get("bandara", []):
            g.tambah_bandara(b["iata"], b["nama"], b["kota"], b["negara"],
                             b.get("zona_waktu","UTC+7"),
                             b.get("terminal",1), b.get("tipe","spoke"))
        for r in data.get("rute", []):
            g.tambah_rute(r["dari"], r["ke"], r["kode_penerbangan"],
                          r["maskapai"], r["pesawat"], r["jarak_km"],
                          r["durasi_mnt"], r["jadwal"],
                          r["hari_operasi"], r["kursi"])
        return g


# ============================================================
# DATA PRESET — Jaringan Penerbangan Asia Tenggara
# ============================================================

def buat_graf_asean():
    """Buat GrafBandara dengan data preset bandara & rute ASEAN."""
    g = GrafBandara()

    # ── BANDARA ─────────────────────────────────────────────
    bandara_data = [
        # IATA, Nama,                             Kota,     Negara,    UTC,    Term, Tipe
        ("CGK","Soekarno-Hatta International",    "Jakarta","Indonesia","UTC+7",3,"hub"),
        ("SUB","Juanda International",            "Surabaya","Indonesia","UTC+7",2,"hub"),
        ("DPS","Ngurah Rai International",        "Denpasar","Indonesia","UTC+8",2,"hub"),
        ("SIN","Changi Airport",                  "Singapura","Singapura","UTC+8",4,"hub"),
        ("KUL","Kuala Lumpur International",      "Kuala Lumpur","Malaysia","UTC+8",2,"hub"),
        ("BKK","Suvarnabhumi Airport",            "Bangkok","Thailand","UTC+7",1,"hub"),
        ("MNL","Ninoy Aquino International",      "Manila","Filipina","UTC+8",4,"hub"),
        ("SGN","Tan Son Nhat International",      "Ho Chi Minh","Vietnam","UTC+7",2,"hub"),
        ("HAN","Noi Bai International",           "Hanoi","Vietnam","UTC+7",2,"spoke"),
        ("RGN","Yangon International",            "Yangon","Myanmar","UTC+6.5",1,"spoke"),
    ]
    for row in bandara_data:
        g.tambah_bandara(*row)

    # ── HELPER KURSI ─────────────────────────────────────────
    def kursi_full(eco_h, bis_h, fir_h=None, eco_k=150, bis_k=24, fir_k=8):
        k = {
            "ECO": {"kapasitas": eco_k, "tersedia": eco_k-16, "harga": eco_h},
            "BIS": {"kapasitas": bis_k, "tersedia": bis_k-4,  "harga": bis_h},
        }
        if fir_h:
            k["FIR"] = {"kapasitas": fir_k, "tersedia": fir_k-1, "harga": fir_h}
        return k

    def kursi_budget(eco_h, bis_h, eco_k=180, bis_k=12):
        return {
            "ECO": {"kapasitas": eco_k, "tersedia": eco_k-20, "harga": eco_h},
            "BIS": {"kapasitas": bis_k, "tersedia": bis_k-2,  "harga": bis_h},
        }

    # ── RUTE PENERBANGAN ─────────────────────────────────────
    rute_data = [
        # CGK (Jakarta)
        ("CGK","SIN","GA830","Garuda Indonesia","Boeing 737-800",
         1410,125,["06:00","10:30","15:00","19:45"],["Setiap Hari"],
         kursi_full(1_350_000, 4_200_000, 12_500_000)),
        ("CGK","KUL","AK391","AirAsia","Airbus A320neo",
         1160,115,["06:30","11:00","16:30","22:00"],["Setiap Hari"],
         kursi_budget(700_000, 2_500_000)),
        ("CGK","BKK","GA866","Garuda Indonesia","Airbus A330-300",
         2250,210,["08:30","22:00"],["Setiap Hari"],
         kursi_full(2_100_000, 6_500_000, 18_000_000)),
        ("CGK","SUB","GA306","Garuda Indonesia","Boeing 737-800",
         664,70,["06:00","10:00","14:00","18:00"],["Setiap Hari"],
         kursi_budget(450_000, 1_500_000)),
        ("CGK","DPS","GA406","Garuda Indonesia","Boeing 737-800",
         950,95,["06:00","09:00","12:00","15:00","18:00"],["Setiap Hari"],
         kursi_budget(650_000, 2_100_000)),
        ("CGK","MNL","GA880","Garuda Indonesia","Airbus A330-300",
         2790,240,["09:00","21:00"],["Setiap Hari"],
         kursi_full(2_800_000, 8_500_000, 22_000_000)),
        # SIN (Singapura)
        ("SIN","CGK","GA831","Garuda Indonesia","Boeing 737-800",
         1410,130,["09:30","14:00","18:30"],["Setiap Hari"],
         kursi_full(1_450_000, 4_500_000, 13_000_000)),
        ("SIN","KUL","SQ118","Singapore Airlines","Airbus A320",
         350,50,["06:00","09:00","12:00","15:00","18:00","21:00"],["Setiap Hari"],
         kursi_full(900_000, 3_200_000)),
        ("SIN","BKK","SQ708","Singapore Airlines","Airbus A330-300",
         1430,145,["07:00","12:00","18:00"],["Setiap Hari"],
         kursi_full(1_600_000, 5_200_000, 16_000_000)),
        ("SIN","SGN","SQ186","Singapore Airlines","Airbus A320",
         1170,115,["07:30","11:30","15:30","20:00"],["Setiap Hari"],
         kursi_full(1_200_000, 4_000_000)),
        # KUL (Kuala Lumpur)
        ("KUL","CGK","MH714","Malaysia Airlines","Boeing 737-800",
         1160,120,["08:30","14:30","21:00"],["Setiap Hari"],
         kursi_full(1_200_000, 4_000_000, 11_500_000)),
        ("KUL","SIN","AK701","AirAsia","Airbus A320",
         350,55,["05:30","09:30","13:30","17:30","21:30"],["Setiap Hari"],
         kursi_budget(550_000, 1_800_000)),
        ("KUL","BKK","AK880","AirAsia","Airbus A320neo",
         1550,155,["06:30","11:00","16:00","21:00"],["Setiap Hari"],
         kursi_budget(900_000, 2_800_000)),
        ("KUL","RGN","MH740","Malaysia Airlines","Boeing 737-800",
         2050,185,["09:00","22:30"],["Setiap Hari"],
         kursi_full(1_800_000, 5_500_000)),
        # BKK (Bangkok)
        ("BKK","SIN","TG401","Thai Airways","Airbus A330-300",
         1430,150,["08:00","14:00","20:30"],["Setiap Hari"],
         kursi_full(1_700_000, 5_500_000, 17_000_000)),
        ("BKK","HAN","TG560","Thai Airways","Airbus A320",
         1290,130,["09:30","16:00"],["Setiap Hari"],
         kursi_full(1_300_000, 4_200_000)),
        # DPS (Bali)
        ("DPS","CGK","JT804","Lion Air","Boeing 737-800",
         950,95,["06:00","10:00","14:00","18:00"],["Setiap Hari"],
         kursi_budget(550_000, 1_700_000)),
        ("DPS","SIN","GA348","Garuda Indonesia","Boeing 737-800",
         1940,180,["08:30","18:00"],["Setiap Hari"],
         kursi_full(1_800_000, 5_500_000)),
        # SUB (Surabaya)
        ("SUB","CGK","GA307","Garuda Indonesia","Boeing 737-800",
         664,70,["05:30","09:30","13:30","17:30"],["Setiap Hari"],
         kursi_budget(450_000, 1_500_000)),
        # MNL (Manila)
        ("MNL","SIN","PR500","Philippine Airlines","Airbus A320",
         2390,215,["07:30","13:00","20:00"],["Setiap Hari"],
         kursi_full(2_300_000, 7_200_000)),
        # SGN (Ho Chi Minh)
        ("SGN","SIN","VN601","Vietnam Airlines","Airbus A320",
         1170,120,["07:00","11:00","15:00","20:00"],["Setiap Hari"],
         kursi_full(1_300_000, 4_200_000)),
        ("SGN","HAN","VN215","Vietnam Airlines","Airbus A320",
         1140,115,["06:00","10:00","14:00","18:00"],["Setiap Hari"],
         kursi_budget(500_000, 1_600_000)),
        ("SGN","BKK","VN602","Vietnam Airlines","Airbus A320",
         1000,100,["09:00","16:00"],["Setiap Hari"],
         kursi_full(1_100_000, 3_500_000)),
        # HAN (Hanoi)
        ("HAN","SIN","VN631","Vietnam Airlines","Airbus A320",
         1680,160,["08:00","14:30","21:00"],["Setiap Hari"],
         kursi_full(1_600_000, 5_000_000)),
    ]
    for row in rute_data:
        g.tambah_rute(*row)

    return g
