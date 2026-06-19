import json
import time
import requests
import websocket

def interact_with_chrome():
    print("[INFO] Connecting to Chrome debugger on port 9222...")
    try:
        # Get the active tab details from Chrome debugger
        response = requests.get("http://127.0.0.1:9222/json")
        tabs = response.json()
        
        # Find the active or relevant AWS tab
        target_tab = None
        for tab in tabs:
            if "signin.aws.amazon.com" in tab.get("url", "") or "console" in tab.get("url", ""):
                target_tab = tab
                break
        
        if not target_tab and len(tabs) > 0:
            target_tab = tabs[0]
            
        if not target_tab:
            print("[ERROR] No open tabs found in Chrome. Please keep Chrome open.")
            return

        ws_url = target_tab["webSocketDebuggerUrl"]
        print(f"[INFO] Connecting to tab: {target_tab.get('title', 'Active Tab')}")
        
        # Connect to Chrome DevTools WebSocket
        ws = websocket.create_connection(ws_url)
        
        # Helper to execute JavaScript
        def run_js(expression):
            payload = {
                "id": 1,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": expression,
                    "returnByValue": True
                }
            }
            ws.send(json.dumps(payload))
            result = json.loads(ws.recv())
            return result.get("result", {}).get("result", {})

        # Let's wait a couple of seconds to make sure page elements are ready
        time.sleep(2)

        # Inject username and password into the DOM
        print("[INFO] Filling in username and password fields...")
        
        # Check IAM Signin page elements
        run_js('if(document.getElementById("username")) { document.getElementById("username").value = "pramesingh1512"; }')
        run_js('if(document.getElementById("password")) { document.getElementById("password").value = "GSirtabc321@"; }')
        
        # Check Root Signin page elements just in case
        run_js('if(document.getElementById("resolving_input")) { document.getElementById("resolving_input").value = "pramesingh1512@gmail.com"; }')
        
        print("[SUCCESS] Credentials successfully filled in Chrome!")
        print("[INFO] Look at the Chrome window on your screen.")
        print("[INFO] Solve any CAPTCHA if prompted, and click 'Sign In' to enter the console.")
        
        ws.close()
        
    except Exception as e:
        print(f"[ERROR] Failed to communicate with Chrome: {e}")
        print("[INFO] Make sure Chrome is open and running on your desktop.")

if __name__ == "__main__":
    interact_with_chrome()
