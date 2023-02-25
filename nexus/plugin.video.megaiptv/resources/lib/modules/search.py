from difflib import SequenceMatcher
import json
import xbmcgui
from .m3u_parser import m3uRegex
from .xml_parser import xmlRegex
from resources.lib.modules.addonvar import dialog,addon,search_json
from uservar import host
from .utils import Log


def NewSearchQuery():
	return dialog.input('Enter new search query')

def SelSources():
	items = []
	selsources = []
	xmlread = xmlRegex(host)
	m3usources = xmlread.xmlSourcesRead()
	for s in m3usources:
		li = xbmcgui.ListItem(s.get('name'))
		li.setPath(s.get('url'))
		li.setArt({'icon':s.get('icon')})
		items.append(li)
	ret = dialog.multiselect('Select which sources you would like to search',items)
	if ret:
		for i in ret:
			selsources.append(items[i])
	return selsources


def SearchSelected(query,sources):
	matches = []
	queryid = ''.join(query.lower())
	sqm = SequenceMatcher()
	sqm.set_seq1(queryid)
	for s in sources:
		data = json.loads(m3uRegex(s.getPath()).EpgRegex())
		for k,v in data.items():
			tvg_name = v.get('tvg_name')
			stream_url = v.get('stream_url')
			if addon.getSettingBool('general.search.sqmatch'):
				sqm.set_seq2(''.join(tvg_name.lower()))
				ratio = sqm.ratio()
				if ratio >= float(addon.getSettingInt('general.search.sqmatch.ratio')/100.00) and stream_url not in matches:
					v.update({'weight':ratio})
					matches.append(v) 
			if addon.getSettingBool('general.search.instring'):
				if query.lower() in tvg_name.lower() and stream_url not in matches:
					ratio = 1/len(tvg_name)*len(query)
					v.update({'weight':ratio})
					matches.append(v)
	matches = sorted(matches,key=lambda k:k['weight'],reverse=True)
	if len(matches) >0: 
		with open(search_json,'r+') as f:
			data = json.load(f)
			search_history = data.get('search_history')
			searchk = list(search_history.keys())
			for sk in searchk:
				if search_history.get(sk).get('query') == query:
					search_history.pop(sk)
			intsearchk = [int(x) for x in searchk]
			if len(searchk)==0:
				newkey = 1
			else:
				newkey = max(intsearchk)+1
			search_history.update({newkey:{'matches':matches,'query':query}})
			f.seek(0)
			json.dump(data,f,indent=4)
			f.truncate()
	return matches,query





