from flask import Flask, render_template, request,redirect, session,flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, News, Favorite, Vote
from forms import UserForm, LoginForm
import requests

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
    news= News.query.all()
    return render_template('home.html',news=news)

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

@app.route('/refresh-news')
def get_data():
    apikey='f2cb68b3e88142f49ef7ca40c24e4ff3'

    response = requests.get(
        'https://newsapi.org/v2/top-headlines', 
        params={"apiKey":'f2cb68b3e88142f49ef7ca40c24e4ff3', "country":'us'} 
        )
    json_response = response.json()
    #Handle Errors Later

    articles = json_response['articles']
    for i in range(len(articles)):    
        author=articles[i]["author"]
        title=articles[i]["title"]
        description=articles[i]["description"]
        url=articles[i]["url"]
        image_url=articles[i]["urlToImage"]
        publisedAt=articles[i]["publishedAt"]
        content=articles[i]["content"]
        if title and description and url and publisedAt and not News.query.filter_by(url=url).first():
            new_news=News(author=author,title=title,description=description,url=url,image_url=image_url,publisedAt=publisedAt,content=content)
        db.session.add(new_news)

    db.session.commit()
    return redirect('/')

@app.route('/users/<username>/favorites',methods=["GET","POST"])
def user_favorites(username):
    favorites=Favorite.query.all()
    return 


