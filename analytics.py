import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px
import os
import numpy as np

# ---------------- FIRESTORE CONFIG ----------------
PROJECT_ID = "recipe-project-87528"
SERVICE_ACCOUNT_PATH = r"serviceAccountKey.json"

def init_firestore():
    if not firebase_admin._apps:
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        firebase_admin.initialize_app(cred, {"projectId": PROJECT_ID})
    return firestore.client()

# ---------------- FETCH DATA ----------------
def fetch_data(db):
    recipes_docs = db.collection("recipes").stream()
    interactions_docs = db.collection("interactions").stream()

    recipes = []
    for r in recipes_docs:
        data = r.to_dict()
        data['recipeId'] = r.id
        recipes.append(data)

    interactions = []
    for i in interactions_docs:
        data = i.to_dict()
        data['interactionId'] = i.id
        interactions.append(data)

    df_recipes = pd.DataFrame(recipes)
    df_interactions = pd.DataFrame(interactions)

    # Ensure numeric columns exist
    for col in ['views', 'likes', 'rating']:
        if col in df_interactions.columns:
            df_interactions[col] = pd.to_numeric(df_interactions[col], errors='coerce').fillna(0)
        else:
            df_interactions[col] = 0

    return df_recipes, df_interactions

# ---------------- ANALYTICS ----------------
def compute_insights(df_recipes, df_interactions):
    # Merge interactions with recipe info
    df = df_interactions.merge(
        df_recipes[['recipeId', 'title', 'difficulty', 'prepTimeMinutes', 'ingredients']],
        on='recipeId', how='left'
    )

    # 1. Top 10 Recipes by Views
    top_views = df.groupby('title')['views'].sum().sort_values(ascending=False).head(10)
    print("\n===== Top 10 Recipes by Views =====")
    print(top_views)

    # 2. Top 10 Recipes by Likes
    top_likes = df.groupby('title')['likes'].sum().sort_values(ascending=False).head(10)
    print("\n===== Top 10 Recipes by Likes =====")
    print(top_likes)

    # 3. Top 10 Recipes by Average Rating
    top_rating = df.groupby('title')['rating'].mean().sort_values(ascending=False).head(10)
    print("\n===== Top 10 Recipes by Average Rating =====")
    print(top_rating.round(2))

    # 4. Average Preparation Time
    avg_prep_time = df_recipes['prepTimeMinutes'].mean()
    print(f"\n===== Average Preparation Time =====\n{avg_prep_time:.2f} minutes")

    # 5. Difficulty Distribution
    difficulty_dist = df_recipes['difficulty'].value_counts()
    print("\n===== Difficulty Distribution =====")
    print(difficulty_dist)

    # 6. Correlation between prep time and likes
    if df['likes'].sum() > 0:
        correlation = df.groupby('recipeId')[['prepTimeMinutes','likes']].mean().corr().iloc[0,1]
        print("\n===== Correlation between Prep Time and Likes =====")
        print(f"Correlation coefficient: {correlation:.2f}")
    else:
        correlation = None
        print("\nCorrelation cannot be calculated (likes are all zero)")

    # 7. Most common ingredients
    all_ingredients = []
    for ing_list in df_recipes['ingredients'].dropna():
        for ing in ing_list:
            all_ingredients.append(ing['name'])
    ingredient_counts = Counter(all_ingredients)
    print("\n===== Top 10 Most Common Ingredients =====")
    for ing, count in ingredient_counts.most_common(10):
        print(f"{ing}: {count}")

    # 8. Ingredients associated with high engagement (likes + rating)
    df_exploded = df_recipes.explode('ingredients')
    df_exploded['ingredient_name'] = df_exploded['ingredients'].apply(lambda x: x['name'] if pd.notnull(x) else None)
    merged = df_interactions.merge(df_exploded[['recipeId','ingredient_name']], on='recipeId')
    merged['engagement'] = merged['likes'] + merged['rating']
    ingredient_engagement = merged.groupby('ingredient_name')['engagement'].mean().sort_values(ascending=False).head(10)
    print("\n===== Ingredients Associated with High Engagement =====")
    print(ingredient_engagement.round(2))

    # 9. Recipes with highest like/view ratio
    df_ratio = df.groupby('title').agg({'likes':'sum','views':'sum'})
    df_ratio['like_view_ratio'] = df_ratio['likes'] / df_ratio['views'].replace(0,1)
    top_ratio = df_ratio.sort_values('like_view_ratio', ascending=False).head(10)
    print("\n===== Top Recipes by Like/View Ratio =====")
    print(top_ratio['like_view_ratio'].round(2))

    # 10. Recipes with most interactions
    top_interactions = df.groupby('title')['interactionId'].count().sort_values(ascending=False).head(10)
    print("\n===== Recipes with Most Interactions =====")
    print(top_interactions)

    return top_views, top_likes, top_rating, difficulty_dist, ingredient_counts, ingredient_engagement, df

