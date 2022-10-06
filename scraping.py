#!/usr/bin/env python
# coding: utf-8


#import dependencies 

from splinter import Browser
from bs4 import BeautifulSoup as soup 
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 
import datetime as dt

#create funcion to initialize broswer, create data dictionary, and end websdriver and scraped data

def scrape_all():

#set up path for brower and open chrome browser

    executable_path = {'executable_path' : ChromeDriverManager().install()}

    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    #run all scraping functions and store results in dictionary

    data = { 
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last modified": dt.datetime.now()
    }

    #stop webdriver and return data

    browser.quit()
    return data

#create function for news title and paragraph 

def mars_news(browser): 
#visit the mars nasa news site
    url = 'https://redplanetscience.com/'

    browser.visit(url)

#optional delay for loading the page, searching for specific tag as well as waiiting 1 sec due to loading on page 

    browser.is_element_present_by_css('div.list_text', wait_time=1)


    html = browser.html

    news_soup = soup(html, 'html.parser')

#slide_elem is parent element, will hold all of the other elements within it, 
#and we'll reference it when we want to filter search results even further.

    #add exception handling using try statement

    try: 

        slide_elem = news_soup.select_one('div.list_text')

#use find() on parent element to parse specific data
        slide_elem.find('div', class_='content_title')


#use the parent element to find the first 'a' tag ans save it as news title 

#use get_text() function to only pull text element 
        news_title = slide_elem.find('div', class_='content_title').get_text()

    #news_title


#use parent element to find paragraph text 

        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    #news_p
    except AttributeError:
        return None, None


    return news_title, news_p

# ### Featured Images

#create function for featured images

def featured_image(browser):

#visit url 

    url = 'https://spaceimages-mars.com/'

    browser.visit(url)


#get full image by clicking the image button

    full_image_elem = browser.find_by_tag('button')[1]

    full_image_elem.click()


#parse html with soup 

    html = browser.html

    img_soup = soup(html, 'html.parser')

#find ithe relative image url, an img tag is nested within this HTML, so we've included it.
#.get('src') pulls the link to the image.
    try: 
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

        img_url_rel

    except AttributeError:
        return None
#use the base URL to create an absolute URL 

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


#we're creating a new DataFrame from the HTML table. The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. 
#By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. 
#Then, it turns the table into a DataFrame.

#create function to gathering facts 

def mars_facts():

    try: 

        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None
#Here, we assign columns to the new DataFrame for additional clarity.
    df.columns=['description','Mars','Earth']

#we're turning the Description column into the DataFrame's index. 
#inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.
    df.set_index('description', inplace=True)

    #df

#convert data frame back to html

    return df.to_html(classes="table table-striped")


if __name__ =='__main__':

    print(scrape_all())
#shut down automated browser 





