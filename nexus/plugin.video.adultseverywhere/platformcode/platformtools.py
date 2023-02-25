# -*- coding: utf-8 -*-

import sys, os, re
import xbmc, xbmcgui, xbmcplugin, xbmcvfs

from platformcode import config, logger
from core.item import Item

PY3 = False

if sys.version_info[0] >= 3:
    translatePath = xbmcvfs.translatePath
    basestring = str
    from urllib.parse import quote_plus
    PY3 = True
else:
    translatePath = xbmc.translatePath   
    from urllib import quote_plus

color_alert = config.get_setting('notification_alert_color', default='red')
color_infor = config.get_setting('notification_infor_color', default='pink')
color_adver = config.get_setting('notification_adver_color', default='violet')
color_avis  = config.get_setting('notification_avis_color', default='yellow')
color_exec  = config.get_setting('notification_exec_color', default='cyan')


# Diálogos de Kodi

def compat(line1, line2, line3):
    message = line1
    if line2:
        message += '\n' + line2
    if line3:
        message += '\n' + line3
    return message

# ~  def compat(**kwargs):
    # ~  message = '\n'.join([line for line in kwargs.values()])
    # ~  return message


def dialog_ok(heading, line1, line2="", line3=""):
    return xbmcgui.Dialog().ok(heading, compat(line1=line1, line2=line2, line3=line3))


def dialog_notification(heading, message, icon=0, time=5000, sound=None):
    if sound is None: sound = config.get_setting('notification_beep', default=True)
    dialog = xbmcgui.Dialog()
    try:
        l_icono = xbmcgui.NOTIFICATION_INFO, xbmcgui.NOTIFICATION_WARNING, xbmcgui.NOTIFICATION_ERROR
        dialog.notification(heading, message, l_icono[icon], time, sound)
    except:
        dialog_ok(heading, message)


def dialog_yesno(heading, line1, line2="", line3="", nolabel="No", yeslabel="Sí", autoclose=0, customlabel=None):
    # customlabel only on kodi 19
    dialog = xbmcgui.Dialog()
    if PY3:
        if autoclose > 0:
            return dialog.yesno(heading, compat(line1=line1, line2=line2, line3=line3), nolabel=nolabel, 
                            yeslabel=yeslabel, customlabel=customlabel, autoclose=autoclose)
        else:
            return dialog.yesno(heading, compat(line1=line1, line2=line2, line3=line3), nolabel=nolabel, 
                            yeslabel=yeslabel)
    else:
        if autoclose > 0:
            return dialog.yesno(heading, compat(line1=line1, line2=line2, line3=line3), nolabel=nolabel, 
                            yeslabel=yeslabel, autoclose=autoclose)
        else:
            return dialog.yesno(heading, compat(line1=line1, line2=line2, line3=line3), nolabel=nolabel, 
                            yeslabel=yeslabel)


def dialog_select(heading, _list, autoclose=0, preselect=-1, useDetails=False):
    return xbmcgui.Dialog().select(heading, _list, autoclose=autoclose, preselect=preselect, useDetails=useDetails)


def dialog_multiselect(heading, _list, autoclose=0, preselect=[], useDetails=False):
    return xbmcgui.Dialog().multiselect(heading, _list, autoclose=autoclose, preselect=preselect, useDetails=useDetails)


def dialog_progress(heading, line1, line2="", line3=""):
    dialog = xbmcgui.DialogProgress()
    def compat(line1, line2, line3):
        message = line1
        if line2:
            message += '\n' + line2
        if line3:
            message += '\n' + line3
        return message
    dialog.create(heading, compat(line1, line2, line3))
    return dialog

# ~  def dialog_progress(heading, line1, line2=" ", line3=" "):
    # ~  dialog = xbmcgui.DialogProgress()
    # ~  dialog.create(heading, compat(line1=line1, line2=line2, line3=line3))
    # ~  return dialog


def dialog_progress_bg(heading, message=""):
    try:
        dialog = xbmcgui.DialogProgressBG()
        dialog.create(heading, message)
        return dialog
    except:
        return dialog_progress(heading, message)


def dialog_input(default="", heading="", hidden=False):
    keyboard = xbmc.Keyboard(str(default), heading, hidden)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return keyboard.getText()
    else:
        return None


def dialog_numeric(_type, heading, default=""):
    dialog = xbmcgui.Dialog()
    d = dialog.numeric(_type, heading, default)
    return d


def dialog_textviewer(heading, text):
    return xbmcgui.Dialog().textviewer(heading, text)


def dialog_recaptcha(sitekey, referer):
    from platformcode import recaptcha
    return recaptcha.get_recaptcha_response(sitekey, referer)


# Para generar items para dialog_select, dialog_multiselect, cuando se llaman con useDetails=True
def listitem_to_select(title, subtitle='', thumbnail=''):
    it = xbmcgui.ListItem(title, subtitle)
    if thumbnail != '': it.setArt({ 'thumb': thumbnail })
    return it


# Renderización

def itemlist_refresh():
    xbmc.executebuiltin("Container.Refresh")

def itemlist_update(item, replace=False):
    xbmc.executebuiltin(config.build_ContainerUpdate(item, replace))


def render_no_items():
    xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=False, updateListing=False)

