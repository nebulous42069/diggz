import xbmc
from .plugin2 import Myaddon


class Tools(Myaddon):
    
    def log(self, message: str):
        return xbmc.log(message, xbmc.LOGINFO)
    
    def color_text(self, color: str, txt: str):
        return(f'[B][COLOR {color}]{txt}[/COLOR][/B]')
    
    def kodi_builtin(self, string: str):
        return(xbmc.executebuiltin(string))
    
    def write_to_file(self, file_path: str, _string: str):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(_string)
    
    def append_lists(self, lists1: list, lists2: list):
        for _list in lists2:
            lists1.append(_list)
        return lists1

tools = Tools()