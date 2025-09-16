using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class MenuManager : MonoBehaviour
{
    public Button playBtn;
    public Button rulesBtn;

    void Start()
    {
        playBtn.onClick.AddListener(LoadGameScreen);
    }

    void LoadGameScreen()
    {
        SceneManager.LoadScene("Game Scene");
    }
}
