"""
author:龚俊老婆
参考：知乎叶强大佬
21点游戏的基类
"""
from random import shuffle
from queue import Queue

from matplotlib import use
from tqdm import tqdm           #用于进度条显示
import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from utils import str_key,set_dict,get_dict         #对字典进行操作的辅助函数


#首先建立游戏的基类
class Game():
    '''
    游戏者基类
    '''
    def __init__(self,name="",A = None,display = False):
        """
        姓名
        自己的牌
        动作空间
        策略
        学习方法
        是否进行信息展示
        """
        self.name = name
        self.cards = []
        self.A = A
        self.policy = None
        self.learning_method = None
        self.display = display
    
    """
    游戏类进行的操作：
    输出名字
    根据牌得到值
    计算自己的牌的总点数
    叫牌
    放弃原来的牌，重新开始
    """
    def __str__(self):
        return self.name 
    def _value_of(self,card):
        """
        根据牌面信息得到牌的数值的大小
        """
        try:
            v = int(card)
        except:
            if card == "A":
                v = 1
            elif card in ["J","Q","K"]:
                v = 10
            else:
                v = 0
        finally:
            return v

    def get_points(self):
        """
        计算拥有的牌的总的点数
        Args:
        self.cards
        Return:
        tuple(points,is_ace)
        """
        num_of_useable_ace = 0
        total_point = 0
        cards = self.cards
        if cards is None:
            return 0,False
        for card in cards:
            v = self._value_of(card)
            if v == 1:
                num_of_useable_ace += 1
                v = 11
            total_point += v
        while total_point > 21 and num_of_useable_ace > 0:
            total_point -= 10
            num_of_useable_ace -= 1
        return total_point, bool(num_of_useable_ace)
    
    def receive(self,cards = []):
        """
        叫牌，一次性可能叫多张牌
        """
        cards = list(cards)
        for card in cards:
            self.cards.append(card)
    
    def discharge_cards(self):
        """
        放弃原来的牌重新开始
        """
        self.cards.clear()

    #辅助函数，进行额外信息的输出
    #to do:why there is self.role
    #这里的self.role在子类中定义
    #说明python中子类定义的属性可以在父类的函数中访问
    def cards_info(self):
        self._info("{}{}现在的牌:{}\n".format(self.role,self,self.cards))
    def _info(self,msg):
        if self.display:
            print(msg,end=" ")
    
#基于游戏者基类，建立庄家类
class Dealer(Game):
    def __init__(self,name="",A = None,display=False):
        """
        庄家和玩家基于基类：角色不同，使用的策略不同
        """
        super().__init__(name,A,display)
        self.role = "庄家"
        self.policy = self.dealer_policy

    """
    庄家进行的操作：
    展示自己的第一张牌
    自己的策略
    """
    def first_card_value(self):
        if self.cards is None or len(self.cards)==0:
            return 0
        return self._value_of(self.cards[0])

    def dealer_policy(self,Dealer = None):
        action = ""
        dealer_points,_ = self.get_points()
        if dealer_points >= 17:
            action = self.A[1]      #停止叫牌
        else:
            action = self.A[0]      #继续叫牌
        return action 
    
class Player(Game):
    def __init__(self, name="", A=None, display=False):
        super().__init__(name=name, A=A, display=display)
        """
        庄家和玩家基于基类的不同：角色不同，采取的策略不同
        """
        self.role = "玩家"
        self.policy = self.naive_policy

    """
    玩家进行的动作：
    获得庄家的第一张牌的点数
    返回当前的状态
    使用的策略
    """
    def get_state(self,dealer):
        """
        Args:
        庄家
        Returns:
        tuple(庄家第一张牌，玩家的分数，是否有ace)
        """
        dealer_first_card_value = dealer.first_card_value()
        player_points,useable_ace = self.get_points()
        return dealer_first_card_value,player_points,useable_ace
    def get_state_name(self,dealer):
        return str_key(self.get_state(dealer))
    
    def naive_policy(self,dealer=None):
        """
        Args:
        庄家作为参数，以便之后要对战的情况的修改提供方便
        Returns:
        返回动作
        """
        player_points,_ = self.get_points()
        if player_points < 20:
            action = self.A[0]
        else:
            action = self.A[1]      #停止叫牌
        return action 
    
