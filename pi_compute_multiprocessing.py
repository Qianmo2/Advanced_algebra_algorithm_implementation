import time
import logging
from multiprocessing import Pool

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()


def pi_compute(n: int) -> str:
    """
    计算圆周率，采用莱布尼茨公式的计算方法
    参考 https://blog.csdn.net/m0_62488776/article/details/131463332
    :param n: 计算项数
    :return: 圆周率的字符串表示
    """
    pi = 0
    for i in range(n):
        pi += (-1) ** i / (2 * i + 1)
    pi *= 4
    return str(pi)


def compute_and_log(n: int) -> None:
    """
    计算圆周率并记录时间
    :param n: 计算项数
    """
    start_time = time.time()
    pi_value = pi_compute(n)
    end_time = time.time()
    logger.info(f"计算 {n} 项圆周率耗时: {end_time - start_time} 秒")

    logger.info(f"圆周率值: {pi_value[:n + 2]}")


def main():
    # 从用户输入获取不同的精度
    input_str = input("请输入精确到小数点后多少位，用空格分隔（例如 100 1000 10000）: ")
    precisions = [int(n) for n in input_str.split()]

    with Pool() as pool:
        pool.map(compute_and_log, precisions)


if __name__ == "__main__":
    main()
