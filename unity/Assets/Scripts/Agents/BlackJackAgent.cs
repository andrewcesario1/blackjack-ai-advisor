// using Unity.MLAgents;
// using Unity.MLAgents.Sensors;
// using Unity.MLAgents.Actuators;

// public class BlackjackAgent : Agent
// {
//     public GameManager game;   // drag your GameManager here

//     public override void Initialize() { }

//     public override void OnEpisodeBegin()
//     {
//         game.ResetForRL();      // you’ll add a method to deal a fresh hand
//     }

//     public override void CollectObservations(VectorSensor sensor)
//     {
//         // 5 floats: playerTotal, isSoft, dealerUp, trueCount, canDouble
//         sensor.AddObservation(game.PlayerTotal);
//         sensor.AddObservation(game.IsSoft ? 1f : 0f);
//         sensor.AddObservation(game.DealerUpValue);
//         sensor.AddObservation(game.TrueCount);
//         sensor.AddObservation(game.CanDouble ? 1f : 0f);
//     }

//     public override void OnActionReceived(ActionBuffers actions)
//     {
//         int act = actions.DiscreteActions[0]; // 0=Hit,1=Stand,2=Double
//         float reward = game.StepRL(act);      // you’ll implement StepRL to apply action, deal next card(s), and return reward
//         SetReward(reward);
//         if (game.IsDone) EndEpisode();
//     }

//     public override void Heuristic(in ActionBuffers actionsOut)
//     {
//         var d = actionsOut.DiscreteActions;
//         // fallback to basic strategy in-editor
//         d[0] = game.BasicAction();
//     }
// }
