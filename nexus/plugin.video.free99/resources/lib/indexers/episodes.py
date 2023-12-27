# -*- coding: utf-8 -*-

#Credit to JewBMX for base code

import re
import os
import sys
import datetime

import simplejson as json
import six
from six.moves import range, urllib_parse

try:
    #from infotagger.listitem import ListItemInfoTag
    from resources.lib.modules.listitem import ListItemInfoTag
except:
    pass

from resources.lib.modules import tmdb_utils
from resources.lib.modules import trakt
from resources.lib.modules import bookmarks
from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import client_utils
from resources.lib.modules import cache
from resources.lib.modules import playcount
from resources.lib.modules import workers
from resources.lib.modules import views


params = dict(urllib_parse.parse_qsl(sys.argv[2].replace('?',''))) if len(sys.argv) > 1 else dict()
action = params.get('action')
control.moderator()
kodi_version = control.getKodiVersion()


class seasons:
    def __init__(self):
        self.list = []
        self.datetime = datetime.datetime.utcnow()
        self.today_date = self.datetime.strftime('%Y-%m-%d')
        self.addon_caching = control.setting('addon.caching') or 'true'
        self.lang = control.apiLanguage()['tmdb'] or 'en'
        self.specials = control.setting('tv.specials') or 'false'
        self.shownoyear = control.setting('show.noyear') or 'false'
        self.showunaired = control.setting('showunaired') or 'true'
        self.unairedcolor = control.setting('unaired.color')
        if self.unairedcolor == '':
            self.unairedcolor = 'darkred'
        self.tmdb_key = control.setting('tmdb.api')
        if self.tmdb_key == '' or self.tmdb_key == None:
            self.tmdb_key = 'c8b7db701bac0b26edfcc93b39858972'
        self.tmdb_link = 'https://api.themoviedb.org'
        #self.tmdb_image_link = 'https://image.tmdb.org/t/p/original'
        self.tmdb_image_link = 'https://image.tmdb.org/t/p/w%s%s'
        self.tmdb_info_link = self.tmdb_link + '/3/tv/%s?api_key=%s&language=en-US&append_to_response=credits,content_ratings,external_ids' % ('%s', self.tmdb_key)


    def tmdb_list(self, tvshowtitle, year, imdb, tmdb, meta=None, lite=False):
        try:
            tvdb = '0'
            if tmdb == '0' and not imdb == '0':
                try:
                    temp_item = tmdb_utils.find_tvshow_by_external_source(imdb=imdb)
                    tmdb = temp_item['id']
                    if not tmdb:
                        tmdb = '0'
                    else:
                        tmdb = str(tmdb)
                except:
                    #log_utils.log('tmdb_list', 1)
                    pass

            if imdb == '0' or tmdb == '0':
                try:
                    ids_from_trakt = trakt.SearchTVShow(tvshowtitle, year, full=False)[0]
                    ids_from_trakt = ids_from_trakt.get('show', '0')
                    if imdb == '0':
                        imdb = ids_from_trakt.get('ids', {}).get('imdb')
                        if not imdb:
                            imdb = '0'
                        else:
                            imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                    if tmdb == '0':
                        tmdb = ids_from_trakt.get('ids', {}).get('tmdb')
                        if not tmdb:
                            tmdb = '0'
                        else:
                            tmdb = str(tmdb)
                    if tvdb == '0':
                        tvdb = ids_from_trakt.get('ids', {}).get('tvdb')
                        if not tvdb:
                            tvdb = '0'
                        else:
                            tvdb = str(tvdb)
                except:
                    #log_utils.log('tmdb_list', 1)
                    pass
        except:
            #log_utils.log('tmdb_list', 1)
            return

        try:
            if tmdb == '0':
                raise Exception()
            seasons_url = self.tmdb_info_link % tmdb
            item = client.scrapePage(seasons_url, timeout='30').json()
            if item == None:
                raise Exception()
            
            if imdb == '0':
                try:
                    imdb = item['external_ids']['imdb_id']
                except:
                    imdb = ''
                if not imdb:
                    imdb = '0'
            if tvdb == '0':
                try:
                    tvdb = item['external_ids']['tvdb_id']
                except:
                    tvdb = ''
                if not tvdb:
                    tvdb = '0'
            
            seasons = item['seasons']
            if self.specials == 'false':
                seasons = [s for s in seasons if not s['season_number'] == 0]
            
            try:
                studio = item['networks']#[0]['name']
                studio = [x['name'] for x in studio]#[0]
            except:
                studio = []#''
            if studio == '' or studio == None or studio == []:
                studio = []#'0'
            try:
                genres = item['genres']
                genre = [d['name'] for d in genres]
                #genre = ' / '.join(genre)
            except:
                genre = []#''
            if genre == '' or genre == None or genre == []:
                genre = []#'0'
            try:
                duration = item['episode_run_time'][0]
                duration = str(duration)
            except:
                duration = ''
            if not duration:
                duration = '0'
            
            try:
                m = item['content_ratings']['results']
                mpaa = [d['rating'] for d in m if d['iso_3166_1'] == 'US'][0]
            except:
                mpaa = ''
            if not mpaa:
                mpaa = '0'
            
            try:
                status = item['status']
            except:
                status = ''
            if not status:
                status = '0'
            
            castwiththumb = []
            try:
                r_cast = item['credits']['cast'][:30]
                for person in r_cast:
                    _icon = person['profile_path']
                    #icon = self.tmdb_image_link + _icon if _icon else ''
                    icon = self.tmdb_image_link % ('185', _icon) if _icon else ''
                    castwiththumb.append({'name': person['name'], 'role': person['character'], 'thumbnail': icon})
            except:
                pass
            if not castwiththumb:
                castwiththumb = '0'
            
            try:
                show_plot = item['overview']
            except:
                show_plot = ''
            if not show_plot:
                show_plot = '0'
            else:
                show_plot = client_utils.replaceHTMLCodes(six.ensure_str(show_plot, errors='replace'))
            
            unaired = ''
            banner = clearlogo = clearart = landscape = '0'
            if meta:
                _meta = json.loads(urllib_parse.unquote_plus(meta))
                show_poster, fanart, banner, clearlogo, clearart, landscape = _meta['poster'], _meta['fanart'], _meta['banner'], _meta['clearlogo'], _meta['clearart'], _meta['landscape']
            else:
                try:
                    poster_path = item['poster_path']
                except:
                    poster_path = ''
                if poster_path:
                    #show_poster = self.tmdb_image_link + poster_path
                    show_poster = self.tmdb_image_link % ('500', poster_path)
                else:
                    show_poster = '0'
                try:
                    fanart_path = item['backdrop_path']
                except:
                    fanart_path = ''
                if fanart_path:
                    #fanart = self.tmdb_image_link + fanart_path
                    fanart = self.tmdb_image_link % ('1280', fanart_path)
                else:
                    fanart = '0'
            
        except:
            #log_utils.log('tmdb_list', 1)
            pass

        for item in seasons:
            try:
                season = str(int(item['season_number']))
                premiered = item.get('air_date', '0')
                if status == 'Ended':
                    pass
                elif not premiered or premiered == '0':
                    if self.shownoyear != 'true':
                        raise Exception()
                elif int(re.sub('[^0-9]', '', str(premiered))) > int(re.sub('[^0-9]', '', str(self.today_date))):
                    unaired = 'true'
                    if self.showunaired != 'true':
                        raise Exception()
                
                plot = item['overview']
                if plot:
                    plot = client_utils.replaceHTMLCodes(six.ensure_str(plot, errors='replace'))
                else:
                    plot = show_plot
                
                try:
                    poster_path = item['poster_path']
                except:
                    poster_path = ''
                if poster_path:
                    #poster = self.tmdb_image_link + poster_path
                    poster = self.tmdb_image_link % ('500', poster_path)
                else:
                    poster = show_poster
                
                self.list.append({'season': season, 'tvshowtitle': tvshowtitle, 'year': year, 'premiered': premiered, 'status': status, 'studio': studio, 'genre': genre, 'duration': duration, 'mpaa': mpaa, 'castwiththumb': castwiththumb,
                    'plot': plot, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'poster': poster, 'fanart': fanart, 'banner': banner,'clearlogo': clearlogo, 'clearart': clearart, 'landscape': landscape, 'unaired': unaired}
                )
            except:
                #log_utils.log('tmdb_list', 1)
                pass
        return self.list


    def get(self, tvshowtitle, year, imdb, tmdb, meta, idx=True, create_directory=True):
        try:
            if idx == True:
                if self.addon_caching == 'true':
                    self.list = cache.get(self.tmdb_list, 24, tvshowtitle, year, imdb, tmdb, meta)
                else:
                    self.list = self.tmdb_list(tvshowtitle, year, imdb, tmdb, meta)
                if create_directory == True:
                    self.seasonDirectory(self.list)
                return self.list
            else:
                self.list = self.tmdb_list(tvshowtitle, year, imdb, tmdb, lite=True)
                return self.list
        except:
            #log_utils.log('get', 1)
            pass


    def seasonDirectory(self, items):
        if items == None or len(items) == 0:
            control.idle()
            #sys.exit()
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        addonPoster = control.addonPoster()
        addonBanner = control.addonBanner()
        addonFanart = control.addonFanart()
        settingFanart = control.setting('fanart')
        traktCredentials = trakt.getTraktCredentialsInfo()
        tmdbCredentials = tmdb_utils.getTMDbCredentialsInfo()
        try:
            indicators = playcount.getSeasonIndicators(items[0]['imdb'])
        except:
            pass
        watchedMenu = 'Watched in Trakt' if trakt.getTraktIndicatorsInfo() == True else 'Watched in Free99'
        unwatchedMenu = 'Unwatched in Trakt' if trakt.getTraktIndicatorsInfo() == True else 'Unwatched in Free99'
        for i in items:
            try:
                label = 'Season %s' % i['season']
                try:
                    stats = re.findall('(\d{4})', i['premiered'])[0]
                except:
                    stats = i['premiered']
                label = '%s (%s)' % (label, stats)
                try:
                    if i['unaired'] == 'true':
                        label = '[COLOR %s][I]%s[/I][/COLOR]' % (self.unairedcolor, label)
                except:
                    pass
                systitle = sysname = urllib_parse.quote_plus(i['tvshowtitle'])
                poster = i['poster'] if 'poster' in i and not i['poster'] == '0' else addonPoster
                fanart = i['fanart'] if 'fanart' in i and not i['fanart'] == '0' else addonFanart
                banner1 = i.get('banner', '')
                banner = banner1 or fanart or addonBanner
                if 'landscape' in i and not i['landscape'] == '0':
                    landscape = i['landscape']
                else:
                    landscape = fanart
                ep_meta = {'poster': poster, 'fanart': fanart, 'banner': banner, 'clearlogo': i.get('clearlogo', '0'), 'clearart': i.get('clearart', '0'), 'landscape': landscape, 'duration': i.get('duration', '45'), 'status': i.get('status', '0')}
                sysmeta = urllib_parse.quote_plus(json.dumps(ep_meta))
                imdb, tvdb, tmdb, year, season, fanart, duration, status = i['imdb'], i['tvdb'], i['tmdb'], i['year'], i['season'], i['fanart'], i['duration'], i['status']
                meta = dict((k,v) for k, v in six.iteritems(i) if not v == '0')
                meta.update({'code': tmdb, 'imdbnumber': imdb, 'imdb_id': imdb})
                meta.update({'tvdb_id': tvdb})
                meta.update({'mediatype': 'tvshow'})
                meta.update({'trailer': '%s?action=trailer&name=%s&tmdb=%s&imdb=%s&season=%s' % (sysaddon, systitle, tmdb, imdb, season)})
                if not 'duration' in i:
                    meta.update({'duration': '60'})
                elif i['duration'] == '0':
                    meta.update({'duration': '60'})
                try:
                    meta.update({'duration': str(int(meta['duration']) * 60)})
                except:
                    pass
                try:
                    seasonYear = i['premiered']
                    seasonYear = re.findall('(\d{4})', seasonYear)[0]
                    seasonYear = six.ensure_str(seasonYear)
                    meta.update({'year': seasonYear})
                except:
                    pass
                cm = []
                cm.append(('Clean Tools Widget', 'RunPlugin(%s?action=cleantools_widget)' % sysaddon))
                cm.append(('Clear Providers', 'RunPlugin(%s?action=clear_sources)' % sysaddon))
                cm.append(('Queue Item', 'RunPlugin(%s?action=queue_item)' % sysaddon))
                if traktCredentials == True:
                    cm.append(('Trakt Manager', 'RunPlugin(%s?action=trakt_manager&name=%s&tmdb=%s&content=tvshow)' % (sysaddon, sysname, tmdb)))
                if tmdbCredentials == True:
                    cm.append(('TMDb Manager', 'RunPlugin(%s?action=tmdb_manager&name=%s&tmdb=%s&content=tvshow)' % (sysaddon, sysname, tmdb)))
                cm.append(('Add to Library', 'RunPlugin(%s?action=tvshow_to_library&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s)' % (sysaddon, systitle, year, imdb, tmdb)))
                if kodi_version < 17:
                    cm.append(('Information', 'Action(Info)'))
                try:
                    overlay = int(playcount.getSeasonOverlay(indicators, imdb, season))
                    if overlay == 7:
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=tvshows_playcount&name=%s&imdb=%s&tmdb=%s&season=%s&query=6)' % (sysaddon, systitle, imdb, tmdb, season)))
                        meta.update({'playcount': 1, 'overlay': 7})
                    else:
                        cm.append((watchedMenu, 'RunPlugin(%s?action=tvshows_playcount&name=%s&imdb=%s&tmdb=%s&season=%s&query=7)' % (sysaddon, systitle, imdb, tmdb, season)))
                        meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass
                try:
                    item = control.item(label=label, offscreen=True)
                except:
                    item = control.item(label=label)
                art = {}
                art.update({'icon': poster, 'thumb': poster, 'poster': poster, 'banner': banner, 'landscape': landscape})
                if settingFanart == 'true':
                    art.update({'fanart': fanart})
                elif not addonFanart == None:
                    art.update({'fanart': addonFanart})
                if 'clearlogo' in i and not i['clearlogo'] == '0':
                    art.update({'clearlogo': i['clearlogo']})
                if 'clearart' in i and not i['clearart'] == '0':
                    art.update({'clearart': i['clearart']})
                item.setArt(art)
                item.addContextMenuItems(cm)
                if kodi_version >= 20:
                    info_tag = ListItemInfoTag(item, 'video')
                castwiththumb = i.get('castwiththumb')
                if castwiththumb and not castwiththumb == '0':
                    if kodi_version >= 18:
                        if kodi_version >= 20:
                            info_tag.set_cast(castwiththumb)
                        else:
                            item.setCast(castwiththumb)
                    else:
                        cast = [(p['name'], p['role']) for p in castwiththumb]
                        meta.update({'cast': cast})
                if kodi_version >= 20:
                    info_tag.set_info(control.metadataClean(meta))
                else:
                    item.setInfo(type='Video', infoLabels=control.metadataClean(meta))
                video_streaminfo = {'codec': 'h264'}
                if kodi_version >= 20:
                    info_tag.add_stream_info('video', video_streaminfo)
                else:
                    item.addStreamInfo('video', video_streaminfo)
                url = '%s?action=episodes&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s&meta=%s&season=%s' % (sysaddon, systitle, year, imdb, tmdb, sysmeta, season)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                #log_utils.log('seasonDirectory', 1)
                pass
        try:
            control.property(syshandle, 'showplot', items[0]['plot'])
        except:
            #log_utils.log('seasonDirectory', 1)
            pass
        control.content(syshandle, 'seasons')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('seasons', {'skin.aeon.nox.silvo' : 50, 'skin.estuary': 55, 'skin.confluence': 500}) #View 50 List #View 501 LowList


