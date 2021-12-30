# 开发时间：2021/12/29  8:59
# 随机生成1-21
import random
lst = []

while len(lst)!=21:
    lst.append(random.randint(1,21))
    set(lst)
