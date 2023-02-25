# -*- coding=utf8 -*-
#******************************************************************************
# Config.py
#------------------------------------------------------------------------------
#
# Copyright (c) 2014-2015 LivingOn <LivingOn@xmail.net>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#******************************************************************************
import xbmc

class Config(object):
    "Die wichtigsten Konfigurationsparameter zusammengefasst."
    
    PLUGIN_NAME    = "plugin.video.chaturbate"
    CHATURBATE_URL = "https://de.chaturbate.com/"

    CHATURBATE_URL_FEATURED    = CHATURBATE_URL 
    CHATURBATE_URL_WEIBLICH    = CHATURBATE_URL + "female-cams/"
    CHATURBATE_URL_MAENNLICH   = CHATURBATE_URL + "male-cams/"
    CHATURBATE_URL_PAAR        = CHATURBATE_URL + "couple-cams/"
    CHATURBATE_URL_TRANSSEXUAL = CHATURBATE_URL + "trans-cams/"

    CHATURBATE_URL_FEATURED_TAGS    = CHATURBATE_URL + "tags/"
    CHATURBATE_URL_WEIBLICH_TAGS    = CHATURBATE_URL + "tags/female/"
    CHATURBATE_URL_MAENNLICH_TAGS   = CHATURBATE_URL + "tags/male/"
    CHATURBATE_URL_PAAR_TAGS        = CHATURBATE_URL + "tags/couple/"
    CHATURBATE_URL_TRANSSEXUAL_TAGS = CHATURBATE_URL + "tags/transsexual/"

    SCRIPT_SETTINGS = "settings.py"
    SCRIPT_INSERT_FAVORITE = "insert_actor.py"
    SCRIPT_REMOVE_FAVORITE = "remove_actor.py"

    FAVORITS_DB = xbmc.translatePath(
        "special://profile/addon_data/%s/Favorits.db" % PLUGIN_NAME
    )

    M3U8_PATTERN = "(https:[^>\s]+?.m3u8)"

    CHUNK_PLAYER_PORT = 18517