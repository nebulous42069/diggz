import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import os

#TMDbH Check
trakt_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.themoviedb.helper/')
trakt_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.themoviedb.helper/settings.xml') 
first_check = xbmcvfs.translatePath('special://userdata/addon_data/plugin.program.chef20/trakt/tmdbhelper_trakt')
second_check = xbmcaddon.Addon('plugin.video.themoviedb.helper').getSetting("trakt_token")
third_check = xbmcaddon.Addon('plugin.video.themoviedb.helper').getSetting("trakt_token")
backup_file_save = xbmcvfs.translatePath('special://userdata/addon_data/plugin.program.chef20/trakt/tmdbhelper_trakt')
check = str(second_check)

#Account Mananger API Keys
check_api = f'4a479b95c8224999eef8d418cfe6c7a4389e2837441672c48c9c8168ea42a407'
client_am = f'4a479b95c8224999eef8d418cfe6c7a4389e2837441672c48c9c8168ea42a407'
secret_am = f'89d8f8f71b312985a9e1f91e9eb426e23050102734bb1fa36ec76cdc74452ab6'
std_client_am = f"'4a479b95c8224999eef8d418cfe6c7a4389e2837441672c48c9c8168ea42a407'"
std_secret_am = f"'89d8f8f71b312985a9e1f91e9eb426e23050102734bb1fa36ec76cdc74452ab6'"

#Account Mananger Check
check_myaccts = xbmcaddon.Addon('script.module.myaccts').getSetting("trakt.token")
check_myaccts_rd = xbmcaddon.Addon('script.module.myaccts').getSetting("realdebrid.token")
check_myaccts_pm = xbmcaddon.Addon('script.module.myaccts').getSetting("premiumize.token")
check_myaccts_ad = xbmcaddon.Addon('script.module.myaccts').getSetting("alldebrid.token")

#Add-on Paths
check_addon_seren = xbmcvfs.translatePath('special://home/addons/plugin.video.seren/')
check_addon_fen = xbmcvfs.translatePath('special://home/addons/plugin.video.fen/')
check_addon_ezra = xbmcvfs.translatePath('special://home/addons/plugin.video.ezra/')
check_addon_pov = xbmcvfs.translatePath('special://home/addons/plugin.video.pov/')
check_addon_umb = xbmcvfs.translatePath('special://home/addons/plugin.video.umbrella/')
check_addon_home = xbmcvfs.translatePath('special://home/addons/plugin.video.homelander/')
check_addon_genocide = xbmcvfs.translatePath('special://home/addons/plugin.video.chainsgenocide/')
check_addon_crew = xbmcvfs.translatePath('special://home/addons/plugin.video.thecrew/')
check_addon_shazam = xbmcvfs.translatePath('special://home/addons/plugin.video.shazam/')
check_addon_night = xbmcvfs.translatePath('special://home/addons/plugin.video.nightwing/')
check_addon_promise = xbmcvfs.translatePath('special://home/addons/plugin.video.thepromise/')
check_addon_scrubs = xbmcvfs.translatePath('special://home/addons/plugin.video.scrubsv2/')
check_addon_alvin = xbmcvfs.translatePath('special://home/addons/plugin.video.alvin/')
check_addon_shadow = xbmcvfs.translatePath('special://home/addons/plugin.video.shadow/')
check_addon_ghost = xbmcvfs.translatePath('special://home/addons/plugin.video.ghost/')
check_addon_unleashed = xbmcvfs.translatePath('special://home/addons/plugin.video.unleashed/')
check_addon_chains = xbmcvfs.translatePath('special://home/addons/plugin.video.thechains/')
check_addon_md = xbmcvfs.translatePath('special://home/addons/plugin.video.magicdragon/')
check_addon_asgard = xbmcvfs.translatePath('special://home/addons/plugin.video.asgard/')
check_addon_moria = xbmcvfs.translatePath('special://home/addons/plugin.video.moria/')
check_addon_base = xbmcvfs.translatePath('special://home/addons/plugin.video.base19/')
check_addon_twisted = xbmcvfs.translatePath('special://home/addons/plugin.video.twisted/')
check_addon_metv = xbmcvfs.translatePath('special://home/addons/plugin.video.metv19/')
check_addon_premiumizer = xbmcvfs.translatePath('special://home/addons/plugin.video.premiumizerx/')
check_addon_realizer = xbmcvfs.translatePath('special://home/addons/plugin.video.realizerx/')
check_addon_rurl= xbmcvfs.translatePath('special://home/addons/script.module.resolveurl/')
check_addon_myaccounts = xbmcvfs.translatePath('special://home/addons/script.module.myaccounts/')
check_addon_tmdbh = xbmcvfs.translatePath('special://home/addons/plugin.video.themoviedb.helper/')
check_addon_trakt = xbmcvfs.translatePath('special://home/addons/script.trakt/')

