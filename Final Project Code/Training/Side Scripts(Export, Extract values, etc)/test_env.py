# test_env.py
from blackjack_env import BlackjackEnv

env = BlackjackEnv(num_decks=1)
obs = env.reset()
print("Initial obs:", obs)

done = False
total_reward = 0
while not done:
    action = env.action_space.sample()
    obs, r, done, _ = env.step(action)
    total_reward += r
print("Episode done. Total reward:", total_reward)
