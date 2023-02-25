import requests, bs4, resolveurl
from resources.lib.browserHeaders import headers
try: from urllib.parse import urlparse
except ImportError: from urllib import urlparse
import xbmcgui

def findURLs(iframe_html):
    soup = bs4.BeautifulSoup(iframe_html, 'html.parser')
    links = soup.find_all('li', {'class': 'linkserver', 'data-status': '1'})
    names, urls = [], []
    for link in links:
        names.append(link.text)
        urls.append(link['data-video'])
    if len(urls) == 1: return urls[0]
    dialog = xbmcgui.Dialog()
    index = dialog.select('Select Server', names)
    if index == -1: exit()
    if names[index] == "StreamSB":
        parsed = urlparse(urls[index])
        path = parsed.path
        return "http://sbplay2.com" + path
    return urls[index]

def grab(url):
    html = requests.get(url, headers=headers).text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    iframe = soup.find('iframe')
    iframe_url = iframe['src'].replace("//", "https://")
    iframe_html = requests.get(iframe_url, headers=headers).text
    URLtoResolve = findURLs(iframe_html)
    if resolveurl.HostedMediaFile(URLtoResolve): return resolveurl.resolve(URLtoResolve)
    return ""
