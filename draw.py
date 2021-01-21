import matplotlib.pyplot as plt


def draw(times, algorithms, name):
    x = range(len(times))
    rects1 = plt.bar(x, height=times, width=0.4, alpha=0.8,
                     color='red')
    plt.ylim(0, 130)     # y轴取值范围
    plt.ylabel(name)
    plt.xticks([index + 0.2 for index in x], algorithms)
    plt.xlabel("Algorithm")
    plt.title("")
    plt.legend()     # 设置题注

    # 编辑文本
    for rect in rects1:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height,
                 str(height), ha="center", va="bottom")

    plt.savefig(f'{name}.png')
    # plt.show()


if __name__ == '__main__':
    times = [110.9324722290039, 112.84710025787354,
             71.55795574188232, 106.52765893936157]
    algorithms = ['dummy_apriori', 'apriori1',
                  'apriori2', 'apriori3', 'fpgrowth']
    draw(times, algorithms[:4], 'time')
    memories = [39.012, 39.062, 39.027, 38.992, 39.031]
    draw(memories, algorithms, 'memory')
