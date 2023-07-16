import xbmc, xbmcaddon
import xbmcvfs
import json
from pathlib import Path
from accountmgr.modules import control
from libs.common import var

class Auth:
        def file_auth(self):
               
        #Umbrella
                try:
                        if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb):
                                
                                chk_file = xbmcaddon.Addon('plugin.video.umbrella').getSetting("filepursuit.api")
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_file_api = accountmgr.getSetting("filepursuit.api.key")
                                enable_file = ("true")
                                
                                if not str(var.chk_accountmgr_file) == str(chk_file) or str(chk_file) == '':
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("filepursuit.enable", enable_file)
                                        addon.setSetting("filepursuit.api", your_file_api)
                except:
                        pass
                
        #Artemis
                try:
                        if xbmcvfs.exists(var.chk_artemis) and xbmcvfs.exists(var.chkset_artemis):
                                
                                chk_file = xbmcaddon.Addon('plugin.video.artemis').getSetting("filepursuit.api")
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_file_api = accountmgr.getSetting("filepursuit.api.key")
                                
                                if not str(var.chk_accountmgr_file) == str(chk_file) or str(chk_file) == '':
                                        addon = xbmcaddon.Addon("plugin.video.artemis")
                                        addon.setSetting("filepursuit.api", your_file_api)
                except:
                        pass
                
        #Dynasty
                try:
                        if xbmcvfs.exists(var.chk_dyna) and xbmcvfs.exists(var.chkset_dyna):
                                
                                chk_file = xbmcaddon.Addon('plugin.video.dynasty').getSetting("filepursuit.api")
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_file_api = accountmgr.getSetting("filepursuit.api.key")
                                
                                if not str(var.chk_accountmgr_file) == str(chk_file) or str(chk_file) == '':
                                        addon = xbmcaddon.Addon("plugin.video.dynasty")
                                        addon.setSetting("filepursuit.api", your_file_api)
                except:
                        pass

                
        #My Accounts
                try:
                        if xbmcvfs.exists(var.chk_myaccounts) and xbmcvfs.exists(var.chkset_myaccounts):
                                
                                chk_file = xbmcaddon.Addon('script.module.myaccounts').getSetting("filepursuit.api.key")
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_file_api = accountmgr.getSetting("filepursuit.api.key")
                                
                                if not str(var.chk_accountmgr_file) == str(chk_file) or str(chk_file) == '':
                                        addon = xbmcaddon.Addon("script.module.myaccounts")
                                        addon.setSetting("filepursuit.api.key", your_file_api)
                except:
                        pass
                
        #Your Accounts
                try:
                        if xbmcvfs.exists(var.chk_youraccounts) and xbmcvfs.exists(var.chkset_youraccounts):
                                
                                chk_file = xbmcaddon.Addon('script.module.youraccounts').getSetting("filepursuit.api.key")
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_file_api = accountmgr.getSetting("filepursuit.api.key")
                                
                                if not str(var.chk_accountmgr_file) == str(chk_file) or str(chk_file) == '':
                                        addon = xbmcaddon.Addon("script.module.youraccounts")
                                        addon.setSetting("filepursuit.api.key", your_file_api)
                except:
                        pass


