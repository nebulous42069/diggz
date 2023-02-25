# -*- coding: UTF-8 -*-

import sys,re, ast , json
import six
from six.moves import urllib_parse

import requests

import collections
import io, os, json

from requests.compat import urlparse
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmc, xbmcvfs


if six.PY3:
	basestring = str
	unicode = str
	xrange = range
	from resources.lib.cmf3 import parseDOM
else:
	from resources.lib.cmf2 import parseDOM

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
params = dict(urllib_parse.parse_qsl(sys.argv[2][1:]))
addon = xbmcaddon.Addon(id='plugin.video.vix')

PATH			= addon.getAddonInfo('path')
if six.PY2:
	DATAPATH		= xbmc.translatePath(addon.getAddonInfo('profile')).decode('utf-8')
else:
	DATAPATH		= xbmcvfs.translatePath(addon.getAddonInfo('profile'))
	
if not os.path.exists(DATAPATH):
	os.mkdir(DATAPATH)

	
RESOURCES	   = PATH+'/resources/'
FANARTX=RESOURCES+'../fanart.jpg'
ikona =RESOURCES+'../icon.png'
prawo =RESOURCES+'../right.png'


exlink = params.get('url', None)
nazwa= params.get('title', None)
rys = params.get('image', None)

try:
	inflabel = ast.literal_eval(params.get('ilabel', None))
except:
	inflabel = params.get('ilabel', None)
	
#page = params.get('page',[1])[0]
lid = params.get('lastid', None)

TIMEOUT=15

main_headers = {
	'authority': 'client-api.vix.com',
	'x-vix-api-key': '8r23XTUiE2SsR7hL19qzIqg0XULLV6FkbuXWVmii1y906aSz',
	'accept': '*/*',
	'x-vix-device-type': 'desktop',
	'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36',
	'x-vix-platform': 'web',
	# Already added when you pass json=
	# 'content-type': 'application/json',
	'sec-gpc': '1',
	'origin': 'https://vix.com',
	'sec-fetch-site': 'same-site',
	'sec-fetch-mode': 'cors',
	'sec-fetch-dest': 'empty',
	'referer': 'https://vix.com/',
	'accept-language': 'en-US,en;q=0.9',}



def build_url(query):
	return base_url + '?' + urllib_parse.urlencode(query)

def add_item(url, name, image, mode,fanart=None, infoLabels=False, lastid=None, contextmenu=None,IsPlayable=False, folder=False):

	if six.PY3:	
		list_item = xbmcgui.ListItem(name)

	else:
		list_item = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
	if IsPlayable:
		list_item.setProperty("IsPlayable", 'True')	
		
	if not infoLabels:
		infoLabels={'title': name}	
	list_item.setInfo(type="video", infoLabels=infoLabels)	
	fnrt = fanart if fanart else FANARTX
	list_item.setArt({'thumb': image,'icon': image,  'poster': image, 'banner': image, 'fanart': fnrt})
	
	if contextmenu:
		out=contextmenu
		list_item.addContextMenuItems(out, replaceItems=True)
	else:
		out = []
		out.append(('Informacja', 'Action(Info)'),)
		list_item.addContextMenuItems(out, replaceItems=False)

	xbmcplugin.addDirectoryItem(
		handle=addon_handle,
		url = build_url({'mode': mode, 'url' : url, 'lastid' : lastid, 'title':name,'image':image, 'ilabel':infoLabels}),			
		listitem=list_item,
		isFolder=folder)
	xbmcplugin.addSortMethod(addon_handle, sortMethod=xbmcplugin.SORT_METHOD_NONE, label2Mask = "%R, %Y, %P")
	
def home():

	add_item('', '[B][COLOR orange]Canales[/COLOR][/B]', ikona, "listkanaly", folder=True,IsPlayable=False)	
	add_item('ondemand', '[B][COLOR orange]On Demand[/COLOR][/B]', ikona, "listvodmenu", folder=True,IsPlayable=False)
	
	
	add_item('ondemand/novelas', '[B][COLOR orange]Novelas[/COLOR][/B]', ikona, "listvodmenu", folder=True,IsPlayable=False)
	add_item('ondemand/peliculas', '[B][COLOR orange]Peliculas[/COLOR][/B]', ikona, "listvodmenu", folder=True,IsPlayable=False)
	add_item('ondemand/series', '[B][COLOR orange]Series[/COLOR][/B]', ikona, "listvodmenu", folder=True,IsPlayable=False)
	add_item('ondemand/kids', '[B][COLOR orange]Kids[/COLOR][/B]', ikona, "listvodmenu", folder=True,IsPlayable=False)
	
	add_item('deportes', '[B][COLOR orange]Deportes[/COLOR][/B]', ikona, "listvodmenu", folder=True,IsPlayable=False)
	
	add_item('noticias', '[B][COLOR orange]Noticias[/COLOR][/B]', ikona, "listvodmenu", folder=True,IsPlayable=False)


def ListVod(_idx):
	if '|' in _idx:
		_id, typ = _idx.split('|')
	else:
		_id = _idx
	vods = load_file(DATAPATH+_id, isJSON=True)
	fnrt = None

	
	
	for vod in vods:
		
		vid = vod.get('node', None).get("video", None)
		if vid:
			ser = False
			title = vid.get('title', None)
			description  = vid.get('description', None)
			#if vid.get('genres', None):
			kateg = ','.join([x.lower() for x in vid.get('genres', None) ]) if vid.get('genres', None) else ''
			year  = vid.get('copyrightYear', None)
			infolab = {'title':title, 'plot':description, 'genre':kateg, 'year':year}
			
			id = vid.get('id', None).split(':')[-1]
			
			for img in vid.get("imageAssets", None):
				if img.get("imageRole", None) == "VERTICAL_POSTER":
					imag = img.get("link", None)
					break
			
			if vid.get("videoType", None) == "MOVIE":
				durat = vid.get("videoTypeData", None).get("playbackData", None).get("streamMetadata", None).get("duration", None)
				
				infolab.update({'duration': durat})
				ser = False
			elif  vid.get("videoType", None)== "SERIES":
				id = vid.get('id', None)+'|'+_idx
				ser = True
		else:

			if vod.get('node', None).get("sportsEvent", None):
				vid = vod.get('node', None).get("sportsEvent", None)
				ser = False
				title = vid.get('name', None)
				id = vid.get('playbackData', None).get("stream", None).get('mcpId', None)

				for img in vid.get("tournament", None).get("imageAssets", None):
					if img.get("imageRole", None) == "TOURNAMENT_LOGO":
						imag = img.get("link", None)
						break
				infolab = {'title':title, 'plot':title}
			elif vod.get('node', None).get("channelId", None): #"channelId" in vod:
				
				ser = False
				nod = vod.get('node', None)
				title = nod.get("schedule", None).get("title", None)
				id = nod.get("channelId", None)
				

				imag  = nod.get("logoImage", None).get("link", None)
				fnrt = nod.get("logoImage", None).get("link", None)
				infolab = {'title':title, 'plot':title}

		mod =	 "playvid"
		fold = False
		ispla = True
		if ser:
			
			mod =	 "getseries"
			fold = True
			ispla = False
		add_item(id, title, imag, mod, fanart = fnrt,  infoLabels=infolab, folder=fold,IsPlayable=ispla)	
	xbmcplugin.endOfDirectory(addon_handle)	
	
