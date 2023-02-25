################################################################################
#      Copyright (C) 2015 Surfacingx                                           #
#                                                                              #
#  This Program is free software; you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation; either version 2, or (at your option)         #
#  any later version.                                                          #
#                                                                              #
#  This Program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with XBMC; see the file COPYING.  If not, write to                    #
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.       #
#  http://www.gnu.org/copyleft/gpl.html                                        #
################################################################################

import glob, os, sys
import shutil
import re
import uservar
import fnmatch
import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs

from datetime import date, datetime, timedelta
# Py2
try:
    from urlparse import urljoin
    from urllib import quote_plus, unquote_plus
    import urllib2
    from HTMLParser import HTMLParser

# Py3:
except ImportError:
    import urllib.request as urllib2
    from urllib.parse import urljoin, quote_plus, unquote_plus

from resources.libs import extract, downloader, notify, debridit, traktit, loginit, skinSwitch, uploadLog, yt, speedtest, wizard as wiz

KODIV            = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
if 18 <= KODIV < 19:
    from resources.libs import zfile as zipfile #FTG mod for Kodi 18
else:
    import zipfile
transPath  = xbmc.translatePath if KODIV < 19 else xbmcvfs.translatePath
legalFilename = xbmc.makeLegalFilename if KODIV < 19 else xbmcvfs.makeLegalFilename
LOGNOTICE = xbmc.LOGNOTICE if KODIV < 19 else xbmc.LOGINFO
ADDON_ID         = uservar.ADDON_ID
ADDONTITLE       = uservar.ADDONTITLE
ADDON            = wiz.addonId(ADDON_ID)
VERSION          = wiz.addonInfo(ADDON_ID,'version')
ADDONPATH        = wiz.addonInfo(ADDON_ID, 'path')
DIALOG           = xbmcgui.Dialog()
DP               = xbmcgui.DialogProgress()
HOME             = transPath('special://home/')
LOG              = transPath('special://logpath/')
PROFILE          = transPath('special://profile/')
TEMPDIR          = transPath('special://temp')
ADDONS           = os.path.join(HOME,      'addons')
USERDATA         = os.path.join(HOME,      'userdata')
PLUGIN           = os.path.join(ADDONS,    ADDON_ID)
PACKAGES         = os.path.join(ADDONS,    'packages')
ADDOND           = os.path.join(USERDATA,  'addon_data')
ADDONDATA        = os.path.join(USERDATA,  'addon_data', ADDON_ID)
ADVANCED         = os.path.join(USERDATA,  'advancedsettings.xml')
SOURCES          = os.path.join(USERDATA,  'sources.xml')
FAVOURITES       = os.path.join(USERDATA,  'favourites.xml')
PROFILES         = os.path.join(USERDATA,  'profiles.xml')
GUISETTINGS      = os.path.join(USERDATA,  'guisettings.xml')
THUMBS           = os.path.join(USERDATA,  'Thumbnails')
DATABASE         = os.path.join(USERDATA,  'Database')
FANART           = os.path.join(PLUGIN,    'fanart.jpg')
ICON             = os.path.join(PLUGIN,    'icon.png')
ART              = os.path.join(PLUGIN,    'resources', 'art')
WIZLOG           = os.path.join(ADDONDATA, 'wizard.log')
SPEEDTESTFOLD    = os.path.join(ADDONDATA, 'SpeedTest')
ARCHIVE_CACHE    = os.path.join(TEMPDIR,   'archive_cache')
SKIN             = xbmc.getSkinDir()
BUILDNAME        = wiz.getS('buildname')
DEFAULTSKIN      = wiz.getS('defaultskin')
DEFAULTNAME      = wiz.getS('defaultskinname')
DEFAULTIGNORE    = wiz.getS('defaultskinignore')
BUILDVERSION     = wiz.getS('buildversion')
BUILDTHEME       = wiz.getS('buildtheme')
BUILDLATEST      = wiz.getS('latestversion')
SHOW15           = wiz.getS('show15')
SHOW16           = wiz.getS('show16')
SHOW17           = wiz.getS('show17')
SHOW18           = wiz.getS('show18')
SHOW19           = wiz.getS('show19')
SHOWADULT        = wiz.getS('adult')
SHOWMAINT        = wiz.getS('showmaint')
AUTOCLEANUP      = wiz.getS('autoclean')
AUTOCACHE        = wiz.getS('clearcache')
AUTOPACKAGES     = wiz.getS('clearpackages')
AUTOTHUMBS       = wiz.getS('clearthumbs')
AUTOFEQ          = wiz.getS('autocleanfeq')
AUTONEXTRUN      = wiz.getS('nextautocleanup')
INCLUDEVIDEO     = wiz.getS('includevideo')
INCLUDEALL       = wiz.getS('includeall')
INCLUDETHECREW    = wiz.getS('includethecrew')
INCLUDEGAIA     = wiz.getS('includegaia')
INCLUDESEREN     = wiz.getS('includeseren')
SEPERATE         = wiz.getS('seperate')
NOTIFY           = wiz.getS('notify')
NOTEID           = wiz.getS('noteid')
NOTEDISMISS      = wiz.getS('notedismiss')
TRAKTSAVE        = wiz.getS('traktlastsave')
REALSAVE         = wiz.getS('debridlastsave')
LOGINSAVE        = wiz.getS('loginlastsave')
KEEPFAVS         = wiz.getS('keepfavourites')
KEEPSOURCES      = wiz.getS('keepsources')
KEEPPROFILES     = wiz.getS('keepprofiles')
KEEPPLAYERCORE     = wiz.getS('keepplayercore')
KEEPADVANCED     = wiz.getS('keepadvanced')
KEEPREPOS        = wiz.getS('keeprepos')
KEEPSUPER        = wiz.getS('keepsuper')
KEEPWHITELIST    = wiz.getS('keepwhitelist')
KEEPTRAKT        = wiz.getS('keeptrakt')
KEEPREAL         = wiz.getS('keepdebrid')
KEEPLOGIN        = wiz.getS('keeplogin')
DEVELOPER        = wiz.getS('developer')
THIRDPARTY       = wiz.getS('enable3rd')
THIRD1NAME       = wiz.getS('wizard1name')
THIRD1URL        = wiz.getS('wizard1url')
THIRD2NAME       = wiz.getS('wizard2name')
THIRD2URL        = wiz.getS('wizard2url')
THIRD3NAME       = wiz.getS('wizard3name')
THIRD3URL        = wiz.getS('wizard3url')
BACKUPLOCATION   = ADDON.getSetting('path') if not ADDON.getSetting('path') == '' else 'special://home/'
BACKUPROMS       = wiz.getS('rompath')
MYBUILDS         = os.path.join(BACKUPLOCATION, 'My_Builds', '')
AUTOFEQ          = int(float(AUTOFEQ)) if AUTOFEQ.isdigit() else 0
TODAY            = date.today()
TOMORROW         = TODAY + timedelta(days=1)
THREEDAYS        = TODAY + timedelta(days=3)

                                                                      
              
                                               
     
                  

