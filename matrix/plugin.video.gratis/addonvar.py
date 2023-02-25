import xbmc, xbmcvfs, xbmcaddon, xbmcgui
import os, sys

addon_id = xbmcaddon.Addon().getAddonInfo('id')
translatePath = xbmcvfs.translatePath
addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon = xbmcaddon.Addon(addon_id)
addoninfo = addon.getAddonInfo
addon_version = addoninfo('version')
addon_name = addoninfo('name')
addon_icon = addoninfo("icon")
addon_fanart = addoninfo("fanart")
addon_profile = translatePath(addoninfo('profile'))
addon_path = translatePath(addoninfo('path'))	
setting = addon.getSetting
setting_set = addon.setSetting
local_string = addon.getLocalizedString
home = translatePath('special://home/')
dialog = xbmcgui.Dialog()
dp = xbmcgui.DialogProgress()
addons_path = os.path.join(home, 'addons/')
user_path = os.path.join(home, 'userdata/')
data_path = os.path.join(user_path, 'addon_data/')
packages = os.path.join(addons_path, 'packages/')
resources = os.path.join(addon_path, 'resources/')
xml_folder = os.path.join(resources, 'xml/')
yt_xml = xml_folder + 'main.xml'###Host and replace with url if you wish
user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
headers = {'User-Agent': user_agent}