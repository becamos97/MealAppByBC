# import random
# import requests

# from flask import Flask, render_template, redirect, session, flash, request, url_for
# from models import db, connect_db, User, Favorite
# from forms import RegisterForm, LoginForm, ProfileEditForm, MealNoteForm
# from meal_api import search_meals_by_ingredients, get_meal_details, extract_ingredients, get_random_ingredients

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///meals'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'thisisbrandonsmealapp'
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)

# connect_db(app)

# with app.app_context():
#     db.create_all()

import os
import random
import requests

from urllib.parse import urlparse
from flask import Flask, render_template, redirect, session, flash, request, url_for
from models import db, connect_db, User, Favorite
from forms import RegisterForm, LoginForm, ProfileEditForm, MealNoteForm
from meal_api import search_meals_by_ingredients, get_meal_details, extract_ingredients, get_random_ingredients

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'thisisbrandonsmealapp')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

db_url = os.environ.get('DATABASE_URL', 'postgresql:///meals')
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url

host = urlparse(db_url).hostname or ''
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {'sslmode': 'require'} if host and host not in ('localhost', '127.0.0.1') else {},
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

print(f"[MealApp] DB → {host or 'local-socket'}")

connect_db(app)

#home route

@app.route("/")
def home():
    favorites = []
    recent_ingredients = session.get("recent_ingredients", [])
    random_ingredients = get_random_ingredients()  #Get the random ingredients!

    if "user_id" in session:
        user = User.query.get(session["user_id"])
        favorites = user.favorites

    return render_template(
        "home.html",
        favorites=favorites,
        recent_ingredients=recent_ingredients,
        random_ingredients=random_ingredients  #Pass to template
    )

#register route

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm = form.confirm.data

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return render_template("register.html", form=form)

        existing = User.query.filter_by(username=username).first()
        if existing:
            flash("Username already taken.", "danger")
            return render_template("register.html", form=form)

        user = User.register(username, password)
        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.id
        flash(f"Welcome, {user.username}!", "success")
        return redirect(url_for("home"))

    return render_template("register.html", form=form)

#log in route!

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["user_id"] = user.id
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials. Try again.", "danger")

    return render_template("login.html", form=form)

#log out route

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

#profile route

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    form = ProfileEditForm(obj=user)

    if form.validate_on_submit():
        user.description = form.description.data
        db.session.commit()
        flash("Profile updated!", "success")
        return redirect(url_for("profile"))

    return render_template("profile.html", user=user, form=form)

#search bar route!

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        ingredients = request.form.get("ingredients")
        meals = search_meals_by_ingredients(ingredients)
        if not meals:
            flash("No meals found with those ingredients. Try fewer or simpler ingredients", "danger")
        # Save ingredients to session or flash if needed
        session['search_meals'] = meals
        session['recent_ingredients'] = ingredients
        return redirect(url_for('search'))  # 🔁 Redirect after POST

    meals = session.pop('search_meals', [])
    recent_ingredients = session.pop('recent_ingredients', None)

    return render_template("search.html", meals=meals, recent_ingredients=recent_ingredients)

@app.route("/meal/<meal_id>", methods=["GET", "POST"])
def meal_detail(meal_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    meal = get_meal_details(meal_id)

    if not meal:
        flash("Meal not found.", "danger")
        return redirect(url_for("home"))

    form = MealNoteForm()

    # Check if already favorited
    favorite = Favorite.query.filter_by(user_id=user_id, meal_id=meal_id).first()

    if form.validate_on_submit():
        if not favorite:
            favorite = Favorite(
                user_id=user_id,
                meal_id=meal_id,
                meal_name=meal["strMeal"],
                meal_image=meal["strMealThumb"]
            )
            db.session.add(favorite)

        favorite.notes = form.notes.data
        favorite.video_url = form.video_url.data
        db.session.commit()

        flash("Saved notes and video!", "success")
        return redirect(url_for("meal_detail", meal_id=meal_id))

    # Pre-fill form if favorite already exists
    if favorite:
        form.notes.data = favorite.notes
        form.video_url.data = favorite.video_url

    ingredients = extract_ingredients(meal)

    return render_template("meal_detail.html",
                           meal=meal,
                           ingredients=ingredients,
                           form=form,
                           is_favorited=bool(favorite))

#favorites route

@app.route("/favorites")
def favorites():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    favs = Favorite.query.filter_by(user_id=user_id).all()

    return render_template("favorites.html", favorites=favs)


#adding favorite route

@app.route("/favorite/<meal_id>", methods=["POST"])
def add_favorite(meal_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    meal = get_meal_details(meal_id)

    # Check if already favorited
    existing = Favorite.query.filter_by(user_id=user_id, meal_id=meal_id).first()

    if not existing and meal:
        favorite = Favorite(
            user_id=user_id,
            meal_id=meal_id,
            meal_name=meal["strMeal"],
            meal_image=meal["strMealThumb"]
        )
        db.session.add(favorite)
        db.session.commit()
        flash("Added to favorites!", "success")
    else:
        flash("Meal already favorited.", "info")

    return redirect(url_for("meal_detail", meal_id=meal_id))


#removing favorites route!

@app.route("/unfavorite/<meal_id>", methods=["POST"])
def remove_favorite(meal_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    favorite = Favorite.query.filter_by(
        user_id=session["user_id"], meal_id=meal_id
    ).first()

    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        flash("Removed from favorites!", "warning")

    return redirect(url_for("meal_detail", meal_id=meal_id))

#error 404!

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)