from endplay import Contract
from endplay.types import Deal, Vul, Player, denom
from endplay.dds import par, calc_dd_table
from endplay import config
from endplay.types import Denom

# 全局设置不使用 Unicode 花色符号
config.use_unicode = False

# 创建一个 Deal 对象
d = Deal("N:AKQJ8..AT8632.43 T742.Q9543.J.QT8 63.AJT8.97.J7652 95.K762.KQ54.AK9")
table = calc_dd_table(d)
par_list = list(par(table, Vul.ew, Player.north))
print(par_list[0])
c = Contract(str(par_list[0]))
print(c)
score = c.score(Vul.ew)
print(score)

c = table[Denom.clubs, Player.north]
print(c)
"""

d = Deal("N:J976..762.KQJ982 K5.JT9843.AK93.A AT42.765.J84.T54 Q83.AKQ2.QT5.763")
parlist = par(d, Vul.ew, Player.north)
# 输出最优定约的得分
print(parlist.score)  
print(Vul.ew)
print(Player.north)
"""
"""
c = Contract("4NTSxx+1")
print(c)
print(c.penalty)
print(c.score)





class Contract:
    "Class representing a specific contract"
    _pat = re.compile(
        r"^([1-7])((?:NT?)|S|H|D|C)([NSEW]?)((?:XX|X|D|R)?)((?:=|(?:[+-]\d+))?)$"
    )

    def __init__(
        self,
        data: Union[_dds.contractType, str, None] = None,
        *,
        level: Optional[int] = None,
        denom: Optional[Denom] = None,
        declarer: Optional[Player] = None,
        penalty: Optional[Penalty] = None,
        result: Optional[int] = None,
    ):
        
        
"""


# 创建一个牌局对象
d = Deal("QJ8.AJ965.K82.AQ 43.QT87.QT64.754 AKT9..A97.J98632 7652.K432.J53.KT")
