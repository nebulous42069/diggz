import xbmc
import xbmcgui
import xbmcaddon
import os
import time
import xbmcvfs
from xml.etree import ElementTree

from resources.libs.common.config import CONFIG
from resources.libs.common import logging
from resources.libs.common import tools
from resources.libs.common import var

ORDER = ['seren',
         'fen',
         'ezra',
         'coal',
         'pov',
         'umbrella',
         'shadow',
         'ghost',
         'base19',
         'unleashed',
         'chains',
         'md',
         'asgard',
         'patriot',
         'blackl',
         'aliunde',
         'homelander',
         'quicksilver',
         'genocide',
         'absolution',
         'shazam',
         'thecrew',
         'nightwing',
         'alvin',
         'moria',
         'nine',
         'scrubs',
         'tmdbhelper',
         'trakt',
         'acctmgr',
         'myact']

TRAKTID = {
   'seren': {
        'name'     : 'Seren',
        'plugin'   : 'plugin.video.seren',
        'saved'    : 'seren',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren/resources/images', 'ico-seren-3.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.seren/resources/images', 'fanart-seren-3.png'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'seren_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'settings.xml'),
        'default'  : 'trakt.username',
        'data'     : ['trakt.auth', 'trakt.clientid', 'trakt.refresh', 'trakt.secret', 'trakt.username', 'trakt.expires'],
        'activate' : 'Addon.OpenSettings(plugin.video.seren)'},
    'fen': {
        'name'     : 'Fen',
        'plugin'   : 'plugin.video.fen',
        'saved'    : 'fen',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_fanart.png'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'fen_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fen', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.refresh', 'trakt.expires', 'trakt.token', 'trakt.user', 'trakt.indicators_active','watched_indicators'],
        'activate' : 'Addon.OpenSettings(plugin.video.fen)'},
    'ezra': {
        'name'     : 'Ezra',
        'plugin'   : 'plugin.video.ezra',
        'saved'    : 'ezra',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra', 'fanart.png'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'ezra_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.ezra', 'settings.xml'),
        'default'  : 'trakt_user',
        'data'     : ['trakt.expires', 'trakt.token', 'trakt_user', 'trakt.indicators_active','watched_indicators'],
        'activate' : 'Addon.OpenSettings(plugin.video.ezra)'},
    'coal': {
        'name'     : 'Coalition',
        'plugin'   : 'plugin.video.coalition',
        'saved'    : 'coal',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.coalition'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.coalition', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.coalition', 'fanart.png'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'coal_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.coalition', 'settings.xml'),
        'default'  : 'trakt_user',
        'data'     : ['trakt.refresh', 'trakt.expires', 'trakt.token', 'trakt_user', 'trakt.indicators_active','watched_indicators'],
        'activate' : 'Addon.OpenSettings(plugin.video.coalition)'},
    'pov': {
        'name'     : 'POV',
        'plugin'   : 'plugin.video.pov',
        'saved'    : 'pov',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.pov'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.pov', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.pov', 'fanart.png'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'pov_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.pov', 'settings.xml'),
        'default'  : 'trakt_user',
        'data'     : ['trakt.refresh', 'trakt.expires', 'trakt.token', 'trakt_user', 'trakt.indicators_active','watched_indicators'],
        'activate' : 'Addon.OpenSettings(plugin.video.pov)'},
    'umbrella': {
        'name'     : 'Umbrella',
        'plugin'   : 'plugin.video.umbrella',
        'saved'    : 'umbrella',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'umbrella_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.umbrella', 'settings.xml'),
        'default'  : 'trakt.user.name',
        'data'     : ['trakt.clientid', 'trakt.clientsecret', 'trakt.user.token', 'trakt.user.name', 'trakt.token.expires', 'trakt.refreshtoken', 'traktuserkey.customenabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.umbrella)'},
    'shadow': {
        'name'     : 'Shadow',
        'plugin'   : 'plugin.video.shadow',
        'saved'    : 'shadow',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'shadow_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.shadow', 'settings.xml'),
        'default'  : 'trakt_access_token',
        'data'     : ['trakt_expires_at', 'trakt_refresh_token', 'trakt_access_token'],
        'activate' : 'Addon.OpenSettings(plugin.video.shadow)'},
    'ghost': {
        'name'     : 'Ghost',
        'plugin'   : 'plugin.video.ghost',
        'saved'    : 'ghost',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'ghost_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.ghost', 'settings.xml'),
        'default'  : 'trakt_access_token',
        'data'     : ['trakt_expires_at', 'trakt_refresh_token', 'trakt_access_token'],
        'activate' : 'Addon.OpenSettings(plugin.video.ghost)'},
    'base19': {
        'name'     : 'Base 19',
        'plugin'   : 'plugin.video.base19',
        'saved'    : 'base19',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.base19'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.base19', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.base19', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'base19_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.base19', 'settings.xml'),
        'default'  : 'trakt_access_token',
        'data'     : ['trakt_expires_at', 'trakt_refresh_token', 'trakt_access_token'],
        'activate' : 'Addon.OpenSettings(plugin.video.base19)'},
    'unleashed': {
        'name'     : 'Unleashed',
        'plugin'   : 'plugin.video.unleashed',
        'saved'    : 'unleashed',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.unleashed'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.unleashed', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.unleashed', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'unleashed_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.unleashed', 'settings.xml'),
        'default'  : 'trakt_access_token',
        'data'     : ['trakt_expires_at', 'trakt_refresh_token', 'trakt_access_token'],
        'activate' : 'Addon.OpenSettings(plugin.video.unleashed)'},
    'chains': {
        'name'     : 'Chains Reaction',
        'plugin'   : 'plugin.video.thechains',
        'saved'    : 'chains',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'chains_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thechains', 'settings.xml'),
        'default'  : 'trakt_access_token',
        'data'     : ['trakt_expires_at', 'trakt_refresh_token', 'trakt_access_token'],
        'activate' : 'Addon.OpenSettings(plugin.video.thechains)'},
    'md': {
        'name'     : 'Magic Dragon',
        'plugin'   : 'plugin.video.magicdragon',
        'saved'    : 'md',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.magicdragon'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.magicdragon', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.magicdragon', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'md_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.magicdragon', 'settings.xml'),
        'default'  : 'trakt_access_token',
        'data'     : ['trakt_expires_at', 'trakt_refresh_token', 'trakt_access_token'],
        'activate' : 'Addon.OpenSettings(plugin.video.magicdragon)'},
    'asgard': {
        'name'     : 'Asgard',
        'plugin'   : 'plugin.video.asgard',
        'saved'    : 'asgard',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'asgard_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.asgard', 'settings.xml'),
        'default'  : 'trakt_access_token',
        'data'     : ['trakt_expires_at', 'trakt_refresh_token', 'trakt_access_token'],
        'activate' : 'Addon.OpenSettings(plugin.video.asgard)'},
    'patriot': {
        'name'     : 'Patriot',
        'plugin'   : 'plugin.video.patriot',
        'saved'    : 'patriot',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.patriot'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.patriot', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.patriot', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'patriot_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.patriot', 'settings.xml'),
        'default'  : 'trakt_access_token',
        'data'     : ['trakt_expires_at', 'trakt_refresh_token', 'trakt_access_token'],
        'activate' : 'Addon.OpenSettings(plugin.video.patriot)'},
    'blackl': {
        'name'     : 'Black Lightning',
        'plugin'   : 'plugin.video.blacklightning',
        'saved'    : 'blackl',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.blacklightning'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.blacklightning', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.blacklightning', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'blackl_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.blacklightning', 'settings.xml'),
        'default'  : 'trakt_access_token',
        'data'     : ['trakt_expires_at', 'trakt_refresh_token', 'trakt_access_token'],
        'activate' : 'Addon.OpenSettings(plugin.video.blacklightning)'},
    'aliunde': {
        'name'     : 'Aliunde K19',
        'plugin'   : 'plugin.video.aliundek19',
        'saved'    : 'aliunde',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.aliundek19'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.aliundek19', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.aliundek19', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'aliunde_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.aliundek19', 'settings.xml'),
        'default'  : 'trakt_access_token',
        'data'     : ['trakt_expires_at', 'trakt_refresh_token', 'trakt_access_token'],
        'activate' : 'Addon.OpenSettings(plugin.video.aliundek19)'},
   'homelander': {
        'name'     : 'Homelander',
        'plugin'   : 'plugin.video.homelander',
        'saved'    : 'homelander',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.homelander'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.homelander', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.homelander', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'homelander_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.homelander', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.authed', 'trakt.user', 'trakt.token' 'trakt.refresh', 'trakt.client_id', 'trakt.client_secret'],
        'activate' : 'Addon.OpenSettings(plugin.video.homelander)'},
   'quicksilver': {
        'name'     : 'Quicksilver',
        'plugin'   : 'plugin.video.quicksilver',
        'saved'    : 'quicksilver',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.quicksilver'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.quicksilver', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.quicksilver', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'quicksilver_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.quicksilver', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.authed', 'trakt.user', 'trakt.token' 'trakt.refresh', 'trakt.client_id', 'trakt.client_secret'],
        'activate' : 'Addon.OpenSettings(plugin.video.quicksilver)'},
   'genocide': {
        'name'     : 'Chains Genocide',
        'plugin'   : 'plugin.video.chainsgenocide',
        'saved'    : 'chainsgenocide',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.chainsgenocide'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.chainsgenocide', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.chainsgenocide', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'chainsgenocide_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.chainsgenocide', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.authed', 'trakt.user', 'trakt.token' 'trakt.refresh', 'trakt.client_id', 'trakt.client_secret'],
        'activate' : 'Addon.OpenSettings(plugin.video.chainsgenocide)'},
   'absolution': {
        'name'     : 'Absolution',
        'plugin'   : 'plugin.video.absolution',
        'saved'    : 'absolution',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.absolution'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.absolution', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.absolution', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'absolution_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.absolution', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.authed', 'trakt.user', 'trakt.token' 'trakt.refresh', 'trakt.client_id', 'trakt.client_secret'],
        'activate' : 'Addon.OpenSettings(plugin.video.absolution)'},
   'shazam': {
        'name'     : 'Shazam',
        'plugin'   : 'plugin.video.shazam',
        'saved'    : 'shazam',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shazam'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shazam', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.shazam', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'shazam_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.shazam', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.authed', 'trakt.user', 'trakt.token' 'trakt.refresh', 'trakt.client_id', 'trakt.client_secret'],
        'activate' : 'Addon.OpenSettings(plugin.video.shazam)'},
   'thecrew': {
        'name'     : 'The Crew',
        'plugin'   : 'plugin.video.thecrew',
        'saved'    : 'thecrew',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'thecrew_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thecrew', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
        'activate' : 'Addon.OpenSettings(plugin.video.thecrew)'},
   'nightwing': {
        'name'     : 'Nightwing',
        'plugin'   : 'plugin.video.nightwing',
        'saved'    : 'nightwing',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.nightwing'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.nightwing', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.nightwing', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'nightwing_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.nightwing', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.client_id', 'trakt.client_secret', 'trakt.refresh', 'trakt.token', 'trakt.user'],
        'activate' : 'Addon.OpenSettings(plugin.video.nightwing)'},
   'alvin': {
        'name'     : 'Alvin',
        'plugin'   : 'plugin.video.alvin',
        'saved'    : 'alvin',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.alvin'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.alvin', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.alvin', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'alvin_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.alvin', 'settings.xml'),
        'default'  : 'trakt.token',
        'data'     : ['trakt.client_id', 'trakt.client_secret', 'trakt.refresh', 'trakt.token', 'trakt.user'],
        'activate' : 'Addon.OpenSettings(plugin.video.alvin)'},
   'moria': {
        'name'     : 'Moria',
        'plugin'   : 'plugin.video.moria',
        'saved'    : 'moria',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.moria'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.moria', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.moria', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'moria_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.moria', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.authed', 'trakt.user', 'trakt.token' 'trakt.refresh', 'trakt.client_id', 'trakt.client_secret'],
        'activate' : 'Addon.OpenSettings(plugin.video.moria)'},
   'nine': {
        'name'     : '9 Lives',
        'plugin'   : 'plugin.video.nine',
        'saved'    : 'nine',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.nine'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.nine', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.nine', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'nine_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.nine', 'settings.xml'),
        'default'  : 'trakt.token',
        'data'     : ['trakt.authed', 'trakt.user', 'trakt.token' 'trakt.refresh', 'trakt.client_id', 'trakt.client_secret'],
        'activate' : 'Addon.OpenSettings(plugin.video.nine)'},
   'scrubs': {
        'name'     : 'Scrubs V2',
        'plugin'   : 'plugin.video.scrubsv2',
        'saved'    : 'scrubsv2',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.scrubsv2'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.scrubsv2/resources/images', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.scrubsv2/resources/images', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'scrubsv2_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.scrubsv2', 'settings.xml'),
        'default'  : 'trakt.user',
        'data'     : ['trakt.refresh', 'trakt.token', 'trakt.user'],
        'activate' : 'Addon.OpenSettings(plugin.video.scrubsv2)'},
   'tmdbhelper': {
        'name'     : 'TMDB Helper',
        'plugin'   : 'plugin.video.themoviedb.helper',
        'saved'    : 'tmdbhelper',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.themoviedb.helper'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.themoviedb.helper', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.themoviedb.helper', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'tmdbhelper_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.themoviedb.helper', 'settings.xml'),
        'default'  : 'trakt_token',
        'data'     : ['trakt_token'],
        'activate' : 'Addon.OpenSettings(plugin.video.themoviedb.helper)'},
   'trakt': {
        'name'     : 'Trakt Add-on',
        'plugin'   : 'script.trakt',
        'saved'    : 'trakt',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.trakt'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.trakt', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.trakt', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'trakt_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.trakt', 'settings.xml'),
        'default'  : 'user',
        'data'     : ['authorization', 'user'],
        'activate' : 'Addon.OpenSettings(script.trakt)'},
   'acctmgr': {
        'name'     : 'Account Manager',
        'plugin'   : 'script.module.accountmgr',
        'saved'    : 'acctmgr',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr', 'fanart.png'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'acctmgr_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.accountmgr', 'settings.xml'),
        'default'  : 'trakt.username',
        'data'     : ['trakt.client.id','trakt.client.secret', 'traktuserkey.enabled', 'trakt.expires', 'trakt.refresh', 'trakt.token', 'trakt.username'],
        'activate' : 'Addon.OpenSettings(script.module.accountmgr)'},
   'myact': {
        'name'     : 'My Accounts',
        'plugin'   : 'script.module.myaccounts',
        'saved'    : 'myact',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'fanart.png'),
        'file'     : os.path.join(CONFIG.TRAKTFOLD, 'myact_trakt'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.myaccounts', 'settings.xml'),
        'default'  : 'trakt.username',
        'data'     : ['trakt.client.id', 'trakt.client.secret', 'trakt.expires', 'trakt.refresh', 'trakt.token', 'trakt.username'],
        'activate' : 'Addon.OpenSettings(script.module.myaccounts)'}
}


