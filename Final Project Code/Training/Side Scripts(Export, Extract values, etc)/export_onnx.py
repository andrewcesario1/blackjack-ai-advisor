import torch
from stable_baselines3 import PPO

# 1) Load fine-tuned SB3 model
model = PPO.load("fast_ppo_blackjack_finetuned.zip", device="cpu")

# 2) Grab the policy network
policy_net = model.policy.mlp_extractor.policy_net
policy_net.eval()

# 3) Build a dummy observation of the correct size
obs_dim = model.observation_space.shape[0] if hasattr(model, "observation_space") \
          else model.env.observation_space.shape[1]  # adapt as needed
dummy = torch.zeros(1, obs_dim, dtype=torch.float32)

# 4) Export to ONNX
torch.onnx.export(
    policy_net,
    dummy,
    "ppo_blackjack_finetuned.onnx",
    input_names=["state"],
    output_names=["action_logits"],
    opset_version=13,
)
print("✅ Exported ONNX model to ppo_blackjack_finetuned.onnx")