def render_items(itemlist, parent_item):
    """
    Función encargada de mostrar el itemlist en kodi, se pasa como parametros el itemlist y el item del que procede
    @type itemlist: list
    @param itemlist: lista de elementos a mostrar

    @type parent_item: item
    @param parent_item: elemento padre
    """

    # Si el itemlist no es un list salimos
    if not type(itemlist) == list: return

    # Si no hay ningun item, mostramos un aviso
    if not len(itemlist):
        itemlist.append(Item(title='[COLOR coral]Sin resultados[/COLOR]', thumbnail=config.get_thumb('roadblock')))

    # Asignamos variables
    handle = int(sys.argv[1])
    breadcrumb = parent_item.category if parent_item.category != '' else parent_item.channel

    # Formatear títulos de manera standard para los listados de pelis/series de los canales
    if parent_item.channel == 'search' or (parent_item.channel != 'tracking' and itemlist[0].contentType in ['movie', 'tvshow']): #, 'season', 'episode'
        itemlist = formatear_titulos(itemlist)

    # Colores personalizados para menú contextual
    colores = {}
    colores['tracking'] = config.get_setting('context_tracking_color', default='blue')
    colores['search_exact'] = config.get_setting('context_search_exact_color', default='gold')
    colores['search_similar'] = config.get_setting('context_search_similar_color', default='yellow')
    colores['download'] = config.get_setting('context_download_color', default='orange')
    colores['trailer'] = config.get_setting('context_trailer_color', default='pink')

    # Recorremos el itemlist
    for item in itemlist:
        #logger.debug(item)

        # Si no hay action o es findvideos/play, folder=False pq no se va a devolver ningún listado
        if item.action in ['findvideos', 'play', '']: item.folder = False

        # Si el item no contiene categoría, le ponemos la del item padre
        if item.category == '': item.category = parent_item.category

        # Si hay color se aplica al título y se suprime el tag para que no se arrastre
        if item.text_color != '': 
            item.title = '[COLOR %s]%s[/COLOR]' % (item.text_color, item.title)
            item.__dict__.pop('text_color')

        # Creamos el listitem
        listitem = xbmcgui.ListItem(item.title)

        # Añadimos los infoLabels
        set_infolabels(listitem, item)

        # No arrastrar plot si no es una peli/serie/temporada/episodio
        if item.plot and item.contentType not in ['movie', 'tvshow', 'season', 'episode']:
            try:
                item.__dict__['infoLabels'].pop('plot')
            except: pass                

        # Montamos el menu contextual y se suprime el tag para que no se arrastre
        context_commands = set_context_commands(item, parent_item, colores)
        listitem.addContextMenuItems(context_commands)
        if item.context: item.__dict__.pop('context')

        # IsPlayable necesario con setResolvedUrl para recibir un "id" en sys.argv[1] (sino recibiría -1)
        if item.action == 'findvideos': 
            listitem.setProperty('IsPlayable', 'true')
            if item.channel == 'tracking':
                # Generar url con los datos mínimos pq Kodi indexa con la url exacta en la tabla files.
                # De esta manera, aunque se cambien title,infoLabels,thumbnail,etc, la url se mantendrá igual
                # y no se perderán las marcas de visto/no visto propias de Kodi.
                it_minimo = Item( channel = 'tracking', action = 'findvideos', folder = False, title='',
                                  contentType = item.contentType, infoLabels = {'tmdb_id': item.infoLabels['tmdb_id']} )
                if item.contentType == 'episode':
                    it_minimo.infoLabels['season'] = item.infoLabels['season']
                    it_minimo.infoLabels['episode'] = item.infoLabels['episode']

        if item.action == 'findvideos' and item.channel == 'tracking':
            item_url = config.build_url(it_minimo)
        else:
            item_url = config.build_url(item)

        xbmcplugin.addDirectoryItem(handle=handle, url=item_url, listitem=listitem, isFolder=item.folder)


    # Fijar los tipos de vistas...
    if parent_item.channel == 'mainmenu' or (parent_item.channel == 'tracking' and parent_item.action in ['mainlist','mainlist_listas']):
        xbmcplugin.setContent(handle, '') # vista con: Lista amplia, Muro de iconos
    elif parent_item.channel == 'tracking' and parent_item.action in ['mainlist_series', 'mainlist_episodios', 'serie_temporadas', 'serie_episodios']:
        xbmcplugin.setContent(handle, 'tvshows') # vista con: Lista, Cartel, Mays., Muro de información, Lista amplia, Muro, Pancarta, Fanart
    else:
        xbmcplugin.setContent(handle, 'movies') # vista con: Lista, Cartel, Mays., Muro de información, Lista amplia, Muro, Fanart

    # Fijamos el "breadcrumb"
    xbmcplugin.setPluginCategory(handle=handle, category=breadcrumb)

    # No ordenar items
    orden = xbmcplugin.SORT_METHOD_NONE
    if parent_item.channel == 'tracking':
        if parent_item.action == 'serie_temporadas': 
            orden = xbmcplugin.SORT_METHOD_TITLE
    xbmcplugin.addSortMethod(handle=handle, sortMethod=orden)

    # Cerramos el directorio
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

    # Fijar la vista
    if parent_item.channel == 'tracking':
        if parent_item.action == 'mainlist_pelis': viewmode = config.get_setting('tracking_viewmode_movies', default=0)
        elif parent_item.action == 'mainlist_series': viewmode = config.get_setting('tracking_viewmode_tvshows', default=0)
        elif parent_item.action == 'serie_temporadas': viewmode = config.get_setting('tracking_viewmode_seasons', default=0)
        elif parent_item.action == 'serie_episodios': viewmode = config.get_setting('tracking_viewmode_episodes', default=0)
        else: viewmode = 0
        if viewmode > 0:
            # ~ Lista(50), Cartel(51), Mays.(53), Muro de información(54), Lista amplia(55), Muro(500), Fanart(502)
            # ~ List(50), Poster(51), Shift(53), InfoWall(54), WideList(55), Wall(500), Fanart(502)
            viewmodes = [0, 50, 51, 53, 54, 55, 500, 502]
            xbmc.executebuiltin("Container.SetViewMode(%d)" % viewmodes[viewmode])

    logger.info('FINAL render_items')


