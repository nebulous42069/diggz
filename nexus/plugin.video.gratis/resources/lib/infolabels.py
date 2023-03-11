import requests
import json
from base64 import b64decode
from .db import DB


class Infolabels:
    def __init__(self, video_info: dict, media_type: str, tv_id: int = None, season_number: int = None, episode_number: int = None):
        self.video_info = video_info
        self.media_type = media_type
        self.tv_id = tv_id
        self.season_number = season_number
        self.episode_number = episode_number
        self.images_path = 'https://image.tmdb.org/t/p/original'
        self.api_key = b64decode('NmE1YmU0OTk5YWJmNzRlYmExZjlhODMxMTI5NGMyNjc=').decode('utf-8')
    
    def tvshow_url(self, tv_id: int):
        return f'https://api.themoviedb.org/3/tv/{tv_id}?api_key={self.api_key}&language=en-US&append_to_response=videos,credits,release_dates,content_ratings,external_ids'
    
    def season_url(self, tv_id: int, season_number: int):
        return f'https://api.themoviedb.org/3/tv/{tv_id}/season/{season_number}?api_key={self.api_key}&language=en-US'
    
    def episode_url(self, tv_id: int, season_number: int, episode_number: int):
        return f'https://api.themoviedb.org/3/tv/{tv_id}/season/{season_number}/episode/{episode_number}?api_key={self.api_key}&language=en-US&append_to_response=videos,credits,release_dates'
    
    def yt_link(self, video_id: int):
        return f'plugin://plugin.video.youtube/play/?video_id={video_id}'
    
    def get_cast(self):
        cast = []
        if self.video_info.get('credits'):
            cast_list = self.video_info['credits'].get('cast')
            if cast_list:
                for actor in cast_list:
                    cast.append(
                        {
                            'name': actor.get('name', ''),
                            'role': actor.get('character', ''),
                            'thumbnail': f"{self.images_path}{actor.get('profile_path', '')}"
                        }
                    )
        return cast
    
    def get_thumbnail(self):
        thumb = self.video_info.get("poster_path")
        if not thumb:
            return ""
        return self.images_path + thumb
        
    
    def get_fanart(self):
        fanart = self.video_info.get("backdrop_path")
        if not fanart:
            return ""
        return self.images_path + fanart
    
    def get_title(self):
        return self.video_info.get('title', self.video_info.get('name', 'Unknown Title'))
    
    def get_plot(self):
        return self.video_info.get('overview', '')
    
    def get_tagline(self):
        return self.video_info.get('tagline', '')
    
    def get_premiered(self):
        return self.video_info.get('release_date', self.video_info.get('first_air_date', self.video_info.get('air_date', '')))
    
    def get_rating(self):
        return self.video_info.get('vote_average', 0)
    
    def get_votes(self):
        return self.video_info.get('vote_count', '')
    
    def get_genre(self):
        if self.video_info.get('genres'):
            return [genra.get('name', '') for genra in self.video_info.get('genres', [])]
        return ''
    
    def get_mpaa(self):
        mpaa_results = self.video_info.get('release_dates', self.video_info.get('content_ratings'))
        if mpaa_results:
            mpaa_results = mpaa_results.get('results')
            if mpaa_results:
                for releases in mpaa_results:
                    if releases.get('iso_3166_1') == 'US':
                        if self.media_type == 'tv':
                            return releases.get('rating', '')
                        elif self.media_type == 'movie':
                            for release in releases['release_dates']:
                                if release.get('certification'):
                                    return release.get('certification', '')
            return ''
    
    def get_crew(self):
        if self.video_info.get('crew'):
            return self.video_info['crew']
        elif self.video_info.get('credits'):
            if self.video_info['credits'].get('crew'):
                return self.video_info['credits']['crew']
        return ''
    
    def get_director(self):
        crew = self.get_crew()
        if crew:
            director = []
            for job in crew:
                if job['job'] == 'Director':
                    director.append(job['name'])
            return director
        return ''
    
    def get_writer(self):
        crew = self.get_crew()
        if crew:
            writer = []
            for job in crew:
                if job['job'] == 'Writer' or job['job'] == 'Screenplay' or job.get('known_for_department') == 'Writing':
                    writer.append(job['name'])
            return writer
        return ''
    
    def get_studio(self):
        if self.video_info.get('production_companies', self.video_info.get('networks')):
            if self.media_type == 'movie':
                studio = [studio['name'] for studio in self.video_info.get('production_companies', [])]
            else:
                studio = [studio['name'] for studio in self.video_info['networks']]
                for company in self.video_info['production_companies']:
                    studio.append(company['name'])
            return studio
        return ''
    
    def get_country(self):
        if self.video_info.get('production_countries'):
            return [country.get('name', '') for country in self.video_info['production_countries']]
        return ''
    
    def get_set(self):
        if self.video_info.get('belongs_to_collection'):
            return self.video_info['belongs_to_collection'].get('name', '')
        return ''
    
    def get_status(self):
        return self.video_info.get('status', '')
    
    def get_duration(self):
        duration = self.video_info.get('runtime', self.video_info.get('episode_run_time', 0))
        if duration:
            if type(duration) == list:
                return duration[0] * 60
            else:
                return duration * 60
        return 0
    
    def get_imdb_id(self):
        ids = self.video_info.get('external_ids')
        if ids:
            return ids.get('imdb_id', '')
        if self.video_info.get('imdb_id'):
            return self.video_info.get('imdb_id', '')
        return ''
        
    
    def get_trailer(self):
        videos = self.video_info.get('videos')
        if videos:
            for video in videos.get('results', []):
                if video.get('type') == 'Trailer':
                    video_id = video.get('key')
                    if video_id:
                        return self.yt_link(video_id)
            for video in videos.get('results', []):
                if video['type'] == 'Teaser':
                    video_id = video['key']
                    return self.yt_link(video_id)
        return ''
    
    def get_episode(self):
        item = {}
        if self.tv_id:
            tv_from_db =  DB('tv')
        
            query = tv_from_db.get(self.tv_id)
            if query:
                item = json.loads(query[0])
                print(f'item= {item}')
        if item:
            tv_infolabels = item.get('infolabels')
            tv_cast = item.get('cast')
        else:
            tv_info = requests.get(self.tvshow_url(self.tv_id)).json()
            tv = Infolabels(tv_info, 'tv')
            tv_infolabels, tv_cast = tv.infolabels_and_cast()
        
        response = self.video_info
        if not response:
            if self.tv_id and self.season_number and self.episode_number:
                url = self.episode_url(self.tv_id, self.season_number, self.episode_number)
                response = requests.get(url).json()
            else:
                return {}, []
            
        ep = Infolabels(response, 'episode')
        episode_infolabels = tv_infolabels
        episode_infolabels['mediatype'] = 'episode'
        #episode_infolabels['title'] = ep.get_title()
        episode_infolabels['plot'] = ep.get_plot()
        episode_infolabels['duration'] = ep.get_duration()
        episode_infolabels['premiered'] = ep.get_premiered()
        cast = tv_cast
        guest_stars = response.get('guest_stars')
        if guest_stars:
           for actor in guest_stars:
                cast.append({"name": actor['name'], "role": actor['character'], "thumbnail": f"{self.images_path}{actor['profile_path']}"})
                        
        episode_infolabels['director'] = ep.get_director()
        episode_infolabels['writer'] = ep.get_writer()
        print(f'Episode {self.episode_number}:')
        return episode_infolabels, cast
        
    
    def get_infolabels(self):
        if self.media_type == 'episode':
            return self.get_episode()
                        
        title = self.get_title()
        plot = self.get_plot()
        tagline = self.get_tagline()
        premiered = self.get_premiered()
        genre = self.get_genre()
        mpaa = self.get_mpaa()
        director = self.get_director()
        writer = self.get_writer()
        rating = self. get_rating()
        votes = self.get_votes()
        studio = self.get_studio()
        country = self.get_country()
        _set = self.get_set()
        status = self.get_status()
        duration = self.get_duration()
        trailer = self.get_trailer()
            
        if self.media_type == 'tv':
            mediatype = 'tvshow'
        else:
            mediatype = self.media_type
        
        return {
            "mediatype": mediatype,
            "title": title,
            "plot": plot,
            "tagline": tagline,
            "premiered": premiered,
            "genre": genre,
            "mpaa": mpaa,
            "director": director,
            "writer": writer,
            "rating": rating,
            "votes": votes,
            "studio": studio,
            "country": country,
            "set": _set,
            "status": status,
            "duration": duration,
            "trailer": trailer
        }
    
    def infolabels_and_cast(self):
        if self.media_type == 'episode':
            return self.get_episode()
        else:
            return self.get_infolabels(), self.get_cast()