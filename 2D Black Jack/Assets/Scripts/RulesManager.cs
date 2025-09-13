using UnityEngine;
using UnityEngine.UI;

public class RulesManager : MonoBehaviour
{
    public GameObject rulesPanel; // Reference to the panel that displays the rules
    public Button rulesButton; // Button to show the rules panel
    public Button closeButton; // Button to close the rules panel

    void Start()
    {
        // Hide the rules panel initially
        rulesPanel.SetActive(false);

        // Add listeners to the buttons
        rulesButton.onClick.AddListener(ShowRules);
        closeButton.onClick.AddListener(CloseRules);
    }

    // Show the rules panel
    void ShowRules()
    {
        rulesPanel.SetActive(true);
    }

    // Hide the rules panel
    void CloseRules()
    {
        rulesPanel.SetActive(false);
    }
}
