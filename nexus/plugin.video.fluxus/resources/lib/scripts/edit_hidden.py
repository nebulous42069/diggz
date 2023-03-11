import json
import os 
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

def main():
	dialog = xbmcgui.Dialog()
	__addon__ = xbmcaddon.Addon(sys.argv[1])
	__addonProfile__ = xbmcvfs.translatePath(__addon__.getAddonInfo('profile'))
	customiser_json = os.path.join(__addonProfile__,'customiser.json')
	toEdit = sys.argv[2]
	with open(customiser_json,'r+') as f:
		data = json.load(f)
		if toEdit == 'category':
			kw = 'hidden_category'
			msg = 'UnSelect Cateogry\'s to show in Category List again'
		elif toEdit == 'channel':
			kw = 'hidden_channel'
			msg = 'UnSelect Channel\'s to show in Channel List again'
		cdata = data.get(kw)
		ckeys = list(cdata.keys())
		items = []
		for c in ckeys:
			li = xbmcgui.ListItem(cdata.get(c),c)
			items.append(li)
		pre = list(range(0,len(items)))
		ret = dialog.multiselect(msg,items,preselect=pre)
		if ret:
			to_del = list(set(pre)^set(ret))
			for i in to_del:
				cdata.pop(ckeys[i])
			f.seek(0)
			json.dump(data,f,indent=4)
			f.truncate()
		

		



if __name__ == '__main__':
	main()