def set_infolabels(listitem, item, player=False):
    """
    Metodo para pasar la informacion al listitem (ver tmdb.set_InfoLabels() )
    item.infoLabels es un dicionario con los pares de clave/valor descritos en:
    http://mirrors.xbmc.org/docs/python-docs/14.x-helix/xbmcgui.html#ListItem-setInfo
    @param listitem: objeto xbmcgui.ListItem
    @type listitem: xbmcgui.ListItem
    @param item: objeto Item que representa a una pelicula, serie o capitulo
    @type item: item
    """

    # values icon, thumb or poster are skin dependent.. so we set all to avoid problems. if not exists thumb it's used icon value
    icon_image = "DefaultFolder.png" if item.folder else "DefaultVideo.png"
    poster_image = item.poster if item.poster != '' else item.thumbnail
    listitem.setArt({'icon': icon_image, 'thumb': item.thumbnail, 'poster': poster_image, 'fanart': item.fanart})

    # Para evitar algunas acciones de kodi en menú contextual (Play, Mark as watched, ...)
    if not item.folder and item.action not in ['findvideos', 'play'] and not item.infoLabels: return

    if item.infoLabels:
        if 'mediatype' not in item.infoLabels and item.contentType != '':
            item.infoLabels['mediatype'] = item.contentType  # "video", "movie", "tvshow", "season", "episode" or "musicvideo"
        # ~ if item.contentExtra == 'documentary': item.infoLabels['mediatype'] = 'video'
        # Descartar infoLabels no reconocidos (https://kodi.wiki/view/InfoLabels)
        nflbls = item.infoLabels.copy()
        descartes = ['tmdb_id', 'tvdb_id', 'imdb_id', 'type', 'filtro', 'quality', 'video', 
                     'popularity', 'homepage', 'budget', 'revenue', 'in_production', 'original_language',
                     'fanart', 'thumbnail', 'poster_path', 'release_date', 'last_air_date',
                     'number_of_episodes', 'number_of_seasons',
                     'temporada_air_date', 'temporada_nombre', 'temporada_num_episodios', 'temporada_poster', 'temporada_sinopsis',
                     'temporada_crew', 'temporada_cast',
                     'episodio_sinopsis', 'episodio_imagen', 'episodio_air_date', 'episodio_vote_count', 'episodio_vote_average',
                     'episodio_titulo', 'episodio_crew', 'episodio_guest_stars']
        for descarte in descartes:
            if descarte in nflbls: del nflbls[descarte]
        listitem.setInfo("video", nflbls)

    if player and not item.contentTitle:
        if item.fulltitle:
            listitem.setInfo("video", {"Title": item.fulltitle})
        else:
            listitem.setInfo("video", {"Title": item.title})

    elif not player:
        listitem.setInfo("video", {"Title": item.title})


def set_context_commands(item, parent_item, colores):
    """
    Función para generar los menus contextuales.
        1. Partiendo de los datos de item.context
             a. Metodo antiguo item.context tipo str separando las opciones por "|" (ejemplo: item.context = "1|2|3")
                (solo predefinidos)
            b. Metodo list: item.context es un list con las diferentes opciones del menu:
                - Predefinidos: Se cargara una opcion predefinida con un nombre.
                    item.context = ["1","2","3"]

                - dict(): Se cargara el item actual modificando los campos que se incluyan en el dict() en caso de
                    modificar los campos channel y action estos serán guardados en from_channel y from_action.
                    item.context = [{"title":"Nombre del menu", "action": "action del menu",
                                        "channel":"channel del menu"}, {...}]

        2. Añadiendo opciones segun criterios
            Se pueden añadir opciones al menu contextual a items que cumplan ciertas condiciones.


        3. Añadiendo opciones a todos los items
            Se pueden añadir opciones al menu contextual para todos los items

        4. Se pueden deshabilitar las opciones del menu contextual añadiendo un comando 'no_context' al item.context.
            Las opciones que Kodi, el skin u otro añadido añada al menu contextual no se pueden deshabilitar.

    @param item: elemento que contiene los menu contextuales
    @type item: item
    @param parent_item:
    @type parent_item: item
    """

    context_commands = []

    # Creamos un list con las diferentes opciones incluidas en item.context
    if type(item.context) == str:
        context = item.context.split("|")
    elif type(item.context) == list:
        context = item.context
    else:
        context = []

    for command in context:
        # Predefinidos
        if type(command) == str:
            if command == "no_context":
                return []

        # Formato dict
        if type(command) == dict:
            # Los parametros del dict, se sobreescriben al nuevo context_item en caso de sobreescribir "action" y
            # "channel", los datos originales se guardan en "from_action" y "from_channel"
            if "action" in command: command["from_action"] = item.action
            if "channel" in command: command["from_channel"] = item.channel

            # link_mode y link_item se usan para especificar como se genera la llamada (run y clone por defecto)
            # link_mode: refresh / update / replace / run (default)
            # link_item: new / clone (default)

            if parent_item.channel == 'tracking': titulo = '[COLOR %s]%s[/COLOR]' % (colores['tracking'], command['title'])
            elif '[/COLOR]' not in command['title']: titulo = '[COLOR blue]%s[/COLOR]' % command['title']
            else: titulo = command['title']

            link_mode = command.pop('link_mode') if 'link_mode' in command else 'run'
            link_item = command.pop('link_item') if 'link_item' in command else 'clone'

            c_it = item.clone(**command) if link_item == 'clone' else Item(**command)

            if link_mode == 'refresh':
                context_commands.append( (titulo, config.build_ContainerRefresh(c_it)) )
            elif link_mode == 'update':
                context_commands.append( (titulo, config.build_ContainerUpdate(c_it)) )
            elif link_mode == 'replace':
                context_commands.append( (titulo, config.build_ContainerUpdate(c_it, replace=True)) )
            else:
                context_commands.append( (titulo, config.build_RunPlugin(c_it)) )


    # Guardar seguimiento (preferidos)
    if not config.get_setting('mnu_simple', default=False):
        if config.get_setting('mnu_preferidos', default=True):
            if item.contentType in ['movie', 'tvshow', 'season', 'episode'] and item.contentExtra != 'documentary' \
               and parent_item.channel not in ['tracking', 'downloads', 'tmdblists']:
                tipo = {'movie':'película', 'tvshow':'serie', 'season':'temporada', 'episode':'episodio',}
                context_commands.append( ('[B][COLOR %s]Guardar %s en preferidos[/COLOR][/B]' % (colores['tracking'], tipo[item.contentType]), config.build_RunPlugin(
                    item.clone(channel="tracking", action="addFavourite", from_channel=item.channel, from_action=item.action))) )

    # Buscar misma peli/serie en otros canales
    if item.contentType in ['movie', 'tvshow'] and parent_item.channel != 'tmdblists': # and parent_item.channel != 'search':
        buscando = item.contentTitle if item.contentType == 'movie' else item.contentSerieName
        if item.contentExtra != 'documentary':
            infolabels = {'tmdb_id': item.infoLabels['tmdb_id']} if item.infoLabels['tmdb_id'] else {}
            item_search = Item(channel='search', action='search', buscando=buscando, search_type=item.contentType, from_channel=item.channel, infoLabels=infolabels)
            tipo_busqueda = 'en los canales' if item.channel == 'tracking' else 'en otros canales'
            context_commands.append( ('[COLOR %s]Buscar exacto %s[/COLOR]' % (colores['search_exact'], tipo_busqueda), config.build_ContainerUpdate(item_search)) )

        search_type = item.contentType if item.contentExtra != 'documentary' else 'documentary'
        item_search = Item(channel='search', action='search', buscando=buscando, search_type=search_type, from_channel='')
        context_commands.append( ('[COLOR %s]Buscar parecido en los canales[/COLOR]' % colores['search_similar'], config.build_ContainerUpdate(item_search)) )

    # Descargar vídeo
    if not config.get_setting('mnu_simple', default=False):
        if config.get_setting('mnu_preferidos', default=True):
            if item.channel != '' and item.action == 'findvideos' and parent_item.channel != 'downloads':
                context_commands.append( ('[COLOR %s]Descargar vídeo[/COLOR]' % colores['download'], config.build_RunPlugin(
                    item.clone(channel="downloads", action="save_download", from_channel=item.channel, from_action=item.action))) )

    # Buscar trailer
    if item.contentType in ['movie', 'tvshow'] and item.infoLabels['tmdb_id']:
        context_commands.append( ('[COLOR %s]Buscar tráiler[/COLOR]' % colores['trailer'], config.build_RunPlugin(
            item.clone(channel="actions", action="search_trailers"))) )

    # ~ # Mostrar info haciendo una nueva llamada a tmdb para recuperar más datos
    # ~ if item.contentType in ['movie', 'tvshow', 'season', 'episode'] and item.contentExtra != 'documentary':
        # ~ context_commands.append( ('[COLOR yellow]Información TMDB[/COLOR]', config.build_RunPlugin(
            # ~ item.clone(channel="actions", action="more_info",
                       # ~ from_channel=item.channel, from_action=item.action))) )

    # ~ context_commands = sorted(context_commands, key=lambda comand: comand[0])
    return context_commands


