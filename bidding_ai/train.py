# 
# -*- coding: utf-8 -*-

# 训练流程
class BiddingTrainer:
    def __init__(self, model, rule_checker):
        self.model = model
        self.optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
        self.rule_checker = rule_checker
        
    def simulate_bidding(self, deal_data):
        """与规则模块协同的模拟叫牌过程"""
        state = self._extract_state(deal_data)
        bidding_history = []
        
        while not self.rule_checker.bidding_ended(bidding_history):
            action_logits, value, _ = self.model(state)
            action_dist = Categorical(logits=action_logits)
            action = action_dist.sample()
            
            if self.rule_checker.is_valid_bid(action.item(), bidding_history):
                bidding_history.append(action.item())
            else:
                # 无效叫牌惩罚
                ...
        
        contract = self.rule_checker.determine_contract(bidding_history)
        return contract, self._calculate_reward(contract, deal_data)

    def _calculate_reward(self, contract, deal_data):
        """调用打牌模块计算奖励"""
        declarer_score = simulate_play(deal_data, contract)  # 对接现有打牌模块
        vulnerability = deal_data['vulnerability']
        return calculate_imps(declarer_score, vulnerability)  # 对接规则模块
