# src/bidding/contract.py
# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional

class Contract(NamedTuple):
    level: int      # 阶数 (1-7)
    denom: str       # 花色 (C/D/H/S/NT)
    doubled: Optional[str] = None    # 加倍状态 (空=未加倍, "x"=X, "xx"=XX)

def final_contract(auction: list[str]) -> Contract:
    """从叫牌序列解析最终定约"""
    last_bid = next((b for b in reversed(auction) if b not in ['Pass', 'X', 'XX']), None)
    if not last_bid:
        return None  # 全Pass情况
    
    # 花色提取
    level = int(last_bid[0])
    denom = last_bid[1:].upper()

    # 检查加倍状态
    doubled = None
    check_double = auction[-4]
    if check_double=='XX':
        doubled = "xx"
    elif check_double=='X':
        doubled = "x"

    
    return Contract(level, denom, doubled)