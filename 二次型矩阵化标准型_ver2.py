import numpy as np

# 获取用户输入的矩阵行数
num_rows = int(input("请输入矩阵的行数："))

# 初始化列表以存储矩阵的行
matrix_list = []

print("请输入矩阵，用空格分隔每个元素，输入完一行后按下回车：")
for i in range(num_rows):
    # 获取用户输入的一行，并将其分割成单独的数字
    row_input = input()
    row_elements = [float(num) for num in row_input.split()]
    matrix_list.append(row_elements)

# 将列表转换为NumPy数组
matrix = np.array(matrix_list, dtype=np.float16)

print("原矩阵：\n", matrix)

# 遍历矩阵的每一行
for row_index in range(num_rows):
    # 检查对角线元素是否为零，如果为零，则尝试修正
    if matrix[row_index, row_index] == 0 and row_index != num_rows - 1:
        # 计算当前行的和
        row_sum = np.sum(matrix[row_index, :])
        # 如果当前行的和不为零，则修正矩阵
        if row_sum != 0:
            for col_index in range(num_rows):  # 遍历矩阵的列
                if matrix[row_index, col_index] != 0:
                    for i in range(num_rows):
                        matrix[i, row_index] -= matrix[i, col_index]
                    for i in range(num_rows):
                        matrix[row_index, i] -= matrix[col_index, i]
                    break
    # 对矩阵的非对角线元素进行初等变换，使其变为零
    for i in range(row_index + 1, num_rows):
        if matrix[row_index, row_index] != 0:  # 确保不会除以零
            coefficient = matrix[row_index, i] / matrix[row_index, row_index]
            for j in range(num_rows):
                matrix[j, i] -= matrix[j, row_index] * coefficient
            for j in range(num_rows):
                matrix[i, j] -= matrix[row_index, j] * coefficient

print("对角化矩阵（结果不唯一）：\n", matrix)
