using UnityEngine;

public class ExitButton : MonoBehaviour
{
    public void CloseGame()
    {
        // Exits the game when running a build
        Application.Quit();

        // If you are in the editor, log it because Application.Quit won't work in Editor
        #if UNITY_EDITOR
        UnityEditor.EditorApplication.isPlaying = false;
        #endif
    }
}
