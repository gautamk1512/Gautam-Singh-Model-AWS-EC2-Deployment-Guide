# 📊 Gautam Singh AI — Indicators Index

> Single reference file for all trading indicator products.
> To add a new indicator: add entry here + drop .pine file in project root + run `seed_indicators` or add via admin.

---

## 🗂️ All Indicators

| # | Name | Pine File | Price (INR) | Slug | Status |
|---|------|-----------|-------------|------|--------|
| 1 | Gowtham Singh AI Model | `Gowtham_Singh_AI_Model.pine` | ₹2,000 | `gowtham-singh-ai-model` | ✅ Active |
| 2 | Gowtham Singh AI Model V2 | `Gowtham_Singh_AI_Model_v2.pine` | ₹2,500 | `gowtham-singh-ai-model-v2` | ✅ Active |

---

## 📁 Pine Script Files Location

All `.pine` files must be placed in the **project root** (`Gautamsinghmodle/`):

```
Gautamsinghmodle/
├── Gowtham_Singh_AI_Model.pine        ← Indicator #1
├── Gowtham_Singh_AI_Model_v2.pine     ← Indicator #2
├── manage.py
├── db.sqlite3
└── ...
```

---

## 🛠️ How to Add a New Indicator

### Step 1 — Add the Pine file
Drop your `.pine` file into the project root:
```
Gautamsinghmodle/Your_New_Indicator.pine
```

### Step 2 — Add entry to `seed_indicators.py`
Edit: `landing/management/commands/seed_indicators.py`

```python
{
    "name": "Your Indicator Name",
    "slug": "your-indicator-name",
    "short_description": "One-line description for the store card.",
    "description": "Full description of what the indicator does.",
    "price": 1999,                              # Price in INR (integer)
    "pine_script_file": "Your_New_Indicator.pine",
    "features": "Feature 1\nFeature 2\nFeature 3",  # One per line
    "is_active": True,
    "is_popular": False,
    "sort_order": 3,                            # Order in store
},
```

### Step 3 — Run the seed command
```bash
python manage.py seed_indicators
```

### OR — Add via Django Admin
Go to: **http://127.0.0.1:8000/admin/landing/indicatorproduct/add/**

---

## 🔗 Quick Links

| Link | URL |
|------|-----|
| Store Page | http://127.0.0.1:8000/store/ |
| Admin Panel | http://127.0.0.1:8000/admin/ |
| Indicator Admin | http://127.0.0.1:8000/admin/landing/indicatorproduct/ |
| Purchases Admin | http://127.0.0.1:8000/admin/landing/purchase/ |

---

## 📋 Indicator Detail Template Placeholders

When a user purchases and views an indicator, these placeholders in the `.pine` file are auto-replaced:

| Placeholder | Replaced With |
|-------------|--------------|
| `{{EXPIRY_TIMESTAMP}}` | Unix timestamp (ms) of subscription expiry |
| `{{ACCESS_PASSWORD}}` | Auto-generated 8-char access password |

---

_Last updated: April 2026_
