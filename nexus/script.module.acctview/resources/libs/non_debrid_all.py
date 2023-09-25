import xbmc
import xbmcaddon
import xbmcgui

import os
import time

from xml.etree import ElementTree

from resources.libs.common.config import CONFIG
from resources.libs.common import logging
from resources.libs.common import tools

ORDER = ['fen',
         'ezra',
         'coal',
         'pov',
         'umb',
         'thecrew',
         'homelander',
         'quicksilver',
         'genocide',
         'shazam',
         'nightwing',
         'alvin',
         'moria',
         'absolution',
         'nine',
         'acctmgr',
         'myact']

DEBRIDID = {
    'fen': {
        'name'     : 'Fen',
        'plugin'   : 'plugin.video.fen',
        'saved'    : 'fen',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_fanart.png'),
        'file'     : os.path.join(CONFIG.NONDEBRIDFOLD, 'fen_nondebrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fen', 'settings.xml'),
        'default'  : '',
        'default_furk'  : 'furk_login',
        'default_easy'  : 'easynews_user',
        'default_file'  : '',
        'data'     : ['furk_login', 'furk_password', 'furk_api_key', 'provider.furk', 'provider.easynews', 'easynews_user', 'easynews_password', 'furk.title_filter', 'check.furk', 'fu.priority', 'easynews.use_custom_farm', 'easynews.server_name', 'easynews.title_filter', 'easynews.filter_lang', 'en.priority', 'easynews.lang_filters', 'check.easynews'],
        'activate' : 'Addon.OpenSettings(plugin.video.fen)'},
    'ezra': {
        'name'     : 'Ezra',
        'plugin'   : 'plugin.video.ezra',
        'saved'    : 'ezra',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra', 'fanart.png'),
        'file'     : os.path.join(CONFIG.NONDEBRIDFOLD, 'ezra_nondebrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.ezra', 'settings.xml'),
        'default'  : '',
        'default_furk'  : 'furk_login',
        'default_easy'  : 'easynews_user',
        'default_file'  : '',
        'data'     : ['furk_login', 'furk_password', 'furk_api_key', 'provider.furk', 'provider.easynews', 'easynews_user',  'easynews_password', 'furk.mod.level', 'furk.title_filter', 'check.furk', 'fu.priority', 'easynews.title_filter', 'easynews.filter_lang', 'en.priority', 'easynews.lang_filters', 'easynews_moderation', 'check.easynews'],
        'activate' : 'Addon.OpenSettings(plugin.video.ezra)'},
    'coal': {
        'name'     : 'Coalition',
        'plugin'   : 'plugin.video.coalition',
        'saved'    : 'coal',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.coalition'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.coalition/resources/media/', 'fen_icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.coalition/resources/media/', 'fen_fanart.png'),
        'file'     : os.path.join(CONFIG.NONDEBRIDFOLD, 'coal_nondebrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.coalition', 'settings.xml'),
        'default'  : '',
        'default_furk'  : 'furk_login',
        'default_easy'  : 'easynews_user',
        'default_file'  : '',
        'data'     : ['furk_login', 'furk_password', 'furk_api_key', 'provider.furk', 'provider.easynews', 'easynews_user', 'easynews_password', 'furk.title_filter', 'check.furk', 'fu.priority', 'easynews.use_custom_farm', 'easynews.server_name', 'easynews.title_filter', 'easynews.filter_lang', 'en.priority', 'easynews.lang_filters', 'check.easynews'],
        'activate' : 'Addon.OpenSettings(plugin.video.coalition)'},
    'pov': {
        'name'     : 'POV',
        'plugin'   : 'plugin.video.pov',
        'saved'    : 'pov',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.pov'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.pov', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.pov', 'fanart.png'),
        'file'     : os.path.join(CONFIG.NONDEBRIDFOLD, 'pov_nondebrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.pov', 'settings.xml'),
        'default'  : '',
        'default_furk'  : 'furk_login',
        'default_easy'  : 'easynews_user',
        'default_file'  : '',
        'data'     : ['furk_login', 'furk_password', 'furk_api_key', 'provider.furk', 'provider.easynews', 'easynews_user', 'easynews_password', 'furk.mod.level', 'furk.title_filter', 'check.furk', 'fu.priority', 'easynews.title_filter', 'easynews.filter_lang', 'en.priority', 'easynews.lang_filters', 'easynews_moderation', 'check.easynews'],
        'activate' : 'Addon.OpenSettings(plugin.video.pov)'},
    'umb': {
        'name'     : 'Umbrella',
        'plugin'   : 'plugin.video.umbrella',
        'saved'    : 'umb',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.NONDEBRIDFOLD, 'umb_nondebrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.umbrella', 'settings.xml'),
        'default'  : '',
        'default_furk'  : 'furk.user_name',
        'default_easy'  : 'easynews.user',
        'default_file'  : 'filepursuit.api',
        'data'     : ['easynews.enable', 'easynews.user', 'easynews.password', 'filepursuit.enable', 'filepursuit.api', 'furk.enable', 'furk.user_name', 'furk.user_pass', 'furk.api', 'easynews.priority', 'filepursuit.priority', 'furk.priority'],
        'activate' : 'Addon.OpenSettings(plugin.video.umbrella)'},
   'thecrew': {
        'name'     : 'The Crew',
        'plugin'   : 'plugin.video.thecrew',
        'saved'    : 'thecrew',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.NONDEBRIDFOLD, 'thecrew_nondebrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thecrew', 'settings.xml'),
        'default'  : '',
        'default_furk'  : 'furk.user_name',
        'default_easy'  : 'easynews.user',
        'default_file'  : '',
        'data'     : ['easynews.user', 'easynews.password', 'furk.user_name', 'furk.user_pass', 'furk.api', 'furk.limit'],
        'activate' : 'Addon.OpenSettings(plugin.video.thecrew)'},
   'homelander': {
        'name'     : 'Homelander',
        'plugin'   : 'plugin.video.homelander',
        'saved'    : 'homelander',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.homelander'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.homelander', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.homelander', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.NONDEBRIDFOLD, 'homelander_nondebrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.homelander', 'settings.xml'),
        'default'  : '',
        'default_furk'  : 'furk.user_name',
        'default_easy'  : '',
        'default_file'  : '',
        'data'     : ['furk.user_name', 'furk.user_pass', 'furk.api', 'furk.limit'],
        'activate' : 'Addon.OpenSettings(plugin.video.homelander)'},
   'quicksilver': {
        'name'     : 'Quicksilver',
        'plugin'   : 'plugin.video.quicksilver',
        'saved'    : 'quicksilver',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.quicksilver'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.quicksilver', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.quicksilver', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.NONDEBRIDFOLD, 'quicksilver_nondebrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.quicksilver', 'settings.xml'),
        'default'  : '',
        'default_furk'  : 'furk.user_name',
        'default_easy'  : '',
        'default_file'  : '',
        'data'     : ['furk.user_name', 'furk.user_pass', 'furk.api', 'furk.limit'],
        'activate' : 'Addon.OpenSettings(plugin.video.quicksilver)'},
   'genocide': {
        'name'     : 'Chains Genocide',
        'plugin'   : 'plugin.video.chainsgenocide',
        'saved'    : 'chainsgenocide',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.chainsgenocide'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.chainsgenocide', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.chainsgenocide', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.NONDEBRIDFOLD, 'chainsgenocide_nondebrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.chainsgenocide', 'settings.xml'),
        'default'  : '',
        'default_furk'  : 'furk.user_name',
        'default_easy'  : '',
        'default_file'  : '',
        'data'     : ['furk.user_name', 'furk.user_pass', 'furk.api', 'furk.limit'],
        'activate' : 'Addon.OpenSettings(plugin.video.chainsgenocide)'},
   'shazam': {
        'name'     : 'Shazam',
        'plugin'   : 'plugin.video.shazam',
        'saved'    : 'shazam',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shazam'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shazam', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.shazam', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.NONDEBRIDFOLD, 'shazam_nondebrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.shazam', 'settings.xml'),
        'default'  : '',
        'default_furk'  : 'furk.user_name',
        'default_easy'  : '',
        'default_file'  : '',
        'data'     : ['furk.user_name', 'furk.user_pass', 'furk.api', 'furk.limit'],
        'activate' : 'Addon.OpenSettings(plugin.video.shazam)'},
   'nightwing': {
        'name'     : 'Nightwing',
        'plugin'   : 'plugin.video.nightwing',
        'saved'    : 'nightwing',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.nightwing'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.nightwing', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.nightwing', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.NONDEBRIDFOLD, 'nightwing_nondebrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.nightwing', 'settings.xml'),
        'default'  : '',
        'default_furk'  : 'furk.user_name',
        'default_easy'  : '',
        'default_file'  : '',
        'data'     : ['furk.user_name', 'furk.user_pass', 'furk.api', 'furk.limit'],
        'activate' : 'Addon.OpenSettings(plugin.video.nightwing)'},
   'alvin': {
        'name'     : 'Alvin',
        'plugin'   : 'plugin.video.alvin',
        'saved'    : 'alvin',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.alvin'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.alvin', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.alvin', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.NONDEBRIDFOLD, 'alvin_nondebrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.alvin', 'settings.xml'),
        'default'  : '',
        'default_furk'  : 'furk.user_name',
        'default_easy'  : '',
        'default_file'  : '',
        'data'     : ['furk.user_name', 'furk.user_pass', 'furk.api', 'furk.limit'],
        'activate' : 'Addon.OpenSettings(plugin.video.alvin)'},
   'moria': {
        'name'     : 'Moria',
        'plugin'   : 'plugin.video.moria',
        'saved'    : 'moria',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.moria'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.moria', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.moria', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.NONDEBRIDFOLD, 'moria_nondebrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.moria', 'settings.xml'),
        'default'  : '',
        'default_furk'  : 'furk.user_name',
        'default_easy'  : '',
        'default_file'  : '',
        'data'     : ['furk.user_name', 'furk.user_pass', 'furk.api', 'furk.limit'],
        'activate' : 'Addon.OpenSettings(plugin.video.moria)'},
   'absolution': {
        'name'     : 'Absolution',
        'plugin'   : 'plugin.video.absolution',
        'saved'    : 'absolution',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.absolution'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.absolution', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.absolution', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.NONDEBRIDFOLD, 'absolution_nondebrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.absolution', 'settings.xml'),
        'default'  : '',
        'default_furk'  : 'furk.user_name',
        'default_easy'  : '',
        'default_file'  : '',
        'data'     : ['furk.user_name', 'furk.user_pass', 'furk.api', 'furk.limit'],
        'activate' : 'Addon.OpenSettings(plugin.video.absolution)'},
   'nine': {
        'name'     : '9 Lives',
        'plugin'   : 'plugin.video.nine',
        'saved'    : 'nine',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.nine'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.nine', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.nine', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.NONDEBRIDFOLD, 'nine_nondebrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.nine', 'settings.xml'),
        'default'  : '',
        'default_furk'  : 'furk.user_name',
        'default_easy'  : '',
        'default_file'  : '',
        'data'     : ['furk.user_name', 'furk.user_pass', 'furk.api', 'furk.limit'],
        'activate' : 'Addon.OpenSettings(plugin.video.nine)'},
    'acctmgr': {
        'name'     : 'Account Manager',
        'plugin'   : 'script.module.accountmgr',
        'saved'    : 'acctmgr',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr', 'fanart.png'),
        'file'     : os.path.join(CONFIG.NONDEBRIDFOLD, 'acctmgr_nondebrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.accountmgr', 'settings.xml'),
        'default'  : '',
        'default_furk'  : 'furk.username',
        'default_easy'  : 'easynews.username',
        'default_file'  : 'filepursuit.api.key',
        'data'     : ['furk.username', 'furk.password', 'furk.api.key', 'easynews.username', 'easynews.password', 'filepursuit.api.key'],
        'activate' : 'Addon.OpenSettings(script.module.accountmgr)'},
    'myact': {
        'name'     : 'My Accounts',
        'plugin'   : 'script.module.myaccounts',
        'saved'    : 'myact',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'fanart.png'),
        'file'     : os.path.join(CONFIG.NONDEBRIDFOLD, 'myact_nondebrid'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.myaccounts', 'settings.xml'),
        'default'  : '',
        'default_furk'  : 'furk.username',
        'default_easy'  : 'easynews.username',
        'default_file'  : 'filepursuit.api.key',
        'data'     : ['furk.username', 'furk.password', 'furk.api.key', 'easynews.username', 'easynews.password', 'filepursuit.api.key'],
        'activate' : 'Addon.OpenSettings(script.module.myaccounts)'}
}
    
