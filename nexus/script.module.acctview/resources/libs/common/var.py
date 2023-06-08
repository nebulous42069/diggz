import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import os

addon_id = 'script.module.accountmgr'
addon = xbmcaddon.Addon(addon_id)
setting = addon.getSetting

#Account Mananger API Keys
client_am = f'4a479b95c8224999eef8d418cfe6c7a4389e2837441672c48c9c8168ea42a407'
secret_am = f'89d8f8f71b312985a9e1f91e9eb426e23050102734bb1fa36ec76cdc74452ab6'

#Account Mananger Check
chk_accountmgr_tk = xbmcaddon.Addon('script.module.accountmgr').getSetting("trakt.token")
chk_accountmgr_tk_rd = xbmcaddon.Addon('script.module.accountmgr').getSetting("realdebrid.token")
chk_accountmgr_tk_pm = xbmcaddon.Addon('script.module.accountmgr').getSetting("premiumize.token")
chk_accountmgr_tk_ad = xbmcaddon.Addon('script.module.accountmgr').getSetting("alldebrid.token")

#Add-on Paths
chk_seren = xbmcvfs.translatePath('special://home/addons/plugin.video.seren/')
chk_fen = xbmcvfs.translatePath('special://home/addons/plugin.video.fen/')
chk_ezra = xbmcvfs.translatePath('special://home/addons/plugin.video.ezra/')
chk_pov = xbmcvfs.translatePath('special://home/addons/plugin.video.pov/')
chk_umb = xbmcvfs.translatePath('special://home/addons/plugin.video.umbrella/')
chk_home = xbmcvfs.translatePath('special://home/addons/plugin.video.homelander/')
chk_quick = xbmcvfs.translatePath('special://home/addons/plugin.video.quicksilver/')
chk_genocide = xbmcvfs.translatePath('special://home/addons/plugin.video.chainsgenocide/')
chk_crew = xbmcvfs.translatePath('special://home/addons/plugin.video.thecrew/')
chk_shazam = xbmcvfs.translatePath('special://home/addons/plugin.video.shazam/')
chk_night = xbmcvfs.translatePath('special://home/addons/plugin.video.nightwing/')
chk_promise = xbmcvfs.translatePath('special://home/addons/plugin.video.thepromise/')
chk_scrubs = xbmcvfs.translatePath('special://home/addons/plugin.video.scrubsv2/')
chk_alvin = xbmcvfs.translatePath('special://home/addons/plugin.video.alvin/')
chk_shadow = xbmcvfs.translatePath('special://home/addons/plugin.video.shadow/')
chk_ghost = xbmcvfs.translatePath('special://home/addons/plugin.video.ghost/')
chk_unleashed = xbmcvfs.translatePath('special://home/addons/plugin.video.unleashed/')
chk_chains = xbmcvfs.translatePath('special://home/addons/plugin.video.thechains/')
chk_md = xbmcvfs.translatePath('special://home/addons/plugin.video.magicdragon/')
chk_asgard = xbmcvfs.translatePath('special://home/addons/plugin.video.asgard/')
chk_moria = xbmcvfs.translatePath('special://home/addons/plugin.video.moria/')
chk_base = xbmcvfs.translatePath('special://home/addons/plugin.video.base19/')
chk_twisted = xbmcvfs.translatePath('special://home/addons/plugin.video.twisted/')
chk_metv = xbmcvfs.translatePath('special://home/addons/plugin.video.metv19/')
chk_premiumizer = xbmcvfs.translatePath('special://home/addons/plugin.video.premiumizerx/')
chk_realizer = xbmcvfs.translatePath('special://home/addons/plugin.video.realizerx/')
chk_rurl= xbmcvfs.translatePath('special://home/addons/script.module.resolveurl/')
chk_myaccounts = xbmcvfs.translatePath('special://home/addons/script.module.myaccounts/')
chk_tmdbh = xbmcvfs.translatePath('special://home/addons/plugin.video.themoviedb.helper/')
chk_trakt = xbmcvfs.translatePath('special://home/addons/script.trakt/')

