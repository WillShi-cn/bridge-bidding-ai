# src.deals.generator.py
# -*- coding: utf-8 -*-

from endplay import Deal
from typing import Dict

def generate_random_deal() -> Dict[str, str]:
    """Generate random bridge deal with string representation"""
    deal = Deal()
    deal.shuffle()
    return {
        'north': deal.north.str(),  # Convert to string
        'east': deal.east.str(),
        'south': deal.south.str(),
        'west': deal.west.str()
    }

# deal.north 什么意思？