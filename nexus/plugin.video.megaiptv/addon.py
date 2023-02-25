import json, os, sys
import xbmc, xbmcgui, xbmcplugin, xbmcvfs
from resources.lib.modules.addonvar import addon_icon,addon_fanart,addon_name,data,addon_profile,resources,icon_search,icon_fav,icon_recent,icon_settings,search_json,local_string,dialog,fav_json,addon,recentplayed_json, customiser_json, m3udata_json
from resources.lib.modules.utils import addDir,Log,NewJsonFile,ParamsDict,Timestamp_Region_dt
from resources.lib.modules.params import p
from resources.lib.modules.m3u_parser import m3u,m3uRegex
from resources.lib.modules.http import UrlValidator
from resources.lib.modules.xml_parser import xmlRegex
from resources.lib.modules.search import SearchSelected,NewSearchQuery,SelSources
from uservar import host

Log(str(sys.argv))

xmlread         = xmlRegex(host)
m3usources      = xmlread.xmlSourcesRead()
iso_info        = json.load(open(os.path.join(data,'iso_3166-2.json')))

def MainMenu():
    for s in m3usources:
        url=s.get('url')
        if UrlValidator(url):
            statuslabel = '[COLOR green]Online[/COLOR]'
        else:
            statuslabel = '[COLOR red]Offline[/COLOR]'
        img = s.get('icon') if s.get('icon') else addon_icon
        addDir(s.get("name"),url,1,img, addon_fanart,statuslabel)
    addDir(local_string(32000),'',4,icon_search,addon_fanart,local_string(32004))
    addDir(local_string(32001),'',5,icon_fav,addon_fanart,local_string(32005))
    addDir(local_string(32002),'',6,icon_recent,addon_fanart,local_string(32006))
    addDir(local_string(32003),'',7,icon_settings,addon_fanart,local_string(32007),isFolder=False)


def CatMenu(source):
    m3uread = m3uRegex(source)
    m3udata = m3uread.EpgRegex()
    f=open(m3udata_json,'w')
    f.write(m3udata)
    f.close()
    m = m3u(m3udata)
    del m3udata
    for cat in m.get_categories():
        if len(cat)==2:
            for k,v in iso_info.items():
                if v.get('alpha2')==cat:
                    name = v.get('name')
                    break
                else:
                    name = cat
        else:
            name = cat
        hidden_cats = json.load(open(customiser_json)).get('hidden_category').keys()
        if not ''.join(name.lower().split()) in hidden_cats:  
            addDir(name,cat,2, addon_icon, addon_fanart, 'Categories',addcontext=['hide_cat'])


def ChannelMenu(cname):
    f=open(m3udata_json,'r')
    m3udata =  f.read()
    f.close()
    m = m3u(m3udata)
    for channel in m.get_catlist(cname):
        keyid = list(channel.keys())
        c = channel.get(keyid[0])
        hidden_chan = json.load(open(customiser_json)).get('hidden_channel').keys()
        if not c.get('tvg_id') in hidden_chan:
            addDir(c.get('channel_name','Unknown'), c.get('stream_url',''), 3, c.get('tvg_logo', addon_icon), addon_fanart, 'Channels',isFolder=False,channeldata=c,addcontext=['hide_chan','add_fav_chan'])

def SearchMenu():
    matches = []
    query = None
    with open(search_json,'r+') as f:
        data = json.load(f)
        searches = data.get('search_history')
        searches = dict(reversed(list(searches.items())))
        if len(searches)>0:
            items = [(xbmcgui.ListItem(local_string(32008)),None)]
            for k,v in searches.items():
                items.append((xbmcgui.ListItem(v.get('query')),v.get('matches')))
            ret = dialog.select(local_string(32009),[x[0] for x in items])
            if ret >=0:
                label = items[ret][0].getLabel()
                if label == local_string(32008):
                    #New search
                    nsq = NewSearchQuery()
                    if nsq:
                        ss = SelSources()
                        if ss:
                            matches,query = SearchSelected(nsq,ss)
                    else:
                        xbmc.executebuiltin('Action(Back)')
                elif label in [x[0].getLabel() for x in items]:
                    retu = dialog.yesnocustom(addon_name,local_string(32010),local_string(32025),local_string(32012),local_string(32011))
                    if retu == 1:
                        ss = SelSources()
                        if ss:
                            matches,query = SearchSelected(label,ss)
                        else:
                            xbmc.executebuiltin('Action(Back)')
                    elif retu == 0:
                        matches = items[ret][1]
                        query = items[ret][0].getLabel()
                    else:
                        xbmc.executebuiltin('Action(Back)')
            else:
                xbmc.executebuiltin('Action(Back)')
        else:
            nsq = NewSearchQuery()
            if nsq:
                ss = SelSources()
                if ss:
                    matches,query = SearchSelected(nsq,ss)
    if len(matches) >0:
        with open(customiser_json,'r') as _f:
            hidden_chan = json.load(_f).get('hidden_channel').keys()
            for c in matches:
                if not c.get('tvg_id') in hidden_chan:
                    addDir(c.get('channel_name','Unknown'), c.get('stream_url',''), 3, c.get('tvg_logo', addon_icon), addon_fanart, 'Channels',isFolder=False,addcontext=['hide_chan','add_fav_chan'],channeldata=c)
    elif query:
        ret = dialog.yesno(addon_name,local_string(32013).format(query=query))
        if ret:
            SearchMenu()
        else:
            xbmc.executebuiltin('Action(Back)') 
    else:
        return 

