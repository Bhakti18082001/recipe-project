import pandas as pd
import json
from datetime import datetime
import os

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------
DATA_DIR = "data"  # your CSV folder
OUTPUT_FILE = "validation_report.json"

# -------------------------------------------------------------------
# HELPERS
# -------------------------------------------------------------------
def is_valid_timestamp(value):
    if pd.isna(value):
        return False
    try:
        datetime.fromisoformat(str(value).replace("Z", ""))
        return True
    except:
        return False

def fail(reason):
    return {"valid": False, "reason": reason}

def ok():
    return {"valid": True, "reason": ""}

# -------------------------------------------------------------------
# VALIDATION FUNCTIONS
# -------------------------------------------------------------------
def validate_recipes(df):
    results = []

    for _, row in df.iterrows():
        required = ["recipeId", "title", "description", "authorId",
                    "difficulty", "prepTimeMinutes", "cookTimeMinutes",
                    "totalTimeMinutes", "servings", "createdAt", "updatedAt"]

        # Check required fields
        for col in required:
            if pd.isna(row.get(col)):
                results.append(fail(f"Missing required field: {col}"))
                break
        else:
            # Difficulty
            if str(row["difficulty"]).lower() not in ["easy", "medium", "hard"]:
                results.append(fail("Invalid difficulty value"))
                continue

            # Numeric checks
            if row["prepTimeMinutes"] <= 0:
                results.append(fail("prepTimeMinutes must be > 0"))
                continue
            if row["cookTimeMinutes"] < 0:
                results.append(fail("cookTimeMinutes must be >= 0"))
                continue
            if row["prepTimeMinutes"] + row["cookTimeMinutes"] != row["totalTimeMinutes"]:
                results.append(fail("totalTimeMinutes mismatch"))
                continue
            if row["servings"] <= 0:
                results.append(fail("servings must be > 0"))
                continue

            # Timestamp
            if not is_valid_timestamp(row["createdAt"]):
                results.append(fail("Invalid createdAt timestamp"))
                continue
            if not is_valid_timestamp(row["updatedAt"]):
                results.append(fail("Invalid updatedAt timestamp"))
                continue

            results.append(ok())

    return results

def validate_ingredients(df):
    results = []
    for _, row in df.iterrows():
        if pd.isna(row.get("recipeId")):
            results.append(fail("Missing recipeId"))
            continue
        if pd.isna(row.get("ingredientId")):
            results.append(fail("Missing ingredientId"))
            continue
        if pd.isna(row.get("name")) or str(row.get("name")).strip() == "":
            results.append(fail("Invalid ingredient name"))
            continue
        if row.get("quantity") is not None and row["quantity"] < 0:
            results.append(fail("quantity must be >= 0"))
            continue

        results.append(ok())
    return results

def validate_steps(df):
    results = []
    for _, row in df.iterrows():
        if row.get("stepNumber") is None or row["stepNumber"] < 1:
            results.append(fail("stepNumber must be >= 1"))
            continue
        if pd.isna(row.get("instruction")) or str(row.get("instruction")).strip() == "":
            results.append(fail("Invalid instruction"))
            continue
        if row.get("approxMinutes") is not None and row["approxMinutes"] < 0:
            results.append(fail("approxMinutes must be >= 0"))
            continue

        results.append(ok())
    return results

def validate_interactions(df):
    results = []
    for _, row in df.iterrows():
        # Validate timestamp
        if not is_valid_timestamp(row.get("createdAt")):
            results.append(fail("Invalid createdAt timestamp"))
            continue

        # rating validation
        rating = row.get("rating")
        if rating is not None and not pd.isna(rating):
            if not (1 <= rating <= 5):
                results.append(fail("rating must be 1–5"))
                continue

        # difficultyRating validation
        diff_rating = row.get("difficultyRating")
        if diff_rating is not None and not pd.isna(diff_rating):
            if not (1 <= diff_rating <= 5):
                results.append(fail("difficultyRating must be 1–5"))
                continue

        results.append(ok())
    return results

# -------------------------------------------------------------------
# MAIN
# -------------------------------------------------------------------
def summarize(results):
    valid = sum(1 for r in results if r["valid"])
    invalid = len(results) - valid
    return valid, invalid, results

if __name__ == "__main__":
    # Load CSVs
    recipes_df = pd.read_csv(os.path.join(DATA_DIR, "recipe.csv"))
    ingredients_df = pd.read_csv(os.path.join(DATA_DIR, "ingredients.csv"))
    steps_df = pd.read_csv(os.path.join(DATA_DIR, "steps.csv"))
    interactions_df = pd.read_csv(os.path.join(DATA_DIR, "interactions.csv"))

    # Validate
    r1 = validate_recipes(recipes_df)
    r2 = validate_ingredients(ingredients_df)
    r3 = validate_steps(steps_df)
    r4 = validate_interactions(interactions_df)

    # Summarize
    report = {
        "recipes": {"valid": summarize(r1)[0], "invalid": summarize(r1)[1]},
        "ingredients": {"valid": summarize(r2)[0], "invalid": summarize(r2)[1]},
        "steps": {"valid": summarize(r3)[0], "invalid": summarize(r3)[1]},
        "interactions": {
            "valid": summarize(r4)[0],
            "invalid": summarize(r4)[1],
            "invalid_records": [r for r in summarize(r4)[2] if not r["valid"]]
        }
    }

    # Save JSON report
    with open(OUTPUT_FILE, "w") as f:
        json.dump(report, f, indent=4)

    print("Validation complete! Report saved to", OUTPUT_FILE)
