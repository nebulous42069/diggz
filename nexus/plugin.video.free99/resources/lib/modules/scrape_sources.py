# -*- coding: utf-8 -*-
            
#Credit to JewBMX for base code

import re
import requests

import simplejson as json
from six.moves.urllib_parse import urlencode

from resources.lib.modules import client
from resources.lib.modules import client_utils
from resources.lib.modules import source_utils



gdriveplayer_domains = ['database.gdriveplayer.us', 'databasegdriveplayer.co', 'series.databasegdriveplayer.co']
gomo_domains = ['playerhost.net', 'gomo.to', 'gomostream.com', 'gomoplayer.com']
linkbin_domains = ['linkbin.me']
ronemo_domains = ['ronemo.com']
source_stream_domains = ['goodstream.uno', 'krakenfiles.com', 'youdboox.com']
superembed_domains = ['streamembed.net']
twoembed_domains = ['2embed.ru', '2embed.to']
vidembed_domains = ['vidcloud9.com', 'vidnode.net', 'vidnext.net', 'vidembed.net', 'vidembed.cc', 'vidembed.io',
    'vidembed.me', 'membed.net', 'membed.co', 'membed1.com', 'goload.pro', 'goload.io', 'anihdplay.com'
]
vidlink_domains = ['vidlink.org']
voxzer_domains = ['voxzer.org']


"""Example...

from resources.lib.modules import scrape_sources

for source in scrape_sources.process(hostDict, link, host=None, info=None):
    sources.append(source)

scrape_sources.rescrape(url, regex=None)

scrape_sources.prepare_link(url)
if not link: continue

"""


def prepare_link(url):  # Retard Reminder: dont forget to "unfold" the lines in this def when your done fool.
    if not url:
        return
    url = "https:" + url if url.startswith('//') else url
    if not url.startswith('http'):
        try:
            url = re.sub('\s+', '', url)
        except:  # Forgot which one works best, but both fix the issue. (Seen a few random source urls that started with a tab.)
            url = "{}".format(re.sub('\s+', '', url))
        if not url.startswith('http'):
            #log_utils.log('scrape_sources> prepare_link> non-url? link: ' + str(url))
            return
    if '//2embed.ru/' in url:
        url = url.replace('2embed.ru', '2embed.to')
    if '//aparat.cam/' in url:
        url = url.replace('aparat.cam', 'wolfstream.tv')
    if '//clicknupload.club/' in url:
        url = url.replace('clicknupload.club', 'clicknupload.to')
    if '//clicknupload.org/' in url:
        url = url.replace('clicknupload.org', 'clicknupload.to')
    if '//cloudvid.co/' in url:
        url = url.replace('cloudvid.co', 'cloudvideo.tv')
    if '//dood.cx/' in url:
        url = url.replace('dood.cx', 'doodstream.com')
    if '//dood.pm/' in url:
        url = url.replace('dood.pm', 'doodstream.com')
    if '//dood.so/' in url:
        url = url.replace('dood.so', 'doodstream.com')
    if '//dood.to/' in url:
        url = url.replace('dood.to', 'doodstream.com')
    if '//dood.wf/' in url:
        url = url.replace('dood.wf', 'doodstream.com')
    if '//eplayvid.com/' in url:
        url = url.replace('eplayvid.com', 'eplayvid.net')
    if '//fembed.com/' in url:
        url = url.replace('fembed.com', 'vanfem.com')
    if '//gomoplayer.com/' in url:
        url = url.replace('gomoplayer.com', 'xvideosharing.com') # Dud Fix, needs a good link to test still.
    if '//gomostream.com/' in url:
        url = url.replace('gomostream.com', 'gomo.to')
    if '//mediashore.org/' in url:
        url = url.replace('mediashore.org', 'vanfem.com')
    if '//membed.net/' in url:
        url = url.replace('membed.net', 'membed1.com')
    if '//sendit.cloud/' in url:
        url = url.replace('sendit.cloud', 'send.cm')
    if '//streamsss.net/' in url:
        url = url.replace('streamsss.net', 'sbplay2.xyz')
    if '//vidcloud9.com/' in url:
        url = url.replace('vidcloud9.com', 'membed1.com')
    if '//vidcloud.icu/' in url:
        url = url.replace('vidcloud.icu', 'membed1.com')
    if '//vidembed.cc/' in url:
        url = url.replace('vidembed.cc', 'membed1.com')
    if '//vidembed.io/' in url:
        url = url.replace('vidembed.io', 'membed1.com')
    if '//vidembed.me/' in url:
        url = url.replace('vidembed.me', 'membed1.com')
    if '//vidnext.net/' in url:
        url = url.replace('vidnext.net', 'membed1.com')
    if '//vidoza.net/' in url:
        url = url.replace('vidoza.net', 'vidoza.co')
    if '//vidcloud.co/embed/' in url:
        url = url.replace('/embed/', '/v/')  # Ghetto fix to get the resolver pattern to notice the url
    #log_utils.log('scrape_sources - prepare_link link: ' + str(url))
    # this log line should log atleast 90% of the source links when used. altho its gonna have dupes and links from before and after various process steps.
    return url