# Formatear elementos a mostrar

def formatear_enlace_play(item, colorear=False, colores={}):
    if item.server == '' or (item.server != '' and item.title != '' and item.quality == '' and item.language == '' and item.age == '' and item.other == ''):
        mantener_titulo = True
    else:
        mantener_titulo = False

    nombre = item.title if mantener_titulo else item.server.capitalize()
    if nombre == '': nombre = 'Indeterminado'

    if not colorear:
        titulo = nombre
        if item.quality != '': titulo += ' [%s]' % item.quality
        if item.language != '': titulo += ' [%s]' % item.language
        if item.age != '': titulo += ' [%s]' % item.age
        if item.other != '': titulo += ' [%s]' % item.other
    else:
        titulo = '[COLOR %s]%s[/COLOR]' % (colores['server'], nombre)
        if item.quality != '': titulo += ' [COLOR %s][%s][/COLOR]' % (colores['quality'], item.quality)
        if item.language != '': titulo += ' [COLOR %s][%s][/COLOR]' % (colores['language'], item.language)
        if item.age != '': titulo += ' [COLOR %s][%s][/COLOR]' % (colores['age'], item.age)
        if item.other != '': titulo += ' [COLOR %s][%s][/COLOR]' % (colores['other'], item.other)

    return titulo


# Formateo de enlaces devueltos por findvideos 
def formatear_enlaces_servidores(itemlist):
    colorear = config.get_setting('colorear_enlaces_play')
    colores = {}
    if colorear:
        colores['server'] = config.get_setting('play_server_color', default='gold')
        colores['quality'] = config.get_setting('play_quality_color', default='limegreen')
        colores['language'] = config.get_setting('play_language_color', default='red')
        colores['age'] = config.get_setting('play_age_color', default='deepskyblue')
        colores['other'] = config.get_setting('play_other_color', default='white')

    for it in itemlist:
        if it.action == 'play': it.title = formatear_enlace_play(it, colorear, colores)

    return itemlist


def formatear_titulo_peli_serie(item, colores={}, formato={}):
    tit = item.title if item.title != '' else item.contentTitle if item.contentType == 'movie' else item.contentSerieName
    if colores[item.contentType] == 'white':
        titulo = tit
    else:
        titulo = '[COLOR %s]%s[/COLOR]' % (colores[item.contentType], tit)

    if formato['show_year'] > 0 and 'year' in item.infoLabels and item.infoLabels['year'] not in ['','-']:
        if formato['show_year'] == 3 or \
           (formato['show_year'] == 1 and item.contentType == 'movie') or \
           (formato['show_year'] == 2 and item.contentType == 'tvshow'):
            titulo += ' [COLOR %s](%s)[/COLOR]' % (colores['year'], item.infoLabels['year'])

    if formato['info_order'] > 0:
        if formato['info_order'] in [1,3] and item.languages:
            titulo += ' [COLOR %s][%s][/COLOR]' % (colores['languages'], item.languages)
        if formato['info_order'] in [2,3,4] and item.qualities:
            titulo += ' [COLOR %s][%s][/COLOR]' % (colores['qualities'], item.qualities)
        if formato['info_order'] == 4 and item.languages:
            titulo += ' [COLOR %s][%s][/COLOR]' % (colores['languages'], item.languages)

    if item.fmt_sufijo != '':
        if item.fmt_sufijo in ['movie', 'tvshow']: # diferenciar pelis/series en búsquedas mixtas
            opciones = { 'movie': ['deepskyblue', 'película'], 'tvshow': ['hotpink', 'serie'] }
            titulo += ' [COLOR %s](%s)[/COLOR]' % (opciones[item.fmt_sufijo][0], opciones[item.fmt_sufijo][1])
        else:
            titulo += ' ' + item.fmt_sufijo

    return titulo

