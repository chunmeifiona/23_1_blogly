"""Blogly application."""

import telnetlib
from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'It is secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    return redirect('/users')

@app.route('/users')
def show_all_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template("all_users.html", users=users)

@app.route('/users/new')
def show_add_form():
    """Show the user form for create a new user"""
    return render_template("user_form.html")

@app.route('/users/new', methods=["POST"])
def add_user():
    """Create a user"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]
    image_url = image_url if image_url else None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """Show user details"""
    user = User.query.get_or_404(user_id)
    return render_template("user_details.html", user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_form(user_id):
    """Show the edit page for a user."""
    user=User.query.get_or_404(user_id)
    return render_template("user_edit.html", user=user)

@app.route('/users/<int:user_id>/edit',methods=["POST"])
def edit_user(user_id):
    """Process the edit form, returning the user to the /users page."""
    user=User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]
    user.image_url = user.image_url if user.image_url else None

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete the user."""
    user=User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")
