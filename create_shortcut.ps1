# PowerShell script to create Desktop Shortcut for J.A.R.V.I.S.
$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [System.Environment]::GetFolderPath('Desktop')
$ProjectPath = Split-Path -Parent $MyInvocation.MyCommand.Path

$ShortcutPath = Join-Path $DesktopPath "J.A.R.V.I.S..lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "wscript.exe"
$Shortcut.Arguments = "`"$ProjectPath\JARVIS.vbs`""
$Shortcut.WorkingDirectory = $ProjectPath
$Shortcut.IconLocation = "$ProjectPath\jarvis.ico, 0"
$Shortcut.Description = "J.A.R.V.I.S. Autonomous Workstation Co-Pilot"
$Shortcut.Save()

Write-Output "SUCCESS: J.A.R.V.I.S. Desktop Shortcut created at $ShortcutPath"

