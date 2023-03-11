import requests
import json
import time
from datetime import datetime
from base64 import b64decode
from .plugin2 import Myaddon
from .tools import tools
from .db import DB
from .infolabels import Infolabels


class TMDB(Myaddon):
    
    api_key = b64decode('NmE1YmU0OTk5YWJmNzRlYmExZjlhODMxMTI5NGMyNjc=').decode('utf-8')
    base_url = 'https://api.themoviedb.org'
    popular_movies = f'{base_url}/3/movie/popular?api_key={api_key}&language=en-US'
    now_playing_movies = f'{base_url}/3/movie/now_playing?api_key={api_key}&language=en-US'
    upcoming_movies = f'{base_url}/3/movie/upcoming?api_key={api_key}&language=en-US'
    toprated_movies =f'{base_url}/3/movie/top_rated?api_key={api_key}&language=en-US'
    top_rated_shows = f'{base_url}/3/tv/top_rated?api_key={api_key}&language=en-US'
    popular_shows = f'{base_url}/3/tv/popular?api_key={api_key}&language=en-US'
    on_the_air_shows = f'{base_url}/3/tv/on_the_air?api_key={api_key}&language=en-US'
    images_path = 'https://image.tmdb.org/t/p/original'
    
    def movie_url(self, movie_id: int):
        return f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB.api_key}&language=en-US&append_to_response=videos,credits,release_dates,external_ids'
        
    def tvshow_url(self, tv_id: int):
        return f'https://api.themoviedb.org/3/tv/{tv_id}?api_key={TMDB.api_key}&language=en-US&append_to_response=videos,credits,release_dates,content_ratings,external_ids'
    
    def season_url(self, tv_id: int, season_number: int):
        return f'https://api.themoviedb.org/3/tv/{tv_id}/season/{season_number}?api_key={self.api_key}&language=en-US'
    
    def episode_url(self, tv_id: int, season_number: int, episode_number: int):
        return f'https://api.themoviedb.org/3/tv/{tv_id}/season/{season_number}/episode/{episode_number}?api_key={self.api_key}&language=en-US&append_to_response=videos,credits,release_dates'
    
    def search_url(self, media_type: str):
        return f'{self.base_url}/3/search/{media_type}?api_key={self.api_key}&language=en-US&query='
    
    def genre_url(self, media_type: str):
        return f'{self.base_url}/3/discover/{media_type}?api_key={self.api_key}&language=en-US&sort_by=popularity.desc&with_genres='
    
    def videos_url(self, media_type: str, tmdb_id):
        return f'{self.base_url}/3/{media_type}/{tmdb_id}/videos?api_key={self.api_key}&language=en-US'
    
    def get_results(self, url: str):
        response = requests.get(url).json()
        return response.get('results', response.get('parts'))
    
    def yt_link(self, video_id: int):
        return f'plugin://plugin.video.youtube/play/?video_id={video_id}'
    
    def get_tmdb_videos(self, url):
        results = self.get_results(url)
        videos = []
        for result in results:
            name = result['name']
            key = result['key']
            link = self.yt_link(key)
            videos.append([name, link])
        return videos
    
    def get_imdb_id(self, video_info: dict):
        ids = video_info.get('external_ids')
        if ids:
            return ids.get('imdb_id', '')
        if video_info.get('imdb_id'):
            return video_info.get('imdb_id', '')
        return ''
    
    def seasons(self, url, _id=''):
        item_list = requests.get(url).json()
        seasons_list = item_list['seasons']
        
        infolabels = {}
        cast = []
        tv_db = DB('tv')
        from_tv_db = tv_db.get(_id)
        if from_tv_db:
            from_tv_db = json.loads(from_tv_db[0])
            infolabels = from_tv_db['infolabels']
            cast = from_tv_db['cast']
        
        for season in seasons_list:
            name = f"Season {season['season_number']}"
            url = self.season_url(_id, season['season_number'])
            icon = f"{self.images_path}{season['poster_path']}"
            description = season['overview']
            if not description:
                description = infolabels['plot']
            infolabels['title'] = name
            infolabels['plot'] = description
            infolabels['premiered'] = season['air_date']
            
            self.add_dir(name, url, 'tmdb_router', icon, icon, description, foldername=name, _id=_id, media_type='season', infolabels=infolabels, cast=cast,  season_number=season['season_number'])
    
    def process_item(self, item_info: dict, media_type='movie', _id = '', season_number: int = 1):
        if media_type in ['movie', 'tv']:
            db = DB(media_type)
            lookup_id = item_info.get('id')
            query = db.get(lookup_id)
            if query:
                return json.loads(query[0])
        
        if media_type == 'movie':
            _id = item_info.get('id')
            url = self.movie_url(_id)
        elif media_type == 'tv':
            _id = item_info.get('id')
            url = self.tvshow_url(_id)
        elif media_type == 'episode':
            season_number = item_info.get('season_number')
            episode_number = item_info.get('episode_number')
            url = self.episode_url(_id, season_number, episode_number)
        self.log(f'url= {url}')
        video_info = requests.get(url).json()
        
        title = video_info.get('title', video_info.get('name', 'Unknown Title'))
        if media_type == 'episode':
            title = f'{episode_number}. {title}'
        if media_type in ['movie', 'episode']:
            link = f"TRAILERS/{self.videos_url(media_type, _id).replace('/episode/', '/tv/')}"
        else:
            link = url
        thumbnail = f"{self.images_path}{video_info.get('poster_path', video_info.get('still_path', self.addon_icon))}"
        fanart = f"{self.images_path}{video_info.get('backdrop_path', thumbnail)}"
        summary = video_info.get('overview', '')
        
        if media_type == 'episode':
            i = Infolabels(video_info, 'episode', tv_id=_id, season_number=season_number, episode_number=episode_number)
            infolabels, cast = i.infolabels_and_cast()
            
        else:
            i = Infolabels(video_info, media_type)
            infolabels, cast = i.infolabels_and_cast()
        
        premiered = infolabels.get('premiered', '')
        year = infolabels.get('premiered').split('-')[0] if premiered else ''
        if premiered and media_type == 'episode':
            _format = "%Y-%m-%d"
            try:
                if datetime(*(time.strptime(premiered, _format)[0:6])) > datetime.today():
                    title = tools.color_text('red', title)
                    self.log(f'title= {title}')
            except Exception as e:
                self.log(f'datetime failed: {e} premiered= {premiered}')
                
        elif not premiered and media_type == 'episode':
            title = tools.color_text('red', title)
            
        imdb_id = self.get_imdb_id(video_info)
        if media_type in ['movie', 'episode']:
            _type = 'item'
        else:
            _type = 'dir'
        
        item = {
            "title": title,
            "content": media_type,
            "link": link,
            "thumbnail": thumbnail,
            "fanart": fanart,
            "summary": summary,
            "type": _type,
            "year": year,
            "tmdb_id": _id,
            "imdb_id": imdb_id,
            "infolabels": infolabels,
            "cast": cast
        }
        if media_type in ['movie', 'tv']:
            db.set(_id, json.dumps(item))
        return item
    
    ###
    
    def tmdb_list(self, url: str, page: int = 1, _id: int = None, media_type: str = 'movie', mode: str = '', is_folder: bool = False):
        
        if _id and media_type == 'tv':
            return self.seasons(url, _id=_id)
        
        response = requests.get(f'{url}&page={page}').json()
        if media_type == 'season':
            results = response.get('episodes')
            mode = 'play_video'
            media_type = 'episode'
            is_folder = False
        else:
            results = response.get('results', response.get('parts'))
            
        for result in results:
            info = self.process_item(result, media_type=media_type, _id=_id)
            if info:
                _id = info['tmdb_id']
                title = info['title']
                link = info['link']
                thumbnail = info['thumbnail']
                fanart = info['fanart']
                summary = info['summary']
                season_number = info.get('season_number', '')
                media_type = info['content']
                infolabels = info['infolabels']
                cast = info['cast']
                
                self.add_dir(title, link, mode, thumbnail, fanart, summary, infolabels=infolabels, cast=cast, media_type=media_type, page=page, _id=_id, season_number=season_number, isFolder=is_folder)
        
        if response.get('total_pages', 1) > page:
            self.add_dir('Next Page', url, 'tmdb_router', 'https://cdn-icons-png.flaticon.com/512/2883/2883482.png', '', '', media_type=media_type, page=int(page)+1, isFolder=True)
    
    
    def tmdb_router(self, url: str, _id: int, page: int = 1, media_type: str = '', mode: str = ''):
        mode = 'play_video'
        is_folder = False
        
        if '/movie/' in url:
            media_type = 'movie'
        
        elif '/episode/' in url:
            media_type = 'episode'
                
        elif '/tv/' in url:
            mode = 'tmdb_router'
            is_folder = True
            if not '/season/' in url:
                media_type = 'tv'
            else:
                mode = 'tmdb_router'
                media_type = 'season'
        
        self.tmdb_list(url, _id=_id, page=page, media_type=media_type, mode=mode, is_folder=is_folder)


###---End of Class---###

tmdb = TMDB()

def tmdb_main():
    items = {
        'Popular Movies': tmdb.popular_movies,
        'Now Playing Movies': tmdb.now_playing_movies,
        'Upcoming Movies': tmdb.upcoming_movies, 
        'Top Rated Movies': tmdb.toprated_movies,
        'Popular Shows': tmdb.popular_shows,
        'Top Rated Shows': tmdb.top_rated_shows,
        'On the Air Shows': tmdb.on_the_air_shows
    }
    titles = [x for x in items.keys()]
    links = [x for x in items.values()]
    icon = tmdb.addon_path + 'resources/artwork/tmdb.jpg'
    media_type = 'movie'
    for x in range(len(items)):
        if '/movie/' in links[x]:
            media_type = 'movie'
        elif '/tv/' in links[x]:
            media_type = 'tv'
        tmdb.add_dir(titles[x], links[x], 'tmdb_router', icon, icon, '', media_type=media_type)