def trakt_user(who):
    user = None
    if TRAKTID[who]:
        if os.path.exists(TRAKTID[who]['path']):
            try:
                add = tools.get_addon_by_id(TRAKTID[who]['plugin'])
                user = add.getSetting(TRAKTID[who]['default'])
            except:
                return None
    return user


def trakt_it(do, who):
    if not os.path.exists(CONFIG.ADDON_DATA):
        os.makedirs(CONFIG.ADDON_DATA)
    if not os.path.exists(CONFIG.TRAKTFOLD):
        os.makedirs(CONFIG.TRAKTFOLD)
    if who == 'all':
        for log in ORDER:
            if os.path.exists(TRAKTID[log]['path']):
                try:
                    addonid = tools.get_addon_by_id(TRAKTID[log]['plugin'])
                    default = TRAKTID[log]['default']
                    user = addonid.getSetting(default)
                    
                    update_trakt(do, log)
                except:
                    pass
            else:
                logging.log('[Trakt Data] {0}({1}) is not installed'.format(TRAKTID[log]['name'], TRAKTID[log]['plugin']), level=xbmc.LOGERROR)
        CONFIG.set_setting('traktnextsave', tools.get_date(days=3, formatted=True))
    else:
        if TRAKTID[who]:
            if os.path.exists(TRAKTID[who]['path']):
                update_trakt(do, who)
        else:
            logging.log('[Trakt Data] Invalid Entry: {0}'.format(who), level=xbmc.LOGERROR)

