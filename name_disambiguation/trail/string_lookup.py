import random
import numpy
import math
import time
import matplotlib.pyplot as plt
from itertools import combinations, permutations
import random
import itertools


organizations = ["Hebei Key of Optic-electronic information and materials, the college of physics science and technology, Hebei University, Baoding, 071002, P. R. China.",
                 "Satellite Healthcare, Inc., San Jose, CA, USA.",
                 "Faculty of Medicine, Western Sydney University, Australia.",
                 "Univ Calif San Francisco, San Francisco, CA 94143 USA"]


# 蛮力法—顺序查找
def SeqSearch1(r, n, k):
    i = n
    while i > 0 and r[i] != k:
        i -= 1
    return i


# print(SeqSearch1([0, 13, 21, 34, 45, 57, 76, 54, 48], 8, 48))


def SeqSearch2(r, n, k):
    i = n
    r[0] = k
    while r[i] != k:
        i -= 1
    return i


# print(SeqSearch2([0, 13, 21, 34, 45, 57, 76, 54, 48], 8, 48))


# 蛮力法—顺序查找

# 蛮力法—字符串匹配
# BF算法
# start of BF
# def BF(s, p):
#     """
#     蛮力法字符串匹配
#     """
#     indies = []
#     n = len(s)
#     m = len(p)
#     for i in range(n - m + 1):
#         index = i
#         for j in range(m):
#             if s[index] == p[j]:
#                 index += 1
#             else:
#                 break
#         if index - i == m:
#             indies.append(i)
#
#     return indies


def BF(s, p):
    indies = []
    n = len(s)
    m = len(p)
    print(n-m+1)
    for i in range(n-m+1):
        index = i
        for j in range(m):
            if s[index] == p[j]:
                index += 1
            else:
                break
        if index - i == m:
            indies.append(i)

    return indies

print(BF("abcdefg","d"))





# end of BF

# 字符串匹配-KMP算法
# start of KMP
def getNextList(s):
    n = len(s)
    nextList = [0, 0]
    j = 0
    for i in range(1, n):
        while j > 0 and s[i] != s[j]:
            j = nextList[j]
        if s[i] == s[j]:
            j += 1
        nextList.append(j)
    return nextList



def KMP(s, p):
    """
    Knuth-Morris-Pratt算法实现字符串查找
    """
    n = len(s)
    m = len(p)
    nextList = getNextList(p)
    indies = []
    j = 0
    for i in range(n):
        while s[i] != p[j] and j > 0:
            j = nextList[j]

        if s[i] == p[j]:
            j += 1
            if j == m:
                indies.append(i - m + 1)
                j = nextList[j]
    return indies


# end of KMP

# 字符串匹配-BM算法
# start of BM
def getBMBC(pattern):
    # 预生成坏字符表
    BMBC = dict()
    for i in range(len(pattern) - 1):
        char = pattern[i]
        # 记录坏字符最右位置（不包括模式串最右侧字符）
        BMBC[char] = i + 1
    return BMBC


def getBMGS(pattern):
    # 预生成好后缀表
    BMGS = dict()

    # 无后缀仅根据坏字移位符规则
    BMGS[''] = 0

    for i in range(len(pattern)):

        # 好后缀
        GS = pattern[len(pattern) - i - 1:]

        for j in range(len(pattern) - i - 1):

            # 匹配部分
            NGS = pattern[j:j + i + 1]

            # 记录模式串中好后缀最靠右位置（除结尾处）
            if GS == NGS:
                BMGS[GS] = len(pattern) - j - i - 1
    return BMGS


def BM(string, pattern):
    """
    Boyer-Moore算法实现字符串查找
    """
    m = len(pattern)
    n = len(string)
    i = 0
    j = m
    indies = []
    BMBC = getBMBC(pattern=pattern)  # 坏字符表
    BMGS = getBMGS(pattern=pattern)  # 好后缀表
    while i < n:
        while (j > 0):
            if i + j - 1 >= n:  # 当无法继续向下搜索就返回值
                return indies

            # 主串判断匹配部分
            a = string[i + j - 1:i + m]

            # 模式串判断匹配部分
            b = pattern[j - 1:]

            # 当前位匹配成功则继续匹配
            if a == b:
                j = j - 1

            # 当前位匹配失败根据规则移位
            else:
                i = i + max(BMGS.setdefault(b[1:], m), j - BMBC.setdefault(string[i + j - 1], 0))
                j = m

            # 匹配成功返回匹配位置
            if j == 0:
                indies.append(i)
                i += 1
                j = len(pattern)

    return indies


# end of BM
# 蛮力法—字符串匹配


def main():
    t1 = time.time()

    """
    r=[0,10,15,24,6,12,35,40,98,55]
    i=SeqSearch2(r,9,12)
    print('i=',i)
    """

    """
    s='abcabcacb'
    p='abcac'
    i=KMP(s,p)
    print('i=',i)
    """

    t2 = time.time()

    print('time=', (t2 - t1))


if __name__ == "__main__":
    main()
