"""
author:龚俊老婆
参考：叶强大佬
对MDP过程建模，验证Bellman期望方程和Bellman最优方程
"""

#借鉴：这里import的时候最好还是将函数的名字包括，这样方便之后的调用
from utils import str_key,display_dict
from utils import set_prob,set_reward,get_prob,get_reward
from utils import set_value,set_pi,get_value,get_pi

#MDP:<S,A,R,P,GAMMA>
#S
S = ['FB','C1','C2','C3','Sleep']
#A
A = ['FB','Study','Quit-FB','Pub','Quit-Study']
#R
R = {}
#P
P = {}
gamma = 1

#根据MDP，设置状态转移概率矩阵
set_prob(P,S[0],A[0],S[0])
set_prob(P,S[0],A[2],S[1])
set_prob(P,S[1],A[0],S[0])
set_prob(P,S[1],A[1],S[2])
set_prob(P,S[2],A[4],S[4])
set_prob(P,S[2],A[1],S[3])
set_prob(P,S[3],A[1],S[4])
set_prob(P,S[3],A[3],S[1],p=0.2)
set_prob(P,S[3],A[3],S[2],p=0.4)
set_prob(P,S[3],A[3],S[3],p=0.4)

#设置价值
set_reward(R,S[0],A[0],-1)
set_reward(R,S[0],A[2],0)
set_reward(R,S[1],A[0],-1)
set_reward(R,S[1],A[1],-2)
set_reward(R,S[2],A[4],0)
set_reward(R,S[2],A[1],-2)
set_reward(R,S[3],A[1],10)
set_reward(R,S[3],A[3],1)

#得到的MDP模型
MDP = (S,A,R,P,gamma)

print("-"*10+"状态转移概率信息："+"-"*10)
display_dict(P)
print("-"*10+"奖励信息："+"-"*10)
display_dict(R)

#设置当前的策略
Pi = {}
set_pi(Pi,S[0],A[0],0.5)
set_pi(Pi,S[0],A[2],0.5)
set_pi(Pi,S[1],A[0],0.5)
set_pi(Pi,S[1],A[1],0.5)
set_pi(Pi,S[2],A[4],0.5)
set_pi(Pi,S[2],A[1],0.5)
set_pi(Pi,S[3],A[1],0.5)
set_pi(Pi,S[3],A[3],0.5)

#输出策略信息
print("-"*10+"策略信息："+"-"*10)
display_dict(Pi)

V = {}
#价值函数的信息
print("-"*10+"价值函数信息："+"-"*10)
display_dict(V)

#将价值函数的计算拆为两个部分
#首先计算出行为价值函数，将行为价值函数作为跳板
#给定MDP和价值函数，计算行为价值函数
#因为是使用价值函数，所以不涉及策略
def compute_q(MDP,V,s,a):
    S,A,R,P,gamma = MDP
    #s采取动作a之后可能的状态
    q_sa = 0.0
    for s_prime in S:
        q_sa += get_prob(P,s,a,s_prime)*get_value(V,s_prime)
    q_sa = get_reward(R,s,a)+gamma*q_sa
    return q_sa

#计算得行为价值函数，那么就可以计算给定策略下的
def compute_v(MDP,V,Pi,s):
    S,A,R,P,gamma = MDP
    v_s = 0
    for a in A:
        v_s  += get_pi(Pi,s,a)*compute_q(MDP,V,s,a)
    return v_s

#动态规划求解价值函数，其实就是不断进行策略评估
#基于Bellman期望方程，具体实现为compute_v函数
def update_v(MDP,V,Pi):
    S,_,_,_,_=MDP
    #这里的动态规划的实现是用新的计算新的
    V_prime = V.copy()
    for s in S:
        #用新的更新新的值
        V_prime[str_key(s)] = compute_v(MDP,V_prime,Pi,s)
        #一轮一轮地更新，最基本的动态规划
        #V[str_key(s)] = compute_v(MDP,V_prime,Pi,s)
    return V_prime


#策略评估，即动态规划计算价值函数
def policy_evaluate(MDP,V,Pi,n):
    for i in range(n):
        V = update_v(MDP,V,Pi)
        #update_v(MDP,V,Pi)
    return V

V = policy_evaluate(MDP,V,Pi,100)
display_dict(V)
"""
价值函数收敛输出为：
----------价值函数信息：----------

FB: -2.31
C1: -1.31
C2: 2.69
C3: 7.38
Sleep: 0.00
与PPT上的结果相同
"""

#此时已经收敛，计算某状态的价值函数将得到上述相同的结果
v = compute_v(MDP,V,Pi,"C3")
print("the value function of C3 is {:.2f}".format(v))


#求解最优策略和最优价值函数，基于Bellman最优方程，有价值迭代与策略迭代两种方法
def compute_v_from_max_q(MDP,V,s):
    S,A,R,P,gamma = MDP
    v_s = -float('inf')
    for a in A:
        v_s = max(v_s,compute_q(MDP,V,s,a))
    return v_s
def update_V_without_pi(MDP,V):
    S,_,_,_,_ = MDP
    V_prime = V.copy()
    for s in S:
        #这里用新的计算新的，应该更快收敛，但是一轮一轮更新也是可以的
        #V_prime[ste_key(s)] = compute_v_from_max_q(MDP,V,s)
        V_prime[str_key(s)] = compute_v_from_max_q(MDP,V_prime,s)
    return V_prime
def value_iterate(MDP,V,n):
    for i in range(n):
        V = update_V_without_pi(MDP,V)
    return V

V = {}
V_start = value_iterate(MDP,V,100)
display_dict(V_start)
"""
FB: 6.00
C1: 6.00
C2: 8.00
C3: 10.00
Sleep: 0.00
"""

#有了最优价值函数，那么可以得到最优行为价值函数，这时与策略无关
#因为通过价值函数计算行为价值函数的时候不涉及策略
#说明得到最优价值函数之后我们就可以得到最优行为价值函数，并且不需要知道策略
#至于最优价值函数等于行为价值函数，这是确定型策略，这是在求策略，注意区分在求什么
s,a = "C3","Pub"
q = compute_q(MDP,V_start,s,a)
print("在状态{}选择行为{}的最优价值为:{:.2f}".format(s,a,q))
#在状态C3选择行为Pub的最优价值为:9.40
