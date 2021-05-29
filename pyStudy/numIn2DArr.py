def Find(target, array):
    # write code here
    if target and array:
        i = 0
        j = len(array[0]) - 1
        while i < len(array) and j >= 0:
            if array[i][j] == target:
                return True
            elif array[i][j] > target:
                j -= 1
            else:
                i += 1
    return False

array = [[1, 1]]
target = 2
Find(target, array)