def debrid_user_furk(who):
    user_furk = None
    if DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            try:
                add = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
                user_furk = add.getSetting(DEBRIDID[who]['default_furk'])
            except:
                pass
    return user_furk

def debrid_user_easy(who):
    user_easy = None
    if DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            try:
                add = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
                user_easy = add.getSetting(DEBRIDID[who]['default_easy'])
            except:
                pass
    return user_easy

def debrid_user_file(who):
    user_file = None
    if DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            try:
                add = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
                user_file = add.getSetting(DEBRIDID[who]['default_file'])
            except:
                pass
    return user_file


def debrid_it(do, who):
    if not os.path.exists(CONFIG.ADDON_DATA):
        os.makedirs(CONFIG.ADDON_DATA)
    if not os.path.exists(CONFIG.NONDEBRIDFOLD):
        os.makedirs(CONFIG.NONDEBRIDFOLD)
    if who == 'all':
        for log in ORDER:
            if os.path.exists(DEBRIDID[log]['path']):
                try:
                    addonid = tools.get_addon_by_id(DEBRIDID[log]['plugin'])
                    default = DEBRIDID[log]['default']
                    user = addonid.getSetting(default)
                    
                    update_debrid(do, log)
                except:
                    pass
            else:
                logging.log('[Debrid Info] {0}({1}) is not installed'.format(DEBRIDID[log]['name'], DEBRIDID[log]['plugin']), level=xbmc.LOGERROR)
        CONFIG.set_setting('debridnextsave', tools.get_date(days=3, formatted=True))
    else:
        if DEBRIDID[who]:
            if os.path.exists(DEBRIDID[who]['path']):
                update_debrid(do, who)
        else:
            logging.log('[Debrid Info] Invalid Entry: {0}'.format(who), level=xbmc.LOGERROR)


