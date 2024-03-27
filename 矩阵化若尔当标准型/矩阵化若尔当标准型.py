import sympy as sym
from IPython.display import display_latex
from IPython.display import Latex, Math, display
import numpy as np
from functools import reduce

sym.init_printing()


def ColumnContact(M):
    """将列向量列表拼接成一个矩阵"""
    m = M.copy()
    r = m[0]
    for i in range(1, len(m)):
        r = r.row_join(m[i])
    return r


def is_in_space(space, v):
    """判断向量 v 是否在空间 space 中"""
    S = space.copy()
    vect = v.copy()
    dim_S = len(S)
    S.append(vect)
    if ColumnContact(S).rank() > dim_S:
        return False
    return True


def complementary(g, s):
    """找到 r 使得 g 是 s 和 r 的直和"""
    G = g.copy()
    S = s.copy()
    dim_diff = len(G) - len(S)
    R = []
    for vect in G:
        if len(R) == dim_diff:
            return R
        if not is_in_space(S, vect):
            R.append(vect)
    return R


def JordanForm_analysis(A, opt):
    """用分析方法计算矩阵 A 的 Jordan 标准形"""

    n = A.shape[0]
    evs = A.eigenvects()
    num = len(evs)

    特征值列表 = [vals[0] for vals in evs]
    代数重数列表 = [vals[1] for vals in evs]
    矩阵列表 = [A - r * sym.eye(n) for r in 特征值列表]
    广义矩阵列表 = [(A - 特征值列表[i] * sym.eye(n)) ** 代数重数列表[i] for i in range(num)]
    空间列表 = [M.nullspace() for M in 矩阵列表]
    广义空间列表 = [M.nullspace() for M in 广义矩阵列表]
    转换列表 = []
    字符串 = ""
    总字符串 = ""

    if opt:
        display(Math(r'矩阵\ A\ 为'))
        display(A)
        display(Math(r'A\ 的特征值及其代数重数为'))
        for k in range(num):
            display(Math(r'\lambda_{}={}\quad\quad\quad m_{}={}'.format(k + 1, 特征值列表[k], k + 1, 代数重数列表[k])))

    for k in range(num):

        phi = 矩阵列表[k]
        eigspace = 空间列表[k]
        genspace = 广义空间列表[k]
        补空间 = complementary(genspace, eigspace)
        vij列表 = []
        i = 1

        if opt:
            display(Math(r'({})\ 考虑特征值\  \lambda_{}={}\ 代数重数\ m_{}={}'
                         .format(k + 1, k + 1, 特征值列表[k], k + 1, 代数重数列表[k])))
            display(Math(r'矩阵\ A-({})I\ 和\ (A-({})I)^{}\ 分别为'
                         .format(特征值列表[k], 特征值列表[k], 代数重数列表[k])))
            display([矩阵列表[k], 广义矩阵列表[k]])
            display(Math(r'对应的特征空间\ E({},A)\ 是\ A-({})I\ 的零空间，由以下向量张成'
                         .format(特征值列表[k], 特征值列表[k])))
            display(eigspace)
            display(Math(
                r'对应的广义特征空间\ E^g({},A)\ 是\ (A-({})I)^{} 的零空间，由以下向量张成'
                .format(特征值列表[k], 特征值列表[k], 代数重数列表[k])))
            display(genspace)

        while len(补空间) > 0:
            j = 1
            bunch列表 = []
            vect = 补空间[0]
            if opt:
                字符串 = 'v_{' + str(j) + str(i) + '}^{(' + str(k + 1) + ')}'
                display(Math(r'现在我们在 E^g({},A)\ 中选择一个向量 v，但 v 不在 E({},A)，即'
                             .format(特征值列表[k], 特征值列表[k])))
                display(vect)
            while not is_in_space(空间列表[k], vect):
                bunch列表.insert(0, vect)
                vect = phi * vect
                j = j + 1
                if opt:
                    字符串 = 字符串 + r',\ v_{' + str(j) + str(i) + '}^{(' + str(k + 1) + ')}'
            eigspace = complementary(eigspace, [vect])
            补空间 = complementary(补空间, bunch列表)
            bunch列表.insert(0, vect)
            vij列表.extend(bunch列表)
            i = i + 1
            if opt:
                display(Math(r'不断用\ A-({})I\ 作用于 v（直到\ v\in E({},A))\ 得到以下一系列向量'
                             .format(特征值列表[k], 特征值列表[k])))
                display(Math(r'[' + 字符串 + ']='))
                display(bunch列表)
                总字符串 = 总字符串 + 字符串 + r',\ '

        if len(eigspace) > 0:
            vij列表.extend(eigspace)
            if opt:
                j = 1
                字符串 = 'v_{' + str(j) + str(i) + '}^{(' + str(k + 1) + ')}'
                for js in range(len(eigspace) - 1):
                    j = j + 1
                    字符串 = 字符串 + r',\ v_{' + str(j) + str(i) + '}^{(' + str(k + 1) + ')}'
                display(Math(
                    r'此时，我们需要找到 E({},A)\ 中的其余元素(们)以扩展成一组基'
                    .format(特征值列表[k])))
                display(Math(r'[' + 字符串 + ']='))
                display(eigspace)
                总字符串 = 总字符串 + 字符串 + r',\ '

        转换列表.extend(vij列表)

    P = ColumnContact(转换列表)
    J = sym.Inverse(P) * A * P
    if opt:
        display(Math(r'最终，可逆矩阵\ P=[' + 总字符串[:-3] + ']='))
        display(P)
        display(Math(r'因此，Jordan 标准形为\ J=P^{-1}AP='))
        display(J)

    return J


def JordanForm(A):
    """不使用分析方法计算 A 的 Jordan 标准形"""

    return JordanForm_analysis(A, False)


# 在这里指定矩阵 A
A = sym.Matrix([[4, -1, -3, 2], [4, -2, -4, 4], [-4, 4, 6, -4], [-6, 5, 7, -4]])

J = JordanForm_analysis(A, True)
