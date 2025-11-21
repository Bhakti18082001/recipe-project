# **🍽️ Recipe Project — Firestore + Python + Analytics**

A Python-based backend project for storing, analyzing, and visualizing recipe data using **Firestore** and a lightweight **ETL pipeline**.

---

## **1. Data Model Explanation**

### **Firestore Collections**

---

### **1. `recipes` Collection**

## Firestore Data Model

### 1. recipes Collection
Each document stores one recipe.

| Field       | Type          | Description                                  |
|------------|---------------|----------------------------------------------|
| name       | string        | Name of the recipe                           |
| ingredients| array(string) | List of ingredients                           |
| steps      | array(string) | Cooking steps                                 |
| category   | string        | Recipe category (veg, non-veg, dessert, etc.)|
| views      | number        | Total views (popularity metric)             |
| createdAt  | timestamp     | Auto-generated timestamp                     |

**Highlights:**  
- Tracks recipe popularity via views.  
- Stores structured steps and ingredients for analytics.  
- Enables category-based filtering for dashboards.

---

### 2. users Collection
Each document stores one user.

| Field            | Type           | Description                                  |
|-----------------|----------------|----------------------------------------------|
| name             | string         | User’s full name                             |
| email            | string         | User email address                            |
| createdAt        | timestamp      | Auto-generated timestamp                     |
| preferences      | array(string)  | Optional: User dietary preferences          |
| totalInteractions| number         | Total actions by user (likes, comments, views)|

**Highlights:**  
- Helps analyze user engagement and activity patterns.  
- Enables personalized recommendations based on preferences.  
- Supports tracking of total interactions per user for reporting.

---

### 3. interactions Collection
Each document stores one user interaction with a recipe.

| Field       | Type   | Description                                 |
|------------|--------|---------------------------------------------|
| userId     | string | Reference to `users` document               |
| recipeId   | string | Reference to `recipes` document             |
| type       | string | Type of interaction (`view`, `like`, `comment`) |
| comment    | string | Optional: User comment text                 |
| createdAt  | timestamp | Timestamp of the interaction             |

**Highlights:**  
- Captures all user actions for detailed analytics.  
- Enables calculation of metrics like most-liked recipes, engagement per recipe, and view-to-like ratios.  
- Supports correlation analysis between interactions and recipe characteristics.


--
---
**Folder Structure**
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

**Project Title**: Recipe Analytics Pipeline
**Project Overview:**

This project is designed to collect, process, analyze, and visualize recipe data from user interactions and recipe details. The aim is to provide insights into recipe popularity, user engagement, and ingredient usage to help improve recipe content, optimize user experience, and support data-driven decisions.

**Key Objectives:**

**Data Collection:**

Extract recipe and user interaction data from Firestore (recipes, likes, views, interactions).

Normalize data into structured CSV files for analytics.

**ETL (Extract, Transform, Load) Pipeline:**

Extraction: Fetch data from Firestore collections (recipes, interactions).

Transformation:

Flatten nested ingredients and steps.

Calculate derived metrics like engagement (likes + ratings).

Clean missing values and standardize data types.

Load: Store cleaned and normalized data in CSV files for analysis (ingredients.csv, interactions.csv, recipe.csv, steps.csv).

**Data Validation:**

Validate CSV files for missing values, duplicates, and inconsistent data.

Generate validation report in JSON format.

**Analytics and Insights:**

Identify top recipes by views, likes, average ratings, and like/view ratio.

Determine recipe difficulty distribution (easy vs medium).

Measure average preparation time.

**Calculate correlation between preparation time and likes.**

Find top ingredients and those associated with high engagement.

Highlight recipes with most user interactions.

**Visualization:**

Generate charts to make insights easily understandable:

Top recipes (views, likes, ratings)

Difficulty distribution

Prep time vs likes correlation

Ingredient popularity and engagement

Most interacted recipes

**Deliverables:**

Source code: Python scripts (main_file.py, analytics.py, validate_csv_data.py) 
[View main_file.py](main_file.py)
[View analytics.py](analytics.py)

Normalized CSV outputs (recipe.csv, ingredients.csv, interactions.csv, steps.csv)

Analytics charts (PNG/HTML)

Validation report (validation_report.json)


**ER and architecture diagrams**

**Technical Stack:**

Python Libraries: pandas, matplotlib, seaborn, plotly, collections

Data Storage: Firebase Firestore

Data Format: CSV (normalized tables)

Visualization: PNG & interactive HTML charts

Version Control: Git & GitHub

 ## Main Highlights:##

**Data-Driven Insights:**

Identifies popular and highly engaging recipes.

Helps content creators understand user preferences and engagement trends.

**Normalized Data Structure:**

Ingredients, recipes, interactions, and steps are separated into tables.

Enables easier analytics, aggregation, and visualization.

**Correlation Analysis:**

Checks relationship between prep time and likes to optimize recipe creation.

**Engagement Analytics:**

Ingredients linked to high engagement are identified for recipe optimization.

**Comprehensive Visualization:**

Charts provide a clear view of recipe popularity, ingredient usage, and engagement metrics.

**Scalable Pipeline:**

ETL can handle new recipes and interactions automatically, making the pipeline reusable.

**Business Value:**

Improves recipe recommendation for users.

Helps recipe developers focus on popular ingredients and efficient recipes.

Supports data-driven decisions for content updates and marketing strategies.

Enables performance tracking and trend analysis for recipes over time.

**Project Evaluation Summary**
Data Modeling Evaluation

***VISUALIZATION***
1. **Most common ingredients**
   
<img width="1000" height="500" alt="image" src="https://github.com/user-attachments/assets/f12426c7-b07b-4314-a059-b09e48d12b9c" />

2. **Average preparation time**

<img width="1000" height="500" alt="image" src="https://github.com/user-attachments/assets/9470e57a-0f69-4629-9415-78788b064f98" />

3. **Difficulty distribution**

<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/e1fa7e81-c719-4f61-b77a-cc9605160c0a" />

4. **Correlation between prep time and likes**

<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/3545db13-ba34-4c80-98e2-edf74d7f134d" />

5. **Most frequently viewed recipes**

<img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/3294876f-2fda-458a-96df-6bc29cb03c87" />

6. **Ingredients associated with high engagement**

<img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/c28f8506-f00b-4233-a302-7a35243ac8dc" />

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

***ER- DIAGRAM***
<img width="2270" height="1787" alt="image" src="https://github.com/user-attachments/assets/ee7a49e0-3210-4d4b-b7c3-9a87e43aff2a" />

***ARCHITECTURE DIAGRAM(WORKFLOW-PIPELINE)***

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/187a09f2-5965-4f51-932d-7d1d9c17ec31" />

 **Final Evaluation Score**

Overall Performance: 4.5 / 5

Demonstrates strong ETL design, clear documentation, meaningful insights, and good coding standards.

**Author**

Bhakti Dighe
Recipe Analytics Project — Firebase + Python