def clear_saved(who, over=False):
    if who == 'all':
        for debrid in DEBRIDID:
            clear_saved(debrid,  True)
    elif DEBRIDID[who]:
        file = DEBRIDID[who]['file']
        if os.path.exists(file):
            os.remove(file)
    if not over:
        xbmc.executebuiltin('Container.Refresh()')


def update_debrid(do, who):
    file = DEBRIDID[who]['file']
    settings = DEBRIDID[who]['settings']
    data = DEBRIDID[who]['data']
    addonid = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
    saved = DEBRIDID[who]['saved']
    default = DEBRIDID[who]['default']
    user = addonid.getSetting(default)
    suser = CONFIG.get_setting(saved)
    name = DEBRIDID[who]['name']
    icon = DEBRIDID[who]['icon']

    if do == 'update':
        try:
            root = ElementTree.Element(saved)
            
            for setting in data:
                debrid = ElementTree.SubElement(root, 'debrid')
                id = ElementTree.SubElement(debrid, 'id')
                id.text = setting
                value = ElementTree.SubElement(debrid, 'value')
                value.text = addonid.getSetting(setting)
              
            tree = ElementTree.ElementTree(root)
            tree.write(file)
            
            user = addonid.getSetting(default)
            CONFIG.set_setting(saved, user)
            
            logging.log('Debrid Info Saved for {0}'.format(name), level=xbmc.LOGINFO)
        except Exception as e:
            logging.log("[Debrid Info] Unable to Update {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)

    elif do == 'restore':
        if os.path.exists(file):
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            try:
                for setting in root.findall('debrid'):
                    id = setting.find('id').text
                    value = setting.find('value').text
                    addonid.setSetting(id, value)
                
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                
                logging.log('Debrid Info Restored for {0}'.format(name), level=xbmc.LOGINFO)
            except Exception as e:
                logging.log("[Debrid Info] Unable to Restore {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else:
            logging.log('Debrid Info Not Found for {0}'.format(name))
    elif do == 'clearaddon':
        logging.log('{0} SETTINGS: {1}'.format(name, settings))
        if os.path.exists(settings):
            try:
                tree = ElementTree.parse(settings)
                root = tree.getroot()
                
                for setting in root.findall('setting'):
                    if setting.attrib['id'] in data:
                        logging.log('Removing Setting: {0}'.format(setting.attrib))
                        root.remove(setting)
                            
                tree.write(settings)
                
            except Exception as e:
                logging.log("[Debrid Info] Unable to Clear Addon {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
    xbmc.executebuiltin('Container.Refresh()')
    
    revoke_nondebrid() #Restore default API keys for all add-ons

def auto_update(who):
    if who == 'all':
        for log in DEBRIDID:
            if os.path.exists(DEBRIDID[log]['path']):
                auto_update(log)
    elif DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            u = debrid_user(who)
            su = CONFIG.get_setting(DEBRIDID[who]['saved'])
            n = DEBRIDID[who]['name']
            if not u or u == '':
                return
            elif su == '':
                debrid_it('update', who)
            elif not u == su:
                dialog = xbmcgui.Dialog()

                if dialog.yesno(CONFIG.ADDONTITLE,
                                    "Would you like to save the [COLOR {0}]Debrid Info[/COLOR] for [COLOR {1}]{2}[/COLOR]?".format(CONFIG.COLOR2, CONFIG.COLOR1, n),
                                    "Addon: [COLOR springgreen][B]{0}[/B][/COLOR]".format(u),
                                    "Saved:[/COLOR] [COLOR red][B]{0}[/B][/COLOR]".format(su) if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]',
                                    yeslabel="[B][COLOR springreen]Save Debrid[/COLOR][/B]",
                                    nolabel="[B][COLOR red]No, Cancel[/COLOR][/B]"):
                    debrid_it('update', who)
            else:
                debrid_it('update', who)


def import_list(who):
    if who == 'all':
        for log in DEBRIDID:
            if os.path.exists(DEBRIDID[log]['file']):
                import_list(log)
    elif DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['file']):
            file = DEBRIDID[who]['file']
            addonid = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
            saved = DEBRIDID[who]['saved']
            default = DEBRIDID[who]['default']
            suser = CONFIG.get_setting(saved)
            name = DEBRIDID[who]['name']
            
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            for setting in root.findall('debrid'):
                id = setting.find('id').text
                value = setting.find('value').text
            
                addonid.setSetting(id, value)

            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                       '[COLOR {0}]Debrid Info: Imported![/COLOR]'.format(CONFIG.COLOR2))


