import xbmc, xbmcaddon
import xbmcvfs
import json
from pathlib import Path
from myaccts.modules import control
from myaccts.modules import var

#Seren RD
def serenrd_auth():

        if xbmcvfs.exists(var.check_addon_seren) and xbmcvfs.exists(var.check_seren_settings): #Check that the addon is installed and settings.xml exists
                check_seren_rd = xbmcaddon.Addon('plugin.video.seren').getSetting("rd.token")
                if str(var.check_myaccts_rd) != str(check_seren_rd): #Compare Account Mananger token to Add-on token. If they match authorization is skipped

                        #Write debrid data to the add-ons settings.xml
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("realdebrid.username")
                        your_token = myaccts.getSetting("realdebrid.token")
                        your_client_id = myaccts.getSetting("realdebrid.client_id")
                        your_refresh = myaccts.getSetting("realdebrid.refresh")
                        your_secret = myaccts.getSetting("realdebrid.secret")
                
                        addon = xbmcaddon.Addon("plugin.video.seren")
                        addon.setSetting("rd.username", your_username)
                        addon.setSetting("rd.auth", your_token)
                        addon.setSetting("rd.client_id", your_client_id)
                        addon.setSetting("rd.refresh", your_refresh)
                        addon.setSetting("rd.secret", your_secret)

                        enabled_rd = ("true")
                        addon.setSetting("realdebrid.enabled", enabled_rd)

                        enabled_pm = ("false")
                        addon.setSetting("premiumize.enabled", enabled_pm)

                        enabled_ad = ("false")
                        addon.setSetting("alldebrid.enabled", enabled_ad)
                

#Ezra RD
def ezrard_auth():

        if xbmcvfs.exists(var.check_addon_ezra) and xbmcvfs.exists(var.check_ezra_settings):
                check_ezra_rd = xbmcaddon.Addon('plugin.video.ezra').getSetting("rd.token")
                if str(var.check_myaccts_rd) != str(check_ezra_rd):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("realdebrid.username")
                        your_token = myaccts.getSetting("realdebrid.token")
                        your_client_id = myaccts.getSetting("realdebrid.client_id")
                        your_refresh = myaccts.getSetting("realdebrid.refresh")
                        your_secret = myaccts.getSetting("realdebrid.secret")
                
                        addon = xbmcaddon.Addon("plugin.video.ezra")
                        addon.setSetting("rd.username", your_username)
                        addon.setSetting("rd.token", your_token)
                        addon.setSetting("rd.client_id", your_client_id)
                        addon.setSetting("rd.refresh", your_refresh)
                        addon.setSetting("rd.secret", your_secret)


#Fen RD
def fenrd_auth():
        
        if xbmcvfs.exists(var.check_addon_fen) and xbmcvfs.exists(var.check_fen_settings):
                check_fen_rd = xbmcaddon.Addon('plugin.video.fen').getSetting("rd.token")
                if str(var.check_myaccts_rd) != str(check_fen_rd):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("realdebrid.username")
                        your_token = myaccts.getSetting("realdebrid.token")
                        your_client_id = myaccts.getSetting("realdebrid.client_id")
                        your_refresh = myaccts.getSetting("realdebrid.refresh")
                        your_secret = myaccts.getSetting("realdebrid.secret")
                
                        addon = xbmcaddon.Addon("plugin.video.fen")
                        addon.setSetting("rd.account_id", your_username)
                        addon.setSetting("rd.token", your_token)
                        addon.setSetting("rd.client_id", your_client_id)
                        addon.setSetting("rd.refresh", your_refresh)
                        addon.setSetting("rd.secret", your_secret)


