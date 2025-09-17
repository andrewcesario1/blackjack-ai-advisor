import torch
from stable_baselines3 import PPO
import torch.nn as nn

model = PPO.load("ppo_blackjack_finetuned.zip", device="cpu")

actor = nn.Sequential(
    model.policy.mlp_extractor.policy_net,
    model.policy.action_net
)

dummy = torch.zeros(1, 14, dtype=torch.float32)

torch.onnx.export(
    actor,
    dummy,
    "ppo_blackjack_actor.onnx",
    input_names  = ["obs"],
    output_names = ["logits"],
    dynamic_axes = {"obs":{0:"batch"}, "logits":{0:"batch"}},
    opset_version=13,
)
print("Exported actor to ppo_blackjack_actor.onnx")
