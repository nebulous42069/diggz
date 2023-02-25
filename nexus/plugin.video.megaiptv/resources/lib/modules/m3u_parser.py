#Based on Playlist Loader by Avigdor
import requests, re
from . import addonvar
import json
from requests import Session

addon_icon = addonvar.addon_icon


class m3uRegex(object):

    def __init__(self,source):
        self.source = source
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        self.headers = {"User-Agent":self.user_agent, "Connection":'keep-alive', 'Accept':'audio/webm,audio/ogg,udio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5'}
        self.session = Session()
        self.session.headers.update(self.headers)


    def re_me(self,data, re_patten):
        match = ''
        m = re.search(re_patten, data)
        if m != None:
            match = m.group(1).decode('utf-8')
        else:
            match = ''
        return match

    def EpgRegex(self):
        m3udata = {}
        chId = 0
        content = self.session.get(self.source).content
        match = re.compile(rb'#EXTINF:(.+?),(.*?)[\n\r]+([^\n]+)').findall(content)
        for other,channel_name,stream_url in match:
            channel_name = channel_name.decode('utf-8')
            stream_url = stream_url.decode('utf-8')
            tvg_id='';tvg_name='';tvg_country='';tvg_language='';tvg_logo='';group_title=''
            if b'tvg-id' in other:
                tvg_id = self.re_me(other,b'tvg-id=[\'"](.*?)[\'"]')
            if b'tvg-name' in other:
                tvg_name = self.re_me(other,b'tvg-name=[\'"](.*?)[\'"]')
            if b'tvg-country' in other:
                tvg_country = self.re_me(other,b'tvg-country=[\'"](.*?)[\'"]')
            if b'tvg-language' in other:
                tvg_language = self.re_me(other,b'tvg-language=[\'"](.*?)[\'"]')
            if b'tvg-logo' in other:
                tvg_logo = self.re_me(other,b'tvg-logo=[\'"](.*?)[\'"]')
            if b'group-title' in other:
                group_title = self.re_me(other,b'group-title=[\'"](.*?)[\'"]')
            if group_title == '':
                if tvg_country != '':
                    group_title = tvg_country
                else:
                    group_title = 'noGroup'
            if tvg_name == '' and channel_name != '':
                tvg_name = channel_name
            if channel_name =='' and tvg_name !='':
                channel_name = tvg_name
            if tvg_id == '':
                tvg_id = f"{''.join(tvg_name.lower().split())}.{tvg_country}"
            chId += 1
            m3udata.update({chId:{"tvg_id":tvg_id,"tvg_name":tvg_name,"tvg_country":tvg_country,"tvg_language":tvg_language,"tvg_logo":tvg_logo,"group_title":group_title,"channel_name":channel_name,"stream_url":stream_url}})
        return json.dumps(m3udata, indent=4)


class m3u(object):

    def __init__(self,content):
        self.content = content

    def get_categories(self):
        return sorted(list(set(v.get('group_title') for k,v in json.loads(self.content).items())))

    
    def get_catlist(self, category):
        return list({k:v} for k,v in json.loads(self.content).items() if v.get('group_title')==category)
