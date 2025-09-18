# Blackjack PPO Agent

A reinforcement learning project that trains a PPO (Proximal Policy Optimization) agent to play blackjack using a custom environment, then exports the learned policy as ONNX for Unity integration.

## Demo

### Demo Video
[![Watch the demo](https://img.youtube.com/vi/-0ZrOJTF-t0/0.jpg)](https://www.youtube.com/watch?v=-0ZrOJTF-t0)

### Play Online
**Try the game yourself**: [Play Blackjack PPO Agent Online](https://play.unity.com/en/games/fde4d8ab-df09-4f48-a1dc-88a185bff4be/blackjack-ai-advisor)

*Note: Go full screen for optimal UI experience*

### Evaluation Results

#### Performance Comparison Graph
![RL vs Basic+Index Cumulative Profit](docs/RL%20vs%20Basic%20Strategy%20%2B%20Index%20Deviation.PNG)

This graph shows the cumulative profit over 500,000 hands of blackjack:
- **RL Agent (blue line)**: Consistently profitable, ending at +2,200 profit
- **Basic+Index Strategy (orange line)**: Consistently losing, ending at -9,000 loss

The RL agent significantly outperforms the baseline strategy, achieving positive returns while the traditional approach incurs losses.

### Performance Results

#### RL Policy Evaluation (5M Steps Training)
![RL Policy Evaluation](docs/RL%20Evaluation.PNG)

#### Baseline Strategy Evaluation
![Baseline Strategy Evaluation](docs/Baseline%20Evaluation.PNG)

The RL agent shows **significant improvement** over the baseline strategy, achieving positive average reward compared to the baseline's negative performance.

## Project Structure

```
blackjack-ppo-agent/
│
├── unity/             # Unity game project (ready to play)
│   ├── Assets/Models/ppo_blackjack_actor.onnx  # Trained RL model
│   ├── Assets/Scripts/                         # Game logic + PPO agent
│   └── Assets/Scenes/                          # Game scenes
│
├── ppo-agent/         # ML training and evaluation
│   ├── training/      # PyTorch + PPO pipeline
│   ├── evaluation/    # Performance evaluation scripts
│   ├── models/        # Trained models and data
│   ├── tests/         # Test suite
│   └── utils/         # Export and utility scripts
│
├── docs/              # Documentation and results
└── requirements.txt
```

## Features

- Custom Blackjack Environment: Fast, feature-based Gymnasium environment with Hi-Lo counting
- PyTorch + PPO Training: Complete reinforcement learning pipeline
- Complete Training Pipeline: Automated script runs full training process
- Unity Integration: Trained model exported as ONNX for real-time gameplay
- Multiple Strategies: Includes basic strategy, Hi-Lo counting, and RL-based decisions
- Comprehensive Evaluation: Baseline comparison and policy evaluation tools
- Ready-to-Use Models: Includes pretrained models for immediate testing

## Quick Start

### Unity Game (Ready to Play)
The `unity/` folder contains a complete Unity project with everything needed to run the blackjack game:

- **Trained Model**: `unity/Assets/Models/ppo_blackjack_actor.onnx` - Pre-trained RL model ready for testing
- **Game Scripts**: Complete blackjack game logic with PPO agent integration
- **PPO Agent System**: Real-time decision recommendations using the trained model
- **UI Components**: Cards, chips, and game interface
- **Scenes**: Ready-to-play game scenes

**To run the game:**
1. Open Unity and import the `unity/` folder as a new project
2. Open the "Game Scene" to play blackjack with PPO agent
3. The PPO agent provides real-time recommendations based on the trained model

*Note: The model in Unity is for testing purposes. The training process below can be used to retrain or modify the model.*

### Training the PPO Agent

#### Complete Automated Pipeline
```bash
# Install dependencies
pip install -r requirements.txt

# Run complete training pipeline
cd ppo-agent
python train_agent.py
```

#### Manual Step-by-Step
```bash
# Install dependencies
pip install -r requirements.txt

# Step 1: Pretrain with expert data
python ppo-agent/training/pretrain.py

# Step 2: Fine-tune with PPO
python ppo-agent/training/fast_train_rl.py

# Step 3: Export to ONNX
python ppo-agent/utils/export_onnx.py

# Copy the ONNX model to Unity
cp ppo_blackjack_actor.onnx unity/Assets/Models/
```


### Evaluation
```bash
cd ppo-agent

# Compare different strategies (RL vs Basic Strategy vs Index Strategy)
python evaluation/compare_policies.py

# Evaluate PPO agent performance
python evaluation/evaluate_policy.py

# Run baseline evaluation (Basic Strategy only)
python evaluation/baseline_evaluate.py

# Test environment functionality
python utils/test_env.py
```

## Testing

Run the test suite to verify functionality:

```bash
cd ppo-agent
python run_tests.py
```

The tests cover:
- Blackjack environment functionality
- Hand value calculations
- Deck operations
- Data loading and validation
- Model file existence


## Technical Details

- Environment: Custom blackjack environment with hole card visibility
- Algorithm: PPO with behavioral cloning pretraining
- Model: Neural network actor exported to ONNX format
- Features: Hand value, dealer up card, running count, basic strategy deviation
- Integration: ONNX Runtime for Unity inference
- Training Data: 5,762 expert strategy examples
- Model Size: 4-dimensional input, 3-dimensional output (Hit/Stand/Double)
- Training Steps: 5,000,000 PPO iterations for optimal performance

## File Structure Details

### ppo-agent/models/
- `expert_strategy.csv` - Training data (5,762 expert decisions)
- `expert_pretrained.pth` - PyTorch pretrained model (behavioral cloning)
- `ppo_blackjack_finetuned.zip` - Complete PPO model (5M steps)
- `ppo_blackjack_actor.onnx` - Unity-ready ONNX model

### ppo-agent/training/
- `pretrain.py` - PyTorch behavioral cloning
- `fast_train_rl.py` - PPO reinforcement learning

### ppo-agent/utils/
- `export_onnx.py` - Export PPO actor network to ONNX format
- `export_rl.py` - Alternative export method
- `export_scaler.py` - Extract and display scaling parameters
- `test_env.py` - Environment functionality testing

### unity/ (Complete Unity Project)
- `Assets/Models/ppo_blackjack_actor.onnx` - Trained RL model for Unity inference
- `Assets/Scripts/` - Complete game implementation:
  - `AIAdvisor/` - AI decision system (Basic Strategy, Hi-Lo Counter, Index Strategy)
  - `GameScripts/` - Core blackjack game logic and management
  - `Agents/` - RL agent integration scripts
- `Assets/Scenes/` - Ready-to-play game scenes
- `Assets/Cards/` - Card sprites and textures
- `Assets/Chips/` - Chip sprites and UI elements
- `ProjectSettings/` - Unity project configuration
- `Packages/` - Unity package dependencies

## Requirements

- Python 3.8+
- Unity 2022.3.41f1 (required to run the game)
- See `requirements.txt` for Python dependencies

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

