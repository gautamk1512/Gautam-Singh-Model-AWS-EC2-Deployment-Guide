import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def slow_type(element, text):
    element.clear()
    for char in text:
        element.send_keys(char)
        time.sleep(0.1)

def automate_aws_keys():
    print("[INFO] Launching background Chrome browser...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    # Add modern user-agent to avoid bot detection
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Step 1: Navigate to IAM console login
        url = "https://933714557819.signin.aws.amazon.com/console"
        print(f"[INFO] Navigating to sign-in page: {url}")
        driver.get(url)
        time.sleep(5)
        
        # Step 2: Fill credentials
        print("[INFO] Filling in login details...")
        
        # Wait for username and type slowly
        username_field = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "username"))
        )
        # Click first to focus
        ActionChains(driver).move_to_element(username_field).click().perform()
        time.sleep(0.5)
        slow_type(username_field, "pramesingh1512")
        
        # Fill password
        password_field = driver.find_element(By.ID, "password")
        ActionChains(driver).move_to_element(password_field).click().perform()
        time.sleep(0.5)
        slow_type(password_field, "GSirtabc321@")
        
        # Force set via JavaScript as a fallback to be 100% sure
        driver.execute_script('document.getElementById("username").value = "pramesingh1512";')
        driver.execute_script('document.getElementById("password").value = "GSirtabc321@";')
        
        # Save a screenshot to verify they are filled before clicking submit
        driver.save_screenshot("aws_filled_verify.png")
        print("[INFO] Saved input verification screenshot to 'aws_filled_verify.png'")
        
        # Step 3: Click sign in
        print("[INFO] Clicking Sign In...")
        signin_button = driver.find_element(By.ID, "signin_button")
        ActionChains(driver).move_to_element(signin_button).click().perform()
        
        # Wait up to 15 seconds for successful login and redirect
        print("[INFO] Waiting for redirect...")
        WebDriverWait(driver, 20).until(
            lambda d: "signin" not in d.current_url and "home" in d.current_url
        )
        print(f"[INFO] Successfully logged in! Current URL: {driver.current_url}")
        
        # Step 4: Navigate directly to Security Credentials page
        cred_url = "https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-1#/security_credentials"
        print(f"[INFO] Navigating to credentials page: {cred_url}")
        driver.get(cred_url)
        time.sleep(8)
        
        driver.save_screenshot("aws_credentials_page.png")
        print("[INFO] Saved credentials page screenshot to 'aws_credentials_page.png'")
        
        # Step 5: Click "Create access key"
        print("[INFO] Clicking 'Create access key'...")
        create_btn = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Create access key')] | //awsui-button[contains(., 'Create access key')]//button"))
        )
        driver.execute_script("arguments[0].click();", create_btn)
        time.sleep(4)
        
        # Step 6: Choose Command Line Interface (CLI)
        print("[INFO] Selecting CLI option...")
        cli_radio = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@value='cli'] | //span[contains(text(), 'Command Line Interface')]"))
        )
        driver.execute_script("arguments[0].click();", cli_radio)
        time.sleep(1)
        
        # Try checking agreement checkmark if it exists
        try:
            agreement = driver.find_element(By.XPATH, "//input[@type='checkbox'] | //span[contains(text(), 'I understand the recommendation')]")
            driver.execute_script("arguments[0].click();", agreement)
            time.sleep(1)
        except:
            pass
            
        # Click Next
        next_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Next')] | //awsui-button[contains(., 'Next')]//button")
        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(2)
        
        # Click Create
        create_btn2 = driver.find_element(By.XPATH, "//button[contains(text(), 'Create access key')] | //awsui-button[contains(., 'Create access key')]//button")
        driver.execute_script("arguments[0].click();", create_btn2)
        time.sleep(5)
        
        driver.save_screenshot("aws_keys_created.png")
        print("[INFO] Saved created keys screenshot to 'aws_keys_created.png'")
        
        # Step 7: Retrieve the keys!
        print("[INFO] Extracting keys from page...")
        
        # Access key is usually a text block starting with AKIA
        access_key_el = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'AKIA')]"))
        )
        access_key = access_key_el.text.strip()
        
        # Secret key is normally in the second table cell or in an input field
        secret_key_el = driver.find_element(By.XPATH, "//td[2] | //span[contains(text(), '/')] | //div[contains(@class, 'secret')]")
        secret_key = secret_key_el.text.strip()
        
        if access_key and "AKIA" in access_key:
            print(f"[SUCCESS] Retracted Access Key: {access_key}")
            
            # Write standard AWS configs
            aws_dir = os.path.expanduser("~/.aws")
            os.makedirs(aws_dir, exist_ok=True)
            
            with open(os.path.join(aws_dir, "credentials"), "w") as f:
                f.write(f"[default]\naws_access_key_id = {access_key}\naws_secret_access_key = {secret_key}\n")
                
            with open(os.path.join(aws_dir, "config"), "w") as f:
                f.write("[default]\nregion = ap-southeast-2\noutput = json\n")
                
            print("[SUCCESS] AWS Local Credentials Configured Successfully!")
        else:
            print("[ERROR] Failed to extract keys from success page.")
            
    except Exception as e:
        print(f"[ERROR] Automation failed: {e}")
        try:
            driver.save_screenshot("aws_error_debug.png")
            print("[INFO] Saved failure screenshot to 'aws_error_debug.png'")
        except:
            pass
    finally:
        driver.quit()

if __name__ == "__main__":
    automate_aws_keys()