def getSeries(idx):

	if '|' in idx:
		id, pageItemId, urlPath  = idx.split('|')
		json_data = {
			'operationName': 'DetailData',
			'variables': {
				'id': id,
				'navigationSection': {
					'urlPath': urlPath,
					'pageItemId': pageItemId,
				},
				'pagination': {
					'first': None,
					'after': None,
				},
			},
			'query': 'query DetailData($id: ID!, $navigationSection: TrackingNavigationSectionInput!, $pagination: PaginationParams!) {\n  videoById(id: $id) {\n    detailPageMetadata {\n      ...PageMetadataFragment\n      __typename\n    }\n    vodAvailability {\n      isBlocked\n      reason\n      __typename\n    }\n    ...VideoContentFullFragment\n    videoTypeData {\n      ...VideoTypeMovieFullFragment\n      ... on VideoTypeSeriesData {\n        ...VideoTypeSeriesFullFragment\n        ...SeasonsConnectionFragment\n        __typename\n      }\n      ... on VideoTypeEpisodeData {\n        ...VideoTypeEpisodeFullFragment\n        series {\n          id\n          videoTypeData {\n            ... on VideoTypeSeriesData {\n              ...VideoTypeSeriesFullFragment\n              ...SeasonsConnectionFragment\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment VideoContentFullFragment on VideoContent {\n  ...VideoContentBasicFragment\n  id\n  mcpId\n  copyrightNotice\n  language\n  ratings {\n    ratingValue\n    ratingSubValues\n    ratingSourceLink\n    __typename\n  }\n  contributors {\n    name\n    roles\n    __typename\n  }\n  copyrightOwners {\n    name\n    __typename\n  }\n  videoType\n  videoTypeData {\n    ...VideoTypeMovieFullFragment\n    ...VideoTypeEpisodeFullFragment\n    ...VideoTypeSeriesFullFragment\n    __typename\n  }\n  detailPageMetadata {\n    uploadDate\n    __typename\n  }\n  detailPageAnalyticsMetadata {\n    ...AnalyticsTrackingMetadataFragment\n    __typename\n  }\n  __typename\n}\n\nfragment ImageAssetFragment on ImageAsset {\n  filePath\n  imageRole\n  link\n  mediaType\n  __typename\n}\n\nfragment VideoContentBasicFragment on VideoContent {\n  id\n  copyrightYear\n  dateReleased\n  description\n  genres\n  headline\n  keywords\n  title\n  badges\n  contentVertical\n  ratings {\n    ratingValue\n    __typename\n  }\n  imageAssets {\n    ...ImageAssetFragment\n    __typename\n  }\n  videoType\n  videoTypeData {\n    ...VideoTypeMovieBasicFragment\n    ...VideoTypeSeriesBasicFragment\n    ...VideoTypeEpisodeBasicFragment\n    __typename\n  }\n  vodAvailability {\n    isBlocked\n    reason\n    __typename\n  }\n  __typename\n}\n\nfragment VideoTypeMovieBasicFragment on VideoTypeMovieData {\n  playbackData {\n    streamMetadata {\n      duration\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment VideoTypeSeriesBasicFragment on VideoTypeSeriesData {\n  seriesSubType\n  seasonsCount\n  episodesCount\n  __typename\n}\n\nfragment VideoTypeEpisodeBasicFragment on VideoTypeEpisodeData {\n  shortCode\n  episodeNumber\n  playbackData {\n    streamMetadata {\n      duration\n      __typename\n    }\n    __typename\n  }\n  season {\n    id\n    title\n    yearReleased\n    __typename\n  }\n  series {\n    id\n    __typename\n  }\n  __typename\n}\n\nfragment VideoTypeMovieFullFragment on VideoTypeMovieData {\n  playbackData {\n    streamMetadata {\n      duration\n      introStartPosition\n      introEndPosition\n      outroStartPosition\n      __typename\n    }\n    trackingMetadata(navigationSection: $navigationSection) {\n      ...TrackingMetadataFragment\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment TrackingMetadataFragment on VideoPlaybackTrackingData {\n  advertisingMetadata {\n    adUnit\n    keyValues {\n      key\n      value\n      __typename\n    }\n    adConfiguration\n    __typename\n  }\n  analyticsMetadata {\n    keyValues {\n      key\n      value\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment VideoTypeSeriesFullFragment on VideoTypeSeriesData {\n  seriesSubType\n  seasonsCount\n  episodesCount\n  currentSeason {\n    id\n    title\n    __typename\n  }\n  __typename\n}\n\nfragment VideoTypeEpisodeFullFragment on VideoTypeEpisodeData {\n  shortCode\n  episodeNumber\n  playbackData {\n    streamMetadata {\n      duration\n      introStartPosition\n      introEndPosition\n      outroStartPosition\n      __typename\n    }\n    trackingMetadata(navigationSection: $navigationSection) {\n      ...TrackingMetadataFragment\n      __typename\n    }\n    __typename\n  }\n  series {\n    id\n    title\n    __typename\n  }\n  season {\n    id\n    title\n    __typename\n  }\n  __typename\n}\n\nfragment AnalyticsTrackingMetadataFragment on AnalyticsTrackingMetadata {\n  keyValues {\n    key\n    value\n    __typename\n  }\n  __typename\n}\n\nfragment SeasonsConnectionFragment on VideoTypeSeriesData {\n  seasonsConnection(pagination: $pagination) {\n    totalCount\n    edges {\n      cursor\n      node {\n        id\n        title\n        yearReleased\n        episodesConnection(pagination: {first: null, after: null}) {\n          edges {\n            node {\n              id\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    pageInfo {\n      ...PageInfoFragment\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment PageInfoFragment on PageInfo {\n  hasPreviousPage\n  hasNextPage\n  startCursor\n  endCursor\n  __typename\n}\n\nfragment PageMetadataFragment on PageMetadata {\n  title\n  description\n  canonicalUrl\n  altUrls\n  uploadDate\n  twitter {\n    card\n    site\n    description\n    title\n    image\n    imageAlt\n    __typename\n  }\n  og {\n    title\n    type\n    image {\n      url\n      type\n      width\n      height\n      alt\n      __typename\n    }\n    url\n    description\n    siteName\n    locale\n    localeAlternative\n    __typename\n  }\n  __typename\n}',
		}

	else:
		json_data = {
			'operationName': 'DetailData',
			'variables': {
				'id': idx,
				'pagination': {
					'first': None,
					'after': None,
				},
			},
			'query': 'query DetailData($id: ID!, $pagination: PaginationParams!) {\n  videoById(id: $id) {\n	detailPageMetadata {\n	  ...PageMetadataFragment\n	  __typename\n	}\n	streamAvailability {\n	  isBlocked\n	  reason\n	  __typename\n	}\n	...VideoContentFullFragment\n	videoTypeData {\n	  ...VideoTypeMovieFullFragment\n	  ... on VideoTypeSeriesData {\n		...VideoTypeSeriesFullFragment\n		...SeasonsConnectionFragment\n		__typename\n	  }\n	  ... on VideoTypeEpisodeData {\n		...VideoTypeEpisodeFullFragment\n		series {\n		  id\n		  videoTypeData {\n			... on VideoTypeSeriesData {\n			  ...VideoTypeSeriesFullFragment\n			  ...SeasonsConnectionFragment\n			  __typename\n			}\n			__typename\n		  }\n		  __typename\n		}\n		__typename\n	  }\n	  __typename\n	}\n	__typename\n  }\n}\n\nfragment VideoContentFullFragment on VideoContent {\n  ...VideoContentBasicFragment\n  id\n  mcpId\n  copyrightNotice\n  language\n  ratings {\n	ratingValue\n	ratingSubValues\n	ratingSourceLink\n	__typename\n  }\n  contributors {\n	name\n	roles\n	__typename\n  }\n  copyrightOwners {\n	name\n	__typename\n  }\n  videoType\n  videoTypeData {\n	...VideoTypeMovieFullFragment\n	...VideoTypeEpisodeFullFragment\n	...VideoTypeSeriesFullFragment\n	__typename\n  }\n  detailPageMetadata {\n	uploadDate\n	__typename\n  }\n  detailPageAnalyticsMetadata {\n	...AnalyticsTrackingMetadataFragment\n	__typename\n  }\n  __typename\n}\n\nfragment ImageAssetFragment on ImageAsset {\n  filePath\n  imageRole\n  link\n  mediaType\n  __typename\n}\n\nfragment VideoContentBasicFragment on VideoContent {\n  id\n  copyrightYear\n  dateReleased\n  description\n  genres\n  headline\n  keywords\n  title\n  badge\n  yearReleased\n  contentVertical\n  ratings {\n	ratingValue\n	__typename\n  }\n  imageAssets {\n	...ImageAssetFragment\n	__typename\n  }\n  videoType\n  videoTypeData {\n	...VideoTypeMovieBasicFragment\n	...VideoTypeSeriesBasicFragment\n	...VideoTypeEpisodeBasicFragment\n	__typename\n  }\n  streamAvailability {\n	isBlocked\n	reason\n	__typename\n  }\n  __typename\n}\n\nfragment VideoTypeMovieBasicFragment on VideoTypeMovieData {\n  playbackData {\n	streamMetadata {\n	  duration\n	  __typename\n	}\n	__typename\n  }\n  __typename\n}\n\nfragment VideoTypeSeriesBasicFragment on VideoTypeSeriesData {\n  seriesSubType\n  seasonsCount\n  episodesCount\n  __typename\n}\n\nfragment VideoTypeEpisodeBasicFragment on VideoTypeEpisodeData {\n  shortCode\n  episodeNumber\n  playbackData {\n	streamMetadata {\n	  duration\n	  __typename\n	}\n	__typename\n  }\n  season {\n	id\n	title\n	yearReleased\n	__typename\n  }\n  series {\n	id\n	__typename\n  }\n  __typename\n}\n\nfragment VideoTypeMovieFullFragment on VideoTypeMovieData {\n  playbackData {\n	streamMetadata {\n	  duration\n	  introStartPosition\n	  introEndPosition\n	  outroStartPosition\n	  __typename\n	}\n	trackingMetadata(navigationSection: $navigationSection) {\n	  ...TrackingMetadataFragment\n	  __typename\n	}\n	__typename\n  }\n  __typename\n}\n\nfragment TrackingMetadataFragment on VideoPlaybackTrackingData {\n  advertisingMetadata {\n	adUnit\n	keyValues {\n	  key\n	  value\n	  __typename\n	}\n	adConfiguration\n	__typename\n  }\n  analyticsMetadata {\n	keyValues {\n	  key\n	  value\n	  __typename\n	}\n	__typename\n  }\n  __typename\n}\n\nfragment VideoTypeSeriesFullFragment on VideoTypeSeriesData {\n  seriesSubType\n  seasonsCount\n  episodesCount\n  currentSeason {\n	id\n	title\n	__typename\n  }\n  profileCurrentEpisode {\n	id\n	__typename\n  }\n  __typename\n}\n\nfragment VideoTypeEpisodeFullFragment on VideoTypeEpisodeData {\n  shortCode\n  episodeNumber\n  playbackData {\n	streamMetadata {\n	  duration\n	  introStartPosition\n	  introEndPosition\n	  outroStartPosition\n	  __typename\n	}\n	trackingMetadata(navigationSection: $navigationSection) {\n	  ...TrackingMetadataFragment\n	  __typename\n	}\n	__typename\n  }\n  series {\n	id\n	title\n	__typename\n  }\n  season {\n	id\n	title\n	__typename\n  }\n  __typename\n}\n\nfragment AnalyticsTrackingMetadataFragment on AnalyticsTrackingMetadata {\n  keyValues {\n	key\n	value\n	__typename\n  }\n  __typename\n}\n\nfragment SeasonsConnectionFragment on VideoTypeSeriesData {\n  seasonsConnection(pagination: $pagination) {\n	totalCount\n	edges {\n	  cursor\n	  node {\n		id\n		title\n		yearReleased\n		episodesConnection(pagination: {first: null, after: null}) {\n		  edges {\n			node {\n			  id\n			  __typename\n			}\n			__typename\n		  }\n		  __typename\n		}\n		__typename\n	  }\n	  __typename\n	}\n	pageInfo {\n	  ...PageInfoFragment\n	  __typename\n	}\n	__typename\n  }\n  __typename\n}\n\nfragment PageInfoFragment on PageInfo {\n  hasPreviousPage\n  hasNextPage\n  startCursor\n  endCursor\n  __typename\n}\n\nfragment PageMetadataFragment on PageMetadata {\n  title\n  description\n  canonicalUrl\n  altUrls\n  uploadDate\n  twitter {\n	card\n	site\n	description\n	title\n	image\n	imageAlt\n	__typename\n  }\n  og {\n	title\n	type\n	image {\n	  url\n	  type\n	  width\n	  height\n	  alt\n	  __typename\n	}\n	url\n	description\n	siteName\n	locale\n	localeAlternative\n	__typename\n  }\n  __typename\n}',
		}
	


	response = requests.post('https://client-api.vix.com/gql/v2', headers=main_headers, json=json_data)#.text

	dane = response.json().get("data", None).get("videoById", None)
	title = dane.get("title", None)
	description = dane.get("description", None)
	fnrt = dane.get("detailPageMetadata", None).get("og", None).get("image", None)[0].get("url", None)
	
	year  = dane.get("detailPageMetadata", None).get('copyrightYear', None)
	
	for img in dane.get("imageAssets", None):
		if img.get("imageRole", None) == "VERTICAL_POSTER":
			imag = img.get("link", None)
			break
	infolab = {'plot':description, 'year':year}
	sesedges = dane.get("videoTypeData", None).get("seasonsConnection", None).get("edges", [])
	for edg in sesedges:
		nod = edg.get("node", None)
		ses_id = nod.get("id", None)
		titleses = nod.get("title", None)

		mod =	 "getepisodes"
		fold = True
		ispla = False
		ntid = id+'|'+ses_id
		sestitle = title+' ' +titleses
		add_item(ntid, sestitle, imag, mod, fanart = fnrt, infoLabels=infolab, folder=fold,IsPlayable=ispla)
		
	xbmcplugin.endOfDirectory(addon_handle)	
	
