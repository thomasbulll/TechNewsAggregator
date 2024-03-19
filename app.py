from news_scraper.aggregator import fetch_hacker_news_top_articles, fetch_bbc_top_articles, fetch_cnn_top_articles, fetch_business_insider_top_articles, fetch_tech_crunch_top_articles, fetch_venture_beat_top_articles, fetch_wired_top_articles, fetch_sky_news_top_articles, fetch_reddit_top_articles
from database.email_filters.post_email_filters import insert_new_email_filter, delete_specific_email_filter_by_id
from database.email_filters.get_email_filters import get_all_filters_per_user, get_count_filters_per_user
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from database.user.get_user import check_login_username, check_password, get_user_from_id
from flask import Flask, render_template, flash, redirect, url_for, request
from database.post_db import post_all_articles, reset_artice_table
from apscheduler.schedulers.background import BackgroundScheduler
from forms import LoginForm, SignUpForm, EmailNotificationForm
from email_notifications import check_all_filters
from database.user.post_user import post_new_user
from utils.db_utils import get_hash, connect_db
from database.get_db import get_articles, get_all_hashes
from short_form_content import generate_short_videos
from dotenv import load_dotenv
from config import Config

app = Flask(__name__)
load_dotenv()
app.config.from_object(Config)
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
        "Sky News": fetch_sky_news_top_articles("https://news.sky.com/technology/"),
        "Wired": fetch_wired_top_articles("https://www.wired.co.uk/topic/technology/"),
        "Venture Beat": fetch_venture_beat_top_articles("https://venturebeat.com/"),
        "Reddit Tech News": fetch_reddit_top_articles("https://www.reddit.com/r/technews/", 0),
        "Reddit Tech": fetch_reddit_top_articles("https://www.reddit.com/r/tech/", 0),
        "Reddit Technology": fetch_reddit_top_articles("https://www.reddit.com/r/technology/", 0), # To avoid pinned - set offset to 1 (as of commit date)
        "Reddit Software": fetch_reddit_top_articles("https://www.reddit.com/r/software/", 0), # To avoid pinned - set offset to 2 (as of commit date)
    }

# Temporary solution, delete all the contents of the articles table
# and fill it with the new articles once an hour.
def get_new_articles():
    print("GET NEW ARTICLES")
    # old_hashes = get_all_hashes()
    all_articles = get_all_articles()
    reset_artice_table()
    post_all_articles(all_articles)
    # check_all_filters()
    # new_hashes = get_all_hashes()
    # check_all_filters(old_hashes, new_hashes)
    # generate_short_videos(old_hashes, new_hashes)

scheduler = BackgroundScheduler()
scheduler.add_job(get_new_articles, 'interval', hours=1)
scheduler.start()

@app.route("/")
def index():
    # get_new_articles()
    # old_hashes = get_all_hashes()
    # new_hashes = get_all_hashes()
    # generate_short_videos(old_hashes, new_hashes)
    # check_all_filters()
    sources = {
        "Hacker News": "https://news.ycombinator.com/",
        "BBC News": "https://www.bbc.co.uk/news/technology",
        "CNN News": "https://edition.cnn.com/business/tech",
        "Business Insider": "https://www.businessinsider.com/tech",
        "Tech Crunch": "https://techcrunch.com/",
        "Sky News": "https://news.sky.com/technology/",
        "Wired": "https://www.wired.co.uk/topic/technology/",
        "Venture Beat": "https://venturebeat.com/",
        "Reddit Tech News": "https://www.reddit.com/r/technews/",
        "Reddit Tech": "https://www.reddit.com/r/tech/",
        "Reddit Technology": "https://www.reddit.com/r/technology/",
        "Reddit Software": "https://www.reddit.com/r/software/",
    }

    return render_template("index.html", news_sources=get_articles(), sources=sources)

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
    if form.validate_on_submit():
        if get_count_filters_per_user(current_user.email) >= 5:
            flash('Too many filters already', 'error')
            return redirect(url_for('users_email_notifications'))
        else:
            insert_new_email_filter(form.key_word.data, current_user.email)
            flash('New email filter created', 'success')
            return redirect(url_for('users_email_notifications'))
    return render_template("new_email_notifications.html", form=form)

@app.route('/users_email_notifications')
def users_email_notifications():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template("users_email_notifications.html", filters=get_all_filters_per_user(current_user.email))

@app.route('/delete_filter/<int:filter_id>', methods=['POST'])
def delete_filter(filter_id):
    deleted = delete_specific_email_filter_by_id(filter_id, current_user.email)
    if not deleted:
        flash('Email Filter NOT  Deleted', 'failure')
    return redirect(url_for('users_email_notifications'))

if __name__ == "__main__":
    app.run(debug=True)