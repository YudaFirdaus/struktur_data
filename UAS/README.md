SkyGraf – Jaringan Penerbangan Asia Tenggara
Deskripsi Program
SkyGraf adalah aplikasi berbasis Streamlit yang digunakan untuk memodelkan dan memvisualisasikan jaringan penerbangan di kawasan Asia Tenggara menggunakan konsep Graf Berarah Berbobot (Weighted Directed Graph).
Program memungkinkan pengguna untuk:
Melihat peta jaringan penerbangan.
Menambahkan dan menghapus bandara.
Menambahkan dan menghapus rute penerbangan.
Mencari rute penerbangan optimal.
Membandingkan rute berdasarkan harga, durasi, dan jarak.
Menyimpan dan memuat data dalam format JSON.
Menampilkan statistik jaringan penerbangan.

---

Teknologi yang Digunakan
Python 3.x
Streamlit
NetworkX
Matplotlib
NumPy
JSON

---

Cara Menjalankan Program

1. Install Dependency

```bash
pip install streamlit networkx matplotlib numpy
```

atau

```bash
pip install -r requirements.txt
```

2. Jalankan Program

```bash
streamlit run app.py
```

---

Struktur Folder

```text
SkyGraf/
│
├── app.py
├── graf.py
├── data_skygraf.json
├── README.md
└── requirements.txt
```

---

Struktur Data yang Digunakan

1. Graf Berarah Berbobot (Weighted Directed Graph)
   Vertex (Node) merepresentasikan bandara.
   Edge merepresentasikan rute penerbangan.
   Graf bersifat berarah karena rute A→B berbeda dengan B→A.
2. Adjacency List
   Graf disimpan menggunakan struktur adjacency list:

```python
{
    "CGK": [Penerbangan(CGK→SIN), Penerbangan(CGK→KUL)],
    "SIN": [Penerbangan(SIN→BKK)]
}
```

Keuntungan:
Hemat memori.
Cocok untuk graf yang tidak terlalu padat.
Memudahkan traversal dan pencarian rute. 3. Dictionary (Hash Map)
Digunakan untuk menyimpan data bandara berdasarkan kode IATA sehingga pencarian dapat dilakukan dengan cepat. 4. List
Digunakan untuk:
Menyimpan daftar rute.
Menyimpan jadwal penerbangan.
Menyimpan hasil BFS dan DFS.
Menyimpan jalur hasil Dijkstra.

---

Algoritma yang Digunakan
Breadth First Search (BFS)
Digunakan untuk menelusuri seluruh bandara yang terhubung dan mengecek keterhubungan antar bandara.
Kompleksitas: O(V + E)
Depth First Search (DFS)
Digunakan untuk menjelajahi graf secara mendalam.
Kompleksitas: O(V + E)
Dijkstra Algorithm
Digunakan untuk mencari rute optimal berdasarkan:
Harga termurah
Durasi tercepat
Jarak terpendek
Kompleksitas: O(V²)

---

Fitur Program
Manajemen Bandara
Tambah bandara
Hapus bandara
Menampilkan detail bandara
Manajemen Rute
Tambah rute
Hapus rute
Menampilkan jadwal penerbangan
Pencarian Rute
Harga termurah
Durasi tercepat
Jarak terpendek
Visualisasi Graf
Menampilkan jaringan penerbangan
Menyorot rute hasil pencarian
Penyimpanan Data
Impor JSON
Ekspor JSON

---

Kompleksitas Operasi
Operasi Kompleksitas
Tambah Bandara O(1)
Cari Bandara O(1)
Tambah Rute O(1)
Hapus Rute O(E)
BFS O(V+E)
DFS O(V+E)
Dijkstra O(V²)
Keterangan:
V = jumlah bandara
E = jumlah rute

---

Riwayat Commit
Inisialisasi proyek SkyGraf
Menambahkan class Bandara dan Penerbangan
Implementasi GrafBandara dengan Adjacency List
Implementasi BFS dan DFS
Implementasi algoritma Dijkstra
Menambahkan data preset bandara ASEAN
Menambahkan visualisasi graf
Menambahkan antarmuka Streamlit
Menambahkan fitur pencarian rute optimal
Menambahkan fitur ekspor dan impor JSON
Perbaikan tampilan dan bug fixing
Menambahkan dokumentasi README
