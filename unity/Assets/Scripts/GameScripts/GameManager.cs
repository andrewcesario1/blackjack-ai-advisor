using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using static HiLoCounter;
using static IndexStrategy;
using Unity.Barracuda;


public class GameManager : MonoBehaviour
{
    public Button hitBtn;
    public Button standBtn;
    public Button betBtn;
    public Button amountBtn;
    public Button DblBtn;
    public GameScript playerScript;
    public GameScript dealerScript;
    public TMP_Text balanceText;
    public TMP_Text betAmountText;
    public TMP_Text handText;
    public TMP_Text dealerHandText;
    public TMP_Text screenText;
    public GameObject hideCard;
    [Header("AI Advisor")]
    public AIAdvisor advisor;

    [Header("Shuffle Notice")]
    public TMP_Text shuffleNoticeText;
    public float   shuffleNoticeDuration = 2f;

     [Header("RL Advisor")]
    public NNModel rlOnnxModel;
    private IWorker rlWorker;
    private string rlInputName;
    private string rlOutputName;
    private string[] rlActionNames = { "Hit (RL)", "Stand (RL)", "Double (RL)" };
    [Header("RL Policy Scaler / One-Hot")]
    public float[] numMean = {12.5f, 2.5f};
    public float[] numStd  = {5.18812747f, 4.60977223f};
    public int     upMax   = 10;



    int numBetAmount = 0;


    void Start()
    {
        advisor.ShowAdvice($"Running count = {RunningCount}");
        DblBtn.gameObject.SetActive(false);
        hitBtn.gameObject.SetActive(false);
        standBtn.gameObject.SetActive(false);
        betBtn.onClick.AddListener(() => betClicked());
        standBtn.onClick.AddListener(() => standClicked());
        hitBtn.onClick.AddListener(() => hitClicked());
        amountBtn.onClick.AddListener(() => amountBtnClicked());
        DblBtn.onClick.AddListener(() => dblClicked());
        for(int i = 0; i < playerScript.hand.Length-2; i++)
        {
            playerScript.hand[i+2].GetComponent<Renderer>().enabled = false;
            dealerScript.hand[i+2].GetComponent<Renderer>().enabled = false;
        }
        var modelDef = ModelLoader.Load(rlOnnxModel);
        rlInputName  = modelDef.inputs[0].name;
        rlOutputName = modelDef.outputs[0];
        rlWorker     = WorkerFactory.CreateWorker(WorkerFactory.Type.Auto, modelDef);
    }

    void OnDestroy()
    {
        rlWorker?.Dispose();
    }

    private void OnEnable()
    {
        deck.OnShuffle += ShowShuffleNotice;
    }

    private void OnDisable()
    {
        deck.OnShuffle -= ShowShuffleNotice;
    }

    private void ShowShuffleNotice()
    {
        shuffleNoticeText.text = "Reshuffling deck…";
        shuffleNoticeText.gameObject.SetActive(true);
        StartCoroutine(HideShuffleNoticeAfterDelay());
    }

    private IEnumerator HideShuffleNoticeAfterDelay()
    {
        yield return new WaitForSeconds(shuffleNoticeDuration);
        shuffleNoticeText.gameObject.SetActive(false);
    }

    private void dblClicked()
    {
        hitBtn.gameObject.SetActive(false);
        standBtn.gameObject.SetActive(false);
        DblBtn.gameObject.SetActive(false);

        playerScript.UpdateMoney(-numBetAmount);
        numBetAmount *= 2;
        betAmountText.text = numBetAmount.ToString();
        balanceText.text = playerScript.GetBalance().ToString();

        if (playerScript.cardIndex <= 10)
            playerScript.GetCard();

        handText.text = playerScript.handValue.ToString();

        if (playerScript.handValue > 21)
        {
            GameFinished();
            return;
        }

        // after doubling, the correct play is always stand
        advisor.ShowAdvice($"Stand (double done); running count = {RunningCount}");
        standClicked();
    }

    private void amountBtnClicked()
    {
        if(playerScript.GetBalance() >= 100)
        {
            numBetAmount += 100;
            playerScript.UpdateMoney(-100);
            betAmountText.text = numBetAmount.ToString();
            balanceText.text = playerScript.GetBalance().ToString();
        }
        else if(playerScript.GetBalance() == 0 && numBetAmount == 0)
        {
            screenText.text = "Out of Money - Get a job!";
        }
    }

    private void hitClicked()
    {
        DblBtn.gameObject.SetActive(false);

        if (playerScript.cardIndex <= 10)
        {
            playerScript.GetCard();
            handText.text = playerScript.handValue.ToString();

            if (playerScript.handValue > 21)
            {
                // bust → hide advice and finish
                GameFinished();
            }
            else
            {
                string advice = GetAdvice();
                advisor.ShowAdvice($"{advice}; running count = {RunningCount}");
            }
        }
    }
    private void standClicked()
    {
        dealerHandText.gameObject.SetActive(true);
        hideCard.gameObject.SetActive(false);

        // dealer takes all remaining cards—those also get counted in deck.DealCard()
        HitDealer();
        
        int holeVal = dealerScript.hand[0]
            .GetComponent<CardScript>()
            .GetValueOfCard();
        UpdateCount(holeVal);

        // once the hand is over, just display the running count
        advisor.ShowAdvice($"Running count = {RunningCount}");
    }


