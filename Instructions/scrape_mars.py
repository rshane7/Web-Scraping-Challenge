#!/usr/bin/env python
# coding: utf-8

# Import Dependencies
import pandas as pd
import pymongo
import requests 
import time
from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
print('0-scrape-imports')

#   Provide Chromedriver executable path adn browser type - Chrome
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    print('1-def-scrape')
#   Create Dictionary for scraped data
    mars_data = {}

    ### NASA MARS NEWS
    #   Mars URL to Scrape data from 
    nasa_news = "https://mars.nasa.gov/news/"
    browser.visit(nasa_news)
      
    #   Set sleep mode to 'x' seconds so the new chrome window can open to the above url.
    time.sleep(5)

    #   Create new soup using BeautifulSoup and parse the contents
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    print('2-News')

    #   Save the most recent article, title, date, and paragraph
    article = soup.find("div", class_="list_text")
    news_date = article.find("div", class_="list_date").text
    news_title = article.find("div", class_="content_title").text
    news_paragraph = article.find("div", class_="article_teaser_body").text

    #   Add data to dictionary for the 3 fields.
    mars_data["news_date"] = news_date
    mars_data["news_title"] = news_title
    mars_data["news_paragraph"] = news_paragraph
    print('3-News')

    ### JPL MARS SPACE IMAGES - FEATURED IMAGES
    #   Provide URL to be scraped and have browser go to URL provided in the line of code that populated the url variable
    mars_jpl_img = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_jpl_img)

    #   Set sleep mode to 'x' seconds so the new chrome window can open to the above url.
    time.sleep(5)

    #   Create new soup using BeautifulSoup and parse the contents
    html = browser.html
    mars_si_soup = BeautifulSoup(html, 'html.parser')
    image = mars_si_soup.find("img", class_="thumb")["src"]
    img_url = "https://jpl.nasa.gov"+image
    featured_image_url = img_url

    #   Use the requests library to download and save the image from the `img_url` above
    #    response = requests.get(img_url, stream=True)
    #    with open('img.jpg', 'wb') as out_file:
    #        shutil.copyfileobj(response.raw, out_file)

    # Add the feature image to the mars_scraped_data dictionary
    mars_data["featured_image_url"] = featured_image_url
    print('4-Image')

    ####   Display the image with IPython.display
    ####from IPython.display import Image
    ####Image(url='img.jpg')

    ### MARS WEATHER
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    time.sleep(5)

    #   Iterate through all 'tweets' and collect all the span tags.
    weather = browser.html
    weather_soup = BeautifulSoup(weather, 'html.parser')

    #   Find all elements that contain tweets
    tweets = weather_soup.findAll("span", attrs={"class": "css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0"})

    #   Finds the first span from the tweets variable that have 'Sol' and 'pressure' in the text.
    for tweet in tweets: 
        mars_weather = tweet.get_text()
        if 'Sol' and 'pressure' in mars_weather:
            break
        else: 
            pass

    #   Move the contents of the mars_weather variable which should be the latest weather conditions on Mars to the dictionary    
    mars_data["mars_weather"] = mars_weather
    print('5-Weather')

    ### MARS FACTS
    #   Mars Facts url put into a variable
    mars_facts_url = "https://space-facts.com/mars/"
    browser.visit(mars_facts_url)
    time.sleep(5)

    #   Read the url html data and create an index into a pandas variable named table
    table = pd.read_html(mars_facts_url)
    table

    #   This creates a dataFrame showing the index, descripton and value from the tables variable that consisted of raw data/index.
    mars_facts_df = table[0]
    mars_facts_df.columns = ["Description", "Value"]
    mars_facts_df

    #   Takes the above dataFrame in mars_facts_df and converts it into html placing the results in mars_facts_html then moves to the 
    #   dictionary.
    mars_facts_html=mars_facts_df.to_html(header = False, index = False)
    mars_data["mars_facts_html"] = mars_facts_html
    print('6-Facts')

    ### MARS Hemisphere
    #   Visit the USGS Astogeology site and scrape url and picture info for each hemisphere.
    hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere)
    time.sleep(5)
    print('7a-Hemisphere')
    #   Use splinter to loop through the 4 images and load them into a dictionary
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_hemisphere=[]
    print('7b-Hemisphere')
    #   Loop through the four tags then load the data to the dictionary.
    #   Append data from the dictionary into the variable mars_hemisphere to be displayed.
    for i in range (4):
        time.sleep(5)
        images = browser.find_by_tag('h3')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        partial = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h3",class_="title").text
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary={"title":img_title,"img_url":img_url}
        mars_hemisphere.append(dictionary)
        browser.back()
    print('7c-Hemisphere')
    #   Displayed contents of mars_hemisphere - did not use 'print' statement as it does not present as well as with 'print'.
    mars_data["mars_hemisphere"] = mars_hemisphere
    print('7d-Hemisphere')

    #Return the dictionary
    return mars_data
    print('8-Return-Data')
 
    # close browser
    browser.quit()