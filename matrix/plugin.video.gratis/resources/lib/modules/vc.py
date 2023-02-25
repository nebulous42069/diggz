import xbmcgui
import xbmcplugin
import sys
import json
import re
import requests
from urllib.parse import quote_plus
from base64 import b64decode
from bs4 import BeautifulSoup as bs

class Myaddon:
	
	user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
	headers = {"User-Agent":user_agent, "Connection":'keep-alive', 'Accept':'audio/webm,audio/ogg,udio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5'}
	
	#---Request and Other Various Methods---#
	
	def get_page(self, page):
		return requests.get(page, headers=Myaddon.headers).text

	def get_json(self, page):
		return json.loads(self.get_page(page))
	
	def get_soup(self, url):
		return bs(self.get_page(url), 'html.parser')
	
	def write_to_file(self, _file, _string):
		with open(_file, "w") as text_file:
			text_file.write(_string)

	#---Add Directory Method---#

	def add_dir(self, name, url, mode, icon, fanart, description, page='', foldername='', addcontext=False, isFolder=True):
		u=sys.argv[0]+'?name='+quote_plus(name)+'&url='+quote_plus(url)+'&mode='+quote_plus(mode)+'&icon='+quote_plus(icon) +'&fanart='+quote_plus(fanart)+'&description='+quote_plus(description)+'&page='+str(page)+'&foldername='+quote_plus(foldername)
		liz=xbmcgui.ListItem(name)
		liz.setArt({'fanart': fanart, 'icon': icon, 'thumb': icon, 'poster': icon})
		liz.setInfo(type='video', infoLabels={'title': name, 'plot': description})
		if addcontext is True:
			contextMenu = []
			liz.addContextMenuItems(contextMenu)
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,listitem=liz, isFolder=isFolder)

class VC(Myaddon):
	
	def __init__(self):
		self.base_url = 'https://vidcloud9.com'
		self.movies_url = self.base_url + '/movies'
		self.featured_movies_url = self.base_url + '/cinema-movies'
		self.series_url = self.base_url + '/series'
		self.featured_series_url = self.base_url + '/recommended-series'
		self.search_url = self.base_url + '/search.html?keyword='

	def get_main(self, _url, content=None):
		soup = self.get_soup(_url)
		listings = soup.find(class_ = 'listing items')
		item_list = []
		for item in listings.find_all('a'):
			name = item.find(class_ = 'name').text.strip()
			url = self.base_url + item['href']
			icon = item.img['src']
			item_list.append({'name': name, 'url': url, 'icon': icon})
		if content is not None:
			pagination = soup.find(class_ = 'pagination')
			page = pagination.find_all('a')[-1]['href']
			next_page = content + page	
			item_list.append(next_page)
		return item_list
	
	def get_season(self, url):
		soup = self.get_soup(url)
		episodes = soup.find(class_='video-info-left')
		episodes = episodes.find_all(class_='video-block')
		item_list = []
		for episode in episodes:
			title = episode.find('img')['alt']
			link = self.base_url + episode.a['href']
			icon = episode.find('img')['src']
			item_list.append([title, link, icon])
		return item_list

	def get_links(self, _url):
		soup = self.get_soup(_url)
		description = soup.find(class_ = 'content-more-js').text.strip()
		if not description:
			description = ''
		embed = 'https:' + soup.find('iframe')['src']
		soup = self.get_soup(embed)
		links = soup.find_all(class_ = 'linkserver')
		item_list = []
		for link in links:
			x = link.text.lower()
			if 'dood' in x or 'mixdrop' in x or 'streamsb' in x:
				links2 = []
				links2.append(link.text)
				links2.append(link['data-video'].split('?')[0])
				if links2 not in item_list:
					item_list.append(links2)
		item_list.append(description)
		return item_list

class BST(Myaddon):
	
	def __init__(self):
		self.base_url = 'https://bstsrs.one'
		self.new_shows = self.base_url + '/new-shows'
		self.all_shows = self.base_url + '/browse-shows'
		self.most_popular = self.base_url + '/tv-shows/imdb_rating'
		self.api_key = b64decode('ZDQxZmQ5OTc4NDg2MzIxYjQ2NmUyOWJmZWMyMDM5MDI=').decode('utf-8')
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
			next_page = self.new_shows + '/' +str(current_page + 1)
		else:
			next_page = self.new_shows + '/2'
		item_list.append(next_page)
		return item_list

	def get_links(self, url):
		soup = self.get_soup(url)
		links_soup = soup.find_all(class_='embed-selector asg-hover odd')
		links = []
		for link in links_soup:
			link_coded = re.compile("dbneg\('(.+?)'\)").findall(str(link))[0]
			host = re.compile("domain=(.+?)'").findall(str(link))[0]
			url = self.get_url(link_coded)
			links.append({'name': host, 'url': url})
		return links

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
			next_page = self.most_popular + '/' +str(current_page + 1)
		else:
			next_page = self.most_popular + '/2'
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