#POV RD
def povrd_auth():
        
        if xbmcvfs.exists(var.check_addon_pov) and xbmcvfs.exists(var.check_pov_settings):
                check_pov_rd = xbmcaddon.Addon('plugin.video.pov').getSetting("rd.token")
                if str(var.check_myaccts_rd) != str(check_pov_rd):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("realdebrid.username")
                        your_token = myaccts.getSetting("realdebrid.token")
                        your_client_id = myaccts.getSetting("realdebrid.client_id")
                        your_refresh = myaccts.getSetting("realdebrid.refresh")
                        your_secret = myaccts.getSetting("realdebrid.secret")
                
                        addon = xbmcaddon.Addon("plugin.video.pov")
                        addon.setSetting("rd.username", your_username)
                        addon.setSetting("rd.token", your_token)
                        addon.setSetting("rd.client_id", your_client_id)
                        addon.setSetting("rd.refresh", your_refresh)
                        addon.setSetting("rd.secret", your_secret)


#Umbrella RD
def umbrd_auth():
        
        if xbmcvfs.exists(var.check_addon_umb) and xbmcvfs.exists(var.check_umb_settings):
                check_umb_rd = xbmcaddon.Addon('plugin.video.umbrella').getSetting("alldebridtoken")
                if str(var.check_myaccts_rd) != str(check_umb_rd):
                
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("realdebrid.username")
                        your_token = myaccts.getSetting("realdebrid.token")
                        your_client_id = myaccts.getSetting("realdebrid.client_id")
                        your_refresh = myaccts.getSetting("realdebrid.refresh")
                        your_secret = myaccts.getSetting("realdebrid.secret")
                
                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                        addon.setSetting("realdebridusername", your_username)
                        addon.setSetting("realdebridtoken", your_token)
                        addon.setSetting("realdebrid.clientid", your_client_id)
                        addon.setSetting("realdebridrefresh", your_refresh)
                        addon.setSetting("realdebridsecret", your_secret)


#Shadow RD
def shadowrd_auth():
        
        if xbmcvfs.exists(var.check_addon_shadow) and xbmcvfs.exists(var.check_shadow_settings):
                check_shadow_rd = xbmcaddon.Addon('plugin.video.shadow').getSetting("rd.auth")
                if str(var.check_myaccts_rd) != str(check_shadow_rd):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("realdebrid.username")
                        your_token = myaccts.getSetting("realdebrid.token")
                        your_client_id = myaccts.getSetting("realdebrid.client_id")
                        your_refresh = myaccts.getSetting("realdebrid.refresh")
                        your_secret = myaccts.getSetting("realdebrid.secret")
                
                        addon = xbmcaddon.Addon("plugin.video.shadow")
                        addon.setSetting("rd.auth", your_token)
                        addon.setSetting("rd.client_id", your_client_id)
                        addon.setSetting("rd.refresh", your_refresh)
                        addon.setSetting("rd.secret", your_secret)

                        rd_use = ("true")
                        addon.setSetting("debrid_use_rd", rd_use)

                        pm_use = ("false")
                        addon.setSetting("debrid_use_pm", pm_use)

                        ad_use = ("false")
                        addon.setSetting("debrid_use_ad", ad_use)
                
#Ghost RD
def ghostrd_auth():
        
        if xbmcvfs.exists(var.check_addon_ghost) and xbmcvfs.exists(var.check_ghost_settings):
                check_ghost_rd = xbmcaddon.Addon('plugin.video.ghost').getSetting("rd.auth")
                if str(var.check_myaccts_rd) != str(check_ghost_rd):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("realdebrid.username")
                        your_token = myaccts.getSetting("realdebrid.token")
                        your_client_id = myaccts.getSetting("realdebrid.client_id")
                        your_refresh = myaccts.getSetting("realdebrid.refresh")
                        your_secret = myaccts.getSetting("realdebrid.secret")
                
                        addon = xbmcaddon.Addon("plugin.video.ghost")
                        addon.setSetting("rd.auth", your_token)
                        addon.setSetting("rd.client_id", your_client_id)
                        addon.setSetting("rd.refresh", your_refresh)
                        addon.setSetting("rd.secret", your_secret)

                        rd_use = ("true")
                        addon.setSetting("debrid_use_rd", rd_use)

                        pm_use = ("false")
                        addon.setSetting("debrid_use_pm", pm_use)

                        ad_use = ("false")
                        addon.setSetting("debrid_use_ad", ad_use)