# Formateo de títulos en listados de pelis, series, temporadas, episodios
def formatear_titulos(itemlist):
    colores = {}
    colores['movie'] = config.get_setting('list_movie_color', default='white')
    colores['tvshow'] = config.get_setting('list_tvshow_color', default='white')
    colores['year'] = config.get_setting('list_year_color', default='gray')
    colores['qualities'] = config.get_setting('list_qualities_color', default='limegreen')
    colores['languages'] = config.get_setting('list_languages_color', default='red')

    formato = {}
    formato['show_year'] = config.get_setting('list_show_year', default=3) # "No|En películas|En series|En películas y series"
    formato['info_order'] = config.get_setting('list_info_order', default=3) # "Ninguno|Idiomas|Calidades|Idiomas y calidades|Calidades e idiomas"

    for it in itemlist:
        if it.contentType in ['movie', 'tvshow']:
            it.title = formatear_titulo_peli_serie(it, colores, formato)

    return itemlist


def developer_mode_check_findvideos(itemlist, parent_item):
    txt_log_servers = ''; checkeds = []
    txt_log_qualities = ''

    for it in itemlist:
        # ~ logger.debug(it)

        # Verificar servers desconocidos o no implementados
        apuntar = False
        if it.server == 'desconocido':
            # El canal no ha fijado server, y la url no se ha detectado de ningún server conocido
            apuntar = True
        elif it.server:
            # El canal ha fijado server sin verificar la url, y puede que no esté implementado
            if it.server not in checkeds:
                checkeds.append(it.server) # para no repetir servers ya verificados
                path = os.path.join(config.get_runtime_path(), 'servers', it.server + '.json')
                if not os.path.isfile(path):
                    apuntar = True

        if apuntar:
            txt_log_servers += 'Canal: %s Server: %s Url: %s' % (it.channel, it.server, it.url)
            if parent_item.contentType == 'movie':
                txt_log_servers += ' Película: %s' % (parent_item.contentTitle)
            else:
                txt_log_servers += ' Serie: %s Temporada %s Episodio %s' % (parent_item.contentSerieName, parent_item.contentSeason, parent_item.contentEpisodeNumber)
            txt_log_servers += os.linesep

        # Verificar calidades
        if it.quality == '' or it.quality_num == '': continue # Si no hay calidad o el canal no ha fijado el orden de calidades, nada a comprobar
        if it.quality_num == 0: # Orden de calidad no contemplado en el canal, apuntar para añadirlo
            txt_log_qualities += 'Calidad: %s Canal: %s Server: %s Url: %s' % (it.quality, it.channel, it.server, it.url)
            if parent_item.contentType == 'movie':
                txt_log_qualities += ' Película: %s' % (parent_item.contentTitle)
            else:
                txt_log_qualities += ' Serie: %s Temporada %s Episodio %s' % (parent_item.contentSerieName, parent_item.contentSeason, parent_item.contentEpisodeNumber)
            txt_log_qualities += os.linesep

    # Guardar en ficheros de log
    if txt_log_servers != '':
        dev_log = os.path.join(config.get_data_path(), 'servers_todo.log')
        if PY3 and not isinstance(txt_log_servers, bytes): txt_log_servers = txt_log_servers.encode('utf-8')
        with open(dev_log, 'wb') as f: f.write(txt_log_servers); f.close()

    if txt_log_qualities != '':
        dev_log = os.path.join(config.get_data_path(), 'qualities_todo.log')
        if PY3 and not isinstance(txt_log_qualities, bytes): txt_log_qualities = txt_log_qualities.encode('utf-8')
        with open(dev_log, 'wb') as f: f.write(txt_log_qualities); f.close()

    if os.path.isfile(os.path.join(config.get_runtime_path(), 'core', 'developertools.py')):
        try:
            from core import developertools
            developertools.developer_mode_check_findvideos(itemlist, parent_item)
        except:
            pass


