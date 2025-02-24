# main.py
# -*- coding: utf-8 -*-

from src.rules.core import BiddingRuleEngine
from src.deals.generator import generate_random_deal
from src.bidding.simulator import BiddingSimulator

def print_deal(deal):
    """标准化牌局输出"""
    print("Generated Deal:".center(40, '='))
    for position in ['N', 'E', 'S', 'W']:
        print(f"{position.upper()}: {deal[position]}")

if __name__ == "__main__":
    rule_engine = BiddingRuleEngine()
    simulator = BiddingSimulator(rule_engine)

    # 生成测试牌局    
    test_deal = generate_random_deal()
    print_deal(test_deal)
    
    final_auction = simulator.simulate(test_deal)
    print("\nAuction Sequence:", " → ".join(final_auction))
