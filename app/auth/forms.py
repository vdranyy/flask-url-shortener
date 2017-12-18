from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from app.models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
        Required(), Length(1, 64), Email()])
    password = PasswordField("Password", validators=[Required()])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[
        Required(), Length(1, 64), Email()])
    username = StringField("Username", validators=[
        Required(), Length(1, 64), Regexp("^[A-Za-z][A-Za-z0-9_.]*$", 0,
                                          "Username can consist only letters, " +
                                          "numbers, dots or underscores")])
    password = PasswordField("Password", validators=[
        Required(), EqualTo("password2", message="Passwords must match")])
    password2 = PasswordField("Confirm password", validators=[Required()])
    submit = SubmitField("Sign in")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email is already registered")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username is already registered")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old password", validators=[Required()])
    password = PasswordField("New password", validators=[
        Required(), EqualTo("password2", message="Passwords must match")])
    password2 = PasswordField("Confirm password", validators=[Required()])
    submit = SubmitField("Change password")


class PasswordResetRequestForm(FlaskForm):
    email = StringField("Email", validators=[
        Required(), Length(1, 64), Email()])
    submit = SubmitField("Reset password")


class PasswordResetForm(FlaskForm):
    email = StringField("Email", validators=[
        Required(), Length(1, 64), Email()])
    password = PasswordField("New password", validators=[
        Required(), EqualTo("password2", message="Passwords must match")])
    password2 = PasswordField("Confirm password", validators=[Required()])
    submit = SubmitField("Reset password")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError("Unknown email")


class ChangeEmailForm(FlaskForm):
    new_email = StringField("New email", validators=[
        Required(), Length(1, 64), Email()])
    password = PasswordField("Password", validators=[Required()])
    submit = SubmitField("Change email")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email is already register")
