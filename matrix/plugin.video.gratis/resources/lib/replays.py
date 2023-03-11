import xbmcplugin
import sys
import re
import datetime
from .plugin import Myaddon


class Replays(Myaddon):
    def __init__(self):
        self.base_url = 'https://fullmatchtv.com'
    
    def main_menu(self):
        xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Replays')
        for item in self.get_soup(self.base_url).find(class_='sf-menu').find_all('a')[:11]:
            if item.text not in ['Home', 'Other sports', 'All']:
                self.add_dir(item.text.replace('WWE & ', ''), item['href'], 'replays_cat', self.addon_icon, self.addon_fanart, f"{item.text.replace('WWE & ', '')} Replays")
        self.add_dir('Soccer', '', 'soccer_main', self.addon_icon, self.addon_fanart, 'Football Replays')
        self.add_dir('Archives by Date', '', 'replays_archives', self.addon_icon, self.addon_fanart, 'Replay Archives')
        self.add_dir('Search Replays', '', 'replays_search', self.addon_icon, self.addon_fanart, 'Search Replays')
    
    def sub_menu(self, name, url):
        xbmcplugin.setPluginCategory(int(sys.argv[1]), name)
        if name in ['NBA', 'NFL', 'NHL', 'MLB']:
            soup = self.get_soup(url).find_all(class_='td-image-container')
        else:
            soup = self.get_soup(url).find_all(class_='wpb_wrapper')
        for item in soup:
            for x in item.find_all('a', class_='td-image-wrap'):
                try:
                    icon =x.img['src'].split('?')[0]
                except TypeError:
                    icon = re.compile("url\('(.+?)\?resize").findall(str(x))[0]
                self.add_dir(x['title'], x['href'], 'replays_links', icon, icon, x['title'], isFolder=False)
    
    def get_replays_links(self, name, url, icon):
        xbmcplugin.setPluginCategory(int(sys.argv[1]), name)
        item_list = []
        for item in self.get_soup(url).find_all('iframe'):
            link = item['src']
            if link.startswith('//'):
                link = f'http:{link}'
            if not 'facebook' in link:
                domain = link.split('/')[2]
                item_list.append([domain, link])
        item_list = sorted(item_list, reverse=True)
        for domain, link in item_list:
            self.add_dir(domain, link, 'play_video2', icon, icon, name, name2=name, isFolder=False)
    
    def search_url(self, page: int = 1):
        return f'{self.base_url}/page/{page}/?s='

    def archives_main(self):
        for item in self.get_dates()[1:]:
            url = f'{self.search_url()}{item[1]}'
            self.add_dir(item[0], url, 'replays_date', self.addon_icon, self.addon_fanart, f'{item[1]} Replays')
    
    def by_date(self, url, icon):
        soup1 = self.get_soup(url).find_all(class_='td_module_16 td_module_wrap td-animation-stack')
        soup2 = self.get_soup(url.replace('.2022', '.22')).find_all(class_='td_module_16 td_module_wrap td-animation-stack')
        if len(soup1) > 0 or len(soup2) > 0:
            for item in soup1:
                self.add_dir(item.a['title'], item.a['href'], 'replays_links', icon, icon, item.a['title'])
            for item in soup2:
                self.add_dir(item.a['title'], item.a['href'], 'replays_links', icon, icon, item.a['title'])
            page = int(url.split('/')[4])
            query = url.split('?s=')[1]
            self.add_dir('Next Page', f'{self.search_url(page=page+1)}{query}', 'replays_date', self.addon_icon, self.addon_fanart, '')
        else:
            self.add_dir('[B][COLOR red]*****No Items to Display*****[/COLOR][/B]', '', 0, icon, self.addon_fanart, '', isFolder=False)
        
    def get_dates(self):
        dates = []
        d = datetime.date(2021,1,1)
        while d <= datetime.date.today():
            dates.append([datetime.datetime.strftime(d,'%A, %B %d, %Y'), datetime.datetime.strftime(d,'%d.%m.%Y')])
            d += datetime.timedelta(days=1)
        return list(reversed(dates))
    
    def search(self, url, icon):
        if url in [None, '']:
            query = self.from_keyboard()
            if query is None:
                return
            url = f"{self.search_url()}{query.replace(' ', '+')}"
        soup = self.get_soup(url).find_all(class_='td_module_16 td_module_wrap td-animation-stack')
        if len(soup) > 0:
            for item in soup:
                self.add_dir(item.a['title'], item.a['href'], 'replays_links', icon, icon, item.a['title'])
            page = int(url.split('/')[4])
            query = url.split('?s=')[1]
            self.add_dir('Next Page', f'{self.search_url(page=page+1)}{query}', 'replays_search', self.addon_icon, self.addon_fanart, 'Search Replays')
        else:
            self.add_dir('[B][COLOR red]*****No Items to Display*****[/COLOR][/B]', '', 0, icon, self.addon_fanart, '', isFolder=False)

replays = Replays()