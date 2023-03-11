import os
import xml.etree.ElementTree as ET
from requests import Session
from resources.lib.modules.addonvar import addon_path,addon_profile


class xmlRegex(object):

	def __init__(self,path):
		self.path = path
		self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
		self.headers = {"User-Agent":self.user_agent, "Connection":'keep-alive', 'Accept':'audio/webm,audio/ogg,udio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5'}
		self.session = Session()
		self.session.headers.update(self.headers)


	def xmlSourcesRead(self):
		s = []
		if self.path.startswith('http'):
			sources = ET.fromstring(self.session.get(self.path).content)
		elif self.path =='local':
			tree = ET.parse(os.path.join(addon_path,'sources.xml'))
			sources = tree.getroot()
		for source in sources.findall('source'):
			m3upath = source.find('url').text
			m3uname = source.find('name').text
			m3uicon = source.find('icon').text
			s.append({'url':m3upath,'name':m3uname,'icon':m3uicon})
		return s

