# -*- coding: utf-8 -*-
               
#Credit to JewBMX for base code

import re

from kodi_six import xbmc
import six
from six.moves import urllib_parse

from resources.lib.modules import client
from resources.lib.modules import client_utils
from resources.lib.modules import trakt


RES_8K = ['hd8k', '8khd', '4320p', '4320i', 'hd4320', '4320hd', '5120p', '5120i', 'hd5120', '5120hd', '8192p', '8192i', 'hd8192', '8192hd']
RES_6K = ['hd6k', '6khd', '3160p', '3160i', 'hd3160', '3160hd', '4096p', '4096i', 'hd4096', '4096hd']
RES_4K = ['hd4k', '4khd', 'uhd', 'ultrahd', 'ultra hd', 'ultra high', '2160p', '2160i', 'hd2160', '2160hd', '1716p', '1716i', 'hd1716', '1716hd', '2664p', '2664i', 'hd2664', '2664hd', '3112p', '3112i', 'hd3112', '3112hd', '2880p', '2880i', 'hd2880', '2880hd']
RES_2K = ['hd2k', '2khd', '2048p', '2048i', 'hd2048', '2048hd', '1332p', '1332i', 'hd1332', '1332hd', '1556p', '1556i', 'hd1556', '1556hd']
RES_1080 = ['1080p', '1080i', 'hd1080', '1080hd', '1200p', '1200i', 'hd1200', '1200hd']
RES_720 = ['720p', '720i', 'hd720', '720hd', 'hd']
RES_SD = ['576p', '576i', 'sd576', '576sd', '480p', '480i', 'sd480', '480sd', '360p', '360i', 'sd360', '360sd', '240p', '240i', 'sd240', '240sd']
RES_SCR = ['dvdscr', 'screener', 'scr']
RES_CAM = ['camrip', 'cam rip', 'tsrip', 'ts rip', 'hdcam', 'hd cam', 'hdts', 'hd ts', 'dvdcam', 'dvd cam', 'dvdts', 'dvd ts', 'cam', 'telesync', 'tele sync', 'ts']

CODEC_H265 = ['hevc', 'h265', 'x265']
CODEC_H264 = ['avc', 'h264', 'x264']
CODEC_XVID = ['xvid']
CODEC_DIVX = ['divx', 'div2', 'div3']
CODEC_MPEG = ['mpeg', 'm4v', 'mpg', 'mpg1', 'mpg2', 'mpg3', 'mpg4', 'msmpeg', 'msmpeg4', 'mpegurl']
CODEC_MP4 = ['mp4']
CODEC_M3U = ['m3u8', 'm3u']
CODEC_AVI = ['avi']
CODEC_MKV = ['mkv', 'matroska']

AUDIO_8CH = ['ch8', '8ch', 'ch7', '7ch', '7 1', 'ch7 1', '7 1ch']
AUDIO_6CH = ['ch6', '6ch', 'ch6', '6ch', '6 1', 'ch6 1', '6 1ch', '5 1', 'ch5 1', '5 1ch']
AUDIO_2CH = ['ch2', '2ch', 'stereo', 'dualaudio', 'dual', '2 0', 'ch2 0', '2 0ch']
AUDIO_1CH = ['ch1', '1ch', 'mono', 'monoaudio', 'ch1 0', '1 0ch']

VIDEO_3D = ['3d', 'sbs', 'hsbs', 'sidebyside', 'side by side', 'stereoscopic', 'tab', 'htab', 'topandbottom', 'top and bottom']


websites = set()
def check_dupes(url):
    parsed = urllib_parse.urlparse(url)
    website = parsed.hostname + parsed.path
    if website in websites:
        return False
    websites.add(website)
    return True


def append_headers(headers):
    return '|%s' % '&'.join(['%s=%s' % (key, urllib_parse.quote_plus(headers[key])) for key in headers])


