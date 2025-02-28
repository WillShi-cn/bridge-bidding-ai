# src/counters.py
# -*- coding: utf-8 -*-

import threading

class AtomicCounter:
    """线程安全全局计数器"""
    def __init__(self, initial=0):
        self.value = initial
        self._lock = threading.Lock()
    
    def increment(self) -> int:
        with self._lock:
            self.value += 1
            return self.value

# 初始化全局计数器实例
global_counter = AtomicCounter(initial=0)  # 从0开始计数
