# -*- coding: utf-8 -*-
               
#Credit to JewBMX for base code

from six.moves.urllib_parse import parse_qs, urlencode

from resources.lib.modules import client
from resources.lib.modules import client_utils
from resources.lib.modules import cleantitle
from resources.lib.modules import scrape_sources



class source:
    def __init__(self):
        self.results = []
        self.domains = ['couchtuner.show']
        self.base_link = 'https://www.couchtuner.show'
        self.search_link = '/?s=%s'


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        url = {'imdb': imdb, 'tvshowtitle': tvshowtitle, 'year': year}
        url = urlencode(url)
        return url


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        if not url:
            return
        url = parse_qs(url)
        url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
        url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
        url = urlencode(url)
        return url


    def sources(self, url, hostDict):
        try:
            if url == None:
                return self.results
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle']
            season = data['season']
            episode = data['episode']
            search = '%s Season %s' % (title, season)
            search = cleantitle.get_plus(search)
            search2 = '%s Season %s Episode %s' % (title, season, episode)
            search2 = cleantitle.get_plus(search2)
            search_url = self.base_link + self.search_link % search
            r = client.scrapePage(search_url).text
            r = client_utils.parseDOM(r, 'div', attrs={'class': 'movie-content'})
            r = [(client_utils.parseDOM(i, 'a', ret='href'), client_utils.parseDOM(i, 'a')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            try:
                url = [i[0] for i in r if search == cleantitle.get_plus(i[1])][0]
            except:
                url = [i[0] for i in r if cleantitle.get_plus(title) == cleantitle.get_plus(i[1])][0]
            r = client.scrapePage(url).text
            r = r.replace('\r', '').replace('\n', '').replace('\t', '').replace('  ', '').replace('<i class="fas fa-play"></i>', '')
            r = client_utils.parseDOM(r, 'div', attrs={'class': 'episode-watch-wrap'})
            r = client_utils.parseDOM(r, 'li')
            r = [(client_utils.parseDOM(i, 'a', ret='href'), client_utils.parseDOM(i, 'a')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            url = [i[0] for i in r if search2 == cleantitle.get_plus(i[1])][0]
            r = client.scrapePage(url).text
            try:
                linked = client_utils.parseDOM(r, 'a', attrs={'rel': 'bookmark'}, ret='href')[0]
                if linked:
                    r += client.scrapePage(linked).text
            except:
                pass
            links = client_utils.parseDOM(r, 'iframe', ret='src')
            for link in links:
                for source in scrape_sources.process(hostDict, link):
                    self.results.append(source)
            return self.results
        except:
            #log_utils.log('sources', 1)
            return self.results


    def resolve(self, url):
        return url


