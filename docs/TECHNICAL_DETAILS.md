# Technical Implementation Details

## Architecture Overview

This project implements a complete pipeline from reinforcement learning training to real-time game integration:

1. **Environment**: Custom blackjack environment with realistic rules
2. **Training**: PPO agent with behavioral cloning pretraining
3. **Export**: Model conversion to ONNX for Unity integration
4. **Integration**: Real-time inference in Unity game

## Blackjack Environment

The custom environment (`blackjack_env.py`) implements:
- Standard blackjack rules (dealer stands on 17)
- Hole card visibility for training
- Hi-Lo counting system
- Feature extraction for neural network input

### State Features
- Player hand value (with soft/hard distinction)
- Dealer up card
- Running count (Hi-Lo system)
- Basic strategy deviation index

## Training Pipeline

### Step 1: Pretraining (Behavioral Cloning)
1. Load expert strategy data from `models/expert_strategy.csv`
2. Train PyTorch MLP to predict expert actions
3. Fit StandardScaler for feature normalization
4. Save pretrained model as `models/expert_pretrained.pth`

### Step 2: RL Training (PPO)
1. Initialize PPO agent with pretrained weights
2. Train using PPO algorithm for 5,000,000 steps
3. Save complete model as `models/ppo_blackjack_finetuned.zip`

### Step 3: ONNX Export
1. Extract actor network from PPO model
2. Convert PyTorch model to ONNX format
3. Save as `models/ppo_blackjack_actor.onnx` for Unity integration

## Unity Integration

### AI Advisor System
- **AIAdvisor.cs**: Main advisor component with ONNX inference
- **BasicStrategy.cs**: Hard/soft basic strategy tables
- **HiLoCounter.cs**: Running count management
- **IndexStrategy.cs**: Count-based deviations

### Game Scripts
- **GameManager.cs**: Orchestrates game flow and AI integration
- **GameScript.cs**: Hand management and game logic
- **deck.cs**: Card dealing with Hi-Lo integration

## Model Architecture

The PPO actor network:
- **Input**: 4-dimensional feature vector (hand value, dealer up card, running count, basic strategy deviation)
- **Hidden layers**: 2 layers of 64 neurons each
- **Output**: Action probabilities (hit/stand/double)
- **Activation**: ReLU for hidden layers, Softmax for output
- **Training**: 5,000,000 PPO steps for optimal performance

## Performance Results

### RL Policy Performance (5M Steps Training)
- **Episodes Evaluated**: 100,000
- **Average Reward**: 0.0071 ± 0.9811
- **Win Rate**: 44.42%
- **Loss Rate**: 46.04%
- **Push Rate**: 9.54%

### Baseline Strategy Performance
- **Episodes Evaluated**: 100,000
- **Average Reward**: -0.0048 ± 0.9811
- **Win Rate**: 43.12%
- **Loss Rate**: 47.68%
- **Push Rate**: 9.20%

### Key Improvements
- **Positive Expected Value**: RL agent achieves positive average reward vs. baseline's negative
- **Higher Win Rate**: 44.42% vs. 43.12% (1.3% improvement)
- **Better Loss Management**: 46.04% vs. 47.68% (1.64% reduction in losses)
- **Real-time Inference**: < 1ms per decision in Unity
- **Count-based Decisions**: Improved decision-making in high-count situations

## Evaluation Scripts

### Policy Evaluation
- **`evaluate_policy.py`**: Evaluates RL policy performance over 100,000 episodes
- **`baseline_evaluate.py`**: Evaluates Basic+Index strategy baseline performance
- **`compare_policies.py`**: Generates matplotlib comparison graphs between strategies

### Usage
```bash
cd ai-agent

# Evaluate RL policy
python evaluation/evaluate_policy.py

# Evaluate baseline strategy
python evaluation/baseline_evaluate.py

# Generate comparison graphs
python evaluation/compare_policies.py
```

### Output Files
- Evaluation results displayed in terminal
- Matplotlib graphs saved as PNG files
- Performance metrics for win/loss/push rates and average rewards

