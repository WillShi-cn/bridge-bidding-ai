# src/rules/rule.py
# -*- coding: utf-8 -*-

class BiddingRuleEngine:
    # 二分为普通叫品和特殊叫品
    CONTRACT_BID_RANK = {
        '1C':1, '1D':2, '1H':3, '1S':4, '1NT':5,
        '2C':6, '2D':7, '2H':8, '2S':9, '2NT':10,
        '3C':11, '3D':12, '3H':13, '3S':14, '3NT':15,
        '4C':16, '4D':17, '4H':18, '4S':19, '4NT':20,
        '5C':21, '5D':22, '5H':23, '5S':24, '5NT':25,
        '6C':26, '6D':27, '6H':28, '6S':29, '6NT':30,
        '7C':31, '7D':32, '7H':33, '7S':34, '7NT':35
    }
    SPECIAL_BID_RANK = {'Pass':0, 'X':1, 'XX':2}

    def is_valid_bid(self, auction, new_bid):
        """Validate bid legality according to bridge rules"""
        # Pass永远合法
        if new_bid == 'Pass':
            return True
        
        reversed_auction = list(reversed(auction))
        
        # Handle ordinary bids
        if new_bid not in self.SPECIAL_BID_RANK:
            last_ordinary = next(
                (b for b in reversed_auction if b not in self.SPECIAL_BID_RANK),
                None
            )
            return (last_ordinary is None) or (
                self.CONTRACT_BID_RANK[new_bid] > self.CONTRACT_BID_RANK[last_ordinary]
            )
        
        # Handle special bids (X/XX)
        last_non_pass = next((b for b in reversed_auction if b != 'Pass'), None)
        if last_non_pass is None:
            return False
        
        if reversed_auction.index(last_non_pass) % 2 == 1:
            return False
        
        if new_bid == 'XX':
            return last_non_pass == 'X'
        return last_non_pass not in self.SPECIAL_BID_RANK
