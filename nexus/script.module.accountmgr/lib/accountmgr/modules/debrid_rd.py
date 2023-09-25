import xbmc, xbmcaddon
import xbmcvfs
import json
from pathlib import Path
from accountmgr.modules import control
from libs.common import var

class Auth:
    def realdebrid_auth(self):
    #Seren RD
        try:
                if xbmcvfs.exists(var.chk_seren) and xbmcvfs.exists(var.chkset_seren): #Check that the addon is installed and settings.xml exists
                        chk_auth_seren = xbmcaddon.Addon('plugin.video.seren').getSetting("rd.auth")
                        chk_auth_seren_pm = xbmcaddon.Addon('plugin.video.seren').getSetting("premiumize.token")
                        chk_auth_seren_ad = xbmcaddon.Addon('plugin.video.seren').getSetting("alldebrid.apikey")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_seren) or str(chk_auth_seren) == '': #Compare Account Mananger token to Add-on token. If they match authorization is skipped

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                                
                                #Write debrid data to settings.xml
                                addon = xbmcaddon.Addon("plugin.video.seren")
                                addon.setSetting("rd.username", your_username)
                                addon.setSetting("rd.auth", your_token)
                                addon.setSetting("rd.client_id", your_client_id)
                                addon.setSetting("rd.refresh", your_refresh)
                                addon.setSetting("rd.secret", your_secret)

                                premium_stat = ("Premium")
                                addon.setSetting("realdebrid.premiumstatus", premium_stat)
                                
                                #Set enabled for authorized debrid services
                                enabled_rd = ("true")
                                addon.setSetting("realdebrid.enabled", enabled_rd)
                        
                                if str(chk_auth_seren_pm) != '': #Check if Premiumize is authorized
                                        enabled_pm = ("true")
                                        addon.setSetting("premiumize.enabled", enabled_pm)
                                else:
                                        enabled_pm = ("false")
                                        addon.setSetting("premiumize.enabled", enabled_pm)

                                if str(chk_auth_seren_ad) != '': #Check if All-Debrid is authorized
                                        enabled_ad = ("true")
                                        addon.setSetting("alldebrid.enabled", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("alldebrid.enabled", enabled_ad)
        except:
                pass

    #Fen RD
        try:
                if xbmcvfs.exists(var.chk_fen) and xbmcvfs.exists(var.chkset_fen):
                        chk_auth_fen = xbmcaddon.Addon('plugin.video.fen').getSetting("rd.token")
                        chk_auth_fen_pm = xbmcaddon.Addon('plugin.video.fen').getSetting("pm.token")
                        chk_auth_fen_ad = xbmcaddon.Addon('plugin.video.fen').getSetting("ad.token")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_fen) or str(chk_auth_fen) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                        
                                addon = xbmcaddon.Addon("plugin.video.fen")
                                addon.setSetting("rd.account_id", your_username)
                                addon.setSetting("rd.token", your_token)
                                addon.setSetting("rd.client_id", your_client_id)
                                addon.setSetting("rd.refresh", your_refresh)
                                addon.setSetting("rd.secret", your_secret)

                                enabled_rd = ("true")
                                addon.setSetting("rd.enabled", enabled_rd)

                                if str(chk_auth_fen_pm) != '':
                                        enabled_pm = ("true")
                                        addon.setSetting("pm.enabled", enabled_pm)
                                else:
                                        enabled_pm = ("false")
                                        addon.setSetting("pm.enabled", enabled_pm)
                        
                                if str(chk_auth_fen_ad) != '':
                                        enabled_ad = ("true")
                                        addon.setSetting("ad.enabled", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("ad.enabled", enabled_ad)
        except:
                pass
            
    #Ezra RD
        try:
                if xbmcvfs.exists(var.chk_ezra) and xbmcvfs.exists(var.chkset_ezra):
                        chk_auth_ezra = xbmcaddon.Addon('plugin.video.ezra').getSetting("rd.token")
                        chk_auth_ezra_pm = xbmcaddon.Addon('plugin.video.ezra').getSetting("pm.token")
                        chk_auth_ezra_ad = xbmcaddon.Addon('plugin.video.ezra').getSetting("ad.token")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_ezra) or str(chk_auth_ezra) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                        
                                addon = xbmcaddon.Addon("plugin.video.ezra")
                                addon.setSetting("rd.username", your_username)
                                addon.setSetting("rd.token", your_token)
                                addon.setSetting("rd.client_id", your_client_id)
                                addon.setSetting("rd.refresh", your_refresh)
                                addon.setSetting("rd.secret", your_secret)

                                enabled_rd = ("true")
                                addon.setSetting("rd.enabled", enabled_rd)

                                if str(chk_auth_ezra_pm) != '':
                                        enabled_pm = ("true")
                                        addon.setSetting("pm.enabled", enabled_pm)
                                else:
                                        enabled_pm = ("false")
                                        addon.setSetting("pm.enabled", enabled_pm)
                        
                                if str(chk_auth_ezra_ad) != '':
                                        enabled_ad = ("true")
                                        addon.setSetting("ad.enabled", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("ad.enabled", enabled_ad)
        except:
                pass

    #Coalition RD
        try:
                if xbmcvfs.exists(var.chk_coal) and xbmcvfs.exists(var.chkset_coal):
                        chk_auth_coal = xbmcaddon.Addon('plugin.video.coalition').getSetting("rd.token")
                        chk_auth_coal_pm = xbmcaddon.Addon('plugin.video.coalition').getSetting("pm.token")
                        chk_auth_coal_ad = xbmcaddon.Addon('plugin.video.coalition').getSetting("ad.token")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_coal) or str(chk_auth_coal) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                        
                                addon = xbmcaddon.Addon("plugin.video.coalition")
                                addon.setSetting("rd.username", your_username)
                                addon.setSetting("rd.token", your_token)
                                addon.setSetting("rd.client_id", your_client_id)
                                addon.setSetting("rd.refresh", your_refresh)
                                addon.setSetting("rd.secret", your_secret)

                                enabled_rd = ("true")
                                addon.setSetting("rd.enabled", enabled_rd)

                                if str(chk_auth_coal_pm) != '':
                                        enabled_pm = ("true")
                                        addon.setSetting("pm.enabled", enabled_pm)
                                else:
                                        enabled_pm = ("false")
                                        addon.setSetting("pm.enabled", enabled_pm)
                        
                                if str(chk_auth_coal_ad) != '':
                                        enabled_ad = ("true")
                                        addon.setSetting("ad.enabled", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("ad.enabled", enabled_ad)
        except:
                pass
            
    #POV RD
        try:
                if xbmcvfs.exists(var.chk_pov) and xbmcvfs.exists(var.chkset_pov):
                        chk_auth_pov = xbmcaddon.Addon('plugin.video.pov').getSetting("rd.token")
                        chk_auth_pov_pm = xbmcaddon.Addon('plugin.video.pov').getSetting("pm.token")
                        chk_auth_pov_ad = xbmcaddon.Addon('plugin.video.pov').getSetting("ad.token")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_pov) or str(chk_auth_pov) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                        
                                addon = xbmcaddon.Addon("plugin.video.pov")
                                addon.setSetting("rd.username", your_username)
                                addon.setSetting("rd.token", your_token)
                                addon.setSetting("rd.client_id", your_client_id)
                                addon.setSetting("rd.refresh", your_refresh)
                                addon.setSetting("rd.secret", your_secret)

                                enabled_rd = ("true")
                                addon.setSetting("rd.enabled", enabled_rd)

                                if str(chk_auth_pov_pm) != '':
                                        enabled_pm = ("true")
                                        addon.setSetting("pm.enabled", enabled_pm)
                                else:
                                        enabled_pm = ("false")
                                        addon.setSetting("pm.enabled", enabled_pm)
                        
                                if str(chk_auth_pov_ad) != '':
                                        enabled_ad = ("true")
                                        addon.setSetting("ad.enabled", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("ad.enabled", enabled_ad)
        except:
                pass

    #Umbrella RD
        try:
                if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb):
                        chk_auth_umb = xbmcaddon.Addon('plugin.video.umbrella').getSetting("realdebridtoken")
                        chk_auth_umb_pm = xbmcaddon.Addon('plugin.video.umbrella').getSetting("premiumizetoken")
                        chk_auth_umb_ad = xbmcaddon.Addon('plugin.video.umbrella').getSetting("alldebridtoken")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_umb) or str(chk_auth_umb) == '':
                        
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                        
                                addon = xbmcaddon.Addon("plugin.video.umbrella")
                                addon.setSetting("realdebridusername", your_username)
                                addon.setSetting("realdebridtoken", your_token)
                                addon.setSetting("realdebrid.clientid", your_client_id)
                                addon.setSetting("realdebridrefresh", your_refresh)
                                addon.setSetting("realdebridsecret", your_secret)

                                enabled_rd = ("true")
                                addon.setSetting("realdebrid.enabled", enabled_rd)

                 
                                if str(chk_auth_umb_pm) != '':
                                        enabled_pm = ("true")
                                        addon.setSetting("premiumize.enabled", enabled_pm)
                                else:
                                        enabled_pm = ("false")
                                        addon.setSetting("premiumize.enabled", enabled_pm)

                                if str(chk_auth_umb_ad) != '':
                                        enabled_ad = ("true")
                                        addon.setSetting("alldebrid.enabled", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("alldebrid.enabled", enabled_ad)
        except:
                pass

    #Shadow RD
        try:
                if xbmcvfs.exists(var.chk_shadow) and xbmcvfs.exists(var.chkset_shadow):
                        chk_auth_shadow = xbmcaddon.Addon('plugin.video.shadow').getSetting("rd.auth")
                        chk_auth_shadow_pm = xbmcaddon.Addon('plugin.video.shadow').getSetting("premiumize.token")
                        chk_auth_shadow_ad = xbmcaddon.Addon('plugin.video.shadow').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_shadow) or str(chk_auth_shadow) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                        
                                addon = xbmcaddon.Addon("plugin.video.shadow")
                                addon.setSetting("rd.auth", your_token)
                                addon.setSetting("rd.client_id", your_client_id)
                                addon.setSetting("rd.refresh", your_refresh)
                                addon.setSetting("rd.secret", your_secret)

                                rd_use = ("true")
                                addon.setSetting("debrid_use_rd", rd_use)

                                if str(chk_auth_shadow_pm) != '':
                                        pm_use = ("true")
                                        addon.setSetting("debrid_use_pm", pm_use)
                                else:
                                        pm_use = ("false")
                                        addon.setSetting("debrid_use_pm", pm_use)
                                        
                                if str(chk_auth_shadow_ad) != '':
                                        ad_use = ("true")
                                        addon.setSetting("debrid_use_ad", ad_use)
                                else:
                                        ad_use = ("false")
                                        addon.setSetting("debrid_use_ad", ad_use)
        except:
                pass
        
    #Ghost RD
        try:
                if xbmcvfs.exists(var.chk_ghost) and xbmcvfs.exists(var.chkset_ghost):
                        chk_auth_ghost = xbmcaddon.Addon('plugin.video.ghost').getSetting("rd.auth")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_ghost) or str(chk_auth_ghost) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                        
                                addon = xbmcaddon.Addon("plugin.video.ghost")
                                addon.setSetting("rd.auth", your_token)
                                addon.setSetting("rd.client_id", your_client_id)
                                addon.setSetting("rd.refresh", your_refresh)
                                addon.setSetting("rd.secret", your_secret)

                                d_use = ("true")
                                addon.setSetting("debrid_use", d_use)
                                
                                d_select = ("0")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

    #Base 19 RD
        try:
                if xbmcvfs.exists(var.chk_base) and xbmcvfs.exists(var.chkset_base):
                        chk_auth_base = xbmcaddon.Addon('plugin.video.base19').getSetting("rd.auth")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_base) or str(chk_auth_base) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                        
                                addon = xbmcaddon.Addon("plugin.video.base19")
                                addon.setSetting("rd.auth", your_token)
                                addon.setSetting("rd.client_id", your_client_id)
                                addon.setSetting("rd.refresh", your_refresh)
                                addon.setSetting("rd.secret", your_secret)

                                d_select = ("0")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass
            
    #Unleashed RD
        try:
                if xbmcvfs.exists(var.chk_unleashed) and xbmcvfs.exists(var.chkset_unleashed):
                        chk_auth_unleashed = xbmcaddon.Addon('plugin.video.unleashed').getSetting("rd.auth")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_unleashed) or str(chk_auth_unleashed) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                        
                                addon = xbmcaddon.Addon("plugin.video.unleashed")
                                addon.setSetting("rd.auth", your_token)
                                addon.setSetting("rd.client_id", your_client_id)
                                addon.setSetting("rd.refresh", your_refresh)
                                addon.setSetting("rd.secret", your_secret)
                                
                                d_use = ("true")
                                addon.setSetting("debrid_use", d_use)
                                
                                d_select = ("0")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

    #Chains RD
        try:
                if xbmcvfs.exists(var.chk_chains) and xbmcvfs.exists(var.chkset_chains):
                        chk_auth_chains = xbmcaddon.Addon('plugin.video.thechains').getSetting("rd.auth")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_chains) or str(chk_auth_chains) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                        
                                addon = xbmcaddon.Addon("plugin.video.thechains")
                                addon.setSetting("rd.auth", your_token)
                                addon.setSetting("rd.client_id", your_client_id)
                                addon.setSetting("rd.refresh", your_refresh)
                                addon.setSetting("rd.secret", your_secret)

                                d_use = ("true")
                                addon.setSetting("debrid_use", d_use)
                                
                                d_select = ("0")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

    #Twisted RD
        try:
                if xbmcvfs.exists(var.chk_twisted) and xbmcvfs.exists(var.chkset_twisted):
                        chk_auth_twisted = xbmcaddon.Addon('plugin.video.twisted').getSetting("rd.auth")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_twisted) or str(chk_auth_twisted) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                        
                                addon = xbmcaddon.Addon("plugin.video.twisted")
                                addon.setSetting("rd.auth", your_token)
                                addon.setSetting("rd.client_id", your_client_id)
                                addon.setSetting("rd.refresh", your_refresh)
                                addon.setSetting("rd.secret", your_secret)

                                d_use = ("true")
                                addon.setSetting("debrid_use", d_use)
                                
                                d_select = ("0")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass
            
    #Magic Dragon RD
        try:
                if xbmcvfs.exists(var.chk_md) and xbmcvfs.exists(var.chkset_md):
                        chk_auth_md = xbmcaddon.Addon('plugin.video.magicdragon').getSetting("rd.auth")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_md) or str(chk_auth_md) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                        
                                addon = xbmcaddon.Addon("plugin.video.magicdragon")
                                addon.setSetting("rd.auth", your_token)
                                addon.setSetting("rd.client_id", your_client_id)
                                addon.setSetting("rd.refresh", your_refresh)
                                addon.setSetting("rd.secret", your_secret)

                                d_use = ("true")
                                addon.setSetting("debrid_use", d_use)
                                
                                d_select = ("0")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

    #Asgard RD
        try:
                if xbmcvfs.exists(var.chk_asgard) and xbmcvfs.exists(var.chkset_asgard):
                        chk_auth_asgard = xbmcaddon.Addon('plugin.video.asgard').getSetting("rd.auth")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_asgard) or str(chk_auth_asgard) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                        
                                addon = xbmcaddon.Addon("plugin.video.asgard")
                                addon.setSetting("rd.auth", your_token)
                                addon.setSetting("rd.client_id", your_client_id)
                                addon.setSetting("rd.refresh", your_refresh)
                                addon.setSetting("rd.secret", your_secret)

                                d_use = ("true")
                                addon.setSetting("debrid_use", d_use)
                                
                                d_select = ("0")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

    #Patriot RD
        try:
                if xbmcvfs.exists(var.chk_patriot) and xbmcvfs.exists(var.chkset_patriot):
                        chk_auth_patriot = xbmcaddon.Addon('plugin.video.patriot').getSetting("rd.auth")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_patriot) or str(chk_auth_patriot) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                        
                                addon = xbmcaddon.Addon("plugin.video.patriot")
                                addon.setSetting("rd.auth", your_token)
                                addon.setSetting("rd.client_id", your_client_id)
                                addon.setSetting("rd.refresh", your_refresh)
                                addon.setSetting("rd.secret", your_secret)

                                d_select = ("0")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

    #Black Lightning RD
        try:
                if xbmcvfs.exists(var.chk_blackl) and xbmcvfs.exists(var.chkset_blackl):
                        chk_auth_blackl = xbmcaddon.Addon('plugin.video.blacklightning').getSetting("rd.auth")
                        chk_auth_blackl_pm = xbmcaddon.Addon('plugin.video.blacklightning').getSetting("premiumize.token")
                        chk_auth_blackl_ad = xbmcaddon.Addon('plugin.video.blacklightning').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_blackl) or str(chk_auth_blackl) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                        
                                addon = xbmcaddon.Addon("plugin.video.blacklightning")
                                addon.setSetting("rd.auth", your_token)
                                addon.setSetting("rd.client_id", your_client_id)
                                addon.setSetting("rd.refresh", your_refresh)
                                addon.setSetting("rd.secret", your_secret)

                                rd_use = ("true")
                                addon.setSetting("debrid_use_rd", rd_use)

                                if str(chk_auth_blackl_pm) != '':
                                        pm_use = ("true")
                                        addon.setSetting("debrid_use_pm", pm_use)
                                else:
                                        pm_use = ("false")
                                        addon.setSetting("debrid_use_pm", pm_use)
                                        
                                if str(chk_auth_blackl_ad) != '':
                                        ad_use = ("true")
                                        addon.setSetting("debrid_use_ad", ad_use)
                                else:
                                        ad_use = ("false")
                                        addon.setSetting("debrid_use_ad", ad_use)
        except:
                pass

    #M.E.T.V RD
        try:
                if xbmcvfs.exists(var.chk_metv) and xbmcvfs.exists(var.chkset_metv):
                        chk_auth_metv = xbmcaddon.Addon('plugin.video.metv19').getSetting("rd.auth")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_metv) or str(chk_auth_metv) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                        
                                addon = xbmcaddon.Addon("plugin.video.metv19")
                                addon.setSetting("rd.auth", your_token)
                                addon.setSetting("rd.client_id", your_client_id)
                                addon.setSetting("rd.refresh", your_refresh)
                                addon.setSetting("rd.secret", your_secret)

                                d_use = ("true")
                                addon.setSetting("debrid_use", d_use)
                                
                                d_select = ("0")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

    #Aliunde RD
        try:
                if xbmcvfs.exists(var.chk_aliunde) and xbmcvfs.exists(var.chkset_aliunde):
                        chk_auth_aliunde = xbmcaddon.Addon('plugin.video.aliundek19').getSetting("rd.auth")
                        chk_auth_aliunde_pm = xbmcaddon.Addon('plugin.video.aliundek19').getSetting("premiumize.token")
                        chk_auth_aliunde_ad = xbmcaddon.Addon('plugin.video.aliundek19').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_aliunde) or str(chk_auth_aliunde) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                        
                                addon = xbmcaddon.Addon("plugin.video.aliundek19")
                                addon.setSetting("rd.auth", your_token)
                                addon.setSetting("rd.client_id", your_client_id)
                                addon.setSetting("rd.refresh", your_refresh)
                                addon.setSetting("rd.secret", your_secret)

                                rd_use = ("true")
                                addon.setSetting("debrid_use_rd", rd_use)

                                if str(chk_auth_aliunde_pm) != '':
                                        pm_use = ("true")
                                        addon.setSetting("debrid_use_pm", pm_use)
                                else:
                                        pm_use = ("false")
                                        addon.setSetting("debrid_use_pm", pm_use)
                                        
                                if str(chk_auth_aliunde_ad) != '':
                                        ad_use = ("true")
                                        addon.setSetting("debrid_use_ad", ad_use)
                                else:
                                        ad_use = ("false")
                                        addon.setSetting("debrid_use_ad", ad_use)
        except:
                pass

    #My Accounts RD
        try:
                if xbmcvfs.exists(var.chk_myaccounts) and xbmcvfs.exists(var.chkset_myaccounts):
                        chk_auth_myaccounts = xbmcaddon.Addon('script.module.myaccounts').getSetting("realdebrid.token")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_myaccounts) or str(chk_auth_myaccounts) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                        
                                addon = xbmcaddon.Addon("script.module.myaccounts")
                                addon.setSetting("realdebrid.username", your_username)
                                addon.setSetting("realdebrid.token", your_token)
                                addon.setSetting("realdebrid.client_id", your_client_id)
                                addon.setSetting("realdebrid.refresh", your_refresh)
                                addon.setSetting("realdebrid.secret", your_secret)
        except:
                pass
            
    #ResolveURL RD
        try:
                if xbmcvfs.exists(var.chk_rurl) and xbmcvfs.exists(var.chkset_rurl):
                        chk_auth_rurl = xbmcaddon.Addon('script.module.resolveurl').getSetting("RealDebridResolver_token")
                        if not str(var.chk_accountmgr_tk_rd) == str(chk_auth_rurl) or str(chk_auth_rurl) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("realdebrid.username")
                                your_token = accountmgr.getSetting("realdebrid.token")
                                your_client_id = accountmgr.getSetting("realdebrid.client_id")
                                your_refresh = accountmgr.getSetting("realdebrid.refresh")
                                your_secret = accountmgr.getSetting("realdebrid.secret")
                        
                                addon = xbmcaddon.Addon("script.module.resolveurl")
                                addon.setSetting("RealDebridResolver_login", your_username)
                                addon.setSetting("RealDebridResolver_token", your_token)
                                addon.setSetting("RealDebridResolver_client_id", your_client_id)
                                addon.setSetting("RealDebridResolver_refresh", your_refresh)
                                addon.setSetting("RealDebridResolver_client_secret", your_secret)

                                cache_only = ("true")
                                addon.setSetting("RealDebridResolver_cached_only", cache_only)
        except:
                pass