def getEpisodes(mainid_sesid):
	seriesId, seasonId = mainid_sesid.split('|')
	json_data = {
		'operationName': 'SeasonById',
		'variables': {
			'seriesId': seriesId,
			'seasonId': seasonId,
			'episodePagination': {
				'first': None,
				'after': None,
			},
		},
		'query': 'query SeasonById($seriesId: ID!, $seasonId: ID!, $episodePagination: PaginationParams!) {\n  seasonById(seriesId: $seriesId, seasonId: $seasonId) {\n	id\n	title\n	yearReleased\n	episodesConnection(pagination: $episodePagination) {\n	  totalCount\n	  edges {\n		cursor\n		node {\n		  ...EpisodeFullFragment\n		  id\n		  title\n		  description\n		  ratings {\n			ratingValue\n			__typename\n		  }\n		  imageAssets {\n			...ImageAssetFragment\n			__typename\n		  }\n		  videoTypeData {\n			...VideoTypeEpisodeFullFragment\n			__typename\n		  }\n		  __typename\n		}\n		__typename\n	  }\n	  pageInfo {\n		...PageInfoFragment\n		__typename\n	  }\n	  __typename\n	}\n	__typename\n  }\n}\n\nfragment PageInfoFragment on PageInfo {\n  hasPreviousPage\n  hasNextPage\n  startCursor\n  endCursor\n  __typename\n}\n\nfragment ImageAssetFragment on ImageAsset {\n  filePath\n  imageRole\n  link\n  mediaType\n  __typename\n}\n\nfragment TrackingMetadataFragment on VideoPlaybackTrackingData {\n  advertisingMetadata {\n	adUnit\n	keyValues {\n	  key\n	  value\n	  __typename\n	}\n	adConfiguration\n	__typename\n  }\n  analyticsMetadata {\n	keyValues {\n	  key\n	  value\n	  __typename\n	}\n	__typename\n  }\n  __typename\n}\n\nfragment EpisodeFullFragment on VideoContent {\n  id\n  copyrightYear\n  dateReleased\n  description\n  headline\n  title\n  videoType\n  videoTypeData {\n	...VideoTypeEpisodeBasicFragment\n	__typename\n  }\n  ratings {\n	ratingValue\n	__typename\n  }\n  imageAssets {\n	...ImageAssetFragment\n	__typename\n  }\n  __typename\n}\n\nfragment VideoTypeEpisodeBasicFragment on VideoTypeEpisodeData {\n  shortCode\n  episodeNumber\n  playbackData {\n	streamMetadata {\n	  duration\n	  __typename\n	}\n	__typename\n  }\n  season {\n	id\n	title\n	yearReleased\n	__typename\n  }\n  series {\n	id\n	__typename\n  }\n  __typename\n}\n\nfragment VideoTypeEpisodeFullFragment on VideoTypeEpisodeData {\n  shortCode\n  episodeNumber\n  playbackData {\n	streamMetadata {\n	  duration\n	  introStartPosition\n	  introEndPosition\n	  outroStartPosition\n	  __typename\n	}\n	\n	__typename\n  }\n  series {\n	id\n	title\n	__typename\n  }\n  season {\n	id\n	title\n	__typename\n  }\n  __typename\n}',
	}
	
	response = requests.post('https://client-api.vix.com/gql/v2', headers=main_headers, json=json_data)

	edges = response.json().get("data", None).get("seasonById", None).get("episodesConnection", None).get("edges", None)
	for edg in edges:
		nod = edg.get("node", None)
		year = nod.get("copyrightYear", None)
	
		title = nod.get("title", None)
		description = nod.get("description", None)
		id = nod.get("id", None).split(':')[-1]
		for img in nod.get("imageAssets", None):
			if img.get("imageRole", None) == 'SNAPSHOT':
				imag = img.get("link", None)
				break
		durat = nod.get("videoTypeData", None).get("playbackData", None).get("streamMetadata", None).get("duration", None)
		infolab = {'plot':description, 'year':year, 'duration':durat}
		mod =	 "playvid"
		fold = False
		ispla = True

		add_item(id, title, imag, mod, infoLabels=infolab, folder=fold,IsPlayable=ispla)	
	xbmcplugin.endOfDirectory(addon_handle)	

