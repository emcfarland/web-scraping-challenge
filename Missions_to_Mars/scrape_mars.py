import pandas as pd
import time
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Define URLs to visit
    news_url = 'https://mars.nasa.gov/news/'
    jpl_url = 'https://www.jpl.nasa.gov'
    images_url = f'{jpl_url}/spaceimages/?search=&category=Mars'
    mars_facts_url = 'https://space-facts.com/mars/'
    astrogeo_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'



    # Visit NASA news site, scrape latest headline and teaser
    browser.visit(news_url)
    time.sleep(0.1)

    news_html = browser.html
    news_soup = bs(news_html, 'html.parser')

    articles = news_soup.find_all('li', class_='slide')
    latest_article = articles[0]
    latest_headline = latest_article.find('div', class_='content_title').text
    latest_teaser = latest_article.find('div', class_='article_teaser_body').text



    # Visit JPL images site
    browser.visit(images_url)
    time.sleep(0.1)

    # Navigate to full-size image, and scrape featured image URL
    full_image_button = browser.find_by_id('full_image')
    full_image_button.click()

    browser.links.find_by_partial_text('more info').click()
    time.sleep(0.1)

    featured_image_html = browser.html
    featured_image_soup = bs(featured_image_html,'html.parser')

    featured_image_loc = featured_image_soup.find('figure', class_='lede')
    featured_image_url = f"{jpl_url}{featured_image_loc.find('a')['href']}"



    # Visit Mars Facts site
    browser.visit(mars_facts_url)
    time.sleep(0.1)

    mars_facts_table = pd.read_html(mars_facts_url, match='Recorded By')[0]
    mars_facts_table.columns = ["Description", "Mars"]

    mars_facts_html = mars_facts_table.to_html(index=False, classes="table table-striped")



    # Visit Mars hemisphere image site
    time.sleep(0.1)
    browser.visit(astrogeo_url)

    hemisphere_image_urls = []

    # Loop through sections with 'Hemisphere Enhanced' text and find URLs
    for x in range(4):
        # Navigate to image full size
        astrogeo_button = browser.links.find_by_partial_text('Hemisphere Enhanced')[x]
        astrogeo_button.click()

        hemisphere_html = browser.html
        hemisphere_soup = bs(hemisphere_html,'html.parser')
        hemisphere_title = hemisphere_soup.find('h2', class_='title').text
        hemisphere_url = hemisphere_soup.find('div', class_='downloads').find('li').find('a')['href']
        
        # Save title and URL in dictionary
        hemisphere_image = {
            "title": hemisphere_title,
            "img_url": hemisphere_url
        }

        hemisphere_image_urls.append(hemisphere_image)

        # Return to initial page
        browser.back()
        time.sleep(0.1)

    browser.quit()



    # Create dictionary to store all scrape results
    mars_data = {}
    mars_data["headline"] = latest_headline
    mars_data["teaser"] = latest_teaser
    mars_data["featured_image"] = featured_image_url
    mars_data["facts_table"] = mars_facts_html
    mars_data["hemispheres"] = hemisphere_image_urls

    return mars_data