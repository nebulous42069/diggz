# -*- coding: utf-8 -*-

import os, glob

from core import jsontools, filetools
from platformcode import config, logger


def get_channels_list(filtros={}):
    itemlist = []
    
    # Si no se indica lo contrario, sólo se muestran los activos
    if 'active' not in filtros: filtros['active'] = True

    channels_path = os.path.join(config.get_runtime_path(), 'channels', '*.json')
    for channel_path in glob.glob(channels_path):
        channel = os.path.basename(channel_path).replace('.json', '')
        channel_parameters = get_channel_parameters(channel)
        if channel_parameters['id'] != channel:
            logger.error('El id: %s no coincide con el fichero del canal: %s' % (channel_parameters['id'], channel))
            continue

        seleccionar = True
        for parametro, valor in filtros.items():
            if parametro in channel_parameters:
                # Para listas no seleccionar si el valor no está en la lista
                if parametro in ['categories', 'language', 'search_types', 'clusters']:
                    if valor not in channel_parameters[parametro]: seleccionar = False; break
                # Para status, no seleccionar si no tiene el valor mínimo
                elif parametro == 'status':
                    if channel_parameters[parametro] < valor: seleccionar = False; break
                # Para los demás parámetros no seleccionar si el valor no coincide
                else:
                    if valor != channel_parameters[parametro]: seleccionar = False; break

        if not seleccionar: 
            continue

        itemlist.append(channel_parameters)

    channels_list_order = config.get_setting('channels_list_order', default=False) # False:orden alfabético True:preferidos al principio
    if channels_list_order:
        itemlist.sort(key=lambda item: (1-item['status'], item['id']))
    else:
        itemlist.sort(key=lambda item: item['id']) #.lower().strip()

    return itemlist


def get_channel_parameters(channel_name):
    datos = get_channel_json(channel_name)

    # valores por defecto si no existen:
    datos['active'] = datos.get('active', False)
    datos['status'] = datos.get('status', 0) # -1:desactivado, 0:activo, 1:preferido
    datos['searchable'] = datos.get('searchable', False)
    datos['search_types'] = datos.get('search_types', list())
    datos['categories'] = datos.get('categories', list())
    datos['language'] = datos.get('language', list())
    datos['notes'] = datos.get('notes', '')
    datos['adult'] = datos.get('adult', False)
    datos['clusters'] = datos.get('clusters', '')
    datos['thumbnail'] = datos.get('thumbnail', '')

    # ajustar paths:
    if datos['thumbnail'] != '' and '://' not in datos['thumbnail']:
        datos['thumbnail'] = os.path.join(config.get_runtime_path(), 'resources', 'media', 'channels', 'thumb', datos['thumbnail'])

    # Parámetros configurables por el usuario
    user_status = config.get_setting('status', channel_name, default=-9)
    if user_status != -9: datos['status'] = user_status

    return datos


def get_channel_json(channel_name):
    channel_json = {}
    try:
        channel_path = filetools.join(config.get_runtime_path(), "channels", channel_name + ".json")
        if filetools.isfile(channel_path):
            channel_json = jsontools.load(filetools.read(channel_path))

    except Exception as ex:
        template = "An exception of type %s occured. Arguments:\n%r"
        message = template % (type(ex).__name__, ex.args)
        logger.error(" %s" % message)

    return channel_json

