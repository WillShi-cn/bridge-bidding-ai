# src/deals/generator.py
# -*- coding: utf-8 -*-

from endplay.dealer.generate import generate_deal
from endplay.types import Deal

# 随机生成一副牌
deal = generate_deal()
print(deal)