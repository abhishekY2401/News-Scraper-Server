# News-Scraper-Web

## This is Scraper API which scrapes news of different categories from Forbes website 
![image](https://github.com/abhishekY2401/News-Scraper-Server/assets/89199323/93fd3e93-5ed1-402c-9caa-60c48f293459)


### Tools & Frameworks Used 🛠️

- Flask
- BeautifulSoup
- MongoDB (Currently not in use as they have started charging for the clusters, will shift to some other NoSQL DB)
- NLTK, Sumy (for news summarization)

### Why News Scraper? 
The reason to build my own web scraper was that third party webscraping tools charge for their News APIs providing limited content.

### Current features
- Collects news of following categories from forbes
  - Leadership, Businesses, world-billionaires, money, lifestyle
- For AI specific news content, it collects news from wired.com

### New Features to Integrate
- Collect news from different sources (wired, moneycontrol, forbes, yahoo finance, bloomberg)
- Integrate authentication to store user activities
  - bookmarks
  - personalized news recommendation based on past reads
  - sentiment analysis based on the comments
  - share the news article on any social platform

### Deployment
This scraper api is deployed on pythonanywhere.com (currently down due to certain dependency issues, we'll be back soon)
