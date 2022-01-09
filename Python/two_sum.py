"""
Problem: Given an array and a target, find 2 numbers that sum to the target.
Assumption: Exactly one solution. Cannot use same indice.

Naive approach: Using 2 for loops - O(n^2)
Hashmap approach: Using hash map - O(n)
"""

from GS_timing import micros, millis
import numpy
from matplotlib import pyplot


def naive_app(arr, tgt):
    for i in range(len(arr)):
        for j in range(len(arr)):
            if arr[i] + arr[j] == tgt:
                return (i, j)
    raise Exception("Not Found")


def hashmap_app(arr, tgt):
    # {arr[i]: i}
    hashmap = {}
    for i in range(len(arr)):
        # if tgt - arr[i] == a key in hashmap, it means the key + arr[i] = tgt
        complement = tgt - arr[i]
        if complement in hashmap:
            return (i, hashmap[complement])
        else:
            hashmap[arr[i]] = i
    raise Exception("Not Found")


def main():
    func = [naive_app, hashmap_app]
    n = 1000000
    arr = [2, 7, 11, 15]
    tgt = 9

    for i in range(len(func)):
        t1 = millis()
        for j in range(n):
            func[i](arr, tgt)
        t2 = millis()
        y = t2-t1
        print(f"{func[i].__name__} : {t2-t1}")


if __name__ == "__main__":
    main()