def ListVodMenu(typ, last_id):

	json_data = {
		'operationName': 'PageData',
		'variables': {
			'urlPath': '/'+typ,
			'uiModulesPagination': {
				'first': 8,
				'after': last_id,
			},
			'contentPagination': {
				'first': 20,
				'after': None,
			},
		},
		'query': 'query PageData($urlPath: ID!, $uiModulesPagination: PaginationParams, $contentPagination: PaginationParams) {\n  uiPage(urlPath: $urlPath) {\n	urlPath\n	pageName\n	pageMetadata {\n	  ...PageMetadataFragment\n	  __typename\n	}\n	pageAnalyticsMetadata {\n	  ...AnalyticsTrackingMetadataFragment\n	  __typename\n	}\n	pageAvailability {\n	  isBlocked\n	  reason\n	  __typename\n	}\n	uiModules(pagination: $uiModulesPagination) {\n	  totalCount\n	  edges {\n		cursor\n		node {\n		  ...UiContinueWatchingCarouselFragment\n		  ...UiVideoCarouselFragment\n		  ...UiHeroCarouselFragment\n		  ...UiLiveVideoCarouselFragment\n		  ...UiPageCarouselFragment\n		  ...UiSportsEventCarouselFragment\n		  __typename\n		}\n		__typename\n	  }\n	  pageInfo {\n		...PageInfoFragment\n		__typename\n	  }\n	  __typename\n	}\n	__typename\n  }\n}\n\nfragment PageInfoFragment on PageInfo {\n  hasPreviousPage\n  hasNextPage\n  startCursor\n  endCursor\n  __typename\n}\n\nfragment UiContinueWatchingCarouselFragment on UiContinueWatchingCarousel {\n  moduleType\n  trackingId\n  title\n  treatment\n  contents {\n	totalCount\n	edges {\n	  node {\n		image {\n		  ...ImageAssetFragment\n		  __typename\n		}\n		video {\n		  ...VideoContentBasicFragment\n		  __typename\n		}\n		__typename\n	  }\n	  __typename\n	}\n	pageInfo {\n	  ...PageInfoFragment\n	  __typename\n	}\n	__typename\n  }\n  __typename\n}\n\nfragment ImageAssetFragment on ImageAsset {\n  filePath\n  imageRole\n  link\n  mediaType\n  __typename\n}\n\nfragment VideoContentBasicFragment on VideoContent {\n  id\n  copyrightYear\n  dateReleased\n  description\n  genres\n  headline\n  keywords\n  title\n  badge\n  yearReleased\n  contentVertical\n  ratings {\n	ratingValue\n	__typename\n  }\n  imageAssets {\n	...ImageAssetFragment\n	__typename\n  }\n  videoType\n  videoTypeData {\n	...VideoTypeMovieBasicFragment\n	...VideoTypeSeriesBasicFragment\n	...VideoTypeEpisodeBasicFragment\n	__typename\n  }\n  streamAvailability {\n	isBlocked\n	reason\n	__typename\n  }\n  __typename\n}\n\nfragment VideoTypeMovieBasicFragment on VideoTypeMovieData {\n  playbackData {\n	streamMetadata {\n	  duration\n	  __typename\n	}\n	__typename\n  }\n  __typename\n}\n\nfragment VideoTypeSeriesBasicFragment on VideoTypeSeriesData {\n  seriesSubType\n  seasonsCount\n  episodesCount\n  __typename\n}\n\nfragment VideoTypeEpisodeBasicFragment on VideoTypeEpisodeData {\n  shortCode\n  episodeNumber\n  playbackData {\n	streamMetadata {\n	  duration\n	  __typename\n	}\n	__typename\n  }\n  season {\n	id\n	title\n	yearReleased\n	__typename\n  }\n  series {\n	id\n	__typename\n  }\n  __typename\n}\n\nfragment UiVideoCarouselFragment on UiVideoCarousel {\n  moduleType\n  trackingId\n  title\n  treatment\n  landscapeFillImage {\n	...ImageAssetFragment\n	__typename\n  }\n  portraitFillImage {\n	...ImageAssetFragment\n	__typename\n  }\n  sponsorMetadata {\n	logoImage {\n	  ...ImageAssetFragment\n	  __typename\n	}\n	__typename\n  }\n  contents(pagination: $contentPagination) {\n	carouselId\n	totalCount\n	edges {\n	  node {\n		subTitle\n		image {\n		  ...ImageAssetFragment\n		  __typename\n		}\n		logoImage {\n		  ...ImageAssetFragment\n		  __typename\n		}\n		video {\n		  ...VideoContentBasicFragment\n		  __typename\n		}\n		__typename\n	  }\n	  __typename\n	}\n	pageInfo {\n	  ...PageInfoFragment\n	  __typename\n	}\n	__typename\n  }\n  __typename\n}\n\nfragment UiHeroCarouselFragment on UiHeroCarousel {\n  moduleType\n  trackingId\n  title\n  contents {\n	totalCount\n	edges {\n	  node {\n		textTitle\n		heroTargetContentType\n		logoImage {\n		  ...ImageAssetFragment\n		  __typename\n		}\n		sponsorMetadata {\n		  logoImage {\n			...ImageAssetFragment\n			__typename\n		  }\n		  __typename\n		}\n		landscapeFillImage {\n		  ...ImageAssetFragment\n		  __typename\n		}\n		portraitFillImage {\n		  ...ImageAssetFragment\n		  __typename\n		}\n		heroTarget {\n		  ...VideoContentBasicFragment\n		  ...EpgChannelBasicFragment\n		  ...SportsEventBasicFragment\n		  __typename\n		}\n		__typename\n	  }\n	  __typename\n	}\n	pageInfo {\n	  ...PageInfoFragment\n	  __typename\n	}\n	__typename\n  }\n  __typename\n}\n\nfragment EpgChannelBasicFragment on EpgChannel {\n  id\n  channelNumber\n  description\n  title\n  __typename\n}\n\nfragment SportsEventBasicFragment on SportsEvent {\n  id\n  name\n  tournament {\n	...SportsTournamentFragment\n	__typename\n  }\n  playbackData {\n	scheduledStartTime\n	scheduledEndTime\n	kickoffDate\n	streamId\n	stream {\n	  mcpId\n	  __typename\n	}\n	__typename\n  }\n  streamAvailability {\n	isBlocked\n	reason\n	__typename\n  }\n  __typename\n}\n\nfragment SportsTournamentFragment on SportsTournament {\n  id\n  name\n  tournamentType\n  imageAssets {\n	...ImageAssetFragment\n	__typename\n  }\n  __typename\n}\n\nfragment UiLiveVideoCarouselFragment on UiLiveVideoCarousel {\n  moduleType\n  trackingId\n  title\n  treatment\n  contents {\n	...LiveVideoCarouselContentsFragment\n	__typename\n  }\n  __typename\n}\n\nfragment LiveVideoCarouselContentsFragment on UiLiveVideoCardConnection {\n  totalCount\n  carouselId\n  edges {\n	node {\n	  channelId\n	  logoImage {\n		...ImageAssetFragment\n		__typename\n	  }\n	  image {\n		...ImageAssetFragment\n		__typename\n	  }\n	  schedule {\n		id\n		title\n		startDate\n		endDate\n		imageAssets {\n		  ...ImageAssetFragment\n		  __typename\n		}\n		video {\n		  ...VideoContentBasicFragment\n		  __typename\n		}\n		__typename\n	  }\n	  __typename\n	}\n	__typename\n  }\n  pageInfo {\n	...PageInfoFragment\n	__typename\n  }\n  __typename\n}\n\nfragment UiPageCarouselFragment on UiPageCarousel {\n  moduleType\n  trackingId\n  title\n  treatment\n  contents {\n	totalCount\n	edges {\n	  node {\n		name\n		urlPath\n		image {\n		  ...ImageAssetFragment\n		  __typename\n		}\n		__typename\n	  }\n	  __typename\n	}\n	pageInfo {\n	  ...PageInfoFragment\n	  __typename\n	}\n	__typename\n  }\n  __typename\n}\n\nfragment UiSportsEventCarouselFragment on UiSportsEventCarousel {\n  moduleType\n  trackingId\n  title\n  treatment\n  sportId\n  isLive\n  leagueId\n  contents(pagination: $contentPagination) {\n	carouselId\n	totalCount\n	edges {\n	  node {\n		sportsEventId\n		sportsEvent {\n		  ...SportsEventBasicFragment\n		  __typename\n		}\n		tournamentLogo {\n		  ...ImageAssetFragment\n		  __typename\n		}\n		tournamentCardBackground {\n		  ...ImageAssetFragment\n		  __typename\n		}\n		localTeamLogo {\n		  ...ImageAssetFragment\n		  __typename\n		}\n		awayTeamLogo {\n		  ...ImageAssetFragment\n		  __typename\n		}\n		compositeImageLink\n		__typename\n	  }\n	  __typename\n	}\n	pageInfo {\n	  ...PageInfoFragment\n	  __typename\n	}\n	__typename\n  }\n  __typename\n}\n\nfragment AnalyticsTrackingMetadataFragment on AnalyticsTrackingMetadata {\n  keyValues {\n	key\n	value\n	__typename\n  }\n  __typename\n}\n\nfragment PageMetadataFragment on PageMetadata {\n  title\n  description\n  canonicalUrl\n  altUrls\n  uploadDate\n  twitter {\n	card\n	site\n	description\n	title\n	image\n	imageAlt\n	__typename\n  }\n  og {\n	title\n	type\n	image {\n	  url\n	  type\n	  width\n	  height\n	  alt\n	  __typename\n	}\n	url\n	description\n	siteName\n	locale\n	localeAlternative\n	__typename\n  }\n  __typename\n}',
	}
	
	response = requests.post('https://client-api.vix.com/gql/v2', headers=main_headers, json=json_data)#.text

	uiModules = response.json().get('data', None).get('uiPage', None).get('uiModules', None)#.get("edges",[])
	edges = uiModules.get("edges",[])
	pageinfo = uiModules.get("pageInfo", None)
	ntpage = None

	for edg in edges:
		if edg.get("node", None).get("moduleType", None) == "SPORTS_EVENT_CAROUSEL" or edg.get("node", None).get("moduleType", None) == "VIDEO_CAROUSEL" or edg.get("node", None).get("moduleType", None) =="LIVE_VIDEO_CAROUSEL":

			title = edg.get("node", None).get("title", None)
			trackingId = edg.get("node", None).get("trackingId", None)
			edgesx = edg.get("node", None).get("contents", None).get("edges", None)
			save_file(file=DATAPATH+trackingId, data=edgesx, isJSON=True)
			add_item(trackingId+'|/'+typ, title, ikona, "listvod", infoLabels={'plot':title}, folder=True,IsPlayable=False)	
	if pageinfo.get("hasNextPage", None):
		add_item(typ, '[B][COLOR orange]>> Next Page >>[/COLOR][/B]', ikona, "listvodmenu", infoLabels={'plot':title}, lastid = pageinfo.get("endCursor", None), folder=True,IsPlayable=False)

	xbmcplugin.endOfDirectory(addon_handle)	
			

