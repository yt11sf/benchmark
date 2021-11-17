# Reference: youtu.be/pvimAM_SLic
# Given a random function that randomly generate number between 0 and 1 uniformly
# Estimate the value of pi

# Purpose: Multi-threading to improve performance so that estimation can be more precise
# Reference: realpython.com/intro-to-python-threading/

# Result:
"""
Threading in Python might degrade performance for CPU-bound process due to GIL problem
However, IO-bound processess can be improved.
Instead, look at multiprocessing -- process-based parrallellism
"""
# Reference: stackoverflow.com/questions/10789042/python-multi-threading-slower-than-serial

import random
import threading
import time

pi = 0
lock = threading.Lock()

# Given n times to estimate the value of pi
def estimate_pi(n):
    num_point_circle = 0
    num_point_square = 0
    for _ in range(n):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        # find the distance between the point and the center
        # ignore sqrt because sqrt(< 1) = < 1 and vise versa
        d = x ** 2 + y ** 2
        if d <= 1:
            num_point_circle += 1
        num_point_square += 1
    temp = 4 * num_point_circle / num_point_square
    with lock:
        global pi
        pi = (pi + temp) / 2 if pi > 0 else temp


# Create n threads to divide the task
def estimate_pi_sync(no_of_thread, n):
    threads = list()
    total = 0
    avg_n = int(n / no_of_thread)
    rem_n = int(n % no_of_thread)
    try:
        for i in range(no_of_thread):
            if i == 0:
                x = threading.Thread(target=estimate_pi, args=(avg_n + rem_n))
            else:
                x = threading.Thread(target=estimate_pi, args=(avg_n,))
            print(x)
            threads.append(x)
            x.start()
        # Alternate option to create thread
        """        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            executor.map(thread_function, range(3))
        """
    except:
        print("Error: unable to start thread")
    try:
        for index, thread in enumerate(threads):
            print(thread)
            thread.join()
    except:
        print("Error: unable to join thread")
    print(pi)

# the main thread
if __name__ == "__main__":
    n = input("Enter n: ")
    nthread = input("Enter number of thread: ")
    start_time = time.time()
    estimate_pi_sync(int(nthread), int(n))
    print("--- %s seconds ---" % (time.time() - start_time))
