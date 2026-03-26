# Membuat Struktur Data Dictionary
userLogin ={"name": "Budi", "age": 30, "Role": "Admin"}
print(type(userLogin))
# Mengakses Data
print(f"Nama Akun: {userLogin['name']}")
print(f"Umur Akun: {userLogin['age']} Tahun")
print(f"Role Akun: {userLogin['Role']}")

# Akses data seluruh
print(userLogin.items())
print(userLogin.keys())
print(userLogin.values())

# Menambah Data kedalam dictionary big-O O(1)
userLogin["email"] = "example@mail.com"
print(userLogin)

# Menghapus data
userLogin.pop("email")
print(userLogin)

# Mengubah data kedalam dictionary big-O O(1)
userLogin["Role"] = "User"
print(userLogin)

# Nested Dictionary
dbUser= {"user1": {"name":"Andi", "age":30, "Role":"Admin"}}, 
{"user2": {"name":"Budi", "age":25, "Role":"Admin"}}, 
{"user3": {"name":"Candra", "age":29, "Role":"Admin"}}
         
print(dbUser)
# Akses value base key
print(dbUser["user1"])

# Melakukan pencarian data di Dictionary
findWord = input("Masukkan kata yang ingin dicari: ")
if findWord in dbUser:
    print("Data ditemukan")
    print(dbUser[findWord])
else:
    print("Data tidak ditemukan")