def CreateAnvtrid():
	import time
	import hashlib

	str2hash = str(int(time.time() * 1000.0))
	result = hashlib.md5(str2hash.encode())

	a=(result.hexdigest())

	c =a[-24:]

	anvtrid = "w"+"07cbac93"+c
	return anvtrid
	
	

def crypt_url(url):
	import time
	import hashlib
	# ts stores the time in seconds
	timestamp = str(int(time.time() * 1000.0))

	md5url = hashlib.md5(url.encode())
	md5url = (md5url.hexdigest())
	n = timestamp+"~" + md5url + "~"
	i = hashlib.md5(timestamp.encode())
	i = (i.hexdigest())
	a= max(64-len(n),0)
	i = i[0:a]
	n+=i

	try:  # The crypto package depends on the library installed (see Wiki)
		from Cryptodome.Cipher import AES

	except ImportError:
		from Crypto.Cipher import AES

	iv = "31c242849e73a0ce".encode()
	key="31c242849e73a0ce"

	cipher = AES.new(iv, AES.MODE_ECB);
	
	
	ct = n

	result = cipher.encrypt(ct.encode());
	import base64
	auth = base64.b64encode(result)
	return auth.decode()

def save_file(file, data, isJSON=False):
	with io.open(file, 'w', encoding="utf-8") as f:
		if isJSON == True:
			str_ = json.dumps(data,indent=4, sort_keys=True,separators=(',', ': '), ensure_ascii=False)
			f.write(str(str_))
		else:
			f.write(data)

