# -*- coding: utf-8 -*-
import os
import sys

import requests
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs
import re
#import json
#import random
#import time
from urllib.parse import urlencode, quote_plus, quote, unquote, parse_qsl

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
params = dict(parse_qsl(sys.argv[2][1:]))
addon = xbmcaddon.Addon(id='plugin.video.dartstreams')
PATH=addon.getAddonInfo('path')

mode = addon.getSetting('mode')
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
baseurl='https://dartstreams.de.cool'

def build_url(query):
    return base_url + '?' + urlencode(query)

def main_menu():
    categs=[
        ['Livestreams','live'],
        ['VOD','vod'],
        ['Calendar Of Events','calendar']
    ]
    for c in categs:
        li=xbmcgui.ListItem(c[0])
        li.setProperty("IsPlayable", 'false')
        li.setInfo(type='video', infoLabels={'title': c[0],'sorttitle': c[0],'plot': ''})
        li.setArt({'icon':addon.getAddonInfo("path") + '/resources/icon.png'})
        li.setArt({'fanart':addon.getAddonInfo("path") + '/resources/fanart.jpg'})
        url = build_url({'mode':c[1],'page':'0'})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def streamList():
    hea={
        'user-agent':UA
    }
    url='https://dartstreams.de.cool/index.php'
    resp=requests.get(url,headers=hea).text

    x=re.compile('<ul class=\"dropdown-menu\">(.*)</ul>', re.DOTALL).findall(resp)[0]
    x1=x.split('</ul>')[0]
    x2=x1.split('\n')
    y=''
    test_del=0
    for xx in x2:
        if (test_del==0) and '<!--' not in xx and '-->' not in xx and xx!='':
            y+=xx
        if '<!--' in xx:
            test_del=1
        if '-->' in xx:
            test_del=0
    y1=y.split('</li>')
    streams=[]
    for yy in y1:
        if 'href' in yy:
            link=re.compile('href=\"([^"]+?)\"').findall(yy)[0]
            title=re.compile('span>([^<]+?)</a>').findall(yy)[0]
            title=title.replace('\t','')
            streams.append([title,link]) 
    for s in streams:
        if 'hlsplayer' not in s[1]:
            li=xbmcgui.ListItem(s[0])
            li.setProperty("IsPlayable", 'true')
            li.setInfo(type='video', infoLabels={'title': s[0],'sorttitle': s[0],'plot': ''})
            li.setArt({'icon':addon.getAddonInfo("path") + '/resources/icon.png'})
            li.setArt({'fanart':addon.getAddonInfo("path") + '/resources/fanart.jpg'})
            url = build_url({'mode':'playStream','link':s[1]})
            xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)


def playStream(link):
    hea={
    'user-agent':UA
    }
    resp=requests.get(link,headers=hea).text

    url_stream=re.compile('file\":.?\"(.*)\"').findall(resp)[0]
    #url_stream=url_stream+'|Referer='+baseurl+'&User-Agent='+UA
    play_item = xbmcgui.ListItem(path=url_stream)
    play_item.setProperty("IsPlayable", "true")
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
    
def calendar():
    hea={
        'user-agent':UA
    }
    url='https://dartstreams.de.cool/index.php'
    resp=requests.get(url,headers=hea).text
    resp=resp.split('Wrapper')[1].split('<footer')[0]
    line=resp.split('\n')
    date_title=[]
    img_desc=[]
    for l in line:
        if 'class=\"menu_punkt\"' in l:
            date_title.append(re.compile('>([^<]+?)<div class=\"title\".*>(.*)</div>').findall(l)[0])
        if 'class=\"imagebg\"' in l:
            x=re.compile('src=\"(.*)\"></div>([^\.]+?)\.').findall(l)
            if len(x)>0:
                img_desc.append(x[0])
            else:
                img_desc.append(('',''))
    
    for i in range(0,len(date_title)):
        title='[B]'+date_title[i][0]+'[/B]  '+date_title[i][1]
        img=img_desc[i][0]
        desc=img_desc[i][1]
        li=xbmcgui.ListItem(title)
        li.setProperty("IsPlayable", 'false')
        li.setInfo(type='video', infoLabels={'title': title,'sorttitle': title,'plot': desc})
        li.setArt({'thumb': img, 'poster': img, 'banner': img, 'icon': img, 'fanart': img})
        li.setArt({'fanart':addon.getAddonInfo("path") + '/resources/fanart.jpg'})
        url = build_url({'mode':'info'})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
    xbmcplugin.endOfDirectory(addon_handle)
    
def vodList(p):
    hea={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
    }
    url='https://dartstreams.de.cool/vod_append_new.php?page='+p+'&keyword=&competition='
    resp=requests.get(url,headers=hea).text

    title=re.compile('title\">(.*)</div').findall(resp)
    src=re.compile('src\', \'([^\']+?)\'').findall(resp)
    img=re.compile('src=\"([^"]+?)\"').findall(resp)
    date=re.compile('>([^<]+?)</span').findall(resp)
    vodData=[]
    for i in range(0,len(title)):
        vodData.append([title[i],date[i],img[i],src[i]])

    for v in vodData:
        title='[B]'+v[0]+'[/B]  '+v[1]
        img=baseurl+'/'+v[2]
        li=xbmcgui.ListItem(title)
        li.setProperty("IsPlayable", 'true')
        li.setInfo(type='video', infoLabels={'title': title,'sorttitle': title,'plot': ''})
        li.setArt({'thumb': img, 'poster': img, 'banner': img, 'icon': img, 'fanart': img})
        li.setArt({'fanart':addon.getAddonInfo("path") + '/resources/fanart.jpg'})
        url = build_url({'mode':'playVOD','link':v[3]})
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=False)
    
    next_page=str(int(p)+1)
    et='[I][COLOR orange]>>>Next Page[/COLOR][/I]'
    li=xbmcgui.ListItem(et)
    li.setProperty("IsPlayable", 'false')
    #li.setInfo(type='video', infoLabels={'title': '','sorttitle': '','plot': ''})
    li.setArt({'icon':addon.getAddonInfo("path") + '/resources/next.png'})
    li.setArt({'fanart':addon.getAddonInfo("path") + '/resources/fanart.jpg'})
    url = build_url({'mode':'vod','page':next_page})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

def playVOD(link):
    url_stream=link
    play_item = xbmcgui.ListItem(path=url_stream)
    play_item.setProperty("IsPlayable", "true")
    play_item.setContentLookup(False)
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

mode = params.get('mode', None)

if not mode:
    main_menu()
else:
    if mode=='live':
        streamList()
        
    if mode=='playStream':
        link=params.get('link')
        playStream(link)
    
    if mode=='calendar':
        calendar()
        
    if mode=='vod':
        p=params.get('page')
        vodList(p)
    
    if mode=='playVOD':
        link=params.get('link')
        playVOD(link)
    
    if mode=='info':
        xbmcgui.Dialog().notification('[B]INFO[/B]', 'View Events In The Tab [B]Livestream[/B]',xbmcgui.NOTIFICATION_INFO, 8000,False)
        xbmcplugin.endOfDirectory(addon_handle)