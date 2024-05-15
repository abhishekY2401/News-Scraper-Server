import requests
from bs4 import BeautifulSoup

# scraping from forbes
def scrape_news_article_from_forbes(url):
    # authorname = []
    i=0
    article_data = []
    authors = []
    # thearticle = []

    # store the text for each article
    # paragraphtext = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    articles = soup.find_all("a", class_="ObwfaEm5")
    authors = soup.find_all("a", class_="_84Z--AMj")
    
    # extracting article link, title and img
    for article in articles:
        author = ''
        img_url = 'a'
        title = article.get('aria-label')
        link = article.get('href')
        img = article.find_all()    
        if authors[i].get('data-ga-track') is not None:
            author = authors[i].get('data-ga-track')[30:]  

        for child in img:
            if 'src' in child.attrs:
                img_url = child['src']
        
        news = {
            "title": title,
            "author": author,
            "link": link,
            "img_url": img_url
        }
        
        
        article_data.append(news)
        i+=1
        # print(article_data)
    # fetch the news article content
    for news in article_data:
        article_url = news['link']

        # Send GET request to the article URL
        response = requests.get(article_url)
        if response.status_code == 200:
            article_html = response.text

            # Parse the HTML content of the article page
            sup = BeautifulSoup(article_html, 'html.parser')

            # Extract the content from the HTML elements
            content_elements = sup.find_all('p')  # Example: Extract paragraphs
            
            # Extract author name
            # news_author = soup.find_all('div', class_="fs-author-wrapper")
    
            # author = news_author.findAll('a', class_='contrib-link--name')
            # print(author.get_text())
            
            # Process and store the extracted content as needed
            extracted_content = []
            for element in content_elements:
                extracted_content.append(element.get_text())
                
            news['content'] = extracted_content

    # for data in article_data:
    #     print(data)

    return article_data

# scraping from wired for AI news
def scrape_news_article_from_wired(article_url):
    article_data = {}
    extracted_content = []
    
    page_res = requests.get(article_url)
    soup_data = BeautifulSoup(page_res.content, 'html.parser')
    
    # article_info = soup_data.find('div', class_='GridWrapper-cAzTTK')
    title = soup_data.find('h1', class_='BaseWrap-sc-gjQpdd').text # type: ignore
    author = soup_data.find('div', class_='BylinesWrapper-KIudk').text # type: ignore
    image = soup_data.find_all('img', class_='ResponsiveImageContainer-eybHBd fptoWY responsive-image__image')
    content = soup_data.find_all('p')
    # date = soup_data.find('time', class_='SplitScreenContentHeaderPublishDate-bMGEVk kMYmqz').text #type: ignore
    
    for element in content:
        extracted_content.append(element.get_text())
    
    article_data['images'] = image[1]['src']
    article_data['title'] = title
    article_data['author'] = author
    article_data['content'] = extracted_content
    # article_data['date'] = date
    # print(article_data)
    
    return article_data


# scrape_news_article_from_wired("https://wired.com/story/generative-ai-totally-shameless/")
    


