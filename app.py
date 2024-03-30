from flask import Flask, render_template, request,redirect, session,flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, News, Favorite, Vote
from forms import UserForm, LoginForm

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///everyday-news'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']='everyday-news'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False

debug= DebugToolbarExtension(app)
connect_db(app)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/sign-up',methods=["GET","POST"])
def sign_up():
    form=UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password=form.password.data
        first_name=form.first_name.data
        last_name=form.last_name.data
        new_user=User.register(username,password,first_name,last_name)
        db.session.add(new_user)
        db.session.commit()
        session['username']=new_user.username
        return redirect(f"/users/{new_user.username}")
    return render_template('sign_up.html',form=form)

@app.route('/users/<username>')
def show_user(username):
    if 'username' not in session:
        flash('login first to see your account..')
        return redirect('/login')
    user = User.query.filter_by(username=username).first()
    return render_template('user.html',user=user)

@app.route('/login',methods=["GET","POST"])
def log_in():
    form =LoginForm()
    if form.validate_on_submit():
        username =form.username.data
        password =form.password.data
        user = User.authenticate(username,password)
        if user:
            flash(f"Welcome  {user.username}!!")
            session['username'] =user.username
            # id=user.id
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invalid username/password']
    return render_template('login.html',form=form)

@app.route('/logout')
def logout_user():
    session.pop('username')
    return redirect('/login')


