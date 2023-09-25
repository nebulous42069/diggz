import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import os.path
import os
import xbmcvfs
import sys
try:  # Python 3
    from urllib.parse import parse_qsl
except ImportError:  # Python 2
    from urlparse import parse_qsl
from resources.libs.common.config import CONFIG
from resources.libs.common import logging
from resources.libs.common import tools
from resources.libs.common import var
from resources.libs.gui import menu

addon = xbmcaddon.Addon
addonObject = addon('script.module.acctview')
addonInfo = addonObject.getAddonInfo
getLangString = xbmcaddon.Addon().getLocalizedString
condVisibility = xbmc.getCondVisibility
execute = xbmc.executebuiltin
monitor = xbmc.Monitor()
transPath = xbmcvfs.translatePath
joinPath = os.path.join
dialog = xbmcgui.Dialog()
backup_path = var.setting('backupfolder')
rd_backup = xbmcvfs.translatePath(backup_path) + 'realdebrid/'
pm_backup = xbmcvfs.translatePath(backup_path) + 'premiumize/'
ad_backup = xbmcvfs.translatePath(backup_path) + 'alldebrid/'
trakt_backup = xbmcvfs.translatePath(backup_path) + 'trakt/'
meta_backup = xbmcvfs.translatePath(backup_path) + 'meta/'
non_backup = xbmcvfs.translatePath(backup_path) + 'nondebrid/'

amgr_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.acctview').getAddonInfo('path'), 'resources', 'icons'), 'accountmgr.png')
rd_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.acctview').getAddonInfo('path'), 'resources', 'icons'), 'realdebrid.png')
pm_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.acctview').getAddonInfo('path'), 'resources', 'icons'), 'premiumize.png')
ad_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.acctview').getAddonInfo('path'), 'resources', 'icons'), 'alldebrid.png')
trakt_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.acctview').getAddonInfo('path'), 'resources', 'icons'), 'trakt.png')

