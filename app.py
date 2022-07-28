"""Blogly application."""

import telnetlib
from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import Tag, db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'It is secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    return redirect('/users')

#***************************************user route****************************************
@app.route('/users')
def show_all_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template("all_users.html", users=users)

@app.route('/users/new')
def show_add_user_form():
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

##***************************************post route******************************************

@app.route('/users/<int:user_id>/posts/new')
def show_add_post_form(user_id):
    """Show form to add a post for that user."""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("post_form.html", user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Handle add form; add post and redirect to the user detail page.."""
    title = request.form["title"]
    content = request.form["content"]
    newPost = Post(title=title, content=content, user_id=user_id)

    tags = request.form.getlist('tag')
    print(tags)

    db.session.add(newPost)
    db.session.commit()

    return redirect("/users")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post."""
    post = Post.query.get_or_404(post_id)
    return render_template("post_details.html", post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show a post."""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("post_edit.html", post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Handle editing of a post. Redirect back to the post view."""
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post.id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete the post."""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

##***************************************tag route******************************************

@app.route('/tags')
def show_all_tags():
    """Lists all tags, with links to the tag detail page."""
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)

@app.route('/tags/new')
def show_tag_form():
    """Shows a form to add a new tag."""
    return render_template("tag_form.html")

@app.route('/tags/new', methods=["POST"])
def add_tag():
    """Process add form, adds tag, and redirect to tag list."""
    name = request.form["tag"]
    newTag = Tag(name=name)

    db.session.add(newTag)
    db.session.commit()
    return redirect("/tags")

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag_details.html", tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """Show edit form for a tag."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag_edit.html", tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag(tag_id):
    """Process edit form, edit tag, and redirects to the tags list.."""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["tag"]

    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Delete the post."""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")