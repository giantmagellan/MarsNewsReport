# Dependencies
import pymongo
import os
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser 

# Connect to MongoDB default port
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Defining 'MarsDB' database and collection
mars_db = client.marsDB
collection = mars_db.articles

# Mars urls
news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
jpl_url = 'https://www.jpl.nasa.gov/spaceimages/details.php?id=PIA18904'
weather_url = 'https://twitter.com/marswxreport?lang=en'
facts_url = 'https://space-facts.com/mars/'
hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

def scrape():
    """Using Splinter to execute desired paths."""
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    """Latest news and paragraph text from the NASA Mars News site.""" 
    browser.visit(news_url)
    html = browser.html
    news_soup = bs(html, 'html.parser')

    # Determining elements that contain sought info; Retrieving parent divs
    """News title."""
    news_results = news_soup.find('div', {'class': 'content_title'})
    news_title = news_results.find('a').text

    """News article teaser paragraph."""
    list_text = news_soup.find('div', {'class': 'list_text'})
    news_p = list_text.find('div', {'class': 'article_teaser_body'}).text

    # print(news_p)

    """Featured image from JPL's Mars programme."""
    browser.visit(jpl_url)
    html = browser.html
    jpl_soup = bs(html, 'html.parser')
    url_prefix = 'https://www.jps.nasa.gov'

    images_a = jpl_soup.find('figure', class_='lede')
    images_b = images_a.find('a')['href']

    featured_image_url = url_prefix + images_b
    # featured_image_url

