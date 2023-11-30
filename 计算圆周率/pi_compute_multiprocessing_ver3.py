# C佬（我的 Python 师傅，大一）希望我写一个多进程版本的圆周率计算，主要考察多进程，于是我写了这个

# 程序输出
"""
计算 1000 项圆周率耗时: 0.0001406000228598714 秒，圆周率值: 3.140592653839794
计算 10000 项圆周率耗时: 0.001582800003234297 秒，圆周率值: 3.1414926535900345
计算 100000 项圆周率耗时: 0.01815829999395646 秒，圆周率值: 3.1415826535897198
程序运行时间：0.01815829999395646 秒
所有进程总耗时: 0.01988170002005063 秒
"""

import time
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()


def pi_compute(n: int) -> float:
    """
    计算圆周率，采用莱布尼茨公式的计算方法
    参考 https://blog.csdn.net/m0_62488776/article/details/131463332

    :param n: 计算项数
    :return: 圆周率的近似值
    """
    pi = 0.0
    for i in range(n):
        pi += (-1) ** i / (2 * i + 1)
    pi *= 4
    return str(pi)


def compute_and_log(n: int) -> tuple:
    start_time = time.perf_counter()
    pi_value = pi_compute(n)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time  # 单个进程的运行时间
    logger.info(f"计算 {n} 项圆周率耗时: {elapsed_time} 秒，圆周率值: {pi_value}")
    return n, pi_value, elapsed_time


def main():
    input_str = input("请输入精确到小数点后多少位，用空格分隔（例如 100 1000 10000）: ")
    precisions = [int(n) for n in input_str.split()]  # 预分析任务

    with ProcessPoolExecutor() as executor:  # 提交任务
        futures = [executor.submit(compute_and_log, n) for n in precisions]

        # BEGIN!
        sum_time = 0
        max_time = 0
        for future in as_completed(futures):  # 获取结果，as_completed()返回一个迭代器，按照完成顺序产出future
            n, pi_value, elapsed_time = future.result()  # 获取结果
            sum_time += elapsed_time
            if elapsed_time > max_time:  # 更新最长运行时间
                max_time = elapsed_time

    # END!
    logger.info(f"程序运行时间：{max_time} 秒")  # 获取运行时间最长的那个进程的运行时间，这个就是程序运行总时间（吗？）
    logger.info(f"所有进程总耗时: {sum_time} 秒")


if __name__ == "__main__":
    main()
