"""
Taken from [How to remove element from list without using for loop?](https://stackoverflow.com/q/70431650/7099900)
This benchmark is only valid for big list
Result:
remove_fun:     3877.39ms   3830.48ms   3984.32ms
unique_set:     539.52ms    480.89ms    537.63ms
duplicate_set:  487.33ms    530.28ms    476.56ms
different_set:  546.42ms    481.58ms    499.23ms
"""
from GS_timing import millis
import copy


def remove_fun(org_A, org_B):
    # This is somehow the fastest for small list
    A = copy.deepcopy(org_A)
    B = copy.deepcopy(org_B)
    for pair in B:
        if pair in A:
            A.remove(pair)
        elif (pair[1], pair[0]) in A:
            A.remove((pair[1], pair[0]))


def unique_set(org_A, org_B):
    A = copy.deepcopy(org_A)
    B = copy.deepcopy(org_B)
    set_B = set(B).union([(j, i) for (i, j) in B])
    C = list(set(A) - set_B)


def duplicate_set(org_A, org_B):
    A = copy.deepcopy(org_A)
    B = copy.deepcopy(org_B)
    set_B = set(B).union([(j, i) for (i, j) in B])
    C = [tpl for tpl in A if tpl in set_B]


def different_set(org_A, org_B):
    A = copy.deepcopy(org_A)
    B = copy.deepcopy(org_B)
    C = set(A) - set(B + [(y, x)for x, y in B])


def main():
    n = 100
    A = [(i, i*2) for i in range(1000)]
    B = [(i, i*3) for i in range(1000)]
    fList = [remove_fun, unique_set, duplicate_set, different_set]
    for func in fList:
        t1 = millis()
        for _ in range(n):
            func(A, B)
        t2 = millis()
        print(f"{func.__name__}: {t2-t1:.2f}ms")


if __name__ == "__main__":
    main()
