using UnityEngine;
using TMPro;

public class AIAdvisor : MonoBehaviour
{
    [Header("UI References")]
    public GameObject panel;
    public TMP_Text adviceText;

    void Awake()
    {
        panel.SetActive(false);
    }

    public void ShowAdvice(string advice)
    {
        adviceText.text = advice;
        panel.SetActive(true);
    }

    public void HideAdvice()
    {
        panel.SetActive(false);
    }
}