def rescrape(url, regex=None): # unused old code saved.
    try:
        html = client.scrapePage(url).text
        if regex:
            link = re.findall(regex, html)[0]
        else:
            link = re.findall(r'(?:file|source)(?:\:)\s*(?:\"|\')(.+?)(?:\"|\')', html)[0]
        return link
    except:
        #log_utils.log('rescrape', 1)
        return url


def process(hostDict, link, host=None, info=None):
    sources = []
    try:
        if not link:
            return sources
        link = prepare_link(link)
        host = link if host == None else host
        info = link if info == None else info
        #if 'google' in link:
            #link = googlestream.googlepass(link)
        if any(i in host for i in gdriveplayer_domains):
            for source in gdriveplayer(link, hostDict, info=info):
                sources.append(source)
        elif any(i in host for i in gomo_domains):
            for source in gomo(link, hostDict, info=info):
                sources.append(source)
        elif any(i in host for i in linkbin_domains):
            for source in linkbin(link, hostDict, info=info):
                sources.append(source)
        elif any(i in host for i in ronemo_domains):
            for source in ronemo(link, hostDict, info=info):
                sources.append(source)
        elif any(i in host for i in source_stream_domains):
            for source in source_stream(link, hostDict, info=info):
                sources.append(source)
        elif any(i in host for i in superembed_domains):
            for source in superembed(link, hostDict, info=info):
                sources.append(source)
        elif any(i in host for i in twoembed_domains):
            for source in twoembed(link, hostDict, info=info):
                sources.append(source)
        elif any(i in host for i in vidembed_domains):
            for source in vidembed(link, hostDict, info=info):
                sources.append(source)
        elif any(i in host for i in vidlink_domains):
            for source in vidlink(link, hostDict, info=info):
                sources.append(source)
        elif any(i in host for i in voxzer_domains):
            for source in voxzer(link, hostDict, info=info):
                sources.append(source)
        else:
            valid, host = source_utils.is_host_valid(host, hostDict)
            if valid:
                quality, info = source_utils.get_release_quality(link, info)
                sources.append({'source': host, 'quality': quality, 'info': info, 'url': link, 'direct': False})
            #else: log_utils.log('scrape_sources - process - non-valid link: ' + str(link))
        return sources
    except Exception:
        #log_utils.log('process', 1)
        return sources


def linkbin(link, hostDict, info=None):
    sources = []
    try:
        return sources  # Blocked since the sites seems to be dead for me lol.
        html = client.scrapePage(link).text
        results = client_utils.parseDOM(html, 'li', attrs={'class': 'signle-link'})
        results = [(client_utils.parseDOM(i, 'a', ret='href'), client_utils.parseDOM(i, 'a')) for i in results]
        results = [(i[0][0], i[1][0]) for i in results if len(i[0]) > 0 and len(i[1]) > 0]
        for result in results:
            try:
                url = prepare_link(result[0])
                if info:
                    info += result[1]
                else:
                    info = result[1]
                valid, host = source_utils.is_host_valid(url, hostDict)
                if valid:
                    quality, info = source_utils.get_release_quality(url, info)
                    sources.append({'source': host, 'quality': quality, 'info': info, 'url': url, 'direct': False})
                #else: log_utils.log('scrape_sources - linkbin - non-valid link: ' + str(url))
            except:
                #log_utils.log('linkbin', 1)
                pass
        return sources
    except Exception:
        #log_utils.log('linkbin', 1)
        return sources


