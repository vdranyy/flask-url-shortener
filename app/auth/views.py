from flask import render_template, redirect, request, \
    url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from app import db
from app.email import send_email
from . import auth
from app.models import User
from .forms import LoginForm, RegistrationForm, \
    ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm, \
    ChangeEmailForm

from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get("next") or url_for("main.index"))
        flash("Wrong username or password")
    return render_template("auth/login.html", form=LoginForm())


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You successfully log out")
    return redirect(url_for("main.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(
            user.email,
            "Confirm registration",
            "auth/email/confirm",
            user=user,
            token=token
        )
        flash("""Confirmation email has been sent to
              your email.""")
        return redirect(url_for("main.index"))
    return render_template("auth/register.html", form=form)


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    if current_user.confirm(token):
        flash("You successfully confirm your registration")
    else:
        flash("Confirmation email broken or expired")
    return redirect(url_for("main.index"))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != "auth.":
        return redirect(url_for("auth.unconfirmed"))


@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("main.index"))
    return render_template("auth/unconfirmed.html")


@auth.route("/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(
        current_user.email,
        "Confirm registration",
        "auth/email/confirm",
        user=current_user,
        token=token
    )
    flash("New confirmation email has been sent to "
          "your email")
    return redirect(url_for("main.index"))


@auth.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash("Your password has been changed")
            return redirect(url_for("main.index"))
        else:
            flash("Wrong password")
    return render_template("auth/change_password.html", form=form)


@auth.route("/reset", methods=["GET", "POST"])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for("main.index"))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(
                user.email, "Reset password",
                "auth/email/reset_password",
                token=token, user=user,
                next=request.args.get("next")
            )
        flash("Email with steps to recover your password has been "
              "sent to your email")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", form=form)


@auth.route("/reset/<token>", methods=["GET", "POST"])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for("main.index"))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for("main.index"))
        if user.reset_password(token, form.password.data):
            flash("Your password has been changed")
            return redirect(url_for("auth.login"))
        else:
            return redirect(url_for("main.index"))
    return render_template("auth/reset_password.html", form=form)


@auth.route("/change-email", methods=["GET", "POST"])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.new_email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(
                new_email,
                "Confirm email",
                "auth/email/change_email",
                user=current_user,
                token=token
            )
            flash("Confirmation email to update your email has been "
                  "sent to your email")
            return redirect(url_for("main.index"))
        else:
            flash("Wrong password or email is already exists")
    return render_template("auth/change_email.html", form=form)


@auth.route("/change-email/<token>", methods=["GET", "POST"])
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash("Your email updated")
    else:
        flash("Wrong request")
    return redirect(url_for("main.index"))
