# src/deals/generator.py
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from endplay.dealer.generate import generate_deal
from endplay.types import Deal
from typing import Dict, Optional, List
from ..counters import global_counter
import random
import threading
from .validator import Validator

class DealBundle:
    uuid: str = None            # 唯一标识
    deal: Deal
    vul: str                    # 局况 ('none', 'ns', 'ew', 'both')
    opener: str                 # 开叫人位置 ('N', 'E', 'S', 'W')

class Registry:
    """全局牌局注册表单例类（线程安全）"""
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance._data: Dict[str, 'DealBundle'] = {}
                cls._instance._lock = threading.Lock()
            return cls._instance
    
    def add(self, bundle: 'DealBundle'):
        with self._lock:
            self._data[bundle.uuid] = bundle
            
    def get(self, uuid: str) -> Optional['DealBundle']:
        with self._lock:
            return self._data.get(uuid)
    
    def list_all(self) -> List['DealBundle']:
        with self._lock:
            return list(self._data.values())
    
    def count(self) -> int:
        with self._lock:
            return len(self._data)

# 初始化全局注册表
deal_registry = Registry()

class DealGenerator:
    def __init__(self):
        self.vul_rotation = ['none', 'ns', 'ew', 'both']    # 标准局况轮转
        self.opener_rotation = ['N', 'E', 'S', 'W']         # 开叫人轮转
        self.validator = Validator()

    def generate_bundle(self, qty = 1) -> Optional[DealBundle]:
        """生成完整牌局包"""
        bundle = None
        for _ in range(qty):
            for _ in range(1000):
                try:
                    deal: Deal = generate_deal()
                    if self.validator.validate(deal):
                        vul = random.choice(self.vul_rotation)
                        opener = random.choice(self.opener_rotation)
                        seq_id = global_counter.get_next()  # 自动取号
                        uuid = f"D{seq_id:08d}"      # 生成唯一ID（例如D00001001）
                        bundle = DealBundle(uuid=uuid, deal=deal, vul=vul, opener=opener)
                        deal_registry.add(bundle)
                        break  # 跳出内层循环，继续生成下一个牌局包
                except Exception as e:
                    print(f"An error occurred: {e}")
        return bundle

"""
# 外部访问示例
from src.deals.generator import deal_registry

# 获取所有牌局
all_deals = deal_registry.list_all()

# 按ID查询
specific_deal = deal_registry.get("D00000001")

# 统计总数
total_deals = deal_registry.count()
"""