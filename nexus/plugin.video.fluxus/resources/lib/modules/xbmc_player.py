from resources.lib.modules.addonvar import recentplayed_json
from datetime import datetime
import json
import xbmc
import xbmcgui
from .utils import Log



class xbmcPlayer(xbmc.Player):

	playedlogged = False
	errorlogged  = False

	def __new__(cls,channeldata):
		return super(xbmcPlayer,cls).__new__(cls)

	def __init__(self,channeldata):
		super(xbmcPlayer,self).__init__()
		self.channeldata = json.loads(channeldata)
		self.PlayerListItem = self.CreateListItem()

	def onAVStarted(self):
		Log('onAVStarted')
		if self.isPlaying():
			Log('isPlaying')
			if not self.playedlogged:
				self.UpdateRecentPlayed()
				self.playedlogged = True

	def onPlayBackError(self):
		Log('onPlayBackError')
		if not self.errorlogged:
			self.UpdateRecentError()
			self.errorlogged = True

	def PlayStream(self):
		self.play(self.PlayerListItem.getPath(),self.PlayerListItem)
		while(not xbmc.Monitor().abortRequested()):
			xbmc.sleep(1000)

	def CreateListItem(self):
		title = self.channeldata.get('channel_name')
		iconimage = self.channeldata.get('tvg_logo')
		liz = xbmcgui.ListItem(title)
		liz.setPath(self.channeldata.get('stream_url'))
		liz.setInfo('video', {'Title': title})
		liz.setArt({'thumb': iconimage, 'icon': iconimage})
		return liz


	def UpdateRecentPlayed(self):
		with open(recentplayed_json,'r+') as f:
			data = json.load(f)
			recent = data.get('played')
			recentkeys = list(recent.keys())
			intrecentkeys = [int(x) for x in recentkeys]
			if len(recentkeys)==0:
				newkey = 1
			else:
				newkey = max(intrecentkeys)+1
			for k,v in list(recent.items()):
				for k1,v1 in list(v.items()):
					if k1 != 'timestamp' and v1.get('stream_url') == self.PlayerListItem.getPath():
						recent.pop(k)
			recent.update({newkey:{"timestamp":str(int(datetime.now().timestamp())),self.channeldata.get('tvg_id'):self.channeldata}})
			f.seek(0)
			json.dump(data,f,indent=4)
			f.truncate()


	def UpdateRecentError(self):
		pass