#Add-on API Key Paths
path_fen = xbmcvfs.translatePath('special://home/addons/plugin.video.fen/resources/lib/apis/trakt_api.py')
path_pov = xbmcvfs.translatePath('special://home/addons/plugin.video.pov/resources/lib/apis/trakt_api.py')
path_crew = xbmcvfs.translatePath('special://home/addons/script.module.thecrew/lib/resources/lib/modules/trakt.py')
path_shadow = xbmcvfs.translatePath('special://home/addons/plugin.video.shadow/resources/modules/general.py')
path_ghost = xbmcvfs.translatePath('special://home/addons/plugin.video.ghost/resources/modules/general.py')
path_base = xbmcvfs.translatePath('special://home/addons/plugin.video.base19/resources/modules/general.py')
path_unleashed = xbmcvfs.translatePath('special://home/addons/plugin.video.unleashed/resources/modules/general.py')
path_chains = xbmcvfs.translatePath('special://home/addons/plugin.video.thechains/resources/modules/general.py')
path_md = xbmcvfs.translatePath('special://home/addons/plugin.video.magicdragon/resources/modules/general.py')
path_asgard = xbmcvfs.translatePath('special://home/addons/plugin.video.asgard/resources/modules/general.py')
path_scrubs = xbmcvfs.translatePath('special://home/addons/plugin.video.scrubsv2/resources/lib/modules/trakt.py')
path_myaccounts = xbmcvfs.translatePath('special://home/addons/script.module.myaccounts/lib/myaccounts/modules/trakt.py')
path_tmdbh = xbmcvfs.translatePath('special://home/addons/plugin.video.themoviedb.helper/resources/tmdbhelper/lib/api/api_keys/trakt.py')
path_trakt = xbmcvfs.translatePath('special://home/addons/script.trakt/resources/lib/traktapi.py')

#Add-on API Keys
fen_client = f'645b0f46df29d27e63c4a8d5fff158edd0bef0a6a5d32fc12c1b82388be351af'
fen_secret = f'422a282ef5fe4b5c47bc60425c009ac3047ebd10a7f6af790303875419f18f98'
pov_client = f'd4161a7a106424551add171e5470112e4afdaf2438e6ef2fe0548edc75924868'
pov_secret = f'b5fcd7cb5d9bb963784d11bbf8535bc0d25d46225016191eb48e50792d2155c0'
crew_client = f'482f9db52ee2611099ce3aa1abf9b0f7ed893c6d3c6b5face95164eac7b01f71'
crew_secret = f'80a2729728b53ba1cc38137b22f21f34d590edd35454466c4b8920956513d967'
shadow_client = f'8ed545c0b7f92cc26d1ecd6326995c6cf0053bd7596a98e962a472bee63274e6'
shadow_secret = f'1ec4f37e5743e3086abace0c83444c25d9b655d1d77b793806b2c8205a510426'
ghost_client = f'a4e716b4b22b62e59b9e09454435c8710b650b3143dcce553d252b6a66ba60c8'
ghost_secret = f'c6d9aba72214a1ca3c6d45d0351e59f21bbe43df9bbac7c5b740089379f8c5cd'
base_client = f'76578d23add0005f9b723fd66f97f1eb0e226f3fac55a3127baaa78e6ed5b303'
base_secret = f'7110290e5ecf935c1a3ffb3e6410e34cef5d732ef59dbdb141cef2846c8bd227'
unleashed_client = f'19849909a0f8c9dc632bc5f5c7ccafd19f3e452e2e44fee05b83fd5dc1e77675'
unleashed_secret = f'122b7a79437dcf4b657d3af9e92f2d9ff8939ade532e03bc81bfb5ce798b04bf'
chains_client = f'19849909a0f8c9dc632bc5f5c7ccafd19f3e452e2e44fee05b83fd5dc1e77675'
chains_secret = f'122b7a79437dcf4b657d3af9e92f2d9ff8939ade532e03bc81bfb5ce798b04bf'
md_client = f'8ed545c0b7f92cc26d1ecd6326995c6cf0053bd7596a98e962a472bee63274e6'
md_secret = f'1ec4f37e5743e3086abace0c83444c25d9b655d1d77b793806b2c8205a510426'
asgard_client = f'54de56f7b90a4cf7227fd70ecf703c6c043ec135c56ad10c9bb90c539bf2749f'
asgard_secret = f'a43aa6bd62eb5afd37ede4a625457fc903f1961b8384178986bf76eebfcd5999'
scrubs_client = f'63c53edc299b7a05cc6ea2272e8a84e13aade067c18a794362ab9a4a84eafb16'
scrubs_secret = f'9163ebda9d33acd06c74d017e861404b7212ee34675e09e73365d7536b84eab6'
myacts_client = f'e3a8d1c673dfecb7f669b23ecbf77c75fcfd24d3e8c3dbc7f79ed995262fa1db'
myacts_secret = f'73bee6aeee29cb75db4d8771458a440017f7cfe842e85f457ed9d81f7910b349'
tmdbh_client = f'e6fde6173adf3c6af8fd1b0694b9b84d7c519cefc24482310e1de06c6abe5467'
tmdbh_secret = f'15119384341d9a61c751d8d515acbc0dd801001d4ebe85d3eef9885df80ee4d9'
trakt_client = f'd4161a7a106424551add171e5470112e4afdaf2438e6ef2fe0548edc75924868'
trakt_secret = f'b5fcd7cb5d9bb963784d11bbf8535bc0d25d46225016191eb48e50792d2155c0'
