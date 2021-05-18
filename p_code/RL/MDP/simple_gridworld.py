"""
author:龚俊老婆
参考：叶强大佬
基于4*4的小方格世界进行动态规划相关求解（预测与控制）
"""

#首先对4*4的小方格进行建模

S = [i for i in range(16)]
A = ["n","e","s","w"]
#动作导致的状态变化
ds_action = {"n":-4,"e":1,"s":4,"w":-1}

#方格世界的动力学
#即状态s下采取动作a的奖励，后继状态
def dynamic(s,a):
    """
    Args:
    s:current state
    a:action to be executed
    Returns:
    s_prime:the next state
    reward
    is_end:wheather end
    """
    #boundary
    s_prime = s 
    if (s%4==0 and a == "w") or (s<4 and a == "n")\
        or (s>11 and a == "s") or ((s+1)%4==0 and a == "e")\
        or s in [0,15]:
        pass
    else:
        ds = ds_action[a]
        s_prime = s+ds
    if s in [0,15]:
        reward = 0
    else:
        reward = -1
    is_end = True if s in [0,15] else False
    return s_prime,reward,is_end

#得到环境动力学之后，可以继续MDP的建模
#状态转移概率
def P(s,a,s1):
    s_prime,_,_ = dynamic(s,a)
    return s1==s_prime
#得到即时奖励
def R(s,a):
    _,r,_ = dynamic(s,a)
    return r 

gamma = 1.0
#得到MDP模型，这里的R和P不再是字典而是函数
#很多时候MDP的R和P都不是固定的，所以注意这里的模型构建的方式
#不一定是确定型的，可以使用函数
MDP = S,A,R,P,gamma 


#策略函数
#随机策略和贪心策略
#随机策略一般只需要知道状态和动作，最优策略还需要知道价值函数
#这里为了调用参数的一致性，对参数的形式进行相同化处理
def uniform_random_pi(MDP=None,V = None,s = None,a = None):
    _,A,_,_,_ = MDP
    n = len(A)
    return 0 if n== 0 else 1.0/n

#贪心策略取max Q(s,a)=r+sum P(s,a,s')v(s')
#因为这里的状态转移是1，并且采取动作得到的即时奖励是相同的，所以直接判断下一个状态的
#价值就可以了
#最优策略并不是直接返回策略，而是将动作也作为一个参数
def greedy_pi(MDP,V,s,a):
    S,A,R,P,gamma = MDP
    max_v = -float("inf")
    a_max_v = [] #价值函数最大的动作可能有多个
    for a_opt in A:
        s_prime,reward,_ = dynamic(s,a_opt)  #得到下一个状态
        v_s_prime = get_value(V,s_prime)   #得到下一个状态的价值
        if v_s_prime > max_v:
            max_v = v_s_prime
            a_max_v = [a_opt]   #当出现新的最大的时候就重新初始最大价值动作矩阵
            #这个方法学到了
        elif v_s_prime == max_v:
            a_max_v.append(a_opt)
    #得到最大价值的动作
    n = len(a_max_v)
    if n == 0: return 0.0
    return 1.0/n if a in a_max_v else 0.0

#获得策略
#这里学到了，函数也可以作为参数传递
def get_pi(Pi,s,a,MDP = None,V=None):
    return Pi(MDP,V,s,a)

#辅助函数
def get_prob(P,s,a,s1):
    return P(s,a,s1)
def get_reward(R,s,a):
    return R(s,a)

def set_value(V,s,v):
    V[s] = v 

def get_value(V,s):
    return V[s]

def display_V(V):
    for i in range(16):
        print("{0:>6.2f}".format(V[i]),end=" ")
        if(i+1)%4==0:
            print("")
    print()

#建模和辅助函数完成
#现计算行为价值函数
def compute_q(MDP,V,s,a):
    S,A,R,P,gamma = MDP
    q_sa = 0
    for s_prime in S:
        q_sa += get_prob(P,s,a,s_prime)*get_value(V,s_prime)
    q_sa = get_reward(R,s,a)+gamma*q_sa
    return q_sa
#计算价值函数
def compute_v(MDP,V,Pi,s):
    S,A,R,P,gamma = MDP
    v_s = 0
    for a in A:
        v_s += get_pi(Pi,s,a,MDP,V)*compute_q(MDP,V,s,a)
    return v_s

