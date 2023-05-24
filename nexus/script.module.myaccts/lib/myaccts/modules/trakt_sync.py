import xbmc, xbmcaddon, xbmcgui
import os
import xbmcvfs
from pathlib import Path
from myaccts.modules import var

#Seren Trakt
def seren_trakt():

        if xbmcvfs.exists(var.check_addon_seren) and xbmcvfs.exists(var.check_seren_settings): #Check that the addon is installed and settings.xml exists.
                check_seren = xbmcaddon.Addon('plugin.video.seren').getSetting("trakt.auth")                
                if str(var.check_myaccts) != str(check_seren): #Compare Account Mananger token to Add-on token. If they match, authorization is skipped
                
                        #Insert Account Mananger API keys into add-on
                        f = open(var.client_keys_seren,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.seren_client,var.client_am).replace(var.seren_secret,var.secret_am)
                        f = open(var.client_keys_seren,'w')
                        f.write(client)
                        f.close()

                        #Write trakt data to the add-ons settings.xml
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("plugin.video.seren")

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt.auth", your_token)

                        your_username = myaccts.getSetting("trakt.username")
                        addon.setSetting("trakt.username", your_username)
                        
                        your_refresh = myaccts.getSetting("trakt.refresh")
                        addon.setSetting("trakt.refresh", your_refresh)
                        
                        your_expires = myaccts.getSetting("trakt.expires")
                        your_expires_float = float(your_expires)
                        your_expires_rnd = int(your_expires_float)
                        your_expires_str = str(your_expires_rnd)
                        addon.setSetting("trakt.expires", your_expires_str)

#Fen
def fen_trakt():
    
        if xbmcvfs.exists(var.check_addon_fen) and xbmcvfs.exists(var.check_fen_settings):
                check_fen = xbmcaddon.Addon('plugin.video.fen').getSetting("trakt.token")
                if str(var.check_myaccts) != str(check_fen):
                        
                        f = open(var.client_keys_fen,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.fen_client,var.client_am).replace(var.fen_secret,var.secret_am)
                        f = open(var.client_keys_fen,'w')
                        f.write(client)
                        f.close()

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("plugin.video.fen")

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt.token", your_token)

                        your_username = myaccts.getSetting("trakt.username")
                        addon.setSetting("trakt.user", your_username)
                        
                        your_refresh = myaccts.getSetting("trakt.refresh")
                        addon.setSetting("trakt.refresh", your_refresh)

                        your_expires = myaccts.getSetting("trakt.expires")
                        addon.setSetting("trakt.expires", your_expires)

                        addon.setSetting("trakt.indicators_active", 'true')
                        addon.setSetting("watched.indicators", '1')

#Ezra
def ezra_trakt():
                
        if xbmcvfs.exists(var.check_addon_ezra) and xbmcvfs.exists(var.check_ezra_settings):
                check_ezra = xbmcaddon.Addon('plugin.video.ezra').getSetting("trakt.token")
                if str(var.check_myaccts) != str(check_ezra):

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("plugin.video.ezra")

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt.token", your_token)

                        your_username = myaccts.getSetting("trakt.username")
                        addon.setSetting("trakt_user", your_username)
                        
                        your_expires = myaccts.getSetting("trakt.expires")
                        addon.setSetting("trakt.expires", your_expires)
                
#POV
def pov_trakt():
 
        if xbmcvfs.exists(var.check_addon_pov) and xbmcvfs.exists(var.check_pov_settings):
                check_pov = xbmcaddon.Addon('plugin.video.pov').getSetting("trakt.token")
                if str(var.check_myaccts) != str(check_pov):

                        f = open(var.client_keys_pov,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.pov_client,var.client_am).replace(var.pov_client,var.secret_am)
                        f = open(var.client_keys_pov,'w')
                        f.write(client)
                        f.close()

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("plugin.video.pov")

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt.token", your_token)

                        your_username = myaccts.getSetting("trakt.username")
                        addon.setSetting("trakt_user", your_username)
                        
                        your_refresh = myaccts.getSetting("trakt.refresh")
                        addon.setSetting("trakt.refresh", your_refresh)

                        your_expires = myaccts.getSetting("trakt.expires")
                        addon.setSetting("trakt.expires", your_expires)

                        addon.setSetting("trakt.indicators_active", 'true')
                        addon.setSetting("watched.indicators", '1')              

