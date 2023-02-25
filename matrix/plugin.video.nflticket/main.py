# -*- coding: UTF-8 -*-
from __future__ import division
import sys,re,os
import six
from six.moves import urllib_parse

import json

import requests
from requests.compat import urlparse

import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmc, xbmcvfs
import xmltodict


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
params = dict(urllib_parse.parse_qsl(sys.argv[2][1:]))
addon = xbmcaddon.Addon(id='plugin.video.nflticket')

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

page = params.get('page',[1])#[0]

UA= 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
TIMEOUT=15

headers = {'User-Agent': UA,}
sess = requests.Session()

def build_url(query):
    return base_url + '?' + urllib_parse.urlencode(query)

def add_item(url, name, image, mode, itemcount=1, page=1,fanart=FANART, infoLabels=False,contextmenu=None,IsPlayable=False, folder=False):
    list_item = xbmcgui.ListItem(label=name)
    if IsPlayable:
        list_item.setProperty("IsPlayable", 'True')    
    if not infoLabels:
        infoLabels={'title': name}    
    list_item.setInfo(type="video", infoLabels=infoLabels)    
    list_item.setArt({'thumb': image, 'poster': image, 'banner': image, 'fanart': fanart})
    
    if contextmenu:
        out=contextmenu
        list_item.addContextMenuItems(out, replaceItems=True)
   # else:
   #     out = []
   #     out.append(('Informacja', 'XBMC.Action(Info)'),)
   #     list_item.addContextMenuItems(out, replaceItems=False)

    xbmcplugin.addDirectoryItem(
        handle=addon_handle,
        url = build_url({'mode': mode, 'url' : url, 'page' : page, 'title':name,'image':image}),            
        listitem=list_item,
        isFolder=folder)
    xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_NONE, label2Mask = "%R, %Y, %P")
       
def home():
	logged, games = login()
	if logged:
		createGames(games)
	else:
		add_item('', 'Login', ikona, "login",fanart=FANART, folder=True)
		add_item('', 'Settings', ikona, "settings",fanart=FANART, folder=False, IsPlayable=False)

def createGames(items):
	for game in items:
		gameId = game.get('gameId', None)
		homeTeamName = game.get('homeTeamName', None)
		awayTeamName = game.get('awayTeamName', None)
		if homeTeamName == awayTeamName:
			title = homeTeamName
			kickOffTime = ''
		else:
			homeTeamCode = game.get('homeTeamCode', None)
			awayTeamCode = game.get('awayTeamCode', None)
			kickOffTime = game.get('kickOffTime', None)
			title = '%s(%s) - (%s)%s'%(str(homeTeamName),str(homeTeamCode), str(awayTeamCode), str(awayTeamName))
		if game.get('sundayTicket',None):

			add_item(str(gameId), title, ikona, "playgame",fanart=FANART, infoLabels={"title": title,'plot':title, 'code':kickOffTime}, folder=False, IsPlayable=True)
	xbmcplugin.setContent(addon_handle, 'videos')
	if items:
		xbmcplugin.endOfDirectory(addon_handle) 
		
def PlayGame(gameid):
	
	sessionId = get_setting('sessionId')	
	devid = get_setting('devid')	
	kuks = get_setting('kuks')	
	cooks = dict(urllib_parse.parse_qsl(kuks))
	headersx = {
		'X-NewRelic-ID': 'VgYDV15UARABU1FbAgEPVF0=',
		'session': sessionId,
		'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; KODI Build/PPR1.180610.011)',
		'Host': 'nfl.directv.com',
	}
	
	params = {
		'gameId': gameid,
		'streamtype': '30m',
		'device': devid,
		'platform': 'android',
		'quality': 'hi',
	}

	response = sess.get('https://nfl.directv.com/supercast/service/GameIdURLService', params=params, cookies=cooks, headers=headersx, verify=False)
	abc = xmltodict.parse(response.text)
	try:
		url = urllib_parse.unquote(abc.get('GameIdURL', None).get('url', None))
		UAX = 'NFL Sunday Ticket/2.12.005 (Linux;Android 9) ExoPlayerLib/2.13.2'
		stream_url = url+'|User-Agent='+urllib_parse.quote(UAX)+'&Cookie='+urllib_parse.quote(kuks)
		play_item = xbmcgui.ListItem(path=stream_url)
		play_item.setMimeType('application/x-mpegurl')
		play_item.setContentLookup(False)	
		xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
	except exception as exc:
		xbmcgui.Dialog().notification('[COLOR green][B]Error[/B][/COLOR]', "[COLOR green][B]%s[/B][/COLOR]"%str(exc), xbmcgui.NOTIFICATION_INFO, 5000,False)

	
