def check_child(a, i):
    if 2*i+1 < len(a):
        p = int(2*i+2 < len(a) and a[2*i+2] > a[2*i+1]) + 2*i + 1 #最大孩子的位置
        [a[p], a[i]] = [a[i], a[p]] if a[p] > a[i] else [a[p], a[i]] #最大孩子若大于该节点，则交换
        if a[p] > a[i]:
            a = check_child(a, i)
    return a

def heap_sort(a):
    n = len(a)
    if n > 1:
        for j in range(n, 0, -1):
            for i in range(int(n/2) - 1, -1, -1): #从后向前遍历非叶子节点
                a[:j] = check_child(a[:j], i)
            [a[j - 1], a[0]] = [a[0], a[j - 1]]
a = [12, 0, 8, 9, 11, 7, 2, 1]
heap_sort(a)
print(a)

