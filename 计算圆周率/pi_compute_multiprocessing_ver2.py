# C佬（我的 Python 师傅，大一）希望我写一个多进程版本的圆周率计算器，主要考察多进程，于是我写了这个

import time
import logging
from multiprocessing import Pool, Manager

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


def compute_and_log(n: int, result_list: list) -> None:
    """
    计算圆周率并记录时间
    :param n: 计算到小数点后多少位
    :param result_list: 保存结果的列表
    """
    start_time = time.time()
    pi_value = pi_compute(n)
    end_time = time.time()
    elapsed_time = end_time - start_time
    result_list.append((n, pi_value, elapsed_time))


def main():
    # 从用户输入获取不同的精度
    input_str = input("请输入精确到小数点后多少位，用空格分隔（例如 100 1000 10000）: ")
    precisions = [int(n) for n in input_str.split()]

    start_time_main = time.time()

    with Manager() as manager:
        result_list = manager.list()  # 创建一个可在多个进程间共享的列表
        with Pool() as pool:
            for n in precisions:
                pool.apply_async(compute_and_log, (n, result_list))
            pool.close()
            pool.join()

        end_time_main = time.time()

        # 所有进程完成后，统一输出结果
        total_time = sum(result[2] for result in result_list)
        logger.info(f"所有进程总耗时: {total_time} 秒")
        logger.info(f"程序运行时间：{end_time_main - start_time_main} 秒")
        for result in result_list:
            n, pi_value, elapsed_time = result
            logger.info(f"计算 {n} 项圆周率耗时: {elapsed_time} 秒，圆周率值: {str(pi_value)[:n + 2]}")


if __name__ == "__main__":
    main()
