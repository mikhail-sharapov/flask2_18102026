from marshmallow import ValidationError
from api import app, verify_password, multi_auth
from api.forms.user import UserRegistrationForm, UserLogInForm
from flask import abort, jsonify, render_template, redirect, url_for
from api.schemas.user import user_schema


@app.route("/")
def index():
    """Main page"""
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def user_registration():
    """User registration page
    TODO. Check repeat_password validation"""
    form = UserRegistrationForm()

    if form.validate_on_submit():
        try:
            user = user_schema.load(form.data)
        except ValidationError as e:
            abort(400, f"Validation error: {str(e)}")

        user.save()

        return redirect(url_for("registration_success"))

    context = {"form": form}

    return render_template("registration.html", **context)


@app.route("/registration_success")
def registration_success():
    """Success user registration page"""
    return jsonify(message="Registration successfull")


@app.route("/login", methods=["GET", "POST"])
def user_login():
    """LogIn user"""
    form = UserLogInForm()

    if form.validate_on_submit():
        user = verify_password(form.username.data, form.password.data)
        if user:
            return redirect(url_for("login_success"))
        else:
            form.username.errors += ("User identification error",)

    context = {"form": form}

    return render_template("login.html", **context)


@app.route("/login_success")
def login_success():
    """Success user login page"""
    return jsonify(message=f"Wellcome!")