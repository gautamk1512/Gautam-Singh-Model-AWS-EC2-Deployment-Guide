# ═══════════════════════════════════════════════════════════
# Failsafe Windows UI Automation Script
# ═══════════════════════════════════════════════════════════

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName Microsoft.VisualBasic

# Find Chrome Window
$chrome = Get-Process -Name chrome -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -ne "" } | Select-Object -First 1

if ($chrome) {
    Write-Host "[INFO] Found Chrome window: $($chrome.MainWindowTitle)"
    
    # Activate the Chrome window
    [Microsoft.VisualBasic.Interaction]::AppActivate($chrome.Id)
    Start-Sleep -Milliseconds 500
    
    # Type the username
    Write-Host "[INFO] Typing IAM username..."
    [System.Windows.Forms.SendKeys]::SendWait("pramesingh1512")
    Start-Sleep -Milliseconds 300
    
    # Press Tab to move to password field
    [System.Windows.Forms.SendKeys]::SendWait("{TAB}")
    Start-Sleep -Milliseconds 300
    
    # Type the password
    Write-Host "[INFO] Typing password..."
    [System.Windows.Forms.SendKeys]::SendWait("GSirtabc321@")
    Start-Sleep -Milliseconds 300
    
    # Press Enter to log in
    [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
    
    Write-Host "[SUCCESS] Credentials typed successfully!"
} else {
    Write-Host "[ERROR] Could not find any active Chrome window. Please open Chrome first."
}
