import time
from selenium import webdriver

def test_launch():
    print("[INFO] Attempting to launch Chrome via Selenium 4's built-in manager...")
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # run in background
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=options)
        print("[SUCCESS] Chrome launched successfully!")
        driver.get("https://www.google.com")
        print(f"[INFO] Page title: {driver.title}")
        driver.quit()
    except Exception as e:
        print(f"[ERROR] Launch failed: {e}")

if __name__ == "__main__":
    test_launch()
