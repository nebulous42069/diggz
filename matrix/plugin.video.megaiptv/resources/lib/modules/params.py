import sys
from urllib.parse import unquote_plus
from .utils import Log


class Params:
	
	def get_params(self):
		param=[]
		paramstring=sys.argv[2]
		if len(paramstring)>=2:
			params=sys.argv[2]
			cleanedparams=params.replace('?','')
			if (params[len(params)-1]=='/'):
				params=params[0:len(params)-2]
			pairsofparams=cleanedparams.split('&')
			param={}
			for i in range(len(pairsofparams)):
				splitparams={}
				splitparams=pairsofparams[i].split('=')
				if (len(splitparams))==2:
					param[splitparams[0]]=splitparams[1]
		return param
	
	def get_name(self):
		params=self.get_params()
		name = None
		try:
			name = unquote_plus(params["name"])
		except:
			pass
		return name
	
	def get_url(self):
		params=self.get_params()
		url = None
		try:
			url = unquote_plus(params["url"])
		except:
			pass
		return url
	
	def get_mode(self):
		params=self.get_params()
		mode = None
		try:        
			mode=int(params["mode"])
		except:
			pass
		return mode
	
	def get_icon(self):
		params=self.get_params()
		icon = None
		try:
			icon = unquote_plus(params["icon"])
		except:
			pass
		return icon
	
	def get_fanart(self):
		params=self.get_params()
		fanart = None
		try:
			fanart = unquote_plus(params["fanart"])
		except:
			pass
		return fanart
	
	def get_description(self):
		params=self.get_params()
		description = None
		try:
			description = unquote_plus(params["description"])
		except:
			pass
		return description

	def get_channeldata(self):
		params=self.get_params()
		channeldata=None
		try:
			channeldata=str(params["channeldata"])
		except:
			pass 
		return channeldata
p = Params()