import numpy as np
import matplotlib.pyplot as plt
import torch
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="stable_baselines3")
from stable_baselines3 import PPO
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'blackjack_env'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'training'))
from blackjack_env import BlackjackEnv
from fast_train_rl import FastObsEnv

# Index deviation helper
def index_deviation(player_total, is_soft, dealer_up, running_count):
    if is_soft:
        return None
    if player_total == 16 and dealer_up == 10 and running_count >= 0:
        return "S"
    if player_total == 15 and dealer_up == 10 and running_count >= 4:
        return "S"
    if player_total == 12 and dealer_up == 3 and running_count < 2:
        return "H"
    if player_total == 12 and dealer_up == 2 and running_count < 3:
        return "H"
    if player_total == 10 and dealer_up == 1 and running_count >= 3:
        return "D"
    if player_total == 11 and dealer_up == 1 and running_count >= 1:
        return "D"
    if player_total == 10 and dealer_up == 10 and running_count >= 4:
        return "D"
    if player_total == 9 and dealer_up == 2 and running_count >= 1:
        return "D"
    if player_total == 9 and dealer_up == 7 and running_count >= 3:
        return "D"
    if player_total == 16 and dealer_up == 9 and running_count >= 5:
        return "S"
    if player_total == 13 and dealer_up == 2 and running_count >= -1:
        return "S"
    if player_total == 12 and dealer_up == 4 and running_count >= 0:
        return "S"
    if player_total == 12 and dealer_up == 5 and running_count >= -2:
        return "S"
    if player_total == 12 and dealer_up == 6 and running_count >= -1:
        return "S"
    if player_total == 15 and dealer_up == 9 and running_count >= 2:
        return "S"
    return None

# Basic strategy tables
HardTable = [
    ["H"]*10, ["H"]*10, ["H"]*10, ["H"]*10,
    ["H","D","D","D","D","H","H","H","H","H"],
    ["D"]*8 + ["H","H"],
    ["D"]*9 + ["H"],
    ["H","H","S","S","S","H","H","H","H","H"],
    ["S","S","S","S","S","H","H","H","H","H"],
    ["S","S","S","S","S","H","H","H","H","H"],
    ["S","S","S","S","S","H","H","H","H","H"],
    ["S","S","S","S","S","H","H","H","H","H"],
    ["S"]*10
]
SoftTable = [
    ["H","H","H","D","D","H","H","H","H","H"],
    ["H","H","H","D","D","H","H","H","H","H"],
    ["H","H","D","D","D","H","H","H","H","H"],
    ["H","H","D","D","D","H","H","H","H","H"],
    ["H","D","D","D","D","H","H","H","H","H"],
    ["S","D","D","D","D","S","S","H","H","H"],
    ["S"]*10, ["S"]*10
]

def basic_strategy_action(obs):
    pt, soft, up, rc, cd = obs
    playerTotal = int(pt)
    isSoft      = bool(soft)
    dealerUp    = int(up)  # Ace is 1
    runningCount= int(rc)
    dev = index_deviation(playerTotal, isSoft, dealerUp, runningCount)
    if dev is not None:
        return {"H":0,"S":1,"D":2}[dev]
    col = 9 if dealerUp == 1 else dealerUp - 2
    if isSoft:
        row = max(13, min(playerTotal,20)) - 13
        choice = SoftTable[row][col]
    else:
        row = max(5, min(playerTotal,17)) - 5
        choice = HardTable[row][col]
    return {"H":0,"S":1,"D":2}[choice]

# Evaluation routines
def evaluate_rl(model, env, n):
    rewards = np.zeros(n, dtype=np.float32)
    for i in range(n):
        obs, _ = env.reset()
        done = False; total = 0.0
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, r, done, trunc, _ = env.step(action)
            total += r
        rewards[i] = total
        if (i+1) % 100_000 == 0:
            print(f"RL: {i+1}/{n}")
    return rewards

def evaluate_baseline(env, n):
    rewards = np.zeros(n, dtype=np.float32)
    for i in range(n):
        obs, _ = env.reset()
        done = False; total = 0.0
        while not done:
            a = basic_strategy_action(obs)
            obs, r, done, trunc, _ = env.step(a)
            total += r
        rewards[i] = total
        if (i+1) % 100_000 == 0:
            print(f"BL: {i+1}/{n}")
    return rewards

# Main evaluation and plotting
def main():
    N = 500_000

    ckpt = torch.load("../models/expert_pretrained.pth", map_location="cpu", weights_only=False)
    scaler = ckpt["preprocessor"].named_transformers_["num"]
    means = scaler.mean_.astype(np.float32)
    stds  = scaler.scale_.astype(np.float32)
    rl = PPO.load("../models/ppo_blackjack_finetuned.zip", map_location="cpu")
    base_env = BlackjackEnv(num_decks=1)
    rl_env   = FastObsEnv(base_env, means, stds, up_max=10)
    print("▶ Evaluating RL policy …")
    rl_rets = evaluate_rl(rl, rl_env, N)

    bl_env = BlackjackEnv(num_decks=1)
    print("▶ Evaluating Basic+Index baseline …")
    bl_rets = evaluate_baseline(bl_env, N)
    for name, arr in [("RL", rl_rets), ("Baseline", bl_rets)]:
        m  = arr.mean()
        se = arr.std(ddof=1)/np.sqrt(N)
        ci = 1.96 * se
        print(f"{name}: EV = {m:.4f} ± {ci:.4f} (95% CI)")

    plt.plot(np.cumsum(rl_rets), label="RL")
    plt.plot(np.cumsum(bl_rets), label="Basic+Index")
    plt.xlabel("Hand #"); plt.ylabel("Cumulative Profit")
    plt.title("RL vs Basic+Index")
    plt.legend(); plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
