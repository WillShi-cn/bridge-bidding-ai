# bridge-bidding/src/deals/validator.py
# -*- coding: utf-8 -*-

from probability_cache import NORMAL_SHAPES, NORMAL_HCPS
from evaluate import evaluate_north_hand
from collections import defaultdict

class Validator:
    def __init__(self):
        self.count = 0
        self.hcp_total = defaultdict(int)
        self.shape_total = defaultdict(int)
        # 提前构建反向映射字典
        self.hcp_index_map = {hcp: i + 1 for i, hcp in enumerate(NORMAL_HCPS.keys())}
        self.shape_index_map = {shape: i + 1 for i, shape in enumerate(NORMAL_SHAPES.keys())}
        self.indicator = 1.2

    def validate(self, hand):
        hcp, shape = evaluate_north_hand(hand)
        # 使用反向映射字典查找索引
        hcp_index = self.hcp_index_map.get(hcp, 0)
        shape_index = self.shape_index_map.get(shape, 0)

        # 牌型/大牌点的已有概率
        hcp_prob = self.hcp_total.get(hcp_index, 0) / (self.count + 1)
        shape_prob = self.shape_total.get(shape_index, 0) / (self.count + 1)
        
        if hcp_index == 0 or shape_index == 0:
            if self.count <= 1000:
                return False
            if (hcp_index == 0 and hcp_prob > 0.001) or (shape_index == 0 and shape_prob > 0.001):
                return False
        else:
            normal_hcp_prob = NORMAL_HCPS.get(hcp, 0)
            normal_shape_prob = NORMAL_SHAPES.get(shape, 0)
            if (hcp_prob > self.indicator * normal_hcp_prob) or (shape_prob > self.indicator * normal_shape_prob):
                return False
                
        self.count += 1
        self.shape_total [shape_index] = self.shape_total.get(shape_index, 0) + 1
        self.hcp_total [hcp_index] = self.hcp_total.get(hcp_index, 0) + 1
        return True
