import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def launch_and_login():
    print("[INFO] Launching Chrome automation...")
    
    # Configure Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Initialize Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Navigate to AWS IAM console URL
        url = "https://933714557819.signin.aws.amazon.com/console"
        print(f"[INFO] Navigating to {url}...")
        driver.get(url)
        
        # Wait for page to load
        time.sleep(3)
        
        # Fill in IAM Username
        print("[INFO] Entering Username...")
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.clear()
        username_field.send_keys("pramesingh1512")  # Try standard IAM username format
        
        # Fill in Password
        print("[INFO] Entering Password...")
        password_field = driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys("GSirtabc321@")
        
        print("[SUCCESS] Credentials entered automatically! Please check Chrome on your screen.")
        print("[INFO] If there is a CAPTCHA, please solve it and click 'Sign In'.")
        print("[INFO] Keep this Chrome window open so you can generate the Access Keys!")
        
        # Keep browser open
        while True:
            time.sleep(1)
            
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
        # Try root login fallback URL
        try:
            print("[INFO] Attempting root sign-in page fallback...")
            driver.get("https://signin.aws.amazon.com/signin")
            time.sleep(3)
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "resolving_input"))
            )
            email_field.clear()
            email_field.send_keys("pramesingh1512@gmail.com")
            
            # Click next
            next_button = driver.find_element(By.ID, "next_button")
            next_button.click()
            time.sleep(2)
            
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            password_field.clear()
            password_field.send_keys("GSirtabc321@")
            
            print("[SUCCESS] Root login credentials filled! Please check Chrome on your screen.")
            while True:
                time.sleep(1)
        except Exception as e2:
            print(f"[ERROR] Fallback also failed: {e2}")
            while True:
                time.sleep(1)

if __name__ == "__main__":
    launch_and_login()
