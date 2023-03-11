import xbmcplugin
import xbmcgui
import requests
import sys
import re
import json
from bs4 import BeautifulSoup
from html.parser import unescape
from .plugin2 import m

BASE_URL = 'https://daddylivehd.sx'
CHANNELS = f'{BASE_URL}/24-7-channels.php'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
HEADERS = {
    'User-Agent': USER_AGENT,
    'Referer': f'{BASE_URL}/'
}

TITLE = re.compile(r'">(.+?)</')
MATCH = re.compile('(<hr/>.+?</span>)')
HR = re.compile('<hr/>(.+?)<span style=')
HREF = re.compile('href="(.+?)" rel=')
SOURCE = re.compile("source:'(.+?)'")


def main():
    xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Live Sports')
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
    item_list = {}
    response = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    recent = soup.find(class_='recent')
    
    for h2 in str(recent).split('h2 style')[2:]:
        cat = re.findall(TITLE, h2)
        if cat:
            category = cat[0]
            if category.lower() in ['tv show']:
                continue
            if not item_list.get(category):
                item_list[category] = []
        hr = [h for h in h2.split('<hr/>')[1:]]
        for a in hr:
            game_title = re.compile("(\d\d:\d\d.+?)\<span", re.DOTALL|re.MULTILINE).findall(str(a))
            game_link = re.compile("\<a href=\"(.+?)\" rel", re.DOTALL|re.MULTILINE).findall(str(a))
            if game_title and game_link:
                item_list[category].append(
                    [
                        unescape(game_title[0].strip().replace('<strong>', '').replace('</strong>', '')),
                        [f'{BASE_URL}{gl}' for gl in game_link]
                    ]
                )
    
    for item in item_list.keys():
        if item_list[item]:
            m.add_dir(item, json.dumps(item_list[item]), 'live_submenu', m.addon_icon, m.addon_fanart, item)

def get_channels():
    xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Live Channels')
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
    response = requests.get(CHANNELS, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    for a in soup.find_all('a'):
        title = a.text
        link = f"{BASE_URL}{a['href']}"
        m.add_dir(title, link, 'live_links', m.addon_icon, m.addon_fanart, title, isFolder=False)

def submenu(name: str, url: str):
    xbmcplugin.setPluginCategory(int(sys.argv[1]), name)
    for title, link in json.loads(url):
        m.add_dir(title, json.dumps(link), 'live_links', m.addon_icon, m.addon_fanart, title, isFolder=False)

def get_links(name, url: str):
    if url.startswith('['):
        url = json.loads(url)
        if type(url) == list:
            if len(url) > 1:
                url = m.get_multilink(url)
            else:
                url = url[0]
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    recent = soup.find(class_='recent')
    iframe = recent.find('iframe')
    if iframe:
        url2 = iframe.get('src')
        if url2:
            headers = {
                'User-Agent': USER_AGENT,
                'Referer': url
            }
            response2 = requests.get(url2, headers=headers)
            links = re.findall(SOURCE, response2.text)
            if links:
                link = f'{links[-1]}|Referer={url2}&User-Agent={USER_AGENT}'
                liz = xbmcgui.ListItem(name, path=link)
                liz.setInfo('video', {'title': name, 'plot': name})
                liz.setArt({'thumb': m.addon_icon, 'icon': m.addon_icon, 'poster': m.addon_icon})
                liz.setProperty('inputstream', 'inputstream.adaptive')
                liz.setProperty('inputstream.adaptive.manifest_type', 'hls')
                liz.setMimeType('application/x-mpegURL')
                xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, liz)

def runner(p):
    name = p.get('name', '')
    url = p.get('url', '')
    mode = p.get('mode')
    page = p.get('page', '')
    if page: page = int(page)
    
    if mode == 'live_main':
        main()
    
    elif mode == 'live_submenu':
        submenu(name, url)
    
    elif mode == 'live_channels':
        get_channels()
    
    elif mode == 'live_links':
        get_links(name, url)