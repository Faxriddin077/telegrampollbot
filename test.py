def search(array, data):
    left, step = 0, 0
    right = len(array)
    while left <= right:
        center = round((left + right)/2)
        if array[center] % data == 0:
            return [center, step]
        elif array[center] < data:
            left = center + 1
            step += 1
        elif array[center] > data:
            right = center - 1
            step += 1
    return [-1, 0]

print("Massiv qiymatlarini bir qatorda probel bilan kiriting: ")
a = list(map(int, input().split()))
print("Massivdan karrali qiymatini topmoqchi bo'lgan elementingizni kiriting: ")
x = int(input())
res = search(a, x)
if res[0] == -1:
    print("Qiymat massivda mavjud emas!")
else:
    print("Qiymat indeksi: {}, solishtirishlar soni: {}".format(res[0], res[1]))