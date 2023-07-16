# -*- coding: utf-8 -*-
# KodiAddon
#
from resources.lib.scraper import myAddon
import re
import sys
import requests
import xbmc
import xbmcaddon
 
__settings__   = xbmcaddon.Addon('plugin.video.tubitv')
 
# Start of Module
addonName = re.search('plugin\://plugin.video.(.+?)/',str(sys.argv[0])).group(1)
ma = myAddon(addonName)
 
httpHeaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36',
               'Accept':"application/json, text/javascript, text/html,*/*",
               'Accept-Encoding':'gzip,deflate,sdch',
               'Accept-Language':'en-US,en;q=0.8'
               }
 
r = requests.get('https://tubitv.com/')
did=r.cookies.get('deviceId')
xbmc.log(msg=str(r.cookies), level=xbmc.LOGINFO)
httpHeaders.update({'Cookie':'deviceId='+did})
 
r = requests.post('https://tubitv.com/oz/auth/login/', headers=httpHeaders, json={"username":__settings__.getSetting("login_name"),"password":__settings__.getSetting("login_pass")})
sid=r.cookies.get('connect.sid')
 
ma.defaultHeaders.update({'Cookie':'deviceId='+did+'; connect.sid='+sid+';'})
ma.processAddonEvent()

