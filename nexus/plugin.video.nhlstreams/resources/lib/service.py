# -*- coding: utf-8 -*-

from xbmc import Monitor, Player, getInfoLabel

from resources.lib.proxy import Proxy
import xbmc
import xbmcaddon
addon = xbmcaddon.Addon('plugin.video.nhlstreams')
proxyport = addon.getSetting('proxyport')

class BackgroundService(Monitor):
	""" Background service code """

	def __init__(self):
		Monitor.__init__(self)
		self._player = PlayerMonitor()
		self._proxy_thread = None

	def run(self):
		""" Background loop for maintenance tasks """

		addon.setSetting('proxyport', None)

		self._proxy_thread = Proxy.start()

		while not self.abortRequested():

			# Stop when abort requested
			if self.waitForAbort(10):
				break

		# Wait for the proxy thread to stop
		if self._proxy_thread and self._proxy_thread.is_alive():

			Proxy.stop()
			
class PlayerMonitor(Player):
	""" A custom Player object to check subtitles """

	def __init__(self):
		""" Initialises a custom Player object """
		self.__listen = False

		self.__path = None

		Player.__init__(self)

	def onPlayBackStarted(self):  
		""" Will be called when Kodi player starts """
		self.__path = getInfoLabel('Player.FilenameAndPath')
		if not self.__path.startswith('plugin://plugin.video.nhlstreams/'):
			self.__listen = False
			return
		xbmc.log('start odtwarzaniax', level=xbmc.LOGINFO)	
		self.__listen = True

	def onPlayBackEnded(self):  
		""" Will be called when [Kodi] stops playing a file """
		if not self.__listen:
			return
		xbmc.log('koniec odtwarzaniax', level=xbmc.LOGINFO)

		
	def onPlayBackStopped(self):  
		""" Will be called when [user] stops Kodi playing a file """
		if not self.__listen:
			return
		xbmc.log('koniec odtwarzaniax2', level=xbmc.LOGINFO)

def run():
	""" Run the BackgroundService """
	BackgroundService().run()
