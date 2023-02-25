import sys
import json
import xbmc
import xbmcplugin
from .utils import add_dir
from .parser import Parser
from .dropbox import DownloadFile
from uservar import buildfile
from .addonvar import addon_icon, addon_fanart, local_string, build_file, authorizerealdebrid, authorizetrakt, authorizepremiumize, authorizealldebrid, authorizelinksnappy, authorizedebridlink

handle = int(sys.argv[1])

def main_menu():
    xbmcplugin.setPluginCategory(handle, 'Main Menu')
    
    add_dir(local_string(30010),'',1,addon_icon,addon_fanart,local_string(30001),isFolder=True)  # Build Menu
    
    add_dir(local_string(30069),'',51,addon_icon,addon_fanart,local_string(30002),isFolder=True)  # Logins    
    
    add_dir(local_string(30011),'',5,addon_icon,addon_fanart,local_string(30002),isFolder=True)  # Maintenance
    
    add_dir(local_string(30012),'',4,addon_icon,addon_fanart,local_string(30003),isFolder=False)  # Fresh Start
    
    add_dir(local_string(30013),'',100,addon_icon,addon_fanart,local_string(30014),isFolder=False)  # Notification
    
    add_dir(local_string(30015),'',9,addon_icon,addon_fanart,local_string(30016),isFolder=False)  # Settings

def build_menu():
    xbmc.executebuiltin('Dialog.Close(busydialog)')
    xbmcplugin.setPluginCategory(handle, local_string(30010))
    if buildfile.startswith('https://www.dropbox.com'):
        DownloadFile(buildfile, build_file)
        try:
            builds = json.load(open(build_file,'r')).get('builds')
        except:
            xml = Parser(build_file)
            builds = json.loads(xml.get_list2())['builds']
    elif not buildfile.endswith('.xml') and not buildfile.endswith('.json'):
        add_dir(local_string(30017),'','',addon_icon,addon_fanart,local_string(30017),isFolder=False)  # Invalid Build URL
        return
    else:
        p = Parser(buildfile)
        builds = json.loads(p.get_list())['builds']
    
    for build in builds:
        name = (build.get('name', local_string(30018)))  # Unknown Name
        version = (build.get('version', '0'))
        url = (build.get('url', ''))
        icon = (build.get('icon', addon_icon))
        fanart = (build.get('fanart', addon_fanart))
        description = (build.get('description', local_string(30019)))  # No Description Available.
        preview = (build.get('preview',None))
        
        if url.endswith('.xml') or url.endswith('.json'):
            add_dir(name,url,1,icon,fanart,description,name2=name,version=version,isFolder=True)
        add_dir(name + ' ' + local_string(30020) + ' ' + version,url,3,icon,fanart,description,name2=name,version=version,isFolder=False)  # Version
        if preview is not None:
            add_dir(local_string(30021) + ' ' + name + ' ' + local_string(30020) + ' ' + version,preview,2,icon,fanart,description,name2=name,version=version,isFolder=False)  # Video Preview

def submenu_maintenance():
    xbmcplugin.setPluginCategory(handle, local_string(30022))  # Maintenance
    add_dir(local_string(30023),'',6,addon_icon,addon_fanart,local_string(30005),isFolder=False)  # Clear Packages
    add_dir(local_string(30024),'',7,addon_icon,addon_fanart,local_string(30008),isFolder=False)  # Clear Thumbnails
    add_dir(local_string(30025),'',8,addon_icon,addon_fanart,local_string(30009),isFolder=False)  # Advanced Settings
    add_dir(local_string(30064),'',11,addon_icon,addon_fanart,local_string(30064), isFolder=False)  # Edit Whitelist
    add_dir('Backup/Restore','',12,addon_icon,addon_fanart,'Backup and Restore')  # Backup Build
    add_dir('Force Close','', 18, addon_icon,addon_fanart,'Force Close Kodi')
    add_dir('View Log','', 25, addon_icon,addon_fanart,'View Log', isFolder=False)

def backup_restore():
    add_dir('Backup Build','',13,addon_icon,addon_fanart,'Backup Build', isFolder=False)  # Backup Build
    add_dir('Restore Backup','',14, addon_icon,addon_fanart,'Restore Backup')  # Restore Backup
    add_dir('Change Backups Location','',16,addon_icon,addon_fanart,'Change the location where backups will be stored and accessed.', isFolder=False)  # Backup Location
    add_dir('Reset Backups Location','',17,addon_icon,addon_fanart,'Set the backup location to its default.', isFolder=False)  # Reset Backup Location

