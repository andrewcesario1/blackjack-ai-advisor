# export_actor.py
import torch
from stable_baselines3 import PPO
import torch.nn as nn

# 1) load your fine‐tuned SB3 model
model = PPO.load("ppo_blackjack_finetuned.zip", device="cpu")

# 2) grab the two pieces you need:
#    - mlp_extractor.policy_net: shared actor feature net
#    - action_net: final linear that outputs logits
actor = nn.Sequential(
    model.policy.mlp_extractor.policy_net,
    model.policy.action_net
)

# 3) dummy 14‐dim input: [scaled playerTotal, scaled runningCount,
#                        isSoft, one-hot(1→10), canDouble]
dummy = torch.zeros(1, 14, dtype=torch.float32)

# 4) export just that MLP → ONNX
torch.onnx.export(
    actor,
    dummy,
    "ppo_blackjack_actor.onnx",
    input_names  = ["obs"],
    output_names = ["logits"],
    dynamic_axes = {"obs":{0:"batch"}, "logits":{0:"batch"}},
    opset_version=13,
)
print("✅ Exported actor to ppo_blackjack_actor.onnx")