def trakt_it_revoke(do, who):
    if not os.path.exists(CONFIG.ADDON_DATA):
        os.makedirs(CONFIG.ADDON_DATA)
    if not os.path.exists(CONFIG.TRAKTFOLD):
        os.makedirs(CONFIG.TRAKTFOLD)
    if who == 'all':
        for log in ORDER:
            if os.path.exists(TRAKTID[log]['path']):
                try:
                    addonid = tools.get_addon_by_id(TRAKTID[log]['plugin'])
                    default = TRAKTID[log]['default']
                    user = addonid.getSetting(default)
                    
                    update_trakt(do, log)
                except:
                    pass
            else:
                logging.log('[Trakt Data] {0}({1}) is not installed'.format(TRAKTID[log]['name'], TRAKTID[log]['plugin']), level=xbmc.LOGERROR)
        CONFIG.set_setting('traktnextsave', tools.get_date(days=3, formatted=True))
    else:
        if TRAKTID[who]:
            if os.path.exists(TRAKTID[who]['path']):
                update_trakt(do, who)
        else:
            logging.log('[Trakt Data] Invalid Entry: {0}'.format(who), level=xbmc.LOGERROR)

def trakt_it_restore(do, who):
    if not os.path.exists(CONFIG.ADDON_DATA):
        os.makedirs(CONFIG.ADDON_DATA)
    if not os.path.exists(CONFIG.TRAKTFOLD):
        os.makedirs(CONFIG.TRAKTFOLD)
    if who == 'all':
        for log in ORDER:
            if os.path.exists(TRAKTID[log]['path']):
                try:
                    addonid = tools.get_addon_by_id(TRAKTID[log]['plugin'])
                    default = TRAKTID[log]['default']
                    user = addonid.getSetting(default)
                    
                    update_trakt(do, log)
                except:
                    pass
            else:
                logging.log('[Trakt Data] {0}({1}) is not installed'.format(TRAKTID[log]['name'], TRAKTID[log]['plugin']), level=xbmc.LOGERROR)
        CONFIG.set_setting('traktnextsave', tools.get_date(days=3, formatted=True))
    else:
        if TRAKTID[who]:
            if os.path.exists(TRAKTID[who]['path']):
                update_trakt(do, who)
        else:
            logging.log('[Trakt Data] Invalid Entry: {0}'.format(who), level=xbmc.LOGERROR)
    restore_trakt() #Restore API keys for all add-ons


