import xbmcgui
import xbmc
import xbmcaddon
import xbmcplugin
import urllib
import sys
import re
import time
import requests
import base64
import json
from urllib.parse import parse_qsl,urlparse,urlencode
import os
from bs4 import BeautifulSoup as BS

AddonInfo           =  xbmcaddon.Addon().getAddonInfo
EndOfDirectory      = lambda: xbmcplugin.endOfDirectory(int(sys.argv[1]))
UserAgent           = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
Log                 =  lambda x: xbmc.log(str(x),2)
Exe                 = xbmc.executebuiltin
Compile             = lambda x,y: re.compile(x).findall(y)
Decode              = lambda x: base64.b64decode(str(x))
AddonInfo           =  xbmcaddon.Addon().getAddonInfo
Join                = lambda x,y=None: os.path.join(x,y) if y else join(TranslatePath(AddonInfo('profile')),x)
Post                = lambda x,y,z: requests.post(x, data = y, headers = z).text

def parseInt(sin):
  import re
  m = re.search(r'^(\d+)[.,]?\d*?', str(sin))
  return int(m.groups()[-1]) if m and not callable(sin) else None

def javascript(code):
	url = "https://onecompiler.com/api/code/exec"

	payload = json.dumps({
	  "name": "JavaScript",
	  "title": "3xdume9m5",
	  "mode": "javascript",
	  "extension": "js",
	  "languageType": "programming",
	  "properties": {
		"language": "javascript",
		"files": [
		  {
			"name": "HelloWorld.js",
			"content": "%s"%(code)
		  }
		]
	  }
	})
	headers = {
	  'content-type': 'application/json'
	}

	response = requests.request("POST", url, headers=headers, data=payload)

	return response.json()

def Add(name, url='', mode='', iconimage=AddonInfo('icon'), fanart=AddonInfo('fanart'), description='',folder=False,playable=False):
	#This Is Where The Params Are Defined. Were Creating The Following Params ['url','mode','name','iconimage']
	u=urllib.parse.urlunparse(['plugin', AddonInfo('id'), '/', '', urlencode({'url':url,'mode':mode,'name':name,'iconimage':iconimage}), ''])
	liz = xbmcgui.ListItem(name)
	handle=sys.argv[1]
	if playable:
		liz.setProperty('isPlayable', 'true')
		liz.setInfo(type='video', infoLabels={'title':name,'mediatype':'video'})
	liz.setArt({ 'fanart': fanart,'thumb': iconimage})
	ok = xbmcplugin.addDirectoryItem(handle=int(handle), url=u, listitem=liz, isFolder=folder)
	return ok

def Get(url):
	return requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text

def daddylive(url):
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	r = re.findall(r"<iframe src=\"(.+?)\"",response)
	response = requests.get(r[0],headers={"referer":"https://daddylive.me/","user-agent":UserAgent}).text
	r = re.findall(r"source: \"(.+?)\"",response)
	return r[0]+"|Referer=%s&User-Agent=%s"%("https://myzztv.xyz/",UserAgent)

def popofthestream(url):
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	Soup = BS(response,"html.parser")
	url = "http://popofthestream.com/embed/"+Soup.find("iframe")["src"]
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	Soup = BS(response,"html.parser")
	script = str(Soup.body.find("script"))
	timestamp = str(int(time.time())*1000)
	urlpath = os.path.dirname(url)
	script = urlpath+re.findall(r"await fetch\(\"(.+?)\"",script,re.MULTILINE)[0][1:]+timestamp
	videoid = requests.get(script).json()["id"]
	url = "http://emb.x149646.apl74.me/player/live.php?id=%s&w=728&h=450" % (videoid)
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	video = re.findall(r"pl.init\(\'(.+?)\'\)",response)[0]
	return video+"|Referer=%s&User-Agent=%s"%(url,UserAgent)

def blacktiesports(url):
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	Soup = BS(response,"html.parser")
	script = Soup.body.script.contents[0]
	minus = int(re.findall(r"(\d{6,10})",script[script.find("["):])[0])
	script = re.findall(r"\"(.+?)\",",script[script.find("["):])
	string = ""
	for i in script:
		character = chr(int(re.findall(r"\d{1,}",Decode(i).decode("utf-8"))[0]) - minus)
		string +=character
	encodedurl = re.findall(r"atob\('(.+?)'\)",string)[0]
	url = Decode(encodedurl).decode()
	return url+"|Referer=%s&User-Agent=%s"%(url,UserAgent)

