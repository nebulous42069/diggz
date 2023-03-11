import xbmc
import xbmcplugin
import xbmcgui
import sys
from .plugin import Myaddon
from urllib.parse import unquote_plus


class Player(Myaddon):
    
    def play_video(self, name, url, icon, description, resolve=True):
           if url is None:
               return
           link = url
           if type(link) == str and link.startswith('TRAILERS/'):
               from .tmdb import tmdb
               link = tmdb.get_tmdb_videos(link.replace('TRAILERS/', ''))
           if type(link) == list:
               if len(link) > 1:
                   link = self.get_multilink(link)
               elif len(link) == 1:
                   if len(link[0]) == 2:
                       link = link[0][1]
                   elif len(link[0]) == 1:
                       link = link[0]
               else:
                   return
           if not link:
               return
           if link.endswith(')'):
               link = link.split('(')[0]
           
           
           if resolve is True:
               import resolveurl
               if resolveurl.HostedMediaFile(link).valid_url():
                   link = resolveurl.HostedMediaFile(link).resolve()
           liz = xbmcgui.ListItem(name, path=unquote_plus(link))
           liz.setInfo('video', {'title': name, 'plot':description})
           liz.setArt({'thumb': icon, 'icon': icon, 'poster': icon})
           liz.setProperty('IsPlayable', 'true')
           xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, liz)
           #xbmc.Player().play(link, liz)

player = Player()