def myFavMenu(name):
    stream_url_fail = []
    refresh = False
    with open(fav_json,'r+') as f:
        data = json.load(f)
        channels = data.get('channels')
        categorys = data.get('categorys')
        if len(channels)>0 or len(categorys)>0:
            for k,v in list(channels.items()):
                stream_url = v.get('stream_url')
                stream_name = v.get('channel_name','Data missing')
                if addon.getSettingBool('general.smart') and addon.getSettingBool('general.smart.fav'):
                    if not UrlValidator(stream_url):
                        ret = dialog.yesnocustom(addon_name,local_string(32018).format(stream_name=stream_name),local_string(32019),local_string(32020),local_string(32021))
                        #return values to function Remove = 2, Replace = 0 ignore = 1
                        if ret == 0:
                            ss = SelSources()
                            if ss:
                                matches,query = SearchSelected(stream_name,ss)
                                items = []
                                for m in matches:
                                    li = xbmcgui.ListItem(m.get('channel_name'))
                                    li.setArt({'thumb':m.get('tvg_logo')})
                                    items.append((li,m))
                                retu = dialog.multiselect(local_string(32022),[x[0] for x in items])
                                if len(retu) >0:
                                    for i in retu:
                                        channels.update({items[i][1].get('tvg_id'):items[i][1]})
                                    f.seek(0)
                                    json.dump(data,f,indent=4)
                                    f.truncate()
                                    refresh = True
                        elif ret == 2:
                            chanId = v.get('tvg_id')
                            channels.pop(chanId)
                            f.seek(0)
                            json.dump(data,f,indent=4)
                            f.truncate()
                            refresh = True
                        else:
                            pass
                addDir(stream_name,stream_url,3,v.get('tvg_logo',addon_icon),addon_fanart,v.get('group_title'),isFolder=False,addcontext=['re_fav_chan'],channeldata=v)
            if refresh:
                xbmc.executebuiltin("Container.Refresh")
        else:
            dialog.notification(addon_name,local_string(32024).format(menu=name))
            xbmc.executebuiltin('Action(Back)') 


def RecentPlayedMenu(name):
    with open(recentplayed_json,'r') as f:
        data = json.load(f)
        played = data.get('played')
        if len(played)>0:
            for k,v in sorted(played.items(),reverse=True):
                for k1,v1 in v.items():
                    if k1 == 'timestamp':
                        dt = Timestamp_Region_dt(v1)
                    else:
                        c = v1
                addDir(f"{c.get('channel_name')} last played({dt})", c.get('stream_url',''), 3, c.get('tvg_logo', addon_icon), addon_fanart, 'Channels',isFolder=False,addcontext=['hide_chan','add_fav_chan'],channeldata=c)
        else:
            dialog.notification(addon_name,local_string(32024).format(menu=name))
            xbmc.executebuiltin('Action(Back)') 

def play_video(title, link, iconimage,channeldata):
    
    def __play__():
        from resources.lib.modules.xbmc_player import xbmcPlayer
        p = xbmcPlayer(channeldata)
        p.PlayStream()

    if addon.getSettingBool('general.smart') and addon.getSettingBool('general.smart.play'):
        if UrlValidator(link):
            __play__()
        else:
            dialog.notification(addon_name,local_string(32023))
    else:
        __play__()

def CacheClean():
    with open(recentplayed_json,'r+') as f:
        data = json.load(f)
        played = data.get('played')
        if played:
            playedk = [int(x) for x in played.keys()]
            keyids = sorted(playedk)
            csize = addon.getSettingInt('general.cache.played')
            if len(keyids) > csize:
                ktoremove = keyids[0:0-csize]
                for k in ktoremove:
                    played.pop(str(k))
        f.seek(0)
        json.dump(data,f,indent=4)
        f.truncate()
    with open(search_json,'r+') as f:
        data = json.load(f)
        search_history = data.get('search_history')
        if search_history:
            searchk = [int(x) for x in search_history.keys()]
            keyids = sorted(searchk)
            csize = addon.getSettingInt('general.cache.search')
            if len(keyids) > csize:
                ktoremove = keyids[0:0-csize]
                for k in ktoremove:
                    search_history.pop(k)
        f.seek(0)
        json.dump(data,f,indent=4)
        f.truncate()


def CheckRequiremets():
    with open(os.path.join(resources,'data','files.json'),'r') as _f:
        files = json.load(_f)
        filetypes = list(files.keys())
        for filetype in filetypes:
            data = files.get(filetype)
            if filetype == 'json_files':
                alljsfiles = data.get('user_data')+data.get('temp_data')
                for f in alljsfiles:
                    path = os.path.join(addon_profile,f.get('file'))
                    if not xbmcvfs.exists(path) and f.get('req_start'):
                        NewJsonFile(path,f.get('headers'))



Log(str(p.get_params()))
name = p.get_name()
url = p.get_url()
mode = p.get_mode()
icon = p.get_icon()
fanart = p.get_fanart()
description = p.get_description()
channeldata = p.get_channeldata()



if mode==None:
    CheckRequiremets()
    CacheClean()
    MainMenu()
if mode==1:
    CatMenu(url)
elif mode==2:
    ChannelMenu(url)
elif mode==3:
    play_video(name, url, icon,ParamsDict(channeldata))
elif mode==4:
    SearchMenu()
elif mode==5:
    myFavMenu(name)
elif mode==6:
    RecentPlayedMenu(name)
elif mode==7:
    addon.openSettings()
elif mode==100:
    from resources.lib.modules.context_menu import HideCat
    HideCat(name)
elif mode==101:
    from resources.lib.modules.context_menu import HideChannel
    HideChannel(channeldata)
elif mode==102:
    from resources.lib.modules.context_menu import AddFavChannel
    AddFavChannel(ParamsDict(channeldata))
elif mode==103:
    from resources.lib.modules.context_menu import ReFavChannel
    ReFavChannel(ParamsDict(channeldata))
xbmcplugin.endOfDirectory(int(sys.argv[1]))