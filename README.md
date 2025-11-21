# Recipe Analytics Pipeline
recipe-project/
│
├── main.py                   # ETL Pipeline
├── analytics.py              # Charts & insights
├── serviceAccountKey.json    # Firebase key (not uploaded to GitHub)
├── requirements.txt          # Dependencies
├── README.md                 # Documentation
├── data/
│   ├── cleaned_output.csv    # Processed data (after ETL)
│   └── raw_export.json       # Raw extracted data
└── visuals/
    └── most_viewed_chart.png # Saved chart output

## 1. Project Overview
This project collects, processes, and analyzes recipe data from Firestore to generate actionable insights. It includes an ETL pipeline and visualization scripts.

---

## 2. Data Model
- **Recipes Collection**  
  - `recipeId` (string): Unique ID  
  - `name` (string): Recipe name  
  - `category` (string): Cuisine/type  
  - `ingredients` (array): List of ingredients  
  - `views` (number): Number of views  
  - `createdAt` (timestamp): Recipe creation date  

- **Users Collection**  
  - `userId` (string): Unique ID  
  - `name` (string)  
  - `email` (string)  
  - `favorites` (array): Favorite recipe IDs  

- **Interactions Collection**  
  - `interactionId` (string)  
  - `userId` (string)  
  - `recipeId` (string)  
  - `action` (string): view, like, share  
  - `timestamp` (timestamp)  

---

## 3. Running the Pipeline
1. Clone the repository:  
   ```bash
   git clone <repo_url>
   cd recipe-project


          ┌────────────────────┐
          │     Firestore       │
          │  (Recipes, Users,   │
          │   Interactions)     │
          └─────────┬──────────┘
                    │ Extract
                    ▼
          ┌────────────────────┐
          │      Python         │
          │  (main.py - ETL)    │
          └─────────┬──────────┘
                    │ Transform
                    ▼
          ┌────────────────────┐
          │    Processed Data   │
          │  (CSV / JSON Files) │
          └─────────┬──────────┘
                    │ Analyze
                    ▼
          ┌────────────────────┐
          │   analytics.py      │
          │ Data Visualization  │
          └─────────┬──────────┘
                    │ Output
                    ▼
          ┌────────────────────┐
          │ Visuals & Insights │
          └────────────────────┘

2. Install Dependencies
pip install -r requirements.txt

3. Add Firebase Credentials

Place your serviceAccountKey.json file in the project root.

4. Run ETL Pipeline
python main.py

5. Run Analytics Visualization
python analytics.py

📊 ETL Process Overview
🔹 Extract

Pulls Recipes, Users, Interactions from Firestore using Firebase Admin SDK.

🔹 Transform

Data cleaning

Removing null/invalid entries

Aggregating views

Normalizing categories

Preparing analysis-ready format

🔹 Load

Saves cleaned data into /data/cleaned_output.csv

Optionally export to BigQuery

📈 Insights Generated

Most Viewed Recipes

Top Categories

User Engagement Patterns

Recipe Popularity Trends

Daily / Monthly View Patterns

Visual charts are saved inside visuals/.

⚠️ Limitations

Service account key is not committed for security

Visualizations are basic (only top views for now)

No real-time dashboard

Large Firestore datasets may increase read costs

Cloud Functions not implemented yet

📌 Dependencies

Python 3+

firebase-admin

pandas

numpy

matplotlib

plotly

🌟 Future Enhancements

Real-time dashboard (Streamlit / Firebase hosting)

Interactive charts

Advanced ML-based recommendations

BigQuery warehouse integration

