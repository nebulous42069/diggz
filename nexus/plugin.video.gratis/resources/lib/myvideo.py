import xbmcvfs
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from .plugin2 import m

BASE_URL = 'https://get.myvideolinks.net'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
HEADERS = {
    'User-Agent': USER_AGENT,
    'Referer': BASE_URL
}
MAIN_LIST = {
    "Movies": f"{BASE_URL}/category/movies/",
    "2022": f"{BASE_URL}/category/movies/2022/",
    "Older Movies": f"{BASE_URL}/category/movies/older-movies/",
    "3-D": f"{BASE_URL}/category/movies/3-d/",
    "Tv Shows": f"{BASE_URL}/category/tv-shows/",
    "Complete Seasons": f"{BASE_URL}/category/tv-shows/complete-seasons/",
    "Last 70 Posts": f"{BASE_URL}/last-70-posts/"
}

SEARCH_URL = f'{BASE_URL}?s='
SEARCH_HISTORY = m.addon_data + 'search_history.json'

def search_history():
    m.add_dir('New Search', '', 'vid_search', m.addon_icon, m.addon_fanart, 'New Search')
    if xbmcvfs.exists(SEARCH_HISTORY):
        with open(SEARCH_HISTORY, 'r', encoding='utf-8', errors='ignore') as f:
            history = json.load(f)
        if history:
            history.reverse()
        for query in history:
            m.add_dir(query, '', 'vid_search', m.addon_icon, m.addon_fanart, '')

def search(query=''):
    history = []
    if not query or query == 'New Search':
        query = m.from_keyboard()
    if query:
        if not xbmcvfs.exists(SEARCH_HISTORY):
            with open(SEARCH_HISTORY, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(json.dumps(history))
        with open(SEARCH_HISTORY, 'r', encoding='utf-8', errors='ignore') as f:
            history = json.load(f)
        if not query in history:
            history.append(query)
        with open(SEARCH_HISTORY, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(json.dumps(history))
        sub_menu(SEARCH_URL + quote_plus(query))
       
def main_scrape():
    item_list = {}
    response = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser').nav
    for a in soup.find_all('a'):
        title = a.text.lower().capitalize()
        link = a['href']
        item_list[title] = link
    print(item_list)

def sub_menu(url: str):
    infolabels = {}
    cast = []
    description = ''
    r = requests.get(url, headers=HEADERS)
    if 'Try a new keyword' in r.text:
        return
    soup = BeautifulSoup(r.text, 'html.parser')
    if soup.find('article').header:
        for article in soup.find_all('article'):
            title = article.header.h2.a.text
            if '1080p' in title:
                quality = ' - 1080p'
            elif '720p' in title:
                quality = ' - 720p'
            elif '480p' in title:
                quality = ' - 480p'
            else:
                quality = ''
            link = article.header.h2.a['href']
            thumbnail = article.find(class_ = 'entry-content cf').img['src']
            fanart = m.addon_fanart
            imdb = article.find(class_ = 'entry-content cf').find('a')
            if imdb is not None:
                imdb = imdb['href'].replace('https://www.imdb.com/title/', '').rstrip('/')
                response = requests.get(f'https://api.themoviedb.org/3/find/{imdb}?api_key=f090bb54758cabf231fb605d3e3e0468&language=en-US&external_source=imdb_id', headers=HEADERS).json().get('movie_results')
                if response:
                    tmdb_id = response[0]['id']
                    from .tmdb import tmdb
                    r = requests.get(tmdb.movie_url(int(tmdb_id))).json()
                    from .infolabels import Infolabels
                    i = Infolabels(r, 'movie')
                    infolabels, cast = i.infolabels_and_cast()
                    title = infolabels.get('title', title)
                    thumbnail = i.get_thumbnail()
                    fanart = i.get_fanart()
                    description = infolabels.get('plot', '')
                    premiered = infolabels.get('premiered')
                    if premiered:
                        year = f"({premiered.split('-')[0]})"
                        title = f'{title} {year}'
            
            m.add_dir(title + quality, link, 'vid_player', thumbnail, fanart, description, infolabels=infolabels, cast=cast, isFolder=False)
    else:
       items = soup.find(class_ = 'entry-content cf').find_all('li')
       for li in items[:7]:
           m.add_dir(li.a.text, li.a['href'], 'vid_sub', m.addon_icon, m.addon_fanart, li.a.text, isFolder=True)
       for li in items[7:]:
            m.add_dir(li.a.text, li.a['href'], 'vid_player', m.addon_icon, m.addon_fanart, li.a.text, isFolder=False)
        
    pagination = soup.find_all(class_ = 'page larger')
    if pagination:
        m.add_dir('Next Page', pagination[0]['href'], 'vid_sub', 'https://cdn-icons-png.flaticon.com/512/122/122630.png', m.addon_fanart, 'Next Page', isFolder=True)

def get_links(name: str, url: str, icon:str, description: str):
    from .player2 import player
    item_list = []
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.find(class_= 'entry-content cf')
    titles = content.find_all('h4')
    if titles:
        links = content.find_all('ul')
        for x in range(len(titles[1:])):
            for a in links[x].find_all('a'):
                if 'tubeload' in a.text or 'userload' in a.text:
                    item_list.append([f"{titles[x+1].text} {a.text.split('/')[0]}", a['href']])
    
    else:
        for a in soup.find_all(class_ = 'autohyperlink'):
            if 'tubeload' in a.text or 'userload' in a.text:
                item_list.append([a.text.split('/')[0], a['href']])
    
    player.play_video(name, item_list, icon, description)

def main():
    for key in MAIN_LIST:
        m.add_dir(key, MAIN_LIST[key], 'vid_sub', m.addon_icon, m.addon_fanart, key)
    m.add_dir('Search', '', 'vid_search_history', m.addon_icon, m.addon_fanart, 'Search')

def runner(p: dict):
    name = p.get('name', '')
    url = p.get('url', '')
    mode = p.get('mode')
    icon = p.get('icon', m.addon_icon)
    description = p.get('description', '')
    page = p.get('page', '')
    if page: page = int(page)
    
    elif mode == 'vid_main':
        main()
    
    elif mode == 'vid_sub':
        sub_menu(url)
    
    elif mode == 'vid_search_history':
        search_history()
    
    elif mode == 'vid_search':
        search(query = name)
    
    elif mode == 'vid_player':
        get_links(name, url, icon, description)