from bs4 import BeautifulSoup
import requests

base_url = "http://127.0.0.01:5000/home"
urls = [
    base_url
]

for n, url in enumerate(urls):
    if n == 4: # the flask code is janky
        break
    r = requests.get(url)
    if r.status_code == 200:
        html = r.content
        soup = BeautifulSoup(html, "html.parser")
        post_div = soup.find('div', {'class': 'content'})
        posts = post_div.find_all('div', {'class': 'post'})
        page_posts = {}
        for n, post in enumerate(posts):
            title = post.find('h2', {'class': 'title'}).text
            content = post.find('div', {'class': 'article'}).text
            page_posts[n] = [title, content]
        print(page_posts)
        next_link = soup.find('a', {'class':'next'}).get("href")
        urls.append(base_url+str(next_link))
    else:
        print("oops, something went wrong...")