# src/deals/generator.py
# -*- coding: utf-8 -*-

from endplay.evaluate import hcp, shape

def evaluate_north_hand(deal):
    h = hcp(deal.north)
    s = tuple(shape(deal.north))
    return h, s
