# -*- coding: utf-8 -*-

from xbmc import Monitor
from resources.lib.proxy import Proxy

import xbmcaddon
addon = xbmcaddon.Addon('plugin.video.vix')
proxyport = addon.getSetting('proxyport')

class BackgroundService(Monitor):
    """ Background service code """

    def __init__(self):
        Monitor.__init__(self)

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

def run():
    """ Run the BackgroundService """
    BackgroundService().run()