def supported_video_extensions():
    supported_video_extensions = xbmc.getSupportedMedia('video').split('|')
    return [i for i in supported_video_extensions if i != '' and i != '.zip']


def get_supported_formats():
    try:
        from resolveurl.lib import kodi
        video_formats = list(filter(None, kodi.supported_video_extensions()))
        #log_utils.log('Testing: get_supported_formats - video_formats: ' + repr(video_formats))
        return video_formats
    except:
        #log_utils.log('get_supported_formats', 1)
        return []


def is_anime(content, type, type_id):
    try:
        r = trakt.getGenre(content, type, type_id)
        return 'anime' in r or 'animation' in r
    except:
        return False


def aliases_to_array(aliases, filter=None):
    try:
        if not filter:
            filter = []
        if isinstance(filter, six.string_types):
            filter = [filter]
        return [x.get('title') for x in aliases if not filter or x.get('country') in filter]
    except:
        return []


def strip_domain(url):
    try:
        url = six.ensure_str(url)
        if url.lower().startswith('http') or url.startswith('/'):
            url = re.findall('(?://.+?|)(/.+)', url)[0]
        url = client_utils.replaceHTMLCodes(url)
        return url
    except:
        return url


def __top_domain(url):
    if not (url.startswith('//') or url.startswith('http://') or url.startswith('https://')):
        url = '//' + url
    elements = urllib_parse.urlparse(url)
    domain = elements.netloc or elements.path
    domain = domain.split('@')[-1].split(':')[0]
    regex = "(?:www\.)?([\w\-]*\.[\w\-]{2,3}(?:\.[\w\-]{2,3})?)$"
    res = re.search(regex, domain)
    if res:
        domain = res.group(1)
    domain = domain.lower()
    return domain


def is_host_valid(url, domains):
    try:
        host = __top_domain(url)
        hosts = [domain.lower() for domain in domains if host and host in domain.lower()]
        if hosts and '.' not in host:
            host = hosts[0]
        if hosts and any([h for h in ['google', 'picasa', 'blogspot'] if h in host]):
            host = 'gvideo'
        if hosts and any([h for h in ['akamaized', 'ocloud'] if h in host]):
            host = 'CDN'
        return any(hosts), host
    except:
        return False, ''


def get_host(url):
    try:
        elements = urllib_parse.urlparse(url)
        domain = elements.netloc or elements.path
        domain = domain.split('@')[-1].split(':')[0]
        res = re.search("(?:www\.)?([\w\-]*\.[\w\-]{2,3}(?:\.[\w\-]{2,3})?)$", domain)
        if res:
            domain = res.group(1)
        domain = domain.lower()
    except:
        elements = urllib_parse.urlparse(url)
        host = elements.netloc
        domain = host.replace('www.', '')
    return domain


def checkHost(url, hostList):
    host = get_host(url)
    validHost = False
    for i in hostList:
        if i.lower() in url.lower():
            host = i
            validHost = True
            return validHost, host
    return validHost, host


def get_codec(txt):
    if any(value in txt for value in CODEC_H265):
        _codec = "HEVC | "
    elif any(value in txt for value in CODEC_H264):
        _codec = "AVC | "
    elif any(value in txt for value in CODEC_MKV):
        _codec = "MKV | "
    elif any(value in txt for value in CODEC_DIVX):
        _codec = "DIVX | "
    elif any(value in txt for value in CODEC_MPEG):
        _codec = "MPEG | "
    elif any(value in txt for value in CODEC_MP4):
        _codec = "MP4 | "
    elif any(value in txt for value in CODEC_M3U):
        _codec = "M3U | "
    elif any(value in txt for value in CODEC_XVID):
        _codec = "XVID | "
    elif any(value in txt for value in CODEC_AVI):
        _codec = "AVI | "
    else:
        _codec = '0'
    return _codec


