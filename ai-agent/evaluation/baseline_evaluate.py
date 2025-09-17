# baseline_evaluate.py

import numpy as np
import random
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'blackjack_env'))
from blackjack_env import BlackjackEnv

# ─── Basic Strategy Tables ────────────────────────────────────────────────
_HARD = [
    ["H","H","H","H","H","H","H","H","H","H"],  # 5
    ["H","H","H","H","H","H","H","H","H","H"],  # 6
    ["H","H","H","H","H","H","H","H","H","H"],  # 7
    ["H","H","H","H","H","H","H","H","H","H"],  # 8
    ["H","D","D","D","D","H","H","H","H","H"],  # 9
    ["D","D","D","D","D","D","D","D","H","H"],  # 10
    ["D","D","D","D","D","D","D","D","D","H"],  # 11
    ["H","H","S","S","S","H","H","H","H","H"],  # 12
    ["S","S","S","S","S","H","H","H","H","H"],  # 13
    ["S","S","S","S","S","H","H","H","H","H"],  # 14
    ["S","S","S","S","S","H","H","H","H","H"],  # 15
    ["S","S","S","S","S","H","H","H","H","H"],  # 16
    ["S","S","S","S","S","S","S","S","S","S"],  # 17+
]
_SOFT = [
    ["H","H","H","D","D","H","H","H","H","H"],  # A,2 (13)
    ["H","H","H","D","D","H","H","H","H","H"],  # A,3 (14)
    ["H","H","D","D","D","H","H","H","H","H"],  # A,4 (15)
    ["H","H","D","D","D","H","H","H","H","H"],  # A,5 (16)
    ["H","D","D","D","D","H","H","H","H","H"],  # A,6 (17)
    ["S","D","D","D","D","S","S","H","H","H"],  # A,7 (18)
    ["S","S","S","S","S","S","S","S","S","S"],  # A,8 (19)
    ["S","S","S","S","S","S","S","S","S","S"],  # A,9 (20)
]

# ─── Index Deviations ─────────────────────────────────────────────────────
def index_deviation(player_total, is_soft, dealer_up, running_count):
    if is_soft:
        return None
    # 16 vs 10: Stand if count ≥ 0
    if player_total == 16 and dealer_up == 10 and running_count >= 0:
        return "S"
    # 15 vs 10: Stand if count ≥ 4
    if player_total == 15 and dealer_up == 10 and running_count >= 4:
        return "S"
    # 12 vs 3: Hit if count < 2
    if player_total == 12 and dealer_up == 3 and running_count < 2:
        return "H"
    # 12 vs 2: Hit if count < 3
    if player_total == 12 and dealer_up == 2 and running_count < 3:
        return "H"
    # 10 vs Ace: Double if count ≥ 3
    if player_total == 10 and dealer_up == 1 and running_count >= 3:
        return "D"
    # 11 vs Ace: Double if count ≥ 1
    if player_total == 11 and dealer_up == 1 and running_count >= 1:
        return "D"
    # 10 vs 10: Double if count ≥ 4
    if player_total == 10 and dealer_up == 10 and running_count >= 4:
        return "D"
    # 9 vs 2: Double if count ≥ 1
    if player_total == 9 and dealer_up == 2 and running_count >= 1:
        return "D"
    # 9 vs 7: Double if count ≥ 3
    if player_total == 9 and dealer_up == 7 and running_count >= 3:
        return "D"
    # 16 vs 9: Stand if count ≥ 5
    if player_total == 16 and dealer_up == 9 and running_count >= 5:
        return "S"
    # 13 vs 2: Stand if count ≥ -1
    if player_total == 13 and dealer_up == 2 and running_count >= -1:
        return "S"
    # 12 vs 4: Stand if count ≥ 0
    if player_total == 12 and dealer_up == 4 and running_count >= 0:
        return "S"
    # 12 vs 5: Stand if count ≥ -2
    if player_total == 12 and dealer_up == 5 and running_count >= -2:
        return "S"
    # 12 vs 6: Stand if count ≥ -1
    if player_total == 12 and dealer_up == 6 and running_count >= -1:
        return "S"
    # 15 vs 9: Stand if count ≥ 2
    if player_total == 15 and dealer_up == 9 and running_count >= 2:
        return "S"
    return None

# ─── Strategy Decision ────────────────────────────────────────────────────
def decide_action(obs):
    pt, soft_f, up_f, rc_f, cd_f = obs
    player_total  = int(pt)
    is_soft       = bool(soft_f)
    dealer_up     = int(up_f)
    running_count = int(rc_f)
    can_double    = bool(cd_f)

    # 1) Count-based deviation
    dev = index_deviation(player_total, is_soft, dealer_up, running_count)
    if dev is not None:
        return {"H":0,"S":1,"D":2}[dev]

    # 2) Pure basic strategy
    col = 9 if dealer_up == 1 else dealer_up - 2
    if not is_soft:
        row = min(max(player_total, 5), 17) - 5
        act = _HARD[row][col]
    else:
        row = min(max(player_total,13),20) - 13
        act = _SOFT[row][col]

    # Double → Hit if not allowed
    if act == "D" and not can_double:
        act = "H"
    return {"H":0,"S":1,"D":2}[act]

# ─── Evaluation Loop ──────────────────────────────────────────────────────
def evaluate_baseline(num_episodes=100_000, num_decks=1, seed=42):
    random.seed(seed)
    env = BlackjackEnv(num_decks=num_decks)
    returns = []
    wins = losses = pushes = 0

    for ep in range(1, num_episodes+1):
        obs, _ = env.reset()
        done = False
        total_reward = 0.0

        while not done:
            action = decide_action(obs)
            obs, reward, done, truncated, info = env.step(action)
            total_reward += reward

        returns.append(total_reward)
        if total_reward >  0: wins   += 1
        elif total_reward <  0: losses += 1
        else:                   pushes += 1

        if ep % (num_episodes//10) == 0:
            print(f"→ {ep}/{num_episodes} hands done")

    avg_ret = np.mean(returns)
    std_ret = np.std(returns)
    print("\n🏁 Baseline Basic+Index Evaluation:")
    print(f"   Hands:       {num_episodes}")
    print(f"   Avg reward:  {avg_ret:.4f} ±{std_ret:.4f}")
    print(f"   Win rate:    {wins/num_episodes:.2%}")
    print(f"   Loss rate:   {losses/num_episodes:.2%}")
    print(f"   Push rate:   {pushes/num_episodes:.2%}")

if __name__ == "__main__":
    evaluate_baseline()