def load_file(file, isJSON=False):

	if not os.path.isfile(file):
		return None

	with io.open(file, 'r', encoding='utf-8') as f:
		if isJSON == True:
			return json.load(f, object_pairs_hook=collections.OrderedDict)
		else:
			return f.read() 









def getEpgsKateg():

	json_data = {
		'operationName': 'EpgData',
		'variables': {
			'count': 2,
		},
		'query': 'query EpgData($count: Int!) {\n  epgCategories {\n	edges {\n	  cursor\n	  node {\n		id\n		title\n		description\n		imageAssets {\n		  ...ImageAssetFragment\n		  __typename\n		}\n		channels {\n		  edges {\n			cursor\n			node {\n			  ...EpgChannelFullFragment\n			  pageAnalyticsMetadata {\n				...AnalyticsTrackingMetadataFragment\n				__typename\n			  }\n			  upcomingSchedule(count: $count) {\n				...ScheduleItemFragment\n				video {\n				  epgId: id\n				  ...VideoContentBasicFragment\n				  __typename\n				}\n				__typename\n			  }\n			  __typename\n			}\n			__typename\n		  }\n		  __typename\n		}\n		__typename\n	  }\n	  __typename\n	}\n	__typename\n  }\n}\n\nfragment ImageAssetFragment on ImageAsset {\n  filePath\n  imageRole\n  link\n  mediaType\n  __typename\n}\n\nfragment ScheduleItemFragment on ScheduleItem {\n  id\n  startDate\n  endDate\n  vodAvailable\n  title\n  subtitle\n  __typename\n}\n\nfragment EpgChannelFullFragment on EpgChannel {\n  id\n  title\n  isLive\n  channelNumber\n  description\n  backgroundColor\n  imageAssets {\n	...ImageAssetFragment\n	__typename\n  }\n  stream {\n	mcpId\n	__typename\n  }\n  __typename\n}\n\nfragment VideoContentBasicFragment on VideoContent {\n  id\n  copyrightYear\n  dateReleased\n  description\n  genres\n  headline\n  keywords\n  title\n  badge\n  yearReleased\n  contentVertical\n  ratings {\n	ratingValue\n	__typename\n  }\n  imageAssets {\n	...ImageAssetFragment\n	__typename\n  }\n  videoType\n  videoTypeData {\n	...VideoTypeMovieBasicFragment\n	...VideoTypeSeriesBasicFragment\n	...VideoTypeEpisodeBasicFragment\n	__typename\n  }\n  streamAvailability {\n	isBlocked\n	reason\n	__typename\n  }\n  __typename\n}\n\nfragment VideoTypeMovieBasicFragment on VideoTypeMovieData {\n  playbackData {\n	streamMetadata {\n	  duration\n	  __typename\n	}\n	__typename\n  }\n  __typename\n}\n\nfragment VideoTypeSeriesBasicFragment on VideoTypeSeriesData {\n  seriesSubType\n  seasonsCount\n  episodesCount\n  __typename\n}\n\nfragment VideoTypeEpisodeBasicFragment on VideoTypeEpisodeData {\n  shortCode\n  episodeNumber\n  playbackData {\n	streamMetadata {\n	  duration\n	  __typename\n	}\n	__typename\n  }\n  season {\n	id\n	title\n	yearReleased\n	__typename\n  }\n  series {\n	id\n	__typename\n  }\n  __typename\n}\n\nfragment AnalyticsTrackingMetadataFragment on AnalyticsTrackingMetadata {\n  keyValues {\n	key\n	value\n	__typename\n  }\n  __typename\n}',
	}
	
	response = requests.post('https://client-api.vix.com/gql/v2', headers=main_headers, json=json_data)#.json()
	edges = response.json().get('data', None).get('epgCategories', None).get('edges', None)
	return edges
	
