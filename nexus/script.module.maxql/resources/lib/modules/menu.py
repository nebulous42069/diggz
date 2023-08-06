import sys
import json
import xbmc
import xbmcplugin
from .utils import add_dir

addon_fanart = 'special://home/addons/script.module.maxql/icons/fanart.jpg'
min_icon = 'special://home/addons/script.module.maxql/icons/1080p.png'
max_icon = 'special://home/addons/script.module.maxql/icons/4k.png'

handle = int(sys.argv[1])

def main_menu():
    xbmcplugin.setPluginCategory(handle, 'Main Menu')
    
    add_dir('Covert all add-ons to 1080P Max','',1,min_icon,addon_fanart,isFolder=True)

    add_dir('Convert all add-ons to 4K Max','',2,max_icon,addon_fanart,isFolder=True)

