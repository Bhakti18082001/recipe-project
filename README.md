# recipe-project
# Recipe Analytics Pipeline

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