def yrsports(url):
	callsign = re.findall(r"ch=(.*)",url)[0]
	url = "http://out.yrsprts.io/srv/%s.m3u8"%(callsign)+"|Host=%s&Referer=%s&User-Agent=%s"%("out.yrsprts.io",url,UserAgent)
	return url

def yrsports2(url):
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	if "var dmn" in response:
		url = yrsports(url)
		return url
		# dmn = re.findall(r"var dmn = \[\"(.+?)\"",response)[0]
		# path = re.findall(r"<iframe .+?src=\"'\+rndm\+'(.+?)\" .+?<\/iframe>",response)[0]
		# url = "{domain}{path}".format(domain=dmn,path=path)
		# response = Get(url)
		# base64URL = re.findall(r"atob\('(.+?)'\);",response)[0]
		# path = Decode(base64URL).decode("utf-8")
		# dmn = urlparse(dmn).netloc
		# url = "http://{domain}{path}|User-Agent={UserAgent}".format(domain=dmn,path=path,UserAgent=UserAgent)
	else:
		url = Decode(re.findall(r"= '(.+?)';",response)[0])
	return url

def givemenbastreams(url):
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	url = re.findall(r"source: '(.+?)'",response)[0]
	return url+"|Referer=%s&User-Agent=%s"%(url,UserAgent)

def embedstream(url):
	# NOT WORKING
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	matches = re.findall(r"const pdettxt = \"(.+?)\"<\/script><script>const zmid = \"(.+?)\"; const pid = (.+?);const  edm = \"(.+?)\"",response)
	if "www.tvply.me" == matches[0][3]:
		url = "https://www.tvply.me/sdembed?v="+matches[0][1]
		data = {"pid":int(matches[0][2]),"ptxt":matches[0][0]}
		headers = {'authority': 'www.tvply.me','cache-control': 'max-age=0','sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','upgrade-insecure-requests': '1','origin': 'https://embedstream.me','content-type': 'application/x-www-form-urlencoded','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','sec-fetch-site': 'cross-site','sec-fetch-mode': 'navigate','sec-fetch-user': '?1','sec-fetch-dest': 'iframe','referer': 'http://buffstream.fun/','accept-language': 'en-US,en;q=0.9','cookie': 'tamedy=1; _pshflg=~'}
		response = Post(url,data,headers)

def sawlive(url):
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	url = re.findall(r"src=\"(.+?)\"",response)[0]
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	params = re.findall(r"var .+? = \"(.+?);(.+?)\";",response)[0]
	url = "http://www.sawlive.tv/embedm/stream/%s/%s"%(params[1],params[0])
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	evals = re.findall(r"(eval.*)",response)
	chrlist = javascript(evals[0].replace("eval","console.log"))
	chrlistdecoded = chrlist["stdout"]
	chrlist = re.findall(r"\d{1,4}",chrlistdecoded)
	url = ""
	for i in chrlist:
		character = chr(int(i))
		url += character
	return url

def cast4u(url):
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	Soup = BS(response,"html.parser")
	url = "http://cast4u.xyz"+Soup.body.iframe["src"]
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	Soup = BS(response,"html.parser")
	url = "http:"+Soup.body.iframe["src"]
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	url = re.findall(r"source:'(.+?)',",response)[0]
	return url

def streamhd247(url):
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	Soup = BS(response,"html.parser")
	url = Soup.body.iframe["src"]
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	headers = {'authority': 'wigistream.to','sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','sec-fetch-site': 'cross-site','sec-fetch-mode': 'navigate','sec-fetch-dest': 'iframe','referer': 'http://buffstream.fun/','accept-language': 'en-US,en;q=0.9','Cookie': 'hf1=1'}
	if "wigistream.to" in url:
		response = requests.get(url,headers=headers).text
		evals = re.findall(r"(eval.*)",response)
		decoded = javascript(evals[0].replace("eval","console.log"))["stdout"]
		url = re.findall(r"var src=\"(.+?)\"",decoded)[0]+"|User-Agent="+UserAgent
		return url

def bfst(url):
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	encoded = re.findall(r"source: atob\('(.+?)'\),",response)[0]
	url = Decode(encoded)
	return url

def bestsolaris(url):
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	url = re.findall(r"source: \"(.+?)\",",response)[0]
	return url

def mebystreams(url):
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	Soup = BS(response,"html.parser")
	url = Soup.find("iframe")["src"]
	headers = {"Referer":"https://mebystreams.xyz/"}
	response = requests.get(url,headers=headers).text
	url = re.findall(r"source: \"(.+?)\",",response)[0]
	return url