MCNAME           = wiz.mediaCenter()
EXCLUDES         = uservar.EXCLUDES
CACHETEXT        = uservar.CACHETEXT
CACHEAGE         = uservar.CACHEAGE if str(uservar.CACHEAGE).isdigit() else 30
BUILDFILE        = uservar.BUILDFILE
APKFILE          = uservar.APKFILE
YOUTUBETITLE     = uservar.YOUTUBETITLE
YOUTUBEFILE      = uservar.YOUTUBEFILE
ADDONFILE        = uservar.ADDONFILE
ADVANCEDFILE     = uservar.ADVANCEDFILE
UPDATECHECK      = uservar.UPDATECHECK if str(uservar.UPDATECHECK).isdigit() else 1
NEXTCHECK        = TODAY + timedelta(days=UPDATECHECK)
NOTIFICATION     = uservar.NOTIFICATION
ENABLE           = uservar.ENABLE
HEADERMESSAGE    = uservar.HEADERMESSAGE
AUTOUPDATE       = uservar.AUTOUPDATE
BUILDERNAME      = uservar.BUILDERNAME
WIZARDFILE       = uservar.WIZARDFILE
HIDECONTACT      = uservar.HIDECONTACT
CONTACT          = uservar.CONTACT
CONTACTICON      = uservar.CONTACTICON if not uservar.CONTACTICON == 'http://' else ICON
CONTACTFANART    = uservar.CONTACTFANART if not uservar.CONTACTFANART == 'http://' else FANART
HIDESPACERS      = uservar.HIDESPACERS
COLOR1           = uservar.COLOR1
COLOR2           = uservar.COLOR2
THEME1           = uservar.THEME1
THEME2           = uservar.THEME2
THEME3           = uservar.THEME3
THEME4           = uservar.THEME4
THEME5           = uservar.THEME5
ICONBUILDS       = uservar.ICONBUILDS if not uservar.ICONBUILDS == 'http://' else ICON
ICONMAINT        = uservar.ICONMAINT if not uservar.ICONMAINT == 'http://' else ICON
ICONAPK          = uservar.ICONAPK if not uservar.ICONAPK == 'http://' else ICON
ICONADDONS       = uservar.ICONADDONS if not uservar.ICONADDONS == 'http://' else ICON
ICONYOUTUBE      = uservar.ICONYOUTUBE if not uservar.ICONYOUTUBE == 'http://' else ICON
ICONSAVE         = uservar.ICONSAVE if not uservar.ICONSAVE == 'http://' else ICON
ICONTRAKT        = uservar.ICONTRAKT if not uservar.ICONTRAKT == 'http://' else ICON
ICONREAL         = uservar.ICONREAL if not uservar.ICONREAL == 'http://' else ICON
ICONLOGIN        = uservar.ICONLOGIN if not uservar.ICONLOGIN == 'http://' else ICON
ICONCONTACT      = uservar.ICONCONTACT if not uservar.ICONCONTACT == 'http://' else ICON
ICONSETTINGS     = uservar.ICONSETTINGS if not uservar.ICONSETTINGS == 'http://' else ICON
LOGFILES         = wiz.LOGFILES
TRAKTID          = traktit.TRAKTID
DEBRIDID         = debridit.DEBRIDID
LOGINID          = loginit.LOGINID
MODURL           = 'http://tribeca.tvaddons.ag/tools/maintenance/modules/'
MODURL2          = 'http://mirrors.kodi.tv/addons/jarvis/'
INSTALLMETHODS   = ['Always Ask', 'Reload Profile', 'Force Close']
DEFAULTPLUGINS   = ['metadata.album.universal', 'metadata.artists.universal', 'metadata.common.fanart.tv', 'metadata.common.imdb.com', 'metadata.common.musicbrainz.org', 'metadata.themoviedb.org', 'metadata.tvdb.com', 'service.xbmc.versioncheck']
try:
    INSTALLMETHOD    = int(float(wiz.getS('installmethod')))
except:
    INSTALLMETHOD    = 0

###########################
###### Menu Items   #######
###########################
#addDir (display,mode,name=None,url=None,menu=None,overwrite=True,fanart=FANART,icon=ICON, themeit=None)
#addFile(display,mode,name=None,url=None,menu=None,overwrite=True,fanart=FANART,icon=ICON, themeit=None)

def index():

    addDir ('Maintenance', 'maint',    icon=ICONMAINT,    themeit=THEME1)
    setView('files', 'viewType')



def maintMenu(view=None):
    on = '[B][COLOR springgreen]ON[/COLOR][/B]'; off = '[B][COLOR red]OFF[/COLOR][/B]'
    autoclean   = 'true' if AUTOCLEANUP    == 'true' else 'false'
    cache       = 'true' if AUTOCACHE      == 'true' else 'false'
    packages    = 'true' if AUTOPACKAGES   == 'true' else 'false'
    thumbs      = 'true' if AUTOTHUMBS     == 'true' else 'false'
    maint       = 'true' if SHOWMAINT      == 'true' else 'false'
    includevid  = 'true' if INCLUDEVIDEO   == 'true' else 'false'
    includeall  = 'true' if INCLUDEALL     == 'true' else 'false'
    thirdparty  = 'true' if THIRDPARTY     == 'true' else 'false'
    if includeall == 'true':
        includeseren = 'true'
        includegaia = 'true'
        includethecrew = 'true'
    else:
        includethecrew = 'true' if INCLUDETHECREW     == 'true' else 'false'
        includegaia = 'true' if INCLUDEGAIA   == 'true' else 'false'
        includeseren = 'true' if INCLUDESEREN   == 'true' else 'false'
    sizepack   = wiz.getSize(PACKAGES)
    sizethumb  = wiz.getSize(THUMBS)
    archive    = wiz.getSize(ARCHIVE_CACHE)
    sizecache  = (wiz.getCacheSize())-archive
    totalsize  = sizepack+sizethumb+sizecache
    feq        = ['Always', 'Daily', '3 Days', 'Weekly']
    if view == "clean" or SHOWMAINT == 'true':
        addFile('Total Clean Up: [COLOR springgreen][B]%s[/B][/COLOR]' % wiz.convertSize(totalsize),    'fullclean',       icon=ICONMAINT, themeit=THEME3)
        addFile('Clear Cache: [COLOR springgreen][B]%s[/B][/COLOR]' % wiz.convertSize(sizecache),       'clearcache',      icon=ICONMAINT, themeit=THEME3)
        if (xbmc.getCondVisibility('System.HasAddon(script.module.urlresolver)') or xbmc.getCondVisibility('System.HasAddon(script.module.resolveurl)')): addFile('Clear Resolver Function Caches',       'clearfunctioncache',      icon=ICONMAINT, themeit=THEME3)
        addFile('Clear Packages: [COLOR springgreen][B]%s[/B][/COLOR]' % wiz.convertSize(sizepack),     'clearpackages',   icon=ICONMAINT, themeit=THEME3)
        addFile('Clear Thumbnails: [COLOR springgreen][B]%s[/B][/COLOR]' % wiz.convertSize(sizethumb),  'clearthumb',      icon=ICONMAINT, themeit=THEME3)
        if os.path.exists(ARCHIVE_CACHE): addFile('Clear Archive_Cache: [COLOR springgreen][B]%s[/B][/COLOR]' % wiz.convertSize(archive), 'cleararchive',    icon=ICONMAINT, themeit=THEME3)
        addFile('Clear Old Thumbnails', 'oldThumbs',      icon=ICONMAINT, themeit=THEME3)
        addFile('Clear Crash Logs',               'clearcrash',      icon=ICONMAINT, themeit=THEME3)
        addFile('Purge Databases',                'purgedb',         icon=ICONMAINT, themeit=THEME3)
        addFile('Fresh Start',                    'freshstart',      icon=ICONMAINT, themeit=THEME3)
    if view == "addon" or SHOWMAINT == 'true':
        addFile('Remove Addons',                  'removeaddons',    icon=ICONMAINT, themeit=THEME3)
        addDir ('Remove Addon Data',              'removeaddondata', icon=ICONMAINT, themeit=THEME3)
        addDir ('Enable/Disable Addons',          'enableaddons',    icon=ICONMAINT, themeit=THEME3)
        addFile('Enable/Disable Adult Addons',    'toggleadult',     icon=ICONMAINT, themeit=THEME3)
        addFile('Force Update Addons',            'forceupdate',     icon=ICONMAINT, themeit=THEME3)
        addFile('Hide Passwords On Keyboard Entry',   'hidepassword',   icon=ICONMAINT, themeit=THEME3)
        addFile('Unhide Passwords On Keyboard Entry', 'unhidepassword', icon=ICONMAINT, themeit=THEME3)
    if view == "misc" or SHOWMAINT == 'true':
        addFile('Kodi 17 Fix',                    'kodi17fix',       icon=ICONMAINT, themeit=THEME3)
        addFile('Kodi 19 Fix',                    'kodi19fix',       icon=ICONMAINT, themeit=THEME3)
        addFile('Restore Manually Installed Repos Updates',     'restorautoupdt',  icon=ICONMAINT, themeit=THEME3)
        addDir ('Speed Test',                     'speedtest',       icon=ICONMAINT, themeit=THEME3)
        addFile('Enable Unknown Sources',         'unknownsources',  icon=ICONMAINT, themeit=THEME3)
        addFile('Reload Skin',                    'forceskin',       icon=ICONMAINT, themeit=THEME3)
        addFile('Reload Profile',                 'forceprofile',    icon=ICONMAINT, themeit=THEME3)
        addFile('Force Close Kodi',               'forceclose',      icon=ICONMAINT, themeit=THEME3)
        addFile('Upload Log File', 'uploadlog',       icon=ICONMAINT, themeit=THEME3)
        addFile('View Errors in Log: %s' % (errorsfound), 'viewerrorlog', icon=ICONMAINT, themeit=THEME3)
        if errors > 0: addFile('View Last Error In Log', 'viewerrorlast', icon=ICONMAINT, themeit=THEME3)
        addFile('View Log File',                  'viewlog',         icon=ICONMAINT, themeit=THEME3)
        addFile('View Wizard Log File',           'viewwizlog',      icon=ICONMAINT, themeit=THEME3)
        addFile('Clear Wizard Log File%s' % wizlogsize,'clearwizlog',     icon=ICONMAINT, themeit=THEME3)
    if view == "backup" or SHOWMAINT == 'true':
        addFile('Clean Up Back Up Folder',        'clearbackup',     icon=ICONMAINT,   themeit=THEME3)
        addFile('Back Up Location: [COLOR %s]%s[/COLOR]' % (COLOR2, MYBUILDS),'settings', 'Maintenance', icon=ICONMAINT, themeit=THEME3)
        #addFile('Extract a ZipFile',              'extractazip',     icon=ICONMAINT,   themeit=THEME3)
        addFile('[Back Up]: Build',               'backupbuild',     icon=ICONMAINT,   themeit=THEME3)
        addFile('[Back Up]: GuiFix',              'backupgui',       icon=ICONMAINT,   themeit=THEME3)
        addFile('[Back Up]: Theme',               'backuptheme',     icon=ICONMAINT,   themeit=THEME3)
        addFile('[Back Up]: Addon Pack',          'backupaddonpack', icon=ICONMAINT,   themeit=THEME3)
        addFile('[Back Up]: Addon_data',          'backupaddon',     icon=ICONMAINT,   themeit=THEME3)
        addFile('[Restore]: Local Build',         'restorezip',      icon=ICONMAINT,   themeit=THEME3)
        addFile('[Restore]: Local GuiFix',        'restoregui',      icon=ICONMAINT,   themeit=THEME3)
        addFile('[Restore]: Local Addon_data',    'restoreaddon',    icon=ICONMAINT,   themeit=THEME3)
        addFile('[Restore]: External Build',      'restoreextzip',   icon=ICONMAINT,   themeit=THEME3)
        addFile('[Restore]: External GuiFix',     'restoreextgui',   icon=ICONMAINT,   themeit=THEME3)
        addFile('[Restore]: External Addon_data', 'restoreextaddon', icon=ICONMAINT,   themeit=THEME3)
    addDir ('[B]Diggz Advanced Settings[/B]',       'maint', 'tweaks', icon=ICONMAINT, themeit=THEME1)
    if view == "tweaks" or SHOWMAINT == 'true':
        if not ADVANCEDFILE == 'http://' and not ADVANCEDFILE == '':
            addDir ('Advanced Settings',            'advancedsetting',  icon=ICONMAINT, themeit=THEME3)
        else:
            if os.path.exists(ADVANCED):
                addFile('View Current AdvancedSettings.xml',   'currentsettings', icon=ICONMAINT, themeit=THEME3)
                addFile('Remove Current AdvancedSettings.xml', 'removeadvanced',  icon=ICONMAINT, themeit=THEME3)
            addFile('Quick Configure AdvancedSettings.xml',    'autoadvanced',    icon=ICONMAINT, themeit=THEME3)