class Router:
    def __init__(self):
        self.route = None
        self.params = {}

    def _log_params(self, paramstring):
        _url = sys.argv[0]

        self.params = dict(parse_qsl(paramstring))

        logstring = '{0}: '.format(_url)
        for param in self.params:
            logstring += '[ {0}: {1} ] '.format(param, self.params[param])

        logging.log(logstring, level=xbmc.LOGDEBUG)

        return self.params

    def dispatch(self, handle, paramstring):
        self._log_params(paramstring)

        mode = self.params['mode'] if 'mode' in self.params else None
        url = self.params['url'] if 'url' in self.params else None
        name = self.params['name'] if 'name' in self.params else None
        action = self.params['action'] if 'action' in self.params else None

        # MAIN MENU
        if mode is None:
            self._finish(handle)
                 
        elif mode == 'trakt':  # Trakt Account Viewer
            menu.trakt_menu()
            self._finish(handle)
            
        elif mode == 'realdebrid':  # Real-Debrid Account Viewer
            menu.debrid_menu()
            self._finish(handle)

        elif mode == 'premiumize':  # Premiumize Account Viewer
            menu.premiumize_menu()
            self._finish(handle)

        elif mode == 'alldebrid':  # All-Debird Account Viewer
            menu.alldebrid_menu()
            self._finish(handle)

        elif mode == 'nondebrid':  # Non-Debrid Account Viewer
            menu.nondebrid_accounts_menu()
            self._finish(handle)

        elif mode == 'metadata':  # Metadata Account Viewer
            menu.meta_accounts_menu()
            self._finish(handle)

        elif mode == 'allaccts':  # All Account Viewer
            menu.all_accounts_menu()
            self._finish(handle)
            
        # TRAKT MANAGER
        elif mode == 'savetrakt':  # Save Trakt Data
            from resources.libs import traktit
            traktit.trakt_it('update', name)
        elif mode == 'savetrakt_acctmgr':  # Save Trakt Data via Account Manager settings menu
            from resources.libs import traktit
            traktit.trakt_it('update', name)
            xbmcgui.Dialog().notification('Account Manager', 'Trakt Backup Complete!', trakt_icon, 3000)
        elif mode == 'restoretrakt':  # Recover All Saved Trakt Data
            if xbmcvfs.exists(trakt_backup): # Skip restore if no trakt folder present in backup folder
                try:
                    path = os.listdir(trakt_backup)
                    if len(path) != 0: # Skip restore if no saved data in backup folder
                        from resources.libs import traktit
                        traktit.trakt_it_restore('restore', name)
                        xbmcgui.Dialog().notification('Account Manager', 'Trakt Data Restored!', trakt_icon, 3000)
                        xbmc.sleep(2000)
                        xbmcgui.Dialog().ok('Account Manager', 'To save changes, please close Kodi, Press OK to force close Kodi')
                        os._exit(1)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Trakt Data to Restore!', amgr_icon, 3000)
                except:
                    pass
            else:
                xbmcgui.Dialog().notification('Account Manager', 'No Trakt Data to Restore!', amgr_icon, 3000)
        elif mode == 'addontrakt':  # Clear All Addon Trakt Data
            from resources.libs import traktit
            traktit.trakt_it_revoke('wipeaddon', name)
            xbmcgui.Dialog().notification('Account Manager', 'All Add-ons Revoked!', trakt_icon, 3000)
            xbmc.sleep(2000)
            xbmcgui.Dialog().ok('Account Manager', 'To save changes, please close Kodi, Press OK to force close Kodi')
            os._exit(1)
        elif mode == 'cleartrakt':  # Clear All Saved Trakt Data
            if xbmcvfs.exists(trakt_backup): # Skip clearing data if no Trakt folder present in backup folder
                try:
                    path = os.listdir(trakt_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder           
                        from resources.libs import traktit
                        traktit.clear_saved(name)
                        xbmcgui.Dialog().notification('Account Manager', 'Trakt Data Cleared!', trakt_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Trakt Data to Clear!', amgr_icon, 3000)
                except:
                    pass
            else:
                xbmcgui.Dialog().notification('Account Manager', 'No Trakt Data to Clear!', amgr_icon, 3000)
        elif mode == 'opentraktsettings':  # Authorize Trakt
            from resources.libs import traktit
            traktit.open_settings_trakt(name)
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'updatetrakt':  # Update Saved Trakt Data
            from resources.libs import traktit
            traktit.auto_update('all')
            
        # DEBRID MANAGER RD
        elif mode == 'savedebrid_rd':  # Save Debrid Data
            from resources.libs import debridit_rd
            debridit_rd.debrid_it('update', name)
        elif mode == 'savedebrid_acctmgr_rd':  # Save Debrid Data via Account Manager settings menu
            from resources.libs import debridit_rd
            debridit_rd.debrid_it('update', name)
            xbmcgui.Dialog().notification('Account Manager', 'Real-Debrid Backup Complete!', rd_icon, 3000)
        elif mode == 'restoredebrid_rd':  # Recover All Saved Debrid Data
            if xbmcvfs.exists(rd_backup): # Skip restore if no debrid folder present in backup folder
                try:
                    path = os.listdir(rd_backup)
                    if len(path) != 0: # Skip restore if no saved data in backup folder
                        from resources.libs import debridit_rd
                        debridit_rd.debrid_it('restore', name)
                        xbmcgui.Dialog().notification('Account Manager', 'Real-Debrid Data Restored!', rd_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Real-Debrid Data to Restore!', amgr_icon, 3000)
                except:
                    pass
            else:
                xbmcgui.Dialog().notification('Account Manager', 'No Real-Debrid Data to Restore!', amgr_icon, 3000)           
        elif mode == 'addondebrid_rd':  # Clear All Addon Debrid Data
            from resources.libs import debridit_rd
            debridit_rd.debrid_it('wipeaddon', name)
            xbmcgui.Dialog().notification('Account Manager', 'All Add-ons Revoked!', rd_icon, 3000)
        elif mode == 'cleardebrid_rd':  # Clear All Saved Debrid Data
            if xbmcvfs.exists(rd_backup): # Skip clearing data if no debrid folder present in backup folder
                try:
                    path = os.listdir(rd_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder           
                        from resources.libs import debridit_rd
                        debridit_rd.clear_saved(name)
                        xbmcgui.Dialog().notification('Account Manager', 'Real-Debrid Data Cleared!', rd_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Real-Debrid Data to Clear!', rd_icon, 3000)
                except:
                    pass
            else:
                xbmcgui.Dialog().notification('Account Manager', 'No Real-Debrid Data to Clear!', amgr_icon, 3000)
        elif mode == 'opendebridsettings_rd':  # Authorize Debrid
            from resources.libs import debridit_rd
            debridit_rd.open_settings_debrid(name)
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'updatedebrid_rd':  # Update Saved Debrid Data
            from resources.libs import debridit_rd
            debridit_rd.auto_update('all')

        # DEBRID MANAGER PM
        elif mode == 'savedebrid_pm':  # Save Debrid Data
            from resources.libs import debridit_pm
            debridit_pm.debrid_it('update', name)
        elif mode == 'savedebrid_acctmgr_pm':  # Save Debrid Data via Account Manager settings menu
            from resources.libs import debridit_pm
            debridit_pm.debrid_it('update', name)
            xbmcgui.Dialog().notification('Account Manager', 'Premiumize Backup Complete!', pm_icon, 3000)
        elif mode == 'restoredebrid_pm':  # Recover All Saved Debrid Data
            if xbmcvfs.exists(pm_backup): # Skip restore if no debrid folder present in backup folder
                try:
                    path = os.listdir(pm_backup)
                    if len(path) != 0: # Skip restore if no saved data in backup folder
                        from resources.libs import debridit_pm
                        debridit_pm.debrid_it('restore', name)
                        xbmcgui.Dialog().notification('Account Manager', 'Premiumize Data Restored!', pm_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Premiumize Data to Restore!', amgr_icon, 3000)
                except:
                    pass
            else:
                xbmcgui.Dialog().notification('Account Manager', 'No Premiumize Data to Restore!', amgr_icon, 3000)
        elif mode == 'addondebrid_pm':  # Clear All Addon Debrid Data
            from resources.libs import debridit_pm
            debridit_pm.debrid_it('wipeaddon', name)
            xbmcgui.Dialog().notification('Account Manager', 'All Add-ons Revoked!', pm_icon, 3000)
        elif mode == 'cleardebrid_pm':  # Clear All Saved Debrid Data
            if xbmcvfs.exists(pm_backup): # Skip clearing data if no debrid folder present in backup folder
                try:
                    path = os.listdir(pm_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder           
                        from resources.libs import debridit_pm
                        debridit_pm.clear_saved(name)
                        xbmcgui.Dialog().notification('Account Manager', 'Premiumize Data Cleared!', pm_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Premiumize Data to Clear!', amgr_icon, 3000)
                except:
                    pass
            else:
                xbmcgui.Dialog().notification('Account Manager', 'No Premiumize Data to Clear!', amgr_icon, 3000)
        elif mode == 'opendebridsettings_pm':  # Authorize Debrid
            from resources.libs import debridit_pm
            debridit_pm.open_settings_debrid(name)
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'updatedebrid_pm':  # Update Saved Debrid Data
            from resources.libs import debridit_pm
            debridit_pm.auto_update('all')

        # DEBRID MANAGER AD
        elif mode == 'savedebrid_ad':  # Save Debrid Data
            from resources.libs import debridit_ad
            debridit_ad.debrid_it('update', name)
        elif mode == 'savedebrid_acctmgr_ad':  # Save Debrid Data via Account Manager settings menu
            from resources.libs import debridit_ad
            debridit_ad.debrid_it('update', name)
            xbmcgui.Dialog().notification('Account Manager', 'All-Debrid Backup Complete!', ad_icon, 3000)
        elif mode == 'restoredebrid_ad':  # Recover All Saved Debrid Data
            if xbmcvfs.exists(ad_backup): # Skip restore if no debrid folder present in backup folder
                try:
                    path = os.listdir(ad_backup)
                    if len(path) != 0: # Skip restore if no saved data in backup folder
                        from resources.libs import debridit_ad
                        debridit_ad.debrid_it('restore', name)
                        xbmcgui.Dialog().notification('Account Manager', 'All-Debrid Data Restored!', ad_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No All-Debrid Data to Restore!', amgr_icon, 3000)
                except:
                    pass
            else:
                xbmcgui.Dialog().notification('Account Manager', 'No All-Debrid Data to Restore!', amgr_icon, 3000)
        elif mode == 'addondebrid_ad':  # Clear All Addon Debrid Data
            from resources.libs import debridit_ad
            debridit_ad.debrid_it('wipeaddon', name)
            xbmcgui.Dialog().notification('Account Manager', 'All Add-ons Revoked!', ad_icon, 3000)
        elif mode == 'cleardebrid_ad':  # Clear All Saved Debrid Data
            if xbmcvfs.exists(ad_backup): # Skip clearing data if no debrid folder present in backup folder
                try:
                    path = os.listdir(ad_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder           
                        from resources.libs import debridit_ad
                        debridit_ad.clear_saved(name)
                        xbmcgui.Dialog().notification('Account Manager', 'All-Debrid Data Cleared!', ad_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No All-Debrid Data to Clear!', amgr_icon, 3000)
                except:
                    pass
            else:
                xbmcgui.Dialog().notification('Account Manager', 'No All-Debrid Data to Clear!', amgr_icon, 3000)
        elif mode == 'opendebridsettings_ad':  # Authorize Debrid
            from resources.libs import debridit_ad
            debridit_ad.open_settings_debrid(name)
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'updatedebrid_ad':  # Update Saved Debrid Data
            from resources.libs import debridit_ad
            debridit_ad.auto_update('all')

        #FURK/EASYNEWS/FILEPURSUIT MANAGER
        elif mode == 'save_nondebrid':  # Save Data
            from resources.libs import non_debrid_all
            non_debrid_all.debrid_it('update', name)
        elif mode == 'save_non_acctmgr':  # Save Data via Account Manager settings menu
            if str(var.chk_accountmgr_furk) != '' or str(var.chk_accountmgr_easy) != '' or str(var.chk_accountmgr_file) != '':
                from resources.libs import non_debrid_all
                non_debrid_all.debrid_it('update', name)
                xbmcgui.Dialog().notification('Account Manager', 'Backup Complete!', amgr_icon, 3000)
            else:
                xbmcgui.Dialog().notification('Account Manager', 'No Data to Backup!', amgr_icon, 3000)
        elif mode == 'restore_non':  # Recover All Saved Data
            if xbmcvfs.exists(non_backup): # Skip restore if no nondebrid folder present in backup folder
                try:
                    path = os.listdir(non_backup)
                    if len(path) != 0: # Skip restore if no saved data in backup folder
                        from resources.libs import non_debrid_all
                        non_debrid_all.debrid_it('restore', name)
                        xbmcgui.Dialog().notification('Account Manager', 'Data Restored!', amgr_icon, 3000)
                        xbmc.sleep(2000)
                        xbmcgui.Dialog().ok('Account Manager', 'To save changes, please close Kodi, Press OK to force close Kodi')
                        os._exit(1)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Data to Restore!', amgr_icon, 3000)
                except:
                    pass
            else:
                xbmcgui.Dialog().notification('Account Manager', 'No Data to Restore!', amgr_icon, 3000)
        elif mode == 'addon_non':  # Clear All Addon Debrid Data
            from resources.libs import non_debrid_all
            non_debrid_all.debrid_it('clearaddon', name)
            xbmcgui.Dialog().notification('Account Manager', 'All Add-ons Revoked!', amgr_icon, 3000)
            xbmc.sleep(2000)
            xbmcgui.Dialog().ok('Account Manager', 'To save changes, please close Kodi, Press OK to force close Kodi')
            os._exit(1)
        elif mode == 'clear_non':  # Clear All Saved Data
            if xbmcvfs.exists(non_backup): # Skip clearing data if no nondebrid folder present in backup folder
                try:
                    path = os.listdir(non_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder           
                        from resources.libs import non_debrid_all
                        non_debrid_all.clear_saved(name)
                        xbmcgui.Dialog().notification('Account Manager', 'Data Cleared!', amgr_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Data to Clear!', amgr_icon, 3000)
                except:
                    pass
            else:
                xbmcgui.Dialog().notification('Account Manager', 'No Data to Clear!', amgr_icon, 3000)
        elif mode == 'update_non':  # Update Saved Data
            from resources.libs import non_debrid_alll
            non_debrid_all.auto_update('all')

        #META DATA MANAGER
        elif mode == 'savemeta':  # Save Meta Data
            from resources.libs import metait_all
            metait_all.debrid_it('update', name)
        elif mode == 'savemeta_acctmgr':  # Save Meta Data via Account Manager settings menu
            if str(var.chk_accountmgr_fanart) != '' or str(var.chk_accountmgr_omdb) != '' or str(var.chk_accountmgr_mdb) != '' or str(var.chk_accountmgr_imdb) != '' or str(var.chk_accountmgr_tmdb) != '' or str(var.chk_accountmgr_tmdb_user) != '' or str(var.chk_accountmgr_tvdb) != '':
                from resources.libs import metait_all
                metait_all.debrid_it('update', name)
                xbmcgui.Dialog().notification('Account Manager', 'Metadata Backup Complete!', amgr_icon, 3000)
            else:
                xbmcgui.Dialog().notification('Account Manager', 'No Metadata to Backup!', amgr_icon, 3000)
        elif mode == 'restoremeta':  # Recover All Saved Meta Data
            if xbmcvfs.exists(meta_backup): # Skip restore if no meta folder present in backup folder
                try:
                    path = os.listdir(meta_backup)
                    if len(path) != 0: # Skip restore if no saved data in backup folder
                        from resources.libs import metait_all
                        metait_all.debrid_it('restore', name)
                        xbmcgui.Dialog().notification('Account Manager', 'Metadata Restored!', amgr_icon, 3000)
                        xbmc.sleep(2000)
                        xbmcgui.Dialog().ok('Account Manager', 'To save changes, please close Kodi, Press OK to force close Kodi')
                        os._exit(1)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Metadata to Restore!', amgr_icon, 3000)
                except:
                    pass
            else:
                xbmcgui.Dialog().notification('Account Manager', 'No Metadata to Restore!', amgr_icon, 3000)
        elif mode == 'addonmeta':  # Clear All Addon Debrid Data
            from resources.libs import metait_all
            metait_all.debrid_it('clearaddon', name)
            xbmcgui.Dialog().notification('Account Manager', 'All Add-ons Revoked!', amgr_icon, 3000)
            xbmc.sleep(2000)
            xbmcgui.Dialog().ok('Account Manager', 'To save changes, please close Kodi, Press OK to force close Kodi')
            os._exit(1)
        elif mode == 'clearmeta':  # Clear All Saved Meta Data
            if xbmcvfs.exists(meta_backup): # Skip clearing data if no meta folder present in backup folder
                try:
                    path = os.listdir(meta_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder           
                        from resources.libs import metait_all
                        metait_all.clear_saved(name)
                        xbmcgui.Dialog().notification('Account Manager', 'Metadata Cleared!', amgr_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Metadata to Clear!', amgr_icon, 3000)
                except:
                    pass
            else:
                xbmcgui.Dialog().notification('Account Manager', 'No Metadata to Clear!', amgr_icon, 3000)
        elif mode == 'updatemeta':  # Update Saved Meta Data
            from resources.libs import metait_all
            metait_all.auto_update('all')
            
        #REVOKE ALL DEBRID ACCOUNTS
        elif mode == 'revokeall':  # Clear Addon Data for all Debrid services
            if str(var.chk_accountmgr_tk_rd) != '' or str(var.chk_accountmgr_tk_pm) != '' or str(var.chk_accountmgr_tk_ad) != '': #Skip revoke if no Debrid accounts authorized
                from resources.libs import debridit_rd, debridit_pm, debridit_ad 
                debridit_rd.debrid_it('wipeaddon', name)
                debridit_pm.debrid_it('wipeaddon', name)
                debridit_ad.debrid_it('wipeaddon', name)
                xbmcgui.Dialog().notification('Account Manager', 'All Add-ons Revoked!', amgr_icon, 3000)
            else:
                xbmcgui.Dialog().notification('Account Manager', 'No Active Debrid Accounts!', amgr_icon, 3000) # If Accounts authorized notify user
                
        #BACKUP ALL DEBRID ACCOUNTS
        elif mode == 'backupall':  # Save Debrid Data for all Debrid services
            if str(var.chk_accountmgr_tk_rd) != '' or str(var.chk_accountmgr_tk_pm) != '' or str(var.chk_accountmgr_tk_ad) != '': # Skip backup if no Debrid accounts authorized
                from resources.libs import debridit_rd, debridit_pm, debridit_ad
                debridit_rd.debrid_it('update', name)
                debridit_pm.debrid_it('update', name)
                debridit_ad.debrid_it('update', name)
                xbmcgui.Dialog().notification('Account Manager', 'Backup Complete!', amgr_icon, 3000)
            if str(var.chk_accountmgr_tk_rd) == '': # If Account Mananger is not Authorized notify user
                xbmcgui.Dialog().notification('Account Manager', 'No Active Debrid Accounts!', amgr_icon, 3000)
            
        #RESTORE ALL DEBRID ACCOUNTS
        elif mode == 'restoreall':  # Recover All Saved Debrid Data for all Accounts
            if xbmcvfs.exists(rd_backup) or xbmcvfs.exists(pm_backup) or xbmcvfs.exists(ad_backup): # Skip restore if no debrid folder present in backup folder
                try:
                    if xbmcvfs.exists(rd_backup): # Skip restore if no backup folder exists or it's empty
                        path_rd = os.listdir(rd_backup)
                        if len(path_rd) != 0: # Skip if backup directory is empty
                            from resources.libs import debridit_rd
                            debridit_rd.debrid_it('restore', name)
                            xbmcgui.Dialog().notification('Account Manager', 'Real-Debrid Data Restored!', rd_icon, 3000)
                        else:
                            xbmcgui.Dialog().notification('Account Manager', 'No Real-Debrid Data Found!', rd_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Real-Debrid Data Found!', rd_icon, 3000)
                    if xbmcvfs.exists(pm_backup): # Skip restore if no backup folder exists or it's empty
                        path_pm = os.listdir(pm_backup)
                        if len(path_pm) != 0: # Skip if backup directory is empty
                            from resources.libs import debridit_pm
                            debridit_pm.debrid_it('restore', name)
                            xbmcgui.Dialog().notification('Account Manager', 'Premiumize Data Restored!', pm_icon, 3000)
                        else:
                            xbmcgui.Dialog().notification('Account Manager', 'No Premiumize Data Found!', pm_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Premiumize Data Found!', pm_icon, 3000)
                    if xbmcvfs.exists(ad_backup): # Skip restore if no backup folder exists or it's empty
                        path_ad = os.listdir(ad_backup)
                        if len(path_ad) != 0: # Skip if backup directory is empty
                            from resources.libs import debridit_ad
                            debridit_ad.debrid_it('restore', name)
                            xbmcgui.Dialog().notification('Account Manager', 'All-Debrid Data Restored!', ad_icon, 3000)
                        else:
                            xbmcgui.Dialog().notification('Account Manager', 'No All-Debrid Data Found!', ad_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No All-Debrid Data Found!', ad_icon, 3000)
                except:
                    pass
            else:
                xbmcgui.Dialog().notification('Account Manager', 'Restore Failed! No Saved Data Found!', amgr_icon, 3000)
                 
        #CLEAR ALL SAVED DATA FOR DEBRID ACCOUNTS
        elif mode == 'clearall':  # Clear All Saved Debrid Data
            if xbmcvfs.exists(rd_backup) or xbmcvfs.exists(pm_backup) or xbmcvfs.exists(ad_backup): # Skip clearing data if no debrid folder present in backup folder
                try:     
                    if xbmcvfs.exists(rd_backup): # Skip restore if no backup folder exists or it's empty
                        path_rd = os.listdir(rd_backup)
                        if len(path_rd) != 0: # Skip if backup directory is empty
                            from resources.libs import debridit_rd
                            debridit_rd.clear_saved(name)
                            xbmcgui.Dialog().notification('Account Manager', 'Real-Debrid Data Cleared!', rd_icon, 3000)
                        else:
                            xbmcgui.Dialog().notification('Account Manager', 'No Real-Debrid Data to Clear!', rd_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Real-Debrid Data to Clear!', rd_icon, 3000)
                    if xbmcvfs.exists(pm_backup): # Skip restore if no backup folder exists or it's empty
                        path_pm = os.listdir(pm_backup)
                        if len(path_pm) != 0: # Skip if backup directory is empty
                            from resources.libs import debridit_pm
                            debridit_pm.clear_saved(name)
                            xbmcgui.Dialog().notification('Account Manager', 'Premiumize Data Cleared!', pm_icon, 3000)
                        else:
                            xbmcgui.Dialog().notification('Account Manager', 'No Premiumize Data to Clear!', pm_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Premiumize Data to Clear!', pm_icon, 3000)
                    if xbmcvfs.exists(ad_backup): # Skip restore if no backup folder exists or it's empty
                        path_ad = os.listdir(ad_backup)
                        if len(path_ad) != 0: # Skip if backup directory is empty
                            from resources.libs import debridit_ad
                            debridit_ad.clear_saved(name)
                            xbmcgui.Dialog().notification('Account Manager', 'All-Debrid Data Cleared!', ad_icon, 3000)
                        else:
                            xbmcgui.Dialog().notification('Account Manager', 'No All-Debrid Data to Clear!', ad_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No All-Debrid Data to Clear!', ad_icon, 3000)
                except:
                    pass
            else:
                xbmcgui.Dialog().notification('Account Manager', 'No Data to Clear!', amgr_icon, 3000)
                 
        # REVOKE/WIPE CLEAN ALL ADD-ONS
        elif mode == 'wipeclean':  # Clear data and restore stock API Keys for all add-ons
            yes = dialog.yesno('Account Manager', 'WARNING! This will completely wipe all data and restore add-ons to default settings. Click proceed to continue or cancel to quit.', 'Cancel', 'Proceed') # Ask user for permission
            if yes:
                from resources.libs import traktit, metait_all, non_debrid_all, debridit_rd, debridit_pm, debridit_ad
                traktit.trakt_it_revoke('wipeaddon', name)
                metait_all.debrid_it('clearaddon', name)
                non_debrid_all.debrid_it('clearaddon', name)
                debridit_rd.debrid_it('wipeaddon', name)
                debridit_pm.debrid_it('wipeaddon', name)
                debridit_ad.debrid_it('wipeaddon', name)
                traktit.clear_saved(name)
                metait_all.clear_saved(name)
                non_debrid_all.clear_saved(name)
                debridit_rd.clear_saved(name)
                debridit_pm.clear_saved(name)
                debridit_ad.clear_saved(name)
                xbmcgui.Dialog().notification('Account Manager', 'All Data Cleared!', amgr_icon, 3000)
                xbmc.sleep(2000)
                xbmcgui.Dialog().ok('Account Manager', 'To save changes, please close Kodi, Press OK to force close Kodi')
                os._exit(1)


            
    def _finish(self, handle):
        from resources.libs.common import directory
        
        directory.set_view()
        
        xbmcplugin.setContent(handle, 'files')
        xbmcplugin.endOfDirectory(handle)                       
