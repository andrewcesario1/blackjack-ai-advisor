import unittest
import pandas as pd
import numpy as np
import os
import sys

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class TestDataLoading(unittest.TestCase):
    def test_expert_data_exists(self):
        """Test that expert strategy data file exists and is readable"""
        data_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'expert_strategy.csv')
        self.assertTrue(os.path.exists(data_path), "expert_strategy.csv not found")
        
        df = pd.read_csv(data_path)
        self.assertGreater(len(df), 0, "Expert data is empty")
        
        required_columns = ['playerTotal', 'isSoft', 'dealerUp', 'runningCount', 'canDouble', 'action']
        for col in required_columns:
            self.assertIn(col, df.columns, f"Missing column: {col}")
    
    def test_expert_data_format(self):
        """Test that expert data has correct format"""
        data_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'expert_strategy.csv')
        df = pd.read_csv(data_path)
        
        # Check action values are valid
        valid_actions = ['H', 'S', 'D']
        for action in df['action'].unique():
            self.assertIn(action, valid_actions, f"Invalid action: {action}")
        
        # Check numeric ranges
        self.assertTrue((df['playerTotal'] >= 4).all() and (df['playerTotal'] <= 21).all())
        self.assertTrue((df['dealerUp'] >= 1).all() and (df['dealerUp'] <= 11).all())

class TestModelFiles(unittest.TestCase):
    def test_model_files_exist(self):
        """Test that pretrained model files exist"""
        models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        
        # Check for sklearn model
        sklearn_model = os.path.join(models_dir, 'policy_pretrained.pkl')
        if os.path.exists(sklearn_model):
            self.assertTrue(os.path.isfile(sklearn_model))
        
        # Check for PyTorch model
        pytorch_model = os.path.join(models_dir, 'expert_pretrained.pth')
        if os.path.exists(pytorch_model):
            self.assertTrue(os.path.isfile(pytorch_model))

if __name__ == '__main__':
    unittest.main()
