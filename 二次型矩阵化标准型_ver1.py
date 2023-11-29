import numpy as np

num_rows = int(input("请输入矩阵的行数："))

matrix_list = []

print("请输入矩阵，用空格分隔每个元素，输入完一行后按下回车：")
for i in range(num_rows):
    row_input = input()
    row_list = [float(num) for num in row_input.split()]
    matrix_list.append(row_list)

# 将列表转换为NumPy数组
matrix = np.array(matrix_list, dtype=np.float16)

print("原矩阵：\n", matrix)

for n in range(num_rows):
    if matrix[n, n] == 0 and n != num_rows - 1:
        row_sum = np.sum(matrix[n, :])
        if row_sum == 0:
            continue
        else:
            for i in range(num_rows):
                if matrix[n, i] != 0:
                    for p in range(num_rows):
                        matrix[p, n] -= matrix[p, i]
                    for p in range(num_rows):
                        matrix[n, p] -= matrix[i, p]
                    break
        for i in range(n + 1, num_rows):
            coefficient = matrix[n, i] / matrix[n, n]
            for p in range(num_rows):
                matrix[p, i] -= matrix[p, n] * coefficient
            for p in range(num_rows):
                matrix[i, p] -= matrix[n, p] * coefficient
    else:
        for i in range(n + 1, num_rows):
            coefficient = matrix[n, i] / matrix[n, n]
            for p in range(num_rows):
                matrix[p, i] -= matrix[p, n] * coefficient
            for p in range(num_rows):
                matrix[i, p] -= matrix[n, p] * coefficient

print("标准化矩阵（结果不唯一）：\n", matrix)
