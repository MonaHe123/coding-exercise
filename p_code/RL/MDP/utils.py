"""
author:龚俊老婆
参考：叶强大佬
MDP建模时需要的对价值、转移概率、价值函数、行为价值函数的键值设置
"""

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

