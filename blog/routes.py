from blog import app,bcrypt,db
from flask import render_template, redirect, url_for, flash, request, abort
from .forms import RegisterForm, LoginForm, UpdateProfileForm, CreatePostForm
from .models import User, Post
from blog import login_manager
from flask_login import current_user, login_user ,logout_user, login_required
from .decorators import is_login, is_logout




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)




@app.route("/")
def home():
    posts = Post.query.all()
    return render_template("home.html", posts=posts)




@app.route("/register",  methods=['GET', 'POST'])
@is_login
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        
        username = form.username.data
        email = form.email.data
        pass_hash = bcrypt.generate_password_hash(form.password.data)
        user = User(username=username, email=email, password=pass_hash)
        db.session.add(user)
        db.session.commit()

        flash("registered successfully", "success")
        return redirect(url_for('home'))

    return render_template("register.html", form=form)



@app.route("/login",  methods=['GET', 'POST'])
@is_login
def login():
    form = LoginForm()    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.rememberme.data)
            next_page = request.args.get('next')
            flash("login successfully", "success")
            return redirect(next_page if next_page else url_for('home'))
        else:
            flash("Username or password is Wrong !", "danger")

    return render_template("login.html", form=form)




@app.route("/logout")
@is_logout
def logout():
    logout_user()
    flash("logout successfully", "success")
    return redirect(url_for("home"))


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def update_profile():
    form = UpdateProfileForm()

    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        db.session.commit()
        flash('profile updated ', "info")
        redirect(url_for("update_profile"))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    return render_template('profile.html', form=form)
    

@app.route("/create_post", methods=['GET', 'POST'])
@login_required
def create_post():

    form = CreatePostForm()
    if form.validate_on_submit():
        content = form.content.data
        title = form.title.data
        post = Post(content=content, title=title, user=current_user)
        db.session.add(post)
        db.session.commit()
        flash("create a new post", "info")        
        return redirect(url_for("home"))
    return render_template("create_post.html", form=form)


@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post)



@app.route("/post/delete/<int:post_id>", methods=['GET'])
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user == current_user:
        db.session.delete(post)
        db.session.commit()
        flash(f"delete {post.title} successfully" , "info")
        return redirect(url_for('home'))
    else:
        return abort(403)


@app.route("/post/update/<int:post_id>", methods=['GET',"POST"])
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    form = CreatePostForm()
    if post.user == current_user:
        if request.method == "POST":
            if form.validate_on_submit():
                post.content= form.content.data
                post.title= form.title.data 
                db.session.commit()
                flash(f"update {post.title} successfully" , "info")
                return redirect(url_for('home'))
        else:
            form.content.data = post.content
            form.title.data = post.title
            return render_template("update.html", form=form)
    else:
        return abort(403)
