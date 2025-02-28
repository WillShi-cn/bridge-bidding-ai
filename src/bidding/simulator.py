# src.bidding.simulator.py
# -*- coding: utf-8 -*-

from typing import List, Dict
from src.bidding.rule import BiddingRuleEngine

class BiddingSimulator:
    def __init__(self, rule_engine: BiddingRuleEngine):
        self.rule_engine = rule_engine
        
    def simulate(self, deal: Dict) -> List[str]:
        """Simulate complete bidding process"""
        auction = []
        while not self._is_auction_ended(auction):
            bid = self._generate_bid(auction, deal)
            if not self.rule_engine.is_valid_bid(auction, bid):
                raise ValueError(f"Illegal bid generated: {bid}")
            auction.append(bid)
        return auction
    
    def _is_auction_ended(self, auction: List[str]) -> bool:
        """Check auction termination conditions"""
        if not auction or auction[-1] != 'Pass' or auction[-2] != 'Pass' or auction[-3] != 'Pass':
            return False
        return len(auction) >= 4
    
    def _generate_bid(self, auction: List[str], deal: Dict) -> str:
        """Generate next bid (AI placeholder)"""
        # TODO: Implement AI logic
        return 'Pass'