def open_settings_debrid(who):
    addonid = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
    addonid.openSettings()

def revoke_nondebrid():

    if xbmcvfs.exists(var.chk_ezra) and xbmcvfs.exists(var.chkset_ezra):
        try:
            addon = xbmcaddon.Addon("plugin.video.ezra")
            addon.setSetting("fanart_client_key", var.ezra_fan)                        
            addon = xbmcaddon.Addon("plugin.video.ezra")
            addon.setSetting("tmdb_api", var.ezra_tmdb)
        except:
            pass
        
    if xbmcvfs.exists(var.chk_fen) and xbmcvfs.exists(var.chkset_fen):
        try:
            addon = xbmcaddon.Addon("plugin.video.fen")
            addon.setSetting("fanart_client_key", var.fen_fan)                        
            addon = xbmcaddon.Addon("plugin.video.fen")
            addon.setSetting("tmdb_api", var.fen_tmdb)
        except:
            pass

    if xbmcvfs.exists(var.chk_pov) and xbmcvfs.exists(var.chkset_pov):

        addon = xbmcaddon.Addon("plugin.video.pov")
        addon.setSetting("fanart_client_key", var.pov_fan)                        
        addon = xbmcaddon.Addon("plugin.video.pov")
        addon.setSetting("tmdb_api", var.pov_tmdb)

        
    if xbmcvfs.exists(var.chk_adina) and xbmcvfs.exists(var.chkset_adina):
        try:
            addon = xbmcaddon.Addon("plugin.video.adina")
            addon.setSetting("fanart_client_key", var.adina_fan)                        
            addon = xbmcaddon.Addon("plugin.video.adina")
            addon.setSetting("tmdb_api", var.adina_tmdb)
        except:
            pass

    if xbmcvfs.exists(var.chk_home) and xbmcvfs.exists(var.chkset_home):
        try:
            addon = xbmcaddon.Addon("plugin.video.home")
            addon.setSetting("fanart.tv.user", var.home_fan)                        
            addon = xbmcaddon.Addon("plugin.video.home")
            addon.setSetting("tm.user", var.home_tmdb)
        except:
            pass

    if xbmcvfs.exists(var.chk_crew) and xbmcvfs.exists(var.chkset_crew):
        try:
            addon = xbmcaddon.Addon("plugin.video.thecrew")
            addon.setSetting("fanart.tv.user", var.crew_fan)                        
            addon = xbmcaddon.Addon("plugin.video.thecrew")
            addon.setSetting("tm.user", var.crew_tmdb)
        except:
            pass
