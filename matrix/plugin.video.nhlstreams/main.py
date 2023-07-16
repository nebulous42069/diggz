# -*- coding: UTF-8 -*-

import sys,re, ast 
import six
from six.moves import urllib_parse

import requests
from requests.compat import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmc, xbmcvfs

import calendar
from datetime import datetime, timedelta
import time

import iso8601


if six.PY3:
    basestring = str
    unicode = str
    xrange = range

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
params = dict(urllib_parse.parse_qsl(sys.argv[2][1:]))
addon = xbmcaddon.Addon(id='plugin.video.nhlstreams')

PATH            = addon.getAddonInfo('path')
if six.PY2:
    DATAPATH        = xbmc.translatePath(addon.getAddonInfo('profile')).decode('utf-8')
else:
    DATAPATH        = xbmcvfs.translatePath(addon.getAddonInfo('profile'))

RESOURCES       = PATH+'/resources/'
FANART=RESOURCES+'../fanart.jpg'
ikona =RESOURCES+'../icon.png'

exlink = params.get('url', None)
nazwa= params.get('title', None)
rys = params.get('image', None)
proxyport = addon.getSetting('proxyport')
try:
    inflabel = ast.literal_eval(params.get('ilabel', None))
except:
    inflabel = params.get('ilabel', None)
    
page = params.get('page',[1])[0]

UA= 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
TIMEOUT=15


sess = requests.Session()

    
    
def build_url(query):
    return base_url + '?' + urllib_parse.urlencode(query)

def add_item(url, name, image, mode, itemcount=1, page=1,fanart=FANART, infoLabels=False,contextmenu=None,IsPlayable=False, folder=False):

    if six.PY3:    
        list_item = xbmcgui.ListItem(name)

    else:
        list_item = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
    if IsPlayable:
        list_item.setProperty("IsPlayable", 'True')    
        
    if not infoLabels:
        infoLabels={'title': name}    
    list_item.setInfo(type="video", infoLabels=infoLabels)    
    list_item.setArt({'thumb': image,'icon': image,  'poster': image, 'banner': image, 'fanart': fanart})
    
    if contextmenu:
        out=contextmenu
        list_item.addContextMenuItems(out, replaceItems=True)
    else:
        out = []
        out.append(('Informacja', 'Action(Info)'),)
        list_item.addContextMenuItems(out, replaceItems=False)

    xbmcplugin.addDirectoryItem(
        handle=addon_handle,
        url = build_url({'mode': mode, 'url' : url, 'page' : page, 'title':name,'image':image, 'ilabel':infoLabels}),            
        listitem=list_item,
        isFolder=folder)
    xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_NONE, label2Mask = "%R, %Y, %P")
    
def resp_text(resp):
    """Return decoded response text."""
    if resp and resp.headers.get('content-encoding') == 'br':
        out = []
        # terrible implementation but it's pure Python
        return brotlidec(resp.content, out).decode('utf-8')
    response_content = resp.text

    return response_content.replace("\'",'"')
    
    
def request_sess(url, method='get', data={}, headers={}, result=True, json=False, allow=True , json_data = False):
    if method == 'get':
        resp = sess.get(url, headers=headers, timeout=15, verify=False, allow_redirects=allow)
        
    elif method == 'post':
        if json_data:
            resp = sess.post(url, headers=headers, json=data, timeout=15, verify=False, allow_redirects=allow)
        else:
            resp = sess.post(url, headers=headers, data=data, timeout=15, verify=False, allow_redirects=allow)

    if result:
        return resp.json() if json else resp_text(resp)
    else:
        return resp
        
def home():
    add_item('', '[COLOR blue]NHL Schedule[/COLOR]', ikona, "nhlsched", folder=True, IsPlayable=False)

def NHLschedule():
    headers = {
        'Host': 'api.nhl66.ir',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
        'Origin': 'https://nhl66.ir',
        'DNT': '1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
    }
    
    response = requests.get('https://api.nhl66.ir/api/sport/schedule', headers=headers)
    games = response.json().get('games', None)

    for gam in games:

        src_id = gam.get('src_id', None)
        home_name = gam.get('home_name', None)
        away_name = gam.get('away_name', None)
        home_abr = gam.get('home_abr', None)
        away_abr = gam.get('away_abr', None)

        home_score = str(gam.get('home_score', None))
        away_score = str(gam.get('away_score', None))
        start_time_obj = parse_datetime(gam.get('start_datetime',None), localize=True)
        start_time = start_time_obj.strftime('%d-%m %H:%M')
       # xbmc.log('start_timestart_timestart_time: %s'%str(start_time), level=xbmc.LOGINFO)
        tit = home_name + ' ('+home_abr+') [B][COLOR blue]'+home_score+ ':'+away_score+'[/COLOR][/B] '+ away_name+' ('+away_abr+')'
        fold = True
        isplay = False
        if gam.get('status', None) == 'Pre Game':
            tit = '[I][COLOR white]'+home_name + ' ('+home_abr+') : ('+away_abr+') '+ away_name+'[/COLOR][/I]'
            fold = True
            isplay = False
            tit = tit+' [B][COLOR khaki]'+start_time+'[/COLOR][/B]'
        else:
			
            tit = tit+' [B][I][COLOR blue]'+start_time+'[/COLOR][/B][/I]'
        streams = urllib_parse.quote_plus(str(gam.get('streams', None)))
        href = src_id+'|'+streams

        add_item(href,tit, ikona, "listNHL",fanart=FANART, folder=fold, IsPlayable=isplay)
        
    xbmcplugin.endOfDirectory(addon_handle)
    
