import hashlib
H = "d827f12e35eae370ba9c65b7f6026695"
for i in range(0, 5000):
    if hashlib.md5(str(i).encode()).hexdigest() == H:
        print("numero:", i)
        break
