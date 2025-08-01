
import random
import string
import requests

BASE_URL = "https://www.themealdb.com/api/json/v1/1"


def search_meals_by_ingredients(ingredients):
    """Search for meals that include given ingredients (comma-separated string)."""
    url = f"{BASE_URL}/filter.php"
    params = {"i": ingredients}
    res = requests.get(url, params=params)

    data = res.json()

    if data["meals"]:
        return data["meals"]  # List of meals with meal ID, name, and thumbnail
    else:
        return []

#gotta get meal details/and ingredients

def get_meal_details(meal_id):
    """Get full details of a meal by its ID."""
    url = f"{BASE_URL}/lookup.php"
    params = {"i": meal_id}
    res = requests.get(url, params=params)

    data = res.json()

    if data["meals"]:
        return data["meals"][0]
    else:
        return None

#getting meal ingredients

def extract_ingredients(meal):
    """Extract ingredients + measures from meal detail object."""
    ingredients = []

    for i in range(1, 21):  # TheMealDB supports up to 20 ingredients
        ing = meal.get(f"strIngredient{i}")
        measure = meal.get(f"strMeasure{i}")

        if ing and ing.strip():
            ingredients.append(f"{measure.strip()} {ing.strip()}")
    
    return ingredients

#This function is supposed to fetch a list of meals, extract all ingredients, and return
#and return 3 random ingredients

def get_random_ingredients():
    """Fetch meals from a random letter and extract 3 interesting random ingredients."""

    COMMON_INGREDIENTS = {
        "salt", "water", "oil", "sugar", "pepper",
        "vegetable oil", "butter"
    }

    letters = 'abcdefghijklmnopqrstuvwxyz'
    random_letter = random.choice(letters)

    res = requests.get(f"{BASE_URL}/search.php?f={random_letter}")
    data = res.json()

    if not data["meals"]:
        return []

    ingredients = set()

    for meal in data["meals"]:
        for i in range(1, 21):
            ing = meal.get(f"strIngredient{i}")
            if ing:
                ing_clean = ing.strip().lower()
                if ing_clean and ing_clean not in COMMON_INGREDIENTS:
                    ingredients.add(ing_clean)

    if not ingredients:
        return []

    return random.sample(list(ingredients), min(3, len(ingredients)))
# === TESTING ===

if __name__ == "__main__":
    print(get_random_ingredients())