# -*- coding: utf-8 -*-
# Author: Parrot Developers
# License: MPL 2.0 https://www.mozilla.org/en-US/MPL/2.0/

import sys
import os
import xbmcgui
import xbmcplugin
import xbmc
import xbmcaddon
import json as j
import requests
import hashlib
import datetime
import m3u
import xbmcvfs
import base64
from kodiez import KodiEZ
from routing import Plugin
from imgs import getIMG
from resources.utils.common import randString, getAllowed, getPISCTimeShift
try: from urllib.parse import urlencode, urlparse
except ImportError: from urllib import urlencode, urlparse
from ResolveURL import resolve
from ResolveURL.utils.browser import Firefox

plugin = Plugin()
_ADDON = xbmcaddon.Addon()
_URL = "plugin://{}".format(_ADDON.getAddonInfo('id'))
_KODIEZ = KodiEZ(_ADDON, plugin.handle)
_PLAYLIST = 'special://home/addons/'+_ADDON.getAddonInfo('id')+'/resources/playlist.m3u'
_USERDATA = 'special://home/userdata/addon_data/'+_ADDON.getAddonInfo('id')
_ADDON_DIR = "special://home/addons/"+_ADDON.getAddonInfo('id')
_ADDON_NAME = _ADDON.getAddonInfo('name')
groupsFile = xbmcvfs.translatePath(_USERDATA+"/groups.json")

colors = ["white", "black", "gradient"]
color = colors[int(_ADDON.getSetting("selectColor"))]

# Basic auth
if _ADDON.getAddonInfo('author') != "[COLOR cyan]Parrot[/COLOR] [COLOR yellow]Developers[/COLOR]": exit()
if _ADDON.getAddonInfo('id') != "plugin.video.parrottv": exit()

_CUSTOMPLAYLIST_DIR = os.path.join(xbmcvfs.translatePath(_USERDATA), "CustomPlaylist")
_CUSTOMPLAYLIST_FILE = os.path.join(_CUSTOMPLAYLIST_DIR, "list.json")
if not os.path.exists(_CUSTOMPLAYLIST_DIR): os.makedirs(_CUSTOMPLAYLIST_DIR)
if not os.path.exists(_CUSTOMPLAYLIST_FILE): open(_CUSTOMPLAYLIST_FILE, 'w', encoding="utf-8").write('{}')



def addDir(name, genre, icon, url, showPlot=True):
    list_item = xbmcgui.ListItem(label=name)
    if showPlot: plot = name
    list_item.setInfo('video', {'title': name,'genre': genre,'plot': plot,'mediatype': 'video'})
    list_item.setArt({'thumb': icon, 'icon': icon, 'fanart': 'https://cdn.wallpapersafari.com/14/97/Bir3IC.jpg'})
    xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, True)

def addChannel(name, icon, url, id, showAddToPlaylist=True, removeFromPlaylistID = ""):
    showAddToPlaylist = False # TODO: Remove when custom playlist will be fixed
    headers = Firefox().headers
    icon += '|' + urlencode(headers)
    list_item = xbmcgui.ListItem(label=name)
    list_item.setInfo('video', {'title': name,'genre': '','plot': name,'mediatype': 'video'})
    list_item.setArt({'thumb': icon, 'icon': icon, 'fanart': 'https://cdn.wallpapersafari.com/14/97/Bir3IC.jpg'})
    if "/play/" in url:
        parts = url.split("/")
        id = parts[4]
        list_item.setProperty('IsPlayable', 'true')
        contextMenuItems = []
        if showAddToPlaylist:
            args = "{}|{}|{}|{}".format(name, icon, url, id)
            args = base64.b64encode(args.encode("utf-8")).decode("utf-8")
            contextMenuItems.append(('Add to playlist', 'RunPlugin(plugin://plugin.video.parrottv/customAdd/{})'.format(args)))
        if removeFromPlaylistID != "":
            contextMenuItems.append(('Remove from playlist', 'RunPlugin(plugin://plugin.video.parrottv/customRemove/{})'.format(removeFromPlaylistID)))
        list_item.addContextMenuItems(contextMenuItems)
    xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, False)

    

@plugin.route('/')
def root():
    xbmcplugin.setContent(plugin.handle, 'Home')
    xbmcplugin.setPluginCategory(plugin.handle, "Home")
    addDir('[COLOR gold]Search[/COLOR]', '', getIMG('search', color), "{}/search".format(_URL), True)
    addDir('[COLOR gold]Channels[/COLOR]', '', getIMG('list', color), "{}/channels".format(_URL), True)
    addDir('[COLOR gold]Countries[/COLOR]', '', getIMG('grid', color), "{}/categories".format(_URL), True)
    #addDir('[COLOR gold]My Playlist[/COLOR]', '', getIMG('pencilWithWrench', color), "{}/custom".format(_URL), True)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/user')
