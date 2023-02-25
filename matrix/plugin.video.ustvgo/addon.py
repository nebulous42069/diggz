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
import json
import random
import time

try:
    from urllib.parse import urlencode, quote_plus, quote, unquote
except ImportError:
    from urllib import urlencode, quote_plus, quote, unquote
    
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
params = dict(urllib.parse.parse_qsl(sys.argv[2][1:]))
addon = xbmcaddon.Addon(id='plugin.video.ustvgo')
file_name = addon.getSetting('fname')
path_m3u = addon.getSetting('path_m3u')

mode = addon.getSetting('mode')

def build_url(query):
    return base_url + '?' + urllib.parse.urlencode(query)

def add_item(ch_name, ch_site, ch_img, ch_epg):
    def epgInfo(x):
        prog_list=''
        def get_min(m):
            if m<=9:
                return '0'+str(m)
            else:
                return str(m)
        for p in x:
            t_start=time.localtime(p[0])
            t_end=time.localtime(p[1])
            prog_time=str(t_start.tm_hour)+'.'+get_min(t_start.tm_min)+'-'+str(t_end.tm_hour)+'.'+get_min(t_end.tm_min)
            prog_name=p[2]
            prog_list += prog_time+' '+ prog_name+'\n'
        return prog_list
    epg=epgInfo(ch_epg)
    li=xbmcgui.ListItem(ch_name)
    li.setProperty("IsPlayable", 'true')
    li.setInfo(type='video', infoLabels={'title': ch_name,'sorttitle': ch_name,'plot': epg})
    li.setArt({'icon':addon.getAddonInfo("path") + '/resources/icon.png'})
    li.setArt({'fanart':addon.getAddonInfo("path") + '/resources/fanart.jpg'})
    url_ch = build_url({'mode':'play','channel':ch_site})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url_ch, listitem=li, isFolder=False)

def channelArrayGen():
    resp = requests.get('https://ustvgo.tv')
    ch_html_1 = re.compile('<ol>(.*)</ol>').findall(resp.text)[0]
    arr_ch_html = ch_html_1.split('</li>')
    ar_chan=[]
    for c in arr_ch_html:
        c_data=re.compile('a href="(.*)">(.*)</a>').findall(c)
        if len(c_data)!=0:
            chName= c_data[0][1].replace('<strong>','').replace('</strong>','').replace('amp;','')
            if chName[len(chName)-1]==' ':
                chName=chName[:len(chName)-1]
            ar_chan.append([c_data[0][0],chName])
    
    #IMG
    categ=['entertainment','news','sports','kids']
    chan=[]
    for c in categ:
        resp=requests.get('https://ustvgo.tv/category/'+c+'/')
        resp_part=resp.text.split('<div class="featured-image">')
        for i,p in enumerate(resp_part):
            if i>0:
                link=re.compile('<a href="(.*)" title=').findall(p)[0]
                img=re.compile('data-lazy-src="(.*)" /><noscript>').findall(p)[0]
                chan.append([link,img])
    for a in ar_chan:
        for cc in chan:
            if a[0]==cc[0]:
                a.append(cc[1])
                break
        if len(a)==2:
            a.append('')
    #EPG
    tn=int(time.time())
    def get_epg(x):
        ar_epg=[]
        for i,prog in enumerate(x):
            if (prog['startTime']<=tn and prog['endTime']>=tn):
                for k in range (i,i+6):
                    pSt=x[k]['startTime']
                    pEnd=x[k]['endTime']
                    pName=x[k]['title']
                    ar_epg.append([pSt,pEnd,pName])
                break
        return ar_epg

    resp_epg=requests.get('https://ustvgo.tv/tvguide/national.json')
    epg_data=json.loads(resp_epg.text)
    for e in epg_data:
        for a in ar_chan:
            if (a[1]==e['channel']['name'] or a[1]==e['channel']['fullName']):
                a.append(get_epg(e['programSchedules']))
                break
    for d in ar_chan:
        if len(d)==3:
            d.append('')
    
    return ar_chan
    

def channels_gen():
    channels=channelArrayGen()
    for ch in channels:
        add_item(ch[1], ch[0], ch[2], ch[3])
    xbmcplugin.endOfDirectory(addon_handle)

def PlayStream(chUrl):
    resp=requests.get(chUrl)
    player_url_qry=re.compile('src=\'/player.php\?(.*)\'').findall(resp.text)[0]
    if len(player_url_qry)!=0:
        player_url='https://ustvgo.tv/player.php?'+ player_url_qry
        hdrs = {"Referer":"https://ustvgo.tv/"}
        resp_plr=requests.get(player_url,headers=hdrs)
        url_stream_ar=re.compile('hls_src=\'(.*)\';').findall(resp_plr.text)
        if len(url_stream_ar)!=0:
            url_stream=url_stream_ar[0]
            play_item = xbmcgui.ListItem(path=url_stream)
            xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
        else:
            xbmcgui.Dialog().notification('USTVGO', 'NEED A USA IP VPN', xbmcgui.NOTIFICATION_INFO)

            
def generate_m3u(c):
    if file_name == '' or path_m3u == '':
        xbmcgui.Dialog().notification('USTVGO', 'Set the file name and target directory.', xbmcgui.NOTIFICATION_ERROR)
        return
    xbmcgui.Dialog().notification('USTVGO', 'Generate list M3U.', xbmcgui.NOTIFICATION_INFO)
    data = '#EXTM3U\n'
    for item in c:
        channelId = item[0]
        channelName = item[1]
        data += '#EXTINF:0 tvg-id="%s" group-title="USTVGO",%s\nplugin://plugin.video.ustvgo?action=play&channel=%s\n' % (channelName,channelName,channelId)

    f = xbmcvfs.File(path_m3u + file_name, 'w')
    f.write(data)
    f.close()
    xbmcgui.Dialog().notification('USTVGO', 'M3U list has been generated .', xbmcgui.NOTIFICATION_INFO)

mode = params.get('mode', None)
action = params.get('action', '')

if action:
    if action=='play':
        channel_id = params.get('channel', '')
        PlayStream(channel_id)
        
    if action == 'BUILD_M3U':#
        ar_chan=channelArrayGen()   
        generate_m3u(ar_chan)#
    
else:

    if not mode:
        channels_gen()
        
    elif mode == 'play':
        channel_id = params.get('channel', '')
        PlayStream(channel_id)
        
    