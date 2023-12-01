# 信计02班 张祚洲

# 参考了一些资料并化身为cv小子，结合宋浩老师的课程最终得到了此版本
# 我们使用初等变换的方法来实现算法，配方法恕实在写不来


import numpy as np


def print_matrix(mat):
    # 遍历矩阵的每一行
    for row in mat:
        # 格式化每个元素，整数则去掉小数点，浮点数保留，并转换为字符串列表
        formatted_row = ['{:g}'.format(elem) if elem.is_integer() else str(elem) for elem in row]
        print('\t'.join(formatted_row))


def get_input_matrix(num_rows):
    # 初始化一个列表来存储矩阵的所有行
    matrix_list = []
    print("请输入矩阵，用空格分隔每个元素，输入完一行后按下回车：")

    for _ in range(num_rows):
        row_input = input()
        # 将输入的每个数字转换为浮点数，并添加到行列表中
        row_elements = [float(num) for num in row_input.split()]
        # 将行列表添加到矩阵列表中
        matrix_list.append(row_elements)
    # 将矩阵列表转换为NumPy数组
    return np.array(matrix_list, dtype=np.float64)


def diagonalize_matrix(matrix):
    # 获取矩阵的行数
    num_rows = len(matrix)
    # 遍历每一行
    for row_index in range(num_rows):
        # 如果对角线上的元素为0，并且不是最后一行
        if matrix[row_index, row_index] == 0 and row_index != num_rows - 1:
            # 计算当前行的元素和
            row_sum = np.sum(matrix[row_index, :])
            # 如果行和不为0，则进行行变换
            if row_sum != 0:
                for col_index in range(num_rows):
                    if matrix[row_index, col_index] != 0:
                        # 更新矩阵的列
                        for i in range(num_rows):
                            matrix[i, row_index] -= matrix[i, col_index]
                        # 更新矩阵的行
                        for i in range(num_rows):
                            matrix[row_index, i] -= matrix[col_index, i]
                        break
        # 对当前行以下的每一行进行处理，使非对角线元素变为0
        for i in range(row_index + 1, num_rows):
            if matrix[row_index, row_index] != 0:
                # 计算变换系数
                coefficient = matrix[row_index, i] / matrix[row_index, row_index]
                # 更新列
                for j in range(num_rows):
                    matrix[j, i] -= matrix[j, row_index] * coefficient
                # 更新行
                for j in range(num_rows):
                    matrix[i, j] -= matrix[row_index, j] * coefficient
    return matrix


def main():
    num_rows = int(input("请输入矩阵的行数："))

    matrix = get_input_matrix(num_rows)
    print("原矩阵：")
    print(matrix)

    matrix = diagonalize_matrix(matrix)
    print("对角化矩阵（结果不唯一）：")
    print(matrix)


if __name__ == "__main__":
    main()
