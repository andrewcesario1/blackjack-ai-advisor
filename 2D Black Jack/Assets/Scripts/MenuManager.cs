using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement; // Import SceneManagement for scene navigation

public class MenuManager : MonoBehaviour
{
    public Button playBtn; // Reference to the Play button
    public Button rulesBtn; // Reference to the Play button

    void Start()
    {
        // Add a listener to the play button that calls the LoadGameScreen method when clicked
        playBtn.onClick.AddListener(LoadGameScreen);
    }

    void LoadGameScreen()
    {
        // Load the Game screen (replace "GameScreenScene" with your actual scene name)
        SceneManager.LoadScene("Game Scene");
    }
}
