import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import os

addon_id = 'script.module.accountmgr'
addon = xbmcaddon.Addon(addon_id)
setting = addon.getSetting

def traktID():
        traktId = '4a479b95c8224999eef8d418cfe6c7a4389e2837441672c48c9c8168ea42a407'
        if (setting('trakt.client.id') != '' or setting('trakt.client.id') is not None) and setting('traktuserkey.enabled') == 'true':
                traktId = setting('trakt.client.id')
        return traktId
def traktSecret():
        traktSecret = '89d8f8f71b312985a9e1f91e9eb426e23050102734bb1fa36ec76cdc74452ab6'
        if (setting('trakt.client.secret') != '' or setting('trakt.client.secret') is not None) and setting('traktuserkey.enabled') == 'true':
                traktSecret = setting('trakt.client.secret')
        return traktSecret

#Account Mananger API Keys
client_am = traktID()
secret_am = traktSecret()

#Account Mananger Trakt & Debrid Token Check
chk_api = traktID()
chk_accountmgr_tk = xbmcaddon.Addon('script.module.accountmgr').getSetting("trakt.token")
chk_accountmgr_tk_rd = xbmcaddon.Addon('script.module.accountmgr').getSetting("realdebrid.token")
chk_accountmgr_tk_pm = xbmcaddon.Addon('script.module.accountmgr').getSetting("premiumize.token")
chk_accountmgr_tk_ad = xbmcaddon.Addon('script.module.accountmgr').getSetting("alldebrid.token")

#Account Manager Meta Account API Check
chk_accountmgr_fanart = xbmcaddon.Addon('script.module.accountmgr').getSetting("fanart.tv.api.key")
chk_accountmgr_omdb = xbmcaddon.Addon('script.module.accountmgr').getSetting("omdb.api.key")
chk_accountmgr_mdb = xbmcaddon.Addon('script.module.accountmgr').getSetting("mdb.api.key")
chk_accountmgr_imdb = xbmcaddon.Addon('script.module.accountmgr').getSetting("imdb.user")
chk_accountmgr_tmdb = xbmcaddon.Addon('script.module.accountmgr').getSetting("tmdb.api.key")
chk_accountmgr_tmdb_user = xbmcaddon.Addon('script.module.accountmgr').getSetting("tmdb.username")
chk_accountmgr_tmdb_pass = xbmcaddon.Addon('script.module.accountmgr').getSetting("tmdb.password")
chk_accountmgr_tmdb_session = xbmcaddon.Addon('script.module.accountmgr').getSetting("tmdb.session_id")
chk_accountmgr_tvdb = xbmcaddon.Addon('script.module.accountmgr').getSetting("tvdb.api.key")
chk_accountmgr_trakt = xbmcaddon.Addon('script.module.accountmgr').getSetting("trakt.api.key")

#Account Manager Scraper Check
chk_accountmgr_furk = xbmcaddon.Addon('script.module.accountmgr').getSetting("furk.password")
chk_accountmgr_easy = xbmcaddon.Addon('script.module.accountmgr').getSetting("easynews.password")
chk_accountmgr_file = xbmcaddon.Addon('script.module.accountmgr').getSetting("filepursuit.api.key")

