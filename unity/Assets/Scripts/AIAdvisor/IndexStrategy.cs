// Count-based deviations from basic strategy
public static class IndexStrategy
{
    public static string GetDeviation(int playerTotal, bool isSoft, int dealerUp, int runningCount)
    {
        if (isSoft)
            return null;

        if (playerTotal == 16 && dealerUp == 10 && runningCount >= 0)
            return "S";
        if (playerTotal == 15 && dealerUp == 10 && runningCount >= 4)
            return "S";
        if (playerTotal == 12 && dealerUp == 3 && runningCount < 2)
            return "H";
        if (playerTotal == 12 && dealerUp == 2 && runningCount < 3)
            return "H";
        if (playerTotal == 10 && dealerUp == 11 && runningCount >= 3)
            return "D";
        if (playerTotal == 11 && dealerUp == 11 && runningCount >= 1)
            return "D";
        if (playerTotal == 10 && dealerUp == 10 && runningCount >= 4)
            return "D";
        if (playerTotal == 9 && dealerUp == 2 && runningCount >= 1)
            return "D";
        if (playerTotal == 9 && dealerUp == 7 && runningCount >= 3)
            return "D";
        if (playerTotal == 16 && dealerUp == 9 && runningCount >= 5)
            return "S";
        if (playerTotal == 13 && dealerUp == 2 && runningCount >= -1)
            return "S";
        if (playerTotal == 12 && dealerUp == 4 && runningCount >= 0)
            return "S";
        if (playerTotal == 12 && dealerUp == 5 && runningCount >= -2)
            return "S";
        if (playerTotal == 12 && dealerUp == 6 && runningCount >= -1)
            return "S";
        if (playerTotal == 15 && dealerUp == 9 && runningCount >= 2)
            return "S";
        return null;
    }
}