def submenu_logins():
    xbmcplugin.setPluginCategory(handle, local_string(30069))  # Logins
    add_dir(local_string(30027),'',19,addon_icon,addon_fanart,local_string(30027))  # Authorize Trakt    
    add_dir(local_string(30026),'',10,addon_icon,addon_fanart,local_string(30026))  # Authorize Real Debrid 
    add_dir(local_string(30065),'',20,addon_icon,addon_fanart,local_string(30065))  # Authorize Premiumize
    add_dir(local_string(30066),'',23,addon_icon,addon_fanart,local_string(30066))  # Authorize All Debrid    
    add_dir(local_string(30067),'',21,addon_icon,addon_fanart,local_string(30067))  # Authorize Linksnappy
    add_dir(local_string(30068),'',22,addon_icon,addon_fanart,local_string(30068))  # Authorize Debrid Link     

        
def authorizetrakt_menu():
    xbmcplugin.setPluginCategory(handle, local_string(30027))  # Authorize Trakt
    p = Parser(authorizetrakt)
    builds = json.loads(p.get_list())['items']
    for build in builds:
        name = (build.get('name', 'Unknown'))
        url = (build.get('url', ''))
        icon = (build.get('icon', addon_icon))
        fanart = (build.get('fanart', addon_fanart))
        add_dir(name,url,24,icon,fanart,name,name2=name,version='' ,isFolder=False)        
        
def authorizerealdebrid_menu():
    xbmcplugin.setPluginCategory(handle, local_string(30026))  # Authorize Real Debrid
    p = Parser(authorizerealdebrid)
    builds = json.loads(p.get_list())['items']
    for build in builds:
        name = (build.get('name', 'Unknown'))
        url = (build.get('url', ''))
        icon = (build.get('icon', addon_icon))
        fanart = (build.get('fanart', addon_fanart))
        add_dir(name,url,24,icon,fanart,name,name2=name,version='' ,isFolder=False)

def authorizepremiumize_menu():
    xbmcplugin.setPluginCategory(handle, local_string(30065))  # Authorize Premiumize
    p = Parser(authorizepremiumize)
    builds = json.loads(p.get_list())['items']
    for build in builds:
        name = (build.get('name', 'Unknown'))
        url = (build.get('url', ''))
        icon = (build.get('icon', addon_icon))
        fanart = (build.get('fanart', addon_fanart))
        add_dir(name,url,24,icon,fanart,name,name2=name,version='' ,isFolder=False) 

def authorizelinksnappy_menu():
    xbmcplugin.setPluginCategory(handle, local_string(30067))  # Authorize Link Snappy
    p = Parser(authorizelinksnappy)
    builds = json.loads(p.get_list())['items']
    for build in builds:
        name = (build.get('name', 'Unknown'))
        url = (build.get('url', ''))
        icon = (build.get('icon', addon_icon))
        fanart = (build.get('fanart', addon_fanart))
        add_dir(name,url,24,icon,fanart,name,name2=name,version='' ,isFolder=False)

def authorizedebridlink_menu():
    xbmcplugin.setPluginCategory(handle, local_string(30068))  # Authorize Debrid Link
    p = Parser(authorizedebridlink)
    builds = json.loads(p.get_list())['items']
    for build in builds:
        name = (build.get('name', 'Unknown'))
        url = (build.get('url', ''))
        icon = (build.get('icon', addon_icon))
        fanart = (build.get('fanart', addon_fanart))
        add_dir(name,url,24,icon,fanart,name,name2=name,version='' ,isFolder=False)  

def authorizealldebrid_menu():
    xbmcplugin.setPluginCategory(handle, local_string(30066))  # Authorize Debrid Link
    p = Parser(authorizealldebrid)
    builds = json.loads(p.get_list())['items']
    for build in builds:
        name = (build.get('name', 'Unknown'))
        url = (build.get('url', ''))
        icon = (build.get('icon', addon_icon))
        fanart = (build.get('fanart', addon_fanart))
        add_dir(name,url,24,icon,fanart,name,name2=name,version='' ,isFolder=False)