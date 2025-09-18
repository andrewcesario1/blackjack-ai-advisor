using System;
using UnityEngine;

public static class BasicStrategy
{
    // H=Hit, S=Stand, D=Double
    private static readonly string[,] HardTable = {
        { "H","H","H","H","H","H","H","H","H","H" }, // 5
        { "H","H","H","H","H","H","H","H","H","H" }, // 6
        { "H","H","H","H","H","H","H","H","H","H" }, // 7
        { "H","H","H","H","H","H","H","H","H","H" }, // 8
        { "H","D","D","D","D","H","H","H","H","H" }, // 9
        { "D","D","D","D","D","D","D","D","H","H" }, // 10
        { "D","D","D","D","D","D","D","D","D","H" }, // 11
        { "H","H","S","S","S","H","H","H","H","H" }, // 12
        { "S","S","S","S","S","H","H","H","H","H" }, // 13
        { "S","S","S","S","S","H","H","H","H","H" }, // 14
        { "S","S","S","S","S","H","H","H","H","H" }, // 15
        { "S","S","S","S","S","H","H","H","H","H" }, // 16
        { "S","S","S","S","S","S","S","S","S","S" }, // 17+
    };

    private static readonly string[,] SoftTable = {
        { "H","H","H","D","D","H","H","H","H","H" }, // A,2 (13)
        { "H","H","H","D","D","H","H","H","H","H" }, // A,3 (14)
        { "H","H","D","D","D","H","H","H","H","H" }, // A,4 (15)
        { "H","H","D","D","D","H","H","H","H","H" }, // A,5 (16)
        { "H","D","D","D","D","H","H","H","H","H" }, // A,6 (17)
        { "S","D","D","D","D","S","S","H","H","H" }, // A,7 (18)
        { "S","S","S","S","S","S","S","S","S","S" }, // A,8 (19)
        { "S","S","S","S","S","S","S","S","S","S" }, // A,9 (20)
    };

    public static string GetAction(int playerTotal, bool isSoft, int dealerUp)
    {
        int col = dealerUp == 1 ? 9 : dealerUp - 2;
        if (!isSoft)
        {
            int row = Mathf.Clamp(playerTotal, 5, 17) - 5;
            return HardTable[row, col];
        }
        else
        {
            int softVal = playerTotal; // e.g. A+7 = 18
            int row = Mathf.Clamp(softVal, 13, 20) - 13;
            return SoftTable[row, col];
        }
    }
}
