from app.forms import RegisterForm, LoginForm, CommentForm, CreatePostForm, EditProfileForm
from flask import render_template, redirect, flash, url_for, request, get_flashed_messages
from flask_login import logout_user, current_user, login_user, login_required
from app.models import User, Board, Post, Comment
from app import app, db


@app.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html', title='Feed', account=current_user)

@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', title='Profile', posts=posts, account=user)

@app.route('/board/<bname>', methods=['GET', 'POST'])
@login_required
def board(bname):
    if current_user.is_authenticated:    
        board = Board.query.filter_by(name=bname).first()
        if board is None:
            reason = 'Board'
            return render_template('404.html', reason=reason)
        form = CreatePostForm()
        if form.validate_on_submit():
            post = Post(
                title=form.title.data,
                content=form.text.data,
                board_id=board.id,
                user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
        posts = Post.query.filter_by(board_id=board.id).all()
        return render_template('board.html', title=bname, account=current_user, board=board, form=form, posts=posts)
    return redirect(url_for('login'))

@app.route('/thread/<postid>', methods=['POST', 'GET'])
@login_required
def thread(postid):
    if current_user.is_authenticated:
        post = Post.query.filter_by(id=postid).first()
        comments = Comment.query.filter_by(post_id=postid).all()
        form = CommentForm()
        if form.validate_on_submit():
            print('test')
            comment = Comment(
                text=form.text.data,
                post_id=postid,
                user_id=current_user.id)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('thread', postid=postid))
        return render_template('thread.html', title='Thread', account=current_user, post=post, form=form, comments=comments)

@app.route('/delete_thread/<thread_id>', methods=['POST'])
@login_required
def delete_thread(thread_id):
    post = Post.query.filter_by(id=thread_id).first().delete()
    comments = Comment.query.filter_by(post_id=thread_id).all().delete()
    db.session.commit()

@app.route('/delete_comment/<comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    thread = Comment.query.filter_by(id=comment_id).first()
    comment = Comment.query.filter_by(id=comment_id).first().delete()
    db.session.commit()
    return redirect(url_for('thread', postid=thread.id))

@app.route('/', methods=['GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password.')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('profile', username=user.username, next=request.url))
    return render_template('login.html', title='Login', form=form)

@app.route('/explore', methods=['GET'])
@login_required
def explore():
    return render_template('explore.html', title='Explore', account=current_user)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Register Complete!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register Account', form=form)
