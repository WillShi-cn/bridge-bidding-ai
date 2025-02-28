# bridge-bidding/src/deals/probability_cache.py
# -*- coding: utf-8 -*-

import pickle
import os
from collections import defaultdict
from math import comb
from itertools import product

# 定义保存结果的文件路径
SHAPE_FILE = 'normal_shapes.pkl'
HCP_FILE = 'normal_hcps.pkl'

def get_normal_shapes():
    # 检查文件是否存在
    if os.path.exists(SHAPE_FILE):
        with open(SHAPE_FILE, 'rb') as file:
            normal_shapes = pickle.load(file)
            return normal_shapes
    
    # 计算从 52 张牌中选 13 张牌的总组合数
    total_shape_combs = comb(52, 13)

    # 用于存储所有分法及其概率的字典
    shape_probs = defaultdict(float)

    # 枚举所有可能的分法 
    for x1 in range(14):
        for x2 in range(14 - x1):
            for x3 in range(14 - x1 - x2):
                x4 = 13 - x1 - x2 - x3
                # 计算当前分法的组合数
                combs = comb(13, x1) * comb(13, x2) * comb(13, x3) * comb(13, x4)
                # 计算当前分法的概率
                prob = combs / total_shape_combs
                # 将分法及其概率存储到字典中
                sorted_x = tuple(sorted([x1, x2, x3, x4],reverse=True))
                shape_probs[sorted_x] += prob

    # 对概率字典按照概率从高到低排序
    sorted_shape_probs = sorted(shape_probs.items(), key=lambda item: item[1], reverse=True)

    # 用于存储累计概率达到 99.9% 的牌型及其概率的字典
    normal_shapes = {}
    cumulative_prob = 0

    # 遍历排序后的元素，计算累计概率并选择满足条件的牌型
    for distribution, prob in sorted_shape_probs:
        cumulative_prob += prob
        normal_shapes[distribution] = prob
        if cumulative_prob >= 0.999:
            break

    with open(SHAPE_FILE, 'wb') as file:
        pickle.dump(normal_shapes, file)

    return normal_shapes


def get_normal_hcps():
    # 检查文件是否存在
    if os.path.exists(HCP_FILE):
        with open(HCP_FILE, 'rb') as file:
            normal_hcps = pickle.load(file)
            return normal_hcps
    
    # 计算从 52 张牌中选 13 张牌的总组合数
    total_combs = comb(52, 13)

    # 用于存储每种大牌点出现的组合数
    hcp_combs = defaultdict(int)

    # 定义每个花色的 A、K、Q、J 的点数
    high_card_points = [4, 3, 2, 1]

    # 生成所有可能的大牌选取情况
    all_high_card_choices = product([0, 1], repeat=16)

    for choice in all_high_card_choices:
        # 计算当前选取的大牌数量
        high_cards_selected = sum(choice)
        if high_cards_selected > 13:
            continue  # 排除总牌数大于 13 张的情况

        # 计算当前大牌点
        hcp = sum([point * card for point, card in zip(high_card_points * 4, choice)])

        # 计算剩余普通牌的组合数
        remaining_combs = comb(52 - 16, 13 - high_cards_selected)

        # 累加当前大牌点的组合数
        hcp_combs[hcp] += remaining_combs

    # 用于存储每种大牌点出现的概率
    hcp_probs = {}
    for hcp, combs in hcp_combs.items():
        # 计算每种大牌点出现的概率
        hcp_probs[hcp] = combs / total_combs

    # 对大牌点按出现概率从高到低排序
    sorted_hcp_probs = sorted(hcp_probs.items(), key=lambda item: item[1], reverse=True)

    # 用于存储累计概率达到 99.9% 的大牌点情况
    cumulative_prob = 0
    normal_hcps = {}
    for hcp, prob in sorted_hcp_probs:
        cumulative_prob += prob
        normal_hcps[hcp] = prob
        if cumulative_prob >= 0.999:
            break

    with open(HCP_FILE, 'wb') as file:
        pickle.dump(normal_hcps, file)

    return normal_hcps

NORMAL_SHAPES = get_normal_shapes()
NORMAL_HCPS = get_normal_hcps()