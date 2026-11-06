from marshmallow import ValidationError
from api import app, verify_password
from api.forms.user import UserRegistrationForm, UserLogInForm
from flask import abort, jsonify, render_template, redirect, url_for, session, request
from api.schemas.user import user_schema
from flask_babel import _


@app.route("/")
@app.doc(summary="Main page", description="Main page", tags=["pages"])
def index():
    """Main page"""
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
@app.doc(summary="User registration page", description="User registration page", tags=["pages"])
def user_registration():
    """User registration page"""
    form = UserRegistrationForm()

    if form.validate_on_submit():
        try:
            user = user_schema.load(form.data)
        except ValidationError as e:
            abort(400, _("Validation error: %(error)s", error=str(e)))

        user.save()

        return redirect(url_for("registration_success"))

    context = {"form": form}

    return render_template("registration.html", **context)


@app.route("/registration_success")
@app.doc(summary="Success user registration page", description="Success user registration page", tags=["pages"])
def registration_success():
    """Success user registration page"""
    return jsonify(message=_("Registration successfull"))


@app.route("/login", methods=["GET", "POST"])
@app.doc(summary="Login user page", description="Login user page", tags=["pages"])
def user_login():
    """Login user page"""
    form = UserLogInForm()

    if form.validate_on_submit():
        user = verify_password(form.username.data, form.password.data)
        if user:
            session["username"] = user.username
            return redirect(url_for("login_success"))
        else:
            form.username.errors += (_("User identification error"),)

    context = {"form": form}

    return render_template("login.html", **context)


@app.route("/login_success")
@app.doc(summary="Success user login page", description="Success user login page", tags=["pages"])
def login_success():
    """Success user login page"""  
    return jsonify(message=_("Wellcome, %(username)s!", username=session.get("username")))