def gomo(link, hostDict, info=None):
    sources = []
    try:
        domain = re.findall('(?://|\.)(playerhost\.net|gomo\.to|gomostream\.com|gomoplayer\.com)/', link)[0]
        gomo_link = 'https://%s/decoding_v3.php' % domain
        result = client.request(link, timeout='5')
        tc = re.compile('tc = \'(.+?)\';').findall(result)[0]
        if (tc):
            token = re.compile('"_token": "(.+?)",').findall(result)[0]
            post = {'tokenCode': tc, '_token': token}
            def tsd(tokenCode):
                _13x48X = tokenCode
                _71Wxx199 = _13x48X[4:18][::-1]
                return _71Wxx199 + "18" + "432782"
            headers = {'Host': domain, 'Referer': link, 'User-Agent': client.UserAgent, 'x-token': tsd(tc)}
            urls = client.request(gomo_link, XHR=True, post=post, headers=headers, output='json', timeout='5')
            for url in urls:
                if not url:
                    continue
                url = prepare_link(url)
                headers = {'User-Agent': client.UserAgent, 'Referer': url}
                if 'gomo.to' in url or 'playerhost.net' in url:
                    url = client.request(url, headers=headers, output='geturl', timeout='5')
                    if not url:
                        continue
                    url = prepare_link(url)
                    if url == 'http://ww1.gomoplayer.com/':
                        continue
                    if any(i in url for i in ['database.gdriveplayer.us', 'databasegdriveplayer.co', 'series.databasegdriveplayer.co']):
                        for source in gdriveplayer(url, hostDict):
                            sources.append(source)
                    else:
                        valid, host = source_utils.checkHost(url, hostDict)
                        if valid:
                            quality, info = source_utils.get_release_quality(url, info)
                            sources.append({'source': host, 'quality': quality, 'url': url, 'info': info, 'direct': False})
                        #else: log_utils.log('scrape_sources - gomo - non-valid link1: ' + str(url))
                        #sources.append({'source': 'gomo', 'quality': 'SD', 'url': url, 'direct': True})
                else:
                    valid, host = source_utils.checkHost(url, hostDict)
                    if valid:
                        quality, info = source_utils.get_release_quality(url, info)
                        sources.append({'source': host, 'quality': quality, 'url': url, 'info': info, 'direct': False})
                    #else: log_utils.log('scrape_sources - gomo - non-valid link2: ' + str(url))
        return sources
    except Exception:
        #log_utils.log('gomo', 1)
        return sources


def gdriveplayer(link, hostDict, info=None):
    sources = []
    try:
        return sources  # Blocked since the sites seems to be dead for me lol.
        html = client.scrapePage(link).text
        servers = client_utils.parseDOM(html, 'ul', attrs={'class': 'list-server-items'})[0]
        urls = client_utils.parseDOM(servers, 'a', ret='href')
        for url in urls:
            try:
                if not url or url.startswith('/player.php'):
                    continue
                url = prepare_link(url)
                valid, host = source_utils.is_host_valid(url, hostDict)
                if valid:
                    quality, info = source_utils.get_release_quality(url, info)
                    sources.append({'source': host, 'quality': quality, 'info': info, 'url': url, 'direct': False})
                #else: log_utils.log('scrape_sources - gdriveplayer - non-valid link: ' + str(url))
            except:
                pass
        return sources
    except Exception:
        #log_utils.log('gdriveplayer', 1)
        return sources


def vidembed(link, hostDict, info=None):
    sources = []
    try:
        try:
            html = client.scrapePage(link).text
            urls = client_utils.parseDOM(html, 'li', ret='data-video')
            if urls:
                for url in urls:
                    try:
                        if not url:
                            continue
                        url = prepare_link(url)
                        valid, host = source_utils.is_host_valid(url, hostDict)
                        if valid:
                            quality, info = source_utils.get_release_quality(url, info)
                            sources.append({'source': host, 'quality': quality, 'info': info, 'url': url, 'direct': False})
                        #else: log_utils.log('scrape_sources - vidembed - non-valid link1: ' + str(url))
                    except:
                        pass
        except:
            pass
        valid, host = source_utils.is_host_valid(link, hostDict)
        if valid:
            quality, info = source_utils.get_release_quality(link, info)
            sources.append({'source': host, 'quality': quality, 'info': info, 'url': link, 'direct': False})
        #else: log_utils.log('scrape_sources - vidembed - non-valid link2: ' + str(link))
        return sources
    except Exception:
        #log_utils.log('vidembed', 1)
        return sources


