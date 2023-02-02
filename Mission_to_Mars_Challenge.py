# %%
import panda as pd

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# %%
# set up executable path,
# set up the URL

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# %%
# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# %%
# set up HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# %%
# assign the title and summary text to variable
slide_elem.find('div', class_='content_title')

# %%
# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# %%
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# %% [markdown]
# ### Featured Images

# %%
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# %%
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# %%
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# %%
# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# %%
# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# %% [markdown]
# # ## Mars Facts

# %%
# creating new DataFrame from HTML table. Pandas function read_html()
# searching specifically for and returns a list of tables found 
# in the HTML. 
# specify an index of 0, telling Pandas pull ONLY the first table
# it encounters, or first item in the list. Then, it turns table 
# into a DataFrame
df = pd.read_html('https://galaxyfacts-mars.com')[0]

# Assign columns to new DataFrame for addionitional clarity
df.columns=['description', 'Mars', 'Earth']

# .set_index() function, turning Description column into the 
# DataFrame's index.
# inplace=True means the updated index will remain in place, without
# having to reassign the DataFrame to a new variable
df.set_index('description', inplace=True)
df

# %%
# converting DataFrame back into HTML-ready code using .to_html()
df.to_html()

# %%
# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# %%
# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for hemi in range(4):
    # Browse through each article
    browser.links.find_by_partial_text('Hemisphere')[hemi].click()
    
    # Parse the HTML
    html = browser.html
    hemi_soup = soup(html,'html.parser')
    
    # Scraping
    title = hemi_soup.find('h2', class_='title').text
    img_url = hemi_soup.find('li').a.get('href')
    
    # Store findings into a dictionary and append to list
    hemispheres = {}
    hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
    hemispheres['title'] = title
    hemisphere_image_urls.append(hemispheres)
    
    # Browse back to repeat
    browser.back()
    

# %%
# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# %%
# Quit the brower from running anymore
browser.quit()


