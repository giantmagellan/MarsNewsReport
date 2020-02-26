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

    """NASA MARS NEWS: Latest news and paragraph text from the NASA Mars News site.""" 
    browser.visit(news_url)
    html = browser.html
    news_soup = bs(html, 'html.parser')

    # Determining elements that contain sought info; Retrieving parent divs
    """News title."""
    news_results = news_soup.find('div', {'class': 'content_title'})
    news_title = news_results.find('a').text

    """News article teaser paragraph."""
    # list_text = news_soup.find('div', {'class': 'list_text'})
    # news_p = list_text.find('div', {'class': 'article_teaser_body'}).text

    # print(news_p)

    """JPL MARS SPACE IMAGES: Featured image from JPL's Mars programme."""
    browser.visit(jpl_url)
    html = browser.html
    jpl_soup = bs(html, 'html.parser')
    url_prefix = 'https://www.jps.nasa.gov'

    images_a = jpl_soup.find('figure', class_='lede')
    images_b = images_a.find('a')['href']

    featured_image_url = url_prefix + images_b
    # featured_image_url

    """MARS WEATHER TWITTER: Mars weather report tweet from Mars Weather twitter account."""
    browser.visit(weather_url)
    html = browser.html
    weather_soup = bs(html, 'html.parser')

    mars_weather_tweet = weather_soup.find('div', 
                                       attrs={"class": "tweet", "data-name": "Mars Weather"})
    # mars_weather = mars_weather_tweet.find('p', 'tweet-text').get_text()
    # print(mars_weather)

    """MARS FACTS: General Facts about the "Red Planet." """
    # Dependency
    import pandas as pd

    browser.visit(facts_url)
    html = browser.html
    facts_soup = bs(html, 'html.parser')

    mars_facts = []

    # def get_mars_facts():
    """Finds all 'tr' tags and assigns them to a variable."""
    facts = facts_soup.find_all('tr')[:8]
    for tr in facts:
        """Finds all 'td' tags within each 'tr' tag and assigns it to a variable. Then appends to a list."""
        tds = tr.find_all('td')[:8]
        mars_facts.append({
            tds[0].text, tds[1].text,
        })
    # print(mars_facts)

    # get_mars_facts()

    facts_df = pd.DataFrame(mars_facts)
    # facts_df

    # Render pandas dataframe to html table
    facts_html = facts_df.to_html()
    # print(facts_html)

    """MARS HEMISPHERES: High resolution photos for each of Mars' hemisphers."""
    browser.visit(hemi_url)
    html = browser.html
    hemi_soup = bs(html, 'html.parser')

    # Empty list to store hemisphere urls
    hemisphere_urls = []
    hemi_url_prefix = 'https://astrogeology.usgs.gov'

    # def get_hemi_urls(hemi_soup):
    """Querying through html code to find image url suffixes"""
    containers = hemi_soup.find('div', {'class': 'container'})
    items = containers.find_all('div', {'class': 'item'})

    for item in items:
        """Joining image url strings and hemisphere titles to a list."""
        hemi_url_join = hemi_url_prefix + item.find('a')['href']
        # hemi_url = hemi_url_prefix + item.find('img')['src']
        # h3 = item.find('h3')
        # hemisphere_urls.append({'Title': h3.text, 'img_url': hemi_url})
        hemisphere_urls.append(hemi_url_join)
    
    # print(hemisphere_urls)

    # hemi_urls = get_hemi_urls(hemi_soup)
    # hemi_urls

    # For verification
    # hemisphere_urls

    # Empty list to store image urls
    hemisphere_image_urls = []
    links = hemisphere_urls

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    for link in links:
        browser.visit(link)
        html = browser.html
        soup = bs(html, 'html.parser')
        
        """Querying each link to find each full resolution image url and its respective title."""
        containers = soup.find('div', {'class': 'container'})
        
        """Searching for urls."""
        downloads = containers.find('div', {'class': 'downloads'})
        uls = downloads.find('ul')
        lis = uls.find_all('li')[0]
        a = lis.find('a')['href']
        
        """Searching for titles."""
        contents = containers.find('div', {'class': 'content'})
        h2 = contents.find('h2', {'class': 'title'})
        
        hemisphere_image_urls.append({'title': h2.text,
                                    'img_url': a})
    # hemisphere_image_urls

    scrape_dict = {
        'News Title': news_title,
        # 'News Paragraph': news_p,
        'Featured Image url': featured_image_url,
        # 'Mars Weather': mars_weather,
        'Mars Facts': mars_facts,
        'Facts html': facts_html,
        'Hemisphere Image urls': hemisphere_image_urls,
    } 

    print(scrape_dict)

scrape()