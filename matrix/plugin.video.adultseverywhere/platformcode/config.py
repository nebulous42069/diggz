# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Balandro - Config
# ------------------------------------------------------------

import os, sys, re
import xbmc, xbmcaddon, xbmcvfs  
if sys.version_info[0] >= 3:
    translatePath = xbmcvfs.translatePath
    long = int
    unicode = str
else:
    translatePath = xbmc.translatePath   

# GLOBAL ADDON VARIABLES
# ======================

__base_url = sys.argv[0]

__addon_name = 'Balandro'
__addon_id = __base_url.replace('plugin://','').replace('/','')

__settings__ = xbmcaddon.Addon(id=__addon_id)


# HELPERS
# =======

def build_url(item):
    return __base_url + '?' + item.tourl()

def build_RunPlugin(item):
    return 'RunPlugin(%s?%s)' % (__base_url, item.tourl())

def build_ContainerRefresh(item):
    return 'Container.Refresh(%s?%s)' % (__base_url, item.tourl())

def build_ContainerUpdate(item, replace=False):
    if replace: # reset the path history
        return 'Container.Update(%s?%s, replace)' % (__base_url, item.tourl())
    else:
        return 'Container.Update(%s?%s)' % (__base_url, item.tourl())


def get_runtime_path():
    return translatePath(__settings__.getAddonInfo('Path'))

def get_data_path():
    dev = translatePath(__settings__.getAddonInfo('Profile'))
    if not os.path.exists(dev): os.makedirs(dev)
    return dev


def get_addon_version(with_fix=True):
    if with_fix:
        return __settings__.getAddonInfo('version') + get_addon_version_fix()
    else:
        return __settings__.getAddonInfo('version')

def get_addon_version_fix():
    try:
        last_fix_json = os.path.join(get_runtime_path(), 'last_fix.json')   # información de la versión fixeada del usuario
        if os.path.exists(last_fix_json):
            with open(last_fix_json, 'r') as f: data=f.read(); f.close()
            fix = re.findall('"fix_version"\s*:\s*(\d+)', data)
            if fix:
                return '.fix%s' % fix[0]
    except:
        pass
    return ''


def get_thumb(thumb_name, theme='default', mtype='themes'):
    ficheros = {
        'movie': 'clapboard', 'tvshow': 'tv', 'documentary': 'genius', 'search': 'magnifyingglass', 
        'videolibrary': 'star', 'downloads': 'download', 'settings': 'settings', 
        'hot': 'bolt', 'help': 'help', 'genres': 'swatches'
    }
    path = os.path.join(get_runtime_path(), 'resources', 'media', mtype, theme, ficheros.get(thumb_name, thumb_name) + '.png')
    if not os.path.exists(path):
        path = os.path.join(get_runtime_path(), 'resources', 'media', mtype, theme, ficheros.get(thumb_name, thumb_name) + '.jpg')
    if os.path.exists(path): return path
    return ''

def get_localized_category(categ):
    categories = {'movie': 'Películas', 'tvshow': 'Series', 
                  'documentary': 'Documentales', 'vos': 'Versiones originales',
                  'anime': 'Anime', 'adult': 'Adultos',
                  'direct': 'Directos', 'torrent': 'Torrents'}
    return categories[categ] if categ in categories else categ



# FUNCIONES DE USO COMÚN
# ======================

# Eliminar tags de color de un texto
def quitar_colores(texto):
    return re.sub(r'\[COLOR [^\]]*\]', '', texto.replace('[/COLOR]', '')).strip()

# Limpiar texto de acentos y otros caracteres para generar nombres de ficheros
def text_clean(txt, disallowed_chars = '[^a-zA-Z0-9\-_()\[\]. ]+', blank_char = ' '):
    import unicodedata
    try:
        txt = unicode(txt, 'utf-8')
    except: # unicode is a default on python 3 
        pass
    txt = unicodedata.normalize('NFKD', txt).encode('ascii', 'ignore')
    txt = txt.decode('utf-8').strip()
    if blank_char != ' ': txt = txt.replace(' ', blank_char)
    txt = re.sub(disallowed_chars, '', txt)
    return str(txt)

