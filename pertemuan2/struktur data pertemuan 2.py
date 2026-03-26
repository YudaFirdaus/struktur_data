#pertemuan 2, list

import sys
colors: list[str] = ["red"]
print(colors)
print(sys.getsizeof(colors))

#menambahkan elemen ke dalam list
colors.append("blue")
print(colors)
print(sys.getsizeof(colors))

colors.insert(0, "White")
print(colors)
print(sys.getsizeof(colors))

colors.append("green")
print(colors)
print(sys.getsizeof(colors))

colors.append("yellow")
print(colors)
print(sys.getsizeof(colors))

colors.append("purple")
print(colors)
print(sys.getsizeof(colors))

colors.append("pink")
print(colors)
print(sys.getsizeof(colors))

colors.append("black")
print(colors)
print(sys.getsizeof(colors))

colors.append("brown")
print(colors)
print(sys.getsizeof(colors))


#menghapus elemen dari list
colors.pop()
print(colors)
print(sys.getsizeof(colors))

colors.remove("red")
print(colors)
print(sys.getsizeof(colors))

colors.reverse
print(colors)
print(sys.getsizeof(colors))

numbers: list[int] = [3.60, 3.80, 3.60, 3.80, 3.60, 3.80, 3.60, 3.80]
print(sum(numbers)/len(numbers))
print(len(numbers))
print(sys.getsizeof(numbers))
print(numbers)

backup_numbers: list[float] = numbers.copy()
print(backup_numbers)
print(sys.getsizeof(backup_numbers))





