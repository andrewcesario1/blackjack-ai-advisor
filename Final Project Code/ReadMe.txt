Blackjack RL Advisor

Overview

This project trains a PPO agent to play blackjack using a fast, 
feature-based environment, then exports the learned policy as 
ONNX to drive an in-game “advisor” in Unity. It also includes 
baseline evaluation scripts (basic strategy + index deviations) 
and all the tooling you need to reproduce training, export scaler 
parameters, convert to ONNX, and benchmark.


NOTE: Requirements.txt was removed all dependencies needed to run are not included in this code
NOTE: Files were moved into folders for organization for observer, the files don't take this new
      structure into account. For ex. fast_train_rl needs expert_pretrained.pth in the same dir
      however expert_pretrained.pth was moved into the Data folder

Requirements used:
pandas
scikit-learn
joblib
d3rlpy
onnx
onnxruntime

/File Structure
├─ Models/
│   └─ ppo_blackjack_actor.onnx      ← Trained PPO actor network (ONNX) for Unity
│
├─ Scripts/
│   ├─ AIAdvisor.cs                  ← Unity UI component: displays advice text
│   ├─ BasicStrategy.cs              ← Hard/soft basic‐strategy tables
│   ├─ HiLoCounter.cs                ← Running‐count update / undo logic
│   └─ IndexStrategy.cs              ← Count‐based deviations (“index plays”)
│
├─ Back Scripts/
│   ├─ CardScript.cs                 ← Unity card visualization & value logic
│   ├─ CloseGame.cs                  ← UI flow: end‐of‐game panel
│   ├─ deck.cs                       ← Unity deck shuffle / deal / Hi-Lo integration
│   ├─ GameScript.cs                 ← Unity hand assembly, ace‐adjustment, money
│   ├─ MenuManager.cs                ← Main menu UI navigation
│   ├─ RulesManager.cs               ← In-game basic‐rules display
│   └─ GameManager.cs                ← Orchestrates game flow, calls RL ONNX & advisor
│
├─ Training/
│   ├─ Blackjack Environment/
│   │   └─ blackjack_env.py          ← Gymnasium env + Hi-Lo + hole-card logic
│   │
│   ├─ Data/
│   │   ├─ expert_strategy.csv       ← Expert‐play dataset (for behavioral cloning)
│   │   ├─ expert_pretrained.pth     ← Pickled scaler + expert MLP weights
│   │   └─ ppo_black_actor.onnx       ← Exported PPO actor (ONNX) used for Unity import
│   │
│   ├─ Evaluate/
│   │   ├─ baseline_evaluate.py      ← Runs basic+index strategy, prints win/push/loss
│   │   ├─ evaluate_policy.py        ← Runs RL policy, prints metrics
│   │   └─ compare_policies.py       ← 1 M-hand CI & cumulative‐profit plot for both
│   │
│   ├─ RL Training/
│   │   ├─ pretrain.py               ← Trains expert MLP + fits ColumnTransformer
│   │   └─ fast_train_rl.py          ← Loads scaler from pretrain, trains PPO in FastObsEnv
│   │
│   └─ Side Scripts/
│       ├─ check_distribution.py     ← (Optional) Analyzes raw expert data distributions
│       ├─ export_scaler.py          ← Dumps scaler.mean_/scale_ to JSON for Unity
│       ├─ export_onnx.py            ← Converts `.zip` PPO actor to ONNX model file
│       └─ test_env.py               ← Sanity-checks Gym env & preprocessing wrapper

