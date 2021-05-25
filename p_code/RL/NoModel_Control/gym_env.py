"""
author:龚俊老婆
参考：叶强大佬
date:2021-5-23
Gym环境库的核心代码介绍
"""

"""
gym库提供了一整套编程接口和丰富的强化学习环境，同时还提供了可视化功能，方便观察个体的训练结果。
库的核心在文件core.py中，定义了两个最基本的累Env（所有环境的基类）和Space（空间类的基类）。
Space衍生出的类主要包括Discrete类（离散空间）和Box类（多维连续空间），可以用在行为空间，也可描述状态空间
"""
class Env(object):
    #子类需要设置的属性
    action_space = None
    observation_space = None

    #需要重载的方法
    #环境动力学，只能返回三个元素的list，如果多于三个，可以使用tuple进行封装
    def step(self,action):raise NotImplementedError
    #状态的初始化
    def reset(self):raise NotImplementedError
    #可视化方法
    def reset(self,mode='human',close = False):return
    #设置随机数种子
    def seed(self,seed=None):return []

    #其中render的使用过程为：
    """
    首先得到viewer对象，在一个viewer里绘制一个几何图像的步骤为：
    （1）建立该对象需要的数据
    （2）使用rendering提供的方法返回一个geom对象
    （3）对geom对象进行一些对象颜色、线宽、线型、变换属性的设置，其中变换属性比较重要：
    该属性负责对对象在屏幕中的位置、渲染、缩放进行渲染，如果某对象在呈现时可能发生上述变化，
    则应该建立关于该对象的变换属性。该属性是一个Transform对象，而一个Transform对象，包括
    translate\rotate\scale三个属性，每个属性都由以np.array对象描述的矩阵决定。
    （4）将新建立的geom对象添加至viewer的绘制对象列表中，如果在屏幕上只出现一次，将其加入
    到add_onegeom()列表中，如果需要多次渲染，则将其加入add_geom()
    （5）在渲染整个viewer之前，对有需要的geom的参数进行修改，修改主要基于该对象的Transform对象
    （6）调用viewer的render()方法进行绘制
    """