#Unleashed RD
def unleashedrd_auth():
        
        if xbmcvfs.exists(var.check_addon_unleashed) and xbmcvfs.exists(var.check_unleashed_settings):
                check_unleashed_rd = xbmcaddon.Addon('plugin.video.unleashed').getSetting("rd.auth")
                if str(var.check_myaccts_rd) != str(check_unleashed_rd):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("realdebrid.username")
                        your_token = myaccts.getSetting("realdebrid.token")
                        your_client_id = myaccts.getSetting("realdebrid.client_id")
                        your_refresh = myaccts.getSetting("realdebrid.refresh")
                        your_secret = myaccts.getSetting("realdebrid.secret")
                
                        addon = xbmcaddon.Addon("plugin.video.unleashed")
                        addon.setSetting("rd.auth", your_token)
                        addon.setSetting("rd.client_id", your_client_id)
                        addon.setSetting("rd.refresh", your_refresh)
                        addon.setSetting("rd.secret", your_secret)

                        d_select = ("0")
                        addon.setSetting("debrid_select", d_select)


#Chains RD
def chainsrd_auth():
        
        if xbmcvfs.exists(var.check_addon_chains) and xbmcvfs.exists(var.check_chains_settings):
                check_thechains_rd = xbmcaddon.Addon('plugin.video.thechains').getSetting("rd.auth")
                if str(var.check_myaccts_rd) != str(check_thechains_rd):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("realdebrid.username")
                        your_token = myaccts.getSetting("realdebrid.token")
                        your_client_id = myaccts.getSetting("realdebrid.client_id")
                        your_refresh = myaccts.getSetting("realdebrid.refresh")
                        your_secret = myaccts.getSetting("realdebrid.secret")
                
                        addon = xbmcaddon.Addon("plugin.video.thechains")
                        addon.setSetting("rd.auth", your_token)
                        addon.setSetting("rd.client_id", your_client_id)
                        addon.setSetting("rd.refresh", your_refresh)
                        addon.setSetting("rd.secret", your_secret)

                        d_select = ("0")
                        addon.setSetting("debrid_select", d_select)


#Moria RD
def moriard_auth():
        
        if xbmcvfs.exists(var.check_addon_moria) and xbmcvfs.exists(var.check_moria_settings):
                check_moria_rd = xbmcaddon.Addon('plugin.video.moria').getSetting("rd.auth")
                if str(var.check_myaccts_rd) != str(check_moria_rd):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("realdebrid.username")
                        your_token = myaccts.getSetting("realdebrid.token")
                        your_client_id = myaccts.getSetting("realdebrid.client_id")
                        your_refresh = myaccts.getSetting("realdebrid.refresh")
                        your_secret = myaccts.getSetting("realdebrid.secret")
                
                        addon = xbmcaddon.Addon("plugin.video.moria")
                        addon.setSetting("rd.auth", your_token)
                        addon.setSetting("rd.client_id", your_client_id)
                        addon.setSetting("rd.refresh", your_refresh)
                        addon.setSetting("rd.secret", your_secret)

                        d_select = ("0")
                        addon.setSetting("debrid_select", d_select)


#Base 19 RD
def baserd_auth():
        
        if xbmcvfs.exists(var.check_addon_base) and xbmcvfs.exists(var.check_base_settings):
                check_base_rd = xbmcaddon.Addon('plugin.video.base19').getSetting("rd.auth")
                if str(var.check_myaccts_rd) != str(check_base_rd):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("realdebrid.username")
                        your_token = myaccts.getSetting("realdebrid.token")
                        your_client_id = myaccts.getSetting("realdebrid.client_id")
                        your_refresh = myaccts.getSetting("realdebrid.refresh")
                        your_secret = myaccts.getSetting("realdebrid.secret")
                
                        addon = xbmcaddon.Addon("plugin.video.base19")
                        addon.setSetting("rd.auth", your_token)
                        addon.setSetting("rd.client_id", your_client_id)
                        addon.setSetting("rd.refresh", your_refresh)
                        addon.setSetting("rd.secret", your_secret)

                        d_select = ("0")
                        addon.setSetting("debrid_select", d_select)


