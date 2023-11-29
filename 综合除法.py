# 程序暂不支持接收虚数作为参数
def division(f, g):
    # 将多项式转换为系数列表
    f = [int(c) for c in f.split()]
    g = [int(c) for c in g.split()]
    if len(g) != 2:
        print("E: 程序只接收一次多项式的除式参数。")
        return
    # 求出除式本身的根，即x = -b/a
    root = -g[1] / g[0]
    # 初始化商和余式的系数列表
    q = [f[0]]
    r = []
    # 核心算法
    for i in range(1, len(f)):
        # 商的第i项系数等于被除式的第i项系数加上根乘以商的第i-1项系数
        q.append(f[i] + root * q[i - 1])
        # 余式的第i-1项系数等于被除式的第i-1项系数减去根乘以余式的第i-2项系数
        r.append(f[i - 1] - root * r[i - 2] if i > 1 else f[0])

    # 系数列表转多项式str
    def list_to_str(lst):
        string = ""
        n = len(lst)
        for i in range(n):
            if lst[i] != 0:  # 系数不为零时才输出该项
                if lst[i] > 0 and i != 0:  # 系数为正且不是第一项时输出加号
                    string += "+"
                if lst[i] != 1 or i == n - 1:  # 系数不为1或者是常数项时输出系数
                    string += str(lst[i])
                if i < n - 1:  # 不是常数项时输出x
                    string += "x"
                if i < n - 2:  # 次数大于1时输出次数
                    string += "^" + str(n - i - 1)
        return string

    print("\n商q(x) = ", list_to_str(q))
    print("余式r(x) = ", list_to_str(r))


def loop():
    print(
        f"--------------------"
        f"\n离线 / 备份 / 循环"
        f"\n信计02 张祚洲"
        f"\n--------------------"
    )
    f = input("请以空格分隔每个系数的方式输入被除式f(x)：")
    g = input("请以空格分隔每个系数的方式输入除式g(x)：")
    division(f, g)
    print("--------------------\n按Enter以重新运行，按其他键退出。")
    key = input()
    if key == "":
        loop()
    else:
        return


loop()
