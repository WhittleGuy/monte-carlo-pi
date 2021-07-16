import time
import multiprocessing
import random


def makePoint(n):
    inside_circle = 0
    for _ in range(int(n)):
        x = random.random()  # faster than using random.uniform(0,1)
        y = random.random()
        if x**2 + y**2 < 1:  # sqrt not necessary here, per algebra
            inside_circle += 1
    return inside_circle


class WorkerProcess(multiprocessing.Process):

    def __init__(self, args):
        multiprocessing.Process.__init__(self, args=args)
        self.n = args[0]
        self.q = args[1]

    def run(self):
        self.q.put(makePoint(self.n))


def main():
    POINTS = 1000000000
    PROCESSES = 4

    if POINTS % PROCESSES != 0:
        print('[x] Points will be evenly distributed between processes.')
        print('[x] If there is a fractional number of points per process, ')
        print('[x] the number of points will be rounded to the nearest whole integer.')
        print('----------------------------------------------------')

    start = time.perf_counter()

    jobs = []
    q = multiprocessing.Queue()
    for _ in range(PROCESSES):
        process = WorkerProcess(args=(POINTS/PROCESSES, q))
        process.start()
        jobs.append(process)

    sum_in_circle = 0
    for _ in range(PROCESSES):
        sum_in_circle += q.get()

    end = time.perf_counter()

    print(f'[+] Estimation of pi is {4.0*sum_in_circle/POINTS}')
    print(f'[+] Completed in {round(end-start, 2)} second(s)')
    print(f'[+] {round((end-start)*(10**9)/POINTS, 2)}ns per point')


if __name__ == '__main__':
    main()
