# Blackjack AI Advisor

A reinforcement learning project that trains a PPO (Proximal Policy Optimization) agent to play blackjack using a custom environment, then exports the learned policy as ONNX for Unity integration. Includes multiple training approaches and evaluation tools.

## Project Structure

```
blackjack-ai-advisor/
│
├── unity/             # Unity game project
│   ├── Assets/
│   │   ├── Scripts/
│   │   │   ├── AIAdvisor/     # AI advisor scripts (Basic Strategy, Hi-Lo Counter, etc.)
│   │   │   ├── GameScripts/   # Core blackjack game logic
│   │   │   └── Agents/        # RL agent integration
│   │   ├── Models/            # Trained ONNX models
│   │   ├── Scenes/           # Unity scenes
│   │   └── ...
│   ├── ProjectSettings/
│   └── Packages/
│
├── ai-agent/          # All ML code: env, training, eval, models 
│   ├── blackjack_env/ # Custom blackjack environment
│   ├── training/      # Multiple training approaches (PyTorch + Sklearn)
│   ├── evaluation/    # Policy evaluation and comparison
│   ├── models/        # Training data + pretrained models
│   ├── utils/         # Export scripts and utilities
│   └── train_agent.py # Complete training pipeline runner
│
├── docs/              # Documentation
├── README.md
├── LICENSE
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
- **Game Scripts**: Complete blackjack game logic with AI integration
- **AI Advisor System**: Real-time decision recommendations using the trained model
- **UI Components**: Cards, chips, and game interface
- **Scenes**: Ready-to-play game scenes

**To run the game:**
1. Open Unity and import the `unity/` folder as a new project
2. Open the "Game Scene" to play blackjack with AI advisor
3. The AI advisor provides real-time recommendations based on the trained PPO model

*Note: The model in Unity is for testing purposes. The training process below can be used to retrain or modify the model.*

### Training the Agent

#### Complete Automated Pipeline
```bash
# Install dependencies
pip install -r requirements.txt

# Run complete training pipeline
cd ai-agent
python train_agent.py
```

#### Manual Step-by-Step
```bash
# Install dependencies
pip install -r requirements.txt

# Step 1: Pretrain with expert data
python ai-agent/training/pretrain.py

# Step 2: Fine-tune with PPO
python ai-agent/training/fast_train_rl.py

# Step 3: Export to ONNX
python ai-agent/utils/export_onnx.py

# Copy the ONNX model to Unity
cp ppo_blackjack_actor.onnx unity/Assets/Models/
```


### Evaluation
```bash
cd ai-agent

# Compare different strategies (RL vs Basic Strategy vs Index Strategy)
python evaluation/compare_policies.py

# Evaluate RL policy performance
python evaluation/evaluate_policy.py

# Run baseline evaluation (Basic Strategy only)
python evaluation/baseline_evaluate.py

# Test environment functionality
python utils/test_env.py
```

## Testing

Run the test suite to verify functionality:

```bash
cd ai-agent
python run_tests.py
```

The tests cover:
- Blackjack environment functionality
- Hand value calculations
- Deck operations
- Data loading and validation
- Model file existence

## Training Approaches

### PyTorch + PPO (Recommended for Unity)
- **Step 1**: Behavioral Cloning pretraining on expert strategy data (`pretrain.py`)
- **Step 2**: PPO fine-tuning with 5M steps (`fast_train_rl.py`)
- **Step 3**: ONNX export for Unity integration (`export_onnx.py`)
- **Result**: `models/ppo_blackjack_actor.onnx` ready for Unity


## Performance Results

### RL Policy Evaluation (5M Steps Training)
- **Episodes**: 100,000
- **Average Reward**: 0.0071 ± 0.9811
- **Win Rate**: 44.42%
- **Loss Rate**: 46.04%
- **Push Rate**: 9.54%

### Baseline Strategy Evaluation
- **Episodes**: 100,000
- **Average Reward**: -0.0048 ± 0.9811
- **Win Rate**: 43.12%
- **Loss Rate**: 47.68%
- **Push Rate**: 9.20%

The RL agent shows **significant improvement** over the baseline strategy, achieving positive average reward compared to the baseline's negative performance.

## Evaluation Results

### Performance Comparison Graph
![RL vs Basic+Index Cumulative Profit](docs/RL%20vs%20Basic%20Strategy%20%2B%20Index%20Deviation.PNG)

### Terminal Output Examples

#### RL Policy Evaluation Results
![RL Policy Evaluation](docs/RL%20Evaluation.PNG)

#### Baseline Strategy Evaluation Results  
![Baseline Strategy Evaluation](docs/Baseline%20Evaluation.PNG)

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

### ai-agent/models/
- `expert_strategy.csv` - Training data (5,762 expert decisions)
- `expert_pretrained.pth` - PyTorch pretrained model (behavioral cloning)
- `ppo_blackjack_finetuned.zip` - Complete PPO model (5M steps)
- `ppo_blackjack_actor.onnx` - Unity-ready ONNX model

### ai-agent/training/
- `pretrain.py` - PyTorch behavioral cloning
- `fast_train_rl.py` - PPO reinforcement learning

### ai-agent/utils/
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

This project is for educational and demonstration purposes.

