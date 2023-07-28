import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
import json
from bson import json_util, ObjectId
from pymongo import MongoClient
from flask_pymongo import PyMongo
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from newscraper import scrape_news_article
from flask_cors import CORS
import socket
import requests
from bs4 import BeautifulSoup
import textwrap

app = Flask(__name__)
CORS(app)

# Load environment variables from .env file
load_dotenv()

username = os.getenv("MONGO_ROOT_USERNAME")
password = os.getenv("MONGO_ROOT_PASSWORD")

MONGO_URI = f"mongodb+srv://{username}:{password}@cluster0.5wybg2p.mongodb.net/news?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.get_database()

collection = db['article']
colUser = db['user']

api_key = os.environ.get('ASSEMBLYAI_API_KEY')


@app.route("/")
def index():
    hostname = socket.gethostname()
    return jsonify(
        message="Welcome to news app! I am running inside {} pod!".format(hostname)
    )


@app.route("/<category>")
def summarization(category):
    url = "https://www.forbes.com/" + category
    print(url)
    data = scrape_news_article(url)
    
    articles = []

    for news in data:
    
        title = news['title']
        entries = collection.find_one({'title': {'$eq': title}})
    
        if (entries != None): 
            print("record exists in database")
        else:    
            news_content = []
            content = news['content']
            
            # now performing text summarization on extracted news article content
            parser = PlaintextParser.from_string(content, Tokenizer('english'))
            summarizer = LsaSummarizer()
            summary = summarizer(parser.document, 30)

            # <Sentence: " sentence ">
            # print the summary
            sentences = [sentence.__str__() for sentence in summary]
            
            article = ''.join(sentences)
            # wrapper = textwrap.wrap(article, width=500, fix_sentence_endings=True, break_long_words=True, tabsize=8)
            # print(wrapper)
            news_content.append(article)    
                    
            news_article_info = {
                "title": news['title'],
                "category": category,
                "images": news['img_url'],
                "author": news['author'],
                "content": news_content,
                "source": "Forbes"
            }
            
            articles.append(news_article_info)
            collection.insert_one(news_article_info)
        
    return "added all categories of news in the database"

@app.route("/top_news")
def top_news():
    news_article = []
    news_article_link = []
    url = "https://forbes.com/"
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    popular_news = soup.find_all('li', class_='data-viz__item')
    
    print(soup.prettify()[:10000])
    return popular_news

@app.route("/ai_news")
def scrape_from_wired():
    links = []
    page = requests.get("https://wired.com/tag/artificial-intelligence/")
    soup = BeautifulSoup(page.content, 'html.parser')

    articles = soup.find_all("div", class_="SummaryItemContent-eiDYMl")
    
    for article in articles:
        a_tag = article.find_all('a', class_="SummaryItemHedLink-civMjp")
        links.append("https://wired.com" + a_tag[0]['href'])
        
    for link in links:
        data = requests.get(link)
        sup = BeautifulSoup(data.content)
        ai_data_img = sup.find('picture', class_='ResponsiveImagePicture-cWuUZO dUOtEa ContentHeaderResponsiveAsset-bREgIb cZenhb responsive-image')
        
    ai_news = {
        "articles": articles
    }
    print(links)
    return "0"

@app.route("/all_news")
def all_news():
    
    news_articles = []
    news_link = []
    url = "https://forbes.com"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    articles = soup.find_all('section', class_="channel--lazy")
    
    for article in articles:
        for link in article.find_all('a'):
            category = link.get('data-ga-track')
            categories = category.split(" ")
            news_link.append(categories[-1].lower())
            
    for category in news_link:  
        if category == "billionaires":
            category = "worlds-" + category 
            
        summarization(category)
        
    news = collection.find()
    
    for articles in news:
        news_articles.append(articles)
        
    forbes_article = {
        "articles": news_articles
    }
    
    json_articles = json.loads(json_util.dumps(forbes_article))
        
    return json_articles

# create user
# @app.route("/create_user", methods=['GET', 'POST'])
# def createUser():
#     if request.method == 'POST':
#         # get email
#         email = request.form.get("email")
#         # get password
#         password = request.form.get("password")
        
#         try:    
#             user = colUser.insert_one({"email": email, "password": password})
#         except Exception as e:
#             raise e
        
#         return {"msg": "Account created successfully!"}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