#########################################NET TOOLS#############################################

def advancedWindow(url=None):
    if not ADVANCEDFILE == 'http://':
        if url == None:
            TEMPADVANCEDFILE = wiz.textCache(uservar.ADVANCEDFILE)
            if TEMPADVANCEDFILE == False: ADVANCEDWORKING  = wiz.workingURL(uservar.ADVANCEDFILE)
        else:
            TEMPADVANCEDFILE = wiz.textCache(url)
            if TEMPADVANCEDFILE == False: ADVANCEDWORKING  = wiz.workingURL(url)
        addFile('Quick Configure AdvancedSettings.xml', 'autoadvanced', icon=ICONMAINT, themeit=THEME3)
        if os.path.exists(ADVANCED):
            addFile('View Current AdvancedSettings.xml', 'currentsettings', icon=ICONMAINT, themeit=THEME3)
            addFile('Remove Current AdvancedSettings.xml', 'removeadvanced',  icon=ICONMAINT, themeit=THEME3)
        if not TEMPADVANCEDFILE == False:
            if HIDESPACERS == 'No': addFile(wiz.sep(), '', icon=ICONMAINT, themeit=THEME3)
            link = TEMPADVANCEDFILE.decode('utf-8').replace('\n','').replace('\r','').replace('\t','')
            match = re.compile('name="(.+?)".+?ection="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
            if len(match) > 0:
                for name, section, url, icon, fanart, description in match:
                    if section.lower() == "yes":
                        addDir ("[B]%s[/B]" % name, 'advancedsetting', url, description=description, icon=icon, fanart=fanart, themeit=THEME3)
                    else:
                        addFile(name, 'writeadvanced', name, url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
            else: wiz.log("[Advanced Settings] ERROR: Invalid Format.")
        else: wiz.log("[Advanced Settings] URL not working: %s" % ADVANCEDWORKING)
    else: wiz.log("[Advanced Settings] not Enabled")

def writeAdvanced(name, url):
    ADVANCEDWORKING = wiz.workingURL(url)
    if ADVANCEDWORKING == True:
        if os.path.exists(ADVANCED): choice = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to overwrite your current Advanced Settings with [COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, name), yeslabel="[B][COLOR springgreen]Overwrite[/COLOR][/B]", nolabel="[B][COLOR red]Cancel[/COLOR][/B]")
        else: choice = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to download and install [COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, name), yeslabel="[B][COLOR springgreen]Install[/COLOR][/B]", nolabel="[B][COLOR red]Cancel[/COLOR][/B]")

        if choice == 1:
            file = wiz.openURL(url)
            f = xbmcvfs.File(ADVANCED, 'w');
            f.write(file)
            f.close()
            DIALOG.ok(ADDONTITLE, '[COLOR %s]AdvancedSettings.xml file has been successfully written.  Once you click okay it will force close kodi.[/COLOR]' % COLOR2)
            wiz.killxbmc(True)
        else: wiz.log("[Advanced Settings] install canceled"); wiz.LogNotify('[COLOR %s]%s[/COLOR]' % (COLOR1, ADDONTITLE), "[COLOR %s]Write Cancelled![/COLOR]" % COLOR2); return
    else: wiz.log("[Advanced Settings] URL not working: %s" % ADVANCEDWORKING); wiz.LogNotify('[COLOR %s]%s[/COLOR]' % (COLOR1, ADDONTITLE), "[COLOR %s]URL Not Working[/COLOR]" % COLOR2)

def viewAdvanced():
    f = xbmcvfs.File(ADVANCED)
    a = f.read().replace('\t', '    ')
    wiz.TextBox(ADDONTITLE, a)
    f.close()

def removeAdvanced():
    if os.path.exists(ADVANCED):
        wiz.removeFile(ADVANCED)
    else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]AdvancedSettings.xml not found[/COLOR]")

def showAutoAdvanced():
    notify.autoConfig()



ACTION_PREVIOUS_MENU            =  10   ## ESC action
ACTION_NAV_BACK                 =  92   ## Backspace action
ACTION_MOVE_LEFT                =   1   ## Left arrow key
ACTION_MOVE_RIGHT               =   2   ## Right arrow key
ACTION_MOVE_UP                  =   3   ## Up arrow key
ACTION_MOVE_DOWN                =   4   ## Down arrow key
ACTION_MOUSE_WHEEL_UP           = 104   ## Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN         = 105   ## Mouse wheel down
ACTION_MOVE_MOUSE               = 107   ## Down arrow key
ACTION_SELECT_ITEM              =   7   ## Number Pad Enter
ACTION_BACKSPACE                = 110   ## ?
ACTION_MOUSE_LEFT_CLICK         = 100
ACTION_MOUSE_LONG_CLICK         = 108