def user():
    xbmcplugin.setContent(plugin.handle, 'User')
    xbmcplugin.setPluginCategory(plugin.handle, "User")
    addDir(f'[COLOR gold]Username: {getUsername()}[/COLOR]', '', getIMG('user', color), "{}/user".format(_URL), True)
    addDir(f'[COLOR gold]Password: {getPassword()}[/COLOR]', '', getIMG('user', color), "{}/user".format(_URL), True)
    addDir(f'[COLOR gold]Edit Username / Password[/COLOR]', '', getIMG('user', color), "{}/EnterCreds".format(_URL), True)
    addDir(f'[COLOR gold]Version: {_ADDON.getAddonInfo("version")}[/COLOR]', '', getIMG('user', color), "{}/user".format(_URL), True)
    addDir(f'[COLOR gold]Date: {datetime.datetime.now().strftime("%m/%d/%Y")}[/COLOR]', '', getIMG('user', color), "{}/user".format(_URL), True)
    addDir(f'[COLOR gold]Expire: Never[/COLOR]', '', getIMG('user', color), "{}/user".format(_URL), True)
    addDir(f'[COLOR gold]Setup IPTV Simple Client[/COLOR]', '', getIMG('user', color), "{}/ISS".format(_URL), True)
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/search')
def search():
    xbmcplugin.setContent(plugin.handle, 'Search')
    xbmcplugin.setPluginCategory(plugin.handle, "Search")
    query = _KODIEZ.inpt("Enter search query:", False)
    if query:
        names, logos, urls, groups, ids = m3u.parse("names,logos,urls,groups,ids")
        for name, logo, url, group, id in zip(names, logos, urls, groups, ids):
            if query.lower() in name.lower():
                addChannel(f"[COLOR gold]{group}: {name}[/COLOR]", logo, url, id)
        xbmcplugin.endOfDirectory(plugin.handle)
    else:
        xbmcgui.Dialog().ok(_ADDON_NAME, 'No search query entered.')
        exit()

