# ✈️ SkyGraf — Jaringan Penerbangan Asia Tenggara

## Deskripsi Program

SkyGraf adalah aplikasi berbasis Streamlit yang memodelkan dan memvisualisasikan jaringan penerbangan di kawasan Asia Tenggara menggunakan konsep **Graf Berarah Berbobot (Weighted Directed Graph)**.

Program memungkinkan pengguna untuk:

- Melihat peta jaringan penerbangan
- Menambahkan dan menghapus bandara, rute, dan maskapai
- Mencari rute penerbangan optimal (harga, durasi, jarak)
- Membandingkan rute berdasarkan tiga mode sekaligus
- Menyimpan dan memuat data dalam format JSON
- Menampilkan statistik dan struktur data internal graf

---

## Teknologi yang Digunakan

| Library    | Fungsi                                    |
| ---------- | ----------------------------------------- |
| Python 3.x | Bahasa pemrograman utama                  |
| Streamlit  | Antarmuka web interaktif                  |
| NetworkX   | Visualisasi graf (bukan penyimpanan data) |
| Matplotlib | Render gambar peta                        |
| NumPy      | Kalkulasi layout peta                     |
| JSON       | Penyimpanan data permanen                 |

---

## Cara Clone Repository

### 1. Pastikan Git sudah terinstall

```bash
git --version
```

### 2. Clone Repository

```bash
git clone https://github.com/YudaFirdaus/struktur_data
```

### 3. Masuk ke Direktori Proyek

```bash
cd struktur_data
```

### 4. Install Dependency

```bash
pip install streamlit networkx matplotlib numpy
```

