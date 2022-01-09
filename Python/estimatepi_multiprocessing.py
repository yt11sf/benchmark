# Reference: youtu.be/pvimAM_SLic
# Given a random function that randomly generate number between 0 and 1 uniformly
# Estimate the value of pi

# Purpose: Using multiprocessing to improve performance so that estimation can be more precise
# Reference: docs.python.org/3/library/multiprocessing.html

# Results:
"""
    Multiprocessing is significantly faster for CPU-bound process
    Time:
        For 500 million calls, (in seconds)        
        16 processes - 
        14 processes - 
        12 processes - 
        10 processes - 
        08 processes - 
        06 processes - 
        04 processes - 
        02 processes - 

    Accuracy (pi = 3.14159265358979323846):
        1000 dots       : 3.25600000000000000533        96.3583% accurate
        10000 dots      : 3.11640000000000010338        99.1981% accurate
        100000 dots     : 3.14519999999999995133        99.8852% accurate
        1000000 dots    : 3.14300399999999999778        99.9551% accurate
        10000000 dots   : 3.14283439999999996139        99.9605% accurate
        100000000 dots  : 3.14175516000000003558        99.9948% accurate
        1000000000 dots : 3.14154392000000002305        99.9984% accurate 

        1000 dots       : 3.12000000000000001776        99.3127% accurate
        10000 dots      : 3.13680000000000009305        99.8474% accurate
        100000 dots     : 3.14232000000000007753        99.9768% accurate
        1000000 dots    : 3.14305200000000013613        99.9535% accurate
        10000000 dots   : 3.14164320000000006537        99.9984% accurate
        100000000 dots  : 3.14140596000000013844        99.9941% accurate
        1000000000 dots : 3.14159404400000011688        100.0000% accurate

        1000 dots       : 3.04000000000000003553        96.766205% accurate
        10000 dots      : 3.12160000000000008781        99.363614% accurate
        100000 dots     : 3.13844000000000016359        99.899648% accurate
        1000000 dots    : 3.14128800000000004309        99.990303% accurate
        10000000 dots   : 3.14202880000000006078        99.986117% accurate
        100000000 dots  : 3.14185024000000017404        99.991801% accurate
        1000000000 dots : 3.14157413200000010661        99.999410% accurate

        1000 dots       : 3.14799999999999999822        99.796048% accurate
        10000 dots      : 3.11040000000000012233        99.007107% accurate
        100000 dots     : 3.13932000000000011995        99.927659% accurate
        1000000 dots    : 3.14144800000000015071        99.995396% accurate
        10000000 dots   : 3.14171680000000008102        99.996048% accurate
        100000000 dots  : 3.14151040000000008055        99.997382% accurate
        1000000000 dots : 3.14155979200000010924        99.998954% accurate
        10000000000 dots: 3.14157769360000008384        99.999524% accurate
"""

from multiprocessing import Process, Pipe, Lock
import random
from GS_timing import millis
from decimal import Decimal


def estimate_pi(n, conn, lock):
    """
    This function estimate pi by calculating the ratio between 
    the number of dots in circle and the number of dots in square.    
    @param n: number of dots for estimating pi
    @param conn: pipe connection to mainthread
    @param lock: multiprocessing lock
    """
    num_point_circle = 0
    num_point_square = 0
    for _ in range(n):
        # x and y do not need to be precise as we only need
        # to determine whether d is smaller than 1
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        # find the distance between the point and the center
        # ignore sqrt because sqrt(< 1) <= 1 and vise versa
        d = x ** 2 + y ** 2
        if d <= 1:
            num_point_circle += 1
        num_point_square += 1
    # precision of float in Python is 8 digits (24 bits)
    pi = Decimal(4 * num_point_circle / num_point_square)
    with lock:
        conn.send(pi)
    # conn.close()


def estimate_pi_sync(nprocess, n):
    """
    This function distribute the workload n to nprocess number of 
    processes to estimate pi synchronizingly
    @param nprocess: number of process
    @param n: number of dots for estimating pi
    return: estimated pi
    """
    processes = list()
    parent_conn, child_conn = Pipe()
    lock = Lock()
    avg_n = int(n / nprocess)
    rem_n = n % nprocess
    total = Decimal(0)

    try:
        # starting processes
        for _ in range(nprocess - 1):
            p = Process(target=estimate_pi, args=(avg_n, child_conn, lock))
            processes.append(p)
            p.start()
        p = Process(target=estimate_pi, args=(avg_n + rem_n, child_conn, lock))
        processes.append(p)
        p.start()

        # getting result from processes
        for _ in processes:
            total += Decimal(parent_conn.recv())
            # p.join()
        parent_conn.close()
        child_conn.close()
    except Exception as error:
        print("Error: estimate_pi_sync()")
        print(error)
    return Decimal(total / nprocess)


def get_time():
    """
    This function benchmark the time usage for estimating pi
    """
    n = int(input("Enter number of dots\t: "))
    nprocess = input("Enter number of process\t: ")
    start_time = millis()
    pi = estimate_pi_sync(int(nprocess), n)
    end_time = millis() - start_time
    print("****** Result ******")
    print("Estimated pi\t: {0:.20f}".format(pi))
    print("Consumed time\t: {0:.20f} seconds".format(end_time/1000))


def get_accuracy():
    """
    This function benchmark the accuracy of estimating pi    
    """
    pi = Decimal(3.14159265358979323846)
    prev = (0, 0)  # (n, est_pi) of previous loop
    n = int(input("Enter starting number of dots\t: "))
    steps = int(input("Enter number of steps\t\t: "))
    nprocess = int(input("Enter number of process\t\t: "))

    print("********** Result **********")
    for _ in range(steps):
        # skip aquired result from previous loop
        if prev[0] > 0:
            # previous test is always 10% of current test
            est_pi = estimate_pi_sync(
                nprocess, n-prev[0]) * Decimal(.9) + prev[1] * Decimal(.1)
        else:
            est_pi = estimate_pi_sync(nprocess, n)

        print("{0} dots\t: {1:.20f}\t{2:3.6f}% accurate".format(
            n, est_pi, 100 - abs(pi - est_pi)/pi * 100))

        # prepare for next loop
        prev = (n, est_pi)
        n *= 10


# the main process
def main():
    opt = input(
        "Enter 1 for benchmarking time\nEnter 2 for benchmarking result\nOption\t: ")
    if opt == "1":
        get_time()
    elif opt == "2":
        get_accuracy()
    else:
        print("Selected option is not available")


if __name__ == "__main__":
    main()