#Add-on Paths
chk_seren = xbmcvfs.translatePath('special://home/addons/plugin.video.seren/')
chk_fen = xbmcvfs.translatePath('special://home/addons/plugin.video.fen/')
chk_ezra = xbmcvfs.translatePath('special://home/addons/plugin.video.ezra/')
chk_coal = xbmcvfs.translatePath('special://home/addons/plugin.video.coalition/')
chk_pov = xbmcvfs.translatePath('special://home/addons/plugin.video.pov/')
chk_umb = xbmcvfs.translatePath('special://home/addons/plugin.video.umbrella/')
chk_shadow = xbmcvfs.translatePath('special://home/addons/plugin.video.shadow/')
chk_ghost = xbmcvfs.translatePath('special://home/addons/plugin.video.ghost/')
chk_base = xbmcvfs.translatePath('special://home/addons/plugin.video.base19/')
chk_unleashed = xbmcvfs.translatePath('special://home/addons/plugin.video.unleashed/')
chk_chains = xbmcvfs.translatePath('special://home/addons/plugin.video.thechains/')
chk_twisted = xbmcvfs.translatePath('special://home/addons/plugin.video.twisted/')
chk_md = xbmcvfs.translatePath('special://home/addons/plugin.video.magicdragon/')
chk_asgard = xbmcvfs.translatePath('special://home/addons/plugin.video.asgard/')
chk_patriot = xbmcvfs.translatePath('special://home/addons/plugin.video.patriot/')
chk_blackl = xbmcvfs.translatePath('special://home/addons/plugin.video.blacklightning/')
chk_metv = xbmcvfs.translatePath('special://home/addons/plugin.video.metv19/')
chk_aliunde = xbmcvfs.translatePath('special://home/addons/plugin.video.aliundek19/')
chk_home = xbmcvfs.translatePath('special://home/addons/plugin.video.homelander/')
chk_quick = xbmcvfs.translatePath('special://home/addons/plugin.video.quicksilver/')
chk_genocide = xbmcvfs.translatePath('special://home/addons/plugin.video.chainsgenocide/')
chk_absol = xbmcvfs.translatePath('special://home/addons/plugin.video.absolution/')
chk_shazam = xbmcvfs.translatePath('special://home/addons/plugin.video.shazam/')
chk_crew = xbmcvfs.translatePath('special://home/addons/plugin.video.thecrew/')
chk_night = xbmcvfs.translatePath('special://home/addons/plugin.video.nightwing/')
chk_alvin = xbmcvfs.translatePath('special://home/addons/plugin.video.alvin/')
chk_moria = xbmcvfs.translatePath('special://home/addons/plugin.video.moria/')
chk_nine = xbmcvfs.translatePath('special://home/addons/plugin.video.nine/')
chk_scrubs = xbmcvfs.translatePath('special://home/addons/plugin.video.scrubsv2/')
chk_myaccounts = xbmcvfs.translatePath('special://home/addons/script.module.myaccounts/')
chk_rurl= xbmcvfs.translatePath('special://home/addons/script.module.resolveurl/')
chk_tmdbh = xbmcvfs.translatePath('special://home/addons/plugin.video.themoviedb.helper/')
chk_trakt = xbmcvfs.translatePath('special://home/addons/script.trakt/')
chk_embuary = xbmcvfs.translatePath('special://home/addons/script.embuary.info/')
chk_meta = xbmcvfs.translatePath('special://home/addons/script.module.metahandler/')
chk_pvr = xbmcvfs.translatePath('special://home/addons/script.module.pvr.artwork/')

#Add-on settings.xml Paths
chkset_seren = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.seren/settings.xml')
chkset_fen = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.fen/settings.xml')
chkset_ezra = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.ezra/settings.xml')
chkset_coal = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.coalition/settings.xml')
chkset_pov = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.pov/settings.xml')
chkset_umb = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.umbrella/settings.xml')
chkset_shadow = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.shadow/settings.xml')
chkset_ghost = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.ghost/settings.xml')
chkset_base = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.base19/settings.xml')
chkset_unleashed = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.unleashed/settings.xml')
chkset_chains = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.thechains/settings.xml')
chkset_twisted = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.twisted/settings.xml')
chkset_md = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.magicdragon/settings.xml')
chkset_asgard = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.asgard/settings.xml')
chkset_patriot = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.patriot/settings.xml')
chkset_blackl = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.blacklightning/settings.xml')
chkset_metv = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.metv19/settings.xml')
chkset_aliunde = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.aliundek19/settings.xml')
chkset_home = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.homelander/settings.xml')
chkset_quick = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.quicksilver/settings.xml')
chkset_genocide = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.chainsgenocide/settings.xml')
chkset_absol = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.absolution/settings.xml')
chkset_shazam = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.shazam/settings.xml')
chkset_crew = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.thecrew/settings.xml')
chkset_night = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.nightwing/settings.xml')
chkset_alvin = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.alvin/settings.xml')
chkset_moria = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.moria/settings.xml')
chkset_nine = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.nine/settings.xml')
chkset_scrubs = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.scrubsv2/settings.xml')
chkset_myaccounts = xbmcvfs.translatePath('special://userdata/addon_data/script.module.myaccounts/settings.xml')
chkset_rurl = xbmcvfs.translatePath('special://userdata/addon_data/script.module.resolveurl/settings.xml')
chkset_tmdbh = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.themoviedb.helper/settings.xml')
chkset_trakt = xbmcvfs.translatePath('special://userdata/addon_data/script.trakt/settings.xml')
chkset_embuary = xbmcvfs.translatePath('special://userdata/addon_data/script.embuary.info/settings.xml')
chkset_meta = xbmcvfs.translatePath('special://userdata/addon_data/script.module.metahandler/settings.xml')
chkset_pvr = xbmcvfs.translatePath('special://userdata/addon_data/script.module.pvr.artwork/settings.xml')

