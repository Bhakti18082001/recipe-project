# Visualization.py
import os
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------
# 1️⃣ Load CSV files
# ----------------------
data_folder = r"C:\Users\Home\Desktop\Bhakti Dighe\recipe-project\data"
ingredients = pd.read_csv(os.path.join(data_folder, "ingredients.csv"))
interactions = pd.read_csv(os.path.join(data_folder, "interactions.csv"))

# ----------------------
# 2️⃣ Inspect columns
# ----------------------
print("Ingredients columns:", ingredients.columns)
print("Interactions columns:", interactions.columns)

# ----------------------
# 3️⃣ Merge DataFrames
# ----------------------
merged_df = ingredients.merge(interactions, on="recipeId", how="left")

# If 'interaction_count' does not exist, create it
merged_df['interaction_count'] = 1  # each row = 1 interaction

# ----------------------
# 4️⃣ Prepare charts folder
# ----------------------
charts_folder = r"C:\Users\Home\Desktop\Bhakti Dighe\recipe-project\charts"
os.makedirs(charts_folder, exist_ok=True)

# ----------------------
# 5️⃣ Chart 1: Most frequently viewed recipes
# ----------------------
recipe_engagement = merged_df.groupby('recipeId')['interaction_count'].sum().reset_index()
top_recipes = recipe_engagement.sort_values(by='interaction_count', ascending=False).head(10)

plt.figure(figsize=(10,6))
plt.barh(top_recipes['recipeId'], top_recipes['interaction_count'], color='skyblue')
plt.xlabel("Interaction Count")
plt.ylabel("Recipe ID")
plt.title("Top 10 Most Frequently Viewed Recipes")
plt.gca().invert_yaxis()  # highest at top
plt.tight_layout()
plt.savefig(os.path.join(charts_folder, "top_recipes.png"))
plt.close()

# ----------------------
# 6️⃣ Chart 2: Ingredients associated with high engagement
# ----------------------
ingredient_engagement = merged_df.groupby('name')['interaction_count'].sum().reset_index()
top_ingredients = ingredient_engagement.sort_values(by='interaction_count', ascending=False).head(10)

plt.figure(figsize=(10,6))
plt.barh(top_ingredients['name'], top_ingredients['interaction_count'], color='orange')
plt.xlabel("Total Interactions")
plt.ylabel("Ingredient")
plt.title("Top 10 Ingredients Associated with High Engagement")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join(charts_folder, "top_ingredients.png"))
plt.close()

print("Charts saved in folder:", charts_folder)
