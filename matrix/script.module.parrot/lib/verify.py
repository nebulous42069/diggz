import requests
import xbmcaddon
import hashlib
import xbmcgui
import xbmc

authAddonID = "repository.Parrot"
_ADDON_NAME = xbmcaddon.Addon(authAddonID).getAddonInfo('name')

def getUsername(): return xbmcaddon.Addon(authAddonID).getSetting("username")
def getPassword(): return xbmcaddon.Addon(authAddonID).getSetting("password")

def offlineMode(): exit()

def login():
    username = getUsername()
    password = getPassword()
    if username == "" or password == "":
        xbmcaddon.Addon(authAddonID).setSetting('verified', 'false')
        xbmcgui.Dialog().notification(_ADDON_NAME, "Login failed", xbmcgui.NOTIFICATION_INFO, 5000)
        xbmcaddon.Addon(authAddonID).openSettings()
        return False
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'username': username,
        'password': "hash::::" + hashlib.sha256(password.encode()).hexdigest(),
    }
    try:
        jsonResp = requests.get('http://parrot.getenjoyment.net/login.php', headers=headers).json()
    except Exception as e:
        xbmcgui.Dialog().ok(_ADDON_NAME, "Login Failed due to server error, please try again later")
        return False

    if jsonResp['status'] == 'ok':
        xbmcaddon.Addon(authAddonID).setSetting('verified', 'true')
        return True
    else:
        xbmcaddon.Addon(authAddonID).setSetting('verified', 'false')
        xbmcgui.Dialog().notification(_ADDON_NAME, "Login failed", xbmcgui.NOTIFICATION_INFO, 5000)
        xbmcaddon.Addon(authAddonID).openSettings()
        return False
