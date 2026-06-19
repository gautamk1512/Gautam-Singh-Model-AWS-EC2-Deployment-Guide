# 📈 Gautam Singh Trading Indicators

Custom TradingView Pine Script indicators built by **Gautam Singh**.

---

## 📂 Indicators

### 1. `merged_indicator.pine` — SMC + Next Pivot Model
A powerful all-in-one indicator combining **Smart Money Concepts (SMC)** with **correlation-based price forecasting**.

### 2. `gautam_singh_range_nolag.pine` — Range Filter + Zero-Lag MA
A trend-following indicator combining **Zero-Lag Moving Average** with **Range Filter Buy/Sell signals**.

---

## 🔒 Secure License System (For Admins)

Both indicators are protected by a state-of-the-art **Time-Based License System**. The source code is private, and users require active permission to use the tools.

### **How the Protection Works:**
1. **Time-Based Expiry:** The indicator works for specifically allotted timeframes (e.g., 10 days) starting from an activation date.
2. **Rolling License Keys:** You (the admin) generate a new secret license key for every renewal period. Old keys will not work.
3. **Hardware/User Lock:** The indicator verifies the user's TradingView username to prevent sharing licenses.
4. **Complete Lockdown:** If the license is expired, invalid, or unauthorized, the indicator completely hides all plots, signals, and visuals, displaying only an error screen.

### **Admin Instructions: Issuing a License**
To give a user access for 10 days, follow these steps in the Pine Editor before sending them the access:

1. Open the indicator code.
2. Under `─── ADMIN CONTROLS ───`, set the current activation date:
   ```pine
   int act_year   = input.int(2026, "Activation Year", ...)
   int act_month  = input.int(3,    "Activation Month", ...)
   int act_day    = input.int(22,   "Activation Day", ...)
   int lic_days   = input.int(10,   "License Duration (Days)", ...)
   ```
3. Instruct the user to use the static **License Key**: `gautamk1512`
4. Save the indicator and grant the user "Invite-Only" access on TradingView.
5. Provide the user with their active date limit.

---

## 🚀 User Instructions: How to Activate

If you have purchased or been granted access to the Gautam Singh Models, follow these steps to activate your 10-day license.

### Step 1: Add to Chart
Add the indicator to your TradingView chart. You will initially see a red `⛔ UNAUTHORIZED ACCESS` screen.

### Step 2: Open Settings
Click the **⚙️ gear icon** on the indicator to open the settings menu.

### Step 3: Enter Activation Details
Go to the **🔒 LICENSE ACTIVATION** section and enter the following exactly (case-sensitive):

| Field | Value Required |
|---|---|
| **Model Key 1** | `Gautam Singh AI Model` |
| **Model Key 2** | `Gautam Singh AI Trader` |
| **License Key** | `gautamk1512` |
| **Licensed User** | `gautamsingh1207200` |

### Step 4: Confirm Setup
Click **OK**. 
- If successful, the error screen will disappear and a green status bar will appear in the top right showing `✅ Gautam Singh Model | X days remaining`.
- If you see `🔑 INVALID LICENSE KEY` or `⏰ ACCESS EXPIRED`, contact Gautam Singh to renew your license.

---

## 💡 Error Guide

| Error Message | Meaning & Solution |
|---|---|
| `⛔ UNAUTHORIZED ACCESS` | You haven't entered the static Model Keys correctly |
| `🔑 INVALID LICENSE KEY` | The provided key is wrong, or the user username doesn't match |
| `⏰ ACCESS EXPIRED` | Your 10-day license has expired. Contact Gautam to renew. |
| `⏳ LICENSE NOT YET ACTIVE` | The activation date is in the future. Wait until that date. |

---

**Made with ❤️ by Gautam Singh**
