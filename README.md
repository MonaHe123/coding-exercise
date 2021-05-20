# coding-exercise
@[TOC](daily coding exercise)
# reference
一些练习过程中遇到的有用的参考链接
# p_code
coding in python
## RL
### MDP
马尔可夫过程相关代码练习
#### 基于模型的预测和控制
#### simple_gridworld.py
简单4*4格子世界，到达目标点的时候得到奖励1，其余状态得到的奖励为-1。
使用MDP建模，模型已知。
实现的功能：
（1）、动态规划实现策略评估
（2）、价值迭代求解最优策略
（3）、策略迭代求解最优策略

#### 不基于模型的预测
#### （1）MC_blackjack_predict.py，基于MC实现策略评估
##### 21点游戏：
一个玩家一个庄家，游戏规则为：
（1）、开始时玩家和庄家各得两张牌，庄家的一张牌公开
（2）、此后每一轮玩家可以不断进行叫牌，如果玩家停止叫牌，庄家再决定要不要叫牌
（3）、双方都停止叫牌后，谁的点数小于21并且接近21那么获胜，否则平局
##### 建模：S,A,R,P,gamma
（1）、S：玩家和庄家都抽象为游戏参与者，状态包括：庄家公开牌面、当前的总点数、是否有A
（2）、A：叫牌和不叫牌
（3）、R：过程中任意状态奖励为0，结束时获胜则为1，平局为0，输则为-1
（4）、P：转移概率难以确定
（5）、gamma：基于MC的策略评估，所以需要确定的是学习率，不是衰减因子
##### 代码实现
对基本的模型进行讨论之后，考虑代码的具体实现，需要实现的部分包括：
游戏参与者：自身状态，可进行叫牌以及牌清空的操作，辅助函数输出自己的信息
庄家：基于游戏参与者，展示第一张牌，采取的策略
玩家：基于游戏参与者，获得庄家第一张牌的信息，采取的策略
游戏管理者：牌、洗牌、发牌、判断输赢、回收、实现一次对局
策略评估：MC，递增式MC

#### 不基于模型的控制
#### （1）MC_blackjack_control.py，基于MC的模型控制
utils.py中的epsilon_greedy_policy的实现示意图：
![pic]()
#### （2）


# c_code
coding in c/c++
## leetcode_exercise
### 21_5
21年五月完成练习集合
