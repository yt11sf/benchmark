import time

# loop operation without sleep
for _ in range(10):
    t1, cnt = time.time(), 0
    while True:
        cnt += 1
        if (time.time() - t1) > 1.:
            break
    print(cnt)

# loop operation with sleep
for _ in range(10):
    t1, cnt = time.time(), 0
    while True:
        cnt += 1
        if (time.time() - t1) > 1.:
            break
        time.sleep(.05)
    print(cnt)
