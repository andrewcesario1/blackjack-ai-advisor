import unittest
import numpy as np
import sys
import os

# Add the parent directory to the path to import blackjack_env
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'blackjack_env'))
from blackjack_env import BlackjackEnv, Hand, DeckEngine

class TestHand(unittest.TestCase):
    def test_hand_value_basic(self):
        hand = Hand()
        hand.add(5)
        hand.add(6)
        self.assertEqual(hand.value, 11)
    
    def test_hand_value_with_ace(self):
        hand = Hand()
        hand.add(1)  # Ace
        hand.add(5)
        self.assertEqual(hand.value, 16)  # Ace counts as 11
    
    def test_hand_value_multiple_aces(self):
        hand = Hand()
        hand.add(1)  # Ace
        hand.add(1)  # Ace
        hand.add(9)
        self.assertEqual(hand.value, 21)  # One ace as 11, one as 1
    
    def test_hand_bust(self):
        hand = Hand()
        hand.add(10)
        hand.add(10)
        hand.add(5)
        self.assertTrue(hand.is_bust)
    
    def test_hand_blackjack(self):
        hand = Hand()
        hand.add(1)  # Ace
        hand.add(10)
        self.assertTrue(hand.is_blackjack)

class TestDeckEngine(unittest.TestCase):
    def test_deck_creation(self):
        deck = DeckEngine(num_decks=1)
        self.assertEqual(len(deck.cards), 52)
    
    def test_deck_deal(self):
        deck = DeckEngine(num_decks=1)
        card = deck.deal()
        self.assertIsInstance(card, int)
        self.assertGreaterEqual(card, 1)
        self.assertLessEqual(card, 10)

class TestBlackjackEnv(unittest.TestCase):
    def test_env_creation(self):
        env = BlackjackEnv()
        self.assertIsNotNone(env.action_space)
        self.assertIsNotNone(env.observation_space)
    
    def test_env_reset(self):
        env = BlackjackEnv()
        obs, info = env.reset()
        self.assertEqual(len(obs), 5)
        self.assertIsInstance(obs, np.ndarray)
    
    def test_env_step_hit(self):
        env = BlackjackEnv()
        obs, _ = env.reset()
        obs, reward, done, truncated, info = env.step(0)  # Hit
        self.assertEqual(len(obs), 5)
        self.assertIsInstance(reward, float)
        self.assertIsInstance(done, bool)

if __name__ == '__main__':
    unittest.main()
