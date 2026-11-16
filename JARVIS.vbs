' ==========================================================
' J.A.R.V.I.S. Standalone Desktop Application Launcher
' Runs server.py completely hidden without showing any console window,
' and launches the dedicated native application frame.
' ==========================================================

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
strDir = fso.GetParentFolderName(WScript.ScriptFullName)

' 1. Start server.py hidden in background (0 = hide window, False = don't wait)
WshShell.Run "python """ & strDir & "\server.py""", 0, False

' 2. Wait 800ms for local bridge port 8765 to initialize
WScript.Sleep 800

' 3. Detect Chrome or Edge executable
chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
chromePathX86 = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
edgePath = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
edgePath64 = "C:\Program Files\Microsoft\Edge\Application\msedge.exe"

profileDir = strDir & "\data\app_profile"
appUrl = "http://localhost:8765"

appExe = ""
If fso.FileExists(chromePath) Then
    appExe = chromePath
ElseIf fso.FileExists(chromePathX86) Then
    appExe = chromePathX86
ElseIf fso.FileExists(edgePath) Then
    appExe = edgePath
ElseIf fso.FileExists(edgePath64) Then
    appExe = edgePath64
End If

If appExe <> "" Then
    ' Launch as standalone Desktop Window with dedicated profile and dimensions
    appCmd = """" & appExe & """ --app=" & appUrl & " --window-size=1360,880 --user-data-dir=""" & profileDir & """"
    WshShell.Run appCmd, 1, False
Else
    ' Fallback to default browser
    WshShell.Run appUrl, 1, False
End If

