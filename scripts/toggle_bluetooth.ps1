param(
    [string]$Action = "On" # "On" or "Off"
)

try {
    Add-Type -AssemblyName System.Runtime.WindowsRuntime
    $asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { 
        $_.Name -eq 'AsTask' -and 
        $_.GetParameters().Count -eq 1 -and 
        $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' 
    })[0]

    function Await-WinRT($WinRtTask, $ResultType) {
        $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
        $netTask = $asTask.Invoke($null, @($WinRtTask))
        $netTask.Wait(-1) | Out-Null
        return $netTask.Result
    }

    [Windows.Devices.Radios.Radio, Windows.System.Devices, ContentType = WindowsRuntime] | Out-Null
    [Windows.Devices.Radios.RadioKind, Windows.System.Devices, ContentType = WindowsRuntime] | Out-Null
    [Windows.Devices.Radios.RadioState, Windows.System.Devices, ContentType = WindowsRuntime] | Out-Null

    $radios = Await-WinRT ([Windows.Devices.Radios.Radio]::GetRadiosAsync()) ([System.Collections.Generic.IReadOnlyList[Windows.Devices.Radios.Radio]])
    $bt = $radios | Where-Object { $_.Kind -eq 'Bluetooth' }

    if ($bt) {
        $currentState = $bt.State.ToString()
        Write-Output "CURRENT_STATE: $currentState"
        
        $targetState = if ($Action -eq "Off") { [Windows.Devices.Radios.RadioState]::Off } else { [Windows.Devices.Radios.RadioState]::On }
        $res = Await-WinRT ($bt.SetStateAsync($targetState)) ([Windows.Devices.Radios.RadioAccessStatus])
        Write-Output "WINRT_RESULT: $res"

        if ($res -ne "Success") {
            # DeniedByUser means Windows requires user to toggle the switch or permission is restricted.
            # Automated fallback: Open settings and trigger switch toggle
            explorer.exe "ms-settings:bluetooth"
            Start-Sleep -Milliseconds 600
            $wsh = New-Object -ComObject WScript.Shell
            $wsh.SendKeys("{TAB} ")
            Write-Output "TOGGLED_VIA_UI: Opened settings and sent toggle key"
        }
    } else {
        explorer.exe "ms-settings:bluetooth"
        Write-Output "NO_RADIO: Opened settings"
    }
} catch {
    explorer.exe "ms-settings:bluetooth"
    Write-Output "ERROR: $($_.Exception.Message)"
}
