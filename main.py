"""
主函数
"""
from logger import logger
from model import generate_c_k_plus_1, generate_l_k, count_freq, find_frequent_patterns, calculate_association_rules, generate_association_rules
from data_loader import load_data
import argparse
import time


def dummy_apriori(itemset, c_ks, support, num):
    all_lks = []
    all_sps = []
    counter = count_freq(itemset)

    def apriori(itemset, c_k, support):
        l_ks, sp_s, itemset = generate_l_k(itemset, c_k, support, num, counter)
        all_lks.extend(l_ks)
        all_sps.extend(sp_s)
        if len(l_ks) > 1:
            ck_plus_1s = generate_c_k_plus_1(l_ks)
            apriori(itemset, ck_plus_1s, support)

    apriori(itemset, c_ks, support)

    return all_lks, all_sps


def advanced_apriori1(itemset, c_ks, support, num):
    all_lks = []
    all_sps = []
    counter = count_freq(itemset)

    def apriori(itemset, c_k, support):
        l_ks, sp_s, itemset = generate_l_k(itemset, c_k, support, num, counter)
        all_lks.extend(l_ks)
        all_sps.extend(sp_s)
        if len(l_ks) > 1:
            ck_plus_1s = generate_c_k_plus_1(l_ks)
            # 类间排序
            ck_plus_1s = sorted(ck_plus_1s)
            apriori(itemset, ck_plus_1s, support)

    apriori(itemset, c_ks, support)

    return all_lks, all_sps


def advanced_apriori3(itemset, c_ks, support, num):
    all_lks = []
    all_sps = []
    counter = count_freq(itemset)

    def apriori(itemset, c_k, support):
        l_ks, sp_s, itemset = generate_l_k(
            itemset, c_k, support, num, counter, trick='trick_3')
        all_lks.extend(l_ks)
        all_sps.extend(sp_s)
        if len(l_ks) > 1 and len(itemset) > 0:
            ck_plus_1s = generate_c_k_plus_1(l_ks)
            apriori(itemset, ck_plus_1s, support)

    apriori(itemset, c_ks, support)

    return all_lks, all_sps


def advanced_apriori2(itemset, c_ks, support, num):
    all_lks = []
    all_sps = []
    counter = count_freq(itemset)

    def apriori(itemset, c_k, support):
        l_ks, sp_s, itemset = generate_l_k(
            itemset, c_k, support, num, counter, trick='trick_2')
        all_lks.extend(l_ks)
        all_sps.extend(sp_s)
        if len(l_ks) > 1 and len(itemset) > 0:
            ck_plus_1s = generate_c_k_plus_1(l_ks)
            apriori(itemset, ck_plus_1s, support)

    apriori(itemset, c_ks, support)

    return all_lks, all_sps


def main(args):
    support = args.support
    itemset, c_ks = load_data(args.path)
    num = len(itemset)
    logger.info(f'Using algorithm {args.ty}')
    start = time.time()
    if args.ty == 'dummy':
        all_lks, all_sps = dummy_apriori(itemset, c_ks, support, num)
    elif args.ty == 'apriori1':
        all_lks, all_sps = advanced_apriori1(itemset, c_ks, support, num)
    elif args.ty == 'apriori2':
        all_lks, all_sps = advanced_apriori2(itemset, c_ks, support, num)
    elif args.ty == 'apriori3':
        all_lks, all_sps = advanced_apriori3(itemset, c_ks, support, num)
    elif args.ty == 'fpgrowth':
        all_lks = find_frequent_patterns(itemset, support)
        all_sps = []
    else:
        raise(
            f"Not support algorithm {args.ty}, Please choose from [`dummy`,`apriori1`,`apriori2`,`apriori3`]")
    interval = time.time() - start
    logger.info(f"finish algorithm with {interval}")
    return all_lks, all_sps, interval


def get_k_set(all_lks, k=3):
    l_set = []
    for lk in all_lks:
        if len(lk) == k:
            l_set.append(lk)
    return l_set


def get_association_rules(all_lks, all_sps, confidence, model='fp'):
    if model == 'fpgrowth':
        return generate_association_rules(all_lks, confidence)
    elif model == 'apriori':
        return calculate_association_rules(all_lks, all_sps, confidence)
    else:
        raise(
            f"Not support algorithm {model}, Please choose from [`fp`,`apriori`]")


def opt():
    parser = argparse.ArgumentParser(
        description='The association rule mining')
    parser.add_argument('-support', type=float,
                        default=0.01, help='The support rate')
    parser.add_argument('-confidence', type=float,
                        default=0.5, help='The confidence rate')
    parser.add_argument('-k', type=int, default=3,
                        help='The size of k_item_freq')
    parser.add_argument('-path', type=str,
                        default='./data/Groceries.csv',
                        help='The path of dataset')
    parser.add_argument('-ty', type=str,
                        default='dummy',
                        help='The type of algorithm, must be one of [`dummy`,`apriori1`,`apriori2`,`apriori3`,`fp`]')
    args = parser.parse_args()
    if args.ty == 'fpgrowth':
        args.model = 'fpgrowth'
    else:
        args.model = 'apriori'
    return args


if __name__ == "__main__":
    args = opt()
    all_lks, all_sps, interval = main(args)
    k_set = get_k_set(all_lks, k=args.k)
    print(len(all_lks), len(k_set), k_set)
    rules = get_association_rules(
        all_lks, all_sps, args.confidence, model=args.model)
    print(len(rules), rules)