#Twisted RD
def twistedrd_auth():
        
        if xbmcvfs.exists(var.check_addon_twisted) and xbmcvfs.exists(var.check_twisted_settings):
                check_twisted_rd = xbmcaddon.Addon('plugin.video.twisted').getSetting("rd.auth")
                if str(var.check_myaccts_rd) != str(check_twisted_rd):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("realdebrid.username")
                        your_token = myaccts.getSetting("realdebrid.token")
                        your_client_id = myaccts.getSetting("realdebrid.client_id")
                        your_refresh = myaccts.getSetting("realdebrid.refresh")
                        your_secret = myaccts.getSetting("realdebrid.secret")
                
                        addon = xbmcaddon.Addon("plugin.video.twisted")
                        addon.setSetting("rd.auth", your_token)
                        addon.setSetting("rd.client_id", your_client_id)
                        addon.setSetting("rd.refresh", your_refresh)
                        addon.setSetting("rd.secret", your_secret)

                        d_select = ("0")
                        addon.setSetting("debrid_select", d_select)


#Magic Dragon RD
def mdrd_auth():
        
        if xbmcvfs.exists(var.check_addon_md) and xbmcvfs.exists(var.check_md_settings):
                check_md_rd = xbmcaddon.Addon('plugin.video.magicdragon').getSetting("rd.auth")
                if str(var.check_myaccts_rd) != str(check_md_rd):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("realdebrid.username")
                        your_token = myaccts.getSetting("realdebrid.token")
                        your_client_id = myaccts.getSetting("realdebrid.client_id")
                        your_refresh = myaccts.getSetting("realdebrid.refresh")
                        your_secret = myaccts.getSetting("realdebrid.secret")
                
                        addon = xbmcaddon.Addon("plugin.video.magicdragon")
                        addon.setSetting("rd.auth", your_token)
                        addon.setSetting("rd.client_id", your_client_id)
                        addon.setSetting("rd.refresh", your_refresh)
                        addon.setSetting("rd.secret", your_secret)

                        d_select = ("0")
                        addon.setSetting("debrid_select", d_select)


#Asgard RD
def asgardrd_auth():
        
        if xbmcvfs.exists(var.check_addon_asgard) and xbmcvfs.exists(var.check_asgard_settings):
                check_asgard_rd = xbmcaddon.Addon('plugin.video.asgard').getSetting("rd.auth")
                if str(var.check_myaccts_rd) != str(check_asgard_rd):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("realdebrid.username")
                        your_token = myaccts.getSetting("realdebrid.token")
                        your_client_id = myaccts.getSetting("realdebrid.client_id")
                        your_refresh = myaccts.getSetting("realdebrid.refresh")
                        your_secret = myaccts.getSetting("realdebrid.secret")
                
                        addon = xbmcaddon.Addon("plugin.video.asgard")
                        addon.setSetting("rd.auth", your_token)
                        addon.setSetting("rd.client_id", your_client_id)
                        addon.setSetting("rd.refresh", your_refresh)
                        addon.setSetting("rd.secret", your_secret)

                        d_select = ("0")
                        addon.setSetting("debrid_select", d_select)


#M.E.T.V RD
def metvrd_auth():
        
        if xbmcvfs.exists(var.check_addon_metv) and xbmcvfs.exists(var.check_metv_settings):
                check_metv_rd = xbmcaddon.Addon('plugin.video.metv19').getSetting("rd.auth")
                if str(var.check_myaccts_rd) != str(check_metv_rd):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("realdebrid.username")
                        your_token = myaccts.getSetting("realdebrid.token")
                        your_client_id = myaccts.getSetting("realdebrid.client_id")
                        your_refresh = myaccts.getSetting("realdebrid.refresh")
                        your_secret = myaccts.getSetting("realdebrid.secret")
                
                        addon = xbmcaddon.Addon("plugin.video.metv19")
                        addon.setSetting("rd.auth", your_token)
                        addon.setSetting("rd.client_id", your_client_id)
                        addon.setSetting("rd.refresh", your_refresh)
                        addon.setSetting("rd.secret", your_secret)

                        d_select = ("0")
                        addon.setSetting("debrid_select", d_select)


