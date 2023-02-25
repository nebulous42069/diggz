import sys
import xbmcgui
import xbmc
import xbmcplugin
import xbmcaddon
from resources.lib.grab import grab
from resources.lib.Movies import searchMovies, cinema_movies, movies
from resources.lib.TVShows import searchTVShows, listEpisodes, tvshowstab, featuredtvshowstab
from kodiez import KodiEZ
from routing import Plugin
try: from urllib.parse import urlparse
except ImportError: from urllib import urlparse

plugin = Plugin()
_ADDON = xbmcaddon.Addon()
_URL = f"plugin://{_ADDON.getAddonInfo('id')}"
_KODIEZ = KodiEZ(_ADDON, plugin.handle)
vidembedURL = "https://vidembed.io/"

if _ADDON.getAddonInfo('author') != '[COLOR cyan]Parrot[/COLOR] [COLOR yellow]Developers[/COLOR]' or _ADDON.getAddonInfo('id') != 'plugin.video.vidembed': exit()


def inpt():
    kb = xbmc.Keyboard('', "Enter keywords to search for:")
    kb.doModal()
    query = ""
    if kb.isConfirmed():
        query = kb.getText()
    return query

@plugin.route('/')
def home():
    xbmcplugin.setContent(plugin.handle, 'Home')
    xbmcplugin.setPluginCategory(plugin.handle, "Home")
    _KODIEZ.addItemToScreen("Movies", "", "https://i.ibb.co/PGCfS9S/Movies.png", f"{_URL}/MoviesHome/", True)
    _KODIEZ.addItemToScreen("Series", "", "https://i.ibb.co/NZHm9Gr/TV-Shows.png", f"{_URL}/SeriesHome/", True)
    xbmcplugin.endOfDirectory(plugin.handle)




####################################### Movies #############################################
@plugin.route('/MoviesHome/')
def MoviesHome():
    xbmcplugin.setContent(plugin.handle, 'Movies Home')
    xbmcplugin.setPluginCategory(plugin.handle, "Movies Home")
    _KODIEZ.addItemToScreen("Search", "", "https://i.ibb.co/MPhR0r7/Search.png", f"{_URL}/MoviesSearch/", True)
    _KODIEZ.addItemToScreen("Cinema Movies", "", "https://i.ibb.co/m8K59b4/Cinema-Movies.png", f"{_URL}/MoviesCinema/1/", True)
    _KODIEZ.addItemToScreen("Movies", "", "https://i.ibb.co/99RZMQN/Movies.png", f"{_URL}/Movies/1/", True)
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/MoviesSearch/')
def SearchMovies():
    query = inpt()
    if query == "" or query == None:
        MoviesHome()
        return
    xbmcplugin.setContent(plugin.handle, 'Movies')
    xbmcplugin.setPluginCategory(plugin.handle, "Result of: " + query)
    result = searchMovies(query)
    for i in range(len(result)):
        name = result[i].split('---')[0]
        url = result[i].split('---')[1]
        icon = result[i].split('---')[2]
        _KODIEZ.addItemToScreen(name, "", icon, f"{_URL}/play/{url.split('/')[-1]}", False)
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/MoviesCinema/<page>/')
def MoviesCinema(page):
    xbmcplugin.setContent(plugin.handle, 'Movies')
    xbmcplugin.setPluginCategory(plugin.handle, "Cinema Movies")
    page = int(page)
    result = cinema_movies(page)
    for i in range(len(result)):
        name = result[i].split('---')[0]
        url = result[i].split('---')[1]
        icon = result[i].split('---')[2]
        _KODIEZ.addItemToScreen(name, "", icon, f"{_URL}/play/{url.split('/')[-1]}", False)
    _KODIEZ.addItemToScreen("Next Page", "Next Page", "https://i.ibb.co/5YgXnHm/Next.png", f"{_URL}/MoviesCinema/{page + 1}/", True)
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/Movies/<page>/')
def Movies(page):
    xbmcplugin.setContent(plugin.handle, 'Movies')
    xbmcplugin.setPluginCategory(plugin.handle, "Movies")
    page = int(page)
    result = movies(page)
    for i in range(len(result)):
        name = result[i].split('---')[0]
        url = result[i].split('---')[1]
        icon = result[i].split('---')[2]
        _KODIEZ.addItemToScreen(name, "", icon, f"{_URL}/play/{url.split('/')[-1]}", False)
    _KODIEZ.addItemToScreen("Next Page", "Next Page", "https://i.ibb.co/5YgXnHm/Next.png", f"{_URL}/Movies/{page + 1}/", True)
    xbmcplugin.endOfDirectory(plugin.handle)

