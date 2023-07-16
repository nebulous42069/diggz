import xbmc, xbmcaddon, xbmcgui
import xbmcvfs
import os

def seren():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.seren/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.seren/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = '0'
        addon = xbmcaddon.Addon("plugin.video.seren")
        addon.setSetting("general.maxResolution", res)
	
def fen():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.fen/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.fen/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = 'SD, 720p, 1080p, 4K'
        addon = xbmcaddon.Addon("plugin.video.fen")
        addon.setSetting("results_quality_movie", res)
        addon.setSetting("results_quality_episode", res)
        addon.setSetting("autoplay_quality_movie", res)
        addon.setSetting("autoplay_quality_episode", res)

def pov():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.pov/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.pov/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = 'SD, 720p, 1080p, 4K'
        addon = xbmcaddon.Addon("plugin.video.pov")
        addon.setSetting("results_quality_movie", res)
        addon.setSetting("results_quality_episode", res)
        addon.setSetting("autoplay_quality_movie", res)
        addon.setSetting("autoplay_quality_episode", res)

def ezra():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.ezra/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.ezra/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = 'SD, 720p, 1080p, 4K'
        addon = xbmcaddon.Addon("plugin.video.ezra")
        addon.setSetting("results_quality_movie", res)
        addon.setSetting("results_quality_episode", res)
        addon.setSetting("autoplay_quality_movie", res)
        addon.setSetting("autoplay_quality_episode", res)

def ghost():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.ghost/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.ghost/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = '2'
        addon = xbmcaddon.Addon("plugin.video.ghost")
        addon.setSetting("max_q", res)
        addon.setSetting("max_q_tv", res)
	
def shadow():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.shadow/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.shadow/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = '2'
        addon = xbmcaddon.Addon("plugin.video.shadow")
        addon.setSetting("max_q", res)
        addon.setSetting("max_q_tv", res)
	
def thechains():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.thechains/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.thechains/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = '2'
        addon = xbmcaddon.Addon("plugin.video.thechains")
        addon.setSetting("max_q", res)
        addon.setSetting("max_q_tv", res)
	
def unleashed():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.unleashed/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.unleashed/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = '2'
        addon = xbmcaddon.Addon("plugin.video.unleashed")
        addon.setSetting("max_q", res)
        addon.setSetting("max_q_tv", res)
	
def twisted():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.twisted/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.twisted/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = '2'
        addon = xbmcaddon.Addon("plugin.video.twisted")
        addon.setSetting("max_q", res)
        addon.setSetting("max_q_tv", res)
	
def base19():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.base19/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.base19/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = '2'
        addon = xbmcaddon.Addon("plugin.video.base19")
        addon.setSetting("max_q", res)
        addon.setSetting("max_q_tv", res)
	
def metv19():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.metv19/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.metv19/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = '2'
        addon = xbmcaddon.Addon("plugin.video.metv19")
        addon.setSetting("max_q", res)
        addon.setSetting("max_q_tv", res)
	
def asgard():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.asgard/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.asgard/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = '2'
        addon = xbmcaddon.Addon("plugin.video.asgard")
        addon.setSetting("max_q", res)
        addon.setSetting("max_q_tv", res)

def magicdragon():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.magicdragon/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.magicdragon/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = '2'
        addon = xbmcaddon.Addon("plugin.video.magicdragon")
        addon.setSetting("max_q", res)
        addon.setSetting("max_q_tv", res)
	
def aliunde():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.aliundek19/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.aliundek19/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = '2'
        addon = xbmcaddon.Addon("plugin.video.aliundek19")
        addon.setSetting("max_q", res)
        addon.setSetting("max_q_tv", res)
	
def umbrella():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.umbrella/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.umbrella/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = '0'
        addon = xbmcaddon.Addon("plugin.video.umbrella")
        addon.setSetting("hosts.quality", res)
	
def homelander():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.homelander/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.homelander/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = '0'
        addon = xbmcaddon.Addon("plugin.video.homelander")
        addon.setSetting("hosts.quality", res)
	
def thecrew():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.thecrew/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.thecrew/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = '0'
        addon = xbmcaddon.Addon("plugin.video.thecrew")
        addon.setSetting("hosts.quality", res)

def nightwing():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.nightwing/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.nightwing/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = '0'
        addon = xbmcaddon.Addon("plugin.video.nightwing")
        addon.setSetting("hosts.quality", res)

def moria():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.moria/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.moria/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = '0'
        addon = xbmcaddon.Addon("plugin.video.moria")
        addon.setSetting("hosts.quality", res)

def thepromise():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.thepromise/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.thepromise/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = '0'
        addon = xbmcaddon.Addon("plugin.video.thepromise")
        addon.setSetting("hosts.quality", res)

def scrubs():
    addon = xbmcvfs.translatePath('special://home/addons/plugin.video.scrubsv2/')
    file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.scrubsv2/settings.xml')

    if xbmcvfs.exists(addon) and xbmcvfs.exists(file):

        res = '2'
        addon = xbmcaddon.Addon("plugin.video.scrubsv2")
        addon.setSetting("quality.max", res)



def hd_maxset_4k():
        seren()
        fen()
        pov()
        ezra()
        ghost()
        shadow()
        thechains()
        unleashed()
        twisted()
        base19()
        metv19()
        asgard()
        magicdragon()
        aliunde()
        umbrella()
        homelander()
        thecrew()
        nightwing()
        moria()
        thepromise()
        scrubs()
        xbmc.executebuiltin('dialog.close(all)')
        xbmc.executebuiltin('ActivateWindow(home)')
        xbmcgui.Dialog().ok('4K Quality Conversion', 'To save changes you now need to force close Kodi, Press OK to force close Kodi')
        os._exit(1)
exit
