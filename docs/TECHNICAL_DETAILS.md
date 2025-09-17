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

### Pretraining (Behavioral Cloning)
1. Load expert strategy data from CSV
2. Train MLP to predict expert actions
3. Fit feature scaler for normalization

### RL Training (PPO)
1. Initialize with pretrained weights
2. Train using PPO algorithm
3. Export final model to ONNX format

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
- Input: 4-dimensional feature vector
- Hidden layers: 2 layers of 64 neurons each
- Output: Action probabilities (hit/stand/double/split)
- Activation: ReLU for hidden, Softmax for output

## Performance

The trained agent achieves:
- Competitive performance against basic strategy
- Improved decision-making in high-count situations
- Real-time inference (< 1ms per decision)

