"""
date:2021/7/5
author:和敏
references:https://mofanpy.com/tutorials/data-manipulation/np-pd/np-attributes/
numpy的基础
"""

#numpy数组的性质
import  numpy as np

"""
numpy数组的基本性质
"""
#numpy中的数组的性质包括：
#ndim:维度，等于shape的长度
#shape:规模，行数、列数
#size：元素个数

#数组的声明，列表转化为矩阵，参数是列表，然后没一行又是一个列表
a = np.array([[1,2,3],[4,5,6]])
print(a)
print(a.ndim)
print(a.shape)
print(a.size)
"""
output:
[[1 2 3]
 [4 5 6]]
2
(2, 3)
6
"""

"""
numpy创建数组进阶
dtype\zeros\ones\empty\arrange\linspace
"""
a = np.array([2,3,4])
print(a)
#dtype指定数据类型
#numpy中的int与C相同，要么是32要么64；int32那么就是32为有符号整数
a = np.array([2,3,4],dtype=np.int)
print(a.dtype)
a = np.array([2,3,4],dtype=np.float)
print(a.dtype)
a = np.array([2,3,4],dtype=np.int32)
print(a.dtype)
a = np.array([2,3,4],dtype=np.float32)
print(a.dtype)
"""
output:
int32
float64
int32
float32
"""

#创建特定的数组
#创建全零的数组
a = np.zeros((2,3))
print(a)
#创建全1的数组
a = np.ones((2,3))
print(a)
#创建全空数组，实际上就是每个值都接近0
a = np.empty((2,3))
#创建连续的数组
#10-19的数，步长为2
#这里生成的数据是一维的，可以使用reshape更改维度变成多维的矩阵
a = np.arange(10,20,2)
print(a)
#reshape更改数据的形状
a = np.arange(12).reshape(3,4)
print(a)
#linspace:创建线段数据
#起点为1，终点为10，分割成20个数据，生成线段
a = np.linspace(1,10,20)
print(a)
#linspace也可以与reshape一起使用
a = np.linspace(1,10,20).reshape(4,5)
"""
output:
[[0. 0. 0.]
 [0. 0. 0.]]
[[1. 1. 1.]
 [1. 1. 1.]]
[10 12 14 16 18]
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]]
[ 1.          1.47368421  1.94736842  2.42105263  2.89473684  3.36842105
  3.84210526  4.31578947  4.78947368  5.26315789  5.73684211  6.21052632
  6.68421053  7.15789474  7.63157895  8.10526316  8.57894737  9.05263158
  9.52631579 10.        ]
"""