def get_audio(txt):
    if any(value in txt for value in AUDIO_8CH):
        _audio = "7.1 | "
    elif any(value in txt for value in AUDIO_6CH):
        _audio = "5.1 | "
    elif any(value in txt for value in AUDIO_2CH):
        _audio = "2.0 | "
    elif any(value in txt for value in AUDIO_1CH):
        _audio = "Mono | "
    else:
        _audio = '0'
    return _audio


def get_size(txt):
    try:
        _size = re.findall('(\d+(?:\.|/,|)?\d+(?:\s+|)(?:gb|GiB|mb|MiB|GB|MB))', txt)
        _size = _size[0].encode('utf-8')
        _size = _size + " | "
    except:
        _size = '0'
    return _size


def get_3D(txt):
    if any(value in txt for value in VIDEO_3D):
        _3D = "3D | "
    else:
        _3D = '0'
    return _3D


def get_quality(txt1, txt2=None):
    if txt2 is None:
        txt = txt1
    else:
        txt = txt1 +' '+ txt2
    if any(value in txt for value in RES_8K):
        _quality = "8K"
    elif any(value in txt for value in RES_6K):
        _quality = "6K"
    elif any(value in txt for value in RES_4K):
        _quality = "4K"
    elif any(value in txt for value in RES_2K):
        _quality = "2K"
    elif any(value in txt for value in RES_1080):
        _quality = "1080p"
    elif any(value in txt for value in RES_720):
        _quality = "720p"
    elif any(value in txt for value in RES_SD):
        _quality = "SD"
    elif any(value in txt for value in RES_SCR):
        _quality = "SCR"
    elif any(value in txt for value in RES_CAM):
        _quality = "CAM"
    else:
        _quality = "SD"
    return _quality


def get_info(txt1, txt2=None):
    if txt2 is None:
        txt = txt1
    else:
        txt = txt1 +' '+ txt2
    _codec = get_codec(txt)
    if _codec == '0' or _codec == '':
        _codec = ''
    _audio = get_audio(txt)
    if _audio == '0' or _audio == '':
        _audio = ''
    _size = get_size(txt)
    if _size == '0' or _size == '':
        _size = ''
    _3D = get_3D(txt)
    if _3D == '0' or _3D == '':
        _3D = ''			
    _info = _codec + _audio + _size + _3D
    return _info	


def cleanup(txt):
    try:
        _txt = six.ensure_str(txt)
        _txt = strip_domain(_txt)
        _txt = client_utils.replaceHTMLCodes(_txt)
        _txt = urllib_parse.unquote(_txt)
        _txt = _txt.lower()
        _txt = re.sub('[^a-z0-9 ]+', ' ', _txt)
    except:
        _txt = str(txt.lower())
    return _txt	


def cleanupALT(txt):
    try:
        _txt = six.ensure_str(txt)
        _txt = strip_domain(_txt)
        _txt = _txt.upper()
        _txt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*)(\.|\)|\]|\s)', '', _txt)
        _txt = re.split('\.|\(|\)|\[|\]|\s|-', _txt)
        _txt = [i.lower() for i in _txt]
    except:
        _txt = str(txt.lower())
    return _txt	


def get_release_quality(release_name, release_link=None):
    try:
        if release_name is None:
            return 'SD', []
        try:
            release_name = cleanup(release_name)
            if release_link:
                release_link = cleanup(release_link)
        except:
            release_name = cleanupALT(release_name)
            if release_link:
                release_link = cleanupALT(release_link)
        if release_link and release_link == release_name:
            release_link = None
        quality = get_quality(release_name, release_link)
        info = get_info(release_name, release_link)
        return quality, info
    except:
        return 'SD', []


