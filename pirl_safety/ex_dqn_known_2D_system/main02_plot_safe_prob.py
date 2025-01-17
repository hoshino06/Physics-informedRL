# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 14:50:59 2024
@author: hoshino
"""
import torch
import matplotlib.pyplot as plt

import sys, os
sys.path.append(os.pardir)


data_dir    = 'logs/test/1115_1139'
check_point = 'latest'

################################
# Load agent    
################################
from agent.DQN import PIRLagent

obsNum = 2 + 1
actNum = 3 
agent  = PIRLagent(obsNum, actNum)

agent.load_weights(data_dir, ckpt_idx=check_point) 


################################
# Safe probability    
################################
x1 = torch.linspace(-1.5, 1.5, steps=100) 
x2 = torch.linspace(-1.2, 1.2, steps=100) 
X1, X2 = torch.meshgrid(x1, x2, indexing='ij')
T = torch.full_like(X1, 2.0)
input_tensor = torch.stack([X1.flatten(), X2.flatten(), T.flatten()], dim=-1)

with torch.no_grad():
    predictions  = agent.critic(input_tensor)
    max_q_values = predictions.max(dim=-1)[0]

max_q_values_np  = max_q_values.view(100,100).numpy()    

plt.figure(figsize=(8, 6))
plt.contourf(X1.numpy(), X2.numpy(), max_q_values_np, levels=50, cmap='viridis')
plt.colorbar()
plt.xlabel('x1')
plt.ylabel('x2')
plt.title('Max of Agent Predictions for [x1, x2, T=2]')
plt.show()

