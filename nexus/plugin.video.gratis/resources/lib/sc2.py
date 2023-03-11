import requests
import datetime
import re
from bs4 import BeautifulSoup as bs
from base64 import b64decode
from .plugin import m

base_url = 'https://soccercatch.com'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
headers = {"User-Agent":user_agent, 'Referer': base_url}

def date_url(date):
    return f'{base_url}/api/matches/date?date={date}'

def date_post(url):
    return requests.post(url, headers=headers).text

def get_dates():
    dates = []
    d = datetime.date(2021,1,18)
    while d <= datetime.date.today():
        dates.append([datetime.datetime.strftime(d,'%A, %B %d, %Y'), datetime.datetime.strftime(d,'%d-%m-%Y')])
        d += datetime.timedelta(days=1)
    return list(reversed(dates))

def main(icon):
    dates = get_dates()
    for name, number in dates:
        url = date_url(number)
        m.add_dir(name, url, 'soccer_matches', icon, m.addon_fanart, '')

def matches(url):
    r = date_post(url)
    soup = (bs(r, 'html.parser'))
    _matches = soup.find_all('a', class_='match-list-content')
    for match in _matches:
        url = f"{base_url}{match['href']}"
        home = match.find(class_='match-list-home')
        away = match.find(class_='match-list-away')
        home_name = home.img['alt']
        home_icon = home.img['src']
        away_name = away.img['alt']
        away_icon = away.img['src']
        name = f'{home_name} vs {away_name}'
        m.add_dir(name, url, 'soccer_get_links', home_icon, away_icon, name, isFolder=False)

def get_links(name, url, icon):
    links = []
    title = ''
    r = requests.get(url, headers=headers).text
    soup = bs(r, 'html.parser')
    highlights = soup.find_all(class_='iframe-responsive')
    urls = re.findall(' src="(.+?)"| src=\'(.+?)\'', str(highlights))
    highlight_links = []
    for url1, url2 in urls:
        if url1 != '':
            highlight_links.append(url1)
        if url2 != '':
            highlight_links.append(url2)
    if len(highlight_links) > 0:
        for link in highlight_links:
            if 'youtube' in link:
                yt_id = link.split('/')[-1]
                yt_link = f'plugin://plugin.video.youtube/play/?video_id={yt_id}'
                links.append(['Highlights - YouTube', yt_link])
    fullmatch = soup.find_all(class_='hidden-link')
    
    for match in fullmatch:
        link = re.findall('data-url="(.+?)"', str(match))[0]
        link = b64decode(link).decode('utf-8').rstrip('.html')
        if 'payskip.org' in link:
            continue
        host = link.split('/')[2]
        title = match.text.replace('Main Player - ', '')
        title = title.replace('Alternative Player - ', '')
        title = title.replace('Official - ', '')
        title = title.replace('Fast Direct Link - ', '')
        title = f'{title} - {host}'
        if not link in links:
            links.append([title, link])
    if links:
        from .player2 import player
        player.play_video(name, links, icon, name)

def runner(p: dict):
    #---Params---#
    name = p.get('name', '')
    url = p.get('url', '')
    mode = p.get('mode', 'main_menu')
    if mode and str.isdecimal(mode):
        mode = int(mode)
    icon = p.get('icon', m.addon_icon)
    page = p.get('page', '1')
    if str.isdecimal(page):
        page = int(page)
    
    #---Modes---#
    if mode == 'soccer_main':
        main(icon)

    elif mode == 'soccer_matches':
        matches(url)

    elif mode == 'soccer_get_links':
        get_links(name, url, icon)