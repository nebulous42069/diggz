import xbmcplugin
import sys
from .plugin import m

SPORTS = {
    'Hockey': 'https://nhlvideo.net',
    'Basketball': 'https://basketball-video.com',
    'American Football': 'https://nfl-video.com',
    'Baseball': 'https://mlblive.net'
}

SPORTS2 = {
    'MMA': 'https://fullmatchtv.com/category/other-sports/wwe-mma/',
    'Rugby': 'https://fullmatchtv.com/category/other-sports/rugby/',
    'Motorsports': 'https://fullmatchtv.com/category/other-sports/motorsports/',
    'AFL': 'https://fullmatchtv.com/category/other-sports/afl/'
}

FILTERS = [
    '2020-21 NHL Replays',
    'NHL Archive Full Games Replays',
    'NHL All-Star Games',
    'Full Games Replays',
    'Teams',
    'Replays per teams',
    'Disclaimer',
    'Replays per year',
    '2022-23 NBA Season',
    '2021-22 NBA Season',
    'NBA All Star Games',
    'NFL 2022',
    'Hard Knocks 2022 Detroit Lions',
    'NFL Full Games',
    'All Full Games Replay',
    'NFL Video by teams',
    'NCAAF Video by teams'
]

def get_links(name:str, url: str, thumbnail: str) -> list:
    links = []
    splitted = url.split('/')
    referer = '/'.join(splitted[:3])
    soup = m.get_soup(url, referer=referer)
    iframes = soup.find_all('iframe')
    for iframe in iframes:
        link = iframe['src']
        if link.startswith('//'):
            link = f'https:{link}'
        if 'youtube' in link:
            yt_id = link.split('/')[-1]
            link = f'plugin://plugin.video.youtube/play/?video_id={yt_id}'
            title = 'Highlights'
        else:
            title = link.split('/')[2]
        if 'facebook.com' in title:
            continue
        links.append([title, link])
    if links:
        from .player2 import player
        player.play_video(name, links, thumbnail, name)

def submenu(name: str, url: str, page, name2=''):
    if name2:
        name = name2
    xbmcplugin.setPluginCategory(int(sys.argv[1]), name)
    splitted = url.split('/')
    referer = '/'.join(splitted[:3])
    soup = m.get_soup(f'{url}?page{page}', referer=referer)
    games = soup.find_all(class_='short_item block_elem')
    for game in games:
        title = game.h3.a.text.replace('Full Game Replay ', '').rstrip(' NHL')
        link = f"{referer}{game.a['href']}"
        thumbnail = f"{referer}{game.a.img['src']}"
        m.add_dir(title, link, 'replays_links', thumbnail, thumbnail, title, isFolder=False)
    m.add_dir('Next Page', url, 'replays_submenu', m.addon_icon, m.addon_fanart, 'Next Page', name2=name, page=page+1)
        
def categories(url):
    category_list = []
    soup = m.get_soup(url, referer=url)
    cats = soup.find(id='list_cat')
    for a in cats.find_all('a'):
        try:
            if a.text.strip() in FILTERS:
                continue
            title = a.text.strip()
            link = a['href']
            if title in category_list:
                continue
            category_list.append(title)
            m.add_dir(title, link, 'replays_submenu', m.addon_icon, m.addon_fanart, title)
        except KeyError:
            continue
 
def main():
    for sport in SPORTS.keys():
       m.add_dir(sport, SPORTS[sport], 'replays_categories', m.addon_icon, m.addon_fanart, f'Watch {sport} Replays')
    m.add_dir('Soccer', '', 'soccer_main', m.addon_icon, m.addon_fanart, 'Football Replays')
    for sport in SPORTS2.keys():
        m.add_dir(sport, SPORTS2[sport], 'replays2_submenu', m.addon_icon, m.addon_fanart, f'Watch {sport} Replays')

def runner(p: dict):
    #---Params---#
    name = p.get('name', '')
    name2 = p.get('name2', '')
    url = p.get('url', '')
    mode = p.get('mode', 'main_menu')
    if mode and str.isdecimal(mode):
        mode = int(mode)
    icon = p.get('icon', m.addon_icon)
    page = p.get('page', '1')
    if str.isdecimal(page):
        page = int(page)
        
    #---Modes---#
    if mode == 'replays_main':
        main()
    if mode == 'replays_categories':
        categories(url)
    elif mode == 'replays_submenu':
        submenu(name, url, page, name2=name2)
    elif mode == 'replays_links':
        get_links(name, url, icon)
    elif mode == 'replays2_submenu':
        from .replays import Replays
        replays = Replays()
        replays.sub_menu(name, url)