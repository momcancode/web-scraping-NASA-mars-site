# Dependencies
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

# Import Splinter and set the chromedriver path
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    ## NASA Mars News scraping

    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/"

    # Use splinter to navigate the site
    browser.visit(url)

    # Let the script to wait for the browser to be fully loaded
    sleep(1)

    # Create BeautifulSoup object; parse with 'lxml'
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    # Select the first element containing the latest news
    latest_news = soup.select_one("ul.item_list li.slide")

    # Retrieve the latest news title
    news_title = latest_news.find('div', class_="content_title").get_text()

    # Retrieve the latest news paragraph
    news_p = latest_news.find('div', class_='article_teaser_body').get_text()


    ## JPL Mars Space Images - Featured Image

    # URL of page to be scraped
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Use splinter to navigate the site
    browser.visit(image_url)

    # Click the link under id "full_image" to access the featured image
    browser.click_link_by_id("full_image")

    # Click the link under text "more info" to access the largesize featured image
    browser.links.find_by_partial_text("more info").click()

    # Create BeautifulSoup object; parse with 'lxml'
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    # Retrieve the path to the largesize featured image
    large_image_url = soup.find(class_="main_image")["src"]

    # Assign the url string to a variable called featured_image_url
    featured_image_url = f"https://www.jpl.nasa.gov{large_image_url}"


    ## Mars Facts

    # URL of page to be scraped
    fact_url = "https://space-facts.com/mars/"

    # Use Panda's `read_html` to parse the url
    scraped_dfs = pd.read_html(fact_url)

    # Select the dataframe containing facts about the planet including Diameter, Mass, etc.
    df = scraped_dfs[0]

    # Assign the columns Description and Mars to the dataframe and set Description as index
    df.columns = ["Description", "Mars"]
    df.set_index("Description", inplace=True)

    # Use Pandas to convert the data to a HTML table string
    html_table = df.to_html()


    ## Mars Hemispheres

    # URL of page to be scraped
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # Use splinter to navigate the site
    browser.visit(hemisphere_url)

    # Extract the hemisphere titles with embedded links
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    text_to_search = soup.find_all("h3")

    hemisphere_image_urls = list()

    for text in text_to_search:
        
        # Click each of the links to the hemispheres in order to find the image url to the full resolution image.
        browser.links.find_by_partial_text(text.get_text()).click()
        sleep(1)
        html = browser.html
        soup = BeautifulSoup(html, 'lxml')
        
        # Retrieve the Hemisphere title containing the hemisphere name
        title = text.get_text().split("Enhanced")[0]
        
        # Retrieve the image url string for the full resolution hemisphere image
        img_url = soup.select_one("dd a")["href"]
        
        # Append the dictionary with the image url string and the hemisphere title to a list
        hemisphere_image_urls.append({
            "title": title,
            "img_url": img_url
        })
        
        browser.visit(hemisphere_url) 
        sleep(1)
    
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts": html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Quite the browser after scraping
    browser.quit()

    # Return results
    return mars_data

# if running from command line, show the scraped data results
if __name__ == "__main__":
    result = scrape()
    print(result)