# -*- coding: utf-8 -*-
from kodi_six import xbmcgui
import six
try:
    from YDStreamExtractor import getVideoInfo
    from YDStreamExtractor import handleDownload
except Exception:
    xbmcgui.Dialog().notification("LiveStreamsPro", "Please [COLOR yellow]install Youtube-dl[/COLOR] module", "", 10000, False)


def single_YD(url, download=False, dl_info=False, audio=False):
    if dl_info:
        handleDownload(dl_info, bg=True)
        return
    else:
        info = getVideoInfo(url, quality=3, resolve_redirects=True)
    if info is None:
        print('Fail to extract')
        return None
    elif info and download:
        if audio:
            try:
                for s in info.streams():
                    for i in range(len(s['ytdl_format']['formats'])):
                        if s['ytdl_format']['formats'][i]['format_id'] == '140':
                            if six.PY2:
                                audio_url = s['ytdl_format']['formats'][i]['url'].encode('utf-8', 'ignore')
                                title = s['title'].encode('utf-8', 'ignore')
                            else:
                                audio_url = s['ytdl_format']['formats'][i]['url']
                                title = s['title']
                            info = {'url': audio_url, 'title': title, 'media_type': 'audio'}
                            break
            except Exception:
                return

        handleDownload(info, bg=True)
    else:
        for s in info.streams():
            try:
                stream_url = s['xbmc_url'].encode('utf-8', 'ignore') if six.PY2 else s['xbmc_url']
                return stream_url
            except Exception:
                return None
