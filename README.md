1. Data Model Explanation
Firestore Collections
1. recipes Collection

Each document represents one recipe.

Field	Type	Description
name	string	Name of the recipe
ingredients	array(string)	List of ingredients
steps	array(string)	Cooking steps
category	string	Category (veg, non-veg, dessert, etc.)
views	number	Count of how many times recipe is viewed
createdAt	timestamp	Auto timestamp
2. analytics Collection

Aggregated insights stored daily.

Field	Type	Description
topRecipe	string	Most viewed recipe
totalRecipes	number	Total number of recipes
categoryDistribution	map	Recipe count by category
generatedAt	timestamp	ETL run timestamp
2. Instructions for Running the Pipeline
Prerequisites

Python 3+

Firebase Admin SDK

Valid Firestore serviceAccountKey.json

Install Dependencies
pip install firebase-admin
pip install matplotlib

Run Main App
python main.py

Run Analytics ETL
python analytics.py

3. ETL Process Overview

Your ETL is a simple Extract → Transform → Load pipeline.

Extract

Read all documents from recipes collection.

Fetch fields: name, category, views, etc.

Transform

Calculate:

Most viewed recipe

Total recipes

Recipes per category

Clean + structure the data

Prepare visual charts (bar chart for most-viewed recipe)

Load

Store aggregated results into analytics collection.

Save visualization images locally (optional).

4. Insights Summary

After running the analytics pipeline, you get:

Top Recipe

The recipe with the highest views.

Category Distribution

How many recipes per category.

Helps understand what type of recipes users prefer.

Growth Trend

Total number of recipes over time.

Useful for dashboards.

Most Viewed Chart

Generated as a bar chart (.png) for reporting.

5. Known Constraints / Limitations
1. No Authentication Layer

Anyone with service key can modify Firestore.

2. ETL is Manual

You must run:

python analytics.py


No automatic scheduler yet.

3. serviceAccountKey.json Must Be Local

The Firebase SDK requires a local JSON file (kept hidden via .gitignore).

4. Performance Limits

Firestore read cost increases with large data.

Analytics script reads whole collection — no pagination.

5. Limited Visualizations

Only one chart (most-viewed) is generated currently.

6. Minimal Error Handling

Failures in Firestore or missing fields may break the script.

Future Enhancements

Add Cloud Scheduler to automate ETL daily

Add Flask/Streamlit dashboard UI

Add Firestore security rules

Add user authentication

Improve visual reports (Plotly, filters, etc.)
