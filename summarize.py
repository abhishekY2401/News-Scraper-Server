import os
from dotenv import load_dotenv
from flask import Flask, jsonify
import json
from pymongo import MongoClient
from flask_pymongo import PyMongo
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from newscraper import scrape_news_article
import socket

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

username = os.getenv("MONGO_ROOT_USERNAME")
password = os.getenv("MONGO_ROOT_PASSWORD")

MONGO_URI = f"mongodb+srv://{username}:{password}@cluster0.5wybg2p.mongodb.net/news?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.get_database()

collection = db['article']

api_key = os.environ.get('ASSEMBLYAI_API_KEY')


@app.route("/")
def index():
    hostname = socket.gethostname()
    return jsonify(
        message="Welcome to news app! I am running inside {} pod!".format(hostname)
    )


@app.route("/<type>")
def summarization(type):
    url = "https://www.forbes.com/" + type
    data = scrape_news_article(url)

    news_content = []

    for news in data:
        content = news['content']

        # now performing text summarization on extracted news article content
        parser = PlaintextParser.from_string(content, Tokenizer('english'))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 30)

        # <Sentence: " sentence ">
        # print the summary
        sentences = [sentence.__str__() for sentence in summary]
        article = ' '.join(sentences)
        news_content.append(article)

    news_data = json.loads(json.dumps(news_content))
    article_content = {
        type: news_data
    }

    collection.insert_one(article_content)

    return article_content


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
