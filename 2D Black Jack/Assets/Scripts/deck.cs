using System.Collections;
using System.Collections.Generic;
using System;
using UnityEngine;
using static HiLoCounter;



public class deck : MonoBehaviour
{
    public Sprite[] cards;
    int[] cardvalues = new int[53];
    int currentIndex = 0;
    public static event Action OnShuffle;
    
    void Start()
    {
        GetCardValues();
        Shuffle();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    // algorithm to store card values got from kaiser
    void GetCardValues()
    {
        int num = 0;
        for(int i = 0; i < cards.Length; i++)
        {
            // count tp 52 then mod by 13 to get card value
            num = i;
            num %= 13;
            if(num > 10 || num == 0)
            {
                num = 10;
            }
            cardvalues[i] = num++;
        }
        currentIndex = 1;
    }

   public void Shuffle()
   {
        for(int i = cards.Length - 1; i > 0; i--)
        {
            int j = Mathf.FloorToInt(UnityEngine.Random.Range(0.0f, 1.0f) * (cards.Length - 1)) + 1;
            Sprite face = cards[i];
            cards[i] = cards[j];
            cards[j] = face;

            int value = cardvalues[i];
            cardvalues[i] = cardvalues[j];
            cardvalues[j] = value;
        }

        HiLoCounter.Reset(); 
        currentIndex = 1; // Reset the current index after shuffling

        OnShuffle?.Invoke();
   } 
public int DealCard(CardScript cardScript)
{
    if (currentIndex >= cards.Length) 
    {
        // Automatically shuffle and reset if the deck is out of cards
        Debug.Log("Deck is out of cards. Reshuffling...");
        Shuffle();
    }

    int val = cardvalues[currentIndex];
    cardScript.SetSprite(cards[currentIndex]);
    cardScript.SetValue(val);


    currentIndex++;
    // ← update the Hi-Lo count on each dealt card
        Debug.Log($"[DealCard] Dealt {val}. Count before: {RunningCount}");
    HiLoCounter.UpdateCount(val);
    Debug.Log($"[DealCard] Count after:  {RunningCount}");
    return val;
}



    public Sprite GetCardBack()
    {
        return cards[0];
    }
}
