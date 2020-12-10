# web-scraping-challenge

This project uses the splinter, beautifulsoup, and pandas python libraries to scrape text, image URLs, and tables from several websites with data about Mars. A web app, created with the flask python library, displays the scraped data in one page.

The index.html file uses Bootstrap to apply formatting to the web app, and displays data saved to a mongodb database through pymongo. If the database has been populated, the landing page will load information and photos relating to Mars. If the user loads the page before having an active mars_app database, only the site jumbotron with the "Scrape new data" button will show. When clicked, data will be scraped and saved to the database, and the page will then load the rest of the page.
