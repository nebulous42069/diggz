import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import os
addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon = xbmcaddon.Addon(addon_id)
setting = addon.getSetting

#Account Mananger Check
chk_accountmgr_tk = xbmcaddon.Addon('script.module.accountmgr').getSetting("trakt.token")
chk_accountmgr_tk_rd = xbmcaddon.Addon('script.module.accountmgr').getSetting("realdebrid.token")
chk_accountmgr_tk_pm = xbmcaddon.Addon('script.module.accountmgr').getSetting("premiumize.token")
chk_accountmgr_tk_ad = xbmcaddon.Addon('script.module.accountmgr').getSetting("alldebrid.token")