# Reproducción
# Debe acabar haciendo play (o play_fake en su defecto) ya que en Kodi se considera playable
# itemlist: datos de los enlaces devueltos por findvideos (server, url, y opcionalmente quality,language,age,other) 
# parent_item: datos de la película/episodio (para usar sus infoLabels)
def play_from_itemlist(itemlist, parent_item):
    notification_d_ok = config.get_setting('notification_d_ok', default=True)

    if itemlist is None: # si viene de tracking y se cancela el play por no seleccionar ningún canal
        play_fake()
        return

    if parent_item.channel == 'tracking': # si viene de tracking, parent_item contiene los datos mínimos, recuperar infolabels
        from core import trackingtools
        trackingtools.set_infolabels_from_min(parent_item)
        # Para algunos servers (ej: gamovideo) se necesita la url para usar como referer
        if len(itemlist) > 0: parent_item.url = itemlist[0].parent_item_url

    # Reordenar/Filtrar enlaces (descartar servers inactivos, y según idioma)
    itemlist = list(filter(lambda it: it.action == 'play', itemlist)) # aunque por ahora no se usan action != 'play' en los findvideos

    if config.get_setting('developer_mode', default=False): developer_mode_check_findvideos(itemlist, parent_item)

    total_enlaces = len(itemlist)
    
    from core import servertools
    itemlist = servertools.filter_and_sort_by_quality(itemlist)
    itemlist = servertools.filter_and_sort_by_server(itemlist)
    itemlist = servertools.filter_and_sort_by_language(itemlist)

    if len(itemlist) == 0:
        if notification_d_ok:
            if total_enlaces > 0:
                 dialog_ok(config.__addon_name, 'Sin enlaces soportados')
            else:
                 dialog_ok(config.__addon_name, 'Sin enlaces disponibles')
        else:
            if total_enlaces > 0:
                dialog_notification(config.__addon_name, '[B][COLOR %s]Sin enlaces soportados[/COLOR][/B]' % color_alert)
            else:
                dialog_notification(config.__addon_name, '[B][COLOR %s]Sin enlaces disponibles[/COLOR][/B]' % color_exec)

        play_fake()
        return

    itemlist = formatear_enlaces_servidores(itemlist)

    erroneos = [] # para marcar los enlaces que fallan
    esperar_seleccion = True # indica si hay que mostrar el diálogo de selección al usuario. Sí a menos que haya autoplay.

    autoplay = config.get_setting('autoplay', default=False)
    if not autoplay and len(itemlist) == 1 and config.get_setting('autoplay_one_link', default=True): autoplay = True # Activar autoplay si solamente hay un enlace

    if autoplay:
        autoplay_max_links = config.get_setting('autoplay_max_links', default=10) # 0: sin límite, n: nº de enlaces a intentar
        autoplay_channels_discarded = config.get_setting('autoplay_channels_discarded', default='').lower().replace(' ', '').split(',')

    # Descartar autoplay en canales concretos que el usuario haya configurado
    if autoplay and itemlist[0].channel in autoplay_channels_discarded: autoplay = False

    if autoplay:
        esperar_seleccion = False
        num_opciones = float(len(itemlist)) # float para calcular porcentaje
        p_dialog = dialog_progress_bg('Reproducción con AutoPlay', 'Espere por favor...')
        ok_play = False
        for i, it in enumerate(itemlist):
            if autoplay_max_links > 0 and i >= autoplay_max_links: 
                esperar_seleccion = True
                break
            perc = int(i / num_opciones * 100)
            p_dialog.update(perc, 'Reproducción con AutoPlay', '%d/%d: %s' % (i+1, num_opciones, it.title))

            # Si el canal tiene play propio interpretar el itemlist que devuelve (Item o list)
            canal_play = __import__('channels.' + it.channel, fromlist=[''])
            if hasattr(canal_play, 'play'):
                itemlist_play = canal_play.play(it)

                if len(itemlist_play) > 0 and isinstance(itemlist_play[0], Item):
                    ok_play = play_video(itemlist_play[0], parent_item, autoplay=autoplay)

                elif len(itemlist_play) > 0 and isinstance(itemlist_play[0], list):
                    it.video_urls = itemlist_play
                    ok_play = play_video(it, parent_item, autoplay=autoplay)

                else:
                    ok_play = False

            else:
                ok_play = play_video(it, parent_item, autoplay=autoplay)

            if ok_play: 
                logger.debug('Autoplay, resuelto %s con url %s' % (it.server, it.url))
                break
            else:
                erroneos.append(i)
                logger.debug('Autoplay, falla %s con url %s' % (it.server, it.url))

            if xbmc.Monitor().abortRequested(): break

        p_dialog.close()
        if not ok_play:
            if esperar_seleccion: # si se ha llegado al límite de enlaces a intentar y todavía quedan, se muestra diálogo para selección del usuario
                dialog_notification('Autoplay sin éxito', 'Han fallado los %d primeros enlaces' % autoplay_max_links, time=3000)
            else:
                play_fake()
                txt = 'el enlace' if len(itemlist) == 1 else 'ningún enlace'
                if notification_d_ok:
                    dialog_ok(config.__addon_name, 'No se pudo reproducir ' + txt)
                else:
                    el_txt = ('[B][COLOR %s]No se pudo reproducir ' + txt) % color_exec
                    dialog_notification(config.__addon_name, el_txt + '[/COLOR][/B]')
        else:
            if len(itemlist) == 1: dialog_notification('Autoplay resuelto', it.title, time=2000, sound=False)
            else: dialog_notification('Autoplay resuelto', it.title)

    # Diálogo hasta que el usuario cancele o play ok
    if esperar_seleccion:
        while not xbmc.Monitor().abortRequested(): # (while True)
            opciones = []
            for i, it in enumerate(itemlist):
                if i in erroneos:
                    opciones.append('[I][COLOR gray]%s[/COLOR][/I]' % config.quitar_colores(it.title))
                else:
                    opciones.append(it.title)

            seleccion = dialog_select('Enlaces disponibles en %s' % itemlist[0].channel, opciones)
            if seleccion == -1:
                play_fake()
                break
            else:
                # Si el canal tiene play propio interpretar el itemlist que devuelve (Item o list)
                canal_play = __import__('channels.' + itemlist[seleccion].channel, fromlist=[''])
                if hasattr(canal_play, 'play'):
                    itemlist_play = canal_play.play(itemlist[seleccion])

                    if len(itemlist_play) > 0 and isinstance(itemlist_play[0], Item):
                        ok_play = play_video(itemlist_play[0], parent_item)

                    elif len(itemlist_play) > 0 and isinstance(itemlist_play[0], list):
                        itemlist[seleccion].video_urls = itemlist_play
                        ok_play = play_video(itemlist[seleccion], parent_item)

                    elif isinstance(itemlist_play, basestring):
                        ok_play = False
                        if notification_d_ok:
                            dialog_ok(config.__addon_name, itemlist_play)
                        else:
                            el_play = ('[B][COLOR %s]' + itemlist_play) % color_exec
                            dialog_notification(config.__addon_name, el_play + '[/COLOR][/B]')
                    else:
                        ok_play = False
                        if notification_d_ok:
                            dialog_ok(config.__addon_name, 'No se pudo reproducir')
                        else:
                            dialog_notification(config.__addon_name, '[B][COLOR %s]No se pudo reproducir[/COLOR][/B]' % color_exec)
                else:
                    ok_play = play_video(itemlist[seleccion], parent_item)

                if ok_play: break
                else: erroneos.append(seleccion)


# Reproducción fictícia para usar cuando Kodi espera que se haga un play
def play_fake(resuelto=False):
    logger.info()
    if resuelto:
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=os.path.join(config.get_runtime_path(), 'resources', 'subtitle.mp4')) )
        xbmc.Player().stop()
    else:
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, xbmcgui.ListItem(path=os.path.join(config.get_runtime_path(), 'resources', 'subtitle.mp4')) )
        # recomendable en advancedsettings.xml tener <playlistretries>-1</playlistretries> y <playlisttimeout>-1</playlisttimeout>
        # para evitar que se muestre diálogo "Playback failed" "Reproducción de lista abortada"


