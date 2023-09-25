import xbmc, xbmcaddon
import xbmcvfs
import json
from pathlib import Path
from accountmgr.modules import control
from libs.common import var

class Auth:
        def meta_auth(self):
        #Seren
                try:
                        if xbmcvfs.exists(var.chk_seren) and xbmcvfs.exists(var.chkset_seren): #Check that the addon is installed and settings.xml exists
                                #Check Add-on API Keys
                                chk_fanart_api = xbmcaddon.Addon('plugin.video.seren').getSetting("fanart.apikey")
                                chk_omdb_api = xbmcaddon.Addon('plugin.video.seren').getSetting("omdb.apikey")
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.seren').getSetting("tmdb.apikey")
                                chk_tvdb_api = xbmcaddon.Addon('plugin.video.seren').getSetting("tvdb.apikey")

                                #Account Manager API Keys
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
                                your_omdb_api = accountmgr.getSetting("omdb.api.key")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                your_tvdb_api = accountmgr.getSetting("tvdb.api.key")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '': #Compare Account Mananger API to Add-on API. If they match authorization is skipped
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.seren")
                                        addon.setSetting("fanart.apikey", your_fanart_api)
                                        
                                if not str(var.chk_accountmgr_omdb) == str(chk_omdb_api) or str(chk_omdb_api) == '': #Compare Account Mananger API to Add-on API. If they match authorization is skipped
                                        addon = xbmcaddon.Addon("plugin.video.seren")
                                        addon.setSetting("omdb.apikey", your_omdb_api)

                                if not str(var.chk_accountmgr_tvdb) == str(chk_tvdb_api) or str(chk_tvdb_api) == '': #Compare Account Mananger API to Add-on API. If they match authorization is skipped
                                        addon = xbmcaddon.Addon("plugin.video.seren")
                                        addon.setSetting("tvdb.apikey", your_tvdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '': #Compare Account Mananger API to Add-on API. If they match authorization is skipped
                                        addon = xbmcaddon.Addon("plugin.video.seren")
                                        addon.setSetting("tmdb.apikey", your_tmdb_api)
                except:
                        pass
                
        #Fen
                try:
                        if xbmcvfs.exists(var.chk_fen) and xbmcvfs.exists(var.chkset_fen):
                                #Check Add-on API Keys
                                chk_fanart_api = xbmcaddon.Addon('plugin.video.fen').getSetting("fanart_client_key")
                                chk_omdb_api = xbmcaddon.Addon('plugin.video.fen').getSetting("omdb_api")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.fen').getSetting("imdb_user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.fen').getSetting("tmdb_api")

                                #Account Manager API Keys
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
                                your_omdb_api = accountmgr.getSetting("omdb.api.key")
                                your_imdb_api = accountmgr.getSetting("imdb.user")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.fen")
                                        addon.setSetting("fanart_client_key", your_fanart_api)

                                if not str(var.chk_accountmgr_omdb) == str(chk_omdb_api) or str(chk_omdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.fen")
                                        addon.setSetting("omdb_api", your_omdb_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.fen")
                                        addon.setSetting("imdb_user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.fen")
                                        addon.setSetting("tmdb_api", your_tmdb_api)
                except:
                        pass
                
        #Ezra
                try:
                        if xbmcvfs.exists(var.chk_ezra) and xbmcvfs.exists(var.chkset_ezra):
                                #Check Add-on API Keys
                                chk_fanart_api = xbmcaddon.Addon('plugin.video.ezra').getSetting("fanart_client_key")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.ezra').getSetting("imdb_user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.ezra').getSetting("tmdb_api")

                                #Account Manager API Keys
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
                                your_imdb_api = accountmgr.getSetting("imdb.user")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.ezra")
                                        addon.setSetting("fanart_client_key", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.ezra")
                                        addon.setSetting("imdb_user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.ezra")
                                        addon.setSetting("tmdb_api", your_tmdb_api)
                except:
                        pass

        #Coalition
                try:
                        if xbmcvfs.exists(var.chk_coal) and xbmcvfs.exists(var.chkset_coal):
                                #Check Add-on API Keys
                                chk_fanart_api = xbmcaddon.Addon('plugin.video.coalition').getSetting("fanart_client_key")
                                chk_omdb_api = xbmcaddon.Addon('plugin.video.coalition').getSetting("omdb_api")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.coalition').getSetting("imdb_user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.coalition').getSetting("tmdb_api")

                                #Account Manager API Keys
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
                                your_omdb_api = accountmgr.getSetting("omdb.api.key")
                                your_imdb_api = accountmgr.getSetting("imdb.user")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.coalition")
                                        addon.setSetting("fanart_client_key", your_fanart_api)

                                if not str(var.chk_accountmgr_omdb) == str(chk_omdb_api) or str(chk_omdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.coalition")
                                        addon.setSetting("omdb_api", your_omdb_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.coalition")
                                        addon.setSetting("imdb_user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.coalition")
                                        addon.setSetting("tmdb_api", your_tmdb_api)
                except:
                        pass

                
        #POV
                try:
                        if xbmcvfs.exists(var.chk_pov) and xbmcvfs.exists(var.chkset_pov):
                                #Check Add-on API Keys
                                chk_fanart_api = xbmcaddon.Addon('plugin.video.pov').getSetting("fanart_client_key")   
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.pov').getSetting("tmdb_api")

                                #Account Manager API Keys
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.pov")
                                        addon.setSetting("fanart_client_key", your_fanart_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.pov")
                                        addon.setSetting("tmdb_api", your_tmdb_api)
                except:
                        pass

        #Umbrella
                try:
                        if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb):
                                #Check Add-on API Keys
                                chk_fanart_api = xbmcaddon.Addon('plugin.video.umbrella').getSetting("fanart_tv.api_key")
                                chk_mdb_api = xbmcaddon.Addon('plugin.video.umbrella').getSetting("mdblist.api")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.umbrella').getSetting("imdbuser")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.umbrella').getSetting("tmdb.apikey")
                                chk_tmdb_user = xbmcaddon.Addon('plugin.video.umbrella').getSetting("tmdbusername")
                                chk_tmdb_pass = xbmcaddon.Addon('plugin.video.umbrella').getSetting("tmdbpassword")
                                chk_tmdb_session = xbmcaddon.Addon('plugin.video.umbrella').getSetting("tmdb.sessionid")

                                #Account Manager API Keys
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
                                your_mdb_api = accountmgr.getSetting("mdb.api.key")
                                your_imdb_api = accountmgr.getSetting("imdb.user")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                your_tmdb_user = accountmgr.getSetting("tmdb.username")
                                your_tmdb_pass = accountmgr.getSetting("tmdb.password")
                                your_tmdb_session = accountmgr.getSetting("tmdb.session_id")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("fanart_tv.api_key", your_fanart_api)

                                if not str(var.chk_accountmgr_mdb) == str(chk_mdb_api) or str(chk_mdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("mdblist.api", your_mdb_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("imdbuser", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("tmdb.apikey", your_tmdb_api)

                                if not str(var.chk_accountmgr_tmdb_user) == str(chk_tmdb_user) or str(chk_tmdb_user) == '':
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("tmdbusername", your_tmdb_user)

                                if not str(var.chk_accountmgr_tmdb_pass) == str(chk_tmdb_pass) or str(chk_tmdb_pass) == '':
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("tmdbpassword", your_tmdb_pass)

                                if not str(var.chk_accountmgr_tmdb_session) == str(chk_tmdb_session) or str(chk_tmdb_session) == '':
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("tmdb.sessionid", your_tmdb_session)
                except:
                        pass

        #The Crew
                try:
                        if xbmcvfs.exists(var.chk_crew) and xbmcvfs.exists(var.chkset_crew):
                                #Check Add-on API Keys
                                chk_fanart_api = xbmcaddon.Addon('plugin.video.thecrew').getSetting("fanart.tv.user")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.thecrew').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.thecrew').getSetting("tm.user")
                                chk_tvdb_api = xbmcaddon.Addon('plugin.video.thecrew').getSetting("tvdb.user")

                                #Account Manager API Keys
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
                                your_imdb_api = accountmgr.getSetting("imdb.user")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                your_tvdb_api = accountmgr.getSetting("tvdb.api.key")

                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.thecrew")
                                        addon.setSetting("fanart.tv.user", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.thecrew")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tvdb) == str(chk_tvdb_api) or str(chk_tvdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.thecrew")
                                        addon.setSetting("tvdb.user", your_tvdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.thecrew")
                                        addon.setSetting("tm.user", your_tmdb_api)
                except:
                        pass
                
        #Homelander
                try:
                        if xbmcvfs.exists(var.chk_home) and xbmcvfs.exists(var.chkset_home):
                                #Check Add-on API Keys
                                chk_fanart_api = xbmcaddon.Addon('plugin.video.homelander').getSetting("fanart.tv.user")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.homelander').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.homelander').getSetting("tm.user")

                                #Account Manager API Keys
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
                                your_imdb_api = accountmgr.getSetting("imdb.user")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.homelander")
                                        addon.setSetting("fanart.tv.user", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.homelander")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.homelander")
                                        addon.setSetting("tm.user", your_tmdb_api)
                except:
                        pass

        #Quicksilver
                try:
                        if xbmcvfs.exists(var.chk_quick) and xbmcvfs.exists(var.chkset_quick):
                                #Check Add-on API Keys
                                chk_fanart_api = xbmcaddon.Addon('plugin.video.quicksilver').getSetting("fanart.tv.user")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.quicksilver').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.quicksilver').getSetting("tm.user")

                                #Account Manager API Keys
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
                                your_imdb_api = accountmgr.getSetting("imdb.user")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.quicksilver")
                                        addon.setSetting("fanart.tv.user", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.quicksilver")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.quicksilver")
                                        addon.setSetting("tm.user", your_tmdb_api)
                except:
                        pass

        #Chains Genocide
                try:
                        if xbmcvfs.exists(var.chk_genocide) and xbmcvfs.exists(var.chkset_genocide):
                                #Check Add-on API Keys
                                chk_fanart_api = xbmcaddon.Addon('plugin.video.chainsgenocide').getSetting("fanart.tv.user")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.chainsgenocide').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.chainsgenocide').getSetting("tm.user")

                                #Account Manager API Keys
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
                                your_imdb_api = accountmgr.getSetting("imdb.user")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.chainsgenocide")
                                        addon.setSetting("fanart.tv.user", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.chainsgenocide")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.chainsgenocide")
                                        addon.setSetting("tm.user", your_tmdb_api)
                except:
                        pass

        #Shazam
                try:
                        if xbmcvfs.exists(var.chk_shazam) and xbmcvfs.exists(var.chkset_shazam):
                                #Check Add-on API Keys
                                chk_fanart_api = xbmcaddon.Addon('plugin.video.shazam').getSetting("fanart.tv.user")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.shazam').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.shazam').getSetting("tm.user")

                                #Account Manager API Keys
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
                                your_imdb_api = accountmgr.getSetting("imdb.user")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.shazam")
                                        addon.setSetting("fanart.tv.user", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.shazam")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.shazam")
                                        addon.setSetting("tm.user", your_tmdb_api)
                except:
                        pass

        #Nightwing
                try:
                        if xbmcvfs.exists(var.chk_night) and xbmcvfs.exists(var.chkset_night):
                                #Check Add-on API Keys
                                chk_fanart_api = xbmcaddon.Addon('plugin.video.nightwing').getSetting("fanart.tv.user")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.nightwing').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.nightwing').getSetting("tm.user")

                                #Account Manager API Keys
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
                                your_imdb_api = accountmgr.getSetting("imdb.user")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.nightwing")
                                        addon.setSetting("fanart.tv.user", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.nightwing")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.nightwing")
                                        addon.setSetting("tm.user", your_tmdb_api)
                except:
                        pass

        #Alvin
                try:
                        if xbmcvfs.exists(var.chk_alvin) and xbmcvfs.exists(var.chkset_alvin):
                                #Check Add-on API Keys
                                chk_fanart_api = xbmcaddon.Addon('plugin.video.alvin').getSetting("fanart.tv.user")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.alvin').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.alvin').getSetting("tm.user")

                                #Account Manager API Keys
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
                                your_imdb_api = accountmgr.getSetting("imdb.user")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.alvin")
                                        addon.setSetting("fanart.tv.user", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.alvin")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.alvin")
                                        addon.setSetting("tm.user", your_tmdb_api)
                except:
                        pass

        #Moria
                try:
                        if xbmcvfs.exists(var.chk_moria) and xbmcvfs.exists(var.chkset_moria):
                                #Check Add-on API Keys
                                chk_fanart_api = xbmcaddon.Addon('plugin.video.moria').getSetting("fanart.tv.user")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.moria').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.moria').getSetting("tm.user")

                                #Account Manager API Keys
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
                                your_imdb_api = accountmgr.getSetting("imdb.user")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.moria")
                                        addon.setSetting("fanart.tv.user", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.moria")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.moria")
                                        addon.setSetting("tm.user", your_tmdb_api)
                except:
                        pass

        #Absolution
                try:
                        if xbmcvfs.exists(var.chk_absol) and xbmcvfs.exists(var.chkset_absol):
                                #Check Add-on API Keys
                                chk_fanart_api = xbmcaddon.Addon('plugin.video.absolution').getSetting("fanart.tv.user")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.absolution').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.absolution').getSetting("tm.user")

                                #Account Manager API Keys
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
                                your_imdb_api = accountmgr.getSetting("imdb.user")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.absolution")
                                        addon.setSetting("fanart.tv.user", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.absolution")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.absolution")
                                        addon.setSetting("tm.user", your_tmdb_api)
                except:
                        pass

        #Nine Lives
                try:
                        if xbmcvfs.exists(var.chk_nine) and xbmcvfs.exists(var.chkset_nine):
                                #Check Add-on API Keys
                                chk_fanart_api = xbmcaddon.Addon('plugin.video.nine').getSetting("fanart.tv.user")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.nine').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.nine').getSetting("tm.user")

                                #Account Manager API Keys
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
                                your_imdb_api = accountmgr.getSetting("imdb.user")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.nine")
                                        addon.setSetting("fanart.tv.user", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.nine")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.nine")
                                        addon.setSetting("tm.user", your_tmdb_api)
                except:
                        pass
                
        #TMDB Helper
                try:
                        if xbmcvfs.exists(var.chk_tmdbh) and xbmcvfs.exists(var.chkset_tmdbh):
                                #Check Add-on API Keys
                                chk_fanart_api = xbmcaddon.Addon('plugin.video.themoviedb.helper').getSetting("fanarttv_clientkey")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.themoviedb.helper').getSetting("omdb_apikey")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.themoviedb.helper').getSetting("mdblist_apikey")

                                #Account Manager API Keys
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
                                your_omdb_api = accountmgr.getSetting("omdb.api.key")
                                your_mdb_api = accountmgr.getSetting("mdb.api.key")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.themoviedb.helper")
                                        addon.setSetting("fanarttv_clientkey", your_fanart_api)

                                if not str(var.chk_accountmgr_omdb) == str(chk_omdb_api) or str(chk_omdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.themoviedb.helper")
                                        addon.setSetting("omdb_apikey", your_omdb_api)
                                        
                                if not str(var.chk_accountmgr_mdb) == str(chk_mdb_api) or str(chk_mdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.themoviedb.helper")
                                        addon.setSetting("mdblist_apikey", your_mdb_api)
                except:
                        pass

        #Embuary Info
                try:
                        if xbmcvfs.exists(var.chk_embuary) and xbmcvfs.exists(var.chkset_embuary):
                                
                                chk_omdb_api = xbmcaddon.Addon('script.embuary.info').getSetting("omdb_api_key")
                                chk_tmdb_api = xbmcaddon.Addon('script.embuary.info').getSetting("tmdb_api_key")
                               
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_omdb_api = accountmgr.getSetting("omdb.api.key")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                                                       
                                if not str(var.chk_accountmgr_omdb) == str(chk_omdb_api) or str(chk_omdb_api) == '':
                                        addon = xbmcaddon.Addon("script.embuary.info")
                                        addon.setSetting("omdb_api_key", your_omdb_api)
                                       
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("script.embuary.info")
                                        addon.setSetting("tmdb_api_key", your_tmdb_api)
                except:
                        pass

        #Metahandler
                try:
                        if xbmcvfs.exists(var.chk_meta) and xbmcvfs.exists(var.chkset_meta):
                                
                                chk_tvdb_api = xbmcaddon.Addon('script.module.metahandler').getSetting("tvdb_api_key")
                                chk_omdb_api = xbmcaddon.Addon('script.module.metahandler').getSetting("omdb_api_key")
                                chk_tmdb_api = xbmcaddon.Addon('script.module.metahandler').getSetting("tmdb_api_key")
                               
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_tvdb_api = accountmgr.getSetting("tvdb.api.key")
                                your_omdb_api = accountmgr.getSetting("omdb.api.key")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                enable_tvdb = ("true")
                                enable_omdb_fallback = ("true")
                                enable_omdb_override = ("true")
                                enable_tmdb = ("true")
                                
                                if not str(var.chk_accountmgr_tvdb) == str(chk_tvdb_api) or str(chk_tvdb_api) == '':
                                        addon = xbmcaddon.Addon("script.module.metahandler")
                                        addon.setSetting("tvdb_api_key", your_tvdb_api)
                                        
                                if not str(var.chk_accountmgr_omdb) == str(chk_omdb_api) or str(chk_omdb_api) == '':
                                        addon = xbmcaddon.Addon("script.module.metahandler")
                                        addon.setSetting("omdb_api_key", your_omdb_api)
                                       
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("script.module.metahandler")
                                        addon.setSetting("tmdb_api_key", your_tmdb_api)
                                        
                                if str(var.chk_accountmgr_tvdb) != '':
                                        addon = xbmcaddon.Addon("script.module.metahandler")
                                        addon.setSetting("override_tvdb_key", enable_tvdb)

                                if str(var.chk_accountmgr_omdb) != '':
                                        addon = xbmcaddon.Addon("script.module.metahandler")
                                        addon.setSetting("omdbapi_fallback", enable_omdb_fallback)
                                        
                                        addon = xbmcaddon.Addon("script.module.metahandler")
                                        addon.setSetting("override_omdb_key", enable_omdb_override)

                                if str(var.chk_accountmgr_tmdb) != '':
                                        addon = xbmcaddon.Addon("script.module.metahandler")
                                        addon.setSetting("override_tmdb_key", enable_tmdb)
                                        
                except:
                        pass

        #PVR Artwork Module
                try:
                        if xbmcvfs.exists(var.chk_pvr) and xbmcvfs.exists(var.chkset_pvr):
                                
                                chk_trakt_api = xbmcaddon.Addon('script.module.pvr.artwork').getSetting("fanart_apikey")
                                chk_tmdb_api = xbmcaddon.Addon('script.module.pvr.artwork').getSetting("tmdb_apikey")
                               
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                enable_fanart = ("true")
                                enable_fanart_prefer = ("true")
                                enable_tmdb = ("true")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        addon = xbmcaddon.Addon("script.module.pvr.artwork")
                                        addon.setSetting("fanart_apikey", your_fanart_api)
                                       
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("script.module.pvr.artwork")
                                        addon.setSetting("tmdb_apikey", your_tmdb_api)

                                if str(var.chk_accountmgr_fanart) != '':
                                        addon = xbmcaddon.Addon("script.module.pvr.artwork")
                                        addon.setSetting("use_fanart_tv", enable_fanart)

                                        addon = xbmcaddon.Addon("script.module.pvr.artwork")
                                        addon.setSetting("prefer_fanart_tv", enable_fanart_prefer)

                                if str(var.chk_accountmgr_tmdb) != '':
                                        addon = xbmcaddon.Addon("script.module.pvr.artwork")
                                        addon.setSetting("use_tmdb", enable_tmdb)
                except:
                        pass

        #My Accounts
                try:
                        if xbmcvfs.exists(var.chk_myaccounts) and xbmcvfs.exists(var.chkset_myaccounts):
                                #Check Add-on API Keys
                                chk_fanart_api = xbmcaddon.Addon('script.module.myaccounts').getSetting("fanart.tv.api.key")
                                chk_imdb_api = xbmcaddon.Addon('script.module.myaccounts').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('script.module.myaccounts').getSetting("tmdb.api.key")
                                chk_tmdb_user = xbmcaddon.Addon('script.module.myaccounts').getSetting("tmdb.username")
                                chk_tmdb_pass = xbmcaddon.Addon('script.module.myaccounts').getSetting("tmdb.password")
                                chk_tmdb_session = xbmcaddon.Addon('script.module.myaccounts').getSetting("tmdb.session_id")

                                #Account Manager API Keys
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
                                your_imdb_api = accountmgr.getSetting("imdb.user")
                                your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
                                your_tmdb_user = accountmgr.getSetting("tmdb.username")
                                your_tmdb_pass = accountmgr.getSetting("tmdb.password")
                                your_tmdb_session = accountmgr.getSetting("tmdb.session_id")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("script.module.myaccounts")
                                        addon.setSetting("fanart.tv.api.key", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("script.module.myaccounts")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("script.module.myaccounts")
                                        addon.setSetting("tmdb.api.key", your_tmdb_api)

                                if not str(var.chk_accountmgr_tmdb_user) == str(chk_tmdb_user) or str(chk_tmdb_user) == '':
                                        addon = xbmcaddon.Addon("script.module.myaccounts")
                                        addon.setSetting("tmdb.username", your_tmdb_user)

                                if not str(var.chk_accountmgr_tmdb_pass) == str(chk_tmdb_pass) or str(chk_tmdb_pass) == '':
                                        addon = xbmcaddon.Addon("script.module.myaccounts")
                                        addon.setSetting("tmdb.password", your_tmdb_pass)
                                        
                                if not str(var.chk_accountmgr_tmdb_session) == str(chk_tmdb_session) or str(chk_tmdb_session) == '':
                                        addon = xbmcaddon.Addon("script.module.myaccounts")
                                        addon.setSetting("tmdb.session_id", your_tmdb_session)
                except:
                        pass
