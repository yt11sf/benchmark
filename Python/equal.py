import time
a = []

for _ in range(3):
    t1 = time.time()
    for _ in range(1000000):
        if a == []:
            pass
    t2 = time.time()
    print(t2-t1)

    t1 = time.time()
    for _ in range(1000000):
        if len(a) == 0:
            pass
    t2 = time.time()
    print(t2-t1)
    print()
