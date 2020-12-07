#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import time
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[ ]:


news_url = 'https://mars.nasa.gov/news/'
browser.visit(news_url)


# In[3]:


news_html = browser.html
news_soup = bs(news_html, 'html.parser')


# In[4]:


articles = news_soup.find_all('li', class_='slide')
latest_article = articles[0]
latest_headline = latest_article.find('div', class_='content_title').text
latest_teaser = latest_article.find('div', class_='article_teaser_body').text


# In[5]:


jpl_url = 'https://www.jpl.nasa.gov'
images_url = f'{jpl_url}/spaceimages/?search=&category=Mars'
browser.visit(images_url)


# In[6]:


full_image_button = browser.find_by_id('full_image')
full_image_button.click()

browser.links.find_by_partial_text('more info').click()


# In[7]:


featured_image_html = browser.html
featured_image_soup = bs(featured_image_html,'html.parser')

featured_image_loc = featured_image_soup.find('figure', class_='lede')
featured_image_url = f"{jpl_url}{featured_image_loc.find('a')['href']}"


# In[8]:


mars_facts_url = 'https://space-facts.com/mars/'
browser.visit(mars_facts_url)


# In[9]:


mars_facts_table = pd.read_html(mars_facts_url, match='Recorded By')[0]
mars_facts_table.columns = ["Criteria", "Values"]

mars_facts_html = mars_facts_table.to_html(index=False)


# In[10]:


astrogeo_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(astrogeo_url)


# In[11]:


hemisphere_image_urls = []

for x in range(4):
    astrogeo_button = browser.links.find_by_partial_text('Hemisphere Enhanced')[x]
    astrogeo_button.click()

    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html,'html.parser')
    hemisphere_title = hemisphere_soup.find('h2', class_='title').text
    hemisphere_url = hemisphere_soup.find('div', class_='downloads').find('li').find('a')['href']
    
    
    hemisphere_image = {
        "title": hemisphere_title,
        "img_url": hemisphere_url
    }
    hemisphere_image_urls.append(hemisphere_image)

    browser.back()
    time.sleep(1)


# In[12]:


browser.quit()