    private void HitDealer()
    {
        dealerHandText.gameObject.SetActive(true);
        while(dealerScript.handValue < 16 && dealerScript.cardIndex < 10)
        {
            dealerScript.GetCard();
            dealerHandText.text = dealerScript.handValue.ToString();
            if(dealerScript.handValue > 20)
            {
                GameFinished();
            }
        }
        GameFinished();
    }
    private void betClicked()
    {
        // no per-hand shuffle, so count carries over
        playerScript.ResetGame();
        dealerScript.ResetGame();

        hideCard.gameObject.SetActive(true);
        amountBtn.interactable = false;
        screenText.gameObject.SetActive(false);
        dealerHandText.gameObject.SetActive(false);
        betBtn.gameObject.SetActive(false);
        hitBtn.gameObject.SetActive(true);
        standBtn.gameObject.SetActive(true);
        if (playerScript.GetBalance() >= numBetAmount)
            DblBtn.gameObject.SetActive(true);

        playerScript.StartHand();
        dealerScript.StartHand();

        int holeVal = dealerScript.hand[0]
            .GetComponent<CardScript>()
            .GetValueOfCard();
        UndoCount(holeVal);

        hideCard.GetComponent<Renderer>().enabled = true;

        handText.text       = playerScript.handValue.ToString();
        dealerHandText.text = dealerScript.handValue.ToString();
        betAmountText.text  = numBetAmount.ToString();
        balanceText.text    = playerScript.GetBalance().ToString();

        advisor.ShowAdvice($"{GetAdvice()}; running count = {RunningCount}");

        if (playerScript.handValue == 21)
            GameFinished();
    }



    void Update()
    {
        
    }

    void GameFinished()
    {
        if (hideCard.gameObject.activeSelf)
        {
            int holeVal = dealerScript.hand[0]
                .GetComponent<CardScript>()
                .GetValueOfCard();
            UpdateCount(holeVal);
        }
        bool playerBust = playerScript.handValue > 21;
        bool dealerBust = dealerScript.handValue > 21;
        bool player21 = playerScript.handValue == 21;
        bool dealer21 = dealerScript.handValue == 21;

        bool gameFinished = true;

        if(playerBust && dealerBust)
        {
            screenText.text = "All Bust";
            playerScript.UpdateMoney(+numBetAmount); // Return bet if both bust
        }
        else if(playerBust)
        {
            screenText.text = "Dealer wins!";
        }
        else if(dealerBust)
        {
            screenText.text = "You win!";
            playerScript.UpdateMoney(numBetAmount * 2); // Player wins if dealer busts
        }
        else if(dealerScript.handValue > playerScript.handValue)
        {
            screenText.text = "Dealer wins!";
        }
        else if(playerScript.handValue > dealerScript.handValue)
        {
            screenText.text = "You win!";
            playerScript.UpdateMoney(numBetAmount * 2); // Player wins
        }
        else if(playerScript.handValue == dealerScript.handValue)
        {
            screenText.text = "Push";
            playerScript.UpdateMoney(+numBetAmount); // Return bet on tie
        }
        else
        {
            gameFinished = false;
        }

        if(gameFinished)
        {
            hitBtn.gameObject.SetActive(false);
            standBtn.gameObject.SetActive(false);
            DblBtn.gameObject.SetActive(false);
            betBtn.gameObject.SetActive(true);
            screenText.gameObject.SetActive(true);
            dealerHandText.gameObject.SetActive(true);
            hideCard.GetComponent<Renderer>().enabled = false;
            balanceText.text = playerScript.GetBalance().ToString();
            // Reset and shuffle the deck for the next round
            // GameObject.Find("Deck").GetComponent<deck>().Shuffle();
        }
        
        advisor.ShowAdvice($"Running count = {RunningCount}");
        amountBtn.interactable = true;
        numBetAmount = 0;
        betAmountText.text = numBetAmount.ToString();
    }
    private int GetRLAction(int playerTotal, bool isSoft, int dealerUp, int runningCount, bool canDouble)
    {
        var obs = new List<float>(2 + 1 + upMax + 1);
        float[] nums = new float[] { playerTotal, runningCount };
        for (int i = 0; i < nums.Length; i++)
            obs.Add((nums[i] - numMean[i]) / (numStd[i] + 1e-8f));
        obs.Add(isSoft ? 1f : 0f);
        for (int d = 1; d <= upMax; d++)
            obs.Add(d == (dealerUp == 11 ? 1 : dealerUp) ? 1f : 0f);
        obs.Add(canDouble ? 1f : 0f);

        float[] obsArray = obs.ToArray();
        using var inputTensor = new Tensor(1, obsArray.Length, obsArray);
        rlWorker.SetInput(rlInputName, inputTensor);
        rlWorker.Execute();
        using var outputTensor = rlWorker.PeekOutput(rlOutputName);
        float[] logits = outputTensor.ToReadOnlyArray();

        int   best   = 0;
        for (int i = 1; i < logits.Length; i++)
            if (logits[i] > logits[best]) best = i;

        return Mathf.Clamp(best, 0, 2);
    }



    private string GetAdvice()
    {
        int  playerTotal    = playerScript.handValue;
        bool isSoft  = playerScript.aceList.Count > 0 && playerTotal + 10 <= 21;
        int  dealerUp    = dealerScript.hand[0].GetComponent<CardScript>().GetValueOfCard();
        int  runningCount    = HiLoCounter.RunningCount;
        bool canDouble = playerScript.cardIndex == 2;

        int rlAct = GetRLAction(playerTotal, isSoft, dealerUp, runningCount, canDouble);
        if (rlAct == 2 && !canDouble) rlAct = 1;
        return new[] {
            "Advisor: Hit (RL)",
            "Advisor: Stand (RL)",
            "Advisor: Double (RL)"
        }[rlAct];
    }


}
