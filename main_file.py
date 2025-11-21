import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
import random

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------
PROJECT_ID = "recipe-project-87528"
SERVICE_ACCOUNT_PATH = r"serviceAccountKey.json"

# -------------------------------------------------------------------
# INIT FIRESTORE
# -------------------------------------------------------------------
def init_firestore():
    if not firebase_admin._apps:
        cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
        firebase_admin.initialize_app(cred, {"projectId": PROJECT_ID})
    return firestore.client()

# -------------------------------------------------------------------
# SEED USERS
# -------------------------------------------------------------------
def seed_users(db):
    now = datetime.utcnow()

    users = [
        {"userId": "user_adi", "displayName": "Adi", "email": "adi@example.com", "createdAt": now, "skillLevel": "intermediate", "dietPreferences": ["vegetarian"]},
        {"userId": "user_chef_1", "displayName": "Home Chef 1", "email": "chef1@example.com", "createdAt": now - timedelta(days=10), "skillLevel": "beginner", "dietPreferences": ["non-veg"]},
        {"userId": "user_chef_2", "displayName": "Home Chef 2", "email": "chef2@example.com", "createdAt": now - timedelta(days=20), "skillLevel": "expert", "dietPreferences": ["vegan"]},
        {"userId": "user_taster_1", "displayName": "Food Lover 1", "email": "food1@example.com", "createdAt": now - timedelta(days=5), "skillLevel": "beginner", "dietPreferences": []},
        {"userId": "user_taster_2", "displayName": "Food Lover 2", "email": "food2@example.com", "createdAt": now - timedelta(days=2), "skillLevel": "intermediate", "dietPreferences": ["vegetarian"]},
        {"userId": "user_bhakti", "displayName": "Bhakti", "email": "bhakti@example.com", "createdAt": now - timedelta(days=1), "skillLevel": "expert", "dietPreferences": ["non-veg"]},
    ]

    for user in users:
        db.collection("users").document(user["userId"]).set(user)

    print(f" Seeded {len(users)} users.")

# -------------------------------------------------------------------
# RECIPE FUNCTIONS
# -------------------------------------------------------------------
def create_surmai_fry_recipe(now):
    return {
        "recipeId": "recipe_surmai_fry",
        "title": "Surmai Fry",
        "description": "Delicious Surmai Fry with aromatic spices and herbs, crispy on the outside and juicy inside.",
        "authorId": "user_bhakti",
        "cuisine": "Indian",
        "category": "Seafood",
        "difficulty": "Medium",
        "prepTimeMinutes": 15,
        "cookTimeMinutes": 20,
        "totalTimeMinutes": 35,
        "servings": 4,
        "ingredients": [
            {"ingredientId": "SF-ING-01", "name": "Surmai (Kingfish) steaks", "quantity": 1000, "unit": "grams", "notes": "cleaned and pat dry"},
            {"ingredientId": "SF-ING-02", "name": "Ginger-garlic paste", "quantity": 2, "unit": "tbsp", "notes": ""},
            {"ingredientId": "SF-ING-03", "name": "Turmeric powder", "quantity": 1, "unit": "tsp", "notes": ""},
            {"ingredientId": "SF-ING-04", "name": "Red chili powder", "quantity": 1, "unit": "tsp", "notes": ""},
            {"ingredientId": "SF-ING-05", "name": "Garam masala", "quantity": 1, "unit": "tsp", "notes": ""},
            {"ingredientId": "SF-ING-06", "name": "Lemon juice", "quantity": 2, "unit": "tbsp", "notes": ""},
            {"ingredientId": "SF-ING-07", "name": "Salt", "quantity": 1, "unit": "tsp", "notes": "adjust to taste"},
            {"ingredientId": "SF-ING-08", "name": "Oil for frying", "quantity": 4, "unit": "tbsp", "notes": "enough to shallow fry"},
            {"ingredientId": "SF-ING-09", "name": "Fresh coriander", "quantity": 2, "unit": "tbsp", "notes": "for garnish"}
        ],
        "steps": [
            {"stepNumber": 1, "instruction": "Clean and pat dry the fish steaks thoroughly.", "approxMinutes": 5},
            {"stepNumber": 2, "instruction": "In a bowl, marinate the fish with ginger-garlic paste, turmeric, red chili powder, garam masala, lemon juice, and salt.", "approxMinutes": 5},
            {"stepNumber": 3, "instruction": "Let it marinate for at least 30 minutes in the refrigerator.", "approxMinutes": 30},
            {"stepNumber": 4, "instruction": "Heat oil in a frying pan over medium flame.", "approxMinutes": 3},
            {"stepNumber": 5, "instruction": "Shallow fry the fish until golden brown and cooked through.", "approxMinutes": 15},
            {"stepNumber": 6, "instruction": "Garnish with coriander and serve hot with rice or roti.", "approxMinutes": 2},
        ],
        "tags": ["seafood", "fish", "fry", "Indian"],
        "createdAt": now - timedelta(days=1),
        "updatedAt": now,
        "isPublic": True,
    }

