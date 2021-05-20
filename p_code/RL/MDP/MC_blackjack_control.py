"""
author:龚俊老婆
参考：知乎叶强大佬
无模型控制
基于MC寻找21点游戏的最优策略
"""
#不能直接从MC_blackjack_predict中import，因为python为解释型语言，import的时候会执行predict中的代码
#将需要的基类存到blackjack.py中

from blackjack import Player,Dealer,Arena
from utils import str_key,set_dict,get_dict
from utils import draw_value,draw_policy
from utils import epsilon_greedy_policy
import math 

#创建具有MC控制的玩家类
#MC_control:
#(1)MC估计行为价值函数
#(2)epsilon_greedy提升策略
class MC_Player(Player):
    def __init__(self,name="",A = None,display = False):
        """
        不基于模型，使用行为价值函数
        """
        super().__init__(name,A,display)
        self.Q = {}
        self.Nsa = {}
        self.total_learning_times = 0
        #这里设置了策略核学习方法
        self.policy = self.epsilon_greedy_policy
        self.learning_method = self.learn_Q
    
    #(1)MC估计行为价值函数
    def learn_Q(self,episode,r):
        for s,a in episode:
            nsa = get_dict(self.Nsa,s,a)
            q = get_dict(self.Q,s,a)
            set_dict(self.Nsa,nsa+1,s,a)
            set_dict(self.Q,q+(r-q)/(nsa+1),s,a)
        self.total_learning_times += 1
    
    #清空学习经历
    def reset_memory(self):
        self.Q.clear()
        self.Nsa.clear()
        self.total_learning_times = 0
    
    #(2)根据epsilon_greedy_policy进行策略提升
    def epsilon_greedy_policy(self,dealer,epsilon = None):
        player_points,_ = self.get_points()
        if player_points >= 21:
            return self.A[1]
        if player_points < 12: 
            return self.A[0]
        else:
            A,Q = self.A,self.Q
            s = self.get_state_name(dealer)
            if epsilon is None:
                epsilon = 1.0/(1+4*math.log10(1+self.total_learning_times))
                #epsilon = 0.1
            return epsilon_greedy_policy(A,s,Q,epsilon)
    
#接下来进行对局生成episode，然后根据episode进行控制
A = ["继续叫牌","停止叫牌"]
display = False
player = MC_Player(A = A,display=display)
dealer = Dealer(A = A,display=display)
arena = Arena(A = A, display = display)
arena.play_games(dealer=dealer,player = player,num = 20000,show_statistic=True)

#画出最高的行为价值函数和策略空间
#得到训练后的行为价值函数，其实其中就隐含了策略
draw_value(player.Q,useable_ace = True,is_q_dict = True,A = player.A)
draw_policy(epsilon_greedy_policy,player.A,player.Q,epsilon = 1e-10,useable_ace = True)
draw_value(player.Q,useable_ace = False,is_q_dict = True,A = player.A)
draw_policy(epsilon_greedy_policy,player.A,player.Q,epsilon = 1e-10,useable_ace = False)



