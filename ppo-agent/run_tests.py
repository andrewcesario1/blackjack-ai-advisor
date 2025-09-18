#!/usr/bin/env python3
"""
Simple test runner for the blackjack AI agent
"""

import unittest
import sys
import os

# Add tests directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tests'))

def run_tests():
    """Run all tests in the tests directory"""
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\nAll tests passed!")
        return 0
    else:
        print(f"\n{len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        return 1

if __name__ == '__main__':
    sys.exit(run_tests())
