""" 
加载数据
"""
from tqdm import tqdm
from logger import logger


def load_data(path='./data/Groceries.csv'):
    r""" 
    load info from origin data
    generate the itemset and c_1.
    """
    itemset = []
    goods = {}
    with open(path, 'r') as f:
        for i, line in tqdm(enumerate(f.readlines())):
            if i == 0:
                continue
            words = line.replace('{', '').replace('}', '').replace(
                '"', '').strip().split(',')[1:]
            item = {}
            if len(words) > 0:
                for word in words:
                    word = word.replace(' ', '').replace('/', '')
                    goods[word] = 1
                    item[word] = 1
                itemset.append(item)
    c_1 = []
    for word in list(goods.keys()):
        c_1.append(set([word]))
    return itemset, c_1


if __name__ == '__main__':
    itemset, c_1 = load_data()
    logger.info(c_1)
