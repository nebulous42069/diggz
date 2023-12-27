# -*- coding: utf-8 -*-
              
#Credit to JewBMX for base code

import threading

from resources.lib.modules import control
from resources.lib.modules import log_utils


def syncTraktLibrary():
    try:
        control.execute('RunPlugin(plugin://%s)' % 'plugin.video.free99/?action=movies_to_library_silent&url=trakt_collection')
        control.execute('RunPlugin(plugin://%s)' % 'plugin.video.free99/?action=tvshows_to_library_silent&url=trakt_collection')
        log_utils.log('Trakt Library Sync Successful.')
    except Exception:
        log_utils.log('syncTraktLibrary', 1)
        pass


try:
    control.execute('RunPlugin(plugin://%s)' % 'plugin.video.free99/?action=service')
    log_utils.log('Service Process Successful.')
except Exception:
    log_utils.log('Service Process Failed.', 1)
    pass


try:
    if control.setting('trakt.sync') == 'true':
        syncTraktLibrary()
    if int(control.setting('trakt.synctime')) > 0:
        timeout = 3600 * int(control.setting('trakt.synctime'))
        log_utils.log('Trakt Library Sync Scheduled Time: ' + control.setting('trakt.synctime') + ' Hours. TimeOut: ' + timeout)
        schedTrakt = threading.Timer(timeout, syncTraktLibrary)
        schedTrakt.start()
except Exception:
    log_utils.log('Trakt Library Sync Failed.', 1)
    pass


