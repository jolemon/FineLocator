from multiprocessing import Pool
from itertools import combinations
import time


def func_plus(x):
    return x[0] * x[1]


if __name__ == '__main__':
    thread_num = 4
    start1 = time.process_time()
    keys = list(range(10000))
    comb = combinations(keys, 2)
    p = Pool(thread_num)
    res = p.map(func_plus, list(comb))
    print(len(res))
    elapsed1 = round(time.process_time() - start1, 2)
    print('time: ', elapsed1)

    start2 = time.process_time()
    a = []
    comb = combinations(keys, 2)
    for c in comb:
        a.append(func_plus(c))
    elapsed2 = round(time.process_time() - start2, 2)
    print(len(a))
    print('time: ', elapsed2)
    # manager = Manager()
    # res_dic = manager.dict()

    # for _ in range(thread_num):
    #     p = Process(target = func_plus, kwargs = {'res_dic': res_dic, 'q': queue})
    #     procs.append(p)
    #     p.start()
    # for proc in procs:
    #     proc.join()
    # print(res_dic)

# import numpy as np
# trim_vec = '0.0 0.0 0.0'
# vec1 = np.fromstring(string = trim_vec, sep = ',')
# l1 = np.linalg.norm(vec1)

