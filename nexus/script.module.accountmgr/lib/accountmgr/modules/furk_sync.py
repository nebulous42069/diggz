import xbmc, xbmcaddon
import xbmcvfs
import json
from pathlib import Path
from accountmgr.modules import control
from libs.common import var

class Auth:
        def furk_auth(self):

        #Fen
                try:
                        if xbmcvfs.exists(var.chk_fen) and xbmcvfs.exists(var.chkset_fen):

                                chk_furk = xbmcaddon.Addon('plugin.video.fen').getSetting("furk_password")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_furk_user = accountmgr.getSetting("furk.username")
                                your_furk_pass = accountmgr.getSetting("furk.password")
                                your_furk_api = accountmgr.getSetting("furk.api.key")
                                enable_furk = ("true")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.fen")
                                        addon.setSetting("provider.furk", enable_furk)
                                        addon.setSetting("furk_login", your_furk_user)
                                        addon.setSetting("furk_password", your_furk_pass)
                                        addon.setSetting("furk_api_key", your_furk_api)
                except:
                        pass
                
        #Ezra
                try:
                        if xbmcvfs.exists(var.chk_ezra) and xbmcvfs.exists(var.chkset_ezra):
                                
                                #Check add-on settings
                                chk_furk = xbmcaddon.Addon('plugin.video.ezra').getSetting("furk_password")

                                #Account Manager settings
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_furk_user = accountmgr.getSetting("furk.username")
                                your_furk_pass = accountmgr.getSetting("furk.password")
                                your_furk_api = accountmgr.getSetting("furk.api.key")
                                enable_furk = ("true")
                                
                                #Write data to settings.xml
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.ezra")
                                        addon.setSetting("provider.furk", enable_furk)
                                        addon.setSetting("furk_login", your_furk_user)
                                        addon.setSetting("furk_password", your_furk_pass)
                                        addon.setSetting("furk_api_key", your_furk_api)
                except:
                        pass
                
        #Coalition
                try:
                        if xbmcvfs.exists(var.chk_coal) and xbmcvfs.exists(var.chkset_coal):

                                chk_furk = xbmcaddon.Addon('plugin.video.coalition').getSetting("furk_password")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_furk_user = accountmgr.getSetting("furk.username")
                                your_furk_pass = accountmgr.getSetting("furk.password")
                                your_furk_api = accountmgr.getSetting("furk.api.key")
                                enable_furk = ("true")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.coalition")
                                        addon.setSetting("provider.furk", enable_furk)
                                        addon.setSetting("furk_login", your_furk_user)
                                        addon.setSetting("furk_password", your_furk_pass)
                                        addon.setSetting("furk_api_key", your_furk_api)
                except:
                        pass
                
        #POV
                try:
                        if xbmcvfs.exists(var.chk_pov) and xbmcvfs.exists(var.chkset_pov):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.pov').getSetting("furk_password")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_furk_user = accountmgr.getSetting("furk.username")
                                your_furk_pass = accountmgr.getSetting("furk.password")
                                your_furk_api = accountmgr.getSetting("furk.api.key")
                                enable_furk = ("true")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.pov")
                                        addon.setSetting("provider.furk", enable_furk)
                                        addon.setSetting("furk_login", your_furk_user)
                                        addon.setSetting("furk_password", your_furk_pass)
                                        addon.setSetting("furk_api_key", your_furk_api)
                except:
                        pass

        #Umbrella
                try:
                        if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb):

                                chk_furk = xbmcaddon.Addon('plugin.video.umbrella').getSetting("furk.user_pass")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_furk_user = accountmgr.getSetting("furk.username")
                                your_furk_pass = accountmgr.getSetting("furk.password")
                                your_furk_api = accountmgr.getSetting("furk.api.key")
                                enable_furk = ("true")
                                
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("furk.enable", enable_furk)
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        pass

        #The Crew
                try:
                        if xbmcvfs.exists(var.chk_crew) and xbmcvfs.exists(var.chkset_crew):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.thecrew').getSetting("furk.user_pass")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_furk_user = accountmgr.getSetting("furk.username")
                                your_furk_pass = accountmgr.getSetting("furk.password")
                                your_furk_api = accountmgr.getSetting("furk.api.key")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.thecrew")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        pass
                
        #Homelander
                try:
                        if xbmcvfs.exists(var.chk_home) and xbmcvfs.exists(var.chkset_home):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.homelander').getSetting("furk.user_pass")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_furk_user = accountmgr.getSetting("furk.username")
                                your_furk_pass = accountmgr.getSetting("furk.password")
                                your_furk_api = accountmgr.getSetting("furk.api.key")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.homelander")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        pass

        #Quicksilver
                try:
                        if xbmcvfs.exists(var.chk_quick) and xbmcvfs.exists(var.chkset_quick):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.quicksilver').getSetting("furk.user_pass")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_furk_user = accountmgr.getSetting("furk.username")
                                your_furk_pass = accountmgr.getSetting("furk.password")
                                your_furk_api = accountmgr.getSetting("furk.api.key")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.quicksilver")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        pass

        #Chains Genocide
                try:
                        if xbmcvfs.exists(var.chk_genocide) and xbmcvfs.exists(var.chkset_genocide):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.chainsgenocide').getSetting("furk.user_pass")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_furk_user = accountmgr.getSetting("furk.username")
                                your_furk_pass = accountmgr.getSetting("furk.password")
                                your_furk_api = accountmgr.getSetting("furk.api.key")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.chainsgenocide")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        pass
                
        #Shazam
                try:
                        if xbmcvfs.exists(var.chk_shazam) and xbmcvfs.exists(var.chkset_shazam):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.shazam').getSetting("furk.user_pass")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_furk_user = accountmgr.getSetting("furk.username")
                                your_furk_pass = accountmgr.getSetting("furk.password")
                                your_furk_api = accountmgr.getSetting("furk.api.key")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.shazam")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        pass

        #Nightwing
                try:
                        if xbmcvfs.exists(var.chk_night) and xbmcvfs.exists(var.chkset_night):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.nightwing').getSetting("furk.user_pass")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_furk_user = accountmgr.getSetting("furk.username")
                                your_furk_pass = accountmgr.getSetting("furk.password")
                                your_furk_api = accountmgr.getSetting("furk.api.key")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.nightwing")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        pass

        #Alvin
                try:
                        if xbmcvfs.exists(var.chk_alvin) and xbmcvfs.exists(var.chkset_alvin):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.alvin').getSetting("furk.user_pass")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_furk_user = accountmgr.getSetting("furk.username")
                                your_furk_pass = accountmgr.getSetting("furk.password")
                                your_furk_api = accountmgr.getSetting("furk.api.key")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.alvin")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        pass

        #Moria
                try:
                        if xbmcvfs.exists(var.chk_moria) and xbmcvfs.exists(var.chkset_moria):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.moria').getSetting("furk.user_pass")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_furk_user = accountmgr.getSetting("furk.username")
                                your_furk_pass = accountmgr.getSetting("furk.password")
                                your_furk_api = accountmgr.getSetting("furk.api.key")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.moria")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        pass

        #Absolution
                try:
                        if xbmcvfs.exists(var.chk_absol) and xbmcvfs.exists(var.chkset_absol):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.absolution').getSetting("furk.user_pass")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_furk_user = accountmgr.getSetting("furk.username")
                                your_furk_pass = accountmgr.getSetting("furk.password")
                                your_furk_api = accountmgr.getSetting("furk.api.key")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.absolution")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        pass

        #Nine Lives
                try:
                        if xbmcvfs.exists(var.chk_nine) and xbmcvfs.exists(var.chkset_nine):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.nine').getSetting("furk.user_pass")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_furk_user = accountmgr.getSetting("furk.username")
                                your_furk_pass = accountmgr.getSetting("furk.password")
                                your_furk_api = accountmgr.getSetting("furk.api.key")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.nine")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        pass
                
        #My Accounts
                try:
                        if xbmcvfs.exists(var.chk_myaccounts) and xbmcvfs.exists(var.chkset_myaccounts):
                                
                                chk_furk = xbmcaddon.Addon('script.module.myaccounts').getSetting("furk.password")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_furk_user = accountmgr.getSetting("furk.username")
                                your_furk_pass = accountmgr.getSetting("furk.password")
                                your_furk_api = accountmgr.getSetting("furk.api.key")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("script.module.myaccounts")
                                        addon.setSetting("furk.username", your_furk_user)
                                        addon.setSetting("furk.password", your_furk_pass)
                                        addon.setSetting("furk.api.key", your_furk_api)
                except:
                        pass
