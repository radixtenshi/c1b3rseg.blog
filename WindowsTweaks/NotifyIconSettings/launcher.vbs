' Runs Enable-TrayIcons.ps1 hidden, without console flash.
Dim shell, cmd
Set shell = CreateObject("Wscript.Shell")
cmd = "powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -WindowStyle Hidden -File """ _
    & Replace(WScript.ScriptFullName, ".vbs", ".ps1") & """"
shell.Run cmd, 0, False