def get_release_qualityOLD(release_name, release_link=None):
    if release_name is None:
        return
    try:
        release_name = six.ensure_str(release_name)
    except:
        pass
    try:
        quality = None
        release_name = release_name.upper()
        fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*)(\.|\)|\]|\s)', '', release_name)
        fmt = re.split('\.|\(|\)|\[|\]|\s|-', fmt)
        fmt = [i.lower() for i in fmt]
        if '4k' in fmt:
            quality = '4K'
        if '2160p' in fmt:
            quality = '4K'
        elif '1080p' in fmt:
            quality = '1080p'
        elif '720p' in fmt:
            quality = '720p'
        elif 'brrip' in fmt:
            quality = '720p'
        elif 'hd' in fmt:
            quality = '720p'
        elif 'bluray' in fmt:
            quality = '720p'
        elif 'webrip' in fmt:
            quality = '720p'
        elif '480p' in fmt:
            quality = '480p'
        elif any(i in ['dvdscr', 'r5', 'r6'] for i in fmt):
            quality = 'SCR'
        elif any(i in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in fmt):
            quality = 'CAM'
        if not quality:
            if release_link:
                release_link = release_link.lower()
                try:
                    release_link = six.ensure_str(release_link)
                    release_link = client_utils.replaceHTMLCodes(release_link)
                    release_link = urllib_parse.unquote(release_link)
                    release_link = release_link.lower()
                    release_link = re.sub('[^a-z0-9 ]+', ' ', release_link)
                except:
                    release_link = str(release_link)
                if '4k' in release_link:
                    quality = '4K'
                elif '2160p' in release_link:
                    quality = '4K'
                elif '1080p' in release_link:
                    quality = '1080p'
                elif '720p' in release_link:
                    quality = '720p'
                elif 'brrip' in release_link:
                    quality = '720p'
                elif 'hd' in release_link:
                    quality = '720p'
                elif 'bluray' in release_link:
                    quality = '720p'
                elif 'webrip' in release_link:
                    quality = '720p'
                elif '480p' in release_link:
                    quality = '480p'
                elif any(i in ['dvdscr', 'r5', 'r6'] for i in release_link):
                    quality = 'SCR'
                elif any(i in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in release_link):
                    quality = 'CAM'
                else:
                    quality = 'SD'
            else:
                quality = 'SD'
        info = []
        if '3d' in fmt:
            info.append('3D')
        if any(i in ['hevc', 'h265', 'x265'] for i in fmt):
            info.append('HEVC')
        return quality, info
    except:
        return 'SD', []


def getFileType(url):
    try:
        url = six.ensure_str(url)
        url = client_utils.replaceHTMLCodes(url)
        url = urllib_parse.unquote(url)
        url = url.lower()
        url = re.sub('[^a-z0-9 ]+', ' ', url)
    except:
        url = str(url)
    type = ''
    if 'bluray' in url:
        type += ' BLURAY /'
    if 'blu ray' in url:
        type += ' BLURAY /'
    if 'webdl' in url:
        type += ' WEBDL /'
    if 'webrip' in url:
        type += ' WEBRIP /'
    if 'hdrip' in url:
        type += ' HDRIP /'
    if 'bdrip' in url:
        type += ' BD-RIP /'
    if 'atmos' in url:
        type += ' ATMOS /'
    if 'truehd' in url:
        type += ' TRUEHD /'
    if 'uhd' in url:
        type += ' UHD /'
    if 'xvid' in url:
        type += ' XVID /'
    if 'mkv' in url:
        type += ' MKV /'
    if 'mp4' in url:
        type += ' MP4 /'
    if 'avi' in url:
        type += ' AVI /'
    if 'ac3' in url:
        type += ' AC3 /'
    if 'aac' in url:
        type += ' AAC /'
    if 'h264' in url:
        type += ' h264 /'
    if 'x264' in url:
        type += ' x264 /'
    if 'h265' in url:
        type += ' h265 /'
    if 'x265' in url:
        type += ' x265 /'
    if 'hevc' in url:
        type += ' hevc /'
    if 'sub' in url: 
        if type != '':
            type += ' - WITH SUBS'
        else:
            type = 'SUBS'
    type = type.rstrip('/')
    return type


