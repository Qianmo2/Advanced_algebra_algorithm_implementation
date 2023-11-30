# 这是 C佬 自己的代码

import multiprocessing
import time
import random


def calculate_pi(num, _dict, key):
    start = time.time()
    inside_circle = 0

    for _ in range(num):
        x, y = random.random(), random.random()
        distance = x**2 + y**2
        if distance <= 1:
            inside_circle += 1

    pi_estimate = 4 * inside_circle / num
    end_time = time.time()
    _dict[key] = (pi_estimate, end_time - start)


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    samples = [int(1e7), int(2e7), int(3e7)]
    processes = []

    start_time = time.time()

    for i, num_samples in enumerate(samples):
        p = multiprocessing.Process(target=calculate_pi, args=(num_samples, return_dict, i))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    total_time = time.time() - start_time

    # 输出结果
    for i, result in return_dict.items():
        pi_str = str(result[0])
        print(f"进程 {i}: 计算的pi前10位: {pi_str[:10]}, 使用时间: {result[1]}秒")
    print(f"总耗时: {total_time}秒")