def ListKanaly():
	edges = getEpgsKateg()

	for edg in edges:
		id = edg.get('node', None).get('id',None)
		title = edg.get('node', None).get('title',None)
		description = edg.get('node', None).get('description',None)
		dt = edg.get('node', None).get("channels", None) 
		save_file(file=DATAPATH+id, data=dt, isJSON=True)
		add_item(id, title, ikona, "listkateg", infoLabels={'plot':description}, folder=True,IsPlayable=False)	

	xbmcplugin.endOfDirectory(addon_handle)	
	
def ListKateg(idx):
	channels = load_file(DATAPATH+idx, isJSON=True)
	edges = channels.get('edges', None)
	for chan in edges:
		nod = chan.get("node", None)
		title = nod.get('title', None)
		id_ = nod.get("id", None)
		stream_id = nod.get("stream", None).get('mcpId', None)
		description = nod.get("description", None)
		for img in nod.get("imageAssets", None):
			if img.get("imageRole", None) == "CHANNEL_LOGO":
				imag = img.get("link", None)
				break
		add_item(stream_id, title, imag, "playvid", infoLabels={'plot':description}, folder=False ,IsPlayable=True)	
	xbmcplugin.endOfDirectory(addon_handle)	
def getRealStream_id(_id):
	json_data = {
		'operationName': 'ChannelData',
		'variables': {
			'id': _id,
			'count': 2,
		},
		'query': 'query ChannelData($id: ID!, $count: Int!) {\n  channelById(id: $id) {\n	...EpgChannelFullFragment\n	pageAnalyticsMetadata {\n	  ...AnalyticsTrackingMetadataFragment\n	  __typename\n	}\n	upcomingSchedule(count: $count) {\n	  ...ScheduleItemFragment\n	  video {\n		...VideoContentBasicFragment\n		__typename\n	  }\n	  __typename\n	}\n	__typename\n  }\n}\n\nfragment EpgChannelFullFragment on EpgChannel {\n  id\n  title\n  isLive\n  channelNumber\n  description\n  backgroundColor\n  imageAssets {\n	...ImageAssetFragment\n	__typename\n  }\n  stream {\n	mcpId\n	__typename\n  }\n  __typename\n}\n\nfragment ImageAssetFragment on ImageAsset {\n  filePath\n  imageRole\n  link\n  mediaType\n  __typename\n}\n\nfragment ScheduleItemFragment on ScheduleItem {\n  id\n  startDate\n  endDate\n  vodAvailable\n  title\n  subtitle\n  __typename\n}\n\nfragment VideoContentBasicFragment on VideoContent {\n  id\n  copyrightYear\n  dateReleased\n  description\n  genres\n  headline\n  keywords\n  title\n  badge\n  yearReleased\n  contentVertical\n  ratings {\n	ratingValue\n	__typename\n  }\n  imageAssets {\n	...ImageAssetFragment\n	__typename\n  }\n  videoType\n  videoTypeData {\n	...VideoTypeMovieBasicFragment\n	...VideoTypeSeriesBasicFragment\n	...VideoTypeEpisodeBasicFragment\n	__typename\n  }\n  streamAvailability {\n	isBlocked\n	reason\n	__typename\n  }\n  __typename\n}\n\nfragment VideoTypeMovieBasicFragment on VideoTypeMovieData {\n  playbackData {\n	streamMetadata {\n	  duration\n	  __typename\n	}\n	__typename\n  }\n  __typename\n}\n\nfragment VideoTypeSeriesBasicFragment on VideoTypeSeriesData {\n  seriesSubType\n  seasonsCount\n  episodesCount\n  __typename\n}\n\nfragment VideoTypeEpisodeBasicFragment on VideoTypeEpisodeData {\n  shortCode\n  episodeNumber\n  playbackData {\n	streamMetadata {\n	  duration\n	  __typename\n	}\n	__typename\n  }\n  season {\n	id\n	title\n	yearReleased\n	__typename\n  }\n  series {\n	id\n	__typename\n  }\n  __typename\n}\n\nfragment AnalyticsTrackingMetadataFragment on AnalyticsTrackingMetadata {\n  keyValues {\n	key\n	value\n	__typename\n  }\n  __typename\n}',
	}
	
	response = requests.post('https://client-api.vix.com/gql/v2', headers=main_headers, json=json_data)
	stream_id = response.json().get("data", None).get("channelById", None).get("stream", None).get("mcpId", None)
	return stream_id

		