#Bellman期望方程
def update_V(MDP,V,Pi):
    S,_,_,_,_ = MDP
    V_prime = V.copy()
    for s in S:
        set_value(V_prime,s,compute_v(MDP,V_prime,Pi,s))
    return V_prime

#基于策略的预测，策略评估
def policy_evaluate(MDP,V,Pi,n):
    for i in range(n):
        V = update_V(MDP,V,Pi)
    return V

#基于策略的控制，方法一
#策略迭代：首先策略评估然后策略提升
def policy_iterate(MDP,V,Pi,n,m):
    for i in range(m):
        V = policy_evaluate(MDP,V,Pi,n)
        Pi = greedy_pi
    return V


#基于策略的控制，方法二
#价值迭代分为三步实现
#首先获得当下状态下的最大行为价值函数
#将价值函数赋值为最大的行为价值函数
#进行迭代
#价值迭代无策略
def compute_v_from_max_q(MDP,V,s):
    S,A,R,P,gamma = MDP
    v_s = -float("inf")
    for a in A:
        qsa = compute_q(MDP,V,s,a)
        if qsa > v_s:
            v_s = qsa
    return v_s
#赋值
def update_V_without_pi(MDP,V):
    S,_,_,_,_ = MDP
    V_prime = V.copy()
    for s in S:
        set_value(V_prime,s,compute_v_from_max_q(MDP,V_prime,s))
    return V_prime
#迭代
def value_iterate(MDP,V,n):
    for i in range(n):
        V = update_V_without_pi(MDP,V)
    return V

#策略评估，随机的策略和贪心的策略
V = [0 for _ in range(16)]
V_pi = policy_evaluate(MDP,V,uniform_random_pi,100)
print("随机策略价值评估")
display_V(V_pi)

V = [0 for _ in range(16)]
V_pi = policy_evaluate(MDP,V,greedy_pi,100)
print("贪心策略价值评估")
display_V(V_pi)


#求解最优策略
#策略迭代
#策略迭代的时候，策略评估时只进行一轮
#但是写函数的时候可以写为进行多轮进行扩展
V = [0 for _ in range(16)]
V_pi = policy_iterate(MDP,V,uniform_random_pi,1,1)
V_pi = policy_iterate(MDP,V_pi,greedy_pi,1,100)
print("策略迭代求解最优价值函数")
display_V(V_pi)
#价值迭代
V_pi = value_iterate(MDP,V,4)
print("价值迭代求解最优价值函数")
display_V(V_pi)

"""
输出
随机策略价值评估
  0.00 -14.00 -20.00 -22.00 
-14.00 -18.00 -20.00 -20.00
-20.00 -20.00 -18.00 -14.00
-22.00 -20.00 -14.00   0.00

贪心策略价值评估
  0.00  -1.00  -2.00  -3.00 
 -1.00  -2.00  -3.00  -2.00
 -2.00  -3.00  -2.00  -1.00
 -3.00  -2.00  -1.00   0.00

策略迭代求解最优价值函数
  0.00  -1.00  -2.00  -3.00 
 -1.00  -2.00  -3.00  -2.00
 -2.00  -3.00  -2.00  -1.00
 -3.00  -2.00  -1.00   0.00

价值迭代求解最优价值函数
  0.00  -1.00  -2.00  -3.00
 -1.00  -2.00  -3.00  -2.00
 -2.00  -3.00  -2.00  -1.00
 -3.00  -2.00  -1.00   0.00

 可以看出，贪心策略的价值函数与最优价值函数相等
"""

#根据最优价值函数得到最优策略
def greedy_policy(MDP,V,s):
    S,A,P,R,gamma = MDP
    max_v,a_max_v = -float("inf"),[]
    for a_opt in A:
        s_prime,reward,_ = dynamic(s,a_opt)
        v_s_prime = get_value(V,s_prime)
        if v_s_prime > max_v:
            a_max_v = a_opt
            max_v = v_s_prime
        elif v_s_prime == max_v:
            a_max_v+=a_opt
    return str(a_max_v)

#将策略作为参数
def display_policy(policy,MDP,V):
    S,A,R,P,gamma = MDP
    for i in range(16):
        print("{0:^6}".format(policy(MDP,V,S[i])),end=" ")
        if(i+1)%4 == 0:
            print(" ")
    print()
print("根据最优价值函数得到最优策略：")
display_policy(greedy_policy,MDP,V_pi)
"""
根据最优价值函数得到最优策略：
 nesw    w      w      sw
  n      nw    nesw    s
  n     nesw    es     s
  ne     e      e     nesw
"""




