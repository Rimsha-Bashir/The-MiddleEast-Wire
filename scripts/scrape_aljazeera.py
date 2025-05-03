from unicodedata import category
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
from datetime import datetime
from dateutil import parser
import re

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

url = 'https://www.aljazeera.com/news/'
base_url = "https://www.aljazeera.com"

def safe_get(lst, index, default=""):
    try:
        return lst[index] if len(lst) > index else default
    except IndexError:
        return default

def get_details_from_article(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        return {
            "Keywords": soup.find('meta', attrs={'name': 'keywords'}).get('content', '') if soup.find('meta', attrs={'name': 'keywords'}) else '',
            "Topic": soup.find('meta', attrs={'name': 'primaryTag'}).get('content', '') if soup.find('meta', attrs={'name': 'primaryTag'}) else '',
            "Country": soup.find('meta', attrs={'name': 'where'}).get('content', '') if soup.find('meta', attrs={'name': 'where'}) else '',
            "Publish_Date": soup.find('meta', attrs={'name': 'publishedDate'}).get('content', '') if soup.find('meta', attrs={'name': 'publishedDate'}) else '',
            "Description": soup.find('meta', attrs={'name': 'description'}).get('content', '') if soup.find('meta', attrs={'name': 'description'}) else '',
        }
    
    except Exception as e:
        print(f"Error fetching {url}: {e}")

    return {}

def scrape_aljazeera():
    try:
        response = requests.get(url)
        print("Fetching data from Al-Jazeera...")
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article')

        data = []
        for article in articles:
            title_tag = article.find('h3')
            link_tag = article.find('a', href=True)
            link = base_url + link_tag['href']
            img_tag = article.find('img')
            img_src = img_tag['src'] if img_tag else None
            details = get_details_from_article(link)

            if title_tag and link_tag and details:
                data.append({
                    'Source': 'Al Jazeera',
                    'Title': title_tag.text.strip(),
                    'Link': link,
                    'Image': base_url + "/" + img_src, 
                    'Topic': details.get('Topic', ''),
                    'Country': details.get('Country', ''),
                    'Keywords': details.get('Keywords', ''),
                    'Publish_Date': details.get('Publish_Date', ''),
                    'Description': details.get('Description', '')
                })
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Error fetching {url}: {e}")

    
df=scrape_aljazeera()
df['Publish_Date'] = df['Publish_Date'].apply(
    lambda x: parser.parse(x).strftime("%Y-%m-%d") if x and isinstance(x, str) else datetime.now().strftime("%Y-%m-%d")
)
df['Image'] = df['Image'].apply(lambda x: re.sub(r'(\.jpg).*', r'\1', x) if isinstance(x, str) else x)
print("Successfully scraped news articles from Al-Jazeera!") if not df.empty else print("Scraping attempt unsuccesful...")
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
        row['Topic'],
        row['Publish_Date'],
        row['Description']
    ))
conn.commit()
conn.close()