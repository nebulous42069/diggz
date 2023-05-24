import xbmc, xbmcaddon
import xbmcvfs
from pathlib import Path
from myaccts.modules import control
from myaccts.modules import var

#Seren PM
def serenpm_auth():

        if xbmcvfs.exists(var.check_addon_seren) and xbmcvfs.exists(var.check_seren_settings): #Check that the addon is installed and settings.xml exists
                check_seren_pm = xbmcaddon.Addon('plugin.video.seren').getSetting("premiumize.token")
                if str(var.check_myaccts_pm) != str(check_seren_pm): #Compare Account Mananger token to Add-on token. If they match authorization is skipped

                        #Write debrid data to the add-ons settings.xml
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("premiumize.username")
                        your_token = myaccts.getSetting("premiumize.token")

                        addon = xbmcaddon.Addon("plugin.video.seren")
                        addon.setSetting("premiumize.username", your_username)
                        addon.setSetting("premiumize.token", your_token)

                        enabled_rd = ("false")
                        addon.setSetting("realdebrid.enabled", enabled_rd)

                        enabled_pm = ("true")
                        addon.setSetting("premiumize.enabled", enabled_pm)

                        enabled_ad = ("false")
                        addon.setSetting("alldebrid.enabled", enabled_ad)


#Ezra PM
def ezrapm_auth():

        if xbmcvfs.exists(var.check_addon_ezra) and xbmcvfs.exists(var.check_ezra_settings):
                check_ezra_pm = xbmcaddon.Addon('plugin.video.ezra').getSetting("pm.token")
                if str(var.check_myaccts_pm) != str(check_ezra_pm):

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("premiumize.username")
                        your_token = myaccts.getSetting("premiumize.token")
                
                        addon = xbmcaddon.Addon("plugin.video.ezra")
                        addon.setSetting("pm.account_id", your_username)
                        addon.setSetting("pm.token", your_token)


#Fen PM
def fenpm_auth():

        if xbmcvfs.exists(var.check_addon_fen) and xbmcvfs.exists(var.check_fen_settings):
                check_fen_pm = xbmcaddon.Addon('plugin.video.fen').getSetting("pm.token")
                if str(var.check_myaccts_pm) != str(check_fen_pm):

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("premiumize.username")
                        your_token = myaccts.getSetting("premiumize.token")
                
                        addon = xbmcaddon.Addon("plugin.video.fen")
                        addon.setSetting("pm.account_id", your_username)
                        addon.setSetting("pm.token", your_token)


#POV PM
def povpm_auth():

        if xbmcvfs.exists(var.check_addon_pov) and xbmcvfs.exists(var.check_pov_settings):
                check_pov_pm = xbmcaddon.Addon('plugin.video.pov').getSetting("pm.token")
                if str(var.check_myaccts_pm) != str(check_pov_pm):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("premiumize.username")
                        your_token = myaccts.getSetting("premiumize.token")
                
                        addon = xbmcaddon.Addon("plugin.video.pov")
                        addon.setSetting("pm.account_id", your_username)
                        addon.setSetting("pm.token", your_token)
                

#Umbrella PM
def umbpm_auth():

        if xbmcvfs.exists(var.check_addon_umb) and xbmcvfs.exists(var.check_umb_settings):
                check_umb_pm = xbmcaddon.Addon('plugin.video.umbrella').getSetting("premiumize.token")
                if str(var.check_myaccts_pm) != str(check_umb_pm):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("premiumize.username")
                        your_token = myaccts.getSetting("premiumize.token")
                
                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                        addon.setSetting("premiumizeusername", your_username)
                        addon.setSetting("premiumizetoken", your_token)


#Shadow PM
def shadowpm_auth():

        if xbmcvfs.exists(var.check_addon_shadow) and xbmcvfs.exists(var.check_shadow_settings):
                check_shadow_pm = xbmcaddon.Addon('plugin.video.shadow').getSetting("premiumize.token")
                if str(var.check_myaccts_pm) != str(check_shadow_pm):

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("premiumize.username")
                        your_token = myaccts.getSetting("premiumize.token")
                
                        addon = xbmcaddon.Addon("plugin.video.shadow")
                        addon.setSetting("premiumize.token", your_token)

                        rd_use = ("false")
                        addon.setSetting("debrid_use_rd", rd_use)

                        pm_use = ("true")
                        addon.setSetting("debrid_use_pm", pm_use)

                        ad_use = ("false")
                        addon.setSetting("debrid_use_ad", ad_use)

                
