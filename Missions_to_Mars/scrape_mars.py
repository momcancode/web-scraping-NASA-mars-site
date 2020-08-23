#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup
from time import sleep


# In[2]:


# Import Splinter and set the chromedriver path
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ## NASA Mars News scraping

# In[3]:


# URL of page to be scraped
url = "https://mars.nasa.gov/news/"

# Use splinter to navigate the site
browser.visit(url)


# In[4]:


# Let the script to wait for the browser to be fully loaded
sleep(1)


# In[5]:


# Create BeautifulSoup object; parse with 'lxml'
html = browser.html
soup = BeautifulSoup(html, 'lxml')


# In[6]:


# Select the first element containing the latest news
latest_news = soup.select_one("ul.item_list li.slide")
print(latest_news.prettify())


# In[7]:


# Retrieve the latest news title
news_title = latest_news.find('div', class_="content_title").get_text()
news_title


# In[8]:


# Retrieve the latest news paragraph
news_p = latest_news.find('div', class_='article_teaser_body').get_text()
news_p


# ## JPL Mars Space Images - Featured Image

# In[9]:


# URL of page to be scraped
image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

# Use splinter to navigate the site
browser.visit(image_url)


# In[10]:


# Click the link under id "full_image" to access the featured image
browser.click_link_by_id("full_image")


# In[11]:


# Click the link under text "more info" to access the largesize featured image
browser.links.find_by_partial_text("more info").click()


# In[12]:


# Create BeautifulSoup object; parse with 'lxml'
html = browser.html
soup = BeautifulSoup(html, 'lxml')


# In[13]:


# Retrieve the path to the largesize featured image
large_image_url = soup.find(class_="main_image")["src"]


# In[14]:


# Assign the url string to a variable called featured_image_url
featured_image_url = f"https://www.jpl.nasa.gov{large_image_url}"
featured_image_url


# ## Mars Facts

# In[15]:


# Dependencies
import pandas as pd


# In[16]:


# URL of page to be scraped
fact_url = "https://space-facts.com/mars/"

# Use Panda's `read_html` to parse the url
scraped_dfs = pd.read_html(fact_url)


# In[17]:


# Overview of the list of the scraped dataframes
for df in scraped_dfs:
    display(df)


# In[18]:


# Select the dataframe containing facts about the planet including Diameter, Mass, etc.
df = scraped_dfs[0]
df


# In[19]:


# Assign the columns Description and Mars to the dataframe and set Description as index
df.columns = ["Description", "Mars"]
df.set_index("Description", inplace=True)
df


# In[20]:


# Use Pandas to convert the data to a HTML table string
html_table = df.to_html()
print(html_table)


# In[21]:


df.to_html('table.html')


# ## Mars Hemispheres

# In[22]:


# URL of page to be scraped
hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

# Use splinter to navigate the site
browser.visit(hemisphere_url)


# In[23]:


# Extract the hemisphere titles with embedded links
html = browser.html
soup = BeautifulSoup(html, 'lxml')
text_to_search = soup.find_all("h3")


# In[24]:


# Overview of the hemisphere titles
for text in text_to_search:
    print(text)


# In[25]:


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


# In[26]:


hemisphere_image_urls

