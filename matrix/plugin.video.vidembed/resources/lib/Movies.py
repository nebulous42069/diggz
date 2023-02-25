import requests
from bs4 import BeautifulSoup
from resources.lib.browserHeaders import headers


def movies(page):
    url = f"https://vidembed.io/movies?page={str(page)}"
    r = requests.get(url, headers=headers).text
    soup = BeautifulSoup(r, 'html.parser')
    names = []
    images = []
    links = []
    all = []
    for img in soup.find_all('div', {'class': 'picture'}):
        if not 'season' in img.img['src'].split('-'):
            names.append(img.img['alt'])
            images.append(img.img['src'])
    for a in soup.find_all('a', {'href': True}):
        if '/videos/' in a['href']:
            if not 'season' in a['href'].split('-'):
                links.append(f"https://vidembed.io{a['href']}")
    for i in range(len(names)):
        all.append(f"{names[i]}---{links[i]}---{images[i]}")
    return all



def searchMovies(query):
    url = f"https://vidembed.io/search.html?keyword={query}"
    r = requests.get(url, headers=headers).text
    soup = BeautifulSoup(r, 'html.parser')
    names = []
    images = []
    links = []
    all = []
    for img in soup.find_all('div', {'class': 'picture'}):
        if not 'season' in img.img['src'].split('-'):
            names.append(img.img['alt'])
            images.append(img.img['src'])
    for a in soup.find_all('a', {'href': True}):
        if '/videos/' in a['href']:
            if not 'season' in a['href'].split('-'):
                links.append(f"https://vidembed.io{a['href']}")

    for i in range(len(names)):
        all.append(f"{names[i]}---{links[i]}---{images[i]}")
    return all



def cinema_movies(page):
    url = f"https://vidembed.io/cinema-movies?page={str(page)}"
    r = requests.get(url, headers=headers).text
    soup = BeautifulSoup(r, 'html.parser')
    names = []
    images = []
    links = []
    all = []
    for img in soup.find_all('div', {'class': 'picture'}):
        if not 'season' in img.img['src'].split('-'):
            names.append(img.img['alt'])
            images.append(img.img['src'])
    for a in soup.find_all('a', {'href': True}):
        if '/videos/' in a['href']:
            if not 'season' in a['href'].split('-'):
                links.append(f"https://vidembed.io{a['href']}")
    for i in range(len(names)):
        all.append(f"{names[i]}---{links[i]}---{images[i]}")
    return all