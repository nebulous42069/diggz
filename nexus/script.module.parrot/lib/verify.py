import requests
import xbmcaddon
import hashlib
import xbmcgui
import xbmc

authAddonID = "repository.test"
_ADDON_NAME = xbmcaddon.Addon(authAddonID).getAddonInfo('name')

def getUsername(): return xbmcaddon.Addon(authAddonID).getSetting("username")
def getPassword(): return xbmcaddon.Addon(authAddonID).getSetting("password")

def offlineMode(): exit()

def login():
    username = getUsername()
    password = getPassword()
    if username == "" or password == "":
        xbmcaddon.Addon(authAddonID).setSetting('verified', 'true')
        return True
    else:
        xbmcaddon.Addon(authAddonID).setSetting('verified', 'false')
        xbmcgui.Dialog().notification(_ADDON_NAME, "Login failed", xbmcgui.NOTIFICATION_INFO, 5000)
        xbmcaddon.Addon(authAddonID).openSettings()
        return False
