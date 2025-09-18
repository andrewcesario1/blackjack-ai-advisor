
import torch
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'blackjack_env'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'training'))
from fast_train_rl import FastObsEnv
from blackjack_env import BlackjackEnv
from stable_baselines3 import PPO

def evaluate(
    model_path: str = "../models/ppo_blackjack_finetuned.zip",
    expert_ckpt: str = "../models/expert_pretrained.pth",
    num_envs: int = 1,
    num_episodes: int = 100_000,
    num_decks: int = 1,
):
    ckpt = torch.load(expert_ckpt, map_location="cpu", weights_only=False)
    scaler = ckpt["preprocessor"].named_transformers_["num"]
    num_mean = scaler.mean_.tolist()
    num_std  = scaler.scale_.tolist()
    def make_env():
        base = BlackjackEnv(num_decks=num_decks)
        return FastObsEnv(base, num_mean, num_std, up_max=10)

    env = make_env()

    model = PPO.load(model_path, device="cpu")
    print(f"✅ Loaded policy from {model_path}")
    returns = []
    wins = losses = pushes = 0

    for ep in range(num_episodes):
        obs, _ = env.reset()
        done = False
        total_reward = 0.0

        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, truncated, info = env.step(action)
            total_reward += reward

        returns.append(total_reward)
        if total_reward >  0: wins   += 1
        elif total_reward <  0: losses += 1
        else:                   pushes += 1

        if (ep+1) % (num_episodes//10) == 0:
            print(f" → Completed {ep+1}/{num_episodes} episodes")

    avg_return = np.mean(returns)
    std_return = np.std(returns)
    print("\n🏁 Evaluation results:")
    print(f"   Episodes:      {num_episodes}")
    print(f"   Average reward per hand: {avg_return:.4f}  ±{std_return:.4f}")
    print(f"   Win rate:  {wins/num_episodes:.2%}")
    print(f"   Loss rate: {losses/num_episodes:.2%}")
    print(f"   Push rate: {pushes/num_episodes:.2%}")

if __name__ == "__main__":
    evaluate()
