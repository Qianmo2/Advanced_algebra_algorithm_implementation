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
    elapsed_time = end_time - start_time
    return n, pi_value, elapsed_time


def main():
    input_str = input("请输入精确到小数点后多少位，用空格分隔（例如 100 1000 10000）: ")
    precisions = [int(n) for n in input_str.split()]  # 预提交任务

    start_time_main = time.perf_counter()  # 这里必须用perf_counter，time.time()似乎无法输出正确的时间

    with ProcessPoolExecutor() as executor:  # 提交任务
        futures = [executor.submit(compute_and_log, n) for n in precisions]

        # Go!!!
        sum_time = 0
        for future in as_completed(futures):  # 获取结果，as_completed()返回一个迭代器，按照完成顺序产出future
            n, pi_value, elapsed_time = future.result()  # 感谢 Python Cookbook
            logger.info(f"计算 {n} 项圆周率耗时: {elapsed_time} 秒，圆周率值: {pi_value}")
            sum_time += elapsed_time

    # END!
    end_time_main = time.perf_counter()
    logger.info(f"程序运行时间：{end_time_main - start_time_main} 秒")
    logger.info(f"所有进程总耗时: {sum_time} 秒")


if __name__ == "__main__":
    main()
