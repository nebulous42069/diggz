from datetime import datetime
import json
import pathlib
import xbmc
import xbmcgui
import xbmcplugin
import sys
from urllib.parse import quote_plus,urlencode,parse_qs,unquote_plus
from resources.lib.modules.addonvar import addon_name,addon_version,local_string,addon


def addDir(name,url,mode,icon,fanart,description,addcontext=False,isFolder=True,m3udata=None,label2=None,channeldata=None):
	u=sys.argv[0]+"?name="+quote_plus(name)+"&url="+quote_plus(url)+"&mode="+str(mode)+"&icon="+quote_plus(icon) +"&fanart="+quote_plus(fanart)+"&description="+quote_plus(description)+"&channeldata="+DictParams(channeldata)
	liz=xbmcgui.ListItem(name)
	if isFolder:
		liz.setArt({'fanart':fanart,'icon':'DefaultFolder.png','thumb':icon})
	else:
		liz.setArt({'fanart':fanart,'icon':'DefaultStudios.png','thumb':icon})
	if label2:
		liz.setLabel2(label2)
	liz.setInfo(type="Video", infoLabels={ "Title": name, "plot": description})
	liz.setProperties({'m3udata':m3udata,'channeldata':json.dumps(channeldata)})
	if addcontext:
		contextMenu = []
		for context in addcontext:
			if context == 'hide_cat':
				contextMenu.append((local_string(32014),f'RunPlugin({sys.argv[0]}?mode=100&name={quote_plus(name)})'))
			if context == 'hide_chan':
				contextMenu.append((local_string(32015),f'RunPlugin({sys.argv[0]}?mode=101&channeldata={DictParams(channeldata)})'))
			if context == 'add_fav_chan':
				contextMenu.append((local_string(32016), f"RunPlugin({sys.argv[0]}?mode=102&channeldata={DictParams(channeldata)})"))
			if context == 're_fav_chan':
				contextMenu.append((local_string(32017),f'Runplugin({sys.argv[0]}?mode=103&channeldata={DictParams(channeldata)})'))
			# if context == 'userguide':
			# 	mdpath = 'special://home/addons'
			# 	contextMenu.append(('userInfo',f'RunScript(script.context.userguide,{mdpath})'))
		liz.addContextMenuItems(contextMenu)
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)


def Log(msg):
	if addon.getSettingBool('general.debug'):
		from inspect import getframeinfo, stack
		fileinfo = getframeinfo(stack()[1][0])
		xbmc.log('*__{}__{}*{} Python file name = {} Line Number = {}'.format(addon_name,addon_version,msg,fileinfo.filename,fileinfo.lineno), level=xbmc.LOGINFO)


		
def NewJsonFile(filepath,headers):
	dirpath = pathlib.Path(filepath).resolve().parent
	if not dirpath.exists():
		dirpath.mkdir(parents=True, exist_ok=True)
	with open(filepath,'w') as f:
		json.dump(headers,f,indent=4)



def DictParams(item):
	return quote_plus(json.dumps(item))

def ParamsDict(item):
	return unquote_plus(item)



def TimeStamp_dtobj(timestamp):
	if isinstance(timestamp,(str,float)):
		timestamp = int(timestamp)
	return datetime.fromtimestamp(timestamp)

def dtobj_StrF(datetime,fmt):
	return datetime.strftime(fmt)

def RegionSetting_dtfmt():
	return f"{xbmc.getRegion('dateshort')} {xbmc.getRegion('time')}"

def Timestamp_Region_dt(timestamp):
	return dtobj_StrF(TimeStamp_dtobj(timestamp),RegionSetting_dtfmt())

	