# ---------------- VISUALIZATION ----------------
def create_charts(top_views, top_likes, top_rating, difficulty_dist, ingredient_counts, ingredient_engagement, df):
    OUTPUT_DIR = "analytics_charts"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Top Views, Likes, Rating
    fig = go.Figure()
    top_titles = top_views.index
    fig.add_trace(go.Bar(
        x=top_titles, y=top_views.values,
        name="Views", marker_color="skyblue", text=top_views.values, textposition="auto"
    ))
    fig.add_trace(go.Bar(
        x=top_titles, y=[top_likes.get(title,0) for title in top_titles],
        name="Likes", marker_color="lightgreen", text=[top_likes.get(title,0) for title in top_titles], textposition="auto"
    ))
    fig.add_trace(go.Bar(
        x=top_titles, y=[top_rating.get(title,0) for title in top_titles],
        name="Avg Rating", marker_color="salmon", text=[round(top_rating.get(title,0),2) for title in top_titles], textposition="auto"
    ))
    fig.update_layout(
        barmode="group",
        title="Top 10 Recipes: Views, Likes & Avg Rating",
        xaxis_title="Recipe",
        yaxis_title="Count / Rating",
        xaxis_tickangle=-45,
        template="plotly_white",
        height=600,
    )
    fig.write_html(os.path.join(OUTPUT_DIR, "top_recipes_engagement.html"))
    fig.show()

    # Difficulty Distribution
    fig2 = go.Figure([go.Bar(x=difficulty_dist.index, y=difficulty_dist.values, text=difficulty_dist.values, textposition="auto")])
    fig2.update_layout(title="Recipe Difficulty Distribution", xaxis_title="Difficulty", yaxis_title="Count", template="plotly_white")
    fig2.write_html(os.path.join(OUTPUT_DIR, "difficulty_distribution.html"))
    fig2.show()

    # Top Ingredients
    top_ingredients = dict(ingredient_counts.most_common(10))
    fig3 = go.Figure([go.Bar(x=list(top_ingredients.keys()), y=list(top_ingredients.values()), text=list(top_ingredients.values()), textposition="auto")])
    fig3.update_layout(title="Top 10 Ingredients", xaxis_title="Ingredient", yaxis_title="Count", template="plotly_white")
    fig3.write_html(os.path.join(OUTPUT_DIR, "top_ingredients.html"))
    fig3.show()

    # Ingredient Engagement
    fig4 = go.Figure([go.Bar(
        x=ingredient_engagement.index,
        y=ingredient_engagement.values,
        text=ingredient_engagement.round(2).values,
        textposition="auto"
    )])
    fig4.update_layout(title="Ingredients Associated with High Engagement", xaxis_title="Ingredient", yaxis_title="Avg Engagement", template="plotly_white")
    fig4.write_html(os.path.join(OUTPUT_DIR, "ingredient_engagement.html"))
    fig4.show()

    # Prep Time vs Likes Scatter
    df_group = df.groupby('recipeId')[['prepTimeMinutes','likes']].mean().reset_index()
    fig5 = px.scatter(df_group, x='prepTimeMinutes', y='likes', text=df_group['recipeId'],
                      title="Prep Time vs Likes Correlation")
    fig5.write_html(os.path.join(OUTPUT_DIR, "prep_time_vs_likes.html"))
    fig5.show()

# ---------------- MAIN ----------------
if __name__ == "__main__":
    db = init_firestore()
    df_recipes, df_interactions = fetch_data(db)
    top_views, top_likes, top_rating, difficulty_dist, ingredient_counts, ingredient_engagement, df = compute_insights(df_recipes, df_interactions)
    create_charts(top_views, top_likes, top_rating, difficulty_dist, ingredient_counts, ingredient_engagement, df)
