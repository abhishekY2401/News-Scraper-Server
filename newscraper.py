import requests
from bs4 import BeautifulSoup
from datetime import datetime


def scrape_news_article(url):
    authorname = []
    title = []
    thearticle = []

    # store the text for each article
    paragraphtext = []

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # get author name, if there is any for the article
    try:
        abody = soup.find(class_="_84Z--AMj").find('j')
        aname = abody.get_text()
    except:
        aname = 'Anonymous'

    # get article title
    a_title = soup.find(class_='fs-headline')
    thetitle = a_title.get_text()

    # get main article page
    articlebody = soup.find(class_='main-content')

    # get text
    articletext = soup.find_all('p')

    # print text
    for para in articletext:
        # get the text only
        text = para.get_text()
        paragraphtext.append(text)

    # combine all the paragraphs into article
    thearticle.append(paragraphtext)
    authorname.append(aname)
    title.append(thetitle)

    myarticle = [' '.join(article) for article in thearticle]

    data = {
        'Title': thetitle,
        'Author': authorname,
        'Article': myarticle,
        'Date': datetime.now()
    }

    return myarticle
