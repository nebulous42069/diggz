# -*- coding: utf-8 -*-
import os
import sys

import urllib
import requests
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs
import urllib3
import re
#import json
#import random
#import time
import html
from urllib.parse import urlencode, quote_plus, quote, unquote, parse_qsl
   
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
params = dict(parse_qsl(sys.argv[2][1:]))
addon = xbmcaddon.Addon(id='plugin.video.daddylive')

mode = addon.getSetting('mode')
baseurl='https://daddyhd.com/'
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
FANART = addon.getAddonInfo('fanart')
ICON = addon.getAddonInfo('icon')
def build_url(query):
    return base_url + '?' + urlencode(query)

def Main_Menu():
    menu=[
        ['LIVE SPORTS','sched'],
        ['LIVE TV','live_tv'],
    ]
    for m in menu:
        li=xbmcgui.ListItem(m[0])
        li.setProperty("IsPlayable", 'false')
        li.setInfo(type='video', infoLabels={'title': '','sorttitle': '','plot': ''})
        li.setArt({'thumb': '', 'poster': '', 'banner': '', 'icon': ICON, 'fanart': FANART})
        url_li = build_url({'mode':'menu','serv_type':m[1]})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url_li, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
    
def Menu_Trans():
    categs=getCategTrans()
    for c in categs:
        li=xbmcgui.ListItem(c)
        li.setProperty("IsPlayable", 'false')
        li.setInfo(type='video', infoLabels={'title': '','sorttitle': '','plot': ''})
        li.setArt({'thumb': '', 'poster': '', 'banner': '', 'icon': ICON, 'fanart': FANART})
        url_li = build_url({'mode':'trList','trType':c})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url_li, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
        
def getCategTrans():
    hea={
        'User-Agent':UA
    }
    resp=requests.get(baseurl,headers=hea).text

    blocks=resp.split('<h2 style')
    categs=[]
    for b in blocks:
        if 'background-color' in b:

            categ=re.compile('>([^<]+)<\/h2>').findall(b)
            
            
            if len(categ)==1:
                categs.append(categ[0])
    return categs

def getTransData(categ):
    hea={
        'User-Agent':UA
    }
    resp=requests.get(baseurl,headers=hea).text
    blocks=resp.split('<h2 style')
    trns=[]
    for b in blocks:#transmisje dla danej kategorii
        if 'background-color' in b and categ+'</h2>' in b: #    if 'noopener' in b and '<h4>' in b and categ+'</span></h4>' in b:

            ar_tr=([v for v in re.findall('(<hr>.*?\</span>)', b,re.DOTALL)])

            for a in ar_tr: #dane konkretnej transmisji
                if '<hr>' in a:
                    if ' | ' not in a:  #jedno źródło transmisji
                        ii=a.replace('\n','')
                        title=re.compile('<hr>(.*)<span style').findall(a)[0]
                        links=re.compile('href=\"(.*)" target').findall(a)
                        srcs=re.compile('\"noopener\">(.*)</a>').findall(a)
                        trns.append([title,links,srcs])
                    else:   #wiele źródeł transmisji
                        aa= a.split('</span> | <span')
                        title=re.compile('<hr>(.*)<span style').findall(aa[0])[0]
                        l=[]
                        s=[]
                        for aaa in aa:
                            links=re.compile('href=\"(.*)" target').findall(aaa)[0]
                            srcs=re.compile('\"noopener\">(.*)</a>').findall(aaa)[0]
                            l.append(links)
                            s.append(srcs)
                        trns.append([title,l,s])
            break
    addon.setSetting('trns',str(trns))
    return trns
    