#Ghost PM
def ghostpm_auth():

        if xbmcvfs.exists(var.check_addon_ghost) and xbmcvfs.exists(var.check_ghost_settings):
                check_ghost_pm = xbmcaddon.Addon('plugin.video.ghost').getSetting("premiumize.token")
                if str(var.check_myaccts_pm) != str(check_ghost_pm):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("premiumize.username")
                        your_token = myaccts.getSetting("premiumize.token")
                
                        addon = xbmcaddon.Addon("plugin.video.ghost")
                        addon.setSetting("premiumize.token", your_token)

                        rd_use = ("false")
                        addon.setSetting("debrid_use_rd", rd_use)

                        pm_use = ("true")
                        addon.setSetting("debrid_use_pm", pm_use)

                        ad_use = ("false")
                        addon.setSetting("debrid_use_ad", ad_use)


#Unleashed PM
def unleashedpm_auth():

        if xbmcvfs.exists(var.check_addon_unleashed) and xbmcvfs.exists(var.check_unleashed_settings):
                check_unleashed_pm = xbmcaddon.Addon('plugin.video.unleashed').getSetting("premiumize.token")
                if str(var.check_myaccts_pm) != str(check_unleashed_pm):
                        
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("premiumize.username")
                        your_token = myaccts.getSetting("premiumize.token")
                
                        addon = xbmcaddon.Addon("plugin.video.unleashed")
                        addon.setSetting("premiumize.token", your_token)

                        d_select = ("1")
                        addon.setSetting("debrid_select", d_select)


#Chains PM
def chainspm_auth():

        if xbmcvfs.exists(var.check_addon_chains) and xbmcvfs.exists(var.check_chains_settings):
                check_thechains_pm = xbmcaddon.Addon('plugin.video.thechains').getSetting("premiumize.token")
                if str(var.check_myaccts_pm) != str(check_thechains_pm):

                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("premiumize.username")
                        your_token = myaccts.getSetting("premiumize.token")
                
                        addon = xbmcaddon.Addon("plugin.video.thechains")
                        addon.setSetting("premiumize.token", your_token)

                        d_select = ("1")
                        addon.setSetting("debrid_select", d_select)


#Moria PM
def moriapm_auth():

        if xbmcvfs.exists(var.check_addon_moria) and xbmcvfs.exists(var.check_moria_settings):
                check_moria_pm = xbmcaddon.Addon('plugin.video.moria').getSetting("premiumize.token")
                if str(var.check_myaccts_pm) != str(check_moria_pm):
                
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("premiumize.username")
                        your_token = myaccts.getSetting("premiumize.token")
                
                        addon = xbmcaddon.Addon("plugin.video.moria")
                        addon.setSetting("premiumize.token", your_token)

                        d_select = ("1")
                        addon.setSetting("debrid_select", d_select)


#Base19 PM
def basepm_auth():

        if xbmcvfs.exists(var.check_addon_base) and xbmcvfs.exists(var.check_base_settings):
                check_base_pm = xbmcaddon.Addon('plugin.video.base19').getSetting("premiumize.token")
                if str(var.check_myaccts_pm) != str(check_base_pm):
                
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("premiumize.username")
                        your_token = myaccts.getSetting("premiumize.token")
                
                        addon = xbmcaddon.Addon("plugin.video.base19")
                        addon.setSetting("premiumize.token", your_token)

                        d_select = ("1")
                        addon.setSetting("debrid_select", d_select)


#Twisted PM
def twistedpm_auth():

        if xbmcvfs.exists(var.check_addon_twisted) and xbmcvfs.exists(var.check_twisted_settings):
                check_twisted_pm = xbmcaddon.Addon('plugin.video.twisted').getSetting("premiumize.token")
                if str(var.check_myaccts_pm) != str(check_twisted_pm):
                
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("premiumize.username")
                        your_token = myaccts.getSetting("premiumize.token")
                
                        addon = xbmcaddon.Addon("plugin.video.twisted")
                        addon.setSetting("premiumize.token", your_token)

                        d_select = ("1")
                        addon.setSetting("debrid_select", d_select)


