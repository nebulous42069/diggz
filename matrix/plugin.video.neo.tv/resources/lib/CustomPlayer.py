# -*- coding: utf-8 -*-
from kodi_six import xbmc


class MyXBMCPlayer(xbmc.Player):
    def __init__(self, *args, **kwargs):
        self.is_active = True
        self.urlplayed = False
        self.pdialogue = None

    def onPlayBackStarted(self):
        if (self.pdialogue):
            self.pdialogue.close()
        self.urlplayed = True

    def onPlayBackEnded(self):
        self.is_active = False

    def onPlayBackStopped(self):
        self.is_active = False