#Add-on settings.xml Paths
check_seren_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.seren/settings.xml')
check_fen_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.fen/settings.xml')
check_ezra_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.ezra/settings.xml')
check_pov_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.pov/settings.xml')
check_umb_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.umbrella/settings.xml')
check_home_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.homelander/settings.xml')
check_genocide_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.chainsgenocide/settings.xml')
check_crew_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.thecrew/settings.xml')
check_shazam_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.shazam/settings.xml')
check_night_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.nightwing/settings.xml')
check_promise_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.thepromise/settings.xml')
check_scrubs_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.scrubsv2/settings.xml')
check_alvin_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.alvin/settings.xml')
check_shadow_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.shadow/settings.xml')
check_ghost_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.ghost/settings.xml')
check_unleashed_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.unleashed/settings.xml')
check_chains_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.thechains/settings.xml')
check_md_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.magicdragon/settings.xml')
check_asgard_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.asgard/settings.xml')
check_moria_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.moria/settings.xml')
check_base_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.base19/settings.xml')
check_twisted_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.twisted/settings.xml')
check_metv_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.metv19/settings.xml')
check_premiumizer_settings= xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.premiumizerx/settings.xml')
check_realizer_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.realizerx/rdauth.json')
check_rurl_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.ghost/settings.xml')
check_myaccounts_settings = xbmcvfs.translatePath('special://userdata/addon_data/script.module.myaccounts/settings.xml')
check_tmdbh_settings = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.themoviedb.helper/settings.xml')
check_trakt_settings = xbmcvfs.translatePath('special://userdata/addon_data/script.trakt/settings.xml')

#Add-on API Key Paths
client_keys_seren = xbmcvfs.translatePath('special://home/addons/plugin.video.seren/resources/lib/indexers/trakt.py')
client_keys_fen = xbmcvfs.translatePath('special://home/addons/plugin.video.fen/resources/lib/apis/trakt_api.py')
client_keys_pov = xbmcvfs.translatePath('special://home/addons/plugin.video.pov/resources/lib/apis/trakt_api.py')
client_keys_umb = xbmcvfs.translatePath('special://home/addons/plugin.video.umbrella/resources/lib/modules/trakt.py')
client_keys_home = xbmcvfs.translatePath('special://home/addons/plugin.video.homelander/resources/lib/modules/trakt.py')
client_keys_genocide = xbmcvfs.translatePath('special://home/addons/plugin.video.chainsgenocide/resources/lib/modules/trakt.py')
client_keys_crew = xbmcvfs.translatePath('special://home/addons/script.module.thecrew/lib/resources/lib/modules/trakt.py')
client_keys_shazam = xbmcvfs.translatePath('special://home/addons/plugin.video.shazam/resources/lib/modules/trakt.py')
client_keys_night = xbmcvfs.translatePath('special://home/addons/plugin.video.nightwing/resources/lib/modules/trakt.py')
client_keys_home = xbmcvfs.translatePath('special://home/addons/plugin.video.homelander/resources/lib/modules/trakt.py')
client_keys_promise = xbmcvfs.translatePath('special://home/addons/plugin.video.thepromise/resources/lib/modules/trakt.py')
client_keys_scrubs = xbmcvfs.translatePath('special://home/addons/plugin.video.scrubsv2/resources/lib/modules/trakt.py')
client_keys_alvin = xbmcvfs.translatePath('special://home/addons/plugin.video.alvin/resources/lib/modules/trakt.py')
client_keys_shadow = xbmcvfs.translatePath('special://home/addons/plugin.video.shadow/resources/modules/general.py')
client_keys_ghost = xbmcvfs.translatePath('special://home/addons/plugin.video.ghost/resources/modules/general.py')
client_keys_unleashed = xbmcvfs.translatePath('special://home/addons/plugin.video.unleashed/resources/modules/general.py')
client_keys_chains = xbmcvfs.translatePath('special://home/addons/plugin.video.thechains/resources/modules/general.py')
client_keys_md = xbmcvfs.translatePath('special://home/addons/plugin.video.magicdragon/resources/modules/general.py')
client_keys_asgard = xbmcvfs.translatePath('special://home/addons/plugin.video.asgard/resources/modules/general.py')
client_keys_myaccounts = xbmcvfs.translatePath('special://home/addons/script.module.myaccounts/lib/myaccounts/modules/trakt.py')
client_keys_tmdbh = xbmcvfs.translatePath('special://home/addons/plugin.video.themoviedb.helper/resources/tmdbhelper/lib/api/api_keys/trakt.py')
client_keys_trakt = xbmcvfs.translatePath('special://home/addons/script.trakt/resources/lib/traktapi.py')