def PlayVid(stream_id):
	if 'channel:mcp' in stream_id:
		stream_id = getRealStream_id(stream_id)
	license_url = ''
	import inputstreamhelper


	import time
	import random
	import hashlib

	str2hash = str(int(time.time() * 1000.0))
	headers = {
		'Host': 'vix.com',

		'x-video-type': 'Livestream',

		'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36',
		'accept': '*/*',
		'sec-gpc': '1',
		'sec-fetch-site': 'same-origin',
		'sec-fetch-mode': 'cors',
		'sec-fetch-dest': 'empty',
		'referer': 'https://vix.com/es-es/canales',
		'accept-language': 'en-US,en;q=0.9',
	}

	f=requests.get('https://vix.com/api/video/token?videoId='+stream_id+'&timestamp='+str2hash, headers=headers, verify=False)
		
	accesskey = f.json().get('accessKey', None)
	token = f.json().get('token', None)
	
	
	anvtrid = CreateAnvtrid()
	url2crypt = 'https://tkx.mp.lura.live/rest/v2/mcp/video/'+stream_id+'anvack='+accesskey+'&anvtrid='+anvtrid	
	anvatoauth =	 crypt_url(url2crypt)
	
	czas = int(time.time())
	str2hash = str(czas * random.random())
	anvrid = hashlib.md5(str2hash.encode())

	anvrid=(anvrid.hexdigest())[0:30]

	headers = {
		'Host': 'tkx.mp.lura.live',
		'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36',
		'content-type': 'application/x-www-form-urlencoded',
		'accept': '*/*',
		'sec-gpc': '1',
		'origin': 'https://vix.com',
		'sec-fetch-site': 'cross-site',
		'sec-fetch-mode': 'cors',
		'sec-fetch-dest': 'empty',
		'referer': 'https://vix.com/',
		'accept-language': 'en-US,en;q=0.9',
	}

	params = {
		'anvack': accesskey,
		'anvtrid': anvtrid,
		'rtyp': 'fp',
		'X-Anvato-Adst-Auth': anvatoauth,
	}
	
	data = '{"api":{"anvrid":"'+anvrid+'","anvts":'+str(czas)+',"anvstk2":"'+token+'"}}'
	
	response = requests.post('https://tkx.mp.lura.live/rest/v2/mcp/video/'+stream_id, params=params, headers=headers, data=data, verify=False).text
	jstext = re.findall('\(({".*?})\)',response,re.DOTALL)[0]
	jsdata = json.loads(jstext)

	if not '"format":"dash' in jstext:
		embed_url = re.findall('"embed_url"\:"([^"]+)',jstext, re.DOTALL)#[0]
		embed_url = embed_url[0].replace("\\/",'/') if embed_url else ''
	for stream in jsdata.get('published_urls', None):
		if stream.get('format', None) == 'dash':
			embed_url = stream.get('embed_url', None)
			
			license_url = stream.get('license_url', None)
			
		#	xbmc.log('license_urllicense_urllicense_urllicense_urllicense_urllicense_url:  %s '%(stream.get('license_url', None)), level=xbmc.LOGINFO)
		#else:
		#	xbmc.log('embed_urlembed_urlembed_urlembed_urlembed_url%s '%(stream.get('embed_url', None)), level=xbmc.LOGINFO)

	

	if license_url:
		response = requests.get(embed_url, headers=headers, verify=False).text
		locat = re.findall('ocation>(.+?)<',response,re.DOTALL)[0]
		#xbmc.log('locatlocatlocatlocatlocatlocat:   %s '%(locat), level=xbmc.LOGINFO)
		
	
		LICKEY = True
	
		PROTOCOL = 'mpd'
		DRM = 'com.widevine.alpha'
	
	
		proxyport = addon.getSetting('proxyport')
		stream ='http://127.0.0.1:%s/manifest='%(str(proxyport))+locat 
		
		
		is_helper = inputstreamhelper.Helper(PROTOCOL, drm=DRM)
		if is_helper.check_inputstream():
			play_item = xbmcgui.ListItem(path=stream)
	
	
			play_item.setMimeType('application/xml+dash')
	
			if sys.version_info[0] > 2:
				play_item.setProperty('inputstream', is_helper.inputstream_addon)
			else:
				play_item.setProperty('inputstreamaddon', is_helper.inputstream_addon)
			play_item.setProperty("IsPlayable", "true")
	
			play_item.setProperty('inputstream.adaptive.manifest_type', PROTOCOL)
			play_item.setProperty('inputstream.adaptive.license_type', DRM)
			play_item.setProperty('inputstream.adaptive.license_key', license_url+'|Content-Type=|R{SSM}|')
		
		
		
			play_item.setProperty('inputstream.adaptive.manifest_update_parameter', 'full')		
			play_item.setContentLookup(False)	
			play_item.setProperty('inputstream.adaptive.license_flags', "persistent_storage")
	
			xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item) 
	else:
		PROTOCOL = 'mpd'
		typt = 'application/xml+dash'
		headers = {

			'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36',

			'accept-language': 'en-US,en;q=0.9',
		}

		response = requests.get(embed_url, headers=headers, verify=False).json()
		stream_url = response.get("master_m3u8", None)
		
		if 'master.m3u8' in stream_url:
			PROTOCOL = 'hls'
			typt = 'application/vnd.apple.mpegurl'
		
		play_item = xbmcgui.ListItem(path=stream_url )
		if sys.version_info[0] > 2:
			play_item.setProperty('inputstream', 'inputstream.adaptive')
		else:
			play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
		play_item.setProperty('inputstream.adaptive.manifest_type', PROTOCOL)
		play_item.setMimeType(typt)

		xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item) 
def PLchar(char):
	if type(char) is not str:
		char=char.encode('utf-8')
	char = char.replace('\\u0105','\xc4\x85').replace('\\u0104','\xc4\x84')
	char = char.replace('\\u0107','\xc4\x87').replace('\\u0106','\xc4\x86')
	char = char.replace('\\u0119','\xc4\x99').replace('\\u0118','\xc4\x98')
	char = char.replace('\\u0142','\xc5\x82').replace('\\u0141','\xc5\x81')
	char = char.replace('\\u0144','\xc5\x84').replace('\\u0144','\xc5\x83')
	char = char.replace('\\u00f3','\xc3\xb3').replace('\\u00d3','\xc3\x93')
	char = char.replace('\\u015b','\xc5\x9b').replace('\\u015a','\xc5\x9a')
	char = char.replace('\\u017a','\xc5\xba').replace('\\u0179','\xc5\xb9')
	char = char.replace('\\u017c','\xc5\xbc').replace('\\u017b','\xc5\xbb')
	char = char.replace('&#8217;',"'")
	char = char.replace('&#8211;',"-")	
	char = char.replace('&#8230;',"...")	
	char = char.replace('&#8222;','"').replace('&#8221;','"')	
	char = char.replace('[&hellip;]',"...")
	char = char.replace('&#038;',"&").replace('&#38;',"&")
	char = char.replace('&#039;',"'").replace('&#39;',"'")
	char = char.replace('&quot;','"').replace('&oacute;','ó').replace('&rsquo;',"'")
	char = char.replace('&nbsp;',".").replace('&amp;','&').replace('&eacute;','e')
	return char	
def PLcharx(char):
	char=char.replace("\xb9","ą").replace("\xa5","Ą").replace("\xe6","ć").replace("\xc6","Ć")
	char=char.replace("\xea","ę").replace("\xca","Ę").replace("\xb3","ł").replace("\xa3","Ł")
	char=char.replace("\xf3","ó").replace("\xd3","Ó").replace("\x9c","ś").replace("\x8c","Ś")
	char=char.replace("\x9f","ź").replace("\xaf","Ż").replace("\xbf","ż").replace("\xac","Ź")
	char=char.replace("\xf1","ń").replace("\xd1","Ń").replace("\x8f","Ź");
	return char	
	
	
def router(paramstring):
	params = dict(urllib_parse.parse_qsl(paramstring))
	if params:	
		mode = params.get('mode', None)


		if mode == 'playvid':
			PlayVid(exlink)	

			
		elif mode == 'listkanaly':
			ListKanaly()

			
		elif mode == 'playapple':
			playapple()
			
			
		elif mode =="listkateg":
			ListKateg(exlink)
			
		elif mode =="playvid":
			PlayVid(exlink)
			
		elif mode =="listvodmenu":
			ListVodMenu(exlink, lid)	
			
		elif mode =="listvod":
			ListVod(exlink)	
			
		elif mode =="getseries":
			getSeries(exlink)	
			
		elif mode =="getepisodes":
			getEpisodes	(exlink)	
			
	else:
		home()
		xbmcplugin.endOfDirectory(addon_handle)	
if __name__ == '__main__':
	router(sys.argv[2][1:])