def ListNHL(idstreams):
    id,streams = idstreams.split('|')
    streams = ast.literal_eval(urllib_parse.unquote_plus(streams))
    for stream in streams:
        name = stream.get('name', None)
        url = stream.get('url', None)
        t = nazwa + '  [B]('+name+')[/B]'
        add_item(url, t, ikona, "playNHL1",fanart=FANART, folder=False, IsPlayable=True)

    import requests
    
    headers = {
        'Host': 'statsapi.web.nhl.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
        'Origin': 'https://nhl66.ir',
        'DNT': '1',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
    }

    response = requests.get('https://statsapi.web.nhl.com/api/v1/game/'+id+'/content', headers=headers)
    recaps = response.json().get('editorial',None).get('recap',None).get("items", None)
    medias = response.json().get("media" ,None).get("epg", None)
    ite = []
    for epg in medias:
        items = epg.get ('items', None)

        try:
            ite.extend([v for v in epg.get ('items', None) if v.get('type',None)=='video'])    
        except:
            
            vbvbv=''
    highlights = response.json().get("highlights" ,None)
    hih =[]

    for a,b in highlights.items():
        hih.extend([v for v in b.get('items', None) if v.get('type',None)=='video'])    
        break
    a = len(hih)
    a2 = len(highlights)

    if ite or hih:
        add_item('empty', '[B][COLOR gold]#############[/COLOR][/B]', rys, "empty",fanart=FANART, folder=False, IsPlayable=False)
        add_item('empty', '[B][COLOR gold]--> Replays <--[/COLOR][/B]', rys, "empty",fanart=FANART, folder=False, IsPlayable=False)
        add_item('empty', '[B][COLOR gold]#############[/COLOR][/B]', rys, "empty",fanart=FANART, folder=False, IsPlayable=False)
        for i in ite:
            t = i.get('title', None)
            plot = i.get('description', None)
            images = i.get('image', None).get('cuts', None)
            mediaURLS = urllib_parse.quote_plus(str(i.get('playbacks', None)))
            img =''
            for k, v in images.items():
                img = v.get('src', None)
                img = 'https://cms.nhl.bamgrid.com/images/photos/'+img if  not img.startswith('htt') else img
                break
            add_item(mediaURLS, '[B]'+t+'[/B]', img, "playNHL2",fanart=FANART, infoLabels={'plot':plot, 'title': t},folder=False, IsPlayable=True)
        for i in hih:
            t = i.get('title', None)
            plot = i.get('description', None)
            images = i.get('image', None).get('cuts', None)
            mediaURLS = urllib_parse.quote_plus(str(i.get('playbacks', None)))
            img =''
            for k, v in images.items():
                img = v.get('src', None)
                img = 'https://cms.nhl.bamgrid.com/images/photos/'+img if  not img.startswith('htt') else img
                break
            add_item(mediaURLS, '[B]'+t+'[/B]', img, "playNHL2",fanart=FANART, infoLabels={'plot':plot, 'title': t},folder=False, IsPlayable=True)

    if streams or ite or hih:
        xbmcplugin.endOfDirectory(addon_handle)
            

def PlayNHL1(stream_url):
    if stream_url:
        stream_url = 'http://127.0.0.1:{port}/NHL='.format(port=proxyport)+stream_url    
        PlayVid(stream_url)

def PlayNHL2(streams):
    zz=''
    streams = ast.literal_eval(urllib_parse.unquote_plus(streams))

    stream_url=([v.get('url', None) for v in streams if v.get('name',None)=='HTTP_CLOUD_WIRED_WEB']) #'name': 'HTTP_CLOUD_WIRED_WEB'
    if stream_url:
        stream_url = stream_url[0]
        PlayVid(stream_url)

        
def PlayVid(stream_url):
    import inputstreamhelper
    
    is_helper = inputstreamhelper.Helper('hls')
    if is_helper.check_inputstream():
        play_item = xbmcgui.ListItem(path=stream_url)
        play_item.setProperty("IsPlayable", "true")
        play_item.setProperty('inputstream', is_helper.inputstream_addon)
    
        play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
        play_item.setMimeType('application/vnd.apple.mpegurl')
        play_item.setContentLookup(False)
        xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
		
		
def parse_datetime(iso8601_string, localize=False):
    """Parse ISO8601 string to datetime object."""
	
    datetime_obj = iso8601.parse_date(iso8601_string)
    if localize:
        return utc_to_local(datetime_obj)
    else:
        return datetime_obj

def to_timestamp(a_date):
    if a_date.tzinfo:
        epoch = datetime(1970, 1, 1, tzinfo=pytz.UTC)
        diff = a_date.astimezone(pytz.UTC) - epoch
    else:
        epoch = datetime(1970, 1, 1)
        diff = a_date - epoch
    return int(diff.total_seconds())*1000

def utc_to_local(utc_dt):
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)
def router(paramstring):
    params = dict(urllib_parse.parse_qsl(paramstring))
    if params:    
        mode = params.get('mode', None)

        if mode == 'nhlsched':
            NHLschedule()
            
        elif mode == 'listNHL':
            ListNHL(exlink)

        elif mode == 'playNHL1':
            PlayNHL1(exlink)
        elif mode == 'playNHL2':
            PlayNHL2(exlink)

    else:
    
        home()
        xbmcplugin.endOfDirectory(addon_handle)    
if __name__ == '__main__':
    router(sys.argv[2][1:])