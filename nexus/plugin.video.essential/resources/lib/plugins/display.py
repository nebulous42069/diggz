from ..plugin import Plugin
from xbmcplugin import addDirectoryItems, endOfDirectory, setContent
from ..DI import DI
import sys

route_plugin = DI.plugin


class display(Plugin):
    name = "display"

    def display_list(self, jen_list):
        display_list2=[]
        for item in jen_list:
            display_list2 .append((route_plugin.url_for_path(item["link"]), item["list_item"], item["is_dir"]))
        mediatype=item.get("mediatype","videos")
        if mediatype=="movie":
            mediatype="movies"
        addDirectoryItems(route_plugin.handle, display_list2, len(display_list2))
        setContent(int(sys.argv[1]), mediatype) 
        endOfDirectory(route_plugin.handle)
        return True
