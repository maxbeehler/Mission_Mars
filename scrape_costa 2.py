from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser() 

    # Visit visitcostarica.herokuapp.com
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "lxml")

    #1
    news_title = soup.find("div", class_= "content_title").text
    #print(news_title)

    news_p = soup.find("div", class_="rollover_description").text
    #print(news_p)

    #2
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

    html = browser.html
    soup = bs(html, "lxml")

    image = soup.find("img", class_="thumb")
    imgfile = image["src"]
    #imgfile
    featured_image_url = "https://www.jpl.nasa.gov"+imgfile


    #3 (With retweet filter help from jacklyn)
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)

    html = browser.html
    soup = bs(html, "lxml")

    tweets = soup.find_all('div', class_='tweet', attrs={"data-name": "Mars Weather"})

    pressure = 'pressure'

    for x in range(len(tweets)):
        tweet_text = tweets[x].find_all('p')
        weather_dirty = tweet_text[0].contents
        mars_weather = weather_dirty[0].replace('\n',' ')
        if pressure in mars_weather:
            break

    #4
    url4 = 'https://space-facts.com/mars/'
    
    spacefacts = pd.read_html(url4)
    spacefacts = spacefacts[0]
    spacefacts = spacefacts.set_index([0])
    spacefacts.index.names = [None]
    spacefacts = spacefacts.rename(columns={0:'Description', 1:'Data'})
    
    spacefacts_clean = spacefacts.to_html()

    #spacefacts_html = spacefacts.to_html()
    #spacefacts_clean = spacefacts_html.replace('\n', ' ')


    #5
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)

    html = browser.html
    soup = bs(html, "lxml")
    
    hemisphere_image_urls = []

    for x in range (4):
        photos = browser.find_by_tag('h3')
        photos[x].click()
        html = browser.html
        soup = bs(html, 'lxml')
        wide_image = soup.find("img", class_= "wide-image")["src"]
        name = soup.find("h2", class_="title").text
        browser.back()
        image = 'https://astrogeology.usgs.gov' + wide_image
        combined = {"Hemisphere" : name, "Link" : image}
        hemisphere_image_urls.append(combined)

    #Add to dictionary
    costa_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "spacefacts_clean": spacefacts_clean,
        "hemisphere_image_urls": hemisphere_image_urls

    }



    # Close the browser after scraping
    browser.quit()

    # Return results
    return costa_data
