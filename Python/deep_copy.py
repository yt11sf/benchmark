"""
Benchmark different method of copying a list and their effect
1. b = list(a)          : second layer is affected      : 17.424100000411272
2. b = a                : first layer is affected       : 6.462500000372529 
3. b = a[:]             : second layer is affected      : 13.862999999895692
4. b = copy.copy(a)     : second layer is affected      : 33.75569999963045
5. b = copy.deepcopy(a) : actual recursive deep copy    : 788.1727999998257
"""
import copy
from GS_timing import millis

funcList = ["list(a)", "a", "a[:]",
            "copy.copy(a)", "copy.deepcopy(a)"]
for f in funcList:
    i = 100000
    a = [[1, 2, [4, 5]], 6, [8, 9]]
    b = []
    # Benchmark
    t1 = millis()
    for _ in range(i):
        b = eval(f)  # major slow down, but kept for cleanliness
    t2 = millis()
    print(f'b = {f}: {str(t2-t1)}')
    # Changing value
    print("first layer")
    b[2] = 7
    print(a)
    print(b)
    print("second layer")
    b[0][2] = 3
    print(a)
    print(b)
    print("******")
"""
    a = [[1, 2, [4, 5]], 6, [8, 9]]
    t1 = millis()
    for _ in range(i):
        b = a
    t2 = millis()
    print(f'b = a: {str(t2-t1)}')
    b[2] = 7  # first layer is affected
    print(a)
    print(b)
    b[0][2] = 3
    print(a)
    print(b)
    print("******")
    a = [[1, 2, [4, 5]], 6, [8, 9]]
    t1 = millis()
    for _ in range(i):
        b = a[:]
    t2 = millis()
    print(f'b = a[:]: {str(t2-t1)}')
    b[2] = 7  # first layer not affected
    print(a)
    print(b)
    b[0][2] = 3  # second layer is affected
    print(a)
    print(b)
    print("******")
    a = [[1, 2, [4, 5]], 6, [8, 9]]
    t1 = millis()
    for _ in range(i):
        b = copy.copy(a)
    t2 = millis()
    print(f'b = copy.copy(a): {str(t2-t1)}')
    b[2] = 7  # first layer not affected
    print(a)
    print(b)
    b[0][2] = 3  # second layer is affected
    print(a)
    print(b)
    print("******")
    a = [[1, 2, [4, 5]], 6, [8, 9]]
    t1 = millis()
    for _ in range(i):
        b = copy.deepcopy(a)
    t2 = millis()
    print(f'b = copy.deepcopy(a): {str(t2-t1)}')
    b[2] = 7  # actual deepcopy
    print(a)
    print(b)
    b[0][2] = 3
    print(a)
    print(b)
    print("******")
"""
