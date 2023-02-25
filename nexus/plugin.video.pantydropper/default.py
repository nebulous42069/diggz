import xbmc, xbmcaddon, os, audrey, xbmcvfs
addon=xbmcaddon.Addon()
home=xbmcvfs.translatePath(addon.getAddonInfo("path"))
audrey.feedme(os.path.join(home, "sites.json"), "file")