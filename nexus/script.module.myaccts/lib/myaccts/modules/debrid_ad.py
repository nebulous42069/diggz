import xbmc, xbmcaddon
import xbmcvfs
from pathlib import Path
from myaccts.modules import control
from myaccts.modules import var

#Seren AD
def serenad_auth():

        if xbmcvfs.exists(var.check_addon_seren) and xbmcvfs.exists(var.check_seren_settings): #Check that the addon is installed and settings.xml exists
                check_seren_ad = xbmcaddon.Addon('plugin.video.seren').getSetting("alldebrid.token")
                if str(var.check_myaccts_ad) != str(check_seren_ad): #Compare Account Mananger token to Add-on token. If they match authorization is skipped

                        #Write debrid data to the add-ons settings.xml
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("alldebrid.username")
                        your_token = myaccts.getSetting("alldebrid.token")

                        addon = xbmcaddon.Addon("plugin.video.seren")
                        addon.setSetting("alldebrid.username", your_username)
                        addon.setSetting("alldebrid.token", your_token)

                        enabled_rd = ("false")
                        addon.setSetting("realdebrid.enabled", enabled_rd)

                        enabled_pm = ("false")
                        addon.setSetting("premiumize.enabled", enabled_pm)

                        enabled_ad = ("true")
                        addon.setSetting("alldebrid.enabled", enabled_ad)

#Ezra AD
def ezraad_auth():

        if xbmcvfs.exists(var.check_addon_ezra) and xbmcvfs.exists(var.check_ezra_settings):
                check_ezra_ad = xbmcaddon.Addon('plugin.video.ezra').getSetting("ad.token")
                if str(var.check_myaccts_ad) != str(check_ezra_ad):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("alldebrid.username")
                        your_token = myaccts.getSetting("alldebrid.token")
                
                        addon = xbmcaddon.Addon("plugin.video.ezra")
                        addon.setSetting("ad.account_id", your_username)
                        addon.setSetting("ad.token", your_token)


#Fen AD
def fenad_auth():

        if xbmcvfs.exists(var.check_addon_fen) and xbmcvfs.exists(var.check_fen_settings):
                check_fen_ad = xbmcaddon.Addon('plugin.video.fen').getSetting("ad.token")
                if str(var.check_myaccts_ad) != str(check_fen_ad):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("alldebrid.username")
                        your_token = myaccts.getSetting("alldebrid.token")
                
                        addon = xbmcaddon.Addon("plugin.video.fen")
                        addon.setSetting("ad.account_id", your_username)
                        addon.setSetting("ad.token", your_token)


#POV AD
def povad_auth():

        if xbmcvfs.exists(var.check_addon_pov) and xbmcvfs.exists(var.check_pov_settings):
                check_pov_ad = xbmcaddon.Addon('plugin.video.pov').getSetting("ad.token")
                if str(var.check_myaccts_ad) != str(check_pov_ad):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("alldebrid.username")
                        your_token = myaccts.getSetting("alldebrid.token")
                
                        addon = xbmcaddon.Addon("plugin.video.pov")
                        addon.setSetting("ad.account_id", your_username)
                        addon.setSetting("ad.token", your_token)
                

#Umbrella AD
def umbad_auth():

        if xbmcvfs.exists(var.check_addon_umb) and xbmcvfs.exists(var.check_umb_settings):
                check_umb_ad = xbmcaddon.Addon('plugin.video.umbrella').getSetting("alldebridtoken")
                if str(var.check_myaccts_ad) != str(check_umb_ad):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("alldebrid.username")
                        your_token = myaccts.getSetting("alldebrid.token")
                
                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                        addon.setSetting("alldebridusername", your_username)
                        addon.setSetting("alldebridtoken", your_token)


#Shadow AD
def shadowad_auth():

        if xbmcvfs.exists(var.check_addon_shadow) and xbmcvfs.exists(var.check_shadow_settings):
                check_shadow_ad = xbmcaddon.Addon('plugin.video.shadow').getSetting("alldebrid.token")
                if str(var.check_myaccts_ad) != str(check_shadow_ad):
                
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("alldebrid.username")
                        your_token = myaccts.getSetting("alldebrid.token")
                
                        addon = xbmcaddon.Addon("plugin.video.shadow")
                        addon.setSetting("alldebrid.username", your_username)
                        addon.setSetting("alldebrid.token", your_token)

                        rd_use = ("false")
                        addon.setSetting("debrid_use_rd", rd_use)

                        pm_use = ("false")
                        addon.setSetting("debrid_use_pm", pm_use)

                        ad_use = ("true")
                        addon.setSetting("debrid_use_ad", ad_use)

                