def create_synthetic_recipe(recipe_id_suffix, title, cuisine, category, difficulty,
                            prep_time, cook_time, servings, author_id, now):
    total_time = prep_time + cook_time
    ingredients = [
        {"ingredientId": f"{recipe_id_suffix}-ING-01", "name": "Onion", "quantity": 1, "unit": "piece", "notes": "finely chopped"},
        {"ingredientId": f"{recipe_id_suffix}-ING-02", "name": "Tomato", "quantity": 2, "unit": "piece", "notes": "pureed"},
        {"ingredientId": f"{recipe_id_suffix}-ING-03", "name": "Oil", "quantity": 2, "unit": "tbsp", "notes": ""},
    ]
    steps = [
        {"stepNumber": 1, "instruction": "Heat oil and sauté onions until golden.", "approxMinutes": 5},
        {"stepNumber": 2, "instruction": "Add tomatoes and cook until soft.", "approxMinutes": 7},
        {"stepNumber": 3, "instruction": "Add spices and cook for 5 minutes.", "approxMinutes": 5},
    ]
    return {
        "recipeId": f"recipe_{recipe_id_suffix}",
        "title": title,
        "description": f"A simple {title} recipe for everyday cooking.",
        "authorId": author_id,
        "cuisine": cuisine,
        "category": category,
        "difficulty": difficulty,
        "prepTimeMinutes": prep_time,
        "cookTimeMinutes": cook_time,
        "totalTimeMinutes": total_time,
        "servings": servings,
        "ingredients": ingredients,
        "steps": steps,
        "tags": [cuisine.lower(), category.lower()],
        "createdAt": now - timedelta(days=random.randint(1, 30)),
        "updatedAt": now - timedelta(days=random.randint(0, 5)),
        "isPublic": True,
    }

# -------------------------------------------------------------------
# SEED RECIPES
# -------------------------------------------------------------------
def seed_recipes(db):
    now = datetime.utcnow()
    recipes = []
    recipes.append(create_surmai_fry_recipe(now))  # Your main recipe first

    synthetic_specs = [
        ("paneer_butter_masala", "Paneer Butter Masala", "Indian", "Main Course", "medium", 20, 25, 3, "user_chef_1"),
        ("veg_pulao", "Veg Pulao", "Indian", "Main Course", "easy", 15, 20, 2, "user_chef_1"),
        ("masala_omelette", "Masala Omelette", "Indian", "Breakfast", "easy", 10, 5, 1, "user_chef_2"),
        ("choco_brownie", "Chocolate Brownie", "American", "Dessert", "medium", 20, 30, 4, "user_chef_2"),
        ("grilled_sandwich", "Grilled Veg Sandwich", "Global", "Snack", "easy", 10, 10, 2, "user_adi"),
        ("veg_maggi", "Masala Veg Maggi", "Indian", "Snack", "easy", 5, 7, 1, "user_adi"),
        ("salad_bowl", "Rainbow Salad Bowl", "Global", "Salad", "easy", 15, 0, 2, "user_taster_1"),
        ("dal_tadka", "Dal Tadka", "Indian", "Main Course", "easy", 15, 20, 3, "user_chef_1"),
        ("fried_rice", "Veg Fried Rice", "Chinese", "Main Course", "medium", 20, 15, 2, "user_chef_2"),
        ("pancakes", "Soft Pancakes", "American", "Breakfast", "easy", 10, 10, 2, "user_taster_2"),
        ("smoothie", "Berry Banana Smoothie", "Global", "Beverage", "easy", 5, 0, 1, "user_taster_2"),
        ("garlic_bread", "Garlic Bread", "Italian", "Snack", "easy", 10, 12, 2, "user_adi"),
        ("tomato_soup", "Tomato Soup", "Global", "Starter", "easy", 10, 15, 2, "user_chef_1"),
        ("veg_wrap", "Veg Wrap", "Global", "Snack", "medium", 15, 10, 1, "user_chef_2"),
        ("lemon_rice", "Lemon Rice", "Indian", "Main Course", "easy", 10, 10, 2, "user_taster_1"),
        ("chicken_curry", "Simple Chicken Curry", "Indian", "Main Course", "medium", 20, 25, 4, "user_chef_1"),
    ]

    for spec in synthetic_specs:
        recipes.append(create_synthetic_recipe(*spec, now))

    for recipe in recipes:
        db.collection("recipes").document(recipe["recipeId"]).set(recipe)

    print(f" Seeded {len(recipes)} recipes.")

# -------------------------------------------------------------------
# SEED INTERACTIONS WITH VIEWS, LIKES, RATINGS
# -------------------------------------------------------------------
def seed_interactions(db):
    now = datetime.utcnow()
    user_ids = ["user_adi", "user_chef_1", "user_chef_2", "user_taster_1", "user_taster_2", "user_bhakti"]

    recipes_stream = db.collection("recipes").stream()
    recipe_ids = [r.id for r in recipes_stream]

    count = 0
    for recipe_id in recipe_ids:
        for user_id in user_ids:
            # Generate fixed views and likes
            views = random.randint(10, 100)
            likes = random.randint(5, views)
            rating = random.randint(3, 5)

            interaction_data = {
                "interactionId": f"{recipe_id}_{user_id}",
                "recipeId": recipe_id,
                "userId": user_id,
                "views": views,
                "likes": likes,
                "rating": rating,
                "createdAt": now - timedelta(days=random.randint(0, 30)),
                "updatedAt": now,
                "source": random.choice(["web", "mobile"])
            }

            db.collection("interactions").document(interaction_data["interactionId"]).set(interaction_data)
            count += 1

    print(f" Seeded {count} interactions with views, likes, and ratings.")

# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------
if __name__ == "__main__":
    db = init_firestore()
    seed_users(db)
    seed_recipes(db)
    seed_interactions(db)
    print(" Seeding complete.")
