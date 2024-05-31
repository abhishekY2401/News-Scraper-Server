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
from newscraper import scrape_news_article_from_forbes, scrape_news_article_from_wired
from flask_cors import CORS
import socket
import requests
from bs4 import BeautifulSoup
import datetime

app = Flask(__name__)
CORS(app)

# jwt = JWTManager(app) # initialize JWTManager
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)


# Load environment variables from .env file
load_dotenv()

# username = os.environ.get("MONGO_ROOT_USERNAME")
# password = os.environ.get("MONGO_ROOT_PASSWORD")

# MONGO_URI = f"mongodb+srv://{username}:{password}@news-service.egwgjil.mongodb.net/news_db?retryWrites=true&w=majority"
# client = MongoClient(MONGO_URI)
# db = client.get_database()

# collection = db['article']
# colUser = db['users']

# api_key = os.environ.get('ASSEMBLYAI_API_KEY')


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
    data = scrape_news_article_from_forbes(url)
    
    articles = []

    for news in data:
    
        title = news['title']
        # entries = collection.find_one({'title': {'$eq': title}})
    
        # if (entries != None): 
        #     print("record exists in database")
        # else:    
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
            "title": title,
            "category": category,
            "images": news['img_url'],
            "author": news['author'],
            "content": news_content,
            "source": "Forbes"
        }
            
        articles.append(news_article_info)
        # collection.insert_one(news_article_info)
        
    articles_res = {"msg":"added all categories of news in the database", "data": articles}
        
    return articles_res

@app.route("/top_news")
def top_news():
    news_article = []
    news_article_link = []
    url = "https://forbes.com/"
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    popular_news = soup.find_all('li', class_='data-viz__item')
    
    # print(soup.prettify()[:10000])
    return popular_news

@app.route("/ai_news", methods=['GET'])
def scrape_from_wired():
    ai_news = []
    links = []
    
    try:
        page_res = requests.get("https://wired.com/tag/artificial-intelligence/")
        # print(page_res)
        soup = BeautifulSoup(page_res.content, 'html.parser')

        articles = soup.find_all("div", class_="SummaryItemContent-eiDYMl")
        # print(articles)
        
        for article in articles:
            a_tag = article.find_all('a', class_="SummaryItemHedLink-civMjp")
            # print(a_tag[0]['href'])
            if a_tag[0]['href'].startswith('/story'):
                links.append("https://wired.com" + a_tag[0]['href'])
        
        for link in links:
            news_article_data = scrape_news_article_from_wired(link)
            ai_news.append(news_article_data)
    except Exception as e:
        return json.loads(str(e))
        
    return ai_news

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
            
        news_data = summarization(category)
        news_articles.append(news_data['data'])
        
        
    # news = collection.find()
    
    # for articles in news:
    #     news_articles.append(articles)
        
    forbes_article = {
        "articles": news_articles
    }
    
    json_articles = json.loads(json_util.dumps(forbes_article))
        
    return json_articles

# USER AUTHENTICATION

# @app.route("/register/user", methods=["POST"])
# def register():
#     new_user = request.get_json() # get json body request
#     new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8").hexdigest()) # encrypt password
    
#     # check if user already exists
#     doc = colUser.find_one({"username": new_user["username"]})
    
#     # if user does not exists, then create a user
#     if not doc:
#         # create the user
#         colUser.insert_one(new_user)
#         return jsonify({'msg', 'User created successfully'}, 201)
    
#     return jsonify({'msg': "Not authenticated"}, 401)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
