#-*-coding:utf-8-*-
import numpy as np
data = [[1, 2, 8, 9], [2, 4, 9, 12], [4, 7, 10, 13], [6, 8, 11, 15]]
arr = np.array(data)
print(arr * 10)
arr.ndim
arr.shape
arr.dtype
np.zeros((10, 10, 10))
a = range(10)
b = np.arange(10)

np.eye(4)
fltArr = arr.astype(np.float64)
strArr = np.array(['2.3', '3.3123'], dtype=np.string_)
fltArr1 = strArr.astype(np.float64)

fltArr2 = strArr.astype(fltArr1.dtype)

#数组和标量的运算
arr1 = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64)
arr2 = np.array([[1, 2], [3, 4], [5, 6]], dtype=np.float64)
arr1 * arr1
1/arr1

#基本的索引和切片
arr = np.arange(10)
arr[5]
arr[5:8] #左闭右开
arr[5:8] = 12

arr = np.arange(10)
arr_ = arr[5:8]
arr_[0] = 100
print(arr)
arr_[:] = 13
print(arr)

arr = np.arange(10)
arr_ = arr[5:8].copy()
arr_[:] = 100
print(arr)

arr = np.array([[1, 2, 8, 9], [2, 4, 9, 12], [4, 7, 10, 13], [6, 8, 11, 15]])
arr[0]
arr[0, 1]
arr[0][1]

arr3d = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
arr3d[0]

arr_ = arr3d[0].copy()
arr3d[0] = 42
print(arr_)

arr = np.array([[1, 2, 8, 9], [2, 4, 9, 12], [4, 7, 10, 13], [6, 8, 11, 15]])
arr[0, 1:2]

#字符串数组索引
names = np.array(['a', 'b', 'c', 'd', 'c', 'a', 'c'])
data = np.random.randn(7, 4)
names == 'c'
data[names == 'c', 2:]

data[~(names != 'c'), 2:]

data = np.random.randn(7, 4)
data[data > 0] = 0

#花式索引
arr = np.empty((8, 4))
for i in np.arange(8):
    arr[i] = i

arr[[4, 1], :3]