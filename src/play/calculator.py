# src/play/calculator.py
# -*- coding: utf-8 -*-

from endplay.types import Deal, Vul, Player, Denom, Contract
from endplay.dds import par, calc_dd_table
from endplay import config

# 全局设置不使用 Unicode 花色符号
config.use_unicode = False

class DDSCalculator:
    # 创建 Denom 的映射字典
    DENOM_MAPPING = {
        'S': Denom.spades,
        'H': Denom.hearts,
        'D': Denom.diamonds,
        'C': Denom.clubs,
        'NT': Denom.nt
    }

    # 创建 Player 的映射字典
    PLAYER_MAPPING = {
        'N': Player.north,
        'E': Player.east,
        'S': Player.south,
        'W': Player.west
    }
    
    # 创建 Vul 的映射字典
    VUL_MAPPING = {
        'none': Vul.none,
        'ns': Vul.ns,
        'ew': Vul.ew,
        'both': Vul.both
    }

    def _int_to_str(num):
        if num > 0:
            return f"+{num}"
        elif num < 0:
            return str(num)
        else:
            return "="

    # 计算给定定约的得分
    def calculate_score(self, deal, contract, vul, player):
        table = calc_dd_table(deal)    
        tricks = self._int_to_str(table[self.DENOM_MAPPING[contract.denom], self.DENOM_MAPPING[player]] - 6)
        doubled_str = contract.doubled if contract.doubled else ''
        contract_str = f"{contract.level}{contract.denom}{player}{doubled_str}{tricks}"
        c = Contract(contract_str)
        return c.score(self.VUL_MAPPING[vul])

    # 计算最优得分
    def calculate_target_score(self, deal, vul, player):
        table = calc_dd_table(deal)
        par_list = list(par(table, self.VUL_MAPPING[vul], self.PLAYER_MAPPING[player]))
        c = Contract(str(par_list[0]))
        return c.score(self.VUL_MAPPING[vul])
