"""
author:龚俊老婆
参考：叶强大佬
验证MRP，进行简单的轨迹回报计算
"""
#MRP包括：状态，转移概率，奖励，衰减因子
import numpy as np
from numpy.lib.shape_base import expand_dims

#状态
num_state = 7
#states' name to index
i_to_n = {}
i_to_n['0'] = 'C1'
i_to_n['1'] = 'C2'
i_to_n['2'] = 'C3'
i_to_n['3'] = 'Pass'
i_to_n['4'] = 'Pub'
i_to_n['5'] = 'FB'
i_to_n['6'] = 'Sleep'

#according to inedx to get name
#使用zip函数，可以将list进行绑定为元组
n_to_i = {}
for i,name in zip(i_to_n.keys(),i_to_n.values()):
    n_to_i[name] = int(i)

#转移概率矩阵
#C1,C2,C3,PASS,PUB,FB,SLEEP
Pss = [
    [0.0,0.5,0.0,0.0,0.0,0.5,0.0],
    [0.0,0.0,0.8,0.0,0.0,0.0,0.2],
    [0.0,0.0,0.0,0.6,0.4,0.0,0.0],
    [0.0,0.0,0.0,0.0,0.0,0.0,1.0],
    [0.2,0.4,0.4,0.0,0.0,0.0,0.0],
    [0.1,0.0,0.0,0.0,0.0,0.9,0.0],
    [0.0,0.0,0.0,0.0,0.0,0.0,1.0]
]

#reward:根据index可以直接获得在相应状态得到的奖励
reward = [-2,-2,-2,10,1,-1,0]

#衰减因子
gamma = 0.5

#计算某次轨迹的回报
def compute_return(start_index = 0,
                   chain = None,
                   gamma = 0.5)->float:
    """
    Args:
    start_index:chain中开始计算的位置
    chain：轨迹
    gamma:衰减因子
    Returns:
    return:回报，float
    """
    #从chain的start_index开始获得的回报
    G_start = 0.0   
    for i in range(start_index,len(chain)):
        G_start += np.power(gamma,i-start_index)*reward[n_to_i[chain[i]]]
    return G_start


#examples
chains = [
    ['C1','C2','C3','Pass','Sleep'],
    ['C1','FB','FB','C1','C2','Sleep'],
    ['C1','C2','C3','Pub','C2','C3','Pass','Sleep'],
    ['C1','FB','FB','C1','C2','C3','Pub','C1',\
    'FB','FB','FB','C1','C2','C3','Pub','C2','Sleep']
]


example_return = []
for i in range(4):
    example_return.append(compute_return(0,chains[i],0.5))
    print("The return of chian {0} is {1}".format(i,example_return[i]))

#the output is as folllow:
"""
The return of chian 0 is -2.25
The return of chian 1 is -3.125
The return of chian 2 is -3.40625
The return of chian 3 is -3.196044921875
"""