def Resolve(url):
	if "daddylive" in url:
		return daddylive(url)
	elif "popofthestream" in url:
		return popofthestream(url)
	elif "youtube.com" in url:
		return url
	elif "blacktiesports.net" in url:
		return blacktiesports(url)
	elif "out.yrsprts.io" in url:
		return yrsports(url)
	elif "givemenbastreams.com" in url:
		return givemenbastreams(url)
	elif "embedstream.me" in url:
		return embedstream(url)
	elif "sawlive.tv" in url:
		return sawlive(url)
	elif "cast4u.xyz" in url:
		return cast4u(url)
	elif "streamhd247.live" in url:
		return streamhd247(url)
	elif "bfst.to" in url:
		return bfst(url)
	elif "bestsolaris.com" in url:
		return bestsolaris(url)
	elif "yrsprts.io/ing/" in url:
		return yrsports2(url)
	elif "mebystreams.xyz" in url:
		return mebystreams(url)

def parseEmbed(url):
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	Soup = BS(response,"html.parser")
	url = Soup.find("iframe")["src"]
	response = requests.get(url,headers={"referer":url,"user-agent":UserAgent}).text
	Soup = BS(response,"html.parser")
	url = Soup.find("iframe")["src"]
	if url[0] == "/":url = "http:"+url
	return Resolve(url)

def Index():
	url = "https://sportshub.stream/soccer-live-streams/"
	response = Get(url)
	Soup = BS(response,"html.parser")
	Live = Soup.find_all("a",{"class":re.compile("category-line d-flex(.*)")})
	games = {}
	for i in Live:
		image = "https://sportshub.stream/"+i.span.img["src"]
		league = i.h3.text
		total = i.find("span",{"class":"p-10 ml-auto"}).text.strip()
		url = "https://sportshub.stream/"+i["href"]
		title = league.ljust(45)+str("Total: "+total).rjust(15)
		Add(title,url,"Category",image,folder=True)

def CategoryFolder(url):
	response = Get(url)
	Soup = BS(response,"html.parser")
	Today = Soup.find("div",{"id":"sports-shedule","class":"p-20 pl-lg-0 row"}).find_all("li","col-xs-12 col-lg-6")
	for game in Today:
		url = "https://sportshub.stream/"+game.a["href"]
		icon = "http:" + game.a.div.span.i["style"][22:-2] if game.a.div.span.i["style"][23] == "/" else "https://sportshub.stream" + game.a.div.span.i["style"][22:-2]
		title = game.a.find("span",{"class":"mr-5"}).text
		misc = game.find("span",{"class":"evdesc event-desc"}).span.text
		reg = re.findall(r"(.+?) \/ (.*)",misc)
		League = reg[0][0]
		time = reg[0][1]
		gameinfo = {"url":url,"icon":icon,"title":title,"league":League,"time":time}
		Add("%s | %s | %s" % (gameinfo["league"],gameinfo["time"],gameinfo["title"]),gameinfo["url"],"Game",gameinfo["icon"],folder=False)

def StreamFolder(title,url,iconimage):
	url = url.encode('latin-1', 'ignore')
	response = Get(url)
	Soup = BS(response,"html.parser")
	channels = Soup.find_all("table",{"class":"lnktbj"})
	playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	playlist.clear()
	for channel in channels:
		url = channel.find("a")["href"]
		title2 = "{title}: {type}".format(title=title,type=channel.find("td",{"class":"lnktyt"}).span.text)
		params = urlencode({"url":url,"mode":"Play","name":title2})
		playURL = "plugin://plugin.video.buffstreams/?{params}".format(params=params)
		listitem = xbmcgui.ListItem(title2)
		listitem.setInfo('video', {'Title': title2})
		listitem.setArt({'thumb': iconimage})
		playlist.add(url=playURL, listitem=listitem)
	xbmc.Player().play(playlist)
	# if "YouTube" == title:
		# Add(title,url,"Play",folder=False)
	# else:
		# Add(title,url,"Play",playable=True,folder=False)


def Playit(name,url):
	url = parseEmbed(url)
	if "YouTube" == name:
		videoid = re.findall(r"embed\/(.+?)\?autoplay=1",url)[0]
		Exe("RunPlugin(plugin://plugin.video.youtube/play/?video_id=%s)" % (videoid))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=url))
###############################################################################################################
for x in parse_qsl(sys.argv[2][1:]):globals()[x[0]] = x[1]
###############################################################################################################
try:
	if      mode        ==      "Category":     CategoryFolder(url)
	elif    mode        ==      "Game":         StreamFolder(name,url,iconimage)
	elif    mode        ==      "Play":         Playit(name,url)
	elif    mode        ==      "Test":         Resolve(url)
except:Index()
###############################################################################################################
EndOfDirectory()