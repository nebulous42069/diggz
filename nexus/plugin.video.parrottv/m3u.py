# -*- coding: utf-8 -*-
# Author: Parrot Developers
# License: MPL 2.0 https://www.mozilla.org/en-US/MPL/2.0/

import io
import random
import xbmcvfs
import xbmcaddon

_ADDON = xbmcaddon.Addon()

def genID():
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choice(alphabet) for i in range(30))

def parse(reqs):
    file = xbmcvfs.translatePath('special://home/addons/'+_ADDON.getAddonInfo('id')+'/resources/playlist.m3u')
    m3ufile = io.open(file, 'r', encoding='utf-8').read()
    names, logos, urls, ids, groups = [], [], [], [], []
    for line in m3ufile.split('\n'):
        if '#EXTINF:' in line:
            names.append(line.split(',')[1])
            logos.append(line.split('tvg-logo="')[1].split('"')[0])
            try:
                ids.append(line.split('tvg-id="')[1].split('"')[0])
            except:
                ids.append("")
            groups.append(line.split('group-title="')[1].split('"')[0])
        elif 'plugin' in line:
            urls.append(line)
    return eval(reqs)