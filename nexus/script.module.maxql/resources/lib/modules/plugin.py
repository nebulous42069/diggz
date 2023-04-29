import xbmc
import xbmcplugin
import xbmcaddon
import sys
import os
from .params import Params
from .maxql_1080p import hd_maxset_1080p
from .maxql_4k import hd_maxset_4k

handle = int(sys.argv[1])

def router(paramstring):

    p = Params(paramstring)
    xbmc.log(str(p.get_params()),xbmc.LOGDEBUG)

    mode = p.get_mode()
    
    xbmcplugin.setContent(handle, 'files')

    if mode == 1:
        hd_maxset_1080p()

    elif mode == 2:
        hd_maxset_4k()

    xbmcplugin.endOfDirectory(handle)
