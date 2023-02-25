import xbmcgui, xbmcplugin
import sys
from urllib.parse import quote_plus

def addDir(name,url,mode,icon,fanart,description,page = '', addcontext=False,name2='',isFolder=True):
	u=sys.argv[0]+"?name="+quote_plus(name)+"&url="+quote_plus(url)+"&mode="+str(mode)+"&icon="+quote_plus(icon) +"&fanart="+quote_plus(fanart)+"&description="+quote_plus(description)+"&name2="+quote_plus(name2)+"&page="+str(page)
	liz=xbmcgui.ListItem(name)
	liz.setArt({'fanart':fanart,'icon':'DefaultFolder.png','thumb':icon})
	liz.setInfo(type="Video", infoLabels={ "Title": name, "plot": description})
	if addcontext:
		contextMenu = []
		liz.addContextMenuItems(contextMenu)
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)