#Magic Dragon PM
def mdpm_auth():

        if xbmcvfs.exists(var.check_addon_md) and xbmcvfs.exists(var.check_md_settings):
                check_md_pm = xbmcaddon.Addon('plugin.video.magicdragon').getSetting("premiumize.token")
                if str(var.check_myaccts_pm) != str(check_md_pm):
                
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("premiumize.username")
                        your_token = myaccts.getSetting("premiumize.token")
                
                        addon = xbmcaddon.Addon("plugin.video.magicdragon")
                        addon.setSetting("premiumize.token", your_token)

                        d_select = ("1")
                        addon.setSetting("debrid_select", d_select)


#Asgard PM
def asgardpm_auth():

        if xbmcvfs.exists(var.check_addon_asgard) and xbmcvfs.exists(var.check_asgard_settings):
                check_asgard_pm = xbmcaddon.Addon('plugin.video.asgard').getSetting("premiumize.token")
                if str(var.check_myaccts_pm) != str(check_asgard_pm):
                
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("premiumize.username")
                        your_token = myaccts.getSetting("premiumize.token")
                
                        addon = xbmcaddon.Addon("plugin.video.asgard")
                        addon.setSetting("premiumize.token", your_token)

                        d_select = ("1")
                        addon.setSetting("debrid_select", d_select)


#M.E.T.V PM
def metvpm_auth():

        if xbmcvfs.exists(var.check_addon_metv) and xbmcvfs.exists(var.check_metv_settings):
                check_metv_pm = xbmcaddon.Addon('plugin.video.metv19').getSetting("premiumize.token")
                if str(var.check_myaccts_pm) != str(check_metv_pm):
                
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("premiumize.username")
                        your_token = myaccts.getSetting("premiumize.token")
                
                        addon = xbmcaddon.Addon("plugin.video.metv19")
                        addon.setSetting("premiumize.token", your_token)

                        d_select = ("1")
                        addon.setSetting("debrid_select", d_select)


#ResolveURL PM
def rurlpm_auth():

        if xbmcvfs.exists(var.check_addon_rurl) and xbmcvfs.exists(var.check_rurl_settings):
                check_rurl_pm = xbmcaddon.Addon('script.module.resolveurl').getSetting("PremiumizeMeResolver_token")
                if str(var.check_myaccts_pm) != str(check_rurl_pm):
                
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_token = myaccts.getSetting("premiumize.token")
                
                        addon = xbmcaddon.Addon("script.module.resolveurl")
                        addon.setSetting("PremiumizeMeResolver_token", your_token)

                        cache_only = ("true")
                        addon.setSetting("PremiumizeMeResolver_cached_only", cache_only)


#My Accounts PM
def myaccountspm_auth():

        if xbmcvfs.exists(var.check_addon_myaccounts) and xbmcvfs.exists(var.check_myaccounts_settings):
                check_myaccounts_pm = xbmcaddon.Addon('script.module.myaccounts').getSetting("premiumize.token")
                if str(var.check_myaccts_pm) != str(check_myaccounts_pm):
                
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("premiumize.username")
                        your_token = myaccts.getSetting("premiumize.token")
                
                        addon = xbmcaddon.Addon("script.module.myaccounts")
                        addon.setSetting("premiumize.username", your_username)

                        your_token = myaccts.getSetting("premiumize.token")
                        addon.setSetting("premiumize.token", your_token)


#Premiumizer PM
def premiumizer_auth():

        if xbmcvfs.exists(var.check_addon_premiumizer) and xbmcvfs.exists(var.check_premiumizer_settings):
                check_premiumizer = xbmcaddon.Addon('plugin.video.premiumizerx').getSetting("premiumize.token")
                if str(var.check_myaccts_pm) != str(check_premiumizer):
                
                        myaccts = xbmcaddon.Addon("script.module.myaccts")
                        your_username = myaccts.getSetting("premiumize.username")
                        your_token = myaccts.getSetting("premiumize.token")
                
                        addon = xbmcaddon.Addon("plugin.video.premiumizerx")
                        addon.setSetting("premiumize.token", your_token)


def debrid_auth_pm(): #Sync all add-ons
        if str(var.check_myaccts_pm) != '': #Check to make sure Account Manager is authorized
                serenpm_auth()
                ezrapm_auth()
                fenpm_auth()
                povpm_auth()
                umbpm_auth()
                shadowpm_auth()
                ghostpm_auth()
                unleashedpm_auth()
                chainspm_auth()
                moriapm_auth()
                basepm_auth()
                twistedpm_auth()
                mdpm_auth()
                asgardpm_auth()
                metvpm_auth()
                rurlpm_auth()
                myaccountspm_auth()
                premiumizer_auth()