def LogViewer(default=None):
    class LogViewer(xbmcgui.WindowXMLDialog):
        def __init__(self,*args,**kwargs):
            self.default = kwargs['default']

        def onInit(self):
            self.title      = 101
            self.msg        = 102
            self.scrollbar  = 103
            self.upload     = 201
            self.kodi       = 202
            self.kodiold    = 203
            self.wizard     = 204
            self.okbutton   = 205
            f = open(self.default, "rb")
            self.logmsg = f.read().decode('utf-8', errors="ignore")
            f.close()
            self.titlemsg = "%s: %s" % (ADDONTITLE, self.default.replace(LOG, '').replace(ADDONDATA, ''))
            self.showdialog()

        def showdialog(self):
            self.getControl(self.title).setLabel(self.titlemsg)
            self.getControl(self.msg).setText(wiz.highlightText(self.logmsg))
            self.setFocusId(self.scrollbar)

        def onClick(self, controlId):
            if   controlId == self.okbutton: self.close()
            elif controlId == self.upload: self.close(); uploadLog.Main()
            elif controlId == self.kodi:
                newmsg = wiz.Grab_Log(False)
                filename = wiz.Grab_Log(True)
                if newmsg == False:
                    self.titlemsg = "%s: View Log Error" % ADDONTITLE
                    self.getControl(self.msg).setText("Log File Does Not Exists!")
                else:
                    self.titlemsg = "%s: %s" % (ADDONTITLE, filename.replace(LOG, ''))
                    self.getControl(self.title).setLabel(self.titlemsg)
                    self.getControl(self.msg).setText(wiz.highlightText(newmsg))
                    self.setFocusId(self.scrollbar)
            elif controlId == self.kodiold:
                newmsg = wiz.Grab_Log(False, True)
                filename = wiz.Grab_Log(True, True)
                if newmsg == False:
                    self.titlemsg = "%s: View Log Error" % ADDONTITLE
                    self.getControl(self.msg).setText("Log File Does Not Exists!")
                else:
                    self.titlemsg = "%s: %s" % (ADDONTITLE, filename.replace(LOG, ''))
                    self.getControl(self.title).setLabel(self.titlemsg)
                    self.getControl(self.msg).setText(wiz.highlightText(newmsg))
                    self.setFocusId(self.scrollbar)
            elif controlId == self.wizard:
                newmsg = wiz.Grab_Log(False, False, True)
                filename = wiz.Grab_Log(True, False, True)
                if newmsg == False:
                    self.titlemsg = "%s: View Log Error" % ADDONTITLE
                    self.getControl(self.msg).setText("Log File Does Not Exists!")
                else:
                    self.titlemsg = "%s: %s" % (ADDONTITLE, filename.replace(ADDONDATA, ''))
                    self.getControl(self.title).setLabel(self.titlemsg)
                    self.getControl(self.msg).setText(wiz.highlightText(newmsg))
                    self.setFocusId(self.scrollbar)

        def onAction(self, action):
            if   action == ACTION_PREVIOUS_MENU: self.close()
            elif action == ACTION_NAV_BACK: self.close()
    if default == None: default = wiz.Grab_Log(True)
    lv = LogViewer( "LogViewer.xml" , ADDON.getAddonInfo('path'), 'DefaultSkin', default=default)
    lv.doModal()
    del lv

def removeAddon(addon, name, over=False):
    if not over == False:
        yes = 1
    else:
        yes = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Are you sure you want to delete the addon:'% COLOR2, 'Name: [COLOR %s]%s[/COLOR]' % (COLOR1, name), 'ID: [COLOR %s]%s[/COLOR][/COLOR]' % (COLOR1, addon), yeslabel='[B][COLOR springgreen]Remove Addon[/COLOR][/B]', nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]')
    if yes == 1:
        folder = os.path.join(ADDONS, addon)
        wiz.log("Removing Addon %s" % addon)
        wiz.cleanHouse(folder)
        xbmc.sleep(200)
        try: shutil.rmtree(folder)
        except Exception as e: wiz.log("Error removing %s" % addon, LOGNOTICE)
        removeAddonData(addon, name, over)
    if over == False:
        wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]%s Removed[/COLOR]" % (COLOR2, name))

def removeAddonData(addon, name=None, over=False):
    if addon == 'all':
        if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to remove [COLOR %s]ALL[/COLOR] addon data stored in you Userdata folder?[/COLOR]' % (COLOR2, COLOR1), yeslabel='[B][COLOR springgreen]Remove Data[/COLOR][/B]', nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]'):
            wiz.cleanHouse(ADDOND)
        else: wiz.LogNotify('[COLOR %s]Remove Addon Data[/COLOR]' % COLOR1, '[COLOR %s]Cancelled![/COLOR]' % COLOR2)
    elif addon == 'uninstalled':
        if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to remove [COLOR %s]ALL[/COLOR] addon data stored in you Userdata folder for uninstalled addons?[/COLOR]' % (COLOR2, COLOR1), yeslabel='[B][COLOR springgreen]Remove Data[/COLOR][/B]', nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]'):
            total = 0
            for folder in glob.glob(os.path.join(ADDOND, '*')):
                foldername = folder.replace(ADDOND, '').replace('\\', '').replace('/', '')
                if foldername in EXCLUDES: pass
                elif os.path.exists(os.path.join(ADDONS, foldername)): pass
                else: wiz.cleanHouse(folder); total += 1; wiz.log(folder); shutil.rmtree(folder)
            wiz.LogNotify('[COLOR %s]Clean up Uninstalled[/COLOR]' % COLOR1, '[COLOR %s]%s Folders(s) Removed[/COLOR]' % (COLOR2, total))
        else: wiz.LogNotify('[COLOR %s]Remove Addon Data[/COLOR]' % COLOR1, '[COLOR %s]Cancelled![/COLOR]' % COLOR2)
    elif addon == 'empty':
        if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to remove [COLOR %s]ALL[/COLOR] empty addon data folders in you Userdata folder?[/COLOR]' % (COLOR2, COLOR1), yeslabel='[B][COLOR springgreen]Remove Data[/COLOR][/B]', nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]'):
            total = wiz.emptyfolder(ADDOND)
            wiz.LogNotify('[COLOR %s]Remove Empty Folders[/COLOR]' % COLOR1, '[COLOR %s]%s Folders(s) Removed[/COLOR]' % (COLOR2, total))
        else: wiz.LogNotify('[COLOR %s]Remove Empty Folders[/COLOR]' % COLOR1, '[COLOR %s]Cancelled![/COLOR]' % COLOR2)
    else:
        addon_data = os.path.join(USERDATA, 'addon_data', addon)
        if addon in EXCLUDES:
            wiz.LogNotify("[COLOR %s]Protected Plugin[/COLOR]" % COLOR1, "[COLOR %s]Not allowed to remove Addon_Data[/COLOR]" % COLOR2)
        elif os.path.exists(addon_data):
            if DIALOG.yesno(ADDONTITLE, ('[COLOR %s]Would you also like to remove the addon data for:[/COLOR]' % COLOR2)+"[CR]"+('[COLOR %s]%s[/COLOR]' % (COLOR1, addon)), yeslabel='[B][COLOR springgreen]Remove Data[/COLOR][/B]', nolabel='[B][COLOR red]Don\'t Remove[/COLOR][/B]'):
                wiz.cleanHouse(addon_data)
                try:
                    shutil.rmtree(addon_data)
                except:
                    wiz.log("Error deleting: %s" % addon_data)
            else:
                wiz.log('Addon data for %s was not removed' % addon)
    wiz.refresh()

def restoreit(type):
    if type == 'build':
        x = freshStart('restore')
        if x == False: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Local Restore Cancelled[/COLOR]" % COLOR2); return
    if not wiz.currSkin() in ['skin.confluence', 'skin.estuary']:
        wiz.skinToDefault('Restore Backup')
    wiz.restoreLocal(type)

def restoreextit(type):
    if type == 'build':
        x = freshStart('restore')
        if x == False: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]External Restore Cancelled[/COLOR]" % COLOR2); return
    wiz.restoreExternal(type)

