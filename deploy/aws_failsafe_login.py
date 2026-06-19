import time
import os
import ctypes
import subprocess
import webbrowser

# Define key codes
KEYEVENTF_KEYUP = 0x0002
VK_TAB = 0x09
VK_RETURN = 0x0D

def press_key(hexKeyCode):
    ctypes.windll.user32.keybd_event(hexKeyCode, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(hexKeyCode, 0, KEYEVENTF_KEYUP, 0)
    time.sleep(0.05)

def type_string(s):
    for char in s:
        # Convert char to virtual key code
        vk = ctypes.windll.user32.VkKeyScanW(ord(char)) & 0xFF
        # Press key
        ctypes.windll.user32.keybd_event(vk, 0, 0, 0)
        time.sleep(0.02)
        ctypes.windll.user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(0.02)

def automate_aws_login():
    print("[INFO] Launching default browser to AWS IAM Sign-In Page...")
    webbrowser.open("https://933714557819.signin.aws.amazon.com/console")
    
    # Wait for the browser to open and focus
    print("[INFO] Waiting 7 seconds for the browser page to fully load and focus...")
    time.sleep(7)
    
    print("[INFO] Automatically typing IAM Username...")
    type_string("pramesingh1512")
    time.sleep(0.5)
    
    print("[INFO] Pressing Tab...")
    press_key(VK_TAB)
    time.sleep(0.5)
    
    print("[INFO] Automatically typing Password...")
    type_string("GSirtabc321@")
    time.sleep(0.5)
    
    print("[INFO] Pressing Enter to Sign In...")
    press_key(VK_RETURN)
    print("[SUCCESS] Credentials typed into active browser window!")

if __name__ == "__main__":
    automate_aws_login()
