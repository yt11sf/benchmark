# Purpose: Compare the performance of different methods for factorial
# * This file has the potential to be converted to measure every given function

"""
Comparing math, iterative, recursive: 
    'built-in factorial' imported from 'math' performed worst almost everytime it was first called in a program
    - I suspect that it was because of the import of 'math' library when it was first called

    'built-in factorial' then performed better most of the time
    'iterative' was second
    'recursive' was last

Comparing math, iterative, recursive, cache, lrucache: 
    'cache' is significantly fastest with a win rate of >85%
    'built-in' is second with a win rate of ~10%
    'lru cache' is slow with a win rate of ~2% to ~3%
    'iterative' is very slow with a win rate of <1% 
    'recursive' is a disaster with only 1 win observed across multiple test

Comparing cache, lrucache:
    'cache' ~94%
    'lru cache' ~5%
"""
from multiprocessing import Process, Pipe
import math
import GS_timing
import random
from functools import cache, lru_cache


def iterative_factorial(n):
    factorial = 1
    if int(n) > 1:
        for i in range(1, n + 1):
            factorial = factorial * i
    return factorial


def recursive_factorial(n):
    if n == 0:
        return n
    else:
        return n * recursive_factorial(n - 1)


@cache
def cached_fib(n):
    if n <= 1:
        return 1
    return cached_fib(n-1) + cached_fib(n-2)


@lru_cache(maxsize=3)
def lru_cached_fib(n):
    if n <= 1:
        return 1
    return lru_cached_fib(n-1) + lru_cached_fib(n-2)


def compare_order(n, conn, function_list):
    """
    This function count how many times a given function is the fastest.
    """
    recorded_time = {}
    counter = []

    # initializing counter
    for i in function_list:
        recorded_time[i] = []
        counter.append(0)

    for i in range(n):
        num = random.randrange(10, 100)
        min = ["temp", 1000]
        for j in function_list:
            a = num + i
            # measuring time
            start_time = GS_timing.micros()
            j(a)
            end_time = GS_timing.micros()
            recorded_time[j].append(end_time - start_time)
            if min[1] > recorded_time[j][i]:
                min[0] = j
                min[1] = recorded_time[j][i]
        # to check time consumed by each loop
        # print(min)
        counter[function_list.index(min[0])] += 1
    conn.send({"counter": counter})
    conn.close()


# Create n process to divide the task
def compare_order_thread(no_of_process, n, function_list):
    processes = list()
    parent_conn, child_conn = Pipe()
    avg_n = int(n / no_of_process)
    rem_n = int(n % no_of_process)
    out = {"function_list": function_list, "counter": []}
    try:
        for i in range(no_of_process):
            if i == 0:
                process = Process(target=compare_order, args=(
                    avg_n + rem_n, child_conn, function_list))
            else:
                process = Process(target=compare_order, args=(
                    avg_n, child_conn, function_list))
            # print(p)
            processes.append(process)
            process.start()
    except Exception as error:
        print(error)
    try:
        for _, process in enumerate(processes):
            recv = parent_conn.recv()
            if len(out["counter"]) == 0:
                for i in range(len(recv["counter"])):
                    out["counter"].append(0)

            for i in range(len(recv["counter"])):
                out["counter"][i] += recv["counter"][i]
            process.join()
            # print(process)
        parent_conn.close()
    except Exception as error:
        print(error)
    print("\n****The fastest methods are****")
    for i in range(len(out["function_list"])):
        print("{:60}: {:d}".format(
            str(out["function_list"][i]), out["counter"][i]))
    print("Total : ",  sum(out["counter"]))


# the main thread
if __name__ == "__main__":
    nprocess = input("Enter number of process: ")
    n = input("Enter n < process * 888: ")

    print("""
Index : Function
1     : math.factorial
2     : iterative_factorial
3     : recursive_factorial
4     : cached_fib
5     : lru_cached_fib""")
    f = input("Enter indexes of function such as 12345 : ")

    flist = []
    if "1" in f:
        flist.append(math.factorial)
    if "2" in f:
        flist.append(iterative_factorial)
    if "3" in f:
        flist.append(recursive_factorial)
    if "4" in f:
        flist.append(cached_fib)
    if "5" in f:
        flist.append(lru_cached_fib)

    compare_order_thread(int(nprocess), int(n), flist)

# print(recorded_time)
