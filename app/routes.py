from app.forms import RegisterForm, LoginForm, CommentForm, CreatePostForm, EditBioForm
from flask import render_template, redirect, flash, url_for, request, get_flashed_messages
from flask_login import logout_user, current_user, login_user, login_required
from app.models import User, Board, Post, Comment
from app import app, db


@app.route('/index', methods=['GET'])
@login_required
def index():
    user = User.query.filter_by(id=current_user.id).first()
    print(user.followed_boards)
    return render_template('index.html', title='Feed', account=current_user)

@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(user_id=user.id).all()
    form = EditBioForm()
    try:
        if form.validate_on_submit():
            user.bio = form.bio.data
            db.session.commit()
    except Exception as e:
        print(e)
        return render_template('404.html', account=current_user, reason='An unexpected error has occurred..')
    return render_template('profile.html', title='Profile', posts=posts, account=user, form=form)

@app.route('/board/<bname>', methods=['GET', 'POST'])
@login_required
def board(bname):
    if current_user.is_authenticated:    
        board = Board.query.filter_by(name=bname).first()
        user = User.query.filter_by(id=current_user.id).first()
        subs = 0
        for i in board.followers:
            subs += 1
        if user in board.followers:
            subbed = True
        else:
            subbed = False
        if board is None:
            reason = 'Board is not found'
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
        return render_template('board.html', title=bname, account=current_user, board=board, form=form, posts=posts, subs=subs, subbed=subbed)
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

@app.route('/follow/<board_id>')
@login_required
def follow(board_id):
    try:
        board = Board.query.filter_by(id=board_id).first()
        user = User.query.filter_by(id=current_user.id).first()
        if user not in board.followers:
            board.followers.append(user)
            db.session.commit()
    except Exception as e:
        print(e)
        return render_template('404.html', reason='Unexpected error has occurred..')
    return redirect(url_for('board', bname=board.name))

@app.route('/unfollow/<board_id>')
@login_required
def unfollow(board_id):
    try:
        board = Board.query.filter_by(id=board_id).first()
        user = User.query.filter_by(id=current_user.id).first()
        if user in board.followers:
            board.followers.remove(user)
            db.session.commit()
    except Exception as e:
        print(e)
        return render_template('404.html', reason='Unexpected error has occurred..')
    return redirect(url_for('board', bname=board.name))


@app.route('/delete_thread/<thread_id>', methods=['GET', 'POST'])
@login_required
def delete_thread(thread_id):
    try:    
        post = Post.query.filter_by(id=thread_id).first()
        board = Board.query.filter_by(id=post.board_id).first()
        comments = Comment.query.filter_by(post_id=thread_id).all()
        for comment in comments:
            db.session.delete(comment)
        db.session.delete(post)
        db.session.commit()
    except Exception as e:
        print(e)
        return render_template('404.html', reason='Thread not found')
    return redirect(url_for('board', bname=board.name))

@app.route('/delete_comment/<comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('thread', postid=comment.post_id))

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
    boards = Board.query.all()
    return render_template('explore.html', title='Explore', account=current_user, boards=boards)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

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
