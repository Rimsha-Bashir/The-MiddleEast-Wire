from flask import Flask, redirect, url_for, render_template, request, session
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime, timedelta
from sqlalchemy import desc

import os 


newsapp = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'))
bootstrap = Bootstrap4(newsapp)
basedir = os.path.abspath(os.path.dirname(__file__))
newsapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'newsarticles.db')
newsapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(newsapp)

class Article(db.Model): # This defines a Python class named 'Article' that represents a table in the database.
    __tablename__ = 'articles' # Here, the class Article is mapped to a table called articles in the database.
    Source = db.Column(db.String, nullable=False)
    Title = db.Column(db.String, nullable=False)
    Link = db.Column(db.String, primary_key=True)
    Image = db.Column(db.String, nullable=True)
    Topic = db.Column(db.String, nullable=True)
    Country = db.Column(db.String, nullable=True)
    Keywords = db.Column(db.String, nullable=True)
    Publish_Date = db.Column(db.String, nullable=True)
    Description = db.Column(db.String, nullable=True) 

with newsapp.app_context():
    db.create_all()

@newsapp.route("/", methods=["GET"])
def homepage():
    # Page load/submit → Read filter inputs → Filter DB query → Render results + filters → Page load again (Flow of execution)

    source_filter = request.args.get("source")
    topic_filter = request.args.get("topic")
    keyword_filter = request.args.get("keyword")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    page = request.args.get("page", 1, type=int)
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page

    query = Article.query.order_by(desc(Article.Publish_Date))

    total_pages = (query.count() + per_page - 1) // per_page

    if source_filter:
        query = query.filter(Article.Source == source_filter)
    if topic_filter:
        query = query.filter(Article.Topic == topic_filter)
    if keyword_filter:
        query = query.filter(Article.Keywords.like(f"%{keyword_filter}%"))
    if start_date:
        query = query.filter(Article.Publish_Date >= start_date)
    if end_date:
        query = query.filter(Article.Publish_Date <= end_date)

    articles = query.all()

    sources = [row.Source for row in db.session.query(Article.Source).distinct()]
    topics = [row.Topic for row in db.session.query(Article.Topic).distinct() if row.Topic]
    date = [row.Publish_Date for row in db.session.query(Article.Publish_Date).distinct() if row.Publish_Date]

    # Parse all keywords
    raw_keywords = Article.query.with_entities(Article.Keywords).all()
    keywords = sorted(set(
        k.strip() for row in raw_keywords if row.Keywords
        for k in row.Keywords.split(",")
    ))

    return render_template("index.html", articles=articles[start:end], sources=sources, topics=topics, keywords=keywords, date=date, total_pages=total_pages, page=page)

@newsapp.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    newsapp.run(debug=True)