def get_setting(setting_id):
    setting = addon.getSetting(setting_id)
    if setting == 'true':
        return True
    elif setting == 'false':
        return False
    else:
        return setting

def set_setting(key, value):
    return addon.setSetting(key, value)
	
def open_settings():
	addon.openSettings()
	
def login():

	devid = get_setting('devid')	

	if not devid:
		import random

		def gen_hex_code(myrange=6, start=0):
			if not start:
				a = ''.join([random.choice('0123456789abcdef') for x in range(myrange)])
			else:
				a = str(start)+''.join([random.choice('0123456789abcdef') for x in range(myrange-1)])
			return a
		
		def uid():
			a = gen_hex_code(16,0)
			return a
		dev_id = uid()
		set_setting('devid',dev_id)

	username = get_setting('username')	
	password = get_setting('password')	
	logg = False
	games ={}
	if username and password:
		headersx = {
			'X-NewRelic-ID': 'VgYDV15UARABU1FbAgEPVF0=',
			'X-UserAgent': 'kodi;KODI;9',
			'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; KODI Build/PPR1.180610.011)',
			'Host': 'nfl.directv.com',
		}
		
		data = {
			'p': password,
			'site': 'NFL_Supercast_Android_Cust01',
			'u': username,
			'session': '',
			'device': devid,
			'bo': 'true',
			'nonce': 'true',
		}
		response = sess.post('https://nfl.directv.com/supercast/service/AuthenticationManager', headers=headersx, data=data, verify=False)
		data_dict = xmltodict.parse(response.text)

		main = data_dict.get('UserGameAuthInfo', None)
		mainx = main.get('status', None)

		if mainx!='failure':
			sessionId = main.get('sessionId', None)
			set_setting('sessionId',str(sessionId))

			logg = True
			games = main.get("games",None).get('GameAuthInfo', None)
			kuks =''.join(['%s=%s;'%(c.name, c.value) for c in sess.cookies])
			set_setting('kuks',str(kuks))
		else:
			logg = False
			games = {}
			set_setting('kuks','')
			mess = main.get('statusMessage', None)
			xbmcgui.Dialog().notification('[COLOR green][B]Warning[/B][/COLOR]', "[COLOR green][B]%s[/B][/COLOR]"%str(mess), xbmcgui.NOTIFICATION_INFO, 5000,False)

	else:	
		xbmcgui.Dialog().notification('[COLOR green][B]Warning[/B][/COLOR]', "[COLOR green][B]No Username Or Password[/B][/COLOR]", xbmcgui.NOTIFICATION_INFO, 5000,False)

	return logg, games

def router(paramstring):
	params = dict(urllib_parse.parse_qsl(paramstring))
	if params:    
	
		mode = params.get('mode', None)
	
		if mode == 'login':
			home()
		
		elif mode == 'playgame':
			PlayGame(exlink)
			
		elif mode == 'settings':
			open_settings()	
			xbmc.executebuiltin("Container.Refresh") 

	else:
		home()
		xbmcplugin.endOfDirectory(addon_handle)    
if __name__ == '__main__':
    router(sys.argv[2][1:])