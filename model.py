"""
模型
"""
from logger import logger
from tqdm import tqdm


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


def confidence_rate(itemset, A, B):
    """ confidence rate
    置信度
    """
    pass


def generate_c_k_plus_1(l_ks):
    """ generate C_{k+1} 候选集
    l_ks: a set of c_k
    """
    c_k_plus_1s = {}
    for i in tqdm(range(0, len(l_ks)),
                  desc=f'Generate the c_k_plus_1 {len(l_ks[0])+1} dataset', mininterval=0.1):
        for j in range(i + 1, len(l_ks)):
            # 去重复
            c_k_plus_1s[tuple(l_ks[i].union(l_ks[j]))] = 1
    logger.info(f'get the c_k+1 {len(l_ks[0])+1}:{len(c_k_plus_1s)}')
    return [set(c_k_1) for c_k_1 in list(c_k_plus_1s.keys())]


def generate_l_k(itemset, c_ks, support, num, trick=False):
    """ Generate l_k from c_k
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
        if sp >= support:
            l_k.append(c_k)
            sp_s.append(sp)
        # else:
            # logger.info(
            #     f'c_k: {c_k}\'s support:{sp} lower of the support:{support}, filter it')

    # Advanced aprorio 2 filter
    if trick:
        dataset = []
        for record_num, item in zip(all_record_nums, itemset):
            if record_num > k:
                dataset.append(item)
        logger.info(f"before: {len(itemset)}, after: {len(dataset)}")
        itemset = dataset
    logger.info(f' get l_k len:{len(l_k)} ')
    return l_k, sp_s, itemset
