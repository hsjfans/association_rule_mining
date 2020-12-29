"""
主函数
"""
from logger import logger
from model import generate_c_k_plus_1, generate_l_k
from data_loader import load_data
import argparse
import time


def dummy_apriori(itemset, c_ks, support, num):
    all_lks = []
    all_sps = []

    def apriori(itemset, c_k, support):
        l_ks, sp_s, itemset = generate_l_k(itemset, c_k, support, num)
        all_lks.extend(l_ks)
        all_sps.extend(sp_s)
        if len(l_ks) > 1:
            ck_plus_1s = generate_c_k_plus_1(l_ks)
            apriori(itemset, ck_plus_1s, support)

    apriori(itemset, c_ks, support)

    return all_lks, all_sps


def advanced_apriori1(itemset, c_ks, support, num):
    pass


def advanced_apriori3(itemset, c_ks, support, num):
    pass


def advanced_apriori2(itemset, c_ks, support, num):
    all_lks = []
    all_sps = []

    def apriori(itemset, c_k, support):
        l_ks, sp_s, itemset = generate_l_k(
            itemset, c_k, support, num, trick=True)
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
    else:
        raise(
            f"Not support algorithm {args.ty}, Please choose from [`dummy`,`apriori1`,`apriori2`,`apriori3`]")
    interval = time.time() - start
    return all_lks, all_sps, interval


def get_k_set(all_lks, k=3):
    l_set = []
    for lk in all_lks:
        if len(lk) == k:
            l_set.append(lk)
    return l_set


def opt():
    parser = argparse.ArgumentParser(
        description='The association rule mining')
    parser.add_argument('-support', type=float,
                        default=0.01, help='The support rate')
    parser.add_argument('-path', type=str,
                        default='./data/Groceries.csv',
                        help='The path of dataset')
    parser.add_argument('-ty', type=str,
                        default='dummy',
                        help='The type of algorithm, must be one of [`dummy`,`apriori1`,`apriori2`,`apriori3`]')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    all_lks, all_sps, interval = main(opt())
    k_set = get_k_set(all_lks, k=3)
    print(k_set)
