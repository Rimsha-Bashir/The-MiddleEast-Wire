from unicodedata import category
from numpy import append
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from dateutil import parser
import sqlite3

conn = sqlite3.connect('newsarticles.db')  
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS articles (
    Source TEXT,
    Title TEXT,
    Link TEXT PRIMARY KEY,
    Image TEXT,
    Topic TEXT,
    Country TEXT,
    Keywords TEXT, 
    Publish_Date TEXT,
    Description TEXT   
)
''')

url = 'https://www.middleeasteye.net/news/'
base_url = "https://www.middleeasteye.net"

def safe_get(lst, index, default=""):
    try:
        return lst[index] if len(lst) > index else default
    except IndexError:
        return default

def get_details_from_article(url):
    try:
        details = []
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')    
        main_page = soup.find('section', class_='page-main-content')
        date = main_page.find('div', class_='submitted-date').find('span', 'date-created')
        description_tag = soup.find('meta', attrs={'property': 'og:description'})
        if date:
            publish_date = date.next_sibling.strip()
        else:
            publish_date = None
        if description_tag:
            desc = description_tag.get('content', '')
        else:
            desc = None
        details.append(publish_date)
        details.append(desc)
        return details
    
    except Exception as e:
        print(f"Error fetching {url}: {e}")

    return []

def scrape_middleasteye():

    try:
        response = requests.get(url, timeout=10)
        print("Fetching data from Middle East Eye...")
        soup = BeautifulSoup(response.text, 'html.parser')        
        articles = soup.find_all('article')

        data= []
        main_articles = soup.find_all('div', class_='main-article-wrapper')
        for main_article in main_articles:
            title_tag = main_article.find('a', {'aria-label': True, 'href':True})
            
            if title_tag:
                title_text = title_tag.get('aria-label')
                article_link = base_url + title_tag.get('href')
                topic = main_article.find('div', class_='main-article-topic')
                image_tag = title_tag.find('img')

                if topic:
                    topic_text = topic.get_text(strip=True)
                else:
                    topic_text = None
                
                if image_tag:
                    image_url=image_tag.get('src')
                else:
                    image_url = None
                details = get_details_from_article(article_link)
                data.append({
                    'Source': 'Middle East Eye',
                    'Title': title_text,
                    'Link': article_link,
                    'Image': base_url + image_url if image_url else None,
                    'Primary Topic': topic_text, 
                    'Publish_Date' : safe_get(details,0),
                    'Description': safe_get(details, 1)
                })

        secondary_articles = soup.find_all('div', class_='mee-article-tile mee-article-tile-type--story mee-article-tile-image')

        for secondary_article in secondary_articles:
            image_tag = secondary_article.find('div', class_='mee-tile-image').find('img')
            image_url = image_tag.get('src') if image_tag else None
            title_tag = secondary_article.find('a', {'aria-label': True, 'href':True})
            topic_tag = secondary_article.find('div', class_='mee-tile-main')

            if title_tag:
                title_text = title_tag.get('aria-label')
                article_link = base_url + title_tag.get('href')

                if topic_tag:
                    topic_tag = topic_tag.find('div', class_='mee-tile-topic')
                    topic = topic_tag.find('a')
                    topic_text = topic.get_text(strip=True) if topic else None
                else:
                    topic_text = None 
                details = get_details_from_article(article_link)
                data.append({
                    'Source': 'Middle East Eye',
                    'Title': title_text,
                    'Link': article_link,
                    'Image': base_url + image_url if image_url else None,
                    'Topic': topic_text,
                    'Country': "",
                    'Keywords': "", 
                    'Publish_Date' : safe_get(details, 0),
                    'Description': safe_get(details, 1)
                })

    except Exception as e:
        print(f"Error fetching {url}: {e}")

    return pd.DataFrame(data)

df=scrape_middleasteye()
df=df.drop_duplicates()
df['Publish_Date'] = df['Publish_Date'].apply(
    lambda x: parser.parse(x).strftime("%Y-%m-%d") if x and isinstance(x, str) else None
)
print("Successfully scraped news articles from Middle East Eye!") if not df.empty else print("Scraping attempt unsuccesful...")
for _, row in df.iterrows():
    cursor.execute('''
        INSERT OR IGNORE INTO articles (Source, Title, Link, Image, Topic, Country, Keywords, Publish_Date, Description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        row['Source'],
        row['Title'],
        row['Link'],
        row['Image'],
        row['Topic'],
        row['Country'],
        row['Keywords'],
        row['Publish_Date'], 
        row['Description']
    ))
conn.commit()
conn.close()
