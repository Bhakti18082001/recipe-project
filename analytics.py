import pandas as pd
import plotly.graph_objects as go
import os

DATA_DIR = "data"
OUTPUT_DIR = "analytics_charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load data
recipes = pd.read_csv(os.path.join(DATA_DIR, "recipe.csv"))
interactions = pd.read_csv(os.path.join(DATA_DIR, "interactions.csv"))

# Fill missing type/rating if necessary
interactions["type"] = interactions["type"].fillna("unknown")
interactions["rating"] = interactions["rating"].fillna(0)

# Aggregate interactions
views = interactions[interactions["type"] == "view"].groupby("recipeId").size().rename("views")
likes = interactions[interactions["type"] == "like"].groupby("recipeId").size().rename("likes")
ratings = interactions[interactions["type"] == "rating"].groupby("recipeId")["rating"].mean().rename("avg_rating")

# Combine data
engagement = pd.concat([views, likes, ratings], axis=1).fillna(0)

# Merge with recipe titles
engagement = engagement.merge(recipes[["recipeId", "title"]], left_index=True, right_on="recipeId")

# Select top 10 by views
top_engagement = engagement.sort_values("views", ascending=False).head(10)

# Create interactive bar chart
fig = go.Figure()

fig.add_trace(go.Bar(
    x=top_engagement["title"], y=top_engagement["views"],
    name="Views", marker_color="skyblue", text=top_engagement["views"], textposition="auto"
))
fig.add_trace(go.Bar(
    x=top_engagement["title"], y=top_engagement["likes"],
    name="Likes", marker_color="lightgreen", text=top_engagement["likes"], textposition="auto"
))
fig.add_trace(go.Bar(
    x=top_engagement["title"], y=top_engagement["avg_rating"],
    name="Average Rating", marker_color="salmon", text=top_engagement["avg_rating"].round(2), textposition="auto"
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

# Save interactive HTML
output_file = os.path.join(OUTPUT_DIR, "top_recipes_engagement.html")
fig.write_html(output_file)
print(f"Interactive chart saved to {output_file}")

fig.show()