#Add-on API Key Paths
path_seren = xbmcvfs.translatePath('special://home/addons/plugin.video.seren/resources/lib/indexers/trakt.py')
path_fen = xbmcvfs.translatePath('special://home/addons/plugin.video.fen/resources/lib/apis/trakt_api.py')
path_coal = xbmcvfs.translatePath('special://home/addons/plugin.video.coalition/resources/lib/apis/trakt_api.py')
path_pov = xbmcvfs.translatePath('special://home/addons/plugin.video.pov/resources/lib/apis/trakt_api.py')
path_shadow = xbmcvfs.translatePath('special://home/addons/plugin.video.shadow/resources/modules/general.py')
path_ghost = xbmcvfs.translatePath('special://home/addons/plugin.video.ghost/resources/modules/general.py')
path_base = xbmcvfs.translatePath('special://home/addons/plugin.video.base19/resources/modules/general.py')
path_unleashed = xbmcvfs.translatePath('special://home/addons/plugin.video.unleashed/resources/modules/general.py')
path_chains = xbmcvfs.translatePath('special://home/addons/plugin.video.thechains/resources/modules/general.py')
path_md = xbmcvfs.translatePath('special://home/addons/plugin.video.magicdragon/resources/modules/general.py')
path_asgard = xbmcvfs.translatePath('special://home/addons/plugin.video.asgard/resources/modules/general.py')
path_patriot = xbmcvfs.translatePath('special://home/addons/plugin.video.patriot/resources/modules/general.py')
path_blackl = xbmcvfs.translatePath('special://home/addons/plugin.video.blacklightning/resources/modules/general.py')
path_aliunde = xbmcvfs.translatePath('special://home/addons/plugin.video.aliundek19/resources/modules/general.py')
path_crew = xbmcvfs.translatePath('special://home/addons/script.module.thecrew/lib/resources/lib/modules/trakt.py')
path_scrubs = xbmcvfs.translatePath('special://home/addons/plugin.video.scrubsv2/resources/lib/modules/trakt.py')
path_myaccounts = xbmcvfs.translatePath('special://home/addons/script.module.myaccounts/lib/myaccounts/modules/trakt.py')
path_tmdbh = xbmcvfs.translatePath('special://home/addons/plugin.video.themoviedb.helper/resources/tmdbhelper/lib/api/api_keys/trakt.py')
path_trakt = xbmcvfs.translatePath('special://home/addons/script.trakt/resources/lib/traktapi.py')

#Metadata
ezra_fan = 'fe073550acf157bdb8a4217f215c0882'
ezra_tmdb = '05a454b451f2f9003fbca293744e4a85'
fen_fan = 'fa836e1c874ba95ab08a14ee88e05565'
fen_tmdb = 'b370b60447737762ca38457bd77579b3'
coal_fan = '598515b970d81280063107d49d0e2558"'
coal_tmdb = '74f3ce931d65ebda1f77ef24eac2625f'
pov_fan = 'fe073550acf157bdb8a4217f215c0882'
pov_tmdb = 'a07324c669cac4d96789197134ce272b'
home_fan = 'c3469c1cc9465b9f1a1a862feea8b76b'
home_tmdb = 'fb981e5ab89415bba616409d5eb5f05e'
crew_fan = '27bef29779bbffe947232dc310a91f0c'
crew_tmdb = '0049795edb57568b95240bc9e61a9dfc'

