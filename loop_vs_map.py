from GS_timing import millis

a = '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15'

t1 = millis()
for _ in range(100000):
    list(map(int, a.split()))
t2 = millis()
print('list(map(int, a.split()))\t: ', t2-t1)

t1 = millis()
for _ in range(100000):
    [int(x) for x in a.split()]
t2 = millis()
print('[int(x) for x in s.split()]\t: ', t2-t1)
