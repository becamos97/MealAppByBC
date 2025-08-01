# Capstone Project - Meal Finder

## API Link
https://www.themealdb.com/api.php


MealApp is a full-stack meal finder and recipe organizer that helps users search for meals based on ingredients they have on hand. It allows users to view full recipes, save meals to a favorites list, and attach personal notes to their favorite recipes.

## What This Site Does

MealApp allows users to:
- Search meals by ingredients
- View recipe instructions, ingredients, and videos
- Save meals to a personal favorites list
- Leave personal notes tied to favorite meals
- View recently searched ingredients
- Toggle between light and dark themes for better usability

The application was built as part of a full-stack capstone project to demonstrate real-world web development skills, including user authentication, API integration, database design, and dynamic front-end behavior.

## Features Implemented

- **Search by Ingredient**: Users input ingredients they have and receive a list of matching meals.
- **Meal Detail Pages**: Meals display detailed instructions, ingredients, and embedded YouTube videos if available.
- **User Authentication**: Secure registration and login/logout functionality using password hashing.
- **Favorites System**: Logged-in users can save meals to their favorites.
- **Personal Notes**: Users can add notes to any of their saved meals to track thoughts or customizations.
- **Theme Toggle**: Persistent dark and light mode options stored in localStorage.
- **Random Suggestions and Recent Ingredients**: Encourage user exploration and repeat interaction.

These features were chosen to give the app a user-focused, practical utility and to demonstrate skills with Flask, SQLAlchemy, forms, session handling, and external APIs.

## Running Tests

Automated tests are located in the `tests/` directory and cover core routes and database interactions. To run tests:

1. Activate your virtual environment
2. Create a test database
3. Run:

pytest

markdown
Copy
Edit

*Note*: Some tests are in progress or currently disabled during refactoring.

## Standard User Flow

1. A new user registers via the signup form.
2. After logging in, they are taken to the homepage where they can enter ingredients.
3. Submitting ingredients leads to a search results page with clickable meal options.
4. Clicking a meal brings them to the detail page with full instructions and a video if available.
5. From there, they can favorite the meal and optionally add a personal note.
6. Their favorite meals and notes are accessible via the navbar links once logged in.

## API Used

This application uses [TheMealDB API](https://www.themealdb.com/api.php) to:
- Search for meals based on ingredients
- Get detailed information about meals including instructions, ingredients, and videos

No custom API was created for this project. TheMealDB provided an accessible and well-documented API which made integration straightforward.

## Technology Stack

- Python
- Flask
- SQLAlchemy
- WTForms
- PostgreSQL
- Bootstrap 5
- JavaScript
- HTML/CSS
- TheMealDB API
- Jinja2
- pytest

## How to Run Locally

1. Clone the repository

2. Create and activate a virtual environment 

3. Install dependencies(pip install -r requirements.txt)

4. Create the database (createdb mealapp)

5. Run the app (flask run)

## Additional Notes

- Application is responsive and styled with Bootstrap
- Project structure is organized for readability
- Comments are added throughout the codebase to explain behavior and note caveats
- Deployment used Heroku or an equivalent platform like Render or Fly.io (replace this note with what you used)

## Final Checklist

- [x] App is deployed and link is included above
- [x] Tests are written and/or being refined
- [x] Code is organized and commented
- [x] README includes all required documentation
- [x] All files pushed to GitHub

