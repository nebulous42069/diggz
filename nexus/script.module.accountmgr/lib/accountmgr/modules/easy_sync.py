import xbmc, xbmcaddon
import xbmcvfs
import json
from pathlib import Path
from accountmgr.modules import control
from libs.common import var

class Auth:
        def easy_auth(self):

        #Fen
                try:
                        if xbmcvfs.exists(var.chk_fen) and xbmcvfs.exists(var.chkset_fen):

                                chk_easy = xbmcaddon.Addon('plugin.video.fen').getSetting("easynews_password")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_easy_user = accountmgr.getSetting("easynews.username")
                                your_easy_pass = accountmgr.getSetting("easynews.password")
                                enable_easy = ("true")
                                     
                                if not str(var.chk_accountmgr_easy) == str(chk_easy) or str(chk_easy) == '':
                                        addon = xbmcaddon.Addon("plugin.video.fen")
                                        addon.setSetting("provider.easynews", enable_easy)
                                        addon.setSetting("easynews_user", your_easy_user)
                                        addon.setSetting("easynews_password", your_easy_pass)
                except:
                        pass
                
        #Ezra
                try:
                        if xbmcvfs.exists(var.chk_ezra) and xbmcvfs.exists(var.chkset_ezra ):
                                
                                #Check add-on settings
                                chk_easy = xbmcaddon.Addon('plugin.video.ezra').getSetting("easynews_password")

                                #Account Manager settings
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_easy_user = accountmgr.getSetting("easynews.username")
                                your_easy_pass = accountmgr.getSetting("easynews.password")
                                enable_easy = ("true")
                        
                                #Write data to settings.xml                                       
                                if not str(var.chk_accountmgr_easy) == str(chk_easy) or str(chk_easy) == '':
                                        addon = xbmcaddon.Addon("plugin.video.ezra")
                                        addon.setSetting("provider.easynews", enable_easy)
                                        addon.setSetting("easynews_user", your_easy_user)
                                        addon.setSetting("easynews_password", your_easy_pass)
                except:
                        pass

        #Coalition
                try:
                        if xbmcvfs.exists(var.chk_coal) and xbmcvfs.exists(var.chkset_coal):

                                chk_easy = xbmcaddon.Addon('plugin.video.coalition').getSetting("easynews_password")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_easy_user = accountmgr.getSetting("easynews.username")
                                your_easy_pass = accountmgr.getSetting("easynews.password")
                                enable_easy = ("true")
                                     
                                if not str(var.chk_accountmgr_easy) == str(chk_easy) or str(chk_easy) == '':
                                        addon = xbmcaddon.Addon("plugin.video.coalition")
                                        addon.setSetting("provider.easynews", enable_easy)
                                        addon.setSetting("easynews_user", your_easy_user)
                                        addon.setSetting("easynews_password", your_easy_pass)
                except:
                        pass
                
        #POV
                try:
                        if xbmcvfs.exists(var.chk_pov) and xbmcvfs.exists(var.chkset_pov) and accountmgr.getSetting("easynews.password") != '':

                                chk_easy = xbmcaddon.Addon('plugin.video.pov').getSetting("easynews_password")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_easy_user = accountmgr.getSetting("easynews.username")
                                your_easy_pass = accountmgr.getSetting("easynews.password")
                                enable_easy = ("true")
                                     
                                if not str(var.chk_accountmgr_easy) == str(chk_easy) or str(chk_easy) == '':
                                        addon = xbmcaddon.Addon("plugin.video.pov")
                                        addon.setSetting("provider.easynews", enable_easy)
                                        addon.setSetting("easynews_user", your_easy_user)
                                        addon.setSetting("easynews_password", your_easy_pass)
                except:
                        pass

        #Umbrella
                try:
                        if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb):

                                chk_easy = xbmcaddon.Addon('plugin.video.umbrella').getSetting("easynews.password")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_easy_user = accountmgr.getSetting("easynews.username")
                                your_easy_pass = accountmgr.getSetting("easynews.password")
                                enable_easy = ("true")
                                     
                                if not str(var.chk_accountmgr_easy) == str(chk_easy) or str(chk_easy) == '':
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("easynews.enable", enable_easy)
                                        addon.setSetting("easynews.user", your_easy_user)
                                        addon.setSetting("easynews.password", your_easy_pass)
                except:
                        pass

        #The Crew
                try:
                        if xbmcvfs.exists(var.chk_crew) and xbmcvfs.exists(var.chkset_crew):

                                chk_easy = xbmcaddon.Addon('plugin.video.thecrew').getSetting("easynews.password")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_easy_user = accountmgr.getSetting("easynews.username")
                                your_easy_pass = accountmgr.getSetting("easynews.password")
                                     
                                if not str(var.chk_accountmgr_easy) == str(chk_easy) or str(chk_easy) == '':
                                        addon = xbmcaddon.Addon("plugin.video.thecrew")
                                        addon.setSetting("easynews.user", your_easy_user)
                                        addon.setSetting("easynews.password", your_easy_pass)
                except:
                        pass
                
        #My Accounts
                try:
                        if xbmcvfs.exists(var.chk_myaccounts) and xbmcvfs.exists(var.chkset_myaccounts):

                                chk_easy = xbmcaddon.Addon('script.module.myaccounts').getSetting("easynews.password")

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_easy_user = accountmgr.getSetting("easynews.username")
                                your_easy_pass = accountmgr.getSetting("easynews.password")
                                     
                                if not str(var.chk_accountmgr_easy) == str(chk_easy) or str(chk_easy) == '':
                                        addon = xbmcaddon.Addon("script.module.myaccounts")
                                        addon.setSetting("easynews.username", your_easy_user)
                                        addon.setSetting("easynews.password", your_easy_pass)
                except:
                        pass
