import xbmc
import xbmcaddon
import xbmcvfs
import json
import ast
import re
import os
import urllib.parse as urllib
from html.parser import unescape
import util
import resolveurl as urlresolver

supports=["youtube", "openload", "movpod", "zstream", "yourupload", "xvidstage", "faststream", "weshare", "watchvideo", "watchonline", "watchers", "vshare", "vodlock", "vimeo", "vidzi", "vidwatch", "vidup", "vidtodo", "vidstreaming", "vidoza", "vid.me", "vidmad", "tamildrive", "vidlox", "vidics", "vidhos", "byzoo", "playpanda", "videozoo", "videowing", "easyvideo", "play44", "playbb", "video44", "videowood", "bitvid", "videoweed", "videoraj", "videohut", "videoget", "videocloud", "thevideobee", "vidabc", "veehd", "ustream", "usersfiles", "userscloud", "tusfiles", "tubitv", "trollvid", "mp4edge",  "toltsd-fel", "thevideo", "tvad", "teramixer", "streamplay", "stream.moe", "streamin.to", "streame", "streamango", "streamcherry", "stagevu", "spruto", "speedvideo", "speedwatch", "speedvid", "speedplay", "rutube", "rapidvideo", "raptu", "putload", "shitmovie", "powvideo", "playwire", "playhd", "playedto", "play44", "ok.ru", "ocloud", "nowvideo", "novamov", "auroravid", "nosvideo", "noslocker", "myvi", "mystream", "mycloud", "mcloud", "mp4upload", "mp4stream", "movshare", "wholecloud", "vidgg", "mersalaayitten", "mehlizmovies", "megamp4", "mail.ru", "lolzor", "mycollection", "adhqmedia", "gagomatic", "funblr", "favour", "vidbaba", "likeafool", "kingvid", "jetload", "hdvid", "h265.se", "grifthost", "gorillavid", "googlevideo.com", "googleusercontent.com", "get.google.com", "plus.google.com", "googledrive.com", "drive.google.com", "docs.google.com", "youtube.googleapis.com", "goodvideohost", "goflicker", "getvi", "gamovideo", "flashx", "filez.tv", "fileweed", "fastplay.sx", "estream.to", "ecostream.tv", "earnvideos", "downace.com", "cloudtime", "divxstage", "dailymotion", "daclips", "cloudy.ec", "cloudy.eu", "cloudy.sx", "cloudy.ch", "cloudy.com", "clipwatching.com", "castamp", "blazefile", "bitvid.sx", "beststream", "apnasave", "anistream", "anime-portal", "9xplay"]
filetypes=["mp4", "webm", "m3u8", "avi", "mkv"]

ADDON=xbmcaddon.Addon()
HOME=xbmcvfs.translatePath(ADDON.getAddonInfo('path'))
ADDON_TYPE=xbmcaddon.Addon().getAddonInfo('id').split(".")[1]
  

