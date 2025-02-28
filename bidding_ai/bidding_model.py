# 
# -*- coding: utf-8 -*-

# 深度强化学习模型
import torch
import torch.nn as nn
from torch.distributions import Categorical

class BiddingPolicyNetwork(nn.Module):
    def __init__(self, input_dim=128, hidden_dim=256, output_dim=38):
        super().__init__()
        # 输入：手牌特征(32)+叫牌历史(96)
        self.lstm = nn.LSTM(input_dim, hidden_dim, batch_first=True)
        self.policy = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)  # 对应35种叫牌+Pass/Double/Redouble
        )
        self.value = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )
    
    def forward(self, x, hidden=None):
        lstm_out, hidden = self.lstm(x, hidden)
        action_logits = self.policy(lstm_out[:, -1, :])
        state_value = self.value(lstm_out[:, -1, :])
        return action_logits, state_value, hidden

