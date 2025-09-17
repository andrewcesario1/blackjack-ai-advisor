/// <summary>
/// Tracks the running Hi-Lo count across the current shoe.
/// +1 for 2–6,  0 for 7–9,  –1 for 10/Ace.
/// </summary>
public static class HiLoCounter
{
    public static int RunningCount { get; private set; } = 0;

    public static void UpdateCount(int cardValue)
    {
        if (cardValue >= 2 && cardValue <= 6)      RunningCount++;
        else if (cardValue == 1 || cardValue >= 10) RunningCount--;
        // 7–9 => 0
    }

    public static void UndoCount(int cardValue)
    {
        // exact inverse of UpdateCount
        if (cardValue >= 2 && cardValue <= 6)      RunningCount--;
        else if (cardValue == 1 || cardValue >= 10) RunningCount++;
    }

    public static void Reset()
    {
        RunningCount = 0;
    }
}
