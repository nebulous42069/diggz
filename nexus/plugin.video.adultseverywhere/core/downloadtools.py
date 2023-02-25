# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# downloadtools - Herramientas para descargar ficheros
# ------------------------------------------------------------

from platformcode import config, logger

from core.downloader import Downloader
from core import filetools
import sys
PY3 = False
if sys.version_info[0] >= 3:
    unicode = str

STATUS_CODES = type("StatusCode", (), {"stopped": 0, "canceled": 1, "completed": 2, "error": 3})


# Descarga un fichero usando el módulo Downloader y devuelve los parámetros del estado de la descarga
# -------------------
def do_download(mediaurl, download_path, file_name, headers=[], silent=False, resume=True):

    # Crear carpeta de destino si no existe
    if not filetools.exists(download_path):
        filetools.mkdir(download_path)

    # Limpiar caracteres para nombre de fichero válido
    try:
        file_name = config.text_clean(file_name)
    except: pass

    # Evitar unicode que puede dar problemas luego...
    if type(mediaurl) == unicode: mediaurl = mediaurl.encode('ascii','ignore')

    # Lanzamos la descarga
    d = Downloader(mediaurl, download_path, file_name,
                   headers = headers, 
                   resume = resume,
                   max_connections = 1 + int(config.get_setting("max_connections")),
                   block_size = 2 ** (17 + int(config.get_setting("block_size"))),
                   part_size = 2 ** (20 + int(config.get_setting("part_size"))),
                   max_buffer = 2 * int(config.get_setting("max_buffer")))

    if silent:
        d.start()
        # bucle hasta terminar
        import xbmc
        while not xbmc.Monitor().abortRequested() and d.state not in [d.states.error, d.states.stopped, d.states.completed]:
            xbmc.sleep(100)
    else:
        d.start_dialog()

    # Descarga detenida, verificar estado: {"stopped": 0, "connecting": 1, "downloading": 2, "completed": 3, "error": 4, "saving": 5})
    if d.state == d.states.error:
        logger.info('Error en la descarga %s' % mediaurl)
        status = STATUS_CODES.error

    elif d.state == d.states.stopped:
        logger.info("Descarga detenida")
        status = STATUS_CODES.canceled

    elif d.state == d.states.completed:
        logger.info("Descargada finalizada")
        status = STATUS_CODES.completed
    
    else:
        logger.error("Estado de descarga no previsto! %d" % d.state)
        status = STATUS_CODES.stopped

    params = { 
               'downloadStatus': status,              # 3:error / 1:canceled / 2:completed
               'downloadSize': d.size[0],             # total bytes de la descarga
               'downloadCompleted': d.downloaded[0],  # bytes descargados
               'downloadProgress': d.progress,        # porcentaje descargado (float)
               'downloadUrl': d.download_url,         # url origen
               'downloadFilename': d.filename         # nombre del fichero (sin path)
             }

    return params
