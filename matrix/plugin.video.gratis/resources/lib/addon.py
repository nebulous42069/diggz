import xbmcvfs
import xbmcplugin
import sys
from urllib.parse import parse_qsl
from .plugin import m

MAIN = {
    'Latest Movies': {
        'url': '',
        'mode': 'vc_latest_movies',
        'icon': m.addon_icon,
        'fanart': m.addon_fanart,
        'description': 'Watch the Latest Movies',
        'isFolder': True
    },
    'Trending Movies': {
        'url': '',
        'mode': 'vc_trending_movies',
        'icon': m.addon_icon,
        'fanart': m.addon_fanart,
        'description': 'Trending Movies',
        'isFolder': True
    },
    'Latest Episodes': {
        'url': '',
        'mode': 'vc_latest_episodes',
        'icon': m.addon_icon,
        'fanart': m.addon_fanart,
        'description': 'Watch the Latest Episodes',
        'isFolder': True
    },
    'Latest Seasons': {
        'url': '',
        'mode': 'vc_latest_seasons',
        'icon': m.addon_icon,
        'fanart': m.addon_fanart,
        'description': 'The Latest Seasons',
        'isFolder': True
    },
    'Search': {
        'url': '',
        'mode': 'vc_search_history',
        'icon': m.addon_icon,
        'fanart': m.addon_fanart,
        'description': 'Search Movies and Shows',
        'isFolder': True
    },
    'BS Latest': {
        'url': '',
        'mode': 'bst_new_shows',
        'icon': m.addon_icon,
        'fanart': m.addon_fanart,
        'description': 'Latest Shows',
        'isFolder': True
    },
    'BS Popular Series': {
        'url': '',
        'mode': 'bst_series',
        'icon': m.addon_icon,
        'fanart': m.addon_fanart,
        'description': 'Popular Series',
        'isFolder': True
    },
    'Vids': {
        'url': '',
        'mode': 'vid_main',
        'icon': m.addon_icon,
        'fanart': m.addon_fanart,
        'description': 'Vids',
        'isFolder': True
    },
    'Live Sports': {
        'url': '',
        'mode': 'live_main',
        'icon': m.addon_icon,
        'fanart': m.addon_fanart,
        'description': 'Live Sports',
        'isFolder': True
    },
    'Live Channels': {
        'url': '',
        'mode': 'live_channels',
        'icon': m.addon_icon,
        'fanart': m.addon_fanart,
        'description': 'Live Channels',
        'isFolder': True
    },
    'Sports Replays': {
        'url': '',
        'mode': 'replays_main',
        'icon': m.addon_icon,
        'fanart': m.addon_fanart,
        'description': 'Sports Replays',
        'isFolder': True
    }
}

def main_menu():
    xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Main Menu')
    for cat in MAIN.keys():
        m.add_dir(cat, MAIN[cat]['url'], MAIN[cat]['mode'], MAIN[cat]['icon'], MAIN[cat]['fanart'], MAIN[cat]['description'], isFolder=MAIN[cat]['isFolder'])

def router(paramstring):
    p = dict(parse_qsl(paramstring))
    name = p.get('name', '')
    name2 = p.get('name2', '')
    url = p.get('url', '')
    mode = p.get('mode')
    icon = p.get('icon', m.addon_icon)
    description = p.get('description', '')
    page = p.get('page', '')
    if page: page = int(page)
    
    #import json
    #m.textview(json.dumps(p, indent=4))
    
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    
    if mode is None:
        if not xbmcvfs.exists(m.addon_data):
            xbmcvfs.mkdirs(m.addon_data)
        main_menu()
    
    elif mode == 'play_video':
        from .player2 import Player
        p = Player()
        p.play_video(name, url, icon, description,name2)
        
    elif str(mode).startswith('vc'):
        from . import vc
        vc.runner(p)
    
    elif str(mode).startswith('bst'):
        from . import bst
        bst.runner(p)
    
    elif str(mode).startswith('vid'):
        from . import myvideo
        myvideo.runner(p)
        
    elif str(mode).startswith('replays'):
        from . import replays2
        replays2.runner(p)
    
    elif str(mode).startswith('soccer'):
        from . import sc2
        sc2.runner(p)
    
    elif str(mode).startswith('live'):
        from . import dd
        dd.runner(p)
    
    xbmcplugin.endOfDirectory(int(sys.argv[1]))