#Trakt
seren_client = '0c9a30819e4af6ffaf3b954cbeae9b54499088513863c03c02911de00ac2de79'
seren_secret = 'bf02417f27b514cee6a8d135f2ddc261a15eecfb6ed6289c36239826dcdd1842'
fen_client = '645b0f46df29d27e63c4a8d5fff158edd0bef0a6a5d32fc12c1b82388be351af'
fen_secret = '422a282ef5fe4b5c47bc60425c009ac3047ebd10a7f6af790303875419f18f98'
coal_client = '19849909a0f8c9dc632bc5f5c7ccafd19f3e452e2e44fee05b83fd5dc1e77675'
coal_secret = 'b5fcd7cb5d9bb963784d11bbf8535bc0d25d46225016191eb48e50792d2155c0'
pov_client = 'd4161a7a106424551add171e5470112e4afdaf2438e6ef2fe0548edc75924868'
pov_secret = 'b5fcd7cb5d9bb963784d11bbf8535bc0d25d46225016191eb48e50792d2155c0'
shadow_client = '8ed545c0b7f92cc26d1ecd6326995c6cf0053bd7596a98e962a472bee63274e6'
shadow_secret = '1ec4f37e5743e3086abace0c83444c25d9b655d1d77b793806b2c8205a510426'
ghost_client = 'a4e716b4b22b62e59b9e09454435c8710b650b3143dcce553d252b6a66ba60c8'
ghost_secret = 'c6d9aba72214a1ca3c6d45d0351e59f21bbe43df9bbac7c5b740089379f8c5cd'
base_client = f'76578d23add0005f9b723fd66f97f1eb0e226f3fac55a3127baaa78e6ed5b303'
base_secret = f'7110290e5ecf935c1a3ffb3e6410e34cef5d732ef59dbdb141cef2846c8bd227'
unleashed_client = '19849909a0f8c9dc632bc5f5c7ccafd19f3e452e2e44fee05b83fd5dc1e77675'
unleashed_secret = '122b7a79437dcf4b657d3af9e92f2d9ff8939ade532e03bc81bfb5ce798b04b'
chains_client = '19849909a0f8c9dc632bc5f5c7ccafd19f3e452e2e44fee05b83fd5dc1e77675'
chains_secret = '122b7a79437dcf4b657d3af9e92f2d9ff8939ade532e03bc81bfb5ce798b04b'
md_client = '8ed545c0b7f92cc26d1ecd6326995c6cf0053bd7596a98e962a472bee63274e6'
md_secret = '1ec4f37e5743e3086abace0c83444c25d9b655d1d77b793806b2c8205a510426'
asgard_client = '54de56f7b90a4cf7227fd70ecf703c6c043ec135c56ad10c9bb90c539bf2749'
asgard_secret = 'a43aa6bd62eb5afd37ede4a625457fc903f1961b8384178986bf76eebfcd5999'
patriot_client = '5085635871955f48506576375bf736293c4833d491beca8d962c9da45125b63c'
patriot_secret = '2400cb3da2a3cc1f74b53c43793de8f97e6ea867a5639c8f0b0bde606c067e41'
blackl_client = 'cddec5a35d5d39a8b1e189d8f012dc5046880b8f1bbd67fc2e3b14de1b374b5b'
blackl_secret = '1b4b51a3595d03155813a057a566f32c4c37f2a77bd7888c207d85f31687b57f'
aliunde_client = '4d6fbe175e32115ca9117c3b7c55bf46b53f69f90c232d79869ec32f0dd470a6'
aliunde_secret = '6c27014354629b345dbe4b4028ff5956489ee5cb7e7e5857454bcd24430c91ac'
crew_client = '482f9db52ee2611099ce3aa1abf9b0f7ed893c6d3c6b5face95164eac7b01f71'
crew_secret = '80a2729728b53ba1cc38137b22f21f34d590edd35454466c4b8920956513d967'
scrubs_client = '63c53edc299b7a05cc6ea2272e8a84e13aade067c18a794362ab9a4a84eafb16'
scrubs_secret = '9163ebda9d33acd06c74d017e861404b7212ee34675e09e73365d7536b84eab6'
myacts_client = 'e3a8d1c673dfecb7f669b23ecbf77c75fcfd24d3e8c3dbc7f79ed995262fa1db'
myacts_secret = '73bee6aeee29cb75db4d8771458a440017f7cfe842e85f457ed9d81f7910b349'
tmdbh_client = 'e6fde6173adf3c6af8fd1b0694b9b84d7c519cefc24482310e1de06c6abe5467'
tmdbh_secret = '15119384341d9a61c751d8d515acbc0dd801001d4ebe85d3eef9885df80ee4d9'
trakt_client = 'd4161a7a106424551add171e5470112e4afdaf2438e6ef2fe0548edc75924868'
trakt_secret = 'b5fcd7cb5d9bb963784d11bbf8535bc0d25d46225016191eb48e50792d2155c0'