# Hacer la reproducción del item recibido. Devuelve False si falla el vídeo, True si ok o cancelado
# item: datos del enlace (server, url, y opcionalmente quality,language,age,other) 
# parent_item: datos de la película/episodio (infoLabels)
# autoplay: Si True no muestra dialog_ok() en caso de error ni diálogo para elegir si hay varias opciones
def play_video(item, parent_item, autoplay=False):
    notification_d_ok = config.get_setting('notification_d_ok', default=True)

    if item.video_urls:
        video_urls, puedes, motivo = item.video_urls, True, ""
    else:
        from core import servertools
        url_referer = item.url_referer if item.url_referer else parent_item.url
        video_urls, puedes, motivo = servertools.resolve_video_urls_for_playing(item.server, item.url, url_referer=url_referer)

    if not puedes:
        if not autoplay: dialog_ok("No puedes ver el vídeo porque...", motivo, item.url)
        return False

    if len(video_urls) == 1 and '.rar' in video_urls[0][0]:
        if not autoplay: dialog_ok("No puedes ver el vídeo porque...", 'Está comprimido en formato rar', item.url)
        return False

    opciones = []
    for video_url in video_urls:
        opciones.append("Ver el vídeo" + " " + video_url[0])

    # Si hay varias opciones dar a elegir, si sólo hay una reproducir directamente
    if len(opciones) > 1:
        if not autoplay: 
            seleccion = dialog_select("Elige una opción", opciones)
        else:
            seleccion = len(opciones) - 1 # la última es la de más calidad !?
    else:
        seleccion = 0

    if seleccion == -1:
        play_fake()
        return True
    else:
        mediaurl, view, mpd = get_video_seleccionado(item, seleccion, video_urls)
        if mediaurl == '':
            if not autoplay:
                if notification_d_ok:
                    dialog_ok(config.__addon_name, 'Vídeo no encontrado')
                else:
                    dialog_notification(config.__addon_name, '[B][COLOR %s]Vídeo no encontrado[/COLOR][/B]' % color_exec)
            return False

        if mpd and not is_mpd_enabled():
            if not autoplay: dialog_ok(config.__addon_name, 'Para ver el formato MPD se require el addon inputstream.adaptive')
            return False

        if item.server == 'torrent':
            return play_torrent(mediaurl, parent_item)

        # ~ Para evitar ERROR: CCurlFile::Stat - Failed: Peer certificate cannot be authenticated with given CA certificates(60)
        if item.server not in ['m3u8hls', 'zembed']:
            if 'verifypeer=false' not in mediaurl and 'googleusercontent' not in mediaurl: 
                mediaurl += '|' if '|' not in mediaurl else '&'
                mediaurl += 'verifypeer=false'

        xlistitem = xbmcgui.ListItem(path=mediaurl)
        set_infolabels(xlistitem, parent_item, True)

        if mpd:
            xlistitem.setProperty('inputstreamaddon', 'inputstream.adaptive')
            xlistitem.setProperty('inputstream.adaptive.manifest_type', 'mpd')

        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xlistitem)
        # ~ xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, xlistitem) # para probar forzando como si fallara

        if item.subtitle:
            logger.info('Subtítulos: %s' % item.subtitle)
            xbmc.sleep(2000)
            xbmc.Player().setSubtitles(item.subtitle)

        # espera de unos segundos y comprobar si está funcionando !?
        # ~ return xbmc.Player().isPlaying()
        return True


# video_urls: [0]:título [1]:url [2]:wait_time [3]:subtitle [4]:is_mpd
def get_video_seleccionado(item, seleccion, video_urls):
    logger.info()
    mediaurl = ""
    view = False
    wait_time = 0
    mpd = False

    # Ha elegido uno de los vídeos
    if seleccion < len(video_urls):
        mediaurl = video_urls[seleccion][1]
        if len(video_urls[seleccion]) > 4:
            wait_time = video_urls[seleccion][2]
            item.subtitle = video_urls[seleccion][3]
            mpd = True
        elif len(video_urls[seleccion]) > 3:
            wait_time = video_urls[seleccion][2]
            item.subtitle = video_urls[seleccion][3]
        elif len(video_urls[seleccion]) > 2:
            wait_time = video_urls[seleccion][2]
        view = True

    # Si no hay mediaurl es porque el vídeo no está :)
    logger.info("mediaurl=" + mediaurl)
    if mediaurl == '':
        logger.error('No video to play ;-(')
        wait_time = 0

    # Si hay un tiempo de espera (como en megaupload), lo impone ahora
    if wait_time > 0:
        continuar = handle_wait(wait_time, item.server, "Cargando vídeo...")
        if not continuar: mediaurl = ''

    return mediaurl, view, mpd


def handle_wait(time_to_wait, title, text):
    logger.info("handle_wait(time_to_wait=%d)" % time_to_wait)
    espera = dialog_progress(' ' + title, "")

    secs = 0
    increment = int(100 / time_to_wait)

    cancelled = False
    while secs < time_to_wait:
        secs += 1
        percent = increment * secs
        secs_left = str((time_to_wait - secs))
        remaining_display = "Espera " + secs_left + " segundos para que comience el vídeo..."
        espera.update(percent, ' ' + text, remaining_display)
        xbmc.sleep(1000)
        if espera.iscanceled():
            cancelled = True
            break

    if cancelled:
        logger.info('Espera cancelada')
        return False
    else:
        logger.info('Espera finalizada')
        return True