@plugin.route('/channels')
def channels():
    xbmcplugin.setContent(plugin.handle, 'Channels')
    xbmcplugin.setPluginCategory(plugin.handle, "Channels")
    names, logos, urls, ids = m3u.parse("names,logos,urls,ids")
    try: epg = requests.get("https://EPGNow.parrotdevelopers.repl.co/guide.json", timeout=30).json()
    except: epg = {}
    for name, logo, url, id in zip(names, logos, urls, ids):
        name = f"[COLOR gold][B]{name}[/B][/COLOR]"
        if id in epg:
            name += f"\n[COLOR red]●[/COLOR] {epg[id]['title']}"
        
        addChannel(f"{name}", logo, url, id)
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/categories/')
def categories():
    xbmcplugin.setContent(plugin.handle, 'Countries')
    xbmcplugin.setPluginCategory(plugin.handle, "Countries")
    groups = m3u.parse("groups")
    # remove duplicates
    groups = list(set(groups))
    for group in groups:
        img = f"https://flagpedia.net/data/flags/w640/{group.lower() if group.lower() != 'uk' else 'gb'}.webp"
        addDir('[COLOR gold]{}[/COLOR]'.format(group), '', img, "{}/category/{}".format(_URL, group), True)
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/category/<category>')
def category(category):
    xbmcplugin.setContent(plugin.handle, 'Countries')
    xbmcplugin.setPluginCategory(plugin.handle, "Countries")
    names, logos, urls, groups, ids = m3u.parse("names,logos,urls,groups,ids")
    try: epg = requests.get("https://EPGNow.parrotdevelopers.repl.co/guide.json", timeout=30).json()
    except: epg = {}
    for name, logo, url, group, id in zip(names, logos, urls, groups, ids):
        if group != category:
            continue

        name = f"[COLOR gold][B]{name}[/B][/COLOR]"
        if id in epg:
            name += f"\n[COLOR red]●[/COLOR] {epg[id]['title']}"
            addChannel(f"{name}", logo, url, id)
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/play/<id>')
def play(id):
    # List sources
    channels = j.loads(open(os.path.join(xbmcvfs.translatePath(_USERDATA), "channels.json"), 'r', encoding='utf-8').read())
    names = []
    modules, chs = [], []
    for key, value in channels[id]["sources"].items():
        if not value["disabled"]:
            names.append(value["name"])
            modules.append(value["module"])
            chs.append(value["channel"])
    
    #names.append("Search programme in external sites")
    #modules.append("External")
    #chs.append(id)

    select = 0
    if len(names) == 0:
        xbmcgui.Dialog().ok("Error", "No available sources")
        return
    if len(names) > 1:
        select = xbmcgui.Dialog().select("Select source", names)
        if select == -1: exit()
    
    module, stream = modules[select], chs[select]

    # Play selected
    hlsurl, headers = "", {}

    os.makedirs(xbmcvfs.translatePath(_USERDATA + "/ResolveURL_data"), exist_ok=True)

    if not os.path.exists(xbmcvfs.translatePath("{}/LICENSE".format(_ADDON_DIR))) or hashlib.sha256(open(xbmcvfs.translatePath("{}/LICENSE".format(_ADDON_DIR)), "rb").read()).hexdigest() != "2684de17300e0a434686f1ec7f8af6045207a4b457a3fe04b2b9ce655e7c5d50":
        hlsurl, headers = "http://parrotlink.cf/Discovery.m3u8", {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"}
    else:
        if module == "123TV": module = "N123TV"
        rmf = resolve(
            module=module,
            channel=stream,
            data_folder=xbmcvfs.translatePath(_USERDATA + "/ResolveURL_data"),
            data_file=xbmcvfs.translatePath(_USERDATA + "/ResolveURL_data.json")
        )
        hlsurl, headers = rmf.url, rmf.headers
        
    li = xbmcgui.ListItem(path=hlsurl+'|'+urlencode(headers))
    li.setContentLookup(False)
    xbmcplugin.setResolvedUrl(plugin.handle, True, li)

"""
@plugin.route('/custom')
def custom():
    xbmcplugin.setContent(plugin.handle, 'My Playlist')
    xbmcplugin.setPluginCategory(plugin.handle, "My Playlist")
    customList = open(xbmcvfs.translatePath(_CUSTOMPLAYLIST_FILE), 'r', encoding='utf-8').read()
    if customList == "{}":
        xbmcgui.Dialog().ok(_ADDON_NAME, 'No channels added to playlist.')
        exit()
    customList = j.loads(customList)
    for item in customList:
        name = customList[item]["name"]
        logo = customList[item]["logo"]
        url = customList[item]["url"]
        id = customList[item]["id"]
        addChannel(f"[COLOR gold]{name}[/COLOR]", logo, url, id, showAddToPlaylist=False, removeFromPlaylistID=item)
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/customAdd/<args>')
def customAdd(args):
    args = base64.b64decode(args).decode("utf-8")
    args = args.split("|")
    customList = open(xbmcvfs.translatePath(_CUSTOMPLAYLIST_FILE), 'r', encoding='utf-8').read()
    customList = j.loads(customList)
    customList.update({randString(30): {"name": args[0], "logo":args[1], "url": args[2], "id": args[3]}})
    open(xbmcvfs.translatePath(_CUSTOMPLAYLIST_FILE), 'w', encoding='utf-8').write(j.dumps(customList))
    xbmcgui.Dialog().notification(_ADDON_NAME, "Channel added to playlist", xbmcgui.NOTIFICATION_INFO, 5000)
    xbmc.executebuiltin("Container.Refresh")

@plugin.route('/customRemove/<id>')
def customRemove(id):
    customList = open(xbmcvfs.translatePath(_CUSTOMPLAYLIST_FILE), 'r', encoding='utf-8').read()
    customList = j.loads(customList)
    del customList[id]
    open(xbmcvfs.translatePath(_CUSTOMPLAYLIST_FILE), 'w', encoding='utf-8').write(j.dumps(customList))
    xbmcgui.Dialog().notification(_ADDON_NAME, "Channel removed from playlist", xbmcgui.NOTIFICATION_INFO, 5000)
    xbmc.executebuiltin("Container.Refresh")
"""

@plugin.route('/ISS')
def iptvsimpleSetup():
    try:pisc = xbmcaddon.Addon('pvr.iptvsimple')
    except:
        xbmcgui.Dialog().notification(_ADDON_NAME, "IPTV Simple not found", xbmcgui.NOTIFICATION_INFO, 5000)
        return
    pisc.setSetting('m3uPathType','0')
    pisc.setSetting('m3uPath', xbmcvfs.translatePath(_PLAYLIST))
    pisc.setSetting('m3uRefreshMode','1')
    pisc.setSetting('m3uRefreshIntervalMins','30')
    pisc.setSetting('startNum','1')
    pisc.setSetting('epgUrl', 'https://falcon-epg.pages.dev/epg.xml.gz')
    pisc.setSetting('epgCache', 'false')
    pisc.setSetting('epgTimeShift', getPISCTimeShift())
    xbmcgui.Dialog().notification(_ADDON_NAME, "IPTV Simple setup completed", xbmcgui.NOTIFICATION_INFO, 5000)



@plugin.route('/Credits')
def credits():
    list = requests.get("https://images-ddg.pages.dev/list.json").json()
    text = "Created by:\n   Parrot Developers\nImages by:\n"
    credits = []
    for item in list: 
        if not list[item]['credits'].split(" - ")[0] in credits:
            credits.append(list[item]['credits'].split(" - ")[0])
    for credit in credits:
        text += "   {}\n".format(credit)
    xbmcgui.Dialog().textviewer("Credits", text)

if __name__ == "__main__":
                
    path = urlparse(sys.argv[0]).path
    logged = False
    if path in ["/", "/play", "/regenM3U"]:
                        
        if path in ["/", "/play"] : plugin.run(sys.argv)
        elif path == "/regenM3U" : genPlaylist()
                                      
        else: raise Exception("Error ID: 32")
        exit()
    if path == "/EnterCreds": EnterCreds(); exit()
    else: plugin.run(sys.argv)

        