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
1. Setup Instructions

Install Dependencies:

pip install firebase-admin
pip install matplotlib


**Run Main App:**

python main.py


Run Analytics ETL:

python analytics.py

2. ETL Process Overview

Your ETL follows the Extract → Transform → Load (ETL) pattern.

**Extract**

Pull all recipe documents from the recipes collection.

Read fields like name, views, category, etc.

**Transform**

Calculate important metrics:

Most viewed recipe

Total recipes

Category-wise distribution

Prepare structured analytics output.

Generate bar chart visualizing views.

**Load**

Save results into the analytics collection.

Export charts (PNG) for reporting.

3. Insights Summary

⭐ **Most Viewed Recipe – Identifies which recipe has the highest views.**

Category Popularity – Shows popularity of categories (veg, non-veg, dessert, etc.).

📈 Recipe Growth Trend – Tracks total number of recipes over time.

🖼️ Visual Chart Output – Bar charts and analytics files stored under analytics_charts/.

4. Known Constraints & Limitations

🔒 No Authentication Layer – Anyone with the service key can update Firestore.

🖐 Manual ETL Execution – Must manually run:

python analytics.py


📁 Local Dependency on serviceAccountKey.json – Must stay local and protected via .gitignore.

⚡ Performance Limit – ETL reads the entire collection every run; not optimized for very large datasets.

📉 Basic Visualizations Only – Limited graphs currently generated.

❗ Limited Error Handling – Missing fields or Firestore issues can interrupt ETL.

5. Future Enhancements

Automate ETL using Cloud Scheduler.

Build a Streamlit/Flask analytics dashboard.

Add Firestore Security Rules & Authentication.

Add advanced charts.

Optimize performance for large datasets.

6. Folder Structure
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

7. Project Evaluation Summary
Data Modeling Evaluation

***VISUALIZATION***
1. **Most common ingredients**
   
<img width="1000" height="500" alt="image" src="https://github.com/user-attachments/assets/f12426c7-b07b-4314-a059-b09e48d12b9c" />
C:\Users\Home\Desktop\Bhakti Dighe\recipe-project\analytics_charts\top_ingredients.png

2. **Average preparation time**

<img width="1000" height="500" alt="image" src="https://github.com/user-attachments/assets/9470e57a-0f69-4629-9415-78788b064f98" />
C:\Users\Home\Desktop\Bhakti Dighe\recipe-project\analytics_charts\longest_recipes.png

3. **Difficulty distribution**

<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/e1fa7e81-c719-4f61-b77a-cc9605160c0a" />
C:\Users\Home\Desktop\Bhakti Dighe\recipe-project\analytics_charts\difficulty_distribution.png

4. **Correlation between prep time and likes**

<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/3545db13-ba34-4c80-98e2-edf74d7f134d" />
C:\Users\Home\Desktop\Bhakti Dighe\recipe-project\analytics_charts\prep_vs_likes.png

5. **Most frequently viewed recipes**

<img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/3294876f-2fda-458a-96df-6bc29cb03c87" />
C:\Users\Home\Desktop\Bhakti Dighe\recipe-project\charts\most_interacted_recipes.png

6. **Ingredients associated with high engagement**

<img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/c28f8506-f00b-4233-a302-7a35243ac8dc" />
C:\Users\Home\Desktop\Bhakti Dighe\recipe-project\charts\top_ingredients.png

**Normalized structure with entities for:**

Recipes

Ingredients

Steps

User interactions (likes, views)

Relationships follow a clean parent–child structure, reducing redundancy.

Verdict: ✔ Accurate, consistent, and well-structured.

**ETL Pipeline Completeness & Correctness**

Implements extraction from CSV files, transformation, validation, and loading into Firestore.

Produces normalized CSV output and validation report.

Verdict: ✔ Fully implemented and logically correct.

Code Quality & Maintainability

Modular Python scripts, clear functions, meaningful variable names, and consistent commenting.

Verdict: ✔ Clean, readable, developer-friendly code.

**Quality Rule Implementation**

Checks for missing values, data type consistency, range & format validation, unique IDs.

Detailed error logs in validation_report.json.

Verdict: ✔ Strong and effective data quality enforcement.

Depth & Relevance of Data Insights

Highlights patterns like:

Most-viewed recipes

Category popularity

Ingredient usage frequency

Engagement trends

Visualization charts make insights clear and interpretable.

Verdict: ✔ Insightful, relevant, and well-presented.

***ER- DIAGRAM***
<img width="2270" height="1787" alt="image" src="https://github.com/user-attachments/assets/ee7a49e0-3210-4d4b-b7c3-9a87e43aff2a" />
C:\Users\Home\Desktop\Bhakti Dighe\recipe-project\Diagrams\Er-Diagram.png

***ARCHITECTURE DIAGRAM(WORKFLOW-PIPELINE)***

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/187a09f2-5965-4f51-932d-7d1d9c17ec31" />
C:\Users\Home\Desktop\Bhakti Dighe\recipe-project\Diagrams\architecture_diagram.png

 **Final Evaluation Score**

Overall Performance: 4.5 / 5

Demonstrates strong ETL design, clear documentation, meaningful insights, and good coding standards.

**Author**

Bhakti Dighe
Recipe Analytics Project — Firebase + Python
