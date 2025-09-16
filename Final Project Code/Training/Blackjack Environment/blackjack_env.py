import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random

# ─── Simulation core ───

class DeckEngine:
    def __init__(self, num_decks=1):
        self.num_decks = num_decks
        self._build_shoe()

    def _build_shoe(self):
        self.cards = []
        for _ in range(self.num_decks):
            for rank in range(1, 14):
                value = rank if rank < 11 else 10
                self.cards += [value] * 4
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)
        self.idx = 0
        self.running_count = 0

    def deal(self):
        if self.idx >= len(self.cards):
            self.shuffle()
        v = self.cards[self.idx]
        self.idx += 1
        if 2 <= v <= 6:
            self.running_count += 1
        elif v == 1 or v >= 10:
            self.running_count -= 1
        return v

class Hand:
    def __init__(self):
        self.cards = []

    def add(self, v):
        self.cards.append(v)

    @property
    def value(self):
        total = sum(self.cards)
        aces = self.cards.count(1)
        if aces and total + 10 <= 21:
            total += 10
        return total

    @property
    def is_soft(self):
        return 1 in self.cards and sum(self.cards) + 10 <= 21

    @property
    def is_bust(self):
        return self.value > 21

    @property
    def is_blackjack(self):
        return len(self.cards) == 2 and self.value == 21

class PyBlackjackSimulator:
    def __init__(self, num_decks=1):
        self.deck = DeckEngine(num_decks)

    def reset(self):
        self.player = Hand()
        self.dealer = Hand()
        self.bet = 1.0

        self.player.add(self.deck.deal())
        up = self.deck.deal(); self.dealer.add(up)
        self.player.add(self.deck.deal())
        hole = self.deck.deal(); self._hole = hole

        if 2 <= hole <= 6:
            self.deck.running_count -= 1
        elif hole == 1 or hole >= 10:
            self.deck.running_count += 1

        return (self.player.value,
                float(self.player.is_soft),
                self.dealer.cards[0],
                float(self.deck.running_count),
                float(len(self.player.cards) == 2)
               )

    def step(self, action):
        if action == 2 and len(self.player.cards) == 2:
            self.bet *= 2
            v = self.deck.deal(); self.player.add(v)
            if self.player.is_bust:
                return self._get_state(), -self.bet, True, False, {}
            return self._get_state(), 0.0, True, False, {}

        if action == 0:
            v = self.deck.deal(); self.player.add(v)
            if self.player.is_bust:
                return self._get_state(), -self.bet, True, False, {}
            return self._get_state(), 0.0, False, False, {}

        return self._get_state(), 0.0, True, False, {}

    def play_dealer_and_settle(self):
        h = self._hole; self.dealer.add(h)
        if 2 <= h <= 6:
            self.deck.running_count += 1
        elif h == 1 or h >= 10:
            self.deck.running_count -= 1
        while self.dealer.value < 16:
            v = self.deck.deal(); self.dealer.add(v)
        if self.player.is_blackjack and not self.dealer.is_blackjack:
            return 1.5 * self.bet
        if self.player.is_blackjack and self.dealer.is_blackjack:
            return 0.0
        if self.player.is_bust:
            return -self.bet
        if self.dealer.is_bust:
            return +self.bet
        p, d = self.player.value, self.dealer.value
        if p > d: return +self.bet
        if p < d: return -self.bet
        return 0.0

    def _get_state(self):
        return (self.player.value,
                float(self.player.is_soft),
                self.dealer.cards[0],
                float(self.deck.running_count),
                float(len(self.player.cards) == 2)
               )

class BlackjackEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, num_decks=1):
        super().__init__()
        self.sim = PyBlackjackSimulator(num_decks)
        self.action_space = spaces.Discrete(3)
        low  = np.array([4,0,2,-30,0], dtype=np.float32)
        high = np.array([21,1,11,30,1], dtype=np.float32)
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

    def reset(self, seed=None, options=None):
        if seed is not None:
            random.seed(seed)
        obs = np.array(self.sim.reset(), dtype=np.float32)
        return obs, {}

    def step(self, action):
        obs, reward, done, truncated, info = self.sim.step(action)
        if done and reward == 0.0:
            reward += self.sim.play_dealer_and_settle()
        return np.array(obs, dtype=np.float32), reward, done, truncated, info

    def render(self):
        pass
