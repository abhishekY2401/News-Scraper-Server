import os
from dotenv import load_dotenv
import requests
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from newscraper import scrape_news_article

# Load environment variables from .env file
load_dotenv()

api_key = os.environ.get('ASSEMBLYAI_API_KEY')

url = 'https://www.forbes.com/sites/jenamcgregor/2023/05/09/microsoft-expands-copilot-ai-tool-to-600-customers-in-paid-preview-as-digital-debt-weighs-on-workers/?sh=6041ae187244'

data = scrape_news_article(url)

# now performing text summarization on extracted news article content
parser = PlaintextParser.from_string(data, Tokenizer('english'))
summarizer = LsaSummarizer()
summary = summarizer(parser.document, 50)

# print the summary
for sentence in summary:
    print(sentence)