def vidlink(link, hostDict, info=None):
    sources = []
    try:
        return sources # site for update_views bit needs cfscrape so the links are trash.
        # return sources is added to cock block the urls from being seen lol.
        postID = link.split('/embed/')[1]
        post_link = 'https://vidlink.org/embed/update_views'
        headers = {'User-Agent': client.UserAgent, 'Referer': link}
        ihtml = client.request(post_link, post={'postID': postID}, headers=headers, XHR=True)
        #log_utils.log('Scraper Testing ihtml: \n' + repr(ihtml))
        if ihtml:
            linkcode = client_utils.unpacked(ihtml)
            linkcode = linkcode.replace('\\', '')
            links = re.findall(r'var file1="(.+?)"', linkcode)[0]
            stream_link = links.split('/pl/')[0]
            headers = {'Referer': 'https://vidlink.org/', 'User-Agent': client.UserAgent}
            response = client.request(links, headers=headers)
            urls = re.findall(r'[A-Z]{10}=\d+x(\d+)\W[A-Z]+=\"\w+\"\s+\/(.+?)\.', response)
            if urls:
                for qual, url in urls:
                    url = stream_link + '/' + url + '.m3u8'
                    qual = qual + ' ' + info if not info == None else qual
                    #log_utils.log('scrape_sources - process vidlink link: ' + str(url))
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        quality, info = source_utils.get_release_quality(qual, url)
                        sources.append({'source': host, 'quality': quality, 'info': info, 'url': url, 'direct': False})
                    #else: log_utils.log('scrape_sources - vidlink - non-valid link: ' + str(url))
        return sources
    except Exception:
        #log_utils.log('vidlink', 1)
        return sources


def get_recaptcha():
    response = requests.get(
        "https://recaptcha.harp.workers.dev/?anchor=https%3A%2F%2Fwww.google.com%2Frecaptcha%2Fapi2%2Fanchor%3Far%3D1%26k%3D6Lf2aYsgAAAAAFvU3-ybajmezOYy87U4fcEpWS4C%26co%3DaHR0cHM6Ly93d3cuMmVtYmVkLnRvOjQ0Mw..%26hl%3Den%26v%3DPRMRaAwB3KlylGQR57Dyk-pF%26size%3Dinvisible%26cb%3D7rsdercrealf&reload=https%3A%2F%2Fwww.google.com%2Frecaptcha%2Fapi2%2Freload%3Fk%3D6Lf2aYsgAAAAAFvU3-ybajmezOYy87U4fcEpWS4C"
    )
    return response.json()["rresp"]


def twoembed(link, hostDict, info=None):
    sources = []
    try:
        return sources # Seems to be broken again or something.
        token = get_recaptcha()
        headers = {'User-Agent': client.UserAgent, 'Referer': 'https://www.2embed.to/'}
        r = requests.get(link, headers=headers).text
        items = client_utils.parseDOM(r, 'a', ret='data-id')
        for item in items:
            try:
                stream = requests.get("https://www.2embed.to/ajax/embed/play", params={"id": item, "_token": token}, headers=headers).json()
                url = stream['link']
                if 'vidcloud.pro' in url:
                    r = client.request(url, headers={'User-Agent': client.UserAgent, 'Referer': url})
                    r = re.findall('sources = \[{"file":"(.+?)","type"', r)[0]
                    url = r.replace('\\', '')
                url = prepare_link(url)
                valid, host = source_utils.is_host_valid(url, hostDict)
                if valid:
                    quality, info = source_utils.get_release_quality(url, info)
                    sources.append({'source': host, 'quality': quality, 'info': info, 'url': url, 'direct': False})
                #else: log_utils.log('scrape_sources - twoembed - non-valid link: ' + str(url))
            except:
                #log_utils.log('twoembed', 1)
                pass
        return sources
    except Exception:
        #log_utils.log('twoembed', 1)
        return sources


