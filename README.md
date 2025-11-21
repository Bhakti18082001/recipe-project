# **🍽️ Recipe Project — Firestore + Python + Analytics**

A Python-based backend project for storing, analyzing, and visualizing recipe data using **Firestore** and a lightweight **ETL pipeline**.

---

## **1. Data Model Explanation**

### **Firestore Collections**

---

### **1. `recipes` Collection**

Each document stores one recipe.

| **Field** | **Type** | **Description** |
|----------|----------|----------------|
| `name` | string | Name of the recipe |
| `ingredients` | array(string) | List of ingredients |
| `steps` | array(string) | Cooking steps |
| `category` | string | Category (veg, non-veg, dessert, etc.) |
| `views` | number | Total views (popularity metric) |
| `createdAt` | timestamp | Auto-generated timestamp |

---

### **2. `analytics` Collection**

Stores aggregated insights.

| **Field** | **Type** | **Description** |
|----------|----------|----------------|
| `topRecipe` | string | Most viewed recipe name |
| `totalRecipes` | number | Total recipe count |
| `categoryDistribution` | map | Count per category |
| `generatedAt` | timestamp | ETL run timestamp |

---

## **2. Instructions for Running the Pipeline**

### **Prerequisites**
- Python 3+
- Firebase Admin SDK
- Valid Firestore `serviceAccountKey.json` (kept locally, not in GitHub)

---

### **Install Dependencies**
```bash
pip install firebase-admin
pip install matplotlib

Run Main App
python main.py

Run Analytics ETL
python analytics.py

3. ETL Process Overview

Your ETL follows the Extract → Transform → Load pattern.

Extract

Pull all recipe documents from the recipes collection.

Read fields like name, views, category, etc.

Transform

Calculate important metrics:

Most viewed recipe

Total recipes

Category-wise distribution

Prepare structured analytics output.

Generate bar chart visualizing views.

Load

Save results into the analytics collection.

Export charts (PNG) for reporting.

4. Insights Summary
⭐ Most Viewed Recipe

Identifies which recipe has the highest views.

📊 Category Distribution

Shows popularity of categories (veg, non-veg, dessert, etc.).

📈 Recipe Growth Trend

Tracks total number of recipes over time.

🖼️ Visual Chart Output

Bar charts and analytics files stored under analytics_charts/.

5. Known Constraints & Limitations
🔒 No Authentication Layer

Anyone with the service key can update Firestore.

🖐 Manual ETL Execution

You must manually run:

python analytics.py

📁 Local Dependency on serviceAccountKey.json

The key must stay local (protected via .gitignore).

⚡ Performance Limit

ETL reads entire collection every run — not optimized for very large datasets.

📉 Basic Visualizations Only

Currently limited graphs generated.

❗ Limited Error Handling

Missing fields or Firestore issues can interrupt ETL.

6. Future Enhancements

Automate ETL using Cloud Scheduler

Build a Streamlit/Flask analytics dashboard

Add Firestore Security Rules

Add authentication

Add advanced charts

Optimize performance for large datasets

📂 Folder Structure
recipe-project/
│── analytics.py
│── seed_firestore.py
│── validate_csv_data.py
│── data/
│── analytics_charts/
│── charts/
│── firestore_export/
│── README.md
│── .gitignore

👩‍💻 Author

Bhakti Dighe
Recipe Analytics Project — Firebase + Python


---

If you want this **exported as a downloadable file (README.md)**, tell me:  
➡️ **“Give me downloadable file”**
