# cara inisiasi set
# 1 (kurung kurawal)
import sys
tokenword = {"tidak","bisa"}
print(tokenword)
print(type(tokenword))
print("ukuran memory", sys.getsizeof(tokenword))

# 2 (set ())

kataSambung = set(["kemudian", "lalu", "setelah"])
print(kataSambung)
print(type(kataSambung))
print("ukuran memori", sys.getsizeof(kataSambung))

# pembuktian terkait tidak memiliki sistem indexing
# print(kataSambung[-1])

# menghaspus elemen pada set
kataSambung.remove("kemudian")
print(kataSambung)
tokenword.discard("tidak")
print(tokenword)

# menambahkan elemen pada set
tokenword.add("mungkin")
print(tokenword)
tokenword.update(["pasti", "mungkin"])
print(tokenword)

# mengubah elemen set
tokenword.remove("mungkin")
print(tokenword)
tokenword.add("nanti")
print(tokenword)

# operasi pada set
setA = {1,2,3,4}
setB = {3,4,5,6}

# union
print(setA|setB)
# intersection
print(setA&setB)
# difference
print(setA-setB)
# symmetric difference
print(setA^setB)

setUnion = setA.union(setB)
print(setUnion)

# struktur data hash
dataMahasiswa = {
    "Nama" : "Andi", "Budi"
    "NIM": "20240140014", "20240140015"
    "Jurusan": "Teknik Informatika", "Teknik Elektro"
}