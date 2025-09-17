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
- Multiple Training Approaches: PyTorch + PPO (recommended) or Sklearn MLP (simpler)
- Complete Training Pipeline: Automated script runs full training process
- Unity Integration: Trained model exported as ONNX for real-time gameplay
- Multiple Strategies: Includes basic strategy, Hi-Lo counting, and RL-based decisions
- Comprehensive Evaluation: Baseline comparison and policy evaluation tools
- Ready-to-Use Models: Includes pretrained models for immediate testing

## Quick Start

### Unity Game
1. Open Unity and import the `unity/` folder as a new project
2. Open the "Game Scene" to play blackjack with AI advisor
3. The AI advisor provides real-time recommendations based on the trained PPO model

### Training the Agent

#### Option 1: Complete Automated Pipeline (Recommended)
```bash
# Install dependencies
pip install -r requirements.txt

# Run complete training pipeline
cd ai-agent
python train_agent.py
# Choose option 1 (PyTorch + PPO)
```

#### Option 2: Manual Step-by-Step
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

#### Option 3: Simple Sklearn Approach (No Unity Integration)
```bash
cd ai-agent
python train_agent.py
# Choose option 2 (Sklearn MLP)
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
- Behavioral Cloning: Pretrain on expert strategy data
- PPO Fine-tuning: Reinforcement learning optimization
- ONNX Export: Complete actor network for Unity integration
- Result: `ppo_blackjack_actor.onnx` ready for Unity

### Sklearn MLP (Simpler Alternative)
- Direct Training: Single MLP on expert data
- Faster Training: No reinforcement learning step
- Limited Export: No ONNX support for Unity
- Result: `policy_pretrained.pkl` for analysis only

## Technical Details

- Environment: Custom blackjack environment with hole card visibility
- Algorithm: PPO with behavioral cloning pretraining
- Model: Neural network actor exported to ONNX format
- Features: Hand value, dealer up card, running count, basic strategy deviation
- Integration: ONNX Runtime for Unity inference
- Training Data: 5,762 expert strategy examples
- Model Size: ~14-dimensional input, 3-dimensional output (Hit/Stand/Double)

## File Structure Details

### ai-agent/models/
- `expert_strategy.csv` - Training data (5,762 expert decisions)
- `expert_pretrained.pth` - PyTorch pretrained model
- `policy_pretrained.pkl` - Sklearn pretrained model
- `ppo_blackjack_actor.onnx` - Unity-ready ONNX model
- `ppo_blackjack_finetuned/` - Complete PPO model directory

### ai-agent/training/
- `pretrain.py` - PyTorch behavioral cloning
- `fast_train_rl.py` - PPO reinforcement learning
- `train.py` - Sklearn MLP training

### ai-agent/utils/
- `export_onnx.py` - Export complete actor network
- `export_rl.py` - Alternative export method
- `export_scaler.py` - Extract scaling parameters
- `test_env.py` - Environment testing

## Requirements

- Python 3.8+
- Unity 2022.3+
- See `requirements.txt` for Python dependencies

## License

This project is for educational and demonstration purposes.

