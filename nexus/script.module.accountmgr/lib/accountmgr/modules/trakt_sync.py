import xbmc, xbmcaddon, xbmcgui
import os
import xbmcvfs
from pathlib import Path
from libs.common import var
 
class Auth:
    def trakt_auth(self):
    #Seren
        try:
                if xbmcvfs.exists(var.chk_seren) and xbmcvfs.exists(var.chkset_seren) and var.setting('traktuserkey.enabled') == 'true': #Check that the addon is installed and settings.xml exists.
                        chk_auth_seren = xbmcaddon.Addon('plugin.video.seren').getSetting("trakt.auth")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_seren) or str(chk_auth_seren) == '': #Compare Account Mananger token to Add-on token. If they match, authorization is skipped
                
                                #Insert Account Mananger API keys into add-on
                                f = open(var.path_seren,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.seren_client,var.client_am).replace(var.seren_secret,var.secret_am)
                                f = open(var.path_seren,'w')
                                f.write(client)
                                f.close()

                                #Write trakt data to settings.xml
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.seren")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.auth", your_token)

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.username", your_username)
                                
                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)
                                
                                your_expires = accountmgr.getSetting("trakt.expires")
                                your_expires_float = float(your_expires)
                                your_expires_rnd = int(your_expires_float)
                                your_expires_str = str(your_expires_rnd)
                                addon.setSetting("trakt.expires", your_expires_str)
        except:
                pass

    #Fen
        try:
            if xbmcvfs.exists(var.chk_fen) and xbmcvfs.exists(var.chkset_fen):
                    chk_auth_fen = xbmcaddon.Addon('plugin.video.fen').getSetting("trakt.token")
                    if not str(var.chk_accountmgr_tk) == str(chk_auth_fen) or str(chk_auth_fen) == '':
                    
                                f = open(var.path_fen,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.fen_client,var.client_am).replace(var.fen_secret,var.secret_am)
                                f = open(var.path_fen,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.fen")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)
                                
                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt.expires", your_expires)

                                addon.setSetting("trakt.indicators_active", 'true')
                                addon.setSetting("watched_indicators", '1')
        except:
                pass

    #Ezra
        try:
                if xbmcvfs.exists(var.chk_ezra) and xbmcvfs.exists(var.chkset_ezra):
                        chk_auth_ezra = xbmcaddon.Addon('plugin.video.ezra').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_ezra) or str(chk_auth_ezra) == '':

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.ezra")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt_user", your_username)
                                
                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt.expires", your_expires)

                                addon.setSetting("trakt.indicators_active", 'true')
                                addon.setSetting("watched_indicators", '1')
        except:
                pass

     #Coalition
        try:
            if xbmcvfs.exists(var.chk_coal) and xbmcvfs.exists(var.chkset_coal):
                    chk_auth_coal = xbmcaddon.Addon('plugin.video.coalition').getSetting("trakt.token")
                    if not str(var.chk_accountmgr_tk) == str(chk_auth_coal) or str(chk_auth_coal) == '':
                    
                                f = open(var.path_coal,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.coal_client,var.client_am).replace(var.coal_secret,var.secret_am)
                                f = open(var.path_coal,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.coalition")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt_user", your_username)
                                
                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt.expires", your_expires)

                                addon.setSetting("trakt.indicators_active", 'true')
                                addon.setSetting("watched_indicators", '1')
        except:
                pass
            
    #POV
        try:
                if xbmcvfs.exists(var.chk_pov) and xbmcvfs.exists(var.chkset_pov):
                        chk_auth_pov = xbmcaddon.Addon('plugin.video.pov').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_pov) or str(chk_auth_pov) == '':

                                f = open(var.path_pov,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.pov_client,var.client_am).replace(var.pov_client,var.secret_am)
                                f = open(var.path_pov,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.pov")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt_user", your_username)
                                
                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt.expires", your_expires)

                                addon.setSetting("trakt.indicators_active", 'true')
                                addon.setSetting("watched.indicators", '1')              
        except:
                pass
        
    #Umbrella
        try:
                if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb):
                        chk_auth_umb = xbmcaddon.Addon('plugin.video.umbrella').getSetting("trakt.user.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_umb) or str(chk_auth_umb) == '':

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.umbrella")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user.name", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.user.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refreshtoken", your_refresh)

                                your_secret = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt.token.expires", your_secret)

                                addon.setSetting("traktuserkey.customenabled", 'true')
                                addon.setSetting("trakt.clientid", var.client_am)
                                addon.setSetting("trakt.clientsecret", var.secret_am)
                                
        except:
                pass

    #Shadow
        try:
                if xbmcvfs.exists(var.chk_shadow) and xbmcvfs.exists(var.chkset_shadow):
                        chk_auth_shadow = xbmcaddon.Addon('plugin.video.shadow').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_shadow) or str(chk_auth_shadow) == '':
                                
                                f = open(var.path_shadow,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.shadow_client,var.client_am).replace(var.shadow_secret,var.secret_am)
                                f = open(var.path_shadow,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.shadow")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt_access_token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt_refresh_token", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                pass
        
    #Ghost
        try:
                if xbmcvfs.exists(var.chk_ghost) and xbmcvfs.exists(var.chkset_ghost):
                        chk_auth_ghost = xbmcaddon.Addon('plugin.video.ghost').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_ghost) or str(chk_auth_ghost) == '':
                                
                                f = open(var.path_ghost,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.ghost_client,var.client_am).replace(var.ghost_secret,var.secret_am)
                                f = open(var.path_ghost,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.ghost")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt_access_token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt_refresh_token", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                pass

    #Base 19
        try:
                if xbmcvfs.exists(var.chk_base) and xbmcvfs.exists(var.chkset_base):
                        chk_auth_base = xbmcaddon.Addon('plugin.video.base19').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_base) or str(chk_auth_base) == '':
                                
                                f = open(var.path_base,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.base_client,var.client_am).replace(var.base_secret,var.secret_am)
                                f = open(var.path_base,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.base19")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt_access_token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt_refresh_token", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                pass
            
    #Unleashed
        try:
                if xbmcvfs.exists(var.chk_unleashed) and xbmcvfs.exists(var.chkset_unleashed):
                        chk_auth_unleashed = xbmcaddon.Addon('plugin.video.unleashed').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_unleashed) or str(chk_auth_unleashed) == '':
                                
                                f = open(var.path_unleashed,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.unleashed_client,var.client_am).replace(var.unleashed_secret,var.secret_am)
                                f = open(var.path_unleashed,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.unleashed")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt_access_token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt_refresh_token", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                pass
        
    #Chain Reaction
        try:
                if xbmcvfs.exists(var.chk_chains) and xbmcvfs.exists(var.chkset_chains):
                        chk_auth_chains = xbmcaddon.Addon('plugin.video.thechains').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_chains) or str(chk_auth_chains) == '':
                                
                                f = open(var.path_chains,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.chains_client,var.client_am).replace(var.chains_secret,var.secret_am)
                                f = open(var.path_chains,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.thechains")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt_access_token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt_refresh_token", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                pass
           
    #Magic Dragon
        try:
                if xbmcvfs.exists(var.chk_md) and xbmcvfs.exists(var.chkset_md):
                        chk_auth_md = xbmcaddon.Addon('plugin.video.magicdragon').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_md) or str(chk_auth_md) == '':
                               
                                f = open(var.path_md,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.md_client,var.client_am).replace(var.md_client,var.secret_am)
                                f = open(var.path_md,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.magicdragon")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt_access_token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt_refresh_token", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                pass
        
    #Asgard
        try:
                if xbmcvfs.exists(var.chk_asgard) and xbmcvfs.exists(var.chkset_asgard):
                        chk_auth_asgard = xbmcaddon.Addon('plugin.video.asgard').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_asgard) or str(chk_auth_asgard) == '':
                                
                                f = open(var.path_asgard,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.asgard_client,var.client_am).replace(var.asgard_secret,var.secret_am)
                                f = open(var.path_asgard,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.asgard")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt_access_token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt_refresh_token", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                pass

    #Patriot
        try:
                if xbmcvfs.exists(var.chk_patriot) and xbmcvfs.exists(var.chkset_patriot):
                        chk_auth_patriot = xbmcaddon.Addon('plugin.video.patriot').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_patriot) or str(chk_auth_patriot) == '':
                                
                                f = open(var.path_patriot,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.patriot_client,var.client_am).replace(var.patriot_secret,var.secret_am)
                                f = open(var.path_patriot,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.patriot")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt_access_token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt_refresh_token", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                pass

    #Black Lightning
        try:
                if xbmcvfs.exists(var.chk_blackl) and xbmcvfs.exists(var.chkset_blackl):
                        chk_auth_blackl = xbmcaddon.Addon('plugin.video.blacklightning').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_blackl) or str(chk_auth_blackl) == '':
                                
                                f = open(var.path_blackl,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.blackl_client,var.client_am).replace(var.blackl_secret,var.secret_am)
                                f = open(var.path_blackl,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.blacklightning")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt_access_token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt_refresh_token", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                pass
            
    #Aliunde
        try:
                if xbmcvfs.exists(var.chk_aliunde) and xbmcvfs.exists(var.chkset_aliunde):
                        chk_auth_aliunde = xbmcaddon.Addon('plugin.video.aliundek19').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_aliunde) or str(chk_auth_aliunde) == '':
                                
                                f = open(var.path_aliunde,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.aliunde_client,var.client_am).replace(var.aliunde_secret,var.secret_am)
                                f = open(var.path_aliunde,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.aliundek19")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt_access_token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt_refresh_token", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                pass
            
    #Homelander
        try:
                if xbmcvfs.exists(var.chk_home) and xbmcvfs.exists(var.chkset_home):
                        chk_auth_home = xbmcaddon.Addon('plugin.video.homelander').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_home) or str(chk_auth_home) == '':

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.homelander")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                addon.setSetting("trakt.authed", 'yes')
                                addon.setSetting("trakt.client_id", var.client_am)
                                addon.setSetting("trakt.client_secret", var.secret_am)
        except:
                pass
        
    #Quicksilver
        try:
                if xbmcvfs.exists(var.chk_quick) and xbmcvfs.exists(var.chkset_quick):
                        chk_auth_quick = xbmcaddon.Addon('plugin.video.quicksilver').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_quick) or str(chk_auth_quick) == '':

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.quicksilver")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                addon.setSetting("trakt.authed", 'yes')
                                addon.setSetting("trakt.client_id", var.client_am)
                                addon.setSetting("trakt.client_secret", var.secret_am)
        except:
                pass

    #Chains Genocide
        try:
                if xbmcvfs.exists(var.chk_genocide) and xbmcvfs.exists(var.chkset_genocide):
                        chk_auth_genocide = xbmcaddon.Addon('plugin.video.chainsgenocide').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_genocide) or str(chk_auth_genocide) == '':

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.chainsgenocide")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                addon.setSetting("trakt.authed", 'yes')
                                addon.setSetting("trakt.client_id", var.client_am)
                                addon.setSetting("trakt.client_secret", var.secret_am)
        except:
                pass
            
    #Absolution
        try:
                if xbmcvfs.exists(var.chk_absol) and xbmcvfs.exists(var.chkset_absol):
                        chk_auth_absol = xbmcaddon.Addon('plugin.video.absolution').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_absol) or str(chk_auth_absol) == '':

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.absolution")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                addon.setSetting("trakt.authed", 'yes')
                                addon.setSetting("trakt.client_id", var.client_am)
                                addon.setSetting("trakt.client_secret", var.secret_am)
        except:
                pass

    #Shazam
        try:
                if xbmcvfs.exists(var.chk_shazam) and xbmcvfs.exists(var.chkset_shazam):
                        chk_auth_shazam = xbmcaddon.Addon('plugin.video.shazam').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_shazam) or str(chk_auth_shazam) == '':

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.shazam")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                addon.setSetting("trakt.authed", 'yes')
                                addon.setSetting("trakt.client_id", var.client_am)
                                addon.setSetting("trakt.client_secret", var.secret_am)
        except:
                pass
            
    #The Crew
        try:
                if xbmcvfs.exists(var.chk_crew) and xbmcvfs.exists(var.chkset_crew):
                        chk_auth_crew = xbmcaddon.Addon('plugin.video.thecrew').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_crew) or str(chk_auth_crew) == '':

                                f = open(var.path_crew,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.crew_client,var.client_am).replace(var.crew_client,var.secret_am)
                                f = open(var.path_crew,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.thecrew")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)
        except:
                pass
        
    #Nightwing
        try:
                if xbmcvfs.exists(var.chk_night) and xbmcvfs.exists(var.chkset_night):
                        chk_auth_night = xbmcaddon.Addon('plugin.video.nightwing').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_night) or str(chk_auth_night) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.nightwing")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                addon.setSetting("trakt.authed", 'yes')
                                addon.setSetting("trakt.client_id", var.client_am)
                                addon.setSetting("trakt.client_secret", var.secret_am)
        except:
                pass
               
    #Alvin
        try:
                if xbmcvfs.exists(var.chk_alvin) and xbmcvfs.exists(var.chkset_alvin):
                        chk_auth_alvin = xbmcaddon.Addon('plugin.video.alvin').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_alvin) or str(chk_auth_alvin) == '':

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.alvin")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                addon.setSetting("trakt.authed", 'yes')
                                addon.setSetting("trakt.client_id", var.client_am)
                                addon.setSetting("trakt.client_secret", var.secret_am)
        except:
                pass

    #Moria
        try:
                if xbmcvfs.exists(var.chk_moria) and xbmcvfs.exists(var.chkset_moria):
                        chk_auth_moria = xbmcaddon.Addon('plugin.video.moria').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_moria) or str(chk_auth_moria) == '':

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.moria")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                addon.setSetting("trakt.authed", 'yes')
                                addon.setSetting("trakt.client_id", var.client_am)
                                addon.setSetting("trakt.client_secret", var.secret_am)
        except:
                pass

    #Nine Lives
        try:
                if xbmcvfs.exists(var.chk_nine) and xbmcvfs.exists(var.chkset_nine):
                        chk_auth_nine = xbmcaddon.Addon('plugin.video.nine').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_nine) or str(chk_auth_nine) == '':

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.nine")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                addon.setSetting("trakt.authed", 'yes')
                                addon.setSetting("trakt.client_id", var.client_am)
                                addon.setSetting("trakt.client_secret", var.secret_am)
        except:
                pass
            
    #Scrubs V2
        try:
                if xbmcvfs.exists(var.chk_scrubs) and xbmcvfs.exists(var.chkset_scrubs):
                        chk_auth_scrubs = xbmcaddon.Addon('plugin.video.scrubsv2').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_scrubs) or str(chk_auth_scrubs) == '':

                                f = open(var.path_scrubs,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.scrubs_client,var.client_am).replace(var.scrubs_secret,var.secret_am)
                                f = open(var.path_scrubs,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.scrubsv2")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                addon.setSetting("trakt.authed", 'yes')
        except:
                pass

    #TMDB Helper
        try:
                if xbmcvfs.exists(var.chk_tmdbh) and xbmcvfs.exists(var.chkset_tmdbh):
                        
                                f = open(var.path_tmdbh,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.tmdbh_client,var.client_am).replace(var.tmdbh_secret,var.secret_am)
                                f = open(var.path_tmdbh,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.themoviedb.helper")

                                your_token = accountmgr.getSetting("trakt.token")
                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                your_expires = accountmgr.getSetting("trakt.expires")
                                your_expires_float = float(your_expires)
                                your_expires_rnd = int(your_expires_float)

                                token = '{"access_token":"'
                                refresh = f'","token_type":"bearer","expires_in":7776000,"refresh_token":"'
                                expires = f'","scope":"public","created_at":'
                                tmdbh_data = '%s%s%s%s%s%s}' %(token,your_token,refresh,your_refresh,expires,your_expires_rnd)
                                addon.setSettingString("Trakt_token", tmdbh_data)
                                addon.setSetting("startup_notifications", 'false')
        except:
                pass

    #Trakt Addon
        try:
                if xbmcvfs.exists(var.chk_trakt) and xbmcvfs.exists(var.chkset_trakt):
                        
                                f = open(var.path_trakt,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.trakt_client,var.client_am).replace(var.trakt_secret,var.secret_am)
                                f = open(var.path_trakt,'w')
                                f.write(client)
                                f.close()
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("script.trakt")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("user", your_username)
                                
                                your_token = accountmgr.getSetting("trakt.token")
                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                your_expires = accountmgr.getSetting("trakt.expires")
                                your_expires_float = float(your_expires)
                                your_expires_rnd = int(your_expires_float)
                                
                                token = '{"access_token": "'
                                refresh = f'","token_type": "bearer", "expires_in": 7776000, "refresh_token": "'
                                expires = f'", "scope": "public", "created_at": '
                                trakt_data = '%s%s%s%s%s%s}' %(token, your_token, refresh, your_refresh, expires, your_expires_rnd)
                                addon.setSetting("authorization", trakt_data)
        except:
                pass
            
    #My Accounts
        try:
                if xbmcvfs.exists(var.chk_myaccounts) and xbmcvfs.exists(var.chkset_myaccounts):
                        chk_auth_myaccounts = xbmcaddon.Addon('script.module.myaccounts').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_myaccounts) or str(chk_auth_myaccounts) == '':

                                f = open(var.path_myaccounts,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.myacts_client,var.client_am).replace(var.myacts_secret,var.secret_am)
                                f = open(var.path_myaccounts,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("script.module.myaccounts")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.username", your_username)

                                your_expires = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_expires)
                                
                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt.expires", your_expires)
        except:
                pass
