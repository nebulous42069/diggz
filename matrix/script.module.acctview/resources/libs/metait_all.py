import xbmc
import xbmcaddon
import xbmcgui

import os
import time

from xml.etree import ElementTree

from resources.libs.common.config import CONFIG
from resources.libs.common import logging
from resources.libs.common import tools

ORDER = ['acctmgr',
         'seren',
         'ezra',
         'fen',
         'pov',
         'umb',
         'adina',
         'artemis',
         'dynasty',
         'loonatics',
         'thecrew',
         'homelander',
         'quicksilver',
         'genocide',
         'shazam',
         'thepromise',
         'nightwing',
         'alvin',
         'moria',
         'nine',
         'tmdbhelper',
         'embuary',
         'metah',
         'pvr',
         'myact',
         'yact']

DEBRIDID = {
    'seren': {
        'name'     : 'Seren',
        'plugin'   : 'plugin.video.seren',
        'saved'    : 'seren',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren/resources/images', 'ico-seren-3.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.seren/resources/images', 'fanart-seren-3.png'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'seren_meta'), #Backup location
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart.apikey',
        'default_omdb'  : 'omdb.apikey',
        'default_mdb'  : '',
        'default_imdb'  : '',
        'default_tmdb'  : 'tmdb.apikey',
        'default_tvdb'  : 'tvdb.apikey',
        'default_tmdb_user'  : '',
        'default_tmdb_pass'  : '',
        'default_tmdb_session'  : '',
        'data'     : ['tmdb.apikey', 'tvdb.apikey', 'omdb.apikey', 'fanart.apikey'],
        'activate' : 'Addon.OpenSettings(plugin.video.seren)'},
    'ezra': {
        'name'     : 'Ezra',
        'plugin'   : 'plugin.video.ezra',
        'saved'    : 'ezra',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra', 'fanart.png'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'ezra_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.ezra', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart_client_key',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : 'imdb_user',
        'default_tvdb'  : '',
        'default_tmdb'  : 'tmdb_api',
        'default_tmdb_user'  : '',
        'default_tmdb_pass'  : '',
        'default_tmdb_session'  : '',
        'data'     : ['tmdb_api', 'imdb_user', 'fanart_client_key'],
        'activate' : 'Addon.OpenSettings(plugin.video.ezra)'},
    'fen': {
        'name'     : 'Fen',
        'plugin'   : 'plugin.video.fen',
        'saved'    : 'fen',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_fanart.png'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'fen_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fen', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart_client_key',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : 'imdb_user',
        'default_tvdb'  : '',
        'default_tmdb'  : 'tmdb_api',
        'default_tmdb_user'  : '',
        'default_tmdb_pass'  : '',
        'default_tmdb_session'  : '',
        'data'     : ['tmdb_api', 'imdb_user', 'fanart_client_key'],
        'activate' : 'Addon.OpenSettings(plugin.video.fen)'},
    'pov': {
        'name'     : 'POV',
        'plugin'   : 'plugin.video.pov',
        'saved'    : 'pov',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.pov'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.pov', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.pov', 'fanart.png'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'pov_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.pov', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart_client_key',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : '',
        'default_tvdb'  : '',
        'default_tmdb'  : 'tmdb_api',
        'default_tmdb_user'  : '',
        'default_tmdb_pass'  : '',
        'default_tmdb_session'  : '',
        'data'     : ['tmdb_api', 'fanart_client_key'],
        'activate' : 'Addon.OpenSettings(plugin.video.pov)'},
    'umb': {
        'name'     : 'Umbrella',
        'plugin'   : 'plugin.video.umbrella',
        'saved'    : 'umb',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'umb_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.umbrella', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart_tv.api_key',
        'default_omdb'  : '',
        'default_mdb'  : 'mdblist.api',
        'default_imdb'  : 'imdbuser',
        'default_tvdb'  : '',
        'default_tmdb'  : 'tmdb.apikey',
        'default_tmdb_user'  : 'tmdbusername',
        'default_tmdb_pass'  : 'tmdbpassword',
        'default_tmdb_session'  : 'tmdb.sessionid',
        'data'     : ['tmdb.apikey', 'tmdbusername', 'tmdbpassword', 'tmdb.sessionid', 'imdbuser', 'mdblist.api', 'fanart_tv.api_key'],
        'activate' : 'Addon.OpenSettings(plugin.video.umbrella)'},
    'adina': {
        'name'     : 'Adina',
        'plugin'   : 'plugin.video.adina',
        'saved'    : 'adina',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.adina'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.adina', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.adina', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'adina_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.adina', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart_client_key',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : 'imdb_user',
        'default_tvdb'  : '',
        'default_tmdb'  : 'tmdb_api',
        'default_tmdb_user'  : '',
        'default_tmdb_pass'  : '',
        'default_tmdb_session'  : '',
        'data'     : ['tmdb_api', 'imdb_user', 'fanart_client_key'],
        'activate' : 'Addon.OpenSettings(plugin.video.adina)'},
    'artemis': {
        'name'     : 'Artemis',
        'plugin'   : 'plugin.video.artemis',
        'saved'    : 'artemis',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.artemis'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.artemis', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.artemis', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'artemis_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.artemis', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart_tv.api_key',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : 'imdb.user',
        'default_tvdb'  : '',
        'default_tmdb'  : 'tmdb.api.key',
        'default_tmdb_user'  : 'tmdb.username',
        'default_tmdb_pass'  : 'tmdb.password',
        'default_tmdb_session'  : 'tmdb.session_id',
        'data'     : ['tmdb.api.key', 'tmdb.username', 'tmdb.password', 'tmdb.session_id', 'imdb.user', 'fanart_tv.api_key'],
        'activate' : 'Addon.OpenSettings(plugin.video.artemis)'},
    'dynasty': {
        'name'     : 'Dynasty',
        'plugin'   : 'plugin.video.dynasty',
        'saved'    : 'dyna',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.dynasty'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.dynasty', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.dynasty', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'dyna_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.dynasty', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart_tv.api_key',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : 'imdb.user',
        'default_tvdb'  : '',
        'default_tmdb'  : 'tmdb.api.key',
        'default_tmdb_user'  : 'tmdb.username',
        'default_tmdb_pass'  : 'tmdb.password',
        'default_tmdb_session'  : 'tmdb.session_id',
        'data'     : ['tmdb.api.key', 'tmdb.username', 'tmdb.password', 'tmdb.session_id', 'imdb.user', 'fanart_tv.api_key'],
        'activate' : 'Addon.OpenSettings(plugin.video.dynasty)'},
    'loonatics': {
        'name'     : 'Loonatics Empire',
        'plugin'   : 'plugin.video.le',
        'saved'    : 'loon',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.le'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.le', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.le', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'loon_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.le', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart.tv.api.key',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : 'imdb.user',
        'default_tvdb'  : '',
        'default_tmdb'  : 'tmdb.api.key',
        'default_tmdb_user'  : 'tmdb.username',
        'default_tmdb_pass'  : 'tmdb.password',
        'default_tmdb_session'  : 'tmdb.session_id',
        'data'     : ['tmdb.api.key', 'tmdb.username', 'tmdb.password', 'tmdb.session_id', 'imdb.user', 'fanart.tv.api.key'],
        'activate' : 'Addon.OpenSettings(plugin.video.le)'},
   'thecrew': {
        'name'     : 'The Crew',
        'plugin'   : 'plugin.video.thecrew',
        'saved'    : 'thecrew',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.thecrew', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'thecrew_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thecrew', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart.tv.user',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : 'imdb.user',
        'default_tvdb'  : 'tvdb.user',
        'default_tmdb'  : 'tm.user',
        'default_tmdb_user'  : '',
        'default_tmdb_pass'  : '',
        'default_tmdb_session'  : '',
        'data'     : ['tm.user', 'tvdb.user', 'imdb.user', 'fanart.tv.user'],
        'activate' : 'Addon.OpenSettings(plugin.video.thecrew)'},
   'homelander': {
        'name'     : 'Homelander',
        'plugin'   : 'plugin.video.homelander',
        'saved'    : 'homelander',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.homelander'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.homelander', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.homelander', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'homelander_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.homelander', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart.tv.user',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : 'imdb.user',
        'default_tvdb'  : '',
        'default_tmdb'  : 'tm.user',
        'default_tmdb_user'  : '',
        'default_tmdb_pass'  : '',
        'default_tmdb_session'  : '',
        'data'     : ['tm.user', 'imdb.user', 'fanart.tv.user'],
        'activate' : 'Addon.OpenSettings(plugin.video.homelander)'},
   'quicksilver': {
        'name'     : 'Quicksilver',
        'plugin'   : 'plugin.video.quicksilver',
        'saved'    : 'quicksilver',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.quicksilver'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.quicksilver', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.quicksilver', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'quicksilver_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.quicksilver', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart.tv.user',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : 'imdb.user',
        'default_tvdb'  : '',
        'default_tmdb'  : 'tm.user',
        'default_tmdb_user'  : '',
        'default_tmdb_pass'  : '',
        'default_tmdb_session'  : '',
        'data'     : ['tm.user', 'imdb.user', 'fanart.tv.user'],
        'activate' : 'Addon.OpenSettings(plugin.video.quicksilver)'},
   'genocide': {
        'name'     : 'Chains Genocide',
        'plugin'   : 'plugin.video.chainsgenocide',
        'saved'    : 'chainsgenocide',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.chainsgenocide'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.chainsgenocide', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.chainsgenocide', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'chainsgenocide_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.chainsgenocide', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart.tv.user',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : 'imdb.user',
        'default_tvdb'  : '',
        'default_tmdb'  : 'tm.user',
        'default_tmdb_user'  : '',
        'default_tmdb_pass'  : '',
        'default_tmdb_session'  : '',
        'data'     : ['tm.user', 'imdb.user', 'fanart.tv.user'],
        'activate' : 'Addon.OpenSettings(plugin.video.chainsgenocide)'},
   'shazam': {
        'name'     : 'Shazam',
        'plugin'   : 'plugin.video.shazam',
        'saved'    : 'shazam',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shazam'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shazam', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.shazam', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'shazam_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.shazam', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart.tv.user',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : 'imdb.user',
        'default_tvdb'  : '',
        'default_tmdb'  : 'tm.user',
        'default_tmdb_user'  : '',
        'default_tmdb_pass'  : '',
        'default_tmdb_session'  : '',
        'data'     : ['tm.user', 'imdb.user', 'fanart.tv.user'],
        'activate' : 'Addon.OpenSettings(plugin.video.shazam)'},
   'thepromise': {
        'name'     : 'The Promise',
        'plugin'   : 'plugin.video.thepromise',
        'saved'    : 'thepromise',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thepromise'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thepromise', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.thepromise', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'thepromise_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thepromise', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart.tv.user',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : 'imdb.user',
        'default_tvdb'  : '',
        'default_tmdb'  : 'tm.user',
        'default_tmdb_user'  : '',
        'default_tmdb_pass'  : '',
        'default_tmdb_session'  : '',
        'data'     : ['tm.user', 'imdb.user', 'fanart.tv.user'],
        'activate' : 'Addon.OpenSettings(plugin.video.thepromise)'},
   'nightwing': {
        'name'     : 'Nightwing',
        'plugin'   : 'plugin.video.nightwing',
        'saved'    : 'nightwing',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.nightwing'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.nightwing', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.nightwing', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'nightwing_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.nightwing', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart.tv.user',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : 'imdb.user',
        'default_tvdb'  : '',
        'default_tmdb'  : 'tm.user',
        'default_tmdb_user'  : '',
        'default_tmdb_pass'  : '',
        'default_tmdb_session'  : '',
        'data'     : ['tm.user', 'imdb.user', 'fanart.tv.user'],
        'activate' : 'Addon.OpenSettings(plugin.video.nightwing)'},
   'alvin': {
        'name'     : 'Alvin',
        'plugin'   : 'plugin.video.alvin',
        'saved'    : 'alvin',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.alvin'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.alvin', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.alvin', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'alvin_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.alvin', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart.tv.user',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : 'imdb.user',
        'default_tvdb'  : '',
        'default_tmdb'  : 'tm.user',
        'default_tmdb_user'  : '',
        'default_tmdb_pass'  : '',
        'default_tmdb_session'  : '',
        'data'     : ['tm.user', 'imdb.user', 'fanart.tv.user'],
        'activate' : 'Addon.OpenSettings(plugin.video.alvin)'},
   'moria': {
        'name'     : 'Moria',
        'plugin'   : 'plugin.video.moria',
        'saved'    : 'moria',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.moria'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.moria', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.moria', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'moria_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.moria', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart.tv.user',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : 'imdb.user',
        'default_tvdb'  : '',
        'default_tmdb'  : 'tm.user',
        'default_tmdb_user'  : '',
        'default_tmdb_pass'  : '',
        'default_tmdb_session'  : '',
        'data'     : ['tm.user', 'imdb.user', 'fanart.tv.user'],
        'activate' : 'Addon.OpenSettings(plugin.video.moria)'},
   'nine': {
        'name'     : 'Nine Lives',
        'plugin'   : 'plugin.video.nine',
        'saved'    : 'nine',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.nine'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.nine', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.nine', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'nine_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.nine', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart.tv.user',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : 'imdb.user',
        'default_tvdb'  : '',
        'default_tmdb'  : 'tm.user',
        'default_tmdb_user'  : '',
        'default_tmdb_pass'  : '',
        'default_tmdb_session'  : '',
        'data'     : ['tm.user', 'imdb.user', 'fanart.tv.user'],
        'activate' : 'Addon.OpenSettings(plugin.video.nine)'},
   'tmdbhelper': {
        'name'     : 'TMDB Helper',
        'plugin'   : 'plugin.video.themoviedb.helper',
        'saved'    : 'tmdbhelper',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.themoviedb.helper'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.themoviedb.helper', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.themoviedb.helper', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'tmdbhelper_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.themoviedb.helper', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanarttv_clientkey',
        'default_omdb'  : 'omdb_apikey',
        'default_mdb'  : 'mdblist_apikey',
        'default_imdb'  : '',
        'default_tvdb'  : '',
        'default_tmdb'  : '',
        'default_tmdb_user'  : '',
        'default_tmdb_pass'  : '',
        'default_tmdb_session'  : '',
        'data'     : ['omdb_apikey', 'mdblist_apikey', 'fanarttv_clientkey'],
        'activate' : 'Addon.OpenSettings(plugin.video.themoviedb.helper)'},
    'embuary': {
        'name'     : 'Embuary Info',
        'plugin'   : 'script.embuary.info',
        'saved'    : 'embuary',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.embuary.info'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.embuary.info', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.embuary.info', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'embuary_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.embuary.info', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : '',
        'default_omdb'  : 'omdb_api_key',
        'default_mdb'  : '',
        'default_imdb'  : '',
        'default_tmdb'  : 'tmdb_api_key',
        'default_tvdb'  : '',
        'default_tmdb_user'  : '',
        'default_tmdb_pass'  : '',
        'default_tmdb_session'  : '',
        'data'     : ['tmdb_api_key', 'trakt_api_key', 'omdb_api_key', 'language_code', 'country_code', 'filter_shows', 'filter_movies', 'similar_movies_filter', 'filter_upcoming', 'filter_daydelta', 'cache_enabled'],
        'activate' : 'Addon.OpenSettings(script.embuary.info)'},
    'metah': {
        'name'     : 'Metahandler',
        'plugin'   : 'script.module.metahandler',
        'saved'    : 'metah',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.metahandler'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.metahandler', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.metahandler', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'metah_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.metahandler', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : '',
        'default_omdb'  : 'omdb_api_key',
        'default_mdb'  : '',
        'default_imdb'  : '',
        'default_tmdb'  : 'tmdb_api_key',
        'default_tvdb'  : 'tvdb_api_key',
        'default_tmdb_user'  : '',
        'default_tmdb_pass'  : '',
        'default_tmdb_session'  : '',
        'data'     : ['tmdb_api_key', 'omdb_api_key', 'tvdb_api_key', 'override_tmdb_key', 'override_omdb_key', 'override_tvdb_key', 'meta_folder_location', 'tmdb_language', 'tmdb_poster_size', 'tmdb_backdrop_size', 'omdbapi_fallback', 'tvdb_language'],
        'activate' : 'Addon.OpenSettings(script.module.metahandler)'},
    'pvr': {
        'name'     : 'PVR Artwork Module',
        'plugin'   : 'script.module.pvr.artwork',
        'saved'    : 'pvr',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.pvr.artwork'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.pvr.artwork', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.pvr.artwork', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'pvr_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.pvr.artwork', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart_apikey',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : '',
        'default_tmdb'  : 'tmdb_apikey',
        'default_tvdb'  : '',
        'default_tmdb_user'  : '',
        'default_tmdb_pass'  : '',
        'default_tmdb_session'  : '',
        'data'     : ['tmdb_apikey', 'fanart_apikey', 'use_tmdb', 'use_fanart_tv', 'prefer_fanart_tv'],
        'activate' : 'Addon.OpenSettings(script.module.pvr.artwork)'},
    'myact': {
        'name'     : 'My Accounts',
        'plugin'   : 'script.module.myaccounts',
        'saved'    : 'myact',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'fanart.png'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'myact_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.myaccounts', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart.tv.api.key',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : 'imdb.user',
        'default_tvdb'  : '',
        'default_tmdb'  : 'tmdb.api.key',
        'default_tmdb_user'  : 'tmdb.username',
        'default_tmdb_pass'  : 'tmdb.password',
        'default_tmdb_session'  : 'tmdb.session_id',
        'data'     : ['tmdb.api.key', 'tmdb.username', 'tmdb.password', 'tmdb.session_id', 'imdb.user', 'fanart.tv.api.key'],
        'activate' : 'Addon.OpenSettings(script.module.myaccounts)'},
    'yact': {
        'name'     : 'Your Accounts',
        'plugin'   : 'script.module.youraccounts',
        'saved'    : 'yact',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.youraccounts'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.youraccounts', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.youraccounts', 'fanart.png'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'yact_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.youraccounts', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart.tv.api.key',
        'default_omdb'  : '',
        'default_mdb'  : '',
        'default_imdb'  : 'imdb.user',
        'default_tvdb'  : '',
        'default_tmdb'  : 'tmdb.api.key',
        'default_tmdb_user'  : 'tmdb.username',
        'default_tmdb_pass'  : 'tmdb.password',
        'default_tmdb_session'  : 'tmdb.session_id',
        'data'     : ['tmdb.api.key', 'tmdb.username', 'tmdb.password', 'tmdb.session_id', 'imdb.user', 'fanart.tv.api.key'],
        'activate' : 'Addon.OpenSettings(script.module.youraccounts)'},
    'acctmgr': {
        'name'     : 'Account Manager',
        'plugin'   : 'script.module.accountmgr',
        'saved'    : 'acctmgr',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr', 'fanart.png'),
        'file'     : os.path.join(CONFIG.METAFOLD, 'acctmgr_meta'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.accountmgr', 'settings.xml'),
        'default'  : '',
        'default_fanart'  : 'fanart.tv.api.key',
        'default_omdb'  : 'omdb.api.key',
        'default_mdb'  : 'mdb.api.key',
        'default_imdb'  : 'imdb.user',
        'default_tvdb'  : 'tvdb.api.key',
        'default_tmdb'  : 'tmdb.api.key',
        'default_tmdb_user'  : 'tmdb.username',
        'default_tmdb_pass'  : 'tmdb.password',
        'default_tmdb_session'  : 'tmdb.session_id',
        'data'     : ['tmdb.api.key', 'tmdb.username', 'tmdb.password', 'tmdb.session_id', 'imdb.user', 'tvdb.api.key', 'omdb.api.key', 'mdb.api.key', 'fanart.tv.api.key'],
        'activate' : 'Addon.OpenSettings(script.module.accountmgr)'}
}
    
def debrid_user_fanart(who):
    user_fanart = None
    if DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            try:
                add = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
                user_fanart = add.getSetting(DEBRIDID[who]['default_fanart'])
            except:
                pass
    return user_fanart

def debrid_user_omdb(who):
    user_omdb = None
    if DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            try:
                add = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
                user_omdb = add.getSetting(DEBRIDID[who]['default_omdb'])
            except:
                pass
    return user_omdb

def debrid_user_mdb(who):
    user_mdb = None
    if DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            try:
                add = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
                user_mdb = add.getSetting(DEBRIDID[who]['default_mdb'])
            except:
                pass
    return user_mdb

def debrid_user_imdb(who):
    user_imdb = None
    if DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            try:
                add = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
                user_imdb = add.getSetting(DEBRIDID[who]['default_imdb'])
            except:
                pass
    return user_imdb

def debrid_user_tvdb(who):
    user_tvdb = None
    if DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            try:
                add = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
                user_tvdb = add.getSetting(DEBRIDID[who]['default_tvdb'])
            except:
                pass
    return user_tvdb

def debrid_user_tmdb(who):
    user_tmdb = None
    if DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            try:
                add = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
                user_tmdb = add.getSetting(DEBRIDID[who]['default_tmdb'])
            except:
                pass
    return user_tmdb

def debrid_user_tmdb_user(who):
    user_tmdb_user = None
    if DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            try:
                add = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
                user_tmdb_user = add.getSetting(DEBRIDID[who]['default_tmdb_user'])
            except:
                pass
    return user_tmdb_user

def debrid_user_tmdb_pass(who):
    user_tmdb_pass = None
    if DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            try:
                add = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
                user_tmdb_pass = add.getSetting(DEBRIDID[who]['default_tmdb_pass'])
            except:
                pass
    return user_tmdb_pass

def debrid_user_tmdb_session(who):
    user_tmdb_session = None
    if DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            try:
                add = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
                user_tmdb_session = add.getSetting(DEBRIDID[who]['default_tmdb_session'])
            except:
                pass
    return user_tmdb_session

def debrid_it(do, who):
    if not os.path.exists(CONFIG.ADDON_DATA):
        os.makedirs(CONFIG.ADDON_DATA)
    if not os.path.exists(CONFIG.METAFOLD):
        os.makedirs(CONFIG.METAFOLD)
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
    
    revoke_meta() #Restore default API keys for all add-ons

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

def revoke_meta():

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
            addon = xbmcaddon.Addon("plugin.video.Thecrew")
            addon.setSetting("fanart.tv.user", var.crew_fan)                        
            addon = xbmcaddon.Addon("plugin.video.thecrew")
            addon.setSetting("tm.user", var.crew_tmdb)
        except:
            pass