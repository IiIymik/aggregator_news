import aiohttp
import asyncio
import datetime
from aiohttp import web
import aiohttp_jinja2
import jinja2
from bs4 import BeautifulSoup
import requests

# URL's News
hn = 'https://thehackernews.com/'
silicon = 'https://www.siliconvalley.com/news/'
rp = 'https://hackspace.raspberrypi.org/articles'

#Hacker News    
async def get_hn():
    hn_list = []
    r = requests.get(hn).text
    soup = BeautifulSoup(r, 'lxml')
    posts = soup.find_all('div', class_='body-post clear')
    for post in posts:
        title = post.find('h2', class_='home-title').text
        url = post.find('a').get('href')
        data = {'title':title,
                'url':url}
        hn_list.append(data)

    return hn_list
#Silicon News
async def get_silicon_news():
    silicon_news = []
    r = requests.get(silicon).text
    soup = BeautifulSoup(r, "lxml")
    posts = soup.find_all("article")
    for post in posts:
        title = post.find("a", class_="article-title").get('title')
        url = post.find("a", class_="article-title").get("href")

        data = {'title': title,
                'url': url,
                }

        silicon_news.append(data)

    return silicon_news
    
#HackSpace News
async def get_hspace_news():
    hackspace_news = []
    r = requests.get(rp).text
    soup = BeautifulSoup(r, "lxml")
    posts = soup.find_all("article")
    for post in posts:
        title = post.find("p", class_="o-type-sub-heading u-weight-bold rspec-article-card--heading").text
        url = post.find("a").get("href")

        data = {'title': title,
                'url': url,
                }

        hackspace_news.append(data)
    
    return hackspace_news

@aiohttp_jinja2.template('index.html')
async def main_page(requests):
    context = {
        'hn_list': await get_hn(),
        'hackspace_news': await get_hspace_news(),
        'silicon_news': await get_silicon_news(),
    }
    return context


if __name__ == "__main__":
    app = web.Application()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./template'))
    app.add_routes([web.get('/index', main_page)])
    web.run_app(app)