# train_rl.py

import torch
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'blackjack_env'))
from blackjack_env import BlackjackEnv
from multiprocessing import freeze_support

class FastObsEnv(gym.ObservationWrapper):
    """
    Wraps BlackjackEnv to:
      1) handle Gymnasium’s 5-tuple API
      2) apply a one-time NumPy scaling + one-hot encoding
      3) eliminate pandas/sklearn overhead for speed
    """
    def __init__(self, env, num_mean, num_std, up_max=10):
        super().__init__(env)
        # store scaler parameters
        self.mean = np.array(num_mean, dtype=np.float32)
        self.std  = np.array(num_std,  dtype=np.float32)
        self.up_max = up_max

        # calculate observation dimension:
        # 2 scaled values + 1 isSoft + up_max one-hot + 1 canDouble
        dim = 2 + 1 + up_max + 1
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf,
            shape=(dim,), dtype=np.float32
        )
        self.action_space = env.action_space

    def _encode(self, obs):
        pt, soft, up, rc, cd = obs
        # 1) scale numeric features
        nums = np.array([pt, rc], dtype=np.float32)
        nums = (nums - self.mean) / (self.std + 1e-8)
        # 2) isSoft as float
        oh_soft = np.array([soft], dtype=np.float32)
        # 3) dealerUp one-hot
        oh_up = np.zeros(self.up_max, dtype=np.float32)
        idx = int(up) - 1
        if 0 <= idx < self.up_max:
            oh_up[idx] = 1.0
        # 4) canDouble as float
        oh_cd = np.array([cd], dtype=np.float32)
        # concatenate all parts
        return np.concatenate([nums, oh_soft, oh_up, oh_cd], axis=0)

    def reset(self, *, seed=None, options=None):
        obs, info = self.env.reset(seed=seed, options=options)
        return self._encode(obs), info

    def step(self, action):
        obs, reward, done, truncated, info = self.env.step(action)
        return self._encode(obs), reward, done, truncated, info

def main():
    freeze_support()

    # 1) Load expert checkpoint to extract scaler
    checkpoint = torch.load("expert_pretrained.pth", map_location="cpu", weights_only=False)
    preprocessor = checkpoint["preprocessor"]
    scaler = preprocessor.named_transformers_["num"]
    num_mean = scaler.mean_.tolist()
    num_std  = scaler.scale_.tolist()
    print("🚀 Loaded scaler parameters from expert_pretrained.pth")

    # 2) Build vectorized FastObs environments
    def make_env():
        base = BlackjackEnv(num_decks=1)
        return FastObsEnv(base, num_mean, num_std, up_max=10)

    n_envs = 8
    env = DummyVecEnv([make_env for _ in range(n_envs)])
    print(f"✅ Created {n_envs} FastObs vectorized environments.")

    # 3) Initialize PPO with tuned hyperparams
    model = PPO(
        "MlpPolicy",
        env,
        learning_rate=3e-4,
        vf_coef=0.5,
        ent_coef=0.01,
        gae_lambda=0.95,
        clip_range=0.2,
        n_steps=2048,
        batch_size=512,
        n_epochs=10,
        policy_kwargs=dict(net_arch=dict(pi=[64,64], vf=[128,128])),
        verbose=1,
        device="auto",
    )
    print("✅ PPO initialized.")

    # 4) Fine-tune for 5M timesteps
    total_steps = 5_000_000
    print(f"🚀 Starting RL fine-tuning: {total_steps} timesteps…")
    model.learn(total_timesteps=total_steps)

    # 5) Save final policy
    outpath = "ppo_blackjack_finetuned"
    model.save(outpath)
    print(f"🏁 Training complete; model saved as {outpath}.zip")

if __name__ == "__main__":
    main()
