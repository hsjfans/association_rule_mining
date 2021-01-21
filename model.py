"""
模型
"""
from logger import logger
from tqdm import tqdm
import copy
import pyfpgrowth
from itertools import combinations


def trick_2(all_record_nums, itemset, k):
    """
    trick_2: 减小事务表(数据记录表)规模。

    """
    dataset = []
    for record_num, item in zip(all_record_nums, itemset):
        if record_num > k:
            dataset.append(item)
    logger.info(f"before: {len(itemset)}, after: {len(dataset)}")
    return dataset


def trick_3(counter, k, itemset):
    """
    trick_3 : 减少事务表中元组的项。

    Parameters
    ----------
    counter : [dict]
        每一个元素的词频
    k : [int]
        候选集元素的个数
    itemset : [list]
        事务表
    """
    dataset = []
    for item in itemset:
        elements = copy.deepcopy(item)
        for element in item.keys():
            if counter[element] <= k:
                del elements[element]
        if len(elements) > 0:
            dataset.append(elements)
    return dataset


def support_rate(itemset, c_k, num):
    """ support rate
    支持度
    itemset: 数据集
    c_k, the k-th 候选集
    """
    count = 0.0
    record_nums = [0 for _ in range(len(itemset))]
    for i, item in enumerate(itemset):
        hit = 0
        for c in c_k:
            if c in item:
                hit += 1
        if len(c_k) == hit:
            count += 1
            record_nums[i] = 1
    return count / num, record_nums


# def confidence_rate(itemset, A, B):
#     """ confidence rate
#     置信度
#     """
#     pass


def generate_c_k_plus_1(l_ks):
    """ generate C_{k+1} 候选集
    l_ks: a set of c_k
    """
    c_k_plus_1s = {}
    for i in tqdm(range(0, len(l_ks)),
                  desc=f'Generate the c_k_plus_1 {len(l_ks[0])+1} dataset', mininterval=0.1):
        for j in range(i + 1, len(l_ks)):
            # 去重复
            item = sorted(l_ks[i].union(l_ks[j]))
            c_k_plus_1s[tuple(item)] = 1
    logger.info(f'get the c_k+1 {len(l_ks[0])+1}:{len(c_k_plus_1s)}')
    return [set(c_k_1) for c_k_1 in list(c_k_plus_1s.keys())]


def generate_l_k(itemset, c_ks, support, num, counter, trick=None):
    """ Generate l_k from c_k
    trick: trick or not
    """
    l_k = []
    sp_s = []
    k = len(c_ks[0])
    desc = f'Generate l_k k={k}'
    all_record_nums = [0 for _ in range(len(itemset))]
    for c_k in tqdm(c_ks, desc=desc, mininterval=0.1):
        sp, record_nums = support_rate(itemset, c_k, num)
        for i in range(len(record_nums)):
            all_record_nums[i] += record_nums[i]
        if sp > support:
            l_k.append(c_k)
            sp_s.append(sp)

    # Advanced aprorio 2 filter
    if trick is None:
        logger.info('dummy algorithm')
    elif trick == 'trick_2':
        itemset = trick_2(all_record_nums, itemset, k)
    elif trick == 'trick_3':
        itemset = trick_3(counter, k, itemset)

    logger.info(f' get l_k len:{len(l_k)} ')
    return l_k, sp_s, itemset


def count_freq(itemset):
    """ Count freq of item in itemset
    itemset: dataset
    """
    counter = {}
    for item in tqdm(itemset):
        for record in item:
            if record in counter:
                counter[record] += 1
            else:
                counter[record] = 1

    return counter


def find_frequent_patterns(itemset, support):
    dataset = []
    support = support * len(itemset)
    for item in tqdm(itemset):
        dataset.append(item.keys())
    return pyfpgrowth.find_frequent_patterns(dataset, support)


def generate_association_rules(patterns, rate):
    return pyfpgrowth.generate_association_rules(patterns, rate)


def calculate_association_rules(all_lks, all_sps, confidence):
    counter = {}

    # Step1. 将 list to map
    for lk, sp in tqdm(zip(all_lks, all_sps)):
        counter[tuple(sorted(lk))] = sp
    rules = []
    filters = {}
    for lk in tqdm(all_lks):
        # print(type(lk))
        for i in range(1, len(lk)):
            combines = list(combinations(lk, i))
            for a in combines:
                a_s = tuple(sorted(a))
                b = list(set(lk).difference(set(a)))
                b_s = tuple(sorted(b))
                key = tuple(sorted(lk))
                max_info = None
                max_confidence = 0
                if a_s in counter and (counter[key] / counter[a_s]) > confidence and (counter[key] / counter[a_s]) > max_confidence:
                    info = f'{a_s}:{b_s}, {(counter[key] / counter[a_s])}'
                    max_confidence = (counter[key] / counter[a_s])
                    if info not in filters:
                        max_info = info
                        filters[info] = 1
                if b_s in counter and (counter[key] / counter[b_s]) > confidence and (counter[key] / counter[b_s]) > max_confidence:
                    info = f'{b_s}:{a_s}, { (counter[key] / counter[b_s])}'
                    max_confidence = (counter[key] / counter[b_s])
                    if info not in filters:
                        max_info = info
                        filters[info] = 1
                if max_info is not None:
                    rules.append(max_info)
    return rules


if __name__ == '__main__':
    rules = calculate_association_rules([['1', '2', '3'], ['2', '3'], ['4'], ['5']],
                                        [3, 5, 4, 5],
                                        0.03)
    print(rules)