#Umbrella
def umb_trakt():
                
        if xbmcvfs.exists(var.check_addon_umb) and xbmcvfs.exists(var.check_umb_settings):
                check_umb = xbmcaddon.Addon('plugin.video.umbrella').getSetting("trakt.user.token")
                if str(var.check_myaccts) != str(check_umb):

                        f = open(var.client_keys_umb,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.umb_client,var.client_am).replace(var.umb_secret,var.secret_am)
                        f = open(var.client_keys_umb,'w')
                        f.write(client)
                        f.close()

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("plugin.video.umbrella")

                        your_username = myaccts.getSetting("trakt.username")
                        addon.setSetting("trakt.user.name", your_username)

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt.user.token", your_token)

                        your_refresh = myaccts.getSetting("trakt.refresh")
                        addon.setSetting("trakt.refreshtoken", your_refresh)

                        your_secret = myaccts.getSetting("trakt.expires")
                        addon.setSetting("trakt.token.expires", your_secret)
                
#Homelander
def home_trakt():
                
        if xbmcvfs.exists(var.check_addon_home) and xbmcvfs.exists(var.check_home_settings):
                check_home = xbmcaddon.Addon('plugin.video.homelander').getSetting("trakt.token")
                if str(var.check_myaccts) != str(check_home):

                        f = open(var.client_keys_home,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                        f = open(var.client_keys_home,'w')
                        f.write(client)
                        f.close()

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("plugin.video.homelander")

                        your_username = myaccts.getSetting("trakt.username")
                        addon.setSetting("trakt.user", your_username)

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt.token", your_token)

                        your_refresh = myaccts.getSetting("trakt.refresh")
                        addon.setSetting("trakt.refresh", your_refresh)

                        addon.setSetting("trakt.authed", 'yes')

#Chains Genocide
def genocide_trakt():
                
        if xbmcvfs.exists(var.check_addon_genocide) and xbmcvfs.exists(var.check_genocide_settings):
                check_genocide = xbmcaddon.Addon('plugin.video.chainsgenocide').getSetting("trakt.token")
                if str(var.check_myaccts) != str(check_genocide):

                        f = open(var.client_keys_genocide,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                        f = open(var.client_keys_genocide,'w')
                        f.write(client)
                        f.close()

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("plugin.video.chainsgenocide")

                        your_username = myaccts.getSetting("trakt.username")
                        addon.setSetting("trakt.user", your_username)

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt.token", your_token)

                        your_refresh = myaccts.getSetting("trakt.refresh")
                        addon.setSetting("trakt.refresh", your_refresh)

                        addon.setSetting("trakt.authed", 'yes')
                        
#The Crew
def crew_trakt():

        if xbmcvfs.exists(var.check_addon_crew) and xbmcvfs.exists(var.check_crew_settings):
                check_crew = xbmcaddon.Addon('plugin.video.thecrew').getSetting("trakt.token")
                if str(var.check_myaccts) != str(check_crew):

                        f = open(var.client_keys_crew,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.crew_client,var.client_am).replace(var.crew_client,var.secret_am)
                        f = open(var.client_keys_crew,'w')
                        f.write(client)
                        f.close()

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("plugin.video.thecrew")

                        your_username = myaccts.getSetting("trakt.username")
                        addon.setSetting("trakt.user", your_username)

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt.token", your_token)

                        your_refresh = myaccts.getSetting("trakt.refresh")
                        addon.setSetting("trakt.refresh", your_refresh)

#Shazam
def shazam_trakt():
        
        if xbmcvfs.exists(var.check_addon_shazam) and xbmcvfs.exists(var.check_shazam_settings):
                check_shazam = xbmcaddon.Addon('plugin.video.shazam').getSetting("trakt.token")
                if str(var.check_myaccts) != str(check_shazam):

                        f = open(var.client_keys_shazam,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                        f = open(var.client_keys_shazam,'w')
                        f.write(client)
                        f.close()

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("plugin.video.shazam")

                        your_username = myaccts.getSetting("trakt.username")
                        addon.setSetting("trakt.user", your_username)

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt.token", your_token)

                        your_refresh = myaccts.getSetting("trakt.refresh")
                        addon.setSetting("trakt.refresh", your_refresh)

                        addon.setSetting("trakt.authed", 'yes')

#Nightwing
def night_trakt():
       
        if xbmcvfs.exists(var.check_addon_night) and xbmcvfs.exists(var.check_night_settings):
                check_night = xbmcaddon.Addon('plugin.video.nightwing').getSetting("trakt.token")
                if str(var.check_myaccts) != str(check_night):

                        f = open(var.client_keys_night,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.night_client,var.std_client_am).replace(var.night_secret,var.std_secret_am)
                        f = open(var.client_keys_night,'w')
                        f.write(client)
                        f.close()
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("plugin.video.nightwing")

                        your_username = myaccts.getSetting("trakt.username")
                        addon.setSetting("trakt.user", your_username)

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt.token", your_token)

                        your_refresh = myaccts.getSetting("trakt.refresh")
                        addon.setSetting("trakt.refresh", your_refresh)

                        addon.setSetting("trakt.authed", 'yes')

#The Promise
def promise_trakt():
       
        if xbmcvfs.exists(var.check_addon_promise) and xbmcvfs.exists(var.check_promise_settings):
                check_promise = xbmcaddon.Addon('plugin.video.thepromise').getSetting("trakt.token")
                if str(var.check_myaccts) != str(check_promise):

                        f = open(var.client_keys_promise,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                        f = open(var.client_keys_promise,'w')
                        f.write(client)
                        f.close()
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("plugin.video.thepromise")

                        your_username = myaccts.getSetting("trakt.username")
                        addon.setSetting("trakt.user", your_username)

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt.token", your_token)

                        your_refresh = myaccts.getSetting("trakt.refresh")
                        addon.setSetting("trakt.refresh", your_refresh)

                        addon.setSetting("trakt.authed", 'yes')

#Scrubs V2
def scrubs_trakt():
                
        if xbmcvfs.exists(var.check_addon_scrubs) and xbmcvfs.exists(var.check_scrubs_settings):
                check_scrubs = xbmcaddon.Addon('plugin.video.scrubsv2').getSetting("trakt.token")
                if str(var.check_myaccts) != str(check_scrubs):

                        f = open(var.client_keys_scrubs,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.scrubs_client,var.client_am).replace(var.scrubs_secret,var.secret_am)
                        f = open(var.client_keys_scrubs,'w')
                        f.write(client)
                        f.close()

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("plugin.video.scrubsv2")

                        your_username = myaccts.getSetting("trakt.username")
                        addon.setSetting("trakt.user", your_username)

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt.token", your_token)

                        your_refresh = myaccts.getSetting("trakt.refresh")
                        addon.setSetting("trakt.refresh", your_refresh)

                        addon.setSetting("trakt.authed", 'yes')

#Alvin
def alvin_trakt():
                
        if xbmcvfs.exists(var.check_addon_alvin) and xbmcvfs.exists(var.check_alvin_settings):
                check_alvin = xbmcaddon.Addon('plugin.video.alvin').getSetting("trakt.token")
                if str(var.check_myaccts) != str(check_alvin):

                        f = open(var.client_keys_alvin,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                        f = open(var.client_keys_alvin,'w')
                        f.write(client)
                        f.close()

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("plugin.video.alvin")

                        your_username = myaccts.getSetting("trakt.username")
                        addon.setSetting("trakt.user", your_username)

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt.token", your_token)

                        your_refresh = myaccts.getSetting("trakt.refresh")
                        addon.setSetting("trakt.refresh", your_refresh)

                        addon.setSetting("trakt.authed", 'yes')

#Shadow Trakt
def shadow_trakt():
                
        if xbmcvfs.exists(var.check_addon_shadow) and xbmcvfs.exists(var.check_shadow_settings):
                check_shadow = xbmcaddon.Addon('plugin.video.shadow').getSetting("trakt_access_token")
                if str(var.check_myaccts) != str(check_shadow):
                        
                        f = open(var.client_keys_shadow,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.shadow_client,var.client_am).replace(var.shadow_secret,var.secret_am)
                        f = open(var.client_keys_shadow,'w')
                        f.write(client)
                        f.close()

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("plugin.video.shadow")

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt_access_token", your_token)

                        your_refresh = myaccts.getSetting("trakt.refresh")
                        addon.setSetting("trakt_refresh_token", your_refresh)

                        your_expires = myaccts.getSetting("trakt.expires")
                        addon.setSetting("trakt_expires_at", your_expires)
                        
#Ghost Trakt
def ghost_trakt():
                
        if xbmcvfs.exists(var.check_addon_ghost) and xbmcvfs.exists(var.check_ghost_settings):
                check_ghost = xbmcaddon.Addon('plugin.video.ghost').getSetting("trakt_access_token")
                if str(var.check_myaccts) != str(check_ghost):
                        
                        f = open(var.client_keys_ghost,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.ghost_client,var.client_am).replace(var.ghost_secret,var.secret_am)
                        f = open(var.client_keys_ghost,'w')
                        f.write(client)
                        f.close()

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("plugin.video.ghost")

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt_access_token", your_token)

                        your_refresh = myaccts.getSetting("trakt.refresh")
                        addon.setSetting("trakt_refresh_token", your_refresh)

                        your_expires = myaccts.getSetting("trakt.expires")
                        addon.setSetting("trakt_expires_at", your_expires)

#Unleashed Trakt
def unleashed_trakt():
                
        if xbmcvfs.exists(var.check_addon_unleashed) and xbmcvfs.exists(var.check_unleashed_settings):
                check_unleashed = xbmcaddon.Addon('plugin.video.unleashed').getSetting("trakt_access_token")
                if str(var.check_myaccts) != str(check_unleashed):
                        
                        f = open(var.client_keys_unleashed,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.unleashed_client,var.client_am).replace(var.unleashed_secret,var.secret_am)
                        f = open(var.client_keys_unleashed,'w')
                        f.write(client)
                        f.close()

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("plugin.video.unleashed")

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt_access_token", your_token)

                        your_refresh = myaccts.getSetting("trakt.refresh")
                        addon.setSetting("trakt_refresh_token", your_refresh)

                        your_expires = myaccts.getSetting("trakt.expires")
                        addon.setSetting("trakt_expires_at", your_expires)

#Chain Reaction Trakt
def chains_trakt():
                
        if xbmcvfs.exists(var.check_addon_chains) and xbmcvfs.exists(var.check_chains_settings):
                check_thechains = xbmcaddon.Addon('plugin.video.thechains').getSetting("trakt_access_token")
                if str(var.check_myaccts) != str(check_thechains):
                        
                        f = open(var.client_keys_chains,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.chains_client,var.client_am).replace(var.chains_secret,var.secret_am)
                        f = open(var.client_keys_chains,'w')
                        f.write(client)
                        f.close()

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("plugin.video.thechains")

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt_access_token", your_token)

                        your_refresh = myaccts.getSetting("trakt.refresh")
                        addon.setSetting("trakt_refresh_token", your_refresh)

                        your_expires = myaccts.getSetting("trakt.expires")
                        addon.setSetting("trakt_expires_at", your_expires)

#Magic Dragon Trakt
def md_trakt():
               
        if xbmcvfs.exists(var.check_addon_md) and xbmcvfs.exists(var.check_md_settings):
                check_md = xbmcaddon.Addon('plugin.video.magicdragon').getSetting("trakt_access_token")
                if str(var.check_myaccts) != str(check_md):
                       
                        f = open(var.client_keys_md,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.md_client,var.client_am).replace(var.md_client,var.secret_am)
                        f = open(var.client_keys_md,'w')
                        f.write(client)
                        f.close()

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("plugin.video.magicdragon")

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt_access_token", your_token)

                        your_refresh = myaccts.getSetting("trakt.refresh")
                        addon.setSetting("trakt_refresh_token", your_refresh)

                        your_expires = myaccts.getSetting("trakt.expires")
                        addon.setSetting("trakt_expires_at", your_expires)

#Asgard Trakt
def asgard_trakt():
                
        if xbmcvfs.exists(var.check_addon_asgard) and xbmcvfs.exists(var.check_asgard_settings):
                check_asgard = xbmcaddon.Addon('plugin.video.asgard').getSetting("trakt_access_token")
                if str(var.check_myaccts) != str(check_asgard):
                        
                        f = open(var.client_keys_asgard,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.asgard_client,var.client_am).replace(var.asgard_secret,var.secret_am)
                        f = open(var.client_keys_asgard,'w')
                        f.write(client)
                        f.close()

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("plugin.video.asgard")

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt_access_token", your_token)

                        your_refresh = myaccts.getSetting("trakt.refresh")
                        addon.setSetting("trakt_refresh_token", your_refresh)

                        your_expires = myaccts.getSetting("trakt.expires")
                        addon.setSetting("trakt_expires_at", your_expires)
                      
#My Accounts
def myacts_trakt():
                
        if xbmcvfs.exists(var.check_addon_myaccounts) and xbmcvfs.exists(var.check_myaccounts_settings):
                check_myaccounts = xbmcaddon.Addon('script.module.myaccounts').getSetting("trakt.token")
                if str(var.check_myaccts) != str(check_myaccounts):

                        f = open(var.client_keys_myaccounts,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.myacts_client,var.client_am).replace(var.myacts_secret,var.secret_am)
                        f = open(var.client_keys_myaccounts,'w')
                        f.write(client)
                        f.close()

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        addon = xbmcaddon.Addon("script.module.myaccounts")

                        your_token = myaccts.getSetting("trakt.token")
                        addon.setSetting("trakt.token", your_token)

                        your_username = myaccts.getSetting("trakt.username")
                        addon.setSetting("trakt.username", your_username)

                        your_expires = myaccts.getSetting("trakt.refresh")
                        addon.setSetting("trakt.refresh", your_expires)
                        
                        your_expires = myaccts.getSetting("trakt.expires")
                        addon.setSetting("trakt.expires", your_expires)

#TMDB Helper
def tmdbh_trakt():

        if xbmcvfs.exists(var.check_addon_tmdbh) and xbmcvfs.exists(var.check_tmdbh_settings):
                
                f = open(var.client_keys_tmdbh,'r')
                data = f.read()
                f.close()
                client = data.replace(var.tmdbh_client,var.client_am).replace(var.tmdbh_secret,var.secret_am)
                f = open(var.client_keys_tmdbh,'w')
                f.write(client)
                f.close()

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                addon = xbmcaddon.Addon("plugin.video.themoviedb.helper")

                your_token = myaccts.getSetting("trakt.token")
                your_refresh = myaccts.getSetting("trakt.refresh")
                your_expires = myaccts.getSetting("trakt.expires")
                your_expires_float = float(your_expires)
                your_expires_rnd = int(your_expires_float)

                token = '{"access_token":"'
                refresh = f'","token_type":"bearer","expires_in":7776000,"refresh_token":"'
                expires = f'","scope":"public","created_at":'
                tmdbh_data = '%s%s%s%s%s%s}' %(token,your_token,refresh,your_refresh,expires,your_expires_rnd)
                addon.setSettingString("Trakt_token", tmdbh_data)


#Trakt Addon
def trakt_trakt():
        
        if xbmcvfs.exists(var.check_addon_trakt) and xbmcvfs.exists(var.check_trakt_settings):
                
                f = open(var.client_keys_trakt,'r')
                data = f.read()
                f.close()
                client = data.replace(var.trakt_client,var.client_am).replace(var.trakt_secret,var.secret_am)
                f = open(var.client_keys_trakt,'w')
                f.write(client)
                f.close()
                
                myaccts = xbmcaddon.Addon("script.module.myaccts")
                addon = xbmcaddon.Addon("script.trakt")

                your_username = myaccts.getSetting("trakt.username")
                addon.setSetting("user", your_username)
                
                your_token = myaccts.getSetting("trakt.token")
                your_refresh = myaccts.getSetting("trakt.refresh")
                your_expires = myaccts.getSetting("trakt.expires")
                your_expires_float = float(your_expires)
                your_expires_rnd = int(your_expires_float)
                
                token = '{"access_token": "'
                refresh = f'","token_type": "bearer", "expires_in": 7776000, "refresh_token": "'
                expires = f'", "scope": "public", "created_at": '
                trakt_data = '%s%s%s%s%s%s}' %(token, your_token, refresh, your_refresh, expires, your_expires_rnd)
                addon.setSetting("authorization", trakt_data)


def sync_all(): #Sync all add-ons
        if str(var.check_myaccts) != '': #Check to make sure Account Manager is authorized
                seren_trakt()
                fen_trakt()
                pov_trakt()
                ezra_trakt()
                umb_trakt()
                home_trakt()
                genocide_trakt()
                crew_trakt()
                shazam_trakt()
                night_trakt()
                promise_trakt()
                scrubs_trakt()
                alvin_trakt()
                shadow_trakt()
                ghost_trakt()
                unleashed_trakt()
                chains_trakt()
                md_trakt()
                asgard_trakt()
                myacts_trakt()
                tmdbh_trakt()
                trakt_trakt()

