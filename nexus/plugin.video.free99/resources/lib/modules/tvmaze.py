# -*- coding: utf-8 -*-
               
#Credit to JewBMX for base code

import simplejson as json
from six.moves import urllib_parse

from resources.lib.modules import client



class tvMaze:
    def __init__(self, show_id=None):
        self.api_url = 'https://api.tvmaze.com/%s%s'
        self.show_id = show_id


    def showID(self, show_id=None):
        if (show_id != None):
            self.show_id = show_id
            return show_id
        return self.show_id


    def request(self, endpoint, query=None):
        try:
            if (query != None):
                query = '?' + urllib_parse.urlencode(query)
            else:
                query = ''
            request_url = self.api_url % (endpoint, query)
            response = client.scrapePage(request_url, timeout='30')
            return response.json()
        except:
            #log_utils.log('request', 1)
            pass
        return {}


    def showLookup(self, type, id):
        try:
            result = self.request('lookup/shows', {type: id})
            if ('id' in result):
                self.show_id = result['id']
            return result
        except:
            #log_utils.log('showLookup', 1)
            pass
        return {}


    def shows(self, show_id=None, embed=None):
        try:
            if (not self.showID(show_id)):
                raise Exception()
            result = self.request('shows/%d' % self.show_id)
            if ('id' in result):
                self.show_id = result['id']
            return result
        except:
            #log_utils.log('shows', 1)
            pass
        return {}


    def showSeasons(self, show_id=None):
        try:
            if (not self.showID(show_id)):
                raise Exception()
            result = self.request('shows/%d/seasons' % int(self.show_id))
            if (len(result) > 0 and 'id' in result[0]):
                return result
        except:
            #log_utils.log('showSeasons', 1)
            pass
        return []


    def showEpisodeList(self, show_id=None, specials=False):
        try:
            if (not self.showID(show_id)):
                raise Exception()
            result = self.request('shows/%d/episodes' % int(self.show_id), 'specials=1' if specials else '')
            if (len(result) > 0 and 'id' in result[0]):
                return result
        except:
            #log_utils.log('showEpisodeList', 1)
            pass
        return []