def feedme(feed="", type=""):
    colour = ["black", "white", "gray", "blue", "teal", "fuchsia", "indigo", "turquoise", "cyan", "greenyellow", "lime", "green", "olive", "gold", "yello", "lavender", "pink", "magenta", "purple", "maroon", "chocolate", "orange", "red", "brown"]
    parameters=util.parseParameters()
    
    #util.logError(str(parameters))
    
    try:
        mode=int(parameters["mode"])
    except:
        mode=None
    
    try:
        offsite=ast.literal_eval(parameters['extras'])
        #util.logError(str(offsite))
        if "site_xml" in offsite:
            feed=offsite['site_xml']
            type="url"
    except:
        #not set, dont worry about it
        pass
    
    if mode==None or mode==0:
        # if we get here list the sites found in the json file
        menu=[]
        bits=util.getFile(feed, type)
        counter=0
        
        if str(len(bits['sites']))=="1" and 'folder' not in bits['sites']:
            mode=1
            parameters['extras']=str({"site":0})
        else:
            try:
                folder=ast.literal_eval(parameters['extras'])
                folder=folder['folder']
                for site in bits['sites']:
                    try:
                        if site['folder'].lower()==folder.lower():
                            extras={}
                            try:
                                extras['site_xml']=offsite['site_xml']
                            except:
                                pass
                            extras['site']=counter
                            menu.append({
                                "title": site['name'],
                                "url": site['name'],
                                "mode": "1", 
                                "poster":site['poster'],
                                "icon":site['poster'], 
                                "fanart":site['fanart'],
                                "type":ADDON_TYPE, 
                                "plot":"",
                                "isFolder":True,
                                "extras":extras
                            })
                        
                    except:
                        # site not in a folder
                        pass
                    counter=counter+1
            except:
                if "folders" in bits:
                    for site in bits['folders']:
                        extras={}
                        try:
                            extras['site_xml']=offsite['site_xml']
                        except:
                            pass
                        extras['site']=counter
                        folder_extras={}
                        folder_extras['folder']=site['name']
                        if "url" in site:
                            folder_extras['site_xml']=site['url']
                            del(folder_extras['folder'])
                        menu.append({
                            "title": site['name'],
                            "url": site['name'],
                            "mode": "0", 
                            "poster":site['poster'],
                            "icon":site['poster'], 
                            "fanart":site['fanart'],
                            "type":ADDON_TYPE, 
                            "plot":"",
                            "isFolder":True,
                            "extras":folder_extras
                        })
                for site in bits['sites']:
                    if "folder" not in site:
                        extras={}
                        try:
                            extras['site_xml']=offsite['site_xml']
                        except:
                            pass
                        extras['site']=counter
                        menu.append({
                            "title": site['name'],
                            "url": site['name'],
                            "mode": "1", 
                            "poster":site['poster'],
                            "icon":site['poster'], 
                            "fanart":site['fanart'],
                            "type":ADDON_TYPE, 
                            "plot":"",
                            "isFolder":True,
                            "extras":extras
                        })
                    counter=counter+1
            util.addMenuItems(menu)
    if mode==1:
        # first level within a site, show Latest, Search and any Tags within the specified site
        menu=[]
        extras=ast.literal_eval(parameters['extras'])
        
        try:
            extras['site_xml']=offsite['site_xml']
        except:
            pass
        
        bits=util.getFile(feed, type)
        site=bits['sites'][extras['site']]
        
        if "search_url" not in site and "tags" not in site and len(site['items'])==1:
            mode=2
            for item in site['items']:
                parameters['url']=site['items'][item][0]['site_url']
                break
                
        else:
            for item in site['items'].keys():
                if item.lower() != "search":
                    try:
                        poster=parameters['poster']
                    except:
                        try:
                            poster=site['items'][item][0]['folder_poster']
                            if "http" not in poster and "https" not in poster:
                                poster=os.path.join(HOME, '', poster)
                        except:
                            poster=""
                    try:
                        fanart=parameters['fanart']
                    except:
                        try:
                            fanart=site['items'][item][0]['folder_fanart']
                            if "http" not in fanart and "https" not in fanart:
                                fanart=os.path.join(HOME, '', fanart)
                        except:
                            fanart=""
                    extras['level']=item
                    
                    menu.append({
                        "title": item,
                        "url": urllib.quote_plus(site['items'][item][0]['site_url']),
                        "mode": "2", 
                        "poster":poster,
                        "icon":poster, 
                        "fanart":fanart,
                        "type":ADDON_TYPE, 
                        "plot":"",
                        "isFolder":True,
                        "extras":str(extras)
                    })                                          
            
            try:
                counter=0
                for tag in site['tags']:
                    try:
                        poster=parameters['poster']
                    except:
                        poster=""
                        
                    try:
                        fanart=parameters['fanart']
                    except:
                        fanart=""
                    extras['tag']=counter
                    menu.append({
                        "title": tag['name'],
                        "url": tag['url'],
                        "mode": "4", 
                        "poster":poster,
                        "icon":poster, 
                        "fanart":fanart,
                        "type":ADDON_TYPE, 
                        "plot":"",
                        "isFolder":True,
                        "extras":str(extras)
                    })
                    counter=counter+1
            except:
                pass
            if "search_url" in site:
                try:
                    poster=parameters['poster']
                except:
                    poster=""
                    
                try:
                    fanart=parameters['fanart']
                except:
                    fanart=""
                menu.append({
                    "title": "Search",
                    "url": "",
                    "mode": "3", 
                    "poster":poster,
                    "icon":poster, 
                    "fanart":fanart,
                    "type":ADDON_TYPE, 
                    "plot":"",
                    "isFolder":True,
                    "extras":str(extras)
                })
            util.addMenuItems(menu)
    if mode==2:
        # load the first level of relevant video information
        menu = []
        extras=ast.literal_eval(parameters['extras'])
        
        try:
            extras['site_xml']=offsite['site_xml']
        except:
            pass
        
        bits=util.getFile(feed, type)
        site=bits['sites'][extras['site']]
        
        if 'pos' in extras:
            pos=extras['pos']
        else:
            pos=0
            
        if 'level' in extras:
            level=extras['level']
        else:
            for item in site['items']:
                level=item
                break
            
        if len(site['items'][level])>pos+1:
            # another level is needed
            extras['pos']=pos+1
            newMode="2"
            isFolder=True
        else:
            # on a level where next move is to check for sources
            try:
                if site['items'][level][pos]['play_media']=="multiple":
                    newMode="113"
                    isFolder=True
                else:
                    newMode="111" # find source
                    isFolder=False
            except:
                # default to play first found
                newMode="111" # find source
                isFolder=False
            
        #util.alert(newMode)
        page=util.get(unescape(parameters['url']))
        next=page
        
        """if parameters['name']=="Next Page >":
            util.logError(str(next))"""
        
        try:
            if site['items'][level][pos]['global']!="":
                regex = util.prepare(site['items'][level][pos]['global'])
                matches = re.findall(regex, page)
                if matches:
                    page=matches[0]
        except:
            pass
            
        regex = util.prepare(site['items'][level][pos]['pattern'])
        matches = re.findall(regex, page)
        if matches:
            counter=0
            for match in matches:
                try:
                    title=unescape(util.replaceParts(site['items'][level][pos]['name'], matches[counter]).replace('\n', '').replace('\t', '').replace("\\", "").lstrip())
                except:
                    title=""
                #try:
                #    util.alert(site['items'][level][pos]['url'])
                url=urllib.quote_plus(util.replaceParts(site['items'][level][pos]['url'], matches[counter]))
                #    util.alert(">>"+url)
                #except:
                #    url=""
                try:
                    poster=util.replaceParts(site['items'][level][pos]['poster'], matches[counter]).encode('utf-8')
                except:
                    poster=""
                try:
                    fanart=util.replaceParts(site['items'][level][pos]['fanart'], matches[counter]).encode('utf-8')
                except:
                    fanart=""
                try:
                    plot=util.replaceParts(site['items'][level][pos]['plot'], matches[counter]).encode('utf-8')
                except:
                    plot=""
                    
                if isFolder:
                    menu.append({
                        "title": title,
                        "url": url,
                        "mode": newMode, 
                        "poster":poster,
                        "icon":poster, 
                        "fanart":fanart,
                        "type":ADDON_TYPE, 
                        "plot":plot,
                        "isFolder":isFolder,
                        "extras":str(extras)
                    })
                else:
                    menu.append({
                        "title": title,
                        "url": url,
                        "mode": newMode, 
                        "poster":poster,
                        "icon":poster, 
                        "fanart":fanart,
                        "type":ADDON_TYPE, 
                        "plot":plot,
                        "isFolder":isFolder,
                        "isPlayable":"True",
                        "extras":str(extras)
                    })
                counter=counter+1
        try:
            regex = util.prepare(site['items'][level][pos]['next_pattern'])
            matches = re.findall(regex, next)
            if matches:
                parts = []
                if len(matches) > 1:
                    for match in matches:
                        parts.append(match)
                else:
                    match = matches

                #nextlink=util.execPy(util.replaceParts(site['items'][level][pos]['next_url'], match))
                nextlink=util.replaceParts(site['items'][level][pos]['next_url'], match)
                extras['pos']=pos

                menu.append({
                    "title": "Next Page >",
                    "url": urllib.quote_plus(nextlink),
                    "mode": "2", 
                    "poster":"",
                    "icon":"", 
                    "fanart":"",
                    "type":ADDON_TYPE, 
                    "plot":plot,
                    "isFolder":True,
                    "extras":str(extras)
                })
        except Exception as e:
            util.logError(str(e))
            pass
        util.addMenuItems(menu)
    elif mode==3:
        # display the Search dialog and build search results
        menu = []
        extras=ast.literal_eval(parameters['extras'])
        
        try:
            extras['site_xml']=offsite['site_xml']
        except:
            pass
        
        term=util.searchDialog()
        
        if term:
            bits=util.getFile(feed, type)
            site=bits['sites'][extras['site']]
            pos=0
            
            
            for item in site['items']:
                level=item
                extras['level']=level
                break
            
            if len(site['items'][extras['level']])>pos+1:
                # another level is needed
                extras['pos']=1
                newMode="2"
                isFolder=True
                isPlayable=True
            else:
                # on a level where next move is to check for sources
                if site['items'][extras['level']][pos]['play_media'] == "multiple":
                    newMode="113"
                    isFolder=True
                    isPlayable=False
                else:
                    newMode="111" # find source
                    isFolder=False
                    isPlayable=True
            if "{{" in site['search_url'] and "}}" in site['search_url']:
                url =  util.execPy(site['search_url'].replace("{%}", term))
            else:
                url = site['search_url'].replace("{%}", term)
            util.logError(url)
            page=util.get(url)
            next=page
            
            try:
                if site['item']['global']!="":
                    regex = util.prepare(site['item']['global'])
                    matches = re.findall(regex, page)
                    if matches:
                        page=matches[0]
            except:
                pass
            

            regex = util.prepare(site['items'][level][pos]['pattern'])
            matches = re.findall(regex, page)
            
            if matches:
                counter=0
                for match in matches:
                    try:
                        title=unescape(util.replaceParts(site['items'][level][pos]['name'], matches[counter]).replace('\n', '').replace('\t', '').lstrip().encode('utf-8'))
                    except:
                        title=""
                    try:
                        url=util.replaceParts(site['items'][level][pos]['url'], matches[counter]).encode('utf-8')
                        #util.logError(url)
                    except:
                        url=""
                    try:
                        poster=util.replaceParts(site['items'][level][pos]['poster'], matches[counter]).encode('utf-8')
                    except:
                        poster=""
                    try:
                        fanart=util.replaceParts(site['items'][level][pos]['fanart'], matches[counter]).encode('utf-8')
                    except:
                        fanart=""
                    try:
                        plot=util.replaceParts(site['items'][level][pos]['plot'], matches[counter]).encode('utf-8')
                    except:
                        plot=""
                    
                    if isFolder:
                        menu.append({
                            "title": title,
                            "url": url,
                            "mode": newMode, 
                            "poster":poster,
                            "icon":poster, 
                            "fanart":fanart,
                            "type":ADDON_TYPE, 
                            "plot":plot,
                            "isFolder":isFolder,
                            "extras":str(extras)
                        })
                    else:
                        menu.append({
                            "title": title,
                            "url": url,
                            "mode": newMode, 
                            "poster":poster,
                            "icon":poster, 
                            "fanart":fanart,
                            "type":ADDON_TYPE, 
                            "plot":plot,
                            "isFolder":isFolder,
                            "isPlayable":"True",
                            "extras":str(extras)
                        })
                    counter=counter+1
            try:
                regex = util.prepare(site['items'][level][pos]['next_pattern'])
                matches = re.findall(regex, next)
                if matches:
                    parts = []
                    """for match in matches:
                        parts.append(match)"""

                    if len(matches) > 1:
                        for match in matches:
                            parts.append(match)
                        else:
                            match = matches

                    #nextlink=util.execPy(util.replaceParts(site['items'][level][pos]['next_url'], match))
                    nextlink=util.replaceParts(site['items'][level][pos]['next_url'], match)
                    menu.append({
                        "title": "Next Page >",
                        "url": nextlink,
                        "mode": "2", 
                        "poster":"",
                        "icon":"", 
                        "fanart":"",
                        "type":ADDON_TYPE, 
                        "plot":plot,
                        "isFolder":True,
                        "extras":str(extras)
                    })
            except:
                pass
            util.addMenuItems(menu)
        else:
            return False
    elif mode==4:
        # show relevant Tag video results
        menu = []
        
        extras=ast.literal_eval(parameters['extras'])
        
        try:
            extras['site_xml']=offsite['site_xml']
        except:
            pass
        
        bits=util.getFile(feed, type)
        
        site=bits['sites'][extras['site']]['tags'][extras['tag']]
        
        page=util.get(parameters['url'])
        next=page
        
        try:
            if site['item']['global']!="":
                regex = util.prepare(site['item']['global'])
                matches = re.findall(regex, page)
                if matches:
                    page=matches[0]
        except:
            pass
            
        regex = util.prepare(site['item']['pattern'])
        matches = re.findall(regex, page)    
        if matches:
            counter=0
            for match in matches:
                try:
                    title=unescape(util.replaceParts(site['item']['name'], matches[counter]).encode('utf-8'))
                except:
                    title=""
                try:
                    url=util.replaceParts(site['item']['url'], matches[counter]).encode('utf-8')
                except:
                    url=""
                try:
                    poster=util.replaceParts(site['item']['poster'], matches[counter]).encode('utf-8')
                except:
                    poster=""
                try:
                    fanart=util.replaceParts(site['item']['fanart'], matches[counter]).encode('utf-8')
                except:
                    fanart=""
                try:
                    plot=util.replaceParts(site['item']['plot'], matches[counter]).encode('utf-8')
                except:
                    plot=""
                
                menu.append({
                    "title": title,
                    "url": url,
                    "mode": "2", 
                    "poster":poster,
                    "icon":poster, 
                    "fanart":fanart,
                    "type":ADDON_TYPE, 
                    "plot":plot,
                    "isFolder":True,
                    "extras":extras
                })
                counter=counter+1
        util.addMenuItems(menu)
    elif mode==5:
        pass
    elif mode==111:
        # find playable sources in url
        #util.alert(parameters['url'])
        
        extras=ast.literal_eval(parameters['extras'])
        bits=util.getFile(feed, type)
        site=bits['sites'][extras['site']]
        
        try:
            pos=extras['pos']
        except:
            pos=0
            
        try:
            selected_video=int(site['items'][extras['level']][pos]['play_media'])-1
        except:
            selected_video=0
            
        
        page=util.get(parameters['url'])
        
        link=False
        try:
            link=urlresolver.resolve(parameters['url'])
        except Exception as e:
            if str(e).lower()=="sign in to confirm your age":
                util.notify("YouTube Error: Login to confirm age.")
                return False
            else:
                util.notify(str(e))
                return False
                
        if link:
            # play if url resolver reports true
            xbmc.log(f'parameters= {parameters}', xbmc.LOGINFO)
            util.playMedia(parameters['name'], parameters['poster'], link, force=True)
        elif any(ext in parameters['url'] for ext in filetypes):
            # play if url has a video extension
            util.playMedia(parameters['name'], parameters['poster'], parameters['url'], force=True)
        else:
            #search for video urls
            if "urlresolver" in site and site['urlresolver'].lower()=="false":
                regex="\"([^\s]*?\.(:?"+"|".join(filetypes)+"))\""
                matches = re.findall(regex, page)
            else:
                regex="(\/\/.*?\/embed.*?)[\?\"]"
                matches = re.findall(regex, page)
                regex="\"((?:http:|https:)?\/\/.*?\/watch.*?)[\"]"
                matches = matches + re.findall(regex, page)
                matches2=urlresolver.scrape_supported(page)
                #util.alert(str(matches))
                """regex="\"(https?://("+"|".join(supports)+")\..*?)\""
                matches2 = re.findall(regex, page)
                regex="\"((?:http:|https:)?\/\/.*?\/watch.*?)[\"]"
                matches3 = re.findall(regex, page)
                regex = 'https?://(.*?(?:\.googlevideo|(?:plus|drive|get|docs)\.google|google(?:usercontent|drive|apis))\.com)/(.*?(?:videoplayback\?|[\?&]authkey|host/)*.+)'
                matches4 = re.findall(regex, page)
                
                matches2=[ x for x in matches2 if any(sup in x for sup in supports) ]
                matches3=[ x for x in matches3 if any(sup in x for sup in supports) ]"""
            
                matches=matches+matches2
            util.logError("''''''''''''''''''''''''''''''''''''''''''''''''''''''")
            util.logError(">>>>"+str(matches))
            if isinstance(matches[selected_video], tuple):
                url=matches[selected_video][0]
            else:
                url=matches[selected_video]
            #util.alert(url)
            if "http" not in url:
                url="http:"+url
                
            link=urlresolver.resolve(url)
            
            if link==False:
                link=url
            
            util.playMedia(parameters['name'], parameters['poster'], link)
                
    elif mode==112:
        extras=ast.literal_eval(parameters['extras'])
        bits=util.getFile(feed, type)
        site=bits['sites'][extras['site']]
        
        page=util.get(parameters['url'])
        
        """if "urlresolver" in site and site['urlresolver'].lower()=="false":
            regex="\"(.*?\.mp4)\""
            matches = re.findall(regex, page)
            if matches:
                link=matches[0]
        else:"""
        regex="\"(//\S*?(:?"+("|".join(filetypes))+")\S*?)\""
        matches = re.findall(regex, page)
        if matches:
            url=matches[selected_video][0]
            if "http" not in url:
                link="http:"+url
        else:
            link=urlresolver.resolve(parameters['url'])
            if not link:
                try:
                    regex="(\/\/.*?\/embed.*?)[\?\"]"
                    matches = re.findall(regex, page)
                    regex="\"((?:http:|https:)?\/\/.*?\/watch.*?)[\"]"
                    matches = matches + re.findall(regex, page)
                    regex = 'https?://(.*?(?:\.googlevideo|(?:plus|drive|get|docs)\.google|google(?:usercontent|drive|apis))\.com)/(.*?(?:videoplayback\?|[\?&]authkey|host/)*.+)'
                    matches = matches + re.findall(regex, page)
                    if matches:
                        matches=[ x for x in matches if any(sup in x for sup in supports) ]
                        if matches:
                            link=urlresolver.resolve("http:"+matches[0])
                except Exception as e:
                    util.notify(str(e))
        if link:
            from . import downloader
            downloader.download(link, os.path.join(xbmcaddon.Addon().getSetting('folder'), parameters['name']+".mp4"))
        else:
            util.notify("No video found")
    elif mode==113:
        menu=[]
        extras=ast.literal_eval(parameters['extras'])
        bits=util.getFile(feed, type)
        site=bits['sites'][extras['site']]
        
        
        page=util.get(parameters['url'])
        
        matches=urlresolver.scrape_supported(page)
        #regex="(//\S*?(:?"+("|".join(filetypes))+")\S*?)"
        #matches2 = re.findall(regex, page)
        """regex="(\/\/.*?\/embed.*?)[\?\"]"
        matches2 = re.findall(regex, page)
        regex="\"(https?://("+"|".join(supports)+")\..*?)\""
        matches3 = re.findall(regex, page)
        regex = 'https?://(.*?(?:\.googlevideo|(?:plus|drive|get|docs)\.google|google(?:usercontent|drive|apis))\.com)/(.*?(?:videoplayback\?|[\?&]authkey|host/)*.+)'
        matches4 = re.findall(regex, page)
        
        matches2=[ x for x in matches2 if any(sup in x for sup in supports) ]
        matches3=[ x for x in matches3 if any(sup in x for sup in supports) ]
        
        matches=matches+matches2+matches3+matches4"""
        
        unique=[]
        for match in matches:#+matches2:
            if isinstance(match, tuple):
                unique.append(match[0])
            else:
                unique.append(match)
        
        matches=list(set(unique))        
        
        if matches:
            for match in matches:
                if "http" not in match:
                    rl="http:"+match
                else:
                    rl=match
                
                menu.append({
                    "title": rl,
                    "url": rl,
                    "mode": "114", 
                    "poster":parameters['poster'],
                    "icon":parameters['icon'], 
                    "fanart":parameters['fanart'],
                    "type":"", 
                    "plot":"",
                    "isFolder":False,
                    "isPlayable": False,
                    "extras":str(extras)
                })
            util.addMenuItems(menu)
    elif mode==114:
        # find playable sources in url
        #util.alert(parameters['url'])
        urlresolver.relevant_resolvers()
        try:
            link=urlresolver.resolve(str(parameters['url']))
        except Exception as e:
            util.notify(str(e))
            exit()
        if link:
            try:
                util.playMedia(parameters['name'], parameters['poster'], link)
            except:
                util.playMedia(parameters['name'], parameters['poster'], parameters['url'])