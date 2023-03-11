import json
import sys
import xbmc
import xbmcgui
from resources.lib.modules.addonvar import addon_profile,customiser_json,fav_json
from .utils import Log


def HideCat(name):
	Log(name)
	catId = ''.join(name.lower().split())
	with open(customiser_json,'r+') as f:
		data = json.load(f)
		hidden_cats = data.get('hidden_category')
		if not catId in hidden_cats.keys():
			hidden_cats.update({catId:name})
			f.seek(0)
			json.dump(data,f,indent=4)
			f.truncate()
	xbmc.executebuiltin("Container.Refresh")


def HideChannel(channeldata):
	_data = json.loads(channeldata)
	chanId = _data.get('tvg_id')
	with open(customiser_json,'r+') as f:
		data = json.load(f)
		hidden_chan = data.get('hidden_channel')
		if not chanId in hidden_chan.keys():
			hidden_chan.update({chanId:_data.get('channel_name')})
			f.seek(0)
			json.dump(data,f,indent=4)
			f.truncate()
	xbmc.executebuiltin("Container.Refresh")


def AddFavChannel(channeldata):
	_data = json.loads(channeldata)
	chanId = _data.get('tvg_id')
	with open(fav_json,'r+') as f:
		data = json.load(f)
		fav_channels = data.get('channels')
		if not chanId in fav_channels.keys():
			fav_channels.update({chanId:_data})
			f.seek(0)
			json.dump(data,f,indent=4)
			f.truncate() 


def ReFavChannel(channeldata):
	_data = json.loads(channeldata)
	chanId = _data.get('tvg_id')
	with open(fav_json,'r+') as f:
		data = json.load(f)
		fav_channels = data.get('channels')
		fav_channels.pop(chanId)
		f.seek(0)
		json.dump(data,f,indent=4)
		f.truncate()
	xbmc.executebuiltin("Container.Refresh")
