# src.play.calculator.py
# -*- coding: utf-8 -*-

from endplay import dds

class DDSCalculator:
    def calculate_score(self, deal, contract):
        """计算给定定约的得分"""
        solver = dds.SolveAllPBN()
        solver.solve(deal.to_pbn(), declarer=contract.declarer, trump=contract.trump)
        return solver.data.score
