# -*- coding: utf-8 -*-

'''
	Account Manager
'''

import sys
import os
import xbmcgui
import xbmcaddon
from urllib.parse import parse_qsl
from myaccts.modules import control
from myaccts.modules import var

joinPath = os.path.join
dialog = xbmcgui.Dialog()
addon = xbmcaddon.Addon
addonObject = addon('script.module.myaccts')
addonInfo = addonObject.getAddonInfo

rd_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.myaccts').getAddonInfo('path'), 'resources', 'icons'), 'realdebrid.png')
pm_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.myaccts').getAddonInfo('path'), 'resources', 'icons'), 'premiumize.png')
ad_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.myaccts').getAddonInfo('path'), 'resources', 'icons'), 'alldebrid.png')
trakt_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.myaccts').getAddonInfo('path'), 'resources', 'icons'), 'trakt.png')


def notification(title=None, message=None, icon=None, time=3000, sound=False):
	if title == 'default' or title is None: title = addonName()
	if isinstance(title, int): heading = lang(title)
	else: heading = str(title)
	if isinstance(message, int): body = lang(message)
	else: body = str(message)
	if icon is None or icon == '' or icon == 'default': icon = addonIcon()
	elif icon == 'INFO': icon = xbmcgui.NOTIFICATION_INFO
	elif icon == 'WARNING': icon = xbmcgui.NOTIFICATION_WARNING
	elif icon == 'ERROR': icon = xbmcgui.NOTIFICATION_ERROR
	dialog.notification(heading, body, icon, time, sound=sound)

def addonIcon():
	return addonInfo('icon')

def addonName():
	return addonInfo('name')

control.set_active_monitor()

params = {}
for param in sys.argv[1:]:
	param = param.split('=')
	param_dict = dict([param])
	params = dict(params, **param_dict)

action = params.get('action')
query = params.get('query')
addon_id = params.get('addon_id')

if action and not any(i in action for i in ['Auth', 'Revoke']):
	control.release_active_monitor()

if action is None:
	control.openSettings(query, "script.module.myaccts")

elif action == 'traktAcct':
	from myaccts.modules import trakt
	trakt.Trakt().account_info_to_dialog()

elif action == 'traktAuth':
	from myaccts.modules import trakt
	control.function_monitor(trakt.Trakt().auth)

elif action == 'traktSync':
	from myaccts.modules import trakt_sync
	trakt_sync.sync_all()
	
elif action == 'traktReSync':
	from myaccts.modules import trakt_sync
	trakt_sync.sync_all()
	
	if str(var.check_myaccts) != '':
                notification('Account Manager', 'Sync Complete!', icon=trakt_icon)
                xbmc.sleep(3000)
                xbmcgui.Dialog().ok('Account Manager', 'To save changes, please close Kodi, Press OK to force close Kodi')
                os._exit(1)
	if str(var.check_myaccts) == '':
                notification('Account Manager', 'Trakt NOT Authorized!', icon=trakt_icon)
        
elif action == 'traktRevoke':
	from myaccts.modules import trakt
	control.function_monitor(trakt.Trakt().revoke)

elif action == 'alldebridAcct':
	from myaccts.modules import alldebrid
	alldebrid.AllDebrid().account_info_to_dialog()

elif action == 'alldebridAuth':
	from myaccts.modules import alldebrid
	control.function_monitor(alldebrid.AllDebrid().auth)

elif action == 'alldebridSync':
	from myaccts.modules import debrid_ad
	debrid_ad.debrid_auth_ad()

elif action == 'alldebridReSync':
	from myaccts.modules import debrid_ad
	debrid_ad.debrid_auth_ad()
	
	if str(var.check_myaccts_ad) != '':
                notification('Account Manager', 'Sync Complete!', icon=ad_icon)
	if str(var.check_myaccts_ad) == '':
                notification('Account Manager', 'All-Debrid NOT Authorized!', icon=ad_icon)

elif action == 'alldebridRevoke':
	from myaccts.modules import alldebrid
	control.function_monitor(alldebrid.AllDebrid().revoke)

elif action == 'premiumizeAcct':
	from myaccts.modules import premiumize
	premiumize.Premiumize().account_info_to_dialog()

elif action == 'premiumizeAuth':
	from myaccts.modules import premiumize
	control.function_monitor(premiumize.Premiumize().auth)

elif action == 'premiumizeSync':
	from myaccts.modules import debrid_pm
	debrid_pm.debrid_auth_pm()

elif action == 'premiumizeReSync':
	from myaccts.modules import debrid_pm
	debrid_pm.debrid_auth_pm()

	if str(var.check_myaccts_pm) != '':
                notification('Account Manager', 'Sync Complete!', icon=pm_icon)
	if str(var.check_myaccts_pm) == '':
                notification('Account Manager', 'Premiumize NOT Authorized!', icon=pm_icon)
	
elif action == 'premiumizeRevoke':
	from myaccts.modules import premiumize
	control.function_monitor(premiumize.Premiumize().revoke)

elif action == 'realdebridAcct':
	from myaccts.modules import realdebrid
	realdebrid.RealDebrid().account_info_to_dialog()

elif action == 'realdebridAuth':
	from myaccts.modules import realdebrid
	control.function_monitor(realdebrid.RealDebrid().auth)

elif action == 'realdebridSync':
	from myaccts.modules import debrid_rd
	debrid_rd.debrid_auth_rd()

elif action == 'realdebridReSync':
	from myaccts.modules import debrid_rd
	debrid_rd.debrid_auth_rd()

	if str(var.check_myaccts_rd) != '':
                notification('Account Manager', 'Sync Complete!', icon=rd_icon)
	if str(var.check_myaccts_rd) == '':
                notification('Account Manager', 'Real-Debrid NOT Authorized!', icon=rd_icon)
                
elif action == 'realdebridRevoke':
	from myaccts.modules import realdebrid
	control.function_monitor(realdebrid.RealDebrid().revoke)

elif action == 'tmdbAuth':
	from myaccts.modules import tmdb
	control.function_monitor(tmdb.Auth().create_session_id)

elif action == 'tmdbRevoke':
	from myaccts.modules import tmdb
	control.function_monitor(tmdb.Auth().revoke_session_id)

elif action == 'ShowChangelog':
	from myaccts.modules import changelog
	changelog.get()

elif action == 'ShowHelp':
	from myaccts.help import help
	help.get(params.get('name'))

elif action == 'ShowOKDialog':
	control.okDialog(params.get('title', 'default'), int(params.get('message', '')))

elif action == 'tools_clearLogFile':
	from myaccts.modules import log_utils
	cleared = log_utils.clear_logFile()
	if cleared == 'canceled': pass
	elif cleared: control.notification(message='My Accounts Log File Successfully Cleared')
	else: control.notification(message='Error clearing My Accounts Log File, see kodi.log for more info')

elif action == 'tools_viewLogFile':
	from myaccts.modules import log_utils
	log_utils.view_LogFile(params.get('name'))

elif action == 'tools_uploadLogFile':
	from myaccts.modules import log_utils
	log_utils.upload_LogFile()

elif action == 'SetBackupFolder':
	from myaccts.modules import control
	control.set_backup_folder()

elif action == 'ResetBackupFolder':
	from myaccts.modules import control
	control.reset_backup_folder()