def play_torrent(mediaurl, parent_item):
    notification_d_ok = config.get_setting('notification_d_ok', default=True)

    from core import jsontools
    torrent_clients = jsontools.get_node_from_file('torrent.json', 'clients', os.path.join(config.get_runtime_path(), 'servers'))

    cliente_torrent = config.get_setting('cliente_torrent', default='Ninguno')
    if cliente_torrent == 'Seleccionar':
        from modules import filters

        ret = filters.show_clients_torrent(parent_item)

        if ret == -1:
            cliente_torrent = 'Ninguno'
        else:
           seleccionado = torrent_clients[ret]
           cliente_torrent = seleccionado['name']

           if dialog_yesno(config.__addon_name, 'Selecionado:  ' + cliente_torrent.capitalize(), '¿ Desea mantener este motor torrent, como motor habitual y no volver a seleccionarlo más ?'): 
               config.set_setting('cliente_torrent', cliente_torrent.capitalize())

    if cliente_torrent == 'Ninguno':
        dialog_ok(config.__addon_name, 'Necesitas tener instalado un cliente Torrent e indicarlo en la configuración')
        return False
    cliente_torrent = cliente_torrent.lower()

    plugin_url = ''
    for client in torrent_clients:
        if cliente_torrent == client['name']:
            if xbmc.getCondVisibility('System.HasAddon("%s")' % client['id']):
                # ~ plugin_url = client['url']
                plugin_url = client['url_magnet'] if 'url_magnet' in client and mediaurl.startswith('magnet:') else client['url']
            else:
                dialog_ok(config.__addon_name, 'Necesitas instalar el cliente Torrent: ' + client['name'], client['id'])
                return False

    if plugin_url == '':
        if notification_d_ok:
            dialog_ok(config.__addon_name, 'Cliente Torrent no contemplado')
        else:
            dialog_notification(config.__addon_name, '[B][COLOR %s]Cliente Torrent no contemplado[/COLOR][/B]' % color_exec)
        return False

    mediaurl = quote_plus(mediaurl)
    # Llamada con más parámetros para completar el título en algunos clientes
    if cliente_torrent in ['quasar', 'elementum'] and parent_item.infoLabels['tmdb_id']:
        if parent_item.contentType == 'episode' and cliente_torrent == 'quasar':
            mediaurl += "&episode=%s&library=&season=%s&show=%s&tmdb=%s&type=episode" % (parent_item.infoLabels['episode'], parent_item.infoLabels['season'], parent_item.infoLabels['tmdb_id'], parent_item.infoLabels['tmdb_id'])
        elif parent_item.contentType == 'movie':
            mediaurl += "&library=&tmdb=%s&type=movie" % (parent_item.infoLabels['tmdb_id'])

    xlistitem = xbmcgui.ListItem(path=plugin_url % mediaurl)
    # ~ set_infolabels(xlistitem, parent_item, True) # A activar si el plugin externo no lo hiciera
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xlistitem)

    return True


def is_playing():
    return xbmc.Player().isPlaying()

def is_mpd_enabled():
    return xbmc.getCondVisibility('System.HasAddon("inputstream.adaptive")')


# Diálogos internos
# Si falla un enlace de una peli/serie, en default.py se intercepta el error y se ofrece este diálogo
# para buscar la misma peli/serie en otros canales o en el propio canal.
def dialogo_busquedas_por_fallo_web(item):
    item_search = None

    if item.contentType == 'movie' and item.contentExtra == 'documentary':
        busqueda = 'el documental [COLOR gold]%s[/COLOR]' % item.contentTitle
    if item.contentType == 'movie':
        busqueda = 'la película [COLOR gold]%s[/COLOR]' % item.contentTitle
    else:
        busqueda = 'la serie [COLOR gold]%s[/COLOR]' % item.contentSerieName

    if dialog_yesno('Error en el canal ' + item.channel, 
                    'El enlace o la web de la que depende parece no estar disponible.',
                    '¿ Buscar %s en otros canales ?' % busqueda):

        infolabels = {'tmdb_id': item.infoLabels['tmdb_id']} if item.infoLabels['tmdb_id'] else {}
        item_search = Item(channel='search', action='search', from_channel=item.channel, infoLabels=infolabels)

    else:
        if dialog_yesno('Error en el canal ' + item.channel, 
                        'Si crees que la web funciona, quizás ha cambiado el enlace.',
                        '¿ Volver a buscar %s en el mismo canal ?' % busqueda):

            item_search = Item(channel=item.channel, action='search')

    if item_search is not None:
        if item.contentSerieName != '':
            item_search.search_type = 'tvshow'
            item_search.buscando = item.contentSerieName
        else:
            item_search.search_type = 'movie' if item.contentExtra != 'documentary' else 'documentary'
            item_search.buscando = item.contentTitle

    return item_search


# Acceso a DB de Kodi

file_kodi_db = '' # como variable global para no repetir get_kodi_db() si hay múltiples querys

def get_kodi_db():
    from core import filetools

    # Buscamos el archivo de la BBDD de vídeos más reciente (MyVideos[NUM].db)
    file_db = ''
    current_version = 0
    for f in filetools.listdir(translatePath("special://userdata/Database")):
        if f.lower().startswith('myvideos') and f.lower().endswith('.db'):
            version = int(re.sub('[^0-9]*', '', f))
            if version > current_version:
                file_db = filetools.join(translatePath("special://userdata/Database"), f)

    return file_db


def execute_sql_kodi(sql, parms_sql=None):
    """
    Ejecuta la consulta sql contra la base de datos de kodi
    @param sql: Consulta sql valida
    @type sql: str
    @return: Numero de registros modificados o devueltos por la consulta
    @rtype nun_records: int
    @return: lista con el resultado de la consulta
    @rtype records: list of tuples
    """

    logger.info()
    global file_kodi_db

    nun_records = 0
    records = None

    if file_kodi_db == '':
        file_kodi_db = get_kodi_db()
        logger.info("Archivo de BD: %s" % file_kodi_db)

    if file_kodi_db:
        conn = None
        try:
            import sqlite3
            conn = sqlite3.connect(file_kodi_db)
            cursor = conn.cursor()

            logger.info("Ejecutando sql: %s" % sql)
            if parms_sql is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, parms_sql)
            conn.commit()

            records = cursor.fetchall()
            if sql.lower().startswith("select"):
                nun_records = len(records)
                if nun_records == 1 and records[0][0] is None:
                    nun_records = 0
                    records = []
            else:
                nun_records = conn.total_changes

            conn.close()
            logger.info("Consulta ejecutada. Registros: %s" % nun_records)

        except:
            logger.error("Error al ejecutar la consulta sql")
            if conn:
                conn.close()

    else:
        logger.debug("Base de datos no encontrada")

    return nun_records, records

def get_kodi_version():
    kodi_version = re.match("\d+\.\d+", xbmc.getInfoLabel('System.BuildVersion')).group(0)
    return float(kodi_version), int(kodi_version.split('.')[0]), int(kodi_version.split('.')[1]) # ~ Completed Ex: 19.1, Version Build Ex 19, Extension Ex 1