class episodes:
    def __init__(self):
        self.list = []
        self.datetime = datetime.datetime.utcnow()
        self.systime = self.datetime.strftime('%Y%m%d%H%M%S%f')
        self.today_date = self.datetime.strftime('%Y-%m-%d')
        self.addon_caching = control.setting('addon.caching') or 'true'
        self.episode_thumbs = control.setting('episode.thumbs') or 'false'
        self.episode_views = control.setting('episode.views') or 'false'
        self.shownoyear = control.setting('show.noyear') or 'false'
        self.showunaired = control.setting('showunaired') or 'true'
        self.unairedcolor = control.setting('unaired.color')
        if self.unairedcolor == '':
            self.unairedcolor = 'darkred'
        self.specials = control.setting('tv.specials') or 'true'
        self.lang = control.apiLanguage()['tmdb'] or 'en'
        self.hq_artwork = control.setting('hq.artwork') or 'false'
        self.tmdb_key = control.setting('tmdb.api')
        if self.tmdb_key == '' or self.tmdb_key == None:
            self.tmdb_key = 'c8b7db701bac0b26edfcc93b39858972'
        self.trakt_user = control.setting('trakt.user').strip()
        self.trakt_item_limit = str(control.setting('trakt.item.limit')) or '100'
        self.fanart_tv_user = control.setting('fanart.api')
        self.trakt_link = 'https://api.trakt.tv'
        self.tvmaze_link = 'https://api.tvmaze.com'
        self.tmdb_link = 'https://api.themoviedb.org'
        self.fanart_tv_art_link = 'http://webservice.fanart.tv/v3/tv/%s'
        #self.tmdb_image_link = 'https://image.tmdb.org/t/p/original'
        self.tmdb_image_link = 'https://image.tmdb.org/t/p/w%s%s'


        self.tmdb_season_link = self.tmdb_link + '/3/tv/%s/season/%s?api_key=%s&language=en-US&append_to_response=aggregate_credits' % ('%s', '%s', self.tmdb_key)
        self.tmdb_episode_link = self.tmdb_link + '/3/tv/%s/season/%s/episode/%s?api_key=%s&language=en-US&append_to_response=credits' % ('%s', '%s', '%s', self.tmdb_key)

        self.tmdb_by_query_imdb_link = self.tmdb_link + '/3/find/%s?api_key=%s&external_source=imdb_id' % ('%s', self.tmdb_key)

        self.tmdb_search_link = self.tmdb_link + '/3/search/tv?api_key=%s&language=en-US&query=%s&page=1' % (self.tmdb_key, '%s')

        self.trakt_mycalendar_link = self.trakt_link + '/calendars/my/shows/date[30]/31/' #go back 30 and show all shows aired until tomorrow
        self.trakt_progress_link = self.trakt_link + '/users/me/watched/shows'
        self.trakt_hiddenprogress_link = self.trakt_link + '/users/hidden/progress_watched?limit=1000&type=show'
        self.trakt_history_link = self.trakt_link + '/users/me/history/shows?limit=300' # '40'
        self.trakt_ondeck_link = self.trakt_link + '/sync/playback/episodes?limit=20'
        self.trakt_list_link = self.trakt_link + '/users/%s/lists/%s/items'
        self.trakt_lists_link = self.trakt_link + '/users/me/lists'
        self.trakt_likedlists_link = self.trakt_link + '/users/likes/lists?limit=1000000'

        self.tvmaze_added_link = self.tvmaze_link + '/schedule'
        self.tvmaze_calendar_link = self.tvmaze_link + '/schedule?date=%s'


    def get(self, tvshowtitle, year, imdb, tmdb, meta, season=None, episode=None, idx=True, create_directory=True):
        try:
            if idx == True:
                if season == None or episode == None:
                    if self.addon_caching == 'true':
                        self.list = cache.get(self.tmdb_list, 1, tvshowtitle, year, imdb, tmdb, season, meta)
                    else:
                        self.list = self.tmdb_list(tvshowtitle, year, imdb, tmdb, season, meta)
                else:
                    if self.addon_caching == 'true':
                        self.list = cache.get(self.tmdb_list, 1, tvshowtitle, year, imdb, tmdb, season, meta)
                    else:
                        self.list = self.tmdb_list(tvshowtitle, year, imdb, tmdb, season, meta)
                    num = [x for x,y in enumerate(self.list) if y['season'] == str(season) and y['episode'] == str(episode)][-1]
                    self.list = [y for x,y in enumerate(self.list) if x >= num]
                if create_directory == True:
                    self.episodeDirectory(self.list)
                return self.list
            else:
                self.list = self.tmdb_list(tvshowtitle, year, imdb, tmdb, season, lite=True)
                return self.list
        except:
            #log_utils.log('get', 1)
            pass


    def calendar(self, url):
        try:
            try:
                url = getattr(self, url + '_link')
            except:
                pass
            if self.trakt_link in url and url == self.trakt_ondeck_link:
                if self.addon_caching == 'true':
                    self.blist = cache.get(self.trakt_episodes_list, 0, url, self.trakt_user, self.lang)
                else:
                    self.blist = self.trakt_episodes_list(url, self.trakt_user, self.lang)
                self.list = []
                self.list = self.trakt_episodes_list(url, self.trakt_user, self.lang)
                self.list = sorted(self.list, key=lambda k: int(k['paused_at']), reverse=True)
            elif self.trakt_link in url and url == self.trakt_progress_link:
                if self.addon_caching == 'true':
                    self.blist = cache.get(self.trakt_progress_list, 720, url, self.trakt_user, self.lang)
                else:
                    self.blist = self.trakt_progress_list(url, self.trakt_user, self.lang)
                self.list = []
                if self.addon_caching == 'true':
                    self.list = cache.get(self.trakt_progress_list, 0, url, self.trakt_user, self.lang)
                else:
                    self.list = self.trakt_progress_list(url, self.trakt_user, self.lang)
            elif self.trakt_link in url and url == self.trakt_mycalendar_link:
                if self.addon_caching == 'true':
                    self.blist = cache.get(self.trakt_episodes_list, 720, url, self.trakt_user, self.lang)
                else:
                    self.blist = self.trakt_episodes_list(url, self.trakt_user, self.lang)
                self.list = []
                if self.addon_caching == 'true':
                    self.list = cache.get(self.trakt_episodes_list, 0, url, self.trakt_user, self.lang)
                else:
                    self.list = self.trakt_episodes_list(url, self.trakt_user, self.lang)
                self.list = sorted(self.list, key=lambda k: k['premiered'], reverse=True)
            elif self.trakt_link in url and url == self.trakt_history_link:
                if self.addon_caching == 'true':
                    self.list = cache.get(self.trakt_episodes_list, 0.3, url, self.trakt_user, self.lang)
                else:
                    self.list = self.trakt_episodes_list(url, self.trakt_user, self.lang)
                self.list = sorted(self.list, key=lambda k: int(k['watched_at']), reverse=True)
            elif self.trakt_link in url and '/users/' in url:
                if self.addon_caching == 'true':
                    self.list = cache.get(self.trakt_list, 0.3, url, self.trakt_user)
                else:
                    self.list = self.trakt_list(url, self.trakt_user)
                self.list = self.list[::-1]
            elif self.trakt_link in url:
                if self.addon_caching == 'true':
                    self.list = cache.get(self.trakt_list, 1, url, self.trakt_user)
                else:
                    self.list = self.trakt_list(url, self.trakt_user)
            elif self.tvmaze_link in url and url == self.tvmaze_added_link:
                urls = [i['url'] for i in self.calendars(idx=False)][:5]
                self.list = []
                for url in urls:
                    if self.addon_caching == 'true':
                        self.list += cache.get(self.tvmaze_list, 720, url, True)
                    else:
                        self.list += self.tvmaze_list(url, True)
            elif self.tvmaze_link in url:
                if self.addon_caching == 'true':
                    self.list = cache.get(self.tvmaze_list, 1, url, False)
                else:
                    self.list = self.tvmaze_list(url, False)
            self.episodeDirectory(self.list)
            return self.list
        except:
            #log_utils.log('calendar', 1)
            pass


    def widget(self):
        if trakt.getTraktIndicatorsInfo() == True:
            setting = control.setting('episode.widget.alt')
        else:
            setting = control.setting('episode.widget')
        if setting == '2':
            self.calendar(self.tvmaze_added_link)
        elif setting == '3':
            self.calendar(self.trakt_progress_link)
        elif setting == '4':
            self.calendar(self.trakt_mycalendar_link)
        else:
            self.calendars()


    def calendars(self, idx=True):
        m = ('January|February|March|April|May|June|July|August|September|October|November|December').split('|')
        try:
            months = [(m[0], 'January'), (m[1], 'February'), (m[2], 'March'), (m[3], 'April'), (m[4], 'May'), (m[5], 'June'), (m[6], 'July'), (m[7], 'August'), (m[8], 'September'), (m[9], 'October'), (m[10], 'November'), (m[11], 'December')]
        except:
            months = []
        d = ('Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday').split('|')
        try:
            days = [(d[0], 'Monday'), (d[1], 'Tuesday'), (d[2], 'Wednesday'), (d[3], 'Thursday'), (d[4], 'Friday'), (d[5], 'Saturday'), (d[6], 'Sunday')]
        except:
            days = []
        for i in range(0, 30):
            try:
                name = (self.datetime - datetime.timedelta(days = i))
                name = ('[B]%s[/B] : %s' % (name.strftime('%A'), six.ensure_str(name.strftime('%d %B'))))
                for m in months:
                    name = name.replace(m[1], m[0])
                for d in days:
                    name = name.replace(d[1], d[0])
                try:
                    name = six.ensure_str(name)
                except:
                    pass
                url = self.tvmaze_calendar_link % (self.datetime - datetime.timedelta(days = i)).strftime('%Y-%m-%d')
                self.list.append({'name': name, 'url': url, 'image': 'calendar.png', 'action': 'calendar'})
            except:
                #log_utils.log('calendars', 1)
                pass
        if idx == True:
            self.addDirectory(self.list)
        return self.list


    def userlists(self):
        userlists = []
        try:
            if trakt.getTraktCredentialsInfo() == False:
                raise Exception()
            activity = trakt.getActivity()
            userlists += self.trakt_user_list(self.trakt_lists_link, self.trakt_user)
            userlists += self.trakt_user_list(self.trakt_likedlists_link, self.trakt_user)
        except:
            #log_utils.log('userlists', 1)
            pass
        self.list = userlists
        for i in range(0, len(self.list)):
            self.list[i].update({'image': 'userlists.png', 'action': 'calendar'})
        self.addDirectory(self.list, queue=True)
        return self.list


    def trakt_list(self, url, user):
        try:
            for i in re.findall('date\[(\d+)\]', url):
                url = url.replace('date[%s]' % i, (self.datetime - datetime.timedelta(days = int(i))).strftime('%Y-%m-%d'))
            q = dict(urllib_parse.parse_qsl(urllib_parse.urlsplit(url).query))
            q.update({'extended': 'full'})
            q = (urllib_parse.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urllib_parse.urlparse(url).query, '') + '?' + q
            itemlist = []
            items = trakt.getTraktAsJson(u)
        except:
            #log_utils.log('trakt_list', 1)
            return
        for item in items:
            try:
                title = item['episode']['title']
                if title == None or title == '':
                    raise Exception()
                title = client_utils.replaceHTMLCodes(six.ensure_str(title))
                season = item['episode']['season']
                season = re.sub('[^0-9]', '', '%01d' % int(season))
                if season == '0':
                    raise Exception()
                episode = item['episode']['number']
                episode = re.sub('[^0-9]', '', '%01d' % int(episode))
                if episode == '0':
                    raise Exception()
                tvshowtitle = item['show']['title']
                if not tvshowtitle:
                    raise Exception()
                else:
                    tvshowtitle = client_utils.replaceHTMLCodes(six.ensure_str(tvshowtitle))
                year = item['show']['year']
                year = re.sub('[^0-9]', '', str(year))
                imdb = item['show']['ids']['imdb']
                if imdb == None or imdb == '':
                    imdb = '0'
                else:
                    imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                tvdb = item['show']['ids']['tvdb']
                if not tvdb:
                    tvdb == '0'
                tvdb = re.sub('[^0-9]', '', str(tvdb))
                tmdb = item['show']['ids']['tmdb']
                if not tmdb:
                    raise Exception()
                tmdb = str(tmdb)
                premiered = item['episode']['first_aired']
                try:
                    premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except:
                    premiered = '0'
                try:
                    studio = item['show']['network']
                    studio = [x['name'] for x in studio]#[0]
                except:
                    studio = []#'0'
                if studio == '' or studio == None or studio == []:
                    studio = []#'0'
                try:
                    genre = item['show']['genres']
                    genre = [i.title() for i in genre]
                except:
                    genre = []#'0'
                if genre == '' or genre == None or genre == []:
                    genre = []#'0'
                #genre = ' / '.join(genre)
                try:
                    duration = str(item['show']['runtime'])
                except:
                    duration = ''
                if not duration:
                    duration = '0'
                try:
                    rating = str(item['episode']['rating'])
                except:
                    rating = '0'
                if rating == None or rating == '0.0':
                    rating = '0'
                try:
                    votes = str(item['episode']['votes'])
                except:
                    votes = '0'
                try:
                    votes = str(format(int(votes),',d'))
                except:
                    pass
                if not votes:
                    votes = '0'
                mpaa = item['show']['certification']
                if not mpaa:
                    mpaa = '0'
                try:
                    plot = item['episode']['overview']
                except:
                    plot = ''
                if not plot:
                    plot = item['show']['overview']
                if not plot:
                    plot = '0'
                else:
                    plot = client_utils.replaceHTMLCodes(six.ensure_str(plot, errors='replace'))
                try:
                    paused_at = item.get('paused_at', '0') or '0'
                    paused_at = re.sub('[^0-9]+', '', paused_at)
                except:
                    paused_at = '0'
                try:
                    watched_at = item.get('watched_at', '0') or '0'
                    watched_at = re.sub('[^0-9]+', '', watched_at)
                except:
                    watched_at = '0'
                try:
                    if self.lang == 'en':
                        raise Exception()
                    trans_item = trakt.getTVShowTranslation(imdb, lang=self.lang, season=season, episode=episode, full=True)
                    title = client_utils.replaceHTMLCodes(six.ensure_str(trans_item.get('title'))) or title
                    plot = client_utils.replaceHTMLCodes(six.ensure_str(trans_item.get('overview'), errors='replace')) or plot
                    #tvshowtitle = trakt.getTVShowTranslation(imdb, lang=self.lang) or tvshowtitle
                except:
                    #log_utils.log('trakt_list', 1)
                    pass
                itemlist.append({'title': title, 'season': season, 'episode': episode, 'tvshowtitle': tvshowtitle, 'year': year, 'premiered': premiered, 'status': 'Continuing', 'studio': studio, 'genre': genre,
                    'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'plot': plot, 'imdb': imdb, 'tvdb': tvdb, 'tmdb': tmdb, 'poster': '0', 'thumb': '0', 'paused_at': paused_at, 'watched_at': watched_at}
                )
            except:
                #log_utils.log('trakt_list', 1)
                pass
        itemlist = itemlist[::-1]
        return itemlist


    def trakt_progress_list(self, url, user, lang):
        try:
            url += '?extended=full'
            result = trakt.getTraktAsJson(url)
        except:
            #log_utils.log('trakt_progress_list', 1)
            return
        items = []
        sortorder = control.setting('prgr.sortorder')
        for item in result:
            try:
                num_1 = 0
                for i in range(0, len(item['seasons'])):
                    if item['seasons'][i]['number'] > 0:
                        num_1 += len(item['seasons'][i]['episodes'])
                num_2 = int(item['show']['aired_episodes'])
                if num_1 >= num_2:
                    raise Exception()
                season = str(item['seasons'][-1]['number'])
                episode = [x for x in item['seasons'][-1]['episodes'] if 'number' in x]
                episode = sorted(episode, key=lambda x: x['number'])
                episode = str(episode[-1]['number'])
                tvshowtitle = item['show']['title']
                if not tvshowtitle:
                    raise Exception()
                else:
                    tvshowtitle = client_utils.replaceHTMLCodes(six.ensure_str(tvshowtitle))
                year = item['show']['year']
                year = re.sub('[^0-9]', '', str(year))
                if int(year) > int(self.datetime.strftime('%Y')):
                    if self.shownoyear != 'true':
                        raise Exception()
                imdb = item['show']['ids']['imdb']
                if not imdb:
                    imdb = '0'
                tvdb = item['show']['ids']['tvdb']
                if not tvdb:
                    tvdb = '0'
                else:
                    tvdb = re.sub('[^0-9]', '', str(tvdb))
                tmdb = item['show']['ids']['tmdb']
                if not tmdb:
                    tmdb = '0'
                else:
                    tmdb = str(tmdb)
                try:
                    studio = item['show']['network']
                    studio = [x['name'] for x in studio]#[0]
                except:
                    studio = []#'0'
                if studio == '' or studio == None or studio == []:
                    studio = []#'0'
                duration = item['show']['runtime']
                if not duration:
                    duration = '0'
                mpaa = item['show']['certification']
                if not mpaa:
                    mpaa = '0'
                status = item['show']['status']
                if not status:
                    status = '0'
                try:
                    genre = item['show']['genres']
                    genre = [i.title() for i in genre]
                except:
                    genre = []#'0'
                if genre == '' or genre == None or genre == []:
                    genre = []#'0'
                #genre = ' / '.join(genre)
                last_watched = item['last_watched_at']
                if last_watched == None or last_watched == '':
                    last_watched = '0'
                items.append({'imdb': imdb, 'tvdb': tvdb, 'tmdb': tmdb, 'tvshowtitle': tvshowtitle, 'year': year, 'studio': studio, 'duration': duration, 'mpaa': mpaa,
                    'status': status, 'genre': genre, 'snum': season, 'enum': episode, '_last_watched': last_watched}
                )
            except:
                #log_utils.log('trakt_progress_list', 1)
                pass
        try:
            result = trakt.getTraktAsJson(self.trakt_hiddenprogress_link)
            result = [str(i['show']['ids']['tmdb']) for i in result]
            items = [i for i in items if not i['tmdb'] in result]
        except:
            #log_utils.log('trakt_progress_list', 1)
            pass
        def items_list(i):
            tmdb, imdb, tvdb = i['tmdb'], i['imdb'], i['tvdb']
            if (not tmdb or tmdb == '0') and not imdb == '0':
                try:
                    url = self.tmdb_by_query_imdb_link % imdb
                    result = client.scrapePage(url, timeout='30').json()
                    id = result.get('tv_results', [])[0]
                    tmdb = id.get('id')
                    if not tmdb:
                        tmdb = '0'
                    else:
                        tmdb = str(tmdb)
                except:
                    #log_utils.log('trakt_progress_list', 1)
                    pass
            try:
                item = [x for x in self.blist if x['tmdb'] == tmdb and x['snum'] == i['snum'] and x['enum'] == i['enum']][0]
                item['action'] = 'episodes'
                self.list.append(item)
                return
            except:
                #log_utils.log('trakt_progress_list', 1)
                pass
            try:
                if tmdb == '0':
                    raise Exception()
                _episode = str(int(i['enum']) + 1)
                _season = str(int(i['snum']) + 1)
                url = self.tmdb_episode_link % (tmdb, i['snum'], _episode)
                item = client.scrapePage(url, timeout='30').json()
                if item.get('status_code') == 34:
                    url2 = self.tmdb_episode_link % (tmdb, _season, '1')
                    item = client.scrapePage(url2, timeout='30').json()
                try:
                    premiered = item['air_date']
                except:
                    premiered = ''
                if not premiered:
                    premiered = '0'
                unaired = ''
                if i['status'] == 'Ended':
                    pass
                elif premiered == '0':
                    if self.shownoyear != 'true':
                        raise Exception()
                elif int(re.sub(r'[^0-9]', '', str(premiered))) > int(re.sub(r'[^0-9]', '', str(self.today_date))):
                    unaired = 'true'
                    if self.showunaired != 'true':
                        raise Exception()
                title = item['name']
                if not title:
                    title = '0'
                else:
                    title = client_utils.replaceHTMLCodes(six.ensure_str(title))
                season = item['season_number']
                season = '%01d' % season
                #if int(season) == 0:# and self.specials != 'true':
                    #raise Exception()
                episode = item['episode_number']
                episode = '%01d' % episode
                tvshowtitle = i['tvshowtitle']
                year = i['year']
                try:
                    thumb = item['still_path']
                except:
                    thumb = ''
                if not (thumb == '' or thumb == None):
                    #thumb = self.tmdb_image_link + item['still_path']
                    thumb = self.tmdb_image_link % ('300', thumb)
                else:
                    thumb = '0'
                try:
                    rating = str(item['vote_average'])
                except:
                    rating = ''
                if not rating:
                    rating = '0'
                try:
                    votes = str(item['vote_count'])
                except:
                    votes = ''
                if not votes:
                    votes = '0'
                try:
                    plot = item['overview']
                except:
                    plot = ''
                if not plot:
                    plot = '0'
                else:
                    plot = client_utils.replaceHTMLCodes(six.ensure_str(plot, errors='replace'))
                try:
                    r_crew = item['crew']
                    director = [d['name'] for d in r_crew if d['job'] == 'Director']
                    #director = ', '.join([d['name'] for d in director])
                    if not director:
                        director = []#'0'
                    writer = [w['name'] for w in r_crew if w['job'] == 'Writer']
                    #writer = ', '.join([w['name'] for w in writer])
                    if not writer:
                        writer = []#'0'
                except:
                    director = []#''
                    writer = []#''
                castwiththumb = []
                try:
                    r_cast = item['credits']['cast'][:30]
                    for person in r_cast:
                        _icon = person['profile_path']
                        #icon = self.tmdb_image_link + _icon if _icon else ''
                        icon = self.tmdb_image_link % ('185', _icon) if _icon else ''
                        castwiththumb.append({'name': person['name'], 'role': person['character'], 'thumbnail': icon})
                except:
                    pass
                if not castwiththumb:
                    castwiththumb = '0'
                poster = fanart = banner = landscape = clearlogo = clearart = '0'
                if not tvdb == '0':
                    poster, fanart, banner, landscape, clearlogo, clearart = self.fanart_tv_art(tvdb)
                self.list.append({'title': title, 'season': season, 'episode': episode, 'tvshowtitle': tvshowtitle, 'year': year, 'premiered': premiered, 'studio': i.get('studio'), 'genre': i.get('genre'), 'status': i.get('status'),
                    'duration': i.get('duration'), 'rating': rating, 'votes': votes, 'mpaa': i.get('mpaa'), 'director': director, 'writer': writer, 'castwiththumb': castwiththumb, 'plot': plot,
                    'poster': poster, 'banner': banner, 'fanart': fanart, 'thumb': thumb, 'clearlogo': clearlogo, 'clearart': clearart, 'landscape': landscape, 'snum': i['snum'], 'enum': i['enum'], 'action': 'episodes',
                    'unaired': unaired, '_last_watched': i['_last_watched'], 'imdb': imdb, 'tvdb': tvdb, 'tmdb': tmdb, '_sort_key': max(i['_last_watched'],premiered)}
                )
            except:
                #log_utils.log('trakt_progress_list', 1)
                pass
        try:
            if self.trakt_item_limit == '50':
                items = items[:50]
            elif self.trakt_item_limit == '150':
                items = items[:150]
            else:
                items = items[:100]
            threads = []
            for i in items:
                threads.append(workers.Thread(items_list, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            if sortorder == '0':
                self.list = sorted(self.list, key=lambda k: k['premiered'], reverse=True)
            else:
                self.list = sorted(self.list, key=lambda k: k['_sort_key'], reverse=True)
        except:
            #log_utils.log('trakt_progress_list', 1)
            pass
        return self.list


    def trakt_episodes_list(self, url, user, lang):
        items = self.trakt_list(url, user)
        def items_list(i):
            tmdb, imdb, tvdb = i['tmdb'], i['imdb'], i['tvdb']
            if (not tmdb or tmdb == '0') and not imdb == '0':
                try:
                    url = self.tmdb_by_query_imdb_link % imdb
                    result = client.scrapePage(url, timeout='30').json()
                    id = result.get('tv_results', [])[0]
                    tmdb = id.get('id')
                    if not tmdb:
                        tmdb = '0'
                    else:
                        tmdb = str(tmdb)
                except:
                    #log_utils.log('trakt_episodes_list', 1)
                    pass
            try:
                item = [x for x in self.blist if x['tmdb'] == tmdb and x['season'] == i['season'] and x['episode'] == i['episode']][0]
                if item['poster'] == '0':
                    raise Exception()
                self.list.append(item)
                return
            except:
                #log_utils.log('trakt_episodes_list', 1)
                pass
            try:
                if tmdb == '0':
                    raise Exception()
                if i['season'] == '0':
                    raise Exception()
                url = self.tmdb_episode_link % (tmdb, i['season'], i['episode'])
                item = client.scrapePage(url, timeout='30').json()
                title = item['name']
                if not title:
                    title = '0'
                else:
                    title = client_utils.replaceHTMLCodes(six.ensure_str(title))
                season = item['season_number']
                season = '%01d' % season
                #if int(season) == 0:# and self.specials != 'true':
                    #raise Exception()
                episode = item['episode_number']
                episode = '%01d' % episode
                tvshowtitle = i['tvshowtitle']
                premiered = i['premiered']
                status, duration, mpaa, studio, genre, year = i['status'], i['duration'], i['mpaa'], i['studio'], i['genre'], i['year']
                rating, votes = i['rating'], i['votes']
                try:
                    thumb = item['still_path']
                except:
                    thumb = ''
                if not (thumb == '' or thumb == None):
                    #thumb = self.tmdb_image_link + item['still_path']
                    thumb = self.tmdb_image_link % ('300', thumb)
                else:
                    thumb = '0'
                try:
                    plot = item['overview']
                except:
                    plot = ''
                if not plot:
                    plot = i['plot']
                else:
                    plot = client_utils.replaceHTMLCodes(six.ensure_str(plot, errors='replace'))
                try:
                    r_crew = item['crew']
                    director = [d['name'] for d in r_crew if d['job'] == 'Director']
                    #director = ', '.join([d['name'] for d in director])
                    writer = [w['name'] for w in r_crew if w['job'] == 'Writer']
                    #writer = ', '.join([w['name'] for w in writer])
                except:
                    director = writer = []#''
                if not director:
                    director = []#'0'
                if not writer:
                    writer = []#'0'
                castwiththumb = []
                try:
                    r_cast = item['credits']['cast'][:30]
                    for person in r_cast:
                        _icon = person['profile_path']
                        #icon = self.tmdb_image_link + _icon if _icon else ''
                        icon = self.tmdb_image_link % ('185', _icon) if _icon else ''
                        castwiththumb.append({'name': person['name'], 'role': person['character'], 'thumbnail': icon})
                except:
                    pass
                if not castwiththumb:
                    castwiththumb = '0'
                paused_at = i.get('paused_at', '0') or '0'
                watched_at = i.get('watched_at', '0') or '0'
                poster = fanart = banner = landscape = clearlogo = clearart = '0'
                if not tvdb == '0':
                    poster, fanart, banner, landscape, clearlogo, clearart = self.fanart_tv_art(tvdb)
                self.list.append({'title': title, 'season': season, 'episode': episode, 'tvshowtitle': tvshowtitle, 'year': year, 'premiered': premiered, 'status': status, 'studio': studio, 'genre': genre,
                    'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'castwiththumb': castwiththumb, 'plot': plot,
                    'imdb': imdb, 'tvdb': tvdb, 'tmdb': tmdb, 'poster': poster, 'banner': banner, 'fanart': fanart, 'thumb': thumb, 'clearlogo': clearlogo, 'clearart': clearart, 'landscape': landscape,
                    'paused_at': paused_at, 'watched_at': watched_at}
                )
            except:
                #log_utils.log('trakt_episodes_list', 1)
                pass
        if self.trakt_item_limit == '50':
            items = items[:50]
        elif self.trakt_item_limit == '150':
            items = items[:150]
        else:
            items = items[:100]
        threads = []
        for i in items:
            threads.append(workers.Thread(items_list, i))
        [i.start() for i in threads]
        [i.join() for i in threads]
        return self.list


    def trakt_user_list(self, url, user):
        try:
            items = trakt.getTraktAsJson(url)
        except:
            #log_utils.log('trakt_user_list', 1)
            pass
        for item in items:
            try:
                try:
                    name = item['list']['name']
                except:
                    name = item['name']
                name = client_utils.replaceHTMLCodes(six.ensure_str(name))
                try:
                    url = (trakt.slug(item['list']['user']['username']), item['list']['ids']['slug'])
                except:
                    url = ('me', item['ids']['slug'])
                url = self.trakt_list_link % url
                url = six.ensure_str(url)
                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                #log_utils.log('trakt_user_list', 1)
                pass
        self.list = sorted(self.list, key=lambda k: k['name'])
        return self.list


    def tvmaze_list(self, url, limit):
        itemlist = []
        try:
            items = client.scrapePage(url, timeout='30').json()
        except:
            #log_utils.log('tvmaze_list', 1)
            return
        for item in items:
            try:
                if not 'english' in item['show']['language'].lower():
                    raise Exception()
                if limit == True and not 'scripted' in item['show']['type'].lower():
                    raise Exception()
                title = item['name']
                if title == None or title == '':
                    raise Exception()
                title = client_utils.replaceHTMLCodes(six.ensure_str(title))
                season = item['season']
                season = re.sub('[^0-9]', '', '%01d' % int(season))
                if season == '0':
                    raise Exception()
                season = six.ensure_str(season)
                episode = item['number']
                episode = re.sub('[^0-9]', '', '%01d' % int(episode))
                if episode == '0':
                    raise Exception()
                episode = six.ensure_str(episode)
                tvshowtitle = item['show']['name']
                if tvshowtitle == None or tvshowtitle == '':
                    raise Exception()
                tvshowtitle = client_utils.replaceHTMLCodes(six.ensure_str(tvshowtitle))
                year = item['show']['premiered']
                year = re.findall('(\d{4})', year)[0]
                year = six.ensure_str(year)
                imdb = item['show']['externals']['imdb']
                if imdb == None or imdb == '':
                    imdb = '0'
                else:
                    imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
                imdb = six.ensure_str(imdb)
                tvdb = item['show']['externals']['thetvdb']
                if tvdb == None or tvdb == '':
                    tvdb = '0'
                tvdb = re.sub('[^0-9]', '', str(tvdb))
                tvdb = six.ensure_str(tvdb)
                poster1 = '0'
                try:
                    poster1 = item['show']['image']['original']
                except:
                    poster1 = '0'
                if poster1 == None or poster1 == '':
                    poster1 = '0'
                else:
                    poster1 = six.ensure_str(poster1)
                try:
                    thumb1 = item['show']['image']['original']
                except:
                    thumb1 = '0'
                try:
                    thumb2 = item['image']['original']
                except:
                    thumb2 = '0'
                if thumb2 == None or thumb2 == '0':
                    thumb = thumb1
                else:
                    thumb = thumb2
                if thumb == None or thumb == '':
                    thumb = '0'
                thumb = six.ensure_str(thumb)
                premiered = item['airdate']
                try:
                    premiered = re.findall('(\d{4}-\d{2}-\d{2})', premiered)[0]
                except:
                    premiered = '0'
                premiered = six.ensure_str(premiered)
                try:
                    studio = item['show']['network']
                    studio = [x['name'] for x in studio]#[0]
                except:
                    studio = []#'0'
                if studio == '' or studio == None or studio == []:
                    studio = []#'0'
                #studio = six.ensure_str(studio)
                try:
                    genre = item['show']['genres']
                    genre = [i.title() for i in genre]
                except:
                    genre = []#'0'
                if genre == '' or genre == None or genre == []:
                    genre = []#'0'
                #genre = ' / '.join(genre)
                #genre = six.ensure_str(genre)
                try:
                    duration = item['show']['runtime']
                except:
                    duration = '0'
                if duration == None:
                    duration = '0'
                duration = str(duration)
                duration = six.ensure_str(duration)
                try:
                    rating = item['show']['rating']['average']
                except:
                    rating = '0'
                if rating == None or rating == '0.0':
                    rating = '0'
                rating = str(rating)
                rating = six.ensure_str(rating)
                votes = '0'
                try:
                    plot = item['show']['summary']
                except:
                    plot = '0'
                if plot == None:
                    plot = '0'
                plot = re.sub('<.+?>|</.+?>|\n', '', plot)
                plot = client_utils.replaceHTMLCodes(six.ensure_str(plot))
                poster2 = fanart = banner = landscape = clearlogo = clearart = '0'
                if not tvdb == '0':
                    poster2, fanart, banner, landscape, clearlogo, clearart = self.fanart_tv_art(tvdb)
                poster = poster2 if not poster2 == '0' else poster1
                itemlist.append({'title': title, 'season': season, 'episode': episode, 'tvshowtitle': tvshowtitle, 'year': year, 'premiered': premiered, 'status': 'Continuing',
                    'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'plot': plot, 'imdb': imdb, 'tvdb': tvdb, 'tmdb': '0',
                    'thumb': thumb, 'poster': poster, 'banner': banner, 'fanart': fanart, 'clearlogo': clearlogo, 'clearart': clearart, 'landscape': landscape}
                )
            except:
                #log_utils.log('tvmaze_list', 1)
                pass
        itemlist = itemlist[::-1]
        return itemlist


    def fanart_tv_art(self, tvdb):
        artmeta = True
        try:
            fanart_tv_headers = {'api-key': 'cb2f78390c6f7cbc5d1c9a257e013e5c'}
            if not self.fanart_tv_user == '':
                fanart_tv_headers.update({'client-key': self.fanart_tv_user})
            art = client.scrapePage(self.fanart_tv_art_link % tvdb, headers=fanart_tv_headers, timeout='30').json()
        except:
            artmeta = False
        if artmeta == False:
            pass
        poster = fanart = banner = landscape = clearlogo = clearart = '0'
        try:
            _poster = art['tvposter']
            _poster = [x for x in _poster if x.get('lang') == self.lang][::-1] + [x for x in _poster if x.get('lang') == 'en'][::-1] + [x for x in _poster if x.get('lang') in ['00', '']][::-1]
            _poster = _poster[0]['url']
            if _poster:
                poster = six.ensure_str(_poster)
        except:
            pass
        try:
            _fanart = art['showbackground']
            _fanart = [x for x in _fanart if x.get('lang') == self.lang][::-1] + [x for x in _fanart if x.get('lang') == 'en'][::-1] + [x for x in _fanart if x.get('lang') in ['00', '']][::-1]
            _fanart = _fanart[0]['url']
            if _fanart:
                fanart = six.ensure_str(_fanart)
        except:
            pass
        if self.hq_artwork == 'true':
            try:
                _banner = art['tvbanner']
                _banner = [x for x in _banner if x.get('lang') == self.lang][::-1] + [x for x in _banner if x.get('lang') == 'en'][::-1] + [x for x in _banner if x.get('lang') in ['00', '']][::-1]
                _banner = _banner[0]['url']
                if _banner:
                    banner = six.ensure_str(_banner)
            except:
                pass
            try:
                if 'hdtvlogo' in art:
                    _clearlogo = art['hdtvlogo']
                else:
                    _clearlogo = art['clearlogo']
                _clearlogo = [x for x in _clearlogo if x.get('lang') == self.lang][::-1] + [x for x in _clearlogo if x.get('lang') == 'en'][::-1] + [x for x in _clearlogo if x.get('lang') in ['00', '']][::-1]
                _clearlogo = _clearlogo[0]['url']
                if _clearlogo:
                    clearlogo = six.ensure_str(_clearlogo)
            except:
                pass
            try:
                if 'hdclearart' in art:
                    _clearart = art['hdclearart']
                else:
                    _clearart = art['clearart']
                _clearart = [x for x in _clearart if x.get('lang') == self.lang][::-1] + [x for x in _clearart if x.get('lang') == 'en'][::-1] + [x for x in _clearart if x.get('lang') in ['00', '']][::-1]
                _clearart = _clearart[0]['url']
                if _clearart:
                    clearart = six.ensure_str(_clearart)
            except:
                pass
            try:
                if 'tvthumb' in art:
                    _landscape = art['tvthumb']
                else:
                    _landscape = art['showbackground']
                _landscape = [x for x in _landscape if x.get('lang') == self.lang][::-1] + [x for x in _landscape if x.get('lang') == 'en'][::-1] + [x for x in _landscape if x.get('lang') in ['00', '']][::-1]
                _landscape = _landscape[0]['url']
                if _landscape:
                    landscape = six.ensure_str(_landscape)
            except:
                pass
        return poster, fanart, banner, landscape, clearlogo, clearart


    def tmdb_list(self, tvshowtitle, year, imdb, tmdb, season, meta=None, lite=False):
        try:
            tvdb = '0'
            if tmdb == '0' and not imdb == '0':
                try:
                    url = self.tmdb_by_query_imdb_link % imdb
                    result = client.scrapePage(url, timeout='30').json()
                    id = result.get('tv_results', [])[0]
                    tmdb = id.get('id')
                    if not tmdb:
                        tmdb = '0'
                    else:
                        tmdb = str(tmdb)
                except:
                    #log_utils.log('tmdb_list', 1)
                    pass
            if tmdb == '0':
                try:
                    url = self.tmdb_search_link % (urllib_parse.quote(tvshowtitle)) + '&first_air_date_year=' + year
                    result = client.scrapePage(url, timeout='30').json()
                    results = result['results']
                    show = [r for r in results if cleantitle.get(r.get('name')) == cleantitle.get(self.list[i]['title'])][0]# and re.findall('(\d{4})', r.get('first_air_date'))[0] == self.list[i]['year']][0]
                    tmdb = show.get('id')
                    if not tmdb:
                        tmdb = '0'
                    else:
                        tmdb = str(tmdb)
                except:
                    #log_utils.log('tmdb_list', 1)
                    pass
        except:
            #log_utils.log('tmdb_list', 1)
            return
        try:
            if tmdb == '0':
                raise Exception()
            episodes_url = self.tmdb_season_link % (tmdb, season)
            result = client.scrapePage(episodes_url, timeout='30').json()
            #result = control.six_decode(result)
            episodes = result.get('episodes', [])
            r_cast = result.get('aggregate_credits', {}).get('cast', [])
            if self.specials == 'false':
                episodes = [e for e in episodes if not e['season_number'] == 0]
        except:
            #log_utils.log('tmdb_list', 1)
            return
        try:
            poster = result['poster_path']
        except:
            poster = ''
        if not (poster == '' or poster == None):
            poster = self.tmdb_image_link % ('500', poster)
        else:
            poster = '0'
        fanart = banner = clearlogo = clearart = landscape = duration = status = '0'
        if meta:
            _meta = json.loads(urllib_parse.unquote_plus(meta))
            poster, fanart, banner, clearlogo, clearart, landscape, duration, status = _meta['poster'], _meta['fanart'], _meta['banner'], _meta['clearlogo'], _meta['clearart'], _meta['landscape'], _meta['duration'], _meta['status']
        for item in episodes:
            try:
                try:
                    title = item['name']
                except:
                    title = ''
                if not title:
                    title = '0'
                else:
                    title = client_utils.replaceHTMLCodes(six.ensure_str(title))
                label = title
                season = str(item['season_number'])
                episode = str(item['episode_number'])
                try:
                    premiered = item['air_date']
                except:
                    premiered = '0'
                unaired = ''
                if not premiered or premiered == '0':
                    if self.shownoyear != 'true':
                        raise Exception()
                elif int(re.sub('[^0-9]', '', str(premiered))) > int(re.sub('[^0-9]', '', str(self.today_date))):
                    unaired = 'true'
                    if self.showunaired != 'true':
                        raise Exception()
                try:
                    rating = str(item['vote_average'])
                except:
                    rating = ''
                if not rating:
                    rating = '0'
                try:
                    votes = str(item['vote_count'])
                except:
                    votes = ''
                if not votes:
                    votes = '0'
                try:
                    episodeplot = item['overview']
                except:
                    episodeplot = ''
                if not episodeplot:
                    episodeplot = '0'
                else:
                    episodeplot = client_utils.replaceHTMLCodes(six.ensure_str(episodeplot, errors='replace'))
                try:
                    r_crew = item['crew']
                    director = [d['name'] for d in r_crew if d['job'] == 'Director']
                    #director = ', '.join([d['name'] for d in director])
                    writer = [w['name'] for w in r_crew if w['job'] == 'Writer']
                    #writer = ', '.join([w['name'] for w in writer])
                except:
                    director = writer = []#''
                if not director:
                    director = []#'0'
                if not writer:
                    writer = []#'0'
                castwiththumb = []
                try:
                    for person in r_cast[:30]:
                        _icon = person['profile_path']
                        #icon = self.tmdb_image_link + _icon if _icon else ''
                        icon = self.tmdb_image_link % ('185', _icon) if _icon else ''
                        castwiththumb.append({'name': person['name'], 'role': person['roles'][0]['character'], 'thumbnail': icon})
                except:
                    pass
                if not castwiththumb:
                    castwiththumb = '0'
                try:
                    thumb_path = item['still_path']
                except:
                    thumb_path = ''
                if thumb_path:
                    #thumb = self.tmdb_image_link + thumb_path
                    thumb = self.tmdb_image_link % ('300', thumb_path)
                else:
                    thumb = fanart
                self.list.append({'title': title, 'label': label, 'season': season, 'episode': episode, 'tvshowtitle': tvshowtitle, 'year': year, 'premiered': premiered,
                    'rating': rating, 'votes': votes, 'director': director, 'writer': writer, 'castwiththumb': castwiththumb, 'duration': duration,
                    'status': status, 'plot': episodeplot, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': tvdb, 'unaired': unaired, 'thumb': thumb, 'poster': poster,
                    'fanart': fanart, 'banner': banner,'clearlogo': clearlogo, 'clearart': clearart, 'landscape': landscape}
                )
            except:
                #log_utils.log('tmdb_list', 1)
                pass
        return self.list


    def episodeDirectory(self, items):
        if items == None or len(items) == 0:
            control.idle()
            #sys.exit()
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        addonPoster = control.addonPoster()
        addonBanner = control.addonBanner()
        addonFanart = control.addonFanart()
        settingFanart = control.setting('fanart')
        traktCredentials = trakt.getTraktCredentialsInfo()
        tmdbCredentials = tmdb_utils.getTMDbCredentialsInfo()
        isPlayable = True if not 'plugin' in control.infoLabel('Container.PluginName') else False
        indicators = playcount.getTVShowIndicators(refresh=True)
        try:
            multi = [i['tvshowtitle'] for i in items]
        except:
            multi = []
        multi = len([x for y,x in enumerate(multi) if x not in multi[:y]])
        multi = True if multi > 1 else False
        try:
            sysaction = items[0]['action']
        except:
            sysaction = ''
        isFolder = False if not sysaction == 'episodes' else True
        playbackMenu = 'Select Source' if control.setting('hosts.mode') == '2' else 'Auto Play'
        watchedMenu = 'Watched in Trakt' if trakt.getTraktIndicatorsInfo() == True else 'Watched in Free99'
        unwatchedMenu = 'Unwatched in Trakt' if trakt.getTraktIndicatorsInfo() == True else 'Unwatched in Free99'
        for i in items:
            try:
                if not 'label' in i:
                    i['label'] = i['title']
                if i['label'] == '0':
                    label = '%sx%02d . %s %s' % (i['season'], int(i['episode']), 'Episode', i['episode'])
                else:
                    label = '%sx%02d . %s' % (i['season'], int(i['episode']), i['label'])
                if multi == True:
                    label = '%s - %s' % (i['tvshowtitle'], label)
                try:
                    if i['unaired'] == 'true':
                        label = '[COLOR %s][I]%s[/I][/COLOR]' % (self.unairedcolor, label)
                except:
                    pass
                imdb, tvdb, tmdb, year, season, episode = i['imdb'], i['tvdb'], i['tmdb'], i['year'], i['season'], i['episode']
                poster = i['poster'] if 'poster' in i and not i['poster'] == '0' else addonPoster
                fanart = i['fanart'] if 'fanart' in i and not i['fanart'] == '0' else addonFanart
                banner1 = i.get('banner', '')
                banner = banner1 or fanart or addonBanner
                if 'landscape' in i and not i['landscape'] == '0':
                    landscape = i['landscape']
                else:
                    landscape = fanart
                seasons_meta = {'poster': poster, 'fanart': fanart, 'banner': banner, 'clearlogo': i.get('clearlogo', '0'), 'clearart': i.get('clearart', '0'), 'landscape': landscape, 'duration': i.get('duration', '0'), 'status': i.get('status', '0')}
                seas_meta = urllib_parse.quote_plus(json.dumps(seasons_meta))
                systitle = urllib_parse.quote_plus(i['title'])
                systvshowtitle = urllib_parse.quote_plus(i['tvshowtitle'])
                syspremiered = urllib_parse.quote_plus(i['premiered'])
                meta = dict((k,v) for k, v in six.iteritems(i) if not v == '0')
                meta.update({'mediatype': 'episode'})
                meta.update({'code': tmdb, 'imdbnumber': imdb})
                meta.update({'trailer': '%s?action=trailer&name=%s&tmdb=%s&imdb=%s&season=%s&episode=%s' % (sysaddon, systvshowtitle, tmdb, imdb, season, episode)})
                if not 'duration' in i:
                    meta.update({'duration': '45'})
                elif i['duration'] == '0':
                    meta.update({'duration': '45'})
                try:
                    meta.update({'duration': str(int(meta['duration']) * 60)})
                except:
                    pass
                try:
                    meta.update({'year': re.findall('(\d{4})', i['premiered'])[0]})
                except:
                    pass
                try:
                    meta.update({'title': i['label']})
                except:
                    pass
                try:
                    meta.update({'tvshowyear': i['year']}) # Kodi uses the year (the year the show started) as the year for the episode. Change it from the premiered date.
                except:
                    pass
                meta.update({'poster': poster, 'fanart': fanart, 'banner': banner})
                sysmeta = urllib_parse.quote_plus(json.dumps(meta))
                url = '%s?action=play&title=%s&year=%s&imdb=%s&tmdb=%s&season=%s&episode=%s&tvshowtitle=%s&premiered=%s&meta=%s&t=%s' % (sysaddon, systitle, year, imdb, tmdb, season, episode, systvshowtitle, syspremiered, sysmeta, self.systime)
                sysurl = urllib_parse.quote_plus(url)
                path = '%s?action=play&title=%s&year=%s&imdb=%s&tmdb=%s&season=%s&episode=%s&tvshowtitle=%s&premiered=%s' % (sysaddon, systitle, year, imdb, tmdb, season, episode, systvshowtitle, syspremiered)
                if isFolder == True:
                    url = '%s?action=episodes&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s&meta=%s&season=%s&episode=%s' % (sysaddon, systvshowtitle, year, imdb, tmdb, seas_meta, season, episode)
                cm = []
                cm.append(('Clean Tools Widget', 'RunPlugin(%s?action=cleantools_widget)' % sysaddon))
                cm.append(('Clear Providers', 'RunPlugin(%s?action=clear_sources)' % sysaddon))
                if multi == True:
                    cm.append(('Browse Series', 'Container.Update(%s?action=seasons&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s&meta=%s,return)' % (sysaddon, systvshowtitle, year, imdb, tmdb, seas_meta)))
                cm.append(('Queue Item', 'RunPlugin(%s?action=queue_item)' % sysaddon))
                if traktCredentials == True:
                    cm.append(('Trakt Manager', 'RunPlugin(%s?action=trakt_manager&name=%s&tmdb=%s&content=tvshow)' % (sysaddon, systvshowtitle, tmdb)))
                if tmdbCredentials == True:
                    cm.append(('TMDb Manager', 'RunPlugin(%s?action=tmdb_manager&name=%s&tmdb=%s&content=tvshow)' % (sysaddon, systvshowtitle, tmdb)))
                cm.append(('Add to Library', 'RunPlugin(%s?action=tvshow_to_library&tvshowtitle=%s&year=%s&imdb=%s&tmdb=%s)' % (sysaddon, systvshowtitle, year, imdb, tmdb)))
                if kodi_version < 17:
                    cm.append(('Information', 'Action(Info)'))
                try:
                    overlay = int(playcount.getEpisodeOverlay(indicators, imdb, tmdb, season, episode))
                    if overlay == 7:
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=episodes_playcount&imdb=%s&tmdb=%s&season=%s&episode=%s&query=6)' % (sysaddon, imdb, tmdb, season, episode)))
                        meta.update({'playcount': 1, 'overlay': 7})
                    else:
                        cm.append((watchedMenu, 'RunPlugin(%s?action=episodes_playcount&imdb=%s&tmdb=%s&season=%s&episode=%s&query=7)' % (sysaddon, imdb, tmdb, season, episode)))
                        meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass
                if isFolder == False:
                    cm.append((playbackMenu, 'RunPlugin(%s?action=alter_sources&url=%s&meta=%s)' % (sysaddon, sysurl, sysmeta)))
                try:
                    item = control.item(label=label, offscreen=True)
                except:
                    item = control.item(label=label)
                art = {}
                if self.episode_thumbs == 'true':
                    thumb = poster
                else:
                    thumb = meta.get('thumb', '') or fanart
                clearlogo = meta.get('clearlogo', '')
                clearart = meta.get('clearart', '')
                art.update({'icon': thumb, 'thumb': thumb, 'banner': banner, 'poster': thumb, 'tvshow.poster': poster, 'season.poster': poster, 'landscape': landscape, 'clearlogo': clearlogo, 'clearart': clearart})
                if settingFanart == 'true':
                    art.update({'fanart': fanart})
                elif not addonFanart == None:
                    art.update({'fanart': addonFanart})
                item.setArt(art)
                item.addContextMenuItems(cm)
                if isPlayable:
                    item.setProperty('IsPlayable', 'true')
                offset = bookmarks.get('episode', imdb, season, episode, True)
                if float(offset) > 120:
                    percentPlayed = int(float(offset) / float(meta['duration']) * 100)
                    item.setProperty('resumetime', str(offset))
                    item.setProperty('percentplayed', str(percentPlayed))
                if kodi_version >= 20:
                    info_tag = ListItemInfoTag(item, 'video')
                castwiththumb = i.get('castwiththumb')
                if castwiththumb and not castwiththumb == '0':
                    if kodi_version >= 18:
                        if kodi_version >= 20:
                            info_tag.set_cast(castwiththumb)
                        else:
                            item.setCast(castwiththumb)
                    else:
                        cast = [(p['name'], p['role']) for p in castwiththumb]
                        meta.update({'cast': cast})
                if kodi_version >= 20:
                    info_tag.set_info(control.metadataClean(meta))
                else:
                    item.setInfo(type='Video', infoLabels=control.metadataClean(meta))
                video_streaminfo = {'codec': 'h264'}
                if kodi_version >= 20:
                    info_tag.add_stream_info('video', video_streaminfo)
                else:
                    item.addStreamInfo('video', video_streaminfo)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
            except:
                #log_utils.log('episodeDirectory', 1)
                pass
        if self.episode_views == 'true':
            control.content(syshandle, 'seasons')
            control.directory(syshandle, cacheToDisc=True)
            views.setView('seasons', {'skin.aeon.nox.silvo' : 50, 'skin.estuary': 55, 'skin.confluence': 500}) #View 50 List #View 501 LowList
        else:
            control.content(syshandle, 'episodes')
            control.directory(syshandle, cacheToDisc=True)
            views.setView('episodes', {'skin.aeon.nox.silvo' : 50, 'skin.estuary': 55, 'skin.confluence': 504}) #View 50 List #View 501 LowList



    def addDirectory(self, items, queue=False):
        if items == None or len(items) == 0:
            control.idle()
            #sys.exit()
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        addonFanart = control.addonFanart()
        addonThumb = control.addonThumb()
        artPath = control.artPath()
        for i in items:
            try:
                name = i['name']
                if i['image'].startswith('http'):
                    thumb = i['image']
                elif not artPath == None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb
                url = '%s?action=%s' % (sysaddon, i['action'])
                try:
                    url += '&url=%s' % urllib_parse.quote_plus(i['url'])
                except:
                    pass
                cm = []
                cm.append(('Clean Tools Widget', 'RunPlugin(%s?action=cleantools_widget)' % sysaddon))
                if queue == True:
                    cm.append(('Queue Item', 'RunPlugin(%s?action=queue_item)' % sysaddon))
                try:
                    item = control.item(label=name, offscreen=True)
                except:
                    item = control.item(label=name)
                item.setArt({'icon': thumb, 'thumb': thumb, 'fanart': addonFanart})
                item.addContextMenuItems(cm)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                #log_utils.log('addDirectory', 1)
                pass
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