#游戏管理类
"""
可以进行的操作有：
收集牌，进行洗牌
判断玩家和庄家是否结束，给出奖励
发牌
回收牌
进行一次游戏
"""
class Arena():
    def __init__(self,display = None,A = None):
        """
        游戏管理者的状态包括：
        牌的信息：牌、已经公开的牌，产生的对局信息，行为空间
        """
        self.cards = ['A','1','2','3','4','5','6','7','8','9','J','Q','K']*4
        self.card_q = Queue(maxsize = 52)       #洗好的牌
        self.cards_in_pool = []                 #已经公开的牌
        self.display = display
        self.episodes = []                      #产生的对局信息
        self.load_cards(self.cards)             #发牌器
        self.A = A

    def load_cards(self,cards):
        """
        Args:洗好的牌
        Return:None
        """
        shuffle(cards)
        for card in cards:
            self.card_q.put(card)
        cards.clear()
        return

    def reward_of(self,dealer,player):
        """
        Args:玩家和庄家
        Returns:reward,dealer_points,player_points,useable_ace
        """
        dealer_points,_ = dealer.get_points()
        player_points,useable_ace = player.get_points()
        if player_points > 21:
            reward = -1
        else:
            if player_points > dealer_points or dealer_points > 21:
                reward = 1
            elif player_points == dealer_points:
                reward = 0
            else:
                reward = -1
        
        return reward,player_points,dealer_points,useable_ace
    
    def serve_card_to(self,player,n=1):
        """
        Args:palyer,n（发牌的数量）
        Returns:None
        """
        cards = []
        for _ in range(n):
            if self.card_q.empty():
                self._info("\n发牌器没有牌了，整理废牌，重新洗牌；")
                shuffle(self.cards_in_pool)
                self._info("一共整理了{}张已用的牌，重新放入发牌器\n".format(len(self.cards_in_pool)))
                assert(len(self.cards_in_pool)>20)
                """
                确保一次能收集较多的牌
                代码编写不合理的时候，会出现玩家超出21但是仍然继续叫牌的情况
                导致玩家手中牌很多但是发牌器和已经使用的牌很少，避免这种情况
                """
                self.load_cards(self.cards_in_pool)
            cards.append(self.card_q.get())
        self._info("发了{}张牌({})给{}{};".format(n,cards,player.role,player))
        player.receive(cards)
        player.cards_info()
    #辅助函数，进行信息输出
    def _info(self,message):
        if self.display:
            print(message,end="")

    def recycle_cards(self,*players):
        """
        回收牌加入cards_in_pool
        """
        if len(players) == 0:
            return 
        for player in players:
            for card in player.cards:
                self.cards_in_pool.append(card)
            player.discharge_cards()
    
    
    def play_game(self,dealer,player):
        """
        完成一次对局
        Args:庄家和玩家
        Returns:
        tuple(episode,reward)
        """
        self._info("="*10+"开始新一局"+"="*10)
        #没人先发两张牌
        self.serve_card_to(dealer,n=2)
        self.serve_card_to(player,n=2)
        episode = []
        if player.policy is None:
            self._info("玩家需要一个策略")
            return 
        if dealer.policy is None:
            self._info("庄家需要一个策略")
            return 
        while True:
            #玩家进行叫牌
            action = player.policy(dealer)
            self._info("{}{}选择：{}；".format(player.role,player,action))
            #将其加入轨迹,形式为(s,a)
            episode.append((player.get_state_name(dealer),action))
            if action == self.A[0]:     #继续叫牌
                self.serve_card_to(player)
            else:
                break
        #对局面进行判断
        #如果玩家超过21点那么就结束游戏
        #否则庄家可以选择是否叫牌
        reward,player_points,dealer_points,useable_ace = self.reward_of(dealer,player)
        if player_points > 21:
            self._info("玩家爆点{}输了，得分{}\n".format(player_points,reward))
            self.recycle_cards(dealer,player)
            #将轨迹进行储存，包括轨迹和回报
            #MC预测和控制的时候其实不用储存轨迹的list，可以累计状态的回报和次数，或者使用
            #增量式的MC
            self.episodes.append((episode,reward))
            self._info("="*10+"本局结束"+"="*10+"\n")
            return episode,reward

        self._info("\n")
        while True:
            action = dealer.policy()
            self._info("{}{}选择：{}".format(dealer.role,dealer,action))
            if action == self.A[0]:
                self.serve_card_to(dealer)
            else:
                break   
        #双方都停止叫牌
        self._info("\n双方都停止叫牌；\n")
        reward,player_points,dealer_points,useable_ace = self.reward_of(dealer,player)
        player.cards_info()
        dealer.cards_info()
        if reward == 1:
            self._info("玩家赢了！")
        elif reward == -1:
            self._info("玩家输了！")
        else:
            self._info("双方和局！")
        self._info("玩家{}点，庄家{}点\n".format(player_points,dealer_points))
        self._info("="*10+"本局结束"+"="*10+"\n")
        self.recycle_cards(player,dealer)
        #可以看出episode存的是player的，所以这是对palyer的策略进行评估与控制
        self.episodes.append((episode,reward))
        return episode,reward

    #生成多个对局
    def play_games(self,dealer,player,num = 2,show_statistic = True):
        #玩家负、和、胜的次数
        results = [0,0,0]
        self.episodes.clear()
        #进度条显示的写法借鉴
        for i in tqdm(range(num)):
            episode,reward = self.play_game(dealer,player)
            results[1+reward] += 1
            if player.learning_method is not None:
                #递增式学习
                player.learning_method(episode,reward)
        if show_statistic:
            print("总共{}局，玩家赢了{}局，和了{}局，输了{}局，胜率：{:.2f}\n".format(num,results[2],results[1],results[0],results[2]/num))
    
    def _info(self,msg):
        if self.display:
            print(msg,end="")
