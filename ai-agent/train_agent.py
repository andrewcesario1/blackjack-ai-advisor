#!/usr/bin/env python3
"""
Complete training pipeline for Blackjack PPO Agent

This script runs the full training pipeline:
1. Pretrain with expert data (behavioral cloning)
2. Fine-tune with PPO reinforcement learning
3. Export to ONNX for Unity integration

Usage:
    python train_agent.py

Make sure you have expert_strategy.csv in the models/ directory.
"""

import os
import sys
import subprocess

def run_script(script_path, description):
    """Run a Python script and handle errors"""
    print(f"\n{description}")
    print(f"Running: {script_path}")
    
    try:
        result = subprocess.run([sys.executable, script_path], 
                              cwd=os.path.dirname(script_path),
                              check=True, 
                              capture_output=True, 
                              text=True)
        print("Success!")
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False
    return True

def main():
    print("Blackjack PPO Agent Training Pipeline")
    print("=" * 50)
    
    expert_csv = "models/expert_strategy.csv"
    if not os.path.exists(expert_csv):
        print(f"Missing required file: {expert_csv}")
        print("Please ensure expert_strategy.csv is in the models/ directory")
        return
    
    print("\nChoose training approach:")
    print("1. PyTorch + PPO (recommended)")
    print("2. Sklearn MLP (simpler, faster)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        print("\nUsing Sklearn MLP approach")
        if not run_script("training/train.py", "Step 1: Sklearn MLP training"):
            return
        print("\nSklearn training complete!")
        print("Generated files:")
        print("- models/policy_pretrained.pkl (sklearn model)")
        print("\nNote: This approach doesn't generate ONNX for Unity integration")
        
    else:
        print("\nUsing PyTorch + PPO approach")
        
        if not run_script("training/pretrain.py", "Step 1: Pretraining with expert data"):
            return
        
        if not run_script("training/fast_train_rl.py", "Step 2: PPO fine-tuning"):
            return
        
        if not run_script("utils/export_onnx.py", "Step 3: Export to ONNX"):
            return
        
        print("\nTraining pipeline complete!")
        print("Generated files:")
        print("- models/expert_pretrained.pth (pretrained model)")
        print("- ppo_blackjack_finetuned.zip (PPO model)")
        print("- ppo_blackjack_actor.onnx (Unity-ready model)")
        print("\nCopy the .onnx file to unity/Assets/Models/ for Unity integration")

if __name__ == "__main__":
    main()

