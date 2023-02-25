# -*- coding: utf-8 -*-
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info), PlatformCode y Core del Grupo Balandro (https://linktr.ee/balandro)

import os, sys, urllib, re, shutil, zipfile, base64
import xbmc, xbmcgui, xbmcaddon, xbmcplugin, requests
import locale, time, random, plugintools
import resolvers

if sys.version_info[0] < 3:
    import urllib2
else:
    import urllib.error as urllib2

from core import httptools
from core.item import Item
from platformcode.config import WebErrorException


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

version="(v0.0.2)"

addonPath           = xbmcaddon.Addon().getAddonInfo("path")
mi_data = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.adultseverywhere/'))
mi_addon = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.adultseverywhere'))

fondo = xbmc.translatePath(os.path.join(mi_addon,'fanart.jpg'))
logo1 = xbmc.translatePath(os.path.join(mi_addon,'icon.png'))

mislogos = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.adultseverywhere/jpg/'))
logobusca = xbmc.translatePath(os.path.join(mislogos , 'buscar.jpg'))
logo_volver = xbmc.translatePath(os.path.join(mislogos , 'volver.png'))
logo_siguiente = xbmc.translatePath(os.path.join(mislogos , 'siguiente.png'))
logo_finpag = xbmc.translatePath(os.path.join(mislogos , 'final.png'))
logo_transparente = xbmc.translatePath(os.path.join(mislogos , 'transparente.png'))
logo_salida = xbmc.translatePath(os.path.join(mislogos , 'salida.png'))
no_disponible = xbmc.translatePath(os.path.join(mislogos , 'no_disponible.jpg'))


datosConf = httptools.downloadpage(base64.b64decode("aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0FjZVRvcnIvZnV0dHJlYW0vbWFpbi9EYXRvc0NvbmY=".encode('utf-8')).decode('utf-8')).data

if not "<webXXX>" in datosConf:
    datosConf = httptools.downloadpage(base64.b64decode("aHR0cHM6Ly9yZW50cnkuY28veHM2YmYvcmF3".encode('utf-8')).decode('utf-8')).data

web = plugintools.find_single_match(datosConf,'webXXX>(.*?)<Fin')
listaStreamXXX = plugintools.find_single_match(datosConf,'listaStreamXXX>(.*?)<Fin')


if not os.path.exists(mi_data):
	os.makedirs(mi_data)  # Si no existe el directorio, lo creo

vistos = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.adultseverywhere/vistos.db'))
if not os.path.exists(vistos):
    if sys.version_info[0] < 3:
        crear=open(vistos, "w+")
    else:
        crear=open(vistos, "w+", encoding='utf-8')
    crear.close()

cabecera = "[COLOR coral][B]         Adults Everywhere  "+version+" [COLOR red]        ····[COLOR yellowgreen]by AceTorr[COLOR red]····[/B][/COLOR]"
	



# Punto de Entrada
def run():
	plugintools.log('[%s %s] Running %s... ' % (addonName, addonVersion, addonName))

	# Obteniendo parámetros...
	params = plugintools.get_params()
    
	
	if params.get("action") is None:
		main_list(params)
	else:
		action = params.get("action")
		exec(action+"(params)")
        

	plugintools.close_item_list()            



# Principal
def main_list(params):


    data = ""
    webMenu = web + "/lang/espanol"
    data = httptools.downloadpage(webMenu).data
    
    #Saco las diferentes categorias
    acotacion = 'id="main-cat-sub-list'
    grupos1 = plugintools.find_single_match(data,acotacion+'(.*?)</ul')
    acotacion = '<li class="dyn'
    grupos = plugintools.find_multiple_matches(grupos1,acotacion+'(.*?)</li')
    #plugintools.log("*****************Grupos: "+str(len(grupos))+"********************")
    
    plugintools.add_item(action="",url="",title=cabecera,thumbnail=logo1,fanart=fondo,folder=False,isPlayable=False)
    plugintools.add_item(action="",url="",title="",thumbnail=logo_transparente, fanart=fondo, folder=False, isPlayable=False)
    
    plugintools.add_item(action="listaIPTV",url="", title='[COLOR white]Canales en Streaming[/COLOR]' ,thumbnail=logo1, fanart=fondo, folder=True, isPlayable=False)
    
    for item in grupos:
        url = plugintools.find_single_match(item,'a href="(.*?)"').strip()
        if len(url) > 0:
            url = web + url
            titu = plugintools.find_single_match(item,'btn-default">(.*?)</a').strip()  ##.title()
            titu = acentos(titu)
            logo = logo1

            plugintools.add_item(action="abre_categoria",url=url,title='[COLOR white]' + titu + '[/COLOR]' ,thumbnail=logo, fanart=fondo, folder=True, isPlayable=False)
	
    datamovie = {}
    datamovie["Plot"]="Buscar Documentales por palabras clave."
    plugintools.add_item(action="abre_categoria",url="",title="[COLOR blue]Búsqueda[/COLOR]",extra="busca", thumbnail=logobusca, fanart=fondo, info_labels = datamovie, folder=True, isPlayable=False)
    datamovie = {}
    datamovie["Plot"]="Salir de DocumentalesON..."
    plugintools.add_item(action="salida",url="",title="[COLOR red]Salir[/COLOR]",thumbnail=logo_salida, extra="", fanart="https://i.imgur.com/Cp1t1lb.png", info_labels = datamovie, folder=False, isPlayable=False)





def abre_categoria(params):
    url = params.get("url")
    titu = params.get("title")
    logo1 = params.get("thumbnail")
    extra = params.get("extra")

    xbmcplugin.setContent( int(sys.argv[1]) ,"tvshows" )
    
    data = ""
    data = httptools.downloadpage(url).data
    
    acotacion = 'id="video_'
    videos = plugintools.find_multiple_matches(data,acotacion+'(.*?)</script')

    #plugintools.add_item(action="",url="",title=titu,thumbnail=logo1,fanart=fondo,folder=False,isPlayable=False)
    #plugintools.add_item(action="",url="",title="",thumbnail=logo_transparente, fanart=fondo, folder=False, isPlayable=False)

    #Pongo todos los videos de la página
    for item in videos:
    
        acotacion = 'title="'
        titulo = acentos( plugintools.find_single_match(item,acotacion+'(.*?)"') )
        descrip = titulo
        acotacion = 'data-src="'
        logo = plugintools.find_single_match(item,acotacion+'(.*?)"')
        acotacion = '<a href="'
        mivideo = plugintools.find_single_match(item,acotacion+'(.*?)"')
        if len(mivideo) > 0:
            mivideo = web + mivideo
            #plugintools.log("*****************MiVideo2: "+mivideo+"********************")
            duracion = plugintools.find_single_match(item,'duration">(.*?)<')
            calidad = ""
            calidad = plugintools.find_single_match(item,'hd-mark">(.*?)<')
            if len(calidad) == 0:
                calidad = plugintools.find_single_match(item,'sd-mark">(.*?)<')
            
            if len(calidad) == 0:
                calidad = "SD"
                
            titu = '[COLOR red]·'+calidad+'· '+duracion+' [COLOR white]->' + titulo + '[/COLOR]'
            datamovie = {}
            datamovie["Plot"] = descrip
            plugintools.add_item(action="lanza", url=mivideo, title=titu, extra=titulo, genre="NOGESTIONAR", thumbnail=logo, fanart=fondo, info_labels = datamovie, folder=False, isPlayable=False)
    
    acotacion = 'active" href="">'
    pagactiva = plugintools.find_single_match(data,acotacion+'(.*?)<')
    if 'mobile-hide">Siguiente' in data: ## Hay mas páginas, así que busco la siguiente y la última
        bloque = plugintools.find_single_match(data,'last-page"(.*?)Siguiente<')
        pagfin = plugintools.find_single_match(bloque,'>(.*?)<')
        
        url_siguiente = web + plugintools.find_single_match(bloque,'href="(.*?)"')
        el_logo = logo_siguiente
    else:
        pagfin = pagactiva
        url_siguiente = ""
        el_logo = logo_finpag

    texto = "[COLOR mediumaquamarine]Pág: " + pagactiva + " / " + pagfin + "[COLOR lime]          Ir a Siguiente >>>[/COLOR]"

    plugintools.add_item(action="abre_categoria", url=url_siguiente, title=texto, extra=extra ,thumbnail=el_logo, fanart=fondo, folder=True, isPlayable=False)
            
    plugintools.add_item(action="main_list", url="", title="[COLOR orangered]···· Volver a Menú Principal ····[/COLOR]", extra=extra ,thumbnail=logo_volver, fanart=fondo, folder=True, isPlayable=False)
        
            


def listaIPTV(params):

    #listaDoble = httptools.downloadpage(m2Internacional).data
    listaDoble = httptools.downloadpage(listaStreamXXX).data
    listaDoble = listaDoble + "#"
    
    acotacion = "EXTINF:-1"
    acotaFin = "#"
    canales = plugintools.find_multiple_matches(listaDoble,acotacion+'(.*?)'+acotaFin)
    for item in canales:
        item = item + "#"
        titulo = plugintools.find_single_match(item,'tvg-name="(.*?)"').replace("AdultIPTV.net " , "")
        acotacion = 'group-title="'
        acotaFin = "#"
        provi = plugintools.find_single_match(item,acotacion+'(.*?)'+acotaFin) + "#"
        acotacion = "http://"
        link = "http://" + plugintools.find_single_match(item,acotacion+'(.*?)'+acotaFin).replace("\r\n" , "").replace("\n" , "") 
        #plugintools.log("*****************Link: "+link+"********************")
        titu = "[COLOR white]" + titulo + "[/COLOR]"

        if len(titulo) > 0:
            plugintools.add_item(action="lanza", url=link, title=titu, extra="m3u8", thumbnail=logo1, fanart=fondo, folder=False, isPlayable=False)
        
        


    
    

def acentos(texto):

    texto2 = texto.replace("&Aacute;" , "Á").replace("&Eacute;" , "É").replace("&Iacute;" , "Í").replace("&Oacute;" , "Ó").replace("&Uacute;" , "Ú")
    texto2 = texto2.replace("&aacute;" , "á").replace("&eacute;" , "é").replace("&iacute;" , "í").replace("&oacute;" , "ó").replace("&uacute;" , "ú")



    return texto2

    


def lanza(params):
    url = params.get("url")
    logo = params.get("thumbnail")
    titu = params.get("title")
    titulo = params.get("extra")
    extra = params.get("extra")
    
    if extra == "m3u8":
        mivideo = url
    else:
        data = httptools.downloadpage(url).data
        data = data.replace("setVideoHLS('" , "VIDEO01").replace("setVideoUrlHigh('" , "VIDEO02").replace("setVideoUrlLow('" , "VIDEO03")
        #plugintools.log("*****************Url: "+url+"********************")
        
        mivideo = ""
        acotacion = "VIDEO01"  ##Busco 1º el de mayor calidad
        mivideo = plugintools.find_single_match(data,acotacion+"(.*?)'")
        if len(mivideo) == 0:
            acotacion = "VIDEO02"  ##Busco el 2º de mayor calidad
            mivideo = plugintools.find_single_match(data,acotacion+"(.*?)'")
            if len(mivideo) == 0:
                acotacion = "VIDEO03"  ##Busco el 3º de mayor calidad
                mivideo = plugintools.find_single_match(data,acotacion+"(.*?)'")
            else:
                mivideo = ""
    
    #mivideo = ""
    #xbmc.Player().play(mivideo)
    li = xbmcgui.ListItem(titu)
    li.setInfo(type='Video', infoLabels="")
    li.setArt({ 'thumb': logo})
    xbmc.Player().play(mivideo, li)







def salida(params):

	xbmc.executebuiltin('ActivateWindow(10000,return)')
	



	


	


		
run()

		




	

