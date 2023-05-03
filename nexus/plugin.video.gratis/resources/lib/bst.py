import xbmcplugin
import sys
import re
from .plugin2 import Myaddon

base_url = 'https://bstsrs.one'
new_shows = base_url + '/new-shows'
all_shows = base_url + '/browse-shows'
most_popular = base_url + '/tv-shows/imdb_rating'


class BST(Myaddon):
    
    def __init__(self):
        self.index = {
                    '47ab07f2': ':',
                    '47ab07e7': '/',
                    '47ab07e6': '.',
                    '47ab0817': '_',
                    '47ab07e5': '-',
                    '47ab07f9': 'A',
                    '47ab07fa': 'B',
                    '47ab07fb': 'C',
                    '47ab07fc': 'D',
                    '47ab07fd': 'E',
                    '47ab07fe': 'F',
                    '47ab07ff': 'G',
                    '47ab0800': 'H',
                    '47ab0801': 'I',
                    '47ab0802': 'J',
                    '47ab0803': 'K',
                    '47ab0804': 'L',
                    '47ab0805': 'M',
                    '47ab0806': 'N',
                    '47ab0807': 'O',
                    '47ab0808': 'P',
                    '47ab0809': 'Q',
                    '47ab080a': 'R',
                    '47ab080b': 'S',
                    '47ab080c': 'T',
                    '47ab080d': 'U',
                    '47ab080e': 'V',
                    '47ab080f': 'W',
                    '47ab0810': 'X',
                    '47ab0811': 'Y',
                    '47ab0812': 'Z',
                    '47ab0819': 'a',
                    '47ab081a': 'b',
                    '47ab081b': 'c',
                    '47ab081c': 'd',
                    '47ab081d': 'e',
                    '47ab081e': 'f',
                    '47ab081f': 'g',
                    '47ab0820': 'h',
                    '47ab0821': 'i',
                    '47ab0822': 'j',
                    '47ab0823': 'k',
                    '47ab0824': 'l',
                    '47ab0825': 'm',
                    '47ab0826': 'n',
                    '47ab0827': 'o',
                    '47ab0828': 'p',
                    '47ab0829': 'q',
                    '47ab082a': 'r',
                    '47ab082b': 's',
                    '47ab082c': 't',
                    '47ab082d': 'u',
                    '47ab082e': 'v',
                    '47ab082f': 'w',
                    '47ab0830': 'x',
                    '47ab0831': 'y',
                    '47ab0832': 'z',
                    '47ab07e8': '0',
                    '47ab07e9': '1',
                    '47ab07ea': '2',
                    '47ab07eb': '3',
                    '47ab07ec': '4',
                    '47ab07ed': '5',
                    '47ab07ee': '6',
                    '47ab07ef': '7',
                    '47ab07f0': '8',
                    '47ab07f1': '9'
        }

    def get_url(self, string):
        for item in self.index.keys():
            string = string.replace(item, self.index[item])
        return string.replace('-', '')

    def get_latest(self, url):
        soup = self.get_soup(url)
        titles = soup.find_all(class_ = 'hgrid')
        item_list = []
        for title in titles:
            name = title.find(class_ = 'title tags').text
            ep_number = title.find('i').text
            ep_name = title.find('strong').text
            full_name = name + ' ' + ep_number.replace(' ','') + ' - "' + ep_name + '"'
            browse_now = title.find(class_ = 'browse_now morph')
            thumb = re.compile("url\('(.+?)&amp").findall(str(browse_now))[0]
            watch_now = title.find(class_ = 'watch_now morph')
            link = watch_now.get('href')
            fanart = re.compile("url\('(.+?)&amp").findall(str(watch_now))[0]
            item_list.append({'name': full_name, 'url': link, 'icon': thumb, 'fanart': fanart})
        if len(url.split('/'))==5:
            current_page = int(url.split('/')[-1])
            next_page = new_shows + '/' +str(current_page + 1)
        else:
            next_page = new_shows + '/2'
        item_list.append(next_page)
        return item_list

    def get_links(self, title, url, icon):
        soup = self.get_soup(url)
        links_soup = soup.find_all(class_='embed-selector asg-hover odd')
        links = []
        for link in links_soup:
            link_coded = re.compile("dbneg\('(.+?)'\)").findall(str(link))[0]
            host = re.compile("domain=(.+?)'").findall(str(link))[0]
            url = self.get_url(link_coded)
            links.append([host, url])
        from .player2 import Player
        Player().play_video(title, links, icon, title)

    def browse_shows(self, url):
        soup = self.get_soup(url).find_all('a', class_ = 'img_poster browse_now morph')
        item_list = []
        for item in soup:
            name = item['title']
            link = item['href']
            thumb = re.compile("url\('(.+?)&amp").findall(str(item))[0]
            item_list.append({'name': name, 'url': link, 'icon': thumb})
        if len(url.split('/'))==6:
            current_page = int(url.split('/')[-1])
            next_page = most_popular + '/' +str(current_page + 1)
        else:
            next_page = most_popular + '/2'
        item_list.append(next_page)
        return item_list

    def all_episodes(self, url):
        soup = self.get_soup(url)
        episodes = soup.find_all(class_='hgrid')
        item_list = []
        for episode in episodes:
            name1 = episode.find('a', class_='episode').text
            name2 = episode.find(class_='episode').text
            link = episode.find(class_='hb-image watch_now')['href']
            thumb = episode.find(class_='hb-image watch_now')['data-original'].split('&w')[0]
            item_list.append({'name': name1+' - '+name2, 'url': link, 'icon': thumb})
        return item_list

#---BS Menus---#

bst = BST()

def bshows1(url):
    for x in bst.get_latest(url)[:-1]:
        bst.add_dir(x.get('name'), x.get('url'), 'bst_get_links', x.get('icon'), x.get('fanart'),'', name2=x.get('name'), isFolder=False)
    bst.add_dir('Next Page', bst.get_latest(url)[-1], 'bst_new_shows', '', '', 'Next Page')

def bshows_series(url):
    for x in bst.browse_shows(url)[:-1]:
        bst.add_dir(x.get('name'), x.get('url'), 'bst_episodes', x.get('icon'), bst.addon_fanart,'')
    bst.add_dir('Next Page', bst.browse_shows(url)[-1], 'bst_browse_shows', '', '', 'Next Page')

def bshows_episodes(title, url):
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)
    for x in bst.all_episodes(url):
        bst.add_dir(x.get('name'), x.get('url'), 'bst_get_links', x.get('icon'), bst.addon_fanart, '', name2=f'{title} - {x.get("name")}', isFolder=False)

def runner(p: dict):
    name = p.get('name', '')
    name2 = p.get('name2', '')
    url = p.get('url', '')
    mode = p.get('mode')
    icon = p.get('icon', bst.addon_icon)
    page = p.get('page', '')
    if page: page = int(page)
    
    if mode == 'bst_new_shows':
        if url == '':
            url = new_shows
        bshows1(url)
    
    elif mode == 'bst_series':
        bshows_series(most_popular)
    
    elif mode == 'bst_episodes':
        bshows_episodes(name, url)
        
    elif mode == 'bst_get_links':
        bst.get_links(name2, url, icon)
        
    elif mode == 'bst_browse_shows':
        bshows_series(url)