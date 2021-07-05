# 正负条形图
import matplotlib.pyplot as plt
import numpy as np

from sss.util import remove_edge

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def get_chart(right_labels, left_labels, y_labels):
    remove_edge(plt)
    a = np.array(right_labels)
    b = np.array(left_labels)
    #应要求关闭横坐标
    plt.xticks([])
    plt.yticks(range(len(right_labels)), y_labels)
    plt.title('原始分组合平均分-各校对比')
    rect_a = plt.barh(range(len(a)), a, color='#ED7C30', height=0.5)
    rect_b = plt.barh(range(len(b)), -b, color='#9DC3E7', height=0.5)
    # ncol 同一行显示2个图例,bbox_to_anchor 控制具体的位置 0表明底部，0.5表明中部，frameon去除边框
    plt.legend((rect_b, rect_a), ("语文+数学+外语+物理", "语文+数学+外语+历史"), bbox_to_anchor=(0.5, 1.02), frameon=False,
               loc='upper center', ncol=2)

    for x, y in enumerate(a):
        plt.text(0.8 * y, x, '%s' % y)
        # plt.ylim([0, str(y*2)])
    for m, n in enumerate(b):
        plt.text(-n * 0.9, m, '%s' % n)
    plt.show()


if __name__ == '__main__':
    #顺序从小到大排列
    right_labels = [290.3, 308.8, 361.2, 366.4, 367.7, 389.3]
    left_labels = [261.2, 278.3, 332.1, 335.7, 340.7, 364.3]
    y_labels = ['株洲市第八中学', '株洲市第四中学', '醴陵市第一中学', '浏阳市第一中学', '攸县第一中学', '株洲市第二中学']
    get_chart(right_labels, left_labels, y_labels)