#Ghost AD
def ghostad_auth():

        if xbmcvfs.exists(var.check_addon_ghost) and xbmcvfs.exists(var.check_ghost_settings):
                check_ghost_ad = xbmcaddon.Addon('plugin.video.ghost').getSetting("alldebrid.token")
                if str(var.check_myaccts_ad) != str(check_ghost_ad):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("alldebrid.username")
                        your_token = myaccts.getSetting("alldebrid.token")
                        
                        addon = xbmcaddon.Addon("plugin.video.ghost")
                        addon.setSetting("alldebrid.username", your_username)
                        addon.setSetting("alldebrid.token", your_token)

                        rd_use = ("false")
                        addon.setSetting("debrid_use_rd", rd_use)

                        pm_use = ("false")
                        addon.setSetting("debrid_use_pm", pm_use)

                        ad_use = ("true")
                        addon.setSetting("debrid_use_ad", ad_use)


#Unleashed AD
def unleashedad_auth():

        if xbmcvfs.exists(var.check_addon_unleashed) and xbmcvfs.exists(var.check_unleashed_settings):
                check_unleashed_ad = xbmcaddon.Addon('plugin.video.unleashed').getSetting("alldebrid.token")
                if str(var.check_myaccts_ad) != str(check_unleashed_ad):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("alldebrid.username")
                        your_token = myaccts.getSetting("alldebrid.token")
                
                        addon = xbmcaddon.Addon("plugin.video.unleashed")
                        addon.setSetting("alldebrid.username", your_username)
                        addon.setSetting("alldebrid.token", your_token)

                        d_select = ("2")
                        addon.setSetting("debrid_select", d_select)


#Chains AD
def chainsad_auth():

        if xbmcvfs.exists(var.check_addon_chains) and xbmcvfs.exists(var.check_chains_settings):
                check_thechains_ad = xbmcaddon.Addon('plugin.video.thechains').getSetting("alldebrid.token")
                if str(var.check_myaccts_ad) != str(check_thechains_ad):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("alldebrid.username")
                        your_token = myaccts.getSetting("alldebrid.token")
                
                        addon = xbmcaddon.Addon("plugin.video.thechains")
                        addon.setSetting("alldebrid.username", your_username)
                        addon.setSetting("alldebrid.token", your_token)

                        d_select = ("2")
                        addon.setSetting("debrid_select", d_select)


#Moria AD
def moriaad_auth():

        if xbmcvfs.exists(var.check_addon_moria) and xbmcvfs.exists(var.check_moria_settings):
                check_moria_ad = xbmcaddon.Addon('plugin.video.moria').getSetting("alldebrid.token")
                if str(var.check_myaccts_ad) != str(check_moria_ad):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("alldebrid.username")
                        your_token = myaccts.getSetting("alldebrid.token")
                
                        addon = xbmcaddon.Addon("plugin.video.moria")
                        addon.setSetting("alldebrid.username", your_username)
                        addon.setSetting("alldebrid.token", your_token)

                        d_select = ("2")
                        addon.setSetting("debrid_select", d_select)


#Base 19 AD
def basead_auth():

        if xbmcvfs.exists(var.check_addon_base) and xbmcvfs.exists(var.check_base_settings):
                check_base_ad = xbmcaddon.Addon('plugin.video.base19').getSetting("alldebrid.token")
                if str(var.check_myaccts_ad) != str(check_base_ad):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("alldebrid.username")
                        your_token = myaccts.getSetting("alldebrid.token")
                
                        addon = xbmcaddon.Addon("plugin.video.base19")
                        addon.setSetting("alldebrid.username", your_username)
                        addon.setSetting("alldebrid.token", your_token)

                        d_select = ("2")
                        addon.setSetting("debrid_select", d_select)


#Twisted AD
def twistedad_auth():

        if xbmcvfs.exists(var.check_addon_twisted) and xbmcvfs.exists(var.check_twisted_settings):
                check_twisted_ad = xbmcaddon.Addon('plugin.video.twisted').getSetting("alldebrid.token")
                if str(var.check_myaccts_ad) != str(check_twisted_ad):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("alldebrid.username")
                        your_token = myaccts.getSetting("alldebrid.token")
                
                        addon = xbmcaddon.Addon("plugin.video.twisted")
                        addon.setSetting("alldebrid.username", your_username)
                        addon.setSetting("alldebrid.token", your_token)

                        d_select = ("2")
                        addon.setSetting("debrid_select", d_select)