def TransList(categ):
    trns=getTransData(categ)
    for t in trns:
        title=html.unescape(t[0])
        li=xbmcgui.ListItem(title)
        li.setInfo(type='video', infoLabels={'title': '','sorttitle': '','plot': ''})
        li.setArt({'thumb': '', 'poster': '', 'banner': '', 'icon': ICON, 'fanart': FANART})
        li.setProperty("IsPlayable", 'true')
        if len(t[1])==1:
            tr = t[1][0] 
            tr = 'https://daddyhd.com' + tr if tr.startswith('/') else tr
            url_stream = build_url({'mode':'play','url':tr})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url_stream, listitem=li, isFolder=False)
        else:
            url_li = build_url({'mode':'trLinks','trData':str(t)})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url_li, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)

def getSource(trData):
    data=eval(unquote(trData))
    select = xbmcgui.Dialog().select('Źródła', data[2])
    if select > -1:
        url_stream=data[1][select]
        url_stream = 'https://daddyhd.com' + url_stream if url_stream.startswith('/') else url_stream
        print(url_stream)
        xbmcplugin.setContent(addon_handle, 'videos')
        PlayStream(url_stream)
    else:
        quit()
    return
        
def list_gen():
    base_url=baseurl
    chData=channels()
    for c in chData:   
        li=xbmcgui.ListItem(c[1])
        li.setProperty("IsPlayable", 'true')
        li.setInfo(type='video', infoLabels={'title': c[1],'sorttitle': '','plot': ''})
        li.setArt({'thumb': '', 'poster': '', 'banner': '', 'icon': ICON, 'fanart': FANART})
        url_stream = build_url({'mode':'play','url':base_url+c[0]})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url_stream, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)

def channels():
    url=baseurl+'/24-7-channels.php'

    hea={
        'Referer':baseurl+'/',
        'user-agent':UA,
    }

    resp=requests.post(url, headers=hea).text
    ch_data=resp.split('<div class="grid-container">')
    #print(ch_data[-1])
    chan_data=re.compile('href=\"(.*)\" target(.*)<strong>(.*)</strong>').findall(resp)
    #print(chan_data)
    channels=[]
    for c in chan_data:
        channels.append([c[0],c[2]])
    return channels

def PlayStream(link):

    url=link
    
    hea={
        'Referer':baseurl+'/',
        'user-agent':UA,
    }
    
    resp=requests.post(url, headers=hea).text
    url_1=re.compile('iframe src="(.*)" width').findall(resp)[0]
    
    hea={
        'Referer':url,
        'user-agent':UA,
    }
    
    resp=requests.post(url_1, headers=hea).text
    stream=re.compile('source:\'(.*)\'').findall(resp)[-1]
    stream_url=stream
    hdr='Referer='+quote(str(url_1))+'&User-Agent='+UA
    play_item = xbmcgui.ListItem(path=stream+'|'+hdr)
    # xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
    
    import inputstreamhelper
    PROTOCOL = 'hls'
    is_helper = inputstreamhelper.Helper(PROTOCOL)
    if is_helper.check_inputstream():
        play_item = xbmcgui.ListItem(path=stream)
        play_item.setMimeType('application/x-mpegurl')
        play_item.setContentLookup(False)
        if sys.version_info >= (3,0,0):
            play_item.setProperty('inputstream', is_helper.inputstream_addon)
        else:
            play_item.setProperty('inputstreamaddon', is_helper.inputstream_addon)
        play_item.setProperty('inputstream.adaptive.stream_headers', hdr)        
        play_item.setProperty("IsPlayable", "true")
        play_item.setProperty('inputstream.adaptive.manifest_type', PROTOCOL)
    
        xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
   
    


mode = params.get('mode', None)

if not mode:
    Main_Menu()
else:
    if mode=='menu':
        servType=params.get('serv_type')
        if servType=='sched':
            Menu_Trans()
        if servType=='live_tv':
            list_gen()
    
    if mode=='trList':
        transType=params.get('trType')
        TransList(transType)
    
    if mode=='trLinks':
        trData=params.get('trData')
        getSource(trData)
        #todo -> dialog box z linkami do wyboru
    
    if mode=='play':
        link=params.get('url')
        PlayStream(link)
    
