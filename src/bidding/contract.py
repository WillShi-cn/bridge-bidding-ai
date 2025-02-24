# src.bidding.contract.py
# -*- coding: utf-8 -*-

from typing import NamedTuple

class Contract(NamedTuple):
    level: int      # 阶数 (1-7)
    suit: str       # 花色 (C/D/H/S/NT)
    declarer: str   # 庄家方位 (N/E/S/W)
    doubled: int    # 加倍状态 (0=未加倍, 1=X, 2=XX)

def parse_final_contract(auction: list[str], dealer: str) -> Contract:
    """从叫牌序列解析最终定约"""
    last_bid = next((b for b in reversed(auction) if b not in ['Pass', 'X', 'XX']), None)
    if not last_bid:
        return None  # 全Pass情况
    
    # 花色提取
    level = int(last_bid[0])
    suit = last_bid[1:].upper()
    
    # 检查加倍状态
    doubled = 0
    check_double = auction[-4]
    if check_double=='XX':
        doubled = 2
    elif check_double=='X':
        doubled = 1        
       
    # 确定庄家（第一个叫出该定约的玩家）
    positions = ['N', 'E', 'S', 'W']
    declarer = positions[(positions.index(dealer.upper()) + auction.index(last_bid)) % 4]    
    
    return Contract(level, suit, declarer, doubled)