#Add-on API Keys
std_client = f'api_keys.trakt_client_id'
std_secret = f'api_keys.trakt_secret'
seren_client = f'0c9a30819e4af6ffaf3b954cbeae9b54499088513863c03c02911de00ac2de79'
seren_secret = f'bf02417f27b514cee6a8d135f2ddc261a15eecfb6ed6289c36239826dcdd1842'
fen_client = f'645b0f46df29d27e63c4a8d5fff158edd0bef0a6a5d32fc12c1b82388be351af'
fen_secret = f'422a282ef5fe4b5c47bc60425c009ac3047ebd10a7f6af790303875419f18f98'
pov_client = f'd4161a7a106424551add171e5470112e4afdaf2438e6ef2fe0548edc75924868'
pov_secret = f'b5fcd7cb5d9bb963784d11bbf8535bc0d25d46225016191eb48e50792d2155c0'
umb_client = f'87e3f055fc4d8fcfd96e61a47463327ca877c51e8597b448e132611c5a677b13'
umb_secret = f'4a1957a52d5feb98fafde53193e51f692fa9bdcd0cc13cf44a5e39975539edf0'
crew_client = f'482f9db52ee2611099ce3aa1abf9b0f7ed893c6d3c6b5face95164eac7b01f71'
crew_secret = f'80a2729728b53ba1cc38137b22f21f34d590edd35454466c4b8920956513d967'
night_client = f'base64.b64decode("MjFiODhkNGRjZDU4ZjVlY2EzOTEyOGE3MzZkMjIxNmRhNTZiNTIxMTQ4MDUyNThjNGU5ZjlhNjNkOTgwMDcyMg==")'
night_secret = f'base64.b64decode("MjM4OGIzMDdkZDFiYTU0NGQ2ZmEwZTFmNTcxNDczNWJkNTIwYzhmZTM4ZGYyMTEyZDg4ODg1MmJhODE1YWRlOQ==")'
scrubs_client = f'63c53edc299b7a05cc6ea2272e8a84e13aade067c18a794362ab9a4a84eafb16'
scrubs_secret = f'9163ebda9d33acd06c74d017e861404b7212ee34675e09e73365d7536b84eab6'
shadow_client = f'8ed545c0b7f92cc26d1ecd6326995c6cf0053bd7596a98e962a472bee63274e6'
shadow_secret = f'1ec4f37e5743e3086abace0c83444c25d9b655d1d77b793806b2c8205a510426'
ghost_client = f'a4e716b4b22b62e59b9e09454435c8710b650b3143dcce553d252b6a66ba60c8'
ghost_secret = f'c6d9aba72214a1ca3c6d45d0351e59f21bbe43df9bbac7c5b740089379f8c5cd'
unleashed_client = f'19849909a0f8c9dc632bc5f5c7ccafd19f3e452e2e44fee05b83fd5dc1e77675'
unleashed_secret = f'122b7a79437dcf4b657d3af9e92f2d9ff8939ade532e03bc81bfb5ce798b04bf'
chains_client = f'19849909a0f8c9dc632bc5f5c7ccafd19f3e452e2e44fee05b83fd5dc1e77675'
chains_secret = f'122b7a79437dcf4b657d3af9e92f2d9ff8939ade532e03bc81bfb5ce798b04bf'
md_client = f'8ed545c0b7f92cc26d1ecd6326995c6cf0053bd7596a98e962a472bee63274e6'
md_secret = f'1ec4f37e5743e3086abace0c83444c25d9b655d1d77b793806b2c8205a510426'
asgard_client = f'54de56f7b90a4cf7227fd70ecf703c6c043ec135c56ad10c9bb90c539bf2749f'
asgard_secret = f'a43aa6bd62eb5afd37ede4a625457fc903f1961b8384178986bf76eebfcd5999'
myacts_client = f'e3a8d1c673dfecb7f669b23ecbf77c75fcfd24d3e8c3dbc7f79ed995262fa1db'
myacts_secret = f'73bee6aeee29cb75db4d8771458a440017f7cfe842e85f457ed9d81f7910b349'
tmdbh_client = f'e6fde6173adf3c6af8fd1b0694b9b84d7c519cefc24482310e1de06c6abe5467'
tmdbh_secret = f'15119384341d9a61c751d8d515acbc0dd801001d4ebe85d3eef9885df80ee4d9'
trakt_client = f'd4161a7a106424551add171e5470112e4afdaf2438e6ef2fe0548edc75924868'
trakt_secret = f'b5fcd7cb5d9bb963784d11bbf8535bc0d25d46225016191eb48e50792d2155c0'
