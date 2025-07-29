from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm = PasswordField("Confirm Password", validators=[InputRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class ProfileEditForm(FlaskForm):
    description = TextAreaField("Your Description")
    submit = SubmitField("Save Changes")


class MealNoteForm(FlaskForm):
    notes = TextAreaField("Your Notes")
    video_url = StringField("Video URL (optional)")
    submit = SubmitField("Save Notes")