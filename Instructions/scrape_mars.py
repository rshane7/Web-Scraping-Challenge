#!/usr/bin/env python
# coding: utf-8

### Web Scraping Homework - Mission to Mars - Homework Startup Basics
#   ![mission_to_mars](Images/mission_to_mars.png)
#   In this assignment, you will build a web application that scrapes various websites for data related to the
#   Mission to Mars and displays the information in a single HTML page. The following outlines what you need to do.

### Before You Begin - Complete
#   1. Create a new repository for this project called `web-scraping-challenge`. **Do not add this homework to an
#      existing repository**.
#   2. Clone the new repository to your computer.
#   3. Inside your local git repository, create a directory for the web scraping challenge. Use a folder name to 
#      correspond to the challenge: **Missions_to_Mars**.
#   4. Add your notebook files to this folder as well as your flask app.
#   5. Push the above changes to GitHub or GitLab.

### Step 1 - Scraping - Complete
#   Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.
#   * Create a Jupyter Notebook file called `mission_to_mars.ipynb` and use this to complete all of your scraping
#   and analysis tasks. The following outlines what you need to scrape.

# Import Dependencies
import pandas as pd
import pymongo
import requests 
import time
import shutil
import re
from bs4 import BeautifulSoup
from splinter import Browser

def init_browser():
    executable_path = {"executable_path": "/Users/David W. Jones/class/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

###########

#   Provide Chromedriver executable path adn browser type - Chrome
def init_browser()
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

#   Create Dictionary for scraped data
mars_data = {}


#   Set sleep mode to 'x' seconds so the new chrome window can open to the above url.
    t=5
    t1=10
### NASA MARS NEWS
### Paragraph Text. Assign the text to variables that you can reference later.
#   --- python ---
#   Example:
#   news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
#   news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer,
#   on course for launch next May from Vandenberg Air Force Base in central California 
#   -- the first interplanetary launch in history from America's West Coast."

#   Provide URL to be scraped and have browser go to URL provided in the line of code that populated the url variable

#   Mars URL to Scrape data from 
nasa_news = 'https://mars.nasa.gov/news/'
browser.visit(nasa_news)

#   Set sleep mode to 'x' seconds so the new chrome window can open to the above url.
time.sleep(t)

#   Create new soup using BeautifulSoup and parse the contents
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

#   Save the most recent article, title, date, and paragraph
article = soup.find("div", class_="list_text")
news_date = article.find("div", class_="list_date").text
news_title = article.find("div", class_="content_title").text
news_paragraph = article.find("div", class_="article_teaser_body").text

#   Add data to dictionary for the 3 fields.
mars_data =["news_date"] = news_date
mars_data =["news_title"] = news_title
mars_data =["news_paragraph"] = news_paragraph

### JPL MARS SPACE IMAGES - FEATURED IMAGES

#   * Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
#   * Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable #    called `featured_image_url`.
#   * Make sure to find the image url to the full size `.jpg` image.
#   * Make sure to save a complete url string for this image.
#   --- python ---
#   Example:
#   featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'
#   Added a tasks to present the image for the featured article we found in the prior task.

#   Provide URL to be scraped and have browser go to URL provided in the line of code that populated the url variable
mars_jpl_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(mars_jpl_img)

#   Set sleep mode to 'x' seconds so the new chrome window can open to the above url.
time.sleep(t)

#   Create new soup using BeautifulSoup and parse the contents
html = browser.html
mars_si_soup = BeautifulSoup(html, 'html.parser')

#   Found on stack overflow for this and the next box of code
#   Scrape the browser into soup and use soup to find the image of mars for the featured article found in the previous tasks.
#   Save the image url to a variable called `img_url` - move img_url in to featured_image_url to print url in next code box.
#   Use ipython to display image under the image url in the next box of code.
image = mars_si_soup.find("img", class_="thumb")["src"]
img_url = "https://jpl.nasa.gov"+image
featured_image_url = img_url

#   Use the requests library to download and save the image from the `img_url` above
response = requests.get(img_url, stream=True)
with open('img.jpg', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)

    # Add the feature image to the mars_scraped_data dictionary
mars_data = ["featured_image_url"] = featured_image_url

####   Print the image URL
#print(f"The image url is: {featured_image_url}")

####   Display the image with IPython.display
####from IPython.display import Image
####Image(url='img.jpg')

### MARS WEATHER

#   * Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) and scrape the latest 
#   Mars weather tweet from the page. Save the tweet text for the weather report as a variable called `mars_weather`.
#   * **Note: Be sure you are not signed in to twitter, or scraping may become more difficult.**
#   * **Note: Twitter frequently changes how information is presented on their website. If you are having difficulty
#   getting the correct html tag data, consider researching Regular Expression Patterns and how they can be used in
#   combination with the .find() method.**
#   --- python ---
#   Example:
#   mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'

#   Visit the Mars Weather twitter account and scrap the latest Mars weather tweet.
#   https://twitter.com/marswxreport?lang=en
#   Open url in chrome browser using english langauge and sleep for 't' seconds defined at the beginning of the script.
weather_url = "https://twitter.com/marswxreport?lang=en"
browser.visit(weather_url)
time.sleep(t)

#   Iterate through all 'tweets' and collect all the span tags.
#   Create a loop where you are looking for keyword 'Sol' and pressure in the tweet text.
#   If 'Sol' and 'Pressure' not found in tweet continue looping through the tweets.
#   Else if they are both found in a tweet then continue and print the contents of 'mars_weather' variable
#   Parse HTML with Beautiful Soup
weather = browser.html
weather_soup = BeautifulSoup(weather, 'html.parser')

#   Find all elements that contain tweets
tweets = weather_soup.findAll("span", attrs={"class": "css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0"})

#   Finds the first span from the tweets variable that have 'Sol' and 'pressure' in the text.
for tweet in tweets: 
    mars_weather = tweet.get_text()
    if 'Sol' and 'pressure'  in mars_weather:
        break
    else: 
        pass

#   Move the contents of the mars_weather variable which should be the latest weather conditions on Mars to the dictionary    
mars_data["mars_weather"] = mars_weather

### MARS FACTS
#   * Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to
#   scrape the table containing facts about the planet including Diameter, Mass, etc.
#   * Use Pandas to convert the data to a HTML table string.

#   Mars Facts url put into a variable
mars_facts_url = "https://space-facts.com/mars/"
browser.visit(mars_fact_url)

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

### MARS Hemisphere

#   * Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to 
#     obtain high resolution images for each of Mar's hemisphere.
#   * You will need to click each of the links to the hemisphere in order to find the image url to the full resolution image.
#   * Save both the image url string for the full resolution hemisphere image, and the hemispherE title containing the hemisphere name. Use #     a Python dictionary to store the data using the keys `img_url` and `title`.
#   * Append the dictionary with the image url string and the hemispher title to a list. This list will contain one dictionary for each #  #     hemispherephere.
#   --- python ---
#   Example:
#   hemispherephere_image_urls = [
#       {"title": "Valles Marineris hemisphere", "img_url": "..."},
#       {"title": "Cerberus hemisphere", "img_url": "..."},
#       {"title": "Schiaparelli hemisphere", "img_url": "..."},
#       {"title": "Syrtis Major hemispherE", "img_url": "..."},         ]

#   Visit the USGS Astogeology site and scrape url and picture info for each hemisphere.
hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemisphere)

#   Use splinter to loop through the 4 images and load them into a dictionary
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
mars_hemisphere=[]

#   Loop through the four tags then load the data to the dictionary.
#   Append data from the dictionary into the variable mars_hemispherephere to be displayed.

for i in range (4):
    time.sleep(t)
    images = browser.find_by_tag('h3')
    images[i].click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    partial = soup.find("img", class_="wide-image")["src"]
    img_title = soup.find("h2",class_="title").text
    img_url = 'https://astrogeology.usgs.gov'+ partial
    dictionary={"title":img_title,"img_url":img_url}
    mars_hemisphere.append(dictionary)
    browser.back()

    #   Displayed contents of mars_hemispherephere - did not use 'print' statement as it does not present as well as with 'print'.
mars_data["mars_hemisphere"]=mars_hemisphere

#Return the dictionary
return mars_data

# close browser
#browser.quit()

##                                                        THE END                                                                     ##