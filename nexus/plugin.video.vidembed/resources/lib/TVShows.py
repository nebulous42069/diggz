import requests
from bs4 import BeautifulSoup
from resources.lib.browserHeaders import headers

def tvshowstab(page):
    url = f"https://vidembed.io/series?page={str(page)}"
    r = requests.get(url, headers=headers).text
    soup = BeautifulSoup(r, 'html.parser')
    names = []
    images = []
    links = []
    all = []
    for img in soup.find_all('div', {'class': 'picture'}):
        if 'season' in img.img['src'].split('-'):
            names.append(img.img['alt'].split(" Episode")[0])
            images.append(img.img['src'])
    for a in soup.find_all('a', {'href': True}):
        if '/videos/' in a['href']:
            if 'season' in a['href'].split('-'):
                links.append(f"https://vidembed.io{a['href']}")
    for i in range(len(names)):
        all.append(f"{names[i]}---{links[i]}---{images[i]}")
    return all



def featuredtvshowstab(page):
    url = f"https://vidembed.io/recommended-series?page={str(page)}"
    r = requests.get(url, headers=headers).text
    soup = BeautifulSoup(r, 'html.parser')
    names = []
    images = []
    links = []
    all = []
    for img in soup.find_all('div', {'class': 'picture'}):
        if 'season' in img.img['src'].split('-'):
            names.append(img.img['alt'].split(" Episode")[0])
            images.append(img.img['src'])
    for a in soup.find_all('a', {'href': True}):
        if '/videos/' in a['href']:
            if 'season' in a['href'].split('-'):
                links.append(f"https://vidembed.io{a['href']}")
    for i in range(len(names)):
        all.append(f"{names[i]}---{links[i]}---{images[i]}")
    return all





def searchTVShows(query):
    url = f"https://vidembed.io/search.html?keyword={query}"
    r = requests.get(url, headers=headers).text
    soup = BeautifulSoup(r, 'html.parser')
    names = []
    images = []
    links = []
    all = []
    for img in soup.find_all('div', {'class': 'picture'}):
        if 'season' in img.img['src'].split('-'):
            names.append(img.img['alt'].split(" Episode")[0])
            images.append(img.img['src'])
    for a in soup.find_all('a', {'href': True}):
        if '/videos/' in a['href']:
            if 'season' in a['href'].split('-'):
                links.append(f"https://vidembed.io{a['href']}")
    for i in range(len(names)):
        all.append(f"{names[i]}---{links[i]}---{images[i]}")
    return all



def listEpisodes(url):
    qv = url.split('/videos/')[1].split('-')[0]
    r = requests.get(url, headers=headers).text
    soup = BeautifulSoup(r, 'html.parser')
    names = []
    images = []
    links = []
    all = []
    for img in soup.find_all('div', {'class': 'picture'}):
        if 'season' in img.img['alt'].lower():
            if qv in img.img['alt'].lower():
                names.append(img.img['alt'])
                images.append(img.img['src'])
    for a in soup.find_all('a', {'href': True}):
        if "/videos/" in a['href']:
            if qv in a['href']:
                links.append("https://vidembed.io" + a['href'])
    for i in range(len(names)):
        all.append(names[i] + '---' + links[i] + '---' + images[i])
    return all