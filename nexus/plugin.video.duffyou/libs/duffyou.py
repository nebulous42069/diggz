# -*- coding: utf-8 -*-
import plugin, re

def play(id, title="", plot="", thumb=""):
    if id.startswith('list='):
        id = '?' + id

    list = re.findall(r'[&?]list=([^&\s]+)', id)
    if list:
        plugin.reproducir_videos_playlist(plugin.Item(
            action='play',
            id=list[0],
            label=title,
            plot=plot,
            thumb=thumb
        ))
    else:
        plugin.play(plugin.Item(
                action='play',
                url=id,
                label=title,
                plot=plot,
                thumb=thumb
                ))

def resolver(id, title="", plot="", thumb=""):
    if id.startswith('list='):
        id = '?' + id

    list = re.findall(r'[&?]list=([^&\s]+)', id)
    if list:
        return plugin.resolver_playlist(
            plugin.Item(
                id=list[0],
                label=title,
                plot=plot,
                thumb=thumb
        ))
    else:
        ret = plugin.play(plugin.Item(
                action='resolver',
                url=id,
                label=title,
                plot=plot,
                thumb=thumb
                ))

        url, title, plot, thumb = ret
        return url, title, plot, thumb