#ResolveURL RD
def rurlrd_auth():
        
        if xbmcvfs.exists(var.check_addon_rurl) and xbmcvfs.exists(var.check_rurl_settings):
                check_rurl_rd = xbmcaddon.Addon('script.module.resolveurl').getSetting("RealDebridResolver_token")
                if str(var.check_myaccts_rd) != str(check_rurl_rd):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("realdebrid.username")
                        your_token = myaccts.getSetting("realdebrid.token")
                        your_client_id = myaccts.getSetting("realdebrid.client_id")
                        your_refresh = myaccts.getSetting("realdebrid.refresh")
                        your_secret = myaccts.getSetting("realdebrid.secret")
                
                        addon = xbmcaddon.Addon("script.module.resolveurl")
                        addon.setSetting("RealDebridResolver_login", your_username)
                        addon.setSetting("RealDebridResolver_token", your_token)
                        addon.setSetting("RealDebridResolver_client_id", your_client_id)
                        addon.setSetting("RealDebridResolver_refresh", your_refresh)
                        addon.setSetting("RealDebridResolver_client_secret", your_secret)

                        cache_only = ("true")
                        addon.setSetting("RealDebridResolver_cached_only", cache_only)


#My Accounts RD
def myaccountsrd_auth():

        if xbmcvfs.exists(var.check_addon_myaccounts) and xbmcvfs.exists(var.check_myaccounts_settings):
                check_myaccounts_rd = xbmcaddon.Addon('script.module.myaccounts').getSetting("realdebrid.token")
                if str(var.check_myaccts_rd) != str(check_myaccounts_rd):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("realdebrid.username")
                        your_token = myaccts.getSetting("realdebrid.token")
                        your_client_id = myaccts.getSetting("realdebrid.client_id")
                        your_refresh = myaccts.getSetting("realdebrid.refresh")
                        your_secret = myaccts.getSetting("realdebrid.secret")
                
                        addon = xbmcaddon.Addon("script.module.myaccounts")
                        addon.setSetting("realdebrid.username", your_username)
                        addon.setSetting("realdebrid.token", your_token)
                        addon.setSetting("realdebrid.client_id", your_client_id)
                        addon.setSetting("realdebrid.refresh", your_refresh)
                        addon.setSetting("realdebrid.secret", your_secret)

#Realizer RD
def realizer_auth():

        if xbmcvfs.exists(var.check_addon_realizer) and xbmcvfs.exists(var.check_realizer_settings):

                rdauth = {}
                myaccts = xbmcaddon.Addon('script.module.myaccts')
                rdauth = {'client_id': myaccts.getSetting('realdebrid.client_id'), 'client_secret': myaccts.getSetting('realdebrid.secret'), 'token': myaccts.getSetting('realdebrid.token'), 'refresh_token': myaccts.getSetting('realdebrid.refresh'), 'added': '202301010243'}

                with open(var.realizer_path, 'w') as debrid_write:
                        json.dump(rdauth, debrid_write)
                        
def debrid_auth_rd(): #Sync all add-ons
       if str(var.check_myaccts_rd) != '': #Check to make sure Account Manager is authorized
               serenrd_auth()
               ezrard_auth()
               fenrd_auth()
               povrd_auth()
               umbrd_auth()
               shadowrd_auth()
               ghostrd_auth()
               unleashedrd_auth()
               chainsrd_auth()
               moriard_auth()
               baserd_auth()
               twistedrd_auth()
               mdrd_auth()
               asgardrd_auth()
               metvrd_auth()
               rurlrd_auth()
               myaccountsrd_auth()
               realizer_auth()
