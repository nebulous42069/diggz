"""
    Tubi Add-on
    Developed by mhancoc7
    https://patreon.m7kodi.dev

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from resources.lib.modules.channels import *

import xbmcplugin

mode = Tubi().plugin_queries['mode']

if location_check() != "US":
    dlg.ok(addon_name, get_string(9005))
    exit()

if mode == "main":
    patreon_notify()
    Channels.section_list()

elif "tubitv-content" in mode:
    Channels.content_list(mode)

elif "tubitv-episodes" in mode:
    Channels.episode_list(mode)

elif "play-tubitv" in mode:
    Channels.play_tubi(mode)

elif mode == "tubitv-search":
    Channels.search_tubi()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
