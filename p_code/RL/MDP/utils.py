"""
author:龚俊老婆
参考：叶强大佬
MDP建模时需要的对价值、转移概率、价值函数、行为价值函数的键值设置
"""
from matplotlib import use
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random 


#*args表示可变的参数，其是tuple
#MDP中包括状态、动作、价值、转移概率、衰减因子
#价值与状态和动作有关
#转移概率与状态、动作和下一个状态有关
#使用字典进行相关绑定，这里的函数即辅助相关值得绑定

#首先是获得键值，键值可能是tuple(s,a)或者是list[(s,a),s']
#这说明进行参数分析的时候提供多种方法
#键值：string,中间用"_"连接
def str_key(*args):
    new_args = []
    for arg in args:
        if type(arg) in [tuple,list]:
            new_args += [str(i) for i in arg]
        else:
            new_args.append(str(arg))
    
    #join方法将list中的字符使用特定的字符连接成一个新的字符串
    #注意：list中的元素必须是字符才可以
    return "_".join(new_args)

#设置键值
def set_dict(target_dict,value,*args):
    target_dict[str_key(*args)] = value

def get_dict(target_dict,*args):
    return target_dict.get(str_key(*args),0)

#以上部分是基础函数，接下来是具体操作

#设置转移概率
def set_prob(P,s,a,s1,p=1.0):
    set_dict(P,p,s,a,s1)

#获得概率
#返回key对应的价值
def get_prob(P,s,a,s1):
    return P.get(str_key(s,a,s1),0)


#设置价值
def set_reward(R,s,a,r):
    set_dict(R,r,s,a)
#获得价值
def get_reward(R,s,a):
    return R.get(str_key(s,a),0)

#设定价值函数的值
def set_value(V,s,v):
    set_dict(V,v,str_key(s))
#获得价值函数的值
def get_value(V,s):
    return V.get(str_key(s),0)

#策略
def set_pi(Pi,s,a,p=0.5):
    set_dict(Pi,p,s,a)
def get_pi(Pi,s,a):
    return Pi.get(str_key(s,a),0)

#辅助函数，输出字典的内容
def display_dict(target_dict):
    for key in target_dict:
        print("{}: {:.2f}".format(key,target_dict[key]))
    print(" ")

#获取贪心策略下，每个动作采取的概率
#max的动作等概率选取，其余动作的概率为0
#pi返回的是概率
def greedy_pi(A,s,Q,a):
    max_q,a_max_q = -float("inf"),[]
    for a_opt in A:
        q = get_dict(Q,s,a_opt)
        if q > max_q:
            a_max_q = [a_opt]
            max_q = q
        elif q == max_q:
            a_max_q.append(a_opt)
    n = len(a_max_q)
    if n == 0:
        return 0.0
    #判断当前的动作是否是最优贪心对应的动作，返回其概率
    return 1.0/n if a in a_max_q else 0.0

#Policy返回的是策略，即动作
def greedy_policy(A,s,Q):
    """
    返回状态s下最大的Q对应的动作
    """
    q_max,a_max_q = -float("inf"),[]
    for a_opt in A:
        q = get_dict(Q,s,a_opt)
        if q > q_max:
            a_max_q = [a_opt]
            q_max = q
        elif q == q_max:
            a_max_q.append(a_opt)
    return random.choice(a_max_q)





#epsilon-greedy pi，返回的是epsilon-greedy的动作概率
#如果是max，那么可能有多个，所以每个的概率为：
#(1-epsilon)/n+epsilon/m=(1-epsilon)*greedy_p+epsilon/m
def epsilon_greedy_pi(A,s,Q,a,epsilon=0.1):
    m = len(A)
    greedy_p = greedy_pi(A,s,Q,a)
    if greedy_p == 0:
        return epsilon/m
    return (1-epsilon)*greedy_p+epsilon/m


#获得贪心策略，返回的是动作
def epsilon_greedy_policy(A,s,Q,epsilon,show_random_num=False):
    pis = []
    m = len(A)
    #首先获得每个动作的概率
    for i in range(m):
        pis.append(epsilon_greedy_pi(A,s,Q,A[i],epsilon))
    #按照产生的概率选择动作，这个方法实现很好，值得学习
    rand_value = random.random()
    for i in range(m):
        if show_random_num:
            print("产生的随机数为：{:.2f}，拟减去概率:{}".format(rand_value,pis[i]))
        #通过减的过程，相当于不断产生随机数
        rand_value -= pis[i]
        if rand_value < 0:
            return A[i]

#画图辅助函数
#价值函数可视化
#可以选择画价值函数行为价值函数
def draw_value(value_dict,useable_ace = False,is_q_dict = False,A = None):
    #首先定义画图对象
    fig = plt.figure()
    #变为3D
    ax = Axes3D(fig)
    x = np.arange(1,11,1)
    y = np.arange(12,22,1)
    #生成网格数据
    X,Y = np.meshgrid(x,y)
    row,col = X.shape
    Z = np.zeros((row,col))
    if is_q_dict:
        n = len(A)
    for i in range(row):
        for j in range(col):
            state_name = str(X[i,j])+"_"+str(Y[i,j])+"_"+str(useable_ace)
            if not is_q_dict:
                Z[i,j] = get_dict(value_dict,state_name)
            else:
                assert(A is not None)
                #如果是行为价值函数，那么显示的是最大行为价值函数的值
                for a in A:
                    new_state_name = state_name+"_"+str(a)
                    q = get_dict(value_dict,new_state_name)
                    if q>=Z[i,j]:
                        Z[i,j] = q
    #绘制图像
    ax.plot_surface(X,Y,Z,rstride = 1,cstride = 1,color = "lightgray")
    plt.show()

#绘制策略
def draw_policy(policy,A,Q,epsilon,useable_ace = False):
    #只有两个动作，叫牌或者不叫牌
    def value_of(a):
        if a == A[0]:
            #print("0")
            return 0
        else:
            #print("1")
            return 1
    row,col = 11,10
    useable_ace = bool(useable_ace)
    Z = np.zeros((row,col))
    dealer_first_card = np.arange(1,12)
    player_points = np.arange(12,22)
    for i in range(11,22):
        for j in range(1,11):
            s = j,i,useable_ace
            s = str_key(s)
            #根据传入的策略，获得相应状态下的动作
            #策略就是根据状态获得相应的动作！！！！
            a = policy(A,s,Q,epsilon)
            Z[i-11,j-1] = value_of(a)
    
    #画灰度图
    plt.imshow(Z,cmap = plt.cm.cool,interpolation=None,origin="lower",extent = [0.5,11.5,10.5,21.5])

#print("hello")