# This function will convert bytes to MB, GB, etc
def format_bytes(num):
    step_unit = 1000.0 #1024 bad the size
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit

# This function will convert seconds to HhMMm
def format_seconds_to_duration(seconds):
    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    if hours == 0: return '%dm' % minutes
    return '%dh%02dm' % (hours, minutes)


# PARÁMETROS CONFIGURABLES
# ========================

def get_lang_preferences():
    # 0:no mostrar  1:primera opción  2:segunda opción  3:tercera
    pref_esp = get_setting('preferencia_idioma_esp', default='1')
    pref_lat = get_setting('preferencia_idioma_lat', default='2')
    pref_vos = get_setting('preferencia_idioma_vos', default='3')
    return {'Esp': pref_esp, 'Lat': pref_lat, 'VO': pref_vos}


def get_setting(name, channel="", server="", default=None):
    """
    Retorna el valor de configuracion del parametro solicitado.

    Devuelve el valor del parametro 'name' en la configuración global o en la propia del canal o servidor.

    Si se especifica el nombre de un canal o servidor se guarda en la configuración global con un prefijo channel_ o server_.
    Los parametros channel y server no deben usarse simultaneamente.
    """
    if channel:
        name = 'channel_' + channel + '_' + name
    elif server:
        name = 'server_' + server + '_' + name

    value = __settings__.getSetting(name)
    if not value:
        return default

    # Translate Path if start with "special://"
    if value.startswith("special://"):
        value = translatePath(value)

    # hack para devolver el tipo correspondiente
    if value == "true":
        return True
    elif value == "false":
        return False
    else:
        # special case return as str
        if name in ["adult_password", "adult_aux_intro_password", "adult_aux_new_password1", "adult_aux_new_password2"]:
            return value
        elif name.startswith('search_last_'): # Para los settings de textos buscados no convertir si hay numéros (ej: 007)
            return str(value)
        elif name.endswith('_color'): # Para los settings acabados en _color, quitar tags de colores al devolver el valor (Ej: [COLOR gold]gold[/COLOR] => gold)
            return quitar_colores(value)
        else:
            try:
                value = int(value)
            except ValueError:
                pass
            return value


def set_setting(name, value, channel="", server=""):
    """
    Fija el valor de configuración del parametro indicado.

    Establece 'value' como el valor del parametro 'name' en la configuración global o en la propia del canal o servidor.
    Devuelve el valor cambiado o None si la asignación no se ha podido completar.

    Si se especifica el nombre de un canal o servidor se guarda en la configuración global con un prefijo channel_ o server_.
    Los parametros channel y server no deben usarse simultaneamente.
    """
    if channel:
        name = 'channel_' + channel + '_' + name
    elif server:
        name = 'server_' + server + '_' + name

    try:
        if isinstance(value, bool):
            if value:
                value = "true"
            else:
                value = "false"

        elif isinstance(value, (int, long)):
            value = str(value)

        __settings__.setSetting(name, value)

    except Exception as ex:
        from platformcode import logger
        logger.error("Error al convertir '%s' no se guarda el valor \n%s" % (name, ex))
        return None

    return value


# Obtener y guardar últimas búsquedas

def get_last_search(search_type):
    if get_setting('search_show_last', default=False):
        if search_type not in ['all', 'movie', 'tvshow', 'documentary', 'person']: search_type = 'all'
        last_search = get_setting('search_last_' + search_type, default='')
    else:
        last_search = ''

    return last_search

def set_last_search(search_type, tecleado):
    if search_type not in ['all', 'movie', 'tvshow', 'documentary', 'person']: search_type = 'all'
    set_setting('search_last_' + search_type, tecleado)


# CLASSES
# =======

class WebErrorException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