####################################### TV Shows #############################################

@plugin.route('/SeriesHome/')
def TVshows_home():
    xbmcplugin.setContent(plugin.handle, 'Series Home')
    xbmcplugin.setPluginCategory(plugin.handle, "Series Home")
    _KODIEZ.addItemToScreen("Search", "", "https://i.ibb.co/MPhR0r7/Search.png", f"{_URL}/SeriesSearch/", True)
    _KODIEZ.addItemToScreen("Series", "", "https://i.ibb.co/m8K59b4/Cinema-Movies.png", f"{_URL}/Series/0/", True)
    _KODIEZ.addItemToScreen("Featured Series", "", "https://i.ibb.co/99RZMQN/Movies.png", f"{_URL}/SeriesFeatured/0/", True)
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/SeriesSearch/')
def SearchTV():
    query = inpt()
    xbmcplugin.setContent(plugin.handle, 'TV Shows')
    xbmcplugin.setPluginCategory(plugin.handle, "Result of: " + query)
    if query == "" or query == None:
        TVshows_home()
        return
    result = searchTVShows(query)
    for i in range(len(result)):
        name = result[i].split('---')[0]
        url = result[i].split('---')[1]
        icon = result[i].split('---')[2]
        _KODIEZ.addItemToScreen(name, "", icon, f"{_URL}/Episodes/{url.split('/')[-1]}/", True)
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/Episodes/<url>/')
def listEps(url):
    xbmcplugin.setContent(plugin.handle, 'Series')
    xbmcplugin.setPluginCategory(plugin.handle, "Episodes")
    url = f"{vidembedURL}/videos/{url}"
    result = listEpisodes(url)
    for i in range(len(result)):
        name = result[i].split('---')[0]
        url = result[i].split('---')[1]
        icon = result[i].split('---')[2]
        _KODIEZ.addItemToScreen(name, "", icon, f"{_URL}/play/{url.split('/')[-1]}", False)
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/Series/<page>/')
def TVShows(page):
    xbmcplugin.setContent(plugin.handle, 'Series')
    xbmcplugin.setPluginCategory(plugin.handle, "Series")
    page = int(page)
    result = tvshowstab(page)
    for i in range(len(result)):
        name = result[i].split('---')[0]
        url = result[i].split('---')[1]
        icon = result[i].split('---')[2]
        _KODIEZ.addItemToScreen(name, "", icon, f"{_URL}/Episodes/{url.split('/')[-1]}/", True)
    _KODIEZ.addItemToScreen("Next Page", "Next Page", "https://i.ibb.co/5YgXnHm/Next.png",f"{_URL}/Series/{page + 1}/", True)
    xbmcplugin.endOfDirectory(plugin.handle) 

@plugin.route('/SeriesFeatured/<page>/')
def FeaturedTVShows(page):
    xbmcplugin.setContent(plugin.handle, 'Series')
    xbmcplugin.setPluginCategory(plugin.handle, "Series")
    page = int(page)
    result = featuredtvshowstab(page)
    for i in range(len(result)):
        name = result[i].split('---')[0]
        url = result[i].split('---')[1]
        icon = result[i].split('---')[2]
        _KODIEZ.addItemToScreen(name, "", icon, f"{_URL}/Episodes/{url.split('/')[-1]}/", True)
    _KODIEZ.addItemToScreen("Next Page", "Next Page", "https://i.ibb.co/5YgXnHm/Next.png", f"{_URL}/SeriesFeatured/{page + 1}/", True)
    xbmcplugin.endOfDirectory(plugin.handle) 

@plugin.route('/play/<path>/')
def play(path):
    path = f"{vidembedURL}/videos/{path}"
    try:
        play_item = xbmcgui.ListItem(path=grab(path))
        xbmcplugin.setResolvedUrl(plugin.handle, True, listitem=play_item)
    except Exception as e:
        xbmcgui.Dialog().ok("Error", "Could not play the video, Error: " + str(e))

if __name__ == '__main__':
    path = urlparse(sys.argv[0]).path
    if path == "/" or path.startswith("/play"):
        plugin.run(sys.argv)
    else: plugin.run(sys.argv)