def buildInfo(name):
    if wiz.workingURL(BUILDFILE) == True:
        if wiz.checkBuild(name, 'url'):
            name, version, url, minor, gui, kodi, theme, icon, fanart, preview, adult, info, description = wiz.checkBuild(name, 'all')
            adult = 'Yes' if adult.lower() == 'yes' else 'No'
            extend = False
            if not info == "http://":
                try:
                    tname, extracted, zipsize, skin, created, programs, video, music, picture, repos, scripts = wiz.checkInfo(info)
                    extend = True
                except:
                    extend = False
            if extend == True:
                msg  = "[COLOR %s]Build Name:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, name)
                msg += "[COLOR %s]Build Version:[/COLOR] v[COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, version)
                msg += "[COLOR %s]Latest Update:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, created)
                if not theme == "http://":
                    themecount = wiz.themeCount(name, False)
                    msg += "[COLOR %s]Build Theme(s):[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, ', '.join(themecount))
                msg += "[COLOR %s]Kodi Version:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, kodi)
                msg += "[COLOR %s]Extracted Size:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, wiz.convertSize(int(float(extracted))))
                msg += "[COLOR %s]Zip Size:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, wiz.convertSize(int(float(zipsize))))
                msg += "[COLOR %s]Skin Name:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, skin)
                msg += "[COLOR %s]Adult Content:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, adult)
                msg += "[COLOR %s]Description:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, description)
                msg += "[COLOR %s]Programs:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, programs)
                msg += "[COLOR %s]Video:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, video)
                msg += "[COLOR %s]Music:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, music)
                msg += "[COLOR %s]Pictures:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, picture)
                msg += "[COLOR %s]Repositories:[/COLOR] [COLOR %s]%s[/COLOR][CR][CR]" % (COLOR2, COLOR1, repos)
                msg += "[COLOR %s]Scripts:[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, scripts)
            else:
                msg  = "[COLOR %s]Build Name:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, name)
                msg += "[COLOR %s]Build Version:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, version)
                if not theme == "http://":
                    themecount = wiz.themeCount(name, False)
                    msg += "[COLOR %s]Build Theme(s):[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, ', '.join(themecount))
                msg += "[COLOR %s]Kodi Version:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, kodi)
                msg += "[COLOR %s]Adult Content:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, adult)
                msg += "[COLOR %s]Description:[/COLOR] [COLOR %s]%s[/COLOR][CR]" % (COLOR2, COLOR1, description)

            wiz.TextBox(ADDONTITLE, msg)
        else: wiz.log("Invalid Build Name!")
    else: wiz.log("Build text file not working: %s" % WORKINGURL)

def buildVideo(name):
    if wiz.workingURL(BUILDFILE) == True:
        videofile = wiz.checkBuild(name, 'preview')
        if videofile and not videofile == 'http://': playVideo(videofile)
        else: wiz.log("[%s]Unable to find url for video preview" % name)
    else: wiz.log("Build text file not working: %s" % WORKINGURL)

def dependsList(plugin):
    addonxml = os.path.join(ADDONS, plugin, 'addon.xml')
    if os.path.exists(addonxml):
        source = xbmcvfs.File(addonxml); link = source.read(); source.close();
        match  = wiz.parseDOM(link, 'import', ret='addon')
        items  = []
        for depends in match:
            if not 'xbmc.python' in depends:
                items.append(depends)
        return items
    return []