def superembed(link, hostDict, info=None):
    sources = []
    try:
        return sources # Not done looking into or coding.
        r = client.scrapePage(link).text
        i = client_utils.parseDOM(r, 'iframe', ret='src')[0]
        p = re.findall(r'''window.atob\('(.+?)'\)''', i)[0]
        link = base64.b64decode(p)
        link = ensure_text(link, errors='ignore')
        url = link.replace('\/', '/').replace('///', '//')
        valid, host = source_utils.is_host_valid(url, hostDict)
        if valid:
            quality, info = source_utils.get_release_quality(url, info)
            sources.append({'source': host, 'quality': quality, 'info': info, 'url': url, 'direct': False})
        #else: log_utils.log('scrape_sources - superembed - non-valid link: ' + str(url))
        return sources
    except Exception:
        #log_utils.log('superembed', 1)
        return sources


def ronemo(link, hostDict, info=None):
    sources = []
    try:
        html = client.scrapePage(link).text
        url = re.findall('"link":"(.+?)",', html)[0]
        valid, host = source_utils.is_host_valid(url, hostDict)
        quality, info = source_utils.get_release_quality(url, info)
        url += '|%s' % urlencode({'Referer': link})
        sources.append({'source': host, 'quality': quality, 'info': info, 'url': url, 'direct': True})
        return sources
    except Exception:
        #log_utils.log('ronemo', 1)
        return sources


def voxzer(link, hostDict, info=None):
    sources = []
    try:
        link = link.replace('/view/', '/list/')
        html = client.scrapePage(link).json()
        url = html['link']
        valid, host = source_utils.is_host_valid(url, hostDict)
        quality, info = source_utils.get_release_quality(url, info)
        url += '|%s' % urlencode({'Referer': link})
        sources.append({'source': host, 'quality': quality, 'info': info, 'url': url, 'direct': True})
        return sources
    except Exception:
        #log_utils.log('voxzer', 1)
        return sources


def source_stream(link, hostDict, info=None):
    sources = []
    try:
        html = client.scrapePage(link).text
        url = client_utils.parseDOM(html, 'source', ret='src')[0]
        valid, host = source_utils.is_host_valid(url, hostDict)
        quality, info = source_utils.get_release_quality(url, info)
        url += '|%s' % urlencode({'Referer': link})
        sources.append({'source': host, 'quality': quality, 'info': info, 'url': url, 'direct': True})
        return sources
    except Exception:
        #log_utils.log('source_stream', 1)
        return sources


def odnoklassniki(url):
    try:
        if '/safe.php?link=' in url:
            url = url.split('/safe.php?link=')[1]
        url = "https:" + url if url.startswith('//') else url
        #log_utils.log('scrape_sources - odnoklassniki - starting url: ' + str(url))
        media_id = re.compile('//.+?/.+?/([\w]+)').findall(url)[0]
        #log_utils.log('scrape_sources - odnoklassniki - media_id: ' + str(media_id))
        result = client.request('http://ok.ru/dk', post={'cmd': 'videoPlayerMetadata', 'mid': media_id})
        result = re.sub(r'[^\x00-\x7F]+', ' ', result)
        result = json.loads(result).get('videos', [])
        #log_utils.log('scrape_sources - odnoklassniki - result: ' + str(result))
        hd = []
        for name, quali in {'ultra': '4K', 'quad': '1440p', 'full': '1080p', 'hd': 'HD'}.items():
            hd += [{'quality': quali, 'url': i.get('url')} for i in result if i.get('name').lower() == name]
        #log_utils.log('scrape_sources - odnoklassniki - hd: ' + str(hd))
        sd = []
        for name, quali in {'sd': 'SD', 'low': 'SD', 'lowest': 'SD', 'mobile': 'SD'}.items():
            sd += [{'quality': quali, 'url': i.get('url')} for i in result if i.get('name').lower() == name]
        #log_utils.log('scrape_sources - odnoklassniki - sd: ' + str(sd))
        url = hd + sd[:1]
        #log_utils.log('scrape_sources - odnoklassniki - final url: ' + str(url))
        if not url == []:
            return url
    except:
        #log_utils.log('odnoklassniki', 1)
        return url


