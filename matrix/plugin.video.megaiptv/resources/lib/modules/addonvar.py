
import uservar
import xbmcaddon
from xbmcvfs import translatePath
from xbmcgui import Dialog,DialogProgress
from os.path import join as osjoin

addon             = xbmcaddon.Addon(uservar.pluginid)
addoninfo         = addon.getAddonInfo
addon_id          = addoninfo('id')
addon_version     = addoninfo('version')
addon_name        = addoninfo('name')
addon_icon        = addoninfo("icon")
addon_fanart      = addoninfo("fanart")
addon_profile     = translatePath(addoninfo('profile'))
addon_path        = translatePath(addoninfo('path'))	
local_string      = addon.getLocalizedString
dialog            = Dialog()
dp                = DialogProgress()
resources         = osjoin(addon_path, 'resources/')
data              = osjoin(resources,'data')
icons             = osjoin(resources,'icons')
search_json       = osjoin(addon_profile,'search.json')
customiser_json   = osjoin(addon_profile,'customiser.json')
fav_json          = osjoin(addon_profile,'user_fav.json')
m3udata_json      = osjoin(addon_profile,'m3udata.json')
recentplayed_json = osjoin(addon_profile,'recent_played.json')
icon_search       = osjoin(icons,'search.png')
icon_fav          = osjoin(icons,'favorites.png')
icon_recent       = osjoin(icons,'recent.png')
icon_settings     = osjoin(icons,'settings.png')


iso_country_codes = 'http://geohack.net/gis/wikipedia-iso-country-codes.csv'