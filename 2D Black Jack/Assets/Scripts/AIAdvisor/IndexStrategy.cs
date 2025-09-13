/// <summary>
/// A small set of count-based deviations (“index plays”).
/// Returns "H", "S", or "D" when a deviation applies; otherwise null.
/// </summary>
public static class IndexStrategy
{
    public static string GetDeviation(int playerTotal, bool isSoft, int dealerUp, int runningCount)
    {
        if (isSoft)
            return null;

        // 16 vs 10: Stand if count ≥ 0
        if (playerTotal == 16 && dealerUp == 10 && runningCount >= 0)
            return "S";

        // 15 vs 10: Stand if count ≥ 4
        if (playerTotal == 15 && dealerUp == 10 && runningCount >= 4)
            return "S";

        // 12 vs 3: Hit if count < 2
        if (playerTotal == 12 && dealerUp == 3 && runningCount < 2)
            return "H";

        // 12 vs 2: Hit if count < 3
        if (playerTotal == 12 && dealerUp == 2 && runningCount < 3)
            return "H";

        // 10 vs Ace: Double if count ≥ 3
        if (playerTotal == 10 && dealerUp == 11 && runningCount >= 3)
            return "D";
        
        // 11 vs Ace
        if (playerTotal == 11 && dealerUp == 11 && runningCount >= 1)
            return "D";

        // 10 vs 10
        if (playerTotal == 10 && dealerUp == 10 && runningCount >= 4)
            return "D";

        // 9 vs 2
        if (playerTotal == 9 && dealerUp == 2 && runningCount >= 1)
            return "D";

        // 9 vs 7
        if (playerTotal == 9 && dealerUp == 7 && runningCount >= 3)
            return "D";

        // 16 vs 9
        if (playerTotal == 16 && dealerUp == 9 && runningCount >= 5)
            return "S";

        // 13 vs 2
        if (playerTotal == 13 && dealerUp == 2 && runningCount >= -1)
            return "S";

        // 12 vs 4
        if (playerTotal == 12 && dealerUp == 4 && runningCount >= 0)
            return "S";

        // 12 vs 5
        if (playerTotal == 12 && dealerUp == 5 && runningCount >= -2)
            return "S";

        // 12 vs 6
        if (playerTotal == 12 && dealerUp == 6 && runningCount >= -1)
            return "S";

        // 15 vs 9
        if (playerTotal == 15 && dealerUp == 9 && runningCount >= 2)
            return "S";

        // no deviation
        return null;
    }
}
