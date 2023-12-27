# -*- coding: utf-8 -*-
               
#Credit to JewBMX for base code


import os
import pkgutil

from resources.lib.modules import log_utils

__all__ = [x[1] for x in os.walk(os.path.dirname(__file__))][0]


def sources():
    sourceDict = []
    for i in __all__:
        for loader, module_name, is_pkg in pkgutil.walk_packages([os.path.join(os.path.dirname(__file__), i)]):
            if is_pkg:
                continue
            try:
                module = loader.find_module(module_name).load_module(module_name)
                sourceDict.append((module_name, module.source()))
            except Exception as e:
                log_utils.log('Provider loading Error - "%s" : %s' % (module_name, e), 1)
    return sourceDict


### Dev Shit Saved.


# if not url: return
# if url == None: return sources


# link = "https:" + link if link.startswith('//') else link


# url = url.replace('//sexhd.co/', '//fembed.com/') if '//sexhd.co/' in url else url
# url = url.replace('/f/', '/v/') if '//fembed.com/' in url or '//sexhd.co/' in url else url


# if url in str(sources): continue
# if host in str(sources): continue


# results_limit = 30
# if results_limit < 1: continue
# else: results_limit -= 1

#def request(url, close=True, redirect=True, error=False, verify=True, post=None, headers=None, mobile=False, XHR=False,
#            limit=None, referer=None, cookie=None, compression=False, output='', timeout='10', as_bytes=False):
# from resources.lib.modules import client
# url = client.request(url, timeout='10', output='geturl')
# self.cookie = client.request(self.base_link, output='cookie', timeout='5')
# html = client.request(url, cookie=self.cookie)
# html = client.request(url, timeout='6')
# html = client.scrapePage(url).text


# from resources.lib.modules import cleantitle
# cleantitle.geturl(title)
# cleantitle.get_under(title)
# cleantitle.get_dash(title)
# cleantitle.get_plus(title)
# cleantitle.get_utf8(title)


# from resources.lib.modules import source_utils
# return source_utils.strip_domain(url)
# valid, host = source_utils.checkHost(url, hostDict)
# valid, host = source_utils.is_host_valid(host, hostDict)
# quality, info = source_utils.get_release_quality(link, info)


#from resources.lib.modules import scrape_sources
#for source in scrape_sources.process(hostDict, link, host=None, info=None): sources.append(source)
#scrape_sources.rescrape(url, regex=None)
#scrape_sources.prepare_link(url)


#except Exception:

#log_utils.log('Scraper Testing starting url: \n' + str(url))
#log_utils.log('Scraper Testing starting url: \n' + repr(url))
#log_utils.log('def', 1)


# SAVED to be stored in module for example use.
# if not source_utils.is_anime('show', 'tvdb', tvdb): return


