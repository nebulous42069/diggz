#   Kodi downloader
#   Copyright (C) 2018 Mucky Duck
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


import requests
import xbmcgui
import time


def download(url, destination, dp=None, headers=None, cookies=None,
             allow_redirects=True, verify=True, timeout=30, auth=None):
    if not dp:
        dp = xbmcgui.DialogProgressBG()
        dp.create('Download')
    try:
        with open(destination, 'wb') as f:
            start = time.time()
            r = requests.get(url, headers=headers, cookies=cookies,
                             allow_redirects=allow_redirects, verify=verify,
                             timeout=timeout, auth=auth, stream=True)
            content_length = int(r.headers.get('content-length'))
            if content_length is None:
                f.write(r.content)
            else:
                dl = 0
                for chunk in r.iter_content(chunk_size=content_length/100):
                    dl += len(chunk)
                    if chunk:
                        f.write(chunk)
                    progress = (dl * 100 / content_length)
                    byte_speed = dl / (time.time() - start)
                    kbps_speed = byte_speed / 1024
                    mbps_speed = kbps_speed / 1024
                    downloaded = float(dl) / (1024 * 1024)
                    file_size = float(content_length) / (1024 * 1024)
                    if byte_speed > 0:
                        eta = (content_length - dl) / byte_speed
                    else:
                        eta = 0
                    line1 = '[COLOR darkgoldenrod]%.1f Mb[/COLOR] Of [COLOR darkgoldenrod]%.1f Mb[/COLOR]' %(downloaded, file_size)
                    line2 = 'Speed: [COLOR darkgoldenrod]%.01f Mbps[/COLOR]' %mbps_speed
                    line2 += ' ETA: [COLOR darkgoldenrod]%02d:%02d[/COLOR]' %divmod(eta, 60)
                    dp.update(progress, f'{line1}\n{line2}')
            dp.close()
    except:
        dp.close()
        xbmcgui.Dialog().ok('Error', 'Sorry something went wrong please try again')
    
            
    