atau jika tersedia `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. Jalankan Program

```bash
streamlit run app.py
```

---

## Cara Berkontribusi (Contribute)

### Kontribusi via GitHub (Fork & Pull Request)

1. **Fork** repository ini ke akun GitHub kamu
2. **Clone** fork tersebut ke komputer lokal:
   ```bash
   git clone https://github.com/<username-kamu>/struktur_data
   ```
3. **Buat branch baru** untuk fitur atau perbaikan:
   ```bash
   git checkout -b fitur/nama-fitur
   ```
4. **Lakukan perubahan** pada kode
5. **Commit** perubahan dengan pesan yang jelas:
   ```bash
   git add .
   git commit -m "feat: menambahkan fitur nama-fitur"
   ```
6. **Push** branch ke fork kamu:
   ```bash
   git push origin fitur/nama-fitur
   ```
7. Buka **Pull Request** ke repository utama

### Panduan Pesan Commit

| Prefix      | Digunakan untuk                     |
| ----------- | ----------------------------------- |
| `feat:`     | Menambahkan fitur baru              |
| `fix:`      | Memperbaiki bug                     |
| `docs:`     | Perubahan dokumentasi               |
| `refactor:` | Refactor kode tanpa mengubah fungsi |
| `style:`    | Perubahan tampilan/formatting       |

### Kontribusi Tim Pengembang

Proyek ini dikerjakan oleh 3 anggota dengan pembagian sebagai berikut:

| Anggota               | Bagian graf.py                                        | Bagian app.py                                           |
| --------------------- | ----------------------------------------------------- | ------------------------------------------------------- |
| Abdi Malika Putra     | Class `Bandara`, Class `Penerbangan`                  | Tab Peta Rute, Tab Cari Penerbangan, Sidebar Lihat Peta |
| Fadrial Junyana Putra | `GrafBandara` — manajemen vertex & edge, BFS, DFS     | Tab Jadwal & Maskapai, Tab Data Bandara                 |
| Muhamad Yuda Firdaus  | `GrafBandara` — Dijkstra, Analitik, Ekspor/Impor JSON | Sidebar Tambah/Hapus data, fungsi `buat_graf_asean()`   |

---

## Struktur Folder

```text
SkyGraf/
│
├── app.py                  # Antarmuka Streamlit
├── graf.py                 # Struktur data & algoritma
├── data_skygraf.json       # Data tersimpan (dibuat otomatis)
├── requirements.txt        # Daftar dependency
└── README.md               # Dokumentasi ini
```

---

## Struktur Data yang Digunakan

### 1. Graf Berarah Berbobot (Weighted Directed Graph)

- **Vertex (Node)** — merepresentasikan bandara
- **Edge** — merepresentasikan rute penerbangan
- Bersifat **berarah** karena rute A→B berbeda dengan B→A (harga & jadwal bisa berbeda)
- Bersifat **berbobot** dengan **tiga nilai bobot** per edge: harga, durasi, jarak

### 2. Adjacency List

Graf disimpan menggunakan adjacency list manual (dict Python):

```python
_adj = {
    "CGK": [Penerbangan(CGK→SIN, GA830), Penerbangan(CGK→KUL, AK391)],
    "SIN": [Penerbangan(SIN→CGK, GA831), Penerbangan(SIN→BKK, SQ708)],
    ...
}
```

Keuntungan:

- Hemat memori — hanya menyimpan koneksi yang ada
- Cocok untuk graf sparse (tidak semua bandara terhubung langsung)
- Traversal dan pencarian rute lebih efisien

### 3. Dictionary (Hash Map)

Digunakan untuk menyimpan objek `Bandara` dengan kode IATA sebagai key:

```python
_bandara = {
    "CGK": Bandara("CGK", "Soekarno-Hatta", ...),
    "SIN": Bandara("SIN", "Changi Airport", ...),
}
```

Pencarian bandara: **O(1)**

### 4. List

Digunakan untuk:

- Menyimpan daftar `Penerbangan` per bandara di `_adj`
- Menyimpan jadwal keberangkatan per rute
- Menyimpan hasil BFS, DFS, dan jalur Dijkstra

---

## Algoritma yang Digunakan

### Breadth-First Search (BFS)

Menelusuri graf lapis per lapis — cocok untuk mengecek keterhubungan antar bandara.

```
Kompleksitas: O(V + E)
Implementasi: Iteratif menggunakan list sebagai antrian (FIFO)
```

### Depth-First Search (DFS)

Menelusuri graf sedalam mungkin sebelum kembali — cocok untuk eksplorasi semua jalur.

```
Kompleksitas: O(V + E)
Implementasi: Rekursif
```

### Dijkstra Algorithm

Mencari rute optimal dengan tiga mode bobot yang bisa dipilih:

| Mode            | Bobot yang Digunakan    |
| --------------- | ----------------------- |
| Harga Termurah  | `kursi[kelas]["harga"]` |
| Durasi Tercepat | `durasi_mnt`            |
| Jarak Terpendek | `jarak_km`              |

```
Kompleksitas: O(V²)
Implementasi: Manual menggunakan min() pada set belum dikunjungi
```

---

## Fitur Program

### Manajemen Data (Sidebar)

- Tambah / hapus bandara
- Tambah / hapus rute penerbangan
- Tambah maskapai baru ke daftar

### Pencarian Rute (Tab Cari Penerbangan)

- Pilih bandara asal & tujuan
- Pilih mode: harga / durasi / jarak
- Pilih kelas kursi: Ekonomi / Bisnis / First Class
- Bandingkan ketiga mode sekaligus

### Visualisasi (Tab Peta Rute)

- Peta jaringan penerbangan berwarna per negara
- Sorot rute hasil pencarian Dijkstra
- Info hub tersibuk, rute terpanjang & terpendek

### Jadwal (Tab Jadwal & Maskapai)

- Filter penerbangan per hari operasi
- Filter rute per maskapai

### Data & Debug (Tab Data Bandara)

- BFS & DFS interaktif
- Adjacency list yang bisa dilihat langsung

### Penyimpanan Data

- Ekspor ke file JSON
- Impor dari file JSON
- Auto-load saat aplikasi dijalankan

---

## Kompleksitas Operasi

| Operasi        | Kompleksitas | Keterangan                       |
| -------------- | ------------ | -------------------------------- |
| Tambah Bandara | O(1)         | Insert ke dict                   |
| Cari Bandara   | O(1)         | Lookup dict by key               |
| Tambah Rute    | O(1)         | Append ke list                   |
| Hapus Rute     | O(E)         | Filter list                      |
| Hapus Bandara  | O(V + E)     | Hapus + bersihkan semua edge     |
| BFS            | O(V + E)     | Traversal semua node & edge      |
| DFS            | O(V + E)     | Traversal semua node & edge      |
| Dijkstra       | O(V²)        | min() pada set di setiap iterasi |

_V = jumlah bandara, E = jumlah rute_

---

## Riwayat Commit

1. `feat:` Inisialisasi proyek SkyGraf
2. `feat:` Menambahkan class Bandara dan Penerbangan
3. `feat:` Implementasi GrafBandara dengan Adjacency List
4. `feat:` Implementasi BFS dan DFS
5. `feat:` Implementasi algoritma Dijkstra multi-bobot
6. `feat:` Menambahkan data preset bandara ASEAN
7. `feat:` Menambahkan visualisasi graf dengan Matplotlib
8. `feat:` Menambahkan antarmuka Streamlit
9. `feat:` Menambahkan fitur pencarian rute optimal
10. `feat:` Menambahkan fitur ekspor dan impor JSON
11. `feat:` Menambahkan fitur manajemen maskapai
12. `fix:` Perbaikan tampilan dan bug fixing
13. `docs:` Menambahkan dokumentasi README lengkap
