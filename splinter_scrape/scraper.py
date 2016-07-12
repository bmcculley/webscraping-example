from splinter import Browser
from bs4 import BeautifulSoup
from time import sleep

# set the path to phantomjs
executable_path = {'executable_path': '</path/to/phantomjs>'}

# define the function that will strip the info we want from the page


def scrape_data(html):
    soup = BeautifulSoup(html, "html.parser")
    post_div = soup.find('div', {'class': 'postList'})
    posts = post_div.find_all('div', {'class': 'post'})
    page_posts = {}
    for n, post in enumerate(posts):
        title = post.find('h2', {'class': 'postTitle'}).text
        content = post.find('div', {'class': 'postContent'}).text
        page_posts[n] = [title, content]
    return page_posts


with Browser('phantomjs', **executable_path) as browser:
    url = "http://127.0.0.01:5000/"
    browser.visit(url)
    if browser.status_code.is_success():
        print(scrape_data(browser.html))
    	for i in xrange(3): # we have a bit of a janky react setup
        	next_link = browser.find_by_css('.next')
        	next_link.click()
        	sleep(3) # again with the janky react setup
        	if browser.status_code.is_success():
        		print(scrape_data(browser.html))
        	else:
        		print("oops, something went wrong.")
    else:
        print("oops, something went wrong.")
    browser.quit()
