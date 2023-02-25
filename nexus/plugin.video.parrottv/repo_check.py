# Credits: madtitan

import os
import sys
import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon
import sqlite3
import hashlib
from glob import glob

DB_PATH = xbmcvfs.translatePath('special://home/userdata/Database/')
DB_FILE = glob(DB_PATH + 'Addons*.db')[0]
DEV_FILE = "special://home/addons/"+xbmcaddon.Addon().getAddonInfo('id')+"/.dev"
MY_ADDON = xbmcaddon.Addon().getAddonInfo('id')
SAFE_REPOS = ['repository.test']  # list of allowed repos, keep the empty quotes to allow addon to be installed from zip file
MESSAGE = 'This addon was installed by an unofficial repository.\nYou can get official one in https://parrot.ulti.eu.org/\nInvite Only!'  # change to whatever you want

def get_origin(addon_id: str):
    response = ''
    try:
        con = sqlite3.connect(DB_FILE)
        cursor = con.cursor()
        cursor.execute('SELECT origin FROM installed WHERE addonID = ?', (addon_id,))
        response = cursor.fetchone()
    except sqlite3.Error as e:
        xbmc.log('%s: There was an error reading the database - %s' % (xbmcaddon.Addon().getAddonInfo('name'), e), xbmc.LOGINFO)
        return ''
    finally:
        try:
            if con:
                con.close()
        except UnboundLocalError as e:
            xbmc.log('%s: There was an error connecting to the database - %s' % (xbmcaddon.Addon().getAddonInfo('name'), e), xbmc.LOGINFO)
    if type(response) == tuple:
        return  response[0]
    return response

def repo_check():
    if sys.platform == "linux": return
    if os.path.exists(xbmcvfs.translatePath(DEV_FILE)) and hashlib.sha256(open(xbmcvfs.translatePath(DEV_FILE), 'r').read().encode()).hexdigest() == "6ee8da0002462f91912e293070e90faf4e817453b0a54d686f2d771cf840601f": return

    if not get_origin(MY_ADDON) in SAFE_REPOS:
        xbmcgui.Dialog().ok(xbmcaddon.Addon().getAddonInfo('name'), MESSAGE)
        quit()