def manageSaveData(do):
    if do == 'import':
        TEMP = os.path.join(ADDONDATA, 'temp')
        if not os.path.exists(TEMP): os.makedirs(TEMP)
        source = DIALOG.browse(1, '[COLOR %s]Select the location of the SaveData.zip[/COLOR]' % COLOR2, 'files', '.zip', False, False, HOME)
        if not source.endswith('.zip'):
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Import Data Error![/COLOR]" % (COLOR2))
            return
        source   = transPath(source)
        tempfile = transPath(os.path.join(MYBUILDS, 'SaveData.zip'))
        if not tempfile == source:
            goto = xbmcvfs.copy(source, tempfile)
        if extract.all(transPath(tempfile), TEMP) == False:
            wiz.log("Error trying to extract the zip file!")
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Import Data Error![/COLOR]" % (COLOR2))
            return
        trakt  = os.path.join(TEMP, 'trakt')
        login  = os.path.join(TEMP, 'login')
        debrid = os.path.join(TEMP, 'debrid')
        super  = os.path.join(TEMP, 'plugin.program.super.favourites')
        xmls   = os.path.join(TEMP, 'xmls')
        x = 0
        overwrite = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you rather we overwrite all Save Data files or ask you for each file being imported?[/COLOR]" % (COLOR2), yeslabel="[B][COLOR springgreen]Overwrite All[/COLOR][/B]", nolabel="[B][COLOR red]No Ask[/COLOR][/B]")
        if os.path.exists(trakt):
            x += 1
            files = os.listdir(trakt)
            if not os.path.exists(traktit.TRAKTFOLD): os.makedirs(traktit.TRAKTFOLD)
            for item in files:
                old  = os.path.join(traktit.TRAKTFOLD, item)
                temp = os.path.join(trakt, item)
                if os.path.exists(old):
                    if overwrite == 1: xbmcvfs.delete(old)
                    else:
                        if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like replace the current [COLOR %s]%s[/COLOR] file?" % (COLOR2, COLOR1, item), yeslabel="[B][COLOR springgreen]Yes Replace[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"): continue
                        else: xbmcvfs.delete(old)
                shutil.copy(temp, old)
            traktit.importlist('all')
            traktit.traktIt('restore', 'all')
        if os.path.exists(login):
            x += 1
            files = os.listdir(login)
            if not os.path.exists(loginit.LOGINFOLD): os.makedirs(loginit.LOGINFOLD)
            for item in files:
                old  = os.path.join(loginit.LOGINFOLD, item)
                temp = os.path.join(login, item)
                if os.path.exists(old):
                    if overwrite == 1: xbmcvfs.delete(old)
                    else:
                        if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like replace the current [COLOR %s]%s[/COLOR] file?" % (COLOR2, COLOR1, item), yeslabel="[B][COLOR springgreen]Yes Replace[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"): continue
                        else: xbmcvfs.delete(old)
                shutil.copy(temp, old)
            loginit.importlist('all')
            loginit.loginIt('restore', 'all')
        if os.path.exists(debrid):
            x += 1
            files = os.listdir(debrid)
            if not os.path.exists(debridit.REALFOLD): os.makedirs(debridit.REALFOLD)
            for item in files:
                old  = os.path.join(debridit.REALFOLD, item)
                temp = os.path.join(debrid, item)
                if os.path.exists(old):
                    if overwrite == 1: xbmcvfs.delete(old)
                    else:
                        if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like replace the current [COLOR %s]%s[/COLOR] file?" % (COLOR2, COLOR1, item), yeslabel="[B][COLOR springgreen]Yes Replace[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"): continue
                        else: xbmcvfs.delete(old)
                shutil.copy(temp, old)
            debridit.importlist('all')
            debridit.debridIt('restore', 'all')
        if os.path.exists(xmls):
            x += 1
            files = ['advancedsettings.xml', 'sources.xml', 'favourites.xml', 'profiles.xml']
            for item in files:
                old = os.path.join(USERDATA, item)
                new = os.path.join(xmls, item)
                if not os.path.exists(new): continue
                if os.path.exists(old):
                    if not overwrite == 1:
                        if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like replace the current [COLOR %s]%s[/COLOR] file?" % (COLOR2, COLOR1, item), yeslabel="[B][COLOR springgreen]Yes Replace[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"): continue
                xbmcvfs.delete(old)
                shutil.copy(new, old)
        if os.path.exists(super):
            x += 1
            old = os.path.join(ADDOND, 'plugin.program.super.favourites')
            if os.path.exists(old):
                cont = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like replace the current [COLOR %s]Super Favourites[/COLOR] addon_data folder with the new one?" % (COLOR2, COLOR1), yeslabel="[B][COLOR springgreen]Yes Replace[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]")
            else: cont = 1
            if cont == 1:
                wiz.cleanHouse(old)
                wiz.removeFolder(old)
                shutil.copytree(super, old)
        wiz.cleanHouse(TEMP)
        wiz.removeFolder(TEMP)
        if not tempfile == source:
            xbmcvfs.delete(tempfile)
        if x == 0: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Save Data Import Failed[/COLOR]" % COLOR2)
        else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Save Data Import Complete[/COLOR]" % COLOR2)
    elif do == 'export':
        mybuilds = transPath(MYBUILDS)
        dir   = [traktit.TRAKTFOLD, debridit.REALFOLD, loginit.LOGINFOLD]
        xmls  = ['advancedsettings.xml', 'sources.xml', 'favourites.xml', 'profiles.xml']
        keepx = [KEEPADVANCED, KEEPSOURCES, KEEPFAVS, KEEPPROFILES, KEEPPLAYERCORE]
        traktit.traktIt('update', 'all')
        loginit.loginIt('update', 'all')
        debridit.debridIt('update', 'all')
        source = DIALOG.browse(3, '[COLOR %s]Select where you wish to export the savedata zip?[/COLOR]' % COLOR2, 'files', '', False, True, HOME)
        source = transPath(source)
        tempzip = os.path.join(mybuilds, 'SaveData.zip')
        superfold = os.path.join(ADDOND, 'plugin.program.super.favourites')
        zipf = zipfile.ZipFile(tempzip, mode='w')
        for fold in dir:
            if os.path.exists(fold):
                files = os.listdir(fold)
                for file in files:
                    fn = os.path.join(fold, file)
                    zipf.write(fn, fn[len(ADDONDATA):], zipfile.ZIP_DEFLATED)
        if KEEPSUPER == 'true' and os.path.exists(superfold):
            for base, dirs, files in os.walk(superfold):
                for file in files:
                    fn = os.path.join(base, file)
                    zipf.write(fn, fn[len(ADDOND):], zipfile.ZIP_DEFLATED)
        for item in xmls:
            if keepx[xmls.index(item)] == 'true' and os.path.exists(os.path.join(USERDATA, item)):
                zipf.write(os.path.join(USERDATA, item), os.path.join('xmls', item), zipfile.ZIP_DEFLATED)
        zipf.close()
        if source == mybuilds:
            DIALOG.ok(ADDONTITLE, "[COLOR %s]Save data has been backed up to:[/COLOR][CR][COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, tempzip))
        else:
            try:
                xbmcvfs.copy(tempzip, os.path.join(source, 'SaveData.zip'))
                DIALOG.ok(ADDONTITLE, "[COLOR %s]Save data has been backed up to:[/COLOR][CR][COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, os.path.join(source, 'SaveData.zip')))
            except:
                DIALOG.ok(ADDONTITLE, "[COLOR %s]Save data has been backed up to:[/COLOR][CR][COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, tempzip))

###########################
###### Fresh Install ######
###########################
def freshStart(install=None, over=False):
    if KEEPTRAKT == 'true':
        traktit.autoUpdate('all')
        wiz.setS('traktlastsave', str(THREEDAYS))
    if KEEPREAL == 'true':
        debridit.autoUpdate('all')
        wiz.setS('debridlastsave', str(THREEDAYS))
    if KEEPLOGIN == 'true':
        loginit.autoUpdate('all')
        wiz.setS('loginlastsave', str(THREEDAYS))
    if over == True: yes_pressed = 1
    elif install == 'restore': yes_pressed=DIALOG.yesno(ADDONTITLE, "[COLOR %s]Do you want to reset Kodi to its original settings before installing local backup?[/COLOR]"% COLOR2, nolabel = '[B][COLOR red]No, cancel [/COLOR] [/B]', yeslabel = '[B] [COLOR springgreen]Continue[/COLOR][/B]')
    elif install: yes_pressed=DIALOG.yesno(ADDONTITLE, "[COLOR %s]Do you want to reset [CR] Kodi to its original settings before installing [COLOR %s]%s[/COLOR]?"% ( COLOR2, COLOR1, install), nolabel = '[B] [COLOR red]No, cancel [/COLOR][/B]', yeslabel = '[B] [COLOR springgreen] Continue [/COLOR] [/B]' )
    else: yes_pressed=DIALOG.yesno(ADDONTITLE, "[COLOR %s]Do you want to reset Kodi to its original settings? [/COLOR]"% COLOR2, nolabel = '[B][COLOR red]No, cancel [/COLOR] [/B] ', yeslabel =' [B] [COLOR springgreen] Continued [/COLOR][/B] ')
    if yes_pressed:
        if not wiz.currSkin() in ['skin.confluence', 'skin.estuary']:
            swap = wiz.skinToDefault('Fresh Install')
            if swap == False: return False
            xbmc.sleep(1000)
        if not wiz.currSkin() in ['skin.confluence', 'skin.estuary']:
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Fresh Install: Skin Swap Failed![/COLOR]' % COLOR2)
            return
        wiz.addonUpdates('set')
        xbmcPath=os.path.abspath(HOME)
        DP.create(ADDONTITLE,"[COLOR %s]Calculating files and folders Please Wait![/COLOR]" % COLOR2)
        total_files = sum([len(files) for r, d, files in os.walk(xbmcPath)]); del_file = 0
        DP.update(0, "[COLOR %s]Gathering Excludes list." % COLOR2)
        EXCLUDES.append('My_Builds')
        EXCLUDES.append('archive_cache')
        if KEEPREPOS == 'true':
            repos = glob.glob(os.path.join(ADDONS, 'repo*/'))
            for item in repos:
                repofolder = os.path.split(item[:-1])[1]
                if not repofolder == EXCLUDES:
                    EXCLUDES.append(repofolder)
        if KEEPSUPER == 'true':
            EXCLUDES.append('plugin.program.super.favourites')
        if KEEPWHITELIST == 'true':
            pvr = ''
            whitelist = wiz.whiteList('read')
            if len(whitelist) > 0:
                for item in whitelist:
                    try: name, id, fold = item
                    except: pass
                    if fold.startswith('pvr'): pvr = id
                    depends = dependsList(fold)
                    for plug in depends:
                        if not plug in EXCLUDES:
                            EXCLUDES.append(plug)
                        depends2 = dependsList(plug)
                        for plug2 in depends2:
                            if not plug2 in EXCLUDES:
                                EXCLUDES.append(plug2)
                    if not fold in EXCLUDES:
                        EXCLUDES.append(fold)
                if not pvr == '': wiz.setS('pvrclient', fold)
        if wiz.getS('pvrclient') == '':
            for item in EXCLUDES:
                if item.startswith('pvr'):
                    wiz.setS('pvrclient', item)
        DP.update(0, "[COLOR %s]Clearing out files and folders:" % COLOR2)
        latestAddonDB = wiz.latestDB('Addons')
        for root, dirs, files in os.walk(xbmcPath,topdown=True):
            dirs[:] = [d for d in dirs if d not in EXCLUDES]
            for name in files:
                del_file += 1
                fold = root.replace('/','\\').split('\\')
                x = len(fold)-1
                if name == 'sources.xml' and fold[-1] == 'userdata' and KEEPSOURCES == 'true': wiz.log("Keep Sources: %s" % os.path.join(root, name), LOGNOTICE)
                elif name == 'favourites.xml' and fold[-1] == 'userdata' and KEEPFAVS == 'true': wiz.log("Keep Favourites: %s" % os.path.join(root, name), LOGNOTICE)
                elif name == 'profiles.xml' and fold[-1] == 'userdata' and KEEPPROFILES == 'true': wiz.log("Keep Profiles: %s" % os.path.join(root, name), LOGNOTICE)
                elif name == 'playercorefactory.xml' and fold[-1] == 'userdata' and KEEPPLAYERCORE == 'true': wiz.log("Keep playercorefactory.xml: %s" % os.path.join(root, name), LOGNOTICE)
                elif name == 'advancedsettings.xml' and fold[-1] == 'userdata' and KEEPADVANCED == 'true':  wiz.log("Keep Advanced Settings: %s" % os.path.join(root, name), LOGNOTICE)
                elif name in LOGFILES: wiz.log("Keep Log File: %s" % name, LOGNOTICE)
                elif name.endswith('.db'):
                    try:
                        if name == latestAddonDB and KODIV >= 17: wiz.log("Ignoring %s on v%s" % (name, KODIV), LOGNOTICE)
                        else: xbmcvfs.delete(os.path.join(root,name))
                    except Exception as e:
                        if not name.startswith('Textures13'):
                            wiz.log('Failed to delete, Purging DB', LOGNOTICE)
                            wiz.log("-> %s" % (str(e)), LOGNOTICE)
                            wiz.purgeDb(os.path.join(root,name))
                else:
                    DP.update(int(wiz.percentage(del_file, total_files)), '[COLOR %s]File: [/COLOR][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name))
                    try: xbmcvfs.delete(os.path.join(root,name))
                    except Exception as e:
                        wiz.log("Error removing %s" % os.path.join(root, name), LOGNOTICE)
                        wiz.log("-> / %s" % (str(e)), LOGNOTICE)
            if DP.iscanceled():
                DP.close()
                wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Fresh Start Cancelled[/COLOR]" % COLOR2)
                return False
        for root, dirs, files in os.walk(xbmcPath,topdown=True):
            dirs[:] = [d for d in dirs if d not in EXCLUDES]
            for name in dirs:
                DP.update(100, 'Cleaning Up Empty Folder: [COLOR%s]%s[/COLOR]' % (COLOR1, name))
                if name not in ["Database","userdata","temp","addons","addon_data"]:
                    shutil.rmtree(os.path.join(root,name),ignore_errors=True, onerror=None)
            if DP.iscanceled():
                DP.close()
                wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Fresh Start Cancelled[/COLOR]" % COLOR2)
                return False
        DP.close()
        wiz.clearS('build')
        if over == True:
            return True
        elif install == 'restore':
            return True
        elif install:
            buildWizard(install, 'normal', over=True)
        else:
            if INSTALLMETHOD == 1: todo = 1
            elif INSTALLMETHOD == 2: todo = 0
            else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to [COLOR %s]Force close[/COLOR] kodi or [COLOR %s]Reload Profile[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR red]Reload Profile[/COLOR][/B]", nolabel="[B][COLOR springgreen]Force Close[/COLOR][/B]")
            if todo == 1: wiz.reloadFix('fresh')
            else: wiz.addonUpdates('reset'); wiz.killxbmc(True)
    else:
        if not install == 'restore':
            wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Fresh Install: Cancelled![/COLOR]' % COLOR2)
            wiz.refresh()

#############################
###DELETE CACHE##############
####THANKS GUYS @ NaN #######
def clearCache():
    if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to clear cache?[/COLOR]' % COLOR2, nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]', yeslabel='[B][COLOR springgreen]Clear Cache[/COLOR][/B]'):
        wiz.clearCache()

def clearFunctionCache():
    if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to clear resolver function caches?[/COLOR]' % COLOR2, nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]', yeslabel='[B][COLOR springgreen]Clear Cache[/COLOR][/B]'):
        wiz.clearFunctionCache()
        
def clearArchive():
    if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to clear the \'Archive_Cache\' folder?[/COLOR]' % COLOR2, nolabel='[B][COLOR red]No, Cancel[/COLOR][/B]', yeslabel='[B][COLOR springgreen]Yes Clear[/COLOR][/B]'):
        wiz.clearArchive()

def totalClean():
    if DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to clear cache, packages and thumbnails?[/COLOR]' % COLOR2, nolabel='[B][COLOR red]Cancel Process[/COLOR][/B]',yeslabel='[B][COLOR springgreen]Clean All[/COLOR][/B]'):
        wiz.clearCache()
        wiz.clearFunctionCache()
        wiz.clearPackages('total')
        clearThumb('total')

def clearThumb(type=None):
    latest = wiz.latestDB('Textures')
    if not type == None: choice = 1
    else: choice = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Would you like to delete the %s and Thumbnails folder? They will repopulate on the next startup[/COLOR]' % (COLOR2, latest), nolabel='[B][COLOR red]Don\'t Delete[/COLOR][/B]', yeslabel='[B][COLOR springgreen]Delete Thumbs[/COLOR][/B]')
    if choice == 1:
        try: wiz.removeFile(os.path.join(DATABASE, latest))
        except: wiz.log('Failed to delete, Purging DB.'); wiz.purgeDb(latest)
        wiz.removeFolder(THUMBS)
        #if not type == 'total': wiz.killxbmc()
    else: wiz.log('Clear thumbnames cancelled')
    wiz.redoThumbs()

def purgeDb():
    DB = []; display = []
    for dirpath, dirnames, files in os.walk(HOME):
        for f in fnmatch.filter(files, '*.db'):
            if f != 'Thumbs.db':
                found = os.path.join(dirpath, f)
                DB.append(found)
                dir = found.replace('\\', '/').split('/')
                display.append('(%s) %s' % (dir[len(dir)-2], dir[len(dir)-1]))
    if KODIV >= 16:
        choice = DIALOG.multiselect("[COLOR %s]Select DB File to Purge[/COLOR]" % COLOR2, display)
        if choice == None: wiz.LogNotify("[COLOR %s]Purge Database[/COLOR]" % COLOR1, "[COLOR %s]Cancelled[/COLOR]" % COLOR2)
        elif len(choice) == 0: wiz.LogNotify("[COLOR %s]Purge Database[/COLOR]" % COLOR1, "[COLOR %s]Cancelled[/COLOR]" % COLOR2)
        else:
            for purge in choice: wiz.purgeDb(DB[purge])
    else:
        choice = DIALOG.select("[COLOR %s]Select DB File to Purge[/COLOR]" % COLOR2, display)
        if choice == -1: wiz.LogNotify("[COLOR %s]Purge Database[/COLOR]" % COLOR1, "[COLOR %s]Cancelled[/COLOR]" % COLOR2)
        else: wiz.purgeDb(DB[purge])

##########################
### DEVELOPER MENU #######
##########################
def testnotify():
    url = wiz.workingURL(NOTIFICATION)
    if url == True:
        try:
            id, msg = wiz.splitNotify(NOTIFICATION)
            if id == False: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Notification: Not Formated Correctly[/COLOR]" % COLOR2); return
            notify.notification(msg, True)
        except Exception as e:
            wiz.log("Error on Notifications Window: %s" % str(e), xbmc.LOGERROR)
    else: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Invalid URL for Notification[/COLOR]" % COLOR2)

def testupdate():
    if BUILDNAME == "":
        notify.updateWindow()
    else:
        notify.updateWindow(BUILDNAME, BUILDVERSION, BUILDLATEST, wiz.checkBuild(BUILDNAME, 'icon'), wiz.checkBuild(BUILDNAME, 'fanart'))

def testfirst():
    notify.firstRun()

def testfirstRun():
    notify.firstRunSettings()

###########################
## Making the Directory####
###########################

def addDir(display, mode=None, name=None, url=None, menu=None, description=ADDONTITLE, overwrite=True, fanart=FANART, icon=ICON, themeit=None):
    u = sys.argv[0]
    if not mode == None: u += "?mode=%s" % quote_plus(mode)
    if not name == None: u += "&name="+quote_plus(name)
    if not url == None: u += "&url="+quote_plus(url)
    ok=True
    if themeit: display = themeit % display
    liz=xbmcgui.ListItem(display)
    liz.setArt({ 'fanart': fanart, 'icon' : icon, 'thumb' : icon })
    liz.setInfo( type="Video", infoLabels={ "Title": display, "Plot": description} )
    liz.setProperty( "Fanart_Image", fanart )
    if not menu == None: liz.addContextMenuItems(menu, replaceItems=overwrite)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addFile(display, mode=None, name=None, url=None, menu=None, description=ADDONTITLE, overwrite=True, fanart=FANART, icon=ICON, themeit=None):
    u = sys.argv[0]
    if not mode == None: u += "?mode=%s" % quote_plus(mode)
    if not name == None: u += "&name="+quote_plus(name)
    if not url == None: u += "&url="+quote_plus(url)
    ok=True
    if themeit: display = themeit % display
    liz=xbmcgui.ListItem(display)
    liz.setArt({ 'fanart': fanart, 'icon' : icon, 'thumb' : icon })
    liz.setInfo( type="Video", infoLabels={ "Title": display, "Plot": description} )
    liz.setProperty( "Fanart_Image", fanart )
    if not menu == None: liz.addContextMenuItems(menu, replaceItems=overwrite)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]

        return param

################KODI VERSION##########################################
def KodiVer():
    if KODIV >= 16.0 and KODIV <= 16.9:vername = 'Jarvis'
    elif KODIV >= 17.0 and KODIV <= 17.9:vername = 'Krypton'
    elif KODIV >= 18.0 and KODIV <= 18.9:vername = 'Leia'
    elif KODIV >= 19.0 and KODIV <= 19.9:vername = 'Matrix'
    else: vername = "Unknown"
    return vername
######################################################################################################################
######################################################################################################################
params=get_params()
url=None
name=None
mode=None

try:     mode=unquote_plus(params["mode"])
except:  pass
try:     name=unquote_plus(params["name"])
except:  pass
try:     url=unquote_plus(params["url"])
except:  pass

wiz.log('[ Version : \'%s\' ] [ Mode : \'%s\' ] [ Name : \'%s\' ] [ Url : \'%s\' ]' % (VERSION, mode if not mode == '' else None, name, url))

def setView(content, viewType):
    if wiz.getS('auto-view')=='true':
        views = wiz.getS(viewType)
        if views == '50' and KODIV >= 17 and SKIN == 'skin.estuary': views = '55'
        if views == '500' and KODIV >= 17 and SKIN == 'skin.estuary': views = '50'
        wiz.ebi("Container.SetViewMode(%s)" %  views)

if   mode==None             : index()

elif mode=='wizardupdate'   : wiz.wizardUpdate()
elif mode=='builds'         : buildMenu()
elif mode=='viewbuild'      : viewBuild(name)
elif mode=='buildinfo'      : buildInfo(name)
elif mode=='buildpreview'   : buildVideo(name)
elif mode=='install'        : buildWizard(name, url)
elif mode=='theme'          : buildWizard(name, mode, url)
elif mode=='viewthirdparty' : viewThirdList(name)
elif mode=='installthird'   : thirdPartyInstall(name, url)
elif mode=='editthird'      : editThirdParty(name); wiz.refresh()
elif mode=='maint'          : maintMenu(name)
elif mode=='kodi17fix'      : wiz.kodi17Fix()
elif mode=='kodi19fix'      : wiz.kodi19Fix()
elif mode=='unknownsources' : skinSwitch.swapUS()
elif mode=='advancedsetting': advancedWindow(name)
elif mode=='autoadvanced'   : showAutoAdvanced(); wiz.refresh()
elif mode=='removeadvanced' : removeAdvanced(); wiz.refresh()
elif mode=='asciicheck'     : wiz.asciiCheck()
elif mode=='extractazip'    : wiz.extractAZip()
elif mode=='backupbuild'    : wiz.backUpOptions('build')
elif mode=='backupgui'      : wiz.backUpOptions('guifix')
elif mode=='backuptheme'    : wiz.backUpOptions('theme')
elif mode=='backupaddonpack': wiz.backUpOptions('addon pack')
elif mode=='backupaddon'    : wiz.backUpOptions('addondata')
elif mode=='oldThumbs'      : wiz.oldThumbs()
elif mode=='clearbackup'    : wiz.cleanupBackup()
elif mode=='convertpath'    : wiz.convertSpecial(HOME)
elif mode=='currentsettings': viewAdvanced()
elif mode=='fullclean'      : totalClean(); wiz.refresh()
elif mode=='clearcache'     : clearCache(); wiz.refresh()
elif mode=='clearfunctioncache'     : clearFunctionCache(); wiz.refresh()
elif mode=='clearpackages'  : wiz.clearPackages(); wiz.refresh()
elif mode=='clearcrash'     : wiz.clearCrash(); wiz.refresh()
elif mode=='clearthumb'     : clearThumb(); wiz.refresh()
elif mode=='cleararchive'   : clearArchive(); wiz.refresh()
elif mode=='checksources'   : wiz.checkSources(); wiz.refresh()
elif mode=='checkrepos'     : wiz.checkRepos(); wiz.refresh()
elif mode=='freshstart'     : freshStart()
elif mode=='forceupdate'    : wiz.forceUpdate()
elif mode=='forceprofile'   : wiz.reloadProfile(wiz.getInfo('System.ProfileName'))
elif mode=='forceclose'     : wiz.killxbmc()
elif mode=='forceskin'      : wiz.ebi("ReloadSkin()"); wiz.refresh()
elif mode=='hidepassword'   : wiz.hidePassword()
elif mode=='unhidepassword' : wiz.unhidePassword()
elif mode=='enableaddons'   : enableAddons()
elif mode=='toggleaddon'    : wiz.toggleAddon(name, url); wiz.refresh()
elif mode=='togglecache'    : toggleCache(name); wiz.refresh()
elif mode=='toggleadult'    : wiz.toggleAdult(); wiz.refresh()
elif mode=='changefeq'      : changeFeq(); wiz.refresh()
elif mode=='uploadlog'      : uploadLog.Main()
elif mode=='viewlog'        : LogViewer()
elif mode=='viewwizlog'     : LogViewer(WIZLOG)
elif mode=='viewerrorlog'   : errorChecking()
elif mode=='viewerrorlast'  : errorChecking(last=True)
elif mode=='clearwizlog'    : f = xbmcvfs.File(WIZLOG, 'w'); f.close(); wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Wizard Log Cleared![/COLOR]" % COLOR2)
elif mode=='purgedb'        : purgeDb()
elif mode=='fixaddonupdate' : wiz.force_check_updates(auto=True, over=False)
elif mode=='removeaddons'   : removeAddonMenu()
elif mode=='removeaddon'    : removeAddon(name)
elif mode=='removeaddondata': removeAddonDataMenu()
elif mode=='removedata'     : removeAddonData(name)
elif mode=='resetaddon'     : total = wiz.cleanHouse(ADDONDATA, ignore=True); wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Addon_Data reset[/COLOR]" % COLOR2)
elif mode=='systeminfo'     : systemInfo()
elif mode=='restorezip'     : restoreit('build')
elif mode=='restoregui'     : restoreit('gui')
elif mode=='restoreaddon'   : restoreit('addondata')
elif mode=='restoreextzip'  : restoreextit('build')
elif mode=='restoreextgui'  : restoreextit('gui')
elif mode=='restoreextaddon': restoreextit('addondata')
elif mode=='writeadvanced'  : writeAdvanced(name, url)
elif mode=='speedtest'      : net_tools()
elif mode=='runspeedtest'   : runSpeedTest(); wiz.refresh()
elif mode=='clearspeedtest' : clearSpeedTest(); wiz.refresh()
elif mode=='viewspeedtest'  : viewSpeedTest(name); wiz.refresh()
elif mode=="viewIP"         : viewIP();

elif mode=='speedtestM'     : speedTest()

elif mode=='apk'            : apkMenu(name, url)
elif mode=='apkscrape'      : apkScraper(name)
elif mode=='apkinstall'     : apkInstaller(name, url)
elif mode=='rominstall'     : romInstaller(name, url)

elif mode=='youtube'        : youtubeMenu(name, url)
elif mode=='viewVideo'      : playVideo(url)

elif mode=='addons'         : addonMenu(name, url)
elif mode=='addonpack'      : packInstaller(name, url)
elif mode=='skinpack'       : skinInstaller(name, url)
elif mode=='addoninstall'   : addonInstaller(name, url)

elif mode=='savedata'       : saveMenu()
elif mode=='togglesetting'  : wiz.setS(name, 'false' if wiz.getS(name) == 'true' else 'true'); wiz.refresh()
elif mode=='managedata'     : manageSaveData(name)
elif mode=='whitelist'      : wiz.whiteList(name)

elif mode=='trakt'          : traktMenu()
elif mode=='savetrakt'      : traktit.traktIt('update',      name)
elif mode=='restoretrakt'   : traktit.traktIt('restore',     name)
elif mode=='addontrakt'     : traktit.traktIt('clearaddon',  name)
elif mode=='cleartrakt'     : traktit.clearSaved(name)
elif mode=='authtrakt'      : traktit.activateTrakt(name); wiz.refresh()
elif mode=='updatetrakt'    : traktit.autoUpdate('all')
elif mode=='importtrakt'    : traktit.importlist(name); wiz.refresh()

elif mode=='realdebrid'     : realMenu()
elif mode=='savedebrid'     : debridit.debridIt('update',      name)
elif mode=='restoredebrid'  : debridit.debridIt('restore',     name)
elif mode=='addondebrid'    : debridit.debridIt('clearaddon',  name)
elif mode=='cleardebrid'    : debridit.clearSaved(name)
elif mode=='authdebrid'     : debridit.activateDebrid(name); wiz.refresh()
elif mode=='updatedebrid'   : debridit.autoUpdate('all')
elif mode=='importdebrid'   : debridit.importlist(name); wiz.refresh()

elif mode=='login'          : loginMenu()
elif mode=='savelogin'      : loginit.loginIt('update',      name)
elif mode=='restorelogin'   : loginit.loginIt('restore',     name)
elif mode=='addonlogin'     : loginit.loginIt('clearaddon',  name)
elif mode=='clearlogin'     : loginit.clearSaved(name)
elif mode=='authlogin'      : loginit.activateLogin(name); wiz.refresh()
elif mode=='updatelogin'    : loginit.autoUpdate('all')
elif mode=='importlogin'    : loginit.importlist(name); wiz.refresh()

elif mode=='contact'        : notify.contact(CONTACT)
elif mode=='settings'       : wiz.openS(name); wiz.refresh()
elif mode=='forcetext'      : wiz.forceText()
elif mode=='opensettings'   : id = eval(url.upper()+'ID')[name]['plugin']; addonid = wiz.addonId(id); addonid.openSettings(); wiz.refresh()

elif mode=='developer'      : developer()
elif mode=='converttext'    : wiz.convertText()
elif mode=='createqr'       : wiz.createQR()
elif mode=='testnotify'     : testnotify()
elif mode=='testupdate'     : testupdate()
elif mode=='testfirst'      : testfirst()
elif mode=='testfirstrun'   : testfirstRun()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
