# -*- coding: utf-8 -*-

import sys

if sys.version_info[0] < 3:
    pass
else:
    unicode = str

import xbmcgui, xbmc

from platformcode import config, logger, platformtools
from core import httptools, scrapertools


# Muestra diálogo para que el usuario resuelva el recaptcha de imagen y devuelve la resolución en google
def get_recaptcha_response(sitekey, referer):

    def goo_get_version():
        try:
            data = httptools.downloadpage('http://www.google.com/recaptcha/api.js?hl=es').data
            # ~ logger.debug(data)
            version = scrapertools.find_single_match(data, ".*?po.src='(.*?)'")
            if version == '': version = scrapertools.find_single_match(data, '.*?po.src="(.*?)"')
            return version.split('/')[5]
        except:
            return ''

    def goo_get_challenge():
        data = httptools.downloadpage(url, headers=headers).data
        # ~ logger.debug(data)

        mensaje = scrapertools.find_single_match(data, 'canonical.*?">(.*?)<div class="fbc')
        mensaje = mensaje.replace("<strong>", "").replace("<div>", "").replace("<label>", "").replace("</strong>", "").replace("</div>", "").replace("</label>", "")
        mensaje = unicode(scrapertools.htmlclean(mensaje), "utf-8")

        token = scrapertools.find_single_match(data, 'name="c" value="([^"]+)"')

        imagen = "http://www.google.com/recaptcha/api2/payload?k=%s&c=%s" % (sitekey, token)

        return mensaje, imagen, token

    # Verificar sitekey informado
    if sitekey == '':
       logger.info('Se necesita sitekey para recaptcha!')
       return ''

    # Obtener version de google
    version = goo_get_version()
    if version == '':
       logger.info('No se ha detectado versión para recaptcha!')
       return ''

    # Calcular url con sitekey y version
    url = 'https://www.google.com/recaptcha/api/fallback?k=%s&hl=es&v=%s&t=2&ff=true' % (sitekey, version)
    headers = {'Referer': referer}
    resultado = ''

    # Bucle hasta resolver o cancelar
    resultado = ''
    monitor = xbmc.Monitor()
    while not monitor.abortRequested():
        # Obtener datos de google (mensaje, imagen, token)
        mensaje, imagen, token = goo_get_challenge()
        if mensaje == '' or imagen == '' or token == '':
            logger.info('Faltan datos para Recaptcha. %s %s %s' % (mensaje, imagen, token))
            break

        # Mostrar diálogo para resolver
        mainWindow = Recaptcha("Recaptcha.xml", config.get_runtime_path(), mensaje=mensaje, imagen=imagen)
        mainWindow.doModal()
        result = mainWindow.result
        del mainWindow

        # Comprobar respuesta
        if result == '': # Cancelado por el usuario
            break
        elif len(result) > 0: # llamada a google para verificar respuesta
            post = "c=%s" % token
            for r in result: post += "&response=%s" % r
            
            data = httptools.downloadpage(url, post, headers=headers).data
            # ~ logger.debug(data)
            resultado = scrapertools.find_single_match(data, '<div class="fbc-verification-token">.*?>([^<]+)<')
            if resultado != '':
                logger.info('Recaptcha resuelto: %s' % resultado)
                break
            else:
                logger.info('Recaptcha no resuelto')
        # ~ else: # Recargar

    return resultado


class Recaptcha(xbmcgui.WindowXMLDialog):

    def __init__(self, *args, **kwargs):
        self.mensaje = kwargs.get("mensaje")
        self.imagen = kwargs.get("imagen")
        self.checks = {}
        self.result = ''

    def onInit(self):
        self.getControl(10020).setImage(self.imagen)
        self.getControl(10000).addLabel('[B]'+self.mensaje+'[/B]')
        self.setFocusId(10005)

    def onClick(self, control):

        if control == 10003: # Cancelar
            self.result = ''
            self.close()

        elif control == 10004: # Recargar
            self.checks = {}
            self.result = []
            self.close()

        elif control == 10002: # Aceptar
            self.result = [int(k) for k in range(9) if self.checks.get(k, False) == True]
            self.close()

        else: # Marcar/Desmarcar cuadrado sobre la imagen
            self.checks[control - 10005] = not self.checks.get(control - 10005, False)