def clear_saved(who, over=False):
    if who == 'all':
        for trakt in TRAKTID:
            clear_saved(trakt,  True)
    elif TRAKTID[who]:
        file = TRAKTID[who]['file']
        if os.path.exists(file):
            os.remove(file)
    if not over:
        xbmc.executebuiltin('Container.Refresh()')


def update_trakt(do, who):
    file = TRAKTID[who]['file']
    settings = TRAKTID[who]['settings']
    data = TRAKTID[who]['data']
    addonid = tools.get_addon_by_id(TRAKTID[who]['plugin'])
    saved = TRAKTID[who]['saved']
    default = TRAKTID[who]['default']
    user = addonid.getSetting(default)
    suser = CONFIG.get_setting(saved)
    name = TRAKTID[who]['name']
    icon = TRAKTID[who]['icon']

    if do == 'update':
        if not user == '':
            try:
                root = ElementTree.Element(saved)
                
                for setting in data:
                    trakt = ElementTree.SubElement(root, 'trakt')
                    id = ElementTree.SubElement(trakt, 'id')
                    id.text = setting
                    value = ElementTree.SubElement(trakt, 'value')
                    value.text = addonid.getSetting(setting)
                  
                tree = ElementTree.ElementTree(root)
                tree.write(file)
                
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                logging.log('Trakt Data Saved for {0}'.format(name), level=xbmc.LOGINFO)
            except Exception as e:
                logging.log("[Trakt Data] Unable to Update {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else:
            logging.log('Trakt Data Not Registered for {0}'.format(name))
    elif do == 'restore':
        if os.path.exists(file):
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            try:
                for setting in root.findall('trakt'):
                    id = setting.find('id').text
                    value = setting.find('value').text
                    addonid.setSetting(id, value)
                
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                logging.log('Trakt Data Restored for {0}'.format(name), level=xbmc.LOGINFO)
            except Exception as e:
                logging.log("[Trakt Data] Unable to Restore {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else:
            logging.log('Trakt Data Not Found for {0}'.format(name))
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
                
                logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                                   '[COLOR {0}]Addon Data: Cleared![/COLOR]'.format(CONFIG.COLOR2),
                                   2000,
                                   icon)
            except Exception as e:
                logging.log("[Trakt Data] Unable to Clear Addon {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
    elif do == 'wipeaddon':
        logging.log('{0} SETTINGS: {1}'.format(name, settings))
        revoke_trakt() #Restore default API keys for all add-ons
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
                logging.log("[Trakt Data] Unable to Clear Addon {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
    xbmc.executebuiltin('Container.Refresh()')


def auto_update(who):
    if who == 'all':
        for log in TRAKTID:
            if os.path.exists(TRAKTID[log]['path']):
                auto_update(log)
    elif TRAKTID[who]:
        if os.path.exists(TRAKTID[who]['path']):
            u = trakt_user(who)
            su = CONFIG.get_setting(TRAKTID[who]['saved'])
            n = TRAKTID[who]['name']
            if not u or u == '':
                return
            elif su == '':
                trakt_it('update', who)
            elif not u == su:
                dialog = xbmcgui.Dialog()

                if dialog.yesno(CONFIG.ADDONTITLE,
                                    "Would you like to save the [COLOR {0}]Trakt Data[/COLOR] for [COLOR {1}]{2}[/COLOR]?".format(CONFIG.COLOR2, CONFIG.COLOR1, n),
                                    "Addon: [COLOR springgreen][B]{0}[/B][/COLOR]".format(u),
                                    "Saved:[/COLOR] [COLOR red][B]{0}[/B][/COLOR]".format(su) if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]',
                                    yeslabel="[B][COLOR springgreen]Save Data[/COLOR][/B]",
                                    nolabel="[B][COLOR red]No Cancel[/COLOR][/B]"):
                    trakt_it('update', who)
            else:
                trakt_it('update', who)


def import_list(who):
    if who == 'all':
        for log in TRAKTID:
            if os.path.exists(TRAKTID[log]['file']):
                import_list(log)
    elif TRAKTID[who]:
        if os.path.exists(TRAKTID[who]['file']):
            file = TRAKTID[who]['file']
            addonid = tools.get_addon_by_id(TRAKTID[who]['plugin'])
            saved = TRAKTID[who]['saved']
            default = TRAKTID[who]['default']
            suser = CONFIG.get_setting(saved)
            name = TRAKTID[who]['name']
            
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            for setting in root.findall('trakt'):
                id = setting.find('id').text
                value = setting.find('value').text
            
                addonid.setSetting(id, value)

            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                       '[COLOR {0}]Trakt Data: Imported![/COLOR]'.format(CONFIG.COLOR2))


def open_settings_trakt(who):
    addonid = tools.get_addon_by_id(TRAKTID[who]['plugin'])
    addonid.openSettings()

def revoke_trakt(): #Restore default API keys to all add-ons

    if xbmcvfs.exists(var.chk_seren) and var.setting('traktuserkey.enabled') == 'true': #Check if add-on is installed
        #Remove Account Mananger API keys from add-on
        f = open(var.path_seren,'r')
        data = f.read()
        f.close()
        client = data.replace(var.client_am,var.seren_client).replace(var.secret_am,var.seren_secret)
        f = open(var.path_seren,'w')
        f.write(client)
        f.close()
        
    if xbmcvfs.exists(var.chk_fen):
                        
        f = open(var.path_fen,'r')
        data = f.read()
        f.close()
        client = data.replace(var.client_am,var.fen_client).replace(var.secret_am,var.fen_secret)
        f = open(var.path_fen,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_coal):
                        
        f = open(var.path_coal,'r')
        data = f.read()
        f.close()
        client = data.replace(var.client_am,var.coal_client).replace(var.secret_am,var.coal_secret)
        f = open(var.path_coal,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_pov):

        f = open(var.path_pov,'r')
        data = f.read()
        f.close()
        client = data.replace(var.client_am,var.pov_client).replace(var.secret_am,var.pov_secret)
        f = open(var.path_pov,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_shadow):
                        
        f = open(var.path_shadow,'r')
        data = f.read()
        f.close()
        client = data.replace(var.client_am,var.shadow_client).replace(var.secret_am,var.shadow_secret)
        f = open(var.path_shadow,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_ghost):
                        
        f = open(var.path_ghost,'r')
        data = f.read()
        f.close()
        client = data.replace(var.client_am,var.ghost_client).replace(var.secret_am,var.ghost_secret)
        f = open(var.path_ghost,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_base):
                        
        f = open(var.path_base,'r')
        data = f.read()
        f.close()
        client = data.replace(var.client_am,var.base_client).replace(var.secret_am,var.base_secret)
        f = open(var.path_base,'w')
        f.write(client)
        f.close()
        
    if xbmcvfs.exists(var.chk_unleashed):
                        
        f = open(var.path_unleashed,'r')
        data = f.read()
        f.close()
        client = data.replace(var.client_am,var.unleashed_client).replace(var.secret_am,var.unleashed_secret)
        f = open(var.path_unleashed,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_chains):
                        
        f = open(var.path_chains,'r')
        data = f.read()
        f.close()
        client = data.replace(var.client_am,var.chains_client).replace(var.secret_am,var.chains_secret)
        f = open(var.path_chains,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_md):
                       
        f = open(var.path_md,'r')
        data = f.read()
        f.close()
        client = data.replace(var.client_am,var.md_client).replace(var.secret_am,var.md_secret)
        f = open(var.path_md,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_asgard):
                        
        f = open(var.path_asgard,'r')
        data = f.read()
        f.close()
        client = data.replace(var.client_am,var.asgard_client).replace(var.secret_am,var.asgard_secret)
        f = open(var.path_asgard,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_patriot):
                        
        f = open(var.path_patriot,'r')
        data = f.read()
        f.close()
        client = data.replace(var.client_am,var.patriot_client).replace(var.secret_am,var.patriot_secret)
        f = open(var.path_patriot,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_blackl):
                        
        f = open(var.path_blackl,'r')
        data = f.read()
        f.close()
        client = data.replace(var.client_am,var.blackl_client).replace(var.secret_am,var.blackl_secret)
        f = open(var.path_blackl,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_aliunde):
                        
        f = open(var.path_aliunde,'r')
        data = f.read()
        f.close()
        client = data.replace(var.client_am,var.aliunde_client).replace(var.secret_am,var.aliunde_secret)
        f = open(var.path_aliunde,'w')
        f.write(client)
        f.close
        
    if xbmcvfs.exists(var.chk_crew):

        f = open(var.path_crew,'r')
        data = f.read()
        f.close()
        client = data.replace(var.client_am,var.crew_client).replace(var.secret_am,var.crew_secret)
        f = open(var.path_crew,'w')
        f.write(client)
        f.close()
        
    if xbmcvfs.exists(var.chk_scrubs):
                        
        f = open(var.path_scrubs,'r')
        data = f.read()
        f.close()
        client = data.replace(var.client_am,var.scrubs_client).replace(var.secret_am,var.scrubs_secret)
        f = open(var.path_scrubs,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_tmdbh):
                
        f = open(var.path_tmdbh,'r')
        data = f.read()
        f.close()
        client = data.replace(var.client_am,var.tmdbh_client).replace(var.secret_am,var.tmdbh_secret)
        f = open(var.path_tmdbh,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_trakt):
                
        f = open(var.path_trakt,'r')
        data = f.read()
        f.close()
        client = data.replace(var.client_am,var.trakt_client).replace(var.secret_am,var.trakt_secret)
        f = open(var.path_trakt,'w')
        f.write(client)
        f.close()
        
    if xbmcvfs.exists(var.chk_myaccounts):

        f = open(var.path_myaccounts,'r')
        data = f.read()
        f.close()
        client = data.replace(var.client_am,var.myacts_client).replace(var.secret_am,var.myacts_secret)
        f = open(var.path_myaccounts,'w')
        f.write(client)
        f.close()
   
def restore_trakt(): #Restore API Keys to all add-ons

    if xbmcvfs.exists(var.chk_seren) and var.setting('traktuserkey.enabled') == 'true': #Check if add-on is installed
        #Insert Account Mananger API keys into add-on
        f = open(var.path_seren,'r')
        data = f.read()
        f.close()
        client = data.replace(var.seren_client,var.client_am).replace(var.seren_secret,var.secret_am)
        f = open(var.path_seren,'w')
        f.write(client)
        f.close()
        
    if xbmcvfs.exists(var.chk_fen):
                        
        f = open(var.path_fen,'r')
        data = f.read()
        f.close()
        client = data.replace(var.fen_client,var.client_am).replace(var.fen_secret,var.secret_am)
        f = open(var.path_fen,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_coal):
                        
        f = open(var.path_coal,'r')
        data = f.read()
        f.close()
        client = data.replace(var.coal_client,var.client_am).replace(var.coal_secret,var.secret_am)
        f = open(var.path_coal,'w')
        f.write(client)
        f.close()
        
    if xbmcvfs.exists(var.chk_pov):

        f = open(var.path_pov,'r')
        data = f.read()
        f.close()
        client = data.replace(var.pov_client,var.client_am).replace(var.pov_client,var.secret_am)
        f = open(var.path_pov,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_shadow):
                        
        f = open(var.path_shadow,'r')
        data = f.read()
        f.close()
        client = data.replace(var.shadow_client,var.client_am).replace(var.shadow_secret,var.secret_am)
        f = open(var.path_shadow,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_ghost):
                        
        f = open(var.path_ghost,'r')
        data = f.read()
        f.close()
        client = data.replace(var.ghost_client,var.client_am).replace(var.ghost_secret,var.secret_am)
        f = open(var.path_ghost,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_base):
                        
        f = open(var.path_base,'r')
        data = f.read()
        f.close()
        client = data.replace(var.base_client,var.client_am).replace(var.base_secret,var.secret_am)
        f = open(var.path_base,'w')
        f.write(client)
        f.close()
        
    if xbmcvfs.exists(var.chk_unleashed):
                        
        f = open(var.path_unleashed,'r')
        data = f.read()
        f.close()
        client = data.replace(var.unleashed_client,var.client_am).replace(var.unleashed_secret,var.secret_am)
        f = open(var.path_unleashed,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_chains):
                        
        f = open(var.path_chains,'r')
        data = f.read()
        f.close()
        client = data.replace(var.chains_client,var.client_am).replace(var.chains_secret,var.secret_am)
        f = open(var.path_chains,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_md):
                       
        f = open(var.path_md,'r')
        data = f.read()
        f.close()
        client = data.replace(var.md_client,var.client_am).replace(var.md_client,var.secret_am)
        f = open(var.path_md,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_asgard):
                        
        f = open(var.path_asgard,'r')
        data = f.read()
        f.close()
        client = data.replace(var.asgard_client,var.client_am).replace(var.asgard_secret,var.secret_am)
        f = open(var.path_asgard,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_patriot):
                        
        f = open(var.path_patriot,'r')
        data = f.read()
        f.close()
        client = data.replace(var.patriot_client,var.client_am).replace(var.patriot_secret,var.secret_am)
        f = open(var.path_patriot,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_blackl):
                        
        f = open(var.path_blackl,'r')
        data = f.read()
        f.close()
        client = data.replace(var.blackl_client,var.client_am).replace(var.blackl_secret,var.secret_am)
        f = open(var.path_blackl,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_aliunde):
                        
        f = open(var.path_aliunde,'r')
        data = f.read()
        f.close()
        client = data.replace(var.aliunde_client,var.client_am).replace(var.aliunde_secret,var.secret_am)
        f = open(var.path_aliunde,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_crew):

        f = open(var.path_crew,'r')
        data = f.read()
        f.close()
        client = data.replace(var.crew_client,var.client_am).replace(var.crew_client,var.secret_am)
        f = open(var.path_crew,'w')
        f.write(client)
        f.close()
        
    if xbmcvfs.exists(var.chk_scrubs):
                        
        f = open(var.path_scrubs,'r')
        data = f.read()
        f.close()
        client = data.replace(var.scrubs_client,var.client_am).replace(var.scrubs_secret,var.secret_am)
        f = open(var.path_scrubs,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_tmdbh):
                
        f = open(var.path_tmdbh,'r')
        data = f.read()
        f.close()
        client = data.replace(var.tmdbh_client,var.client_am).replace(var.tmdbh_secret,var.secret_am)
        f = open(var.path_tmdbh,'w')
        f.write(client)
        f.close()

    if xbmcvfs.exists(var.chk_trakt):
                
        f = open(var.path_trakt,'r')
        data = f.read()
        f.close()
        client = data.replace(var.trakt_client,var.client_am).replace(var.trakt_secret,var.secret_am)
        f = open(var.path_trakt,'w')
        f.write(client)
        f.close()
        
    if xbmcvfs.exists(var.chk_myaccounts):

        f = open(var.path_myaccounts,'r')
        data = f.read()
        f.close()
        client = data.replace(var.myacts_client,var.client_am).replace(var.myacts_secret,var.secret_am)
        f = open(var.path_myaccounts,'w')
        f.write(client)
        f.close()