#Magic Dragon AD
def mdad_auth():

        if xbmcvfs.exists(var.check_addon_md) and xbmcvfs.exists(var.check_md_settings):
                check_md_ad = xbmcaddon.Addon('plugin.video.magicdragon').getSetting("alldebrid.token")
                if str(var.check_myaccts_ad) != str(check_md_ad):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("alldebrid.username")
                        your_token = myaccts.getSetting("alldebrid.token")
                
                        addon = xbmcaddon.Addon("plugin.video.magicdragon")
                        addon.setSetting("alldebrid.username", your_username)
                        addon.setSetting("alldebrid.token", your_token)

                        d_select = ("2")
                        addon.setSetting("debrid_select", d_select)


#Asgard AD
def asgardad_auth():

        if xbmcvfs.exists(var.check_addon_asgard) and xbmcvfs.exists(var.check_asgard_settings):
                check_asgard_ad = xbmcaddon.Addon('plugin.video.asgard').getSetting("alldebrid.token")
                if str(var.check_myaccts_ad) != str(check_asgard_ad):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("alldebrid.username")
                        your_token = myaccts.getSetting("alldebrid.token")
                
                        addon = xbmcaddon.Addon("plugin.video.asgard")
                        addon.setSetting("alldebrid.username", your_username)
                        addon.setSetting("alldebrid.token", your_token)

                        d_select = ("2")
                        addon.setSetting("debrid_select", d_select)


#M.E.T.V AD
def metvad_auth():

        if xbmcvfs.exists(var.check_addon_metv) and xbmcvfs.exists(var.check_metv_settings):
                check_metv_ad = xbmcaddon.Addon('plugin.video.metv19').getSetting("alldebrid.token")
                if str(var.check_myaccts_ad) != str(check_metv_ad):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("alldebrid.username")
                        your_token = myaccts.getSetting("alldebrid.token")
                
                        addon = xbmcaddon.Addon("plugin.video.metv19")
                        addon.setSetting("alldebrid.username", your_username)
                        addon.setSetting("alldebrid.token", your_token)

                        d_select = ("2")
                        addon.setSetting("debrid_select", d_select)


#ResolveURL AD
def rurlad_auth():

        if xbmcvfs.exists(var.check_addon_rurl) and xbmcvfs.exists(var.check_rurl_settings):
                check_rurl_ad = xbmcaddon.Addon('script.module.resolveurl').getSetting("AllDebridResolver_token")
                if str(var.check_myaccts_ad) != str(check_rurl_ad):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("alldebrid.username")
                        your_token = myaccts.getSetting("alldebrid.token")
                
                        addon = xbmcaddon.Addon("script.module.resolveurl")
                        addon.setSetting("AllDebridResolver_client_id", your_username)
                        addon.setSetting("AllDebridResolver_token", your_token)

                        cache_only = ("true")
                        addon.setSetting("AllDebridResolver_cached_only", cache_only)


#My Accounts AD
def myaccountsad_auth():

        if xbmcvfs.exists(var.check_addon_myaccounts) and xbmcvfs.exists(var.check_myaccounts_settings):
                check_myaccounts_ad = xbmcaddon.Addon('script.module.myaccounts').getSetting("alldebrid.token")
                if str(var.check_myaccts_ad) != str(check_myaccounts_ad):
                
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("alldebrid.username")
                        your_token = myaccts.getSetting("alldebrid.token")
                
                        addon = xbmcaddon.Addon("script.module.myaccounts")
                        addon.setSetting("alldebrid.username", your_username)
                        addon.setSetting("alldebrid.token", your_token)


def debrid_auth_ad(): #Sync all add-ons
        if str(var.check_myaccts_ad) != '': #Check to make sure Account Manager is authorized
                serenad_auth()
                ezraad_auth()
                fenad_auth()
                povad_auth()
                umbad_auth()
                shadowad_auth()
                ghostad_auth()
                unleashedad_auth()
                chainsad_auth()
                moriaad_auth()
                basead_auth()
                twistedad_auth()
                mdad_auth()
                asgardad_auth()
                metvad_auth()
                rurlad_auth()
                myaccountsad_auth()
