from news_scraper.aggregator import fetch_hacker_news_top_articles, fetch_bbc_top_articles, fetch_cnn_top_articles, fetch_business_insider_top_articles, fetch_tech_crunch_top_articles
from database.email_filters.get_email_filters import get_all_filters_per_user, get_count_filters_per_user
from database.get_db import get_articles, check_login_username, check_password, get_user_from_id
from database.post_db import post_all_articles, reset_artice_table, post_new_user
from database.email_filters.post_email_filters import insert_new_email_filter
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from flask import Flask, render_template, flash, redirect, url_for, request
from apscheduler.schedulers.background import BackgroundScheduler
from forms import LoginForm, SignUpForm, EmailNotificationForm
from utils.db_utils import get_hash, connect_db

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_generated_secret_key'

login = LoginManager()
login.init_app(app)

@login.user_loader
def load_user(id):
    return get_user_from_id(int(id))

def get_all_articles():
    return {
        "Hacker News": fetch_hacker_news_top_articles("https://news.ycombinator.com/"),
        "BBC News": fetch_bbc_top_articles("https://www.bbc.co.uk/news/technology"),
        "CNN News": fetch_cnn_top_articles("https://edition.cnn.com/business/tech"),
        "Business Insider": fetch_business_insider_top_articles(
            "https://www.businessinsider.com/tech"
        ),
        "Tech Crunch": fetch_tech_crunch_top_articles("https://techcrunch.com/"),
    }

# Temporary solution, delete all the contents of the articles table
# and fill it with the new articles once an hour.
def get_new_articles():
    print("GET NEW ARTICLES")
    reset_artice_table()
    post_all_articles(get_all_articles())

scheduler = BackgroundScheduler()
scheduler.add_job(get_new_articles, 'interval', hours=1)
scheduler.start()

@app.route("/")
def index():
    return render_template("index.html", news_sources=get_articles())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = check_login_username(form.username.data)
        if user is None or not check_password(user.username, get_hash(form.password.data)) or not user.is_authenticated:
            flash('Username or password is incorrect', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=True)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        post_new_user(form.username.data, form.email.data, get_hash(form.password.data))
        flash('Sign up successfull', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/new-email-notifications', methods=['GET', 'POST'])
def new_email_notifications():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    form = EmailNotificationForm()
    # if form.validate_on_submit():
    #     if get_count_filters_per_user(current_user.get_email) >= 5:
    #         flash('Too many filters already', 'error')
    #         return redirect(url_for('users_email_notifications'))
    #     else:
    #         insert_new_email_filter(form.key_word.data, current_user.get_email)
    #         flash('New email filter created', 'success')
    return render_template("new_email_notifications.html", form=form)

@app.route('/users_email_notifications')
def users_email_notifications():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # filters = get_all_filters_per_user(current_user.get_email)
    filters = [{'id': 1, 'key_word': "word1"}, {'id': 2, 'key_word': "word2"}]

    return render_template("users_email_notifications.html", filters=filters)

if __name__ == "__main__":
    app.run(debug=True)
