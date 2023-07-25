import xbmc, xbmcaddon
import xbmcvfs
from pathlib import Path
from accountmgr.modules import control
from libs.common import var

class Auth:
    def premiumize_auth(self):
    #Seren PM
        try:
                if xbmcvfs.exists(var.chk_seren) and xbmcvfs.exists(var.chkset_seren): #Check that the addon is installed and settings.xml exists
                        chk_auth_seren = xbmcaddon.Addon('plugin.video.seren').getSetting("premiumize.token")
                        chk_auth_seren_rd = xbmcaddon.Addon('plugin.video.seren').getSetting("rd.auth")
                        chk_auth_seren_ad = xbmcaddon.Addon('plugin.video.seren').getSetting("alldebrid.apikey")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_seren) or str(chk_auth_seren) == '': #Compare Account Mananger token to Add-on token. If they match authorization is skipped

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                                
                                #Write debrid data to settings.xml
                                addon = xbmcaddon.Addon("plugin.video.seren")
                                addon.setSetting("premiumize.username", your_username)
                                addon.setSetting("premiumize.token", your_token)

                                premium_stat = ("Premium")
                                addon.setSetting("premiumize.premiumstatus", premium_stat)
                                
                                #Set enabled for authorized debrid services
                                enabled_pm = ("true")
                                addon.setSetting("premiumize.enabled", enabled_pm)

                                if str(chk_auth_seren_rd) != '': #Check if Real-Debrid is authorized
                                        enabled_rd = ("true")
                                        addon.setSetting("realdebrid.enabled", enabled_rd)
                                else:
                                        enabled_rd = ("false")
                                        addon.setSetting("realdebrid.enabled", enabled_rd)
                        
                                if str(chk_auth_seren_ad) != '': #Check if All-Debrid is authorized
                                        enabled_ad = ("true")
                                        addon.setSetting("alldebrid.enabled", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("alldebrid.enabled", enabled_ad)
        except:
                pass

    #Ezra PM
        try:
                if xbmcvfs.exists(var.chk_ezra) and xbmcvfs.exists(var.chkset_ezra):
                        chk_auth_ezra = xbmcaddon.Addon('plugin.video.ezra').getSetting("pm.token")
                        chk_auth_ezra_rd = xbmcaddon.Addon('plugin.video.ezra').getSetting("rd.token")
                        chk_auth_ezra_ad = xbmcaddon.Addon('plugin.video.ezra').getSetting("ad.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_ezra) or str(chk_auth_ezra) == '':

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.ezra")
                                addon.setSetting("pm.account_id", your_username)
                                addon.setSetting("pm.token", your_token)

                                enabled_pm = ("true")
                                addon.setSetting("pm.enabled", enabled_pm)

                                if str(chk_auth_ezra_rd) != '':
                                        enabled_rd = ("true")
                                        addon.setSetting("rd.enabled", enabled_rd)
                                else:
                                        enabled_rd = ("false")
                                        addon.setSetting("rd.enabled", enabled_rd)

                                if str(chk_auth_ezra_ad) != '':
                                        enabled_ad = ("true")
                                        addon.setSetting("ad.enabled", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("ad.enabled", enabled_ad)
        except:
                pass

    #Fen PM
        try:
                if xbmcvfs.exists(var.chk_fen) and xbmcvfs.exists(var.chkset_fen):
                        chk_auth_fen = xbmcaddon.Addon('plugin.video.fen').getSetting("pm.token")
                        chk_auth_fen_rd = xbmcaddon.Addon('plugin.video.fen').getSetting("rd.token")
                        chk_auth_fen_ad = xbmcaddon.Addon('plugin.video.fen').getSetting("ad.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_fen) or str(chk_auth_fen) == '':

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.fen")
                                addon.setSetting("pm.account_id", your_username)
                                addon.setSetting("pm.token", your_token)

                                enabled_pm = ("true")
                                addon.setSetting("pm.enabled", enabled_pm)

                                if str(chk_auth_fen_rd) != '':
                                        enabled_rd = ("true")
                                        addon.setSetting("rd.enabled", enabled_rd)
                                else:
                                        enabled_rd = ("false")
                                        addon.setSetting("rd.enabled", enabled_rd)

                                if str(chk_auth_fen_ad) != '':
                                        enabled_ad = ("true")
                                        addon.setSetting("ad.enabled", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("ad.enabled", enabled_ad)
        except:
                pass

    #POV PM
        try:
                if xbmcvfs.exists(var.chk_pov) and xbmcvfs.exists(var.chkset_pov):
                        chk_auth_pov = xbmcaddon.Addon('plugin.video.pov').getSetting("pm.token")
                        chk_auth_pov_rd = xbmcaddon.Addon('plugin.video.pov').getSetting("rd.token")
                        chk_auth_pov_ad = xbmcaddon.Addon('plugin.video.pov').getSetting("ad.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_pov) or str(chk_auth_pov) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.pov")
                                addon.setSetting("pm.account_id", your_username)
                                addon.setSetting("pm.token", your_token)

                                enabled_pm = ("true")
                                addon.setSetting("pm.enabled", enabled_pm)

                                if str(chk_auth_pov_rd) != '':
                                        enabled_rd = ("true")
                                        addon.setSetting("rd.enabled", enabled_rd)
                                else:
                                        enabled_rd = ("false")
                                        addon.setSetting("rd.enabled", enabled_rd)

                                if str(chk_auth_pov_ad) != '':
                                        enabled_ad = ("true")
                                        addon.setSetting("ad.enabled", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("ad.enabled", enabled_ad)
        except:
                pass                

    #Umbrella PM
        try:
                if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb):
                        chk_auth_umb = xbmcaddon.Addon('plugin.video.umbrella').getSetting("premiumizetoken")
                        chk_auth_umb_rd = xbmcaddon.Addon('plugin.video.umbrella').getSetting("realdebridtoken")
                        chk_auth_umb_ad = xbmcaddon.Addon('plugin.video.umbrella').getSetting("alldebridtoken")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_umb) or str(chk_auth_umb) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.umbrella")
                                addon.setSetting("premiumizeusername", your_username)
                                addon.setSetting("premiumizetoken", your_token)

                                enabled_pm = ("true")
                                addon.setSetting("premiumize.enabled", enabled_pm)

                                if str(chk_auth_umb_rd) != '':
                                        enabled_rd = ("true")
                                        addon.setSetting("alldebrid.enabled", enabled_rd)
                                else:
                                        enabled_rd = ("false")
                                        addon.setSetting("realdebrid.enabled", enabled_rd)

                                if str(chk_auth_umb_ad) != '':
                                        enabled_ad = ("true")
                                        addon.setSetting("alldebrid.enabled", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("alldebrid.enabled", enabled_ad)
        except:
                pass
        
    #Shadow PM
        try:
                if xbmcvfs.exists(var.chk_shadow) and xbmcvfs.exists(var.chkset_shadow):
                        chk_auth_shadow = xbmcaddon.Addon('plugin.video.shadow').getSetting("premiumize.token")
                        chk_auth_shadow_rd = xbmcaddon.Addon('plugin.video.shadow').getSetting("rd.auth")
                        chk_auth_shadow_ad = xbmcaddon.Addon('plugin.video.shadow').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_shadow) or str(chk_auth_shadow) == '':

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.shadow")
                                addon.setSetting("premiumize.token", your_token)

                                pm_use = ("true")
                                addon.setSetting("debrid_use_pm", pm_use)

                                if str(chk_auth_shadow_rd) != '':
                                        rd_use = ("true")
                                        addon.setSetting("debrid_use_rd", rd_use)
                                else:
                                        rd_use = ("false")
                                        addon.setSetting("debrid_use_rd", rd_use)
                        
                                if str(chk_auth_shadow_ad) != '':
                                        ad_use = ("true")
                                        addon.setSetting("debrid_use_ad", ad_use)
                                else:
                                        ad_use = ("false")
                                        addon.setSetting("debrid_use_ad", ad_use)
        except:
                pass
        
    #Ghost PM
        try:
                if xbmcvfs.exists(var.chk_ghost) and xbmcvfs.exists(var.chkset_ghost):
                        chk_auth_ghost = xbmcaddon.Addon('plugin.video.ghost').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_ghost) or str(chk_auth_ghost) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.ghost")
                                addon.setSetting("premiumize.token", your_token)

                                rd_use = ("false")
                                addon.setSetting("debrid_use_rd", rd_use)

                                pm_use = ("true")
                                addon.setSetting("debrid_use_pm", pm_use)

                                ad_use = ("false")
                                addon.setSetting("debrid_use_ad", ad_use)

                                d_select = ("1")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

    #Unleashed PM
        try:
                if xbmcvfs.exists(var.chk_unleashed) and xbmcvfs.exists(var.chkset_unleashed):
                        chk_auth_unleashed = xbmcaddon.Addon('plugin.video.unleashed').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_unleashed) or str(chk_auth_unleashed) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.unleashed")
                                addon.setSetting("premiumize.token", your_token)

                                d_select = ("1")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

    #Chains PM
        try:
                if xbmcvfs.exists(var.chk_chains) and xbmcvfs.exists(var.chkset_chains):
                        chk_auth_chains = xbmcaddon.Addon('plugin.video.thechains').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_chains) or str(chk_auth_chains) == '':

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.thechains")
                                addon.setSetting("premiumize.token", your_token)

                                d_select = ("1")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

    #Twisted PM
        try:
                if xbmcvfs.exists(var.chk_twisted) and xbmcvfs.exists(var.chkset_twisted):
                        chk_auth_twisted = xbmcaddon.Addon('plugin.video.twisted').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_twisted) or str(chk_auth_twisted) == '':
                        
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.twisted")
                                addon.setSetting("premiumize.token", your_token)

                                d_select = ("1")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

    #Base19 PM
        try:
                if xbmcvfs.exists(var.chk_base) and xbmcvfs.exists(var.chkset_base):
                        chk_auth_base = xbmcaddon.Addon('plugin.video.base19').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_base) or str(chk_auth_base) == '':
                        
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.base19")
                                addon.setSetting("premiumize.token", your_token)

                                d_select = ("1")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

    #Magic Dragon PM
        try:
                if xbmcvfs.exists(var.chk_md) and xbmcvfs.exists(var.chkset_md):
                        chk_auth_md = xbmcaddon.Addon('plugin.video.magicdragon').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_md) or str(chk_auth_md) == '':
                        
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.magicdragon")
                                addon.setSetting("premiumize.token", your_token)

                                d_select = ("1")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

    #Asgard PM
        try:
                if xbmcvfs.exists(var.chk_asgard) and xbmcvfs.exists(var.chkset_asgard):
                        chk_auth_asgard = xbmcaddon.Addon('plugin.video.asgard').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_asgard) or str(chk_auth_asgard) == '':
                        
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.asgard")
                                addon.setSetting("premiumize.token", your_token)

                                d_select = ("1")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

    #M.E.T.V PM
        try:
                if xbmcvfs.exists(var.chk_metv) and xbmcvfs.exists(var.chkset_metv):
                        chk_auth_metv = xbmcaddon.Addon('plugin.video.metv19').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_metv) or str(chk_auth_metv) == '':
                        
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.metv19")
                                addon.setSetting("premiumize.token", your_token)

                                d_select = ("1")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

    #Aliunde PM
        try:
                if xbmcvfs.exists(var.chk_aliunde) and xbmcvfs.exists(var.chkset_aliunde):
                        chk_auth_aliunde = xbmcaddon.Addon('plugin.video.aliundek19').getSetting("premiumize.token")
                        chk_auth_aliunde_rd = xbmcaddon.Addon('plugin.video.aliundek19').getSetting("rd.auth")
                        chk_auth_aliunde_ad = xbmcaddon.Addon('plugin.video.aliundek19').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_aliunde) or str(chk_auth_aliunde) == '':

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.aliundek19")
                                addon.setSetting("premiumize.token", your_token)

                                pm_use = ("true")
                                addon.setSetting("debrid_use_pm", pm_use)

                                if str(chk_auth_shadow_rd) != '':
                                        rd_use = ("true")
                                        addon.setSetting("debrid_use_rd", rd_use)
                                else:
                                        rd_use = ("false")
                                        addon.setSetting("debrid_use_rd", rd_use)
                        
                                if str(chk_auth_shadow_ad) != '':
                                        ad_use = ("true")
                                        addon.setSetting("debrid_use_ad", ad_use)
                                else:
                                        ad_use = ("false")
                                        addon.setSetting("debrid_use_ad", ad_use)
        except:
                pass
        
    #Patriot PM
        try:
                if xbmcvfs.exists(var.chk_patriot) and xbmcvfs.exists(var.chkset_patriot):
                        chk_auth_patriot = xbmcaddon.Addon('plugin.video.patriot').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_patriot) or str(chk_auth_patriot) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.patriot")
                                addon.setSetting("premiumize.token", your_token)

                                rd_use = ("false")
                                addon.setSetting("debrid_use_rd", rd_use)

                                pm_use = ("true")
                                addon.setSetting("debrid_use_pm", pm_use)

                                ad_use = ("false")
                                addon.setSetting("debrid_use_ad", ad_use)

                                d_select = ("1")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass
        
    #Adina RD
        try:
                if xbmcvfs.exists(var.chk_adina) and xbmcvfs.exists(var.chkset_adina):
                        chk_auth_adina = xbmcaddon.Addon('plugin.video.adina').getSetting("pm.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_adina) or str(chk_auth_adina) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.adina")
                                addon.setSetting("pm.account_id", your_username)
                                addon.setSetting("pm.token", your_token)
        except:
                pass
        
    #Artemis RD
        try:
                if xbmcvfs.exists(var.chk_artemis) and xbmcvfs.exists(var.chkset_artemis):
                        chk_auth_artemis = xbmcaddon.Addon('plugin.video.artemis').getSetting("premiumize.token")
                        chk_auth_artemis_rd = xbmcaddon.Addon('plugin.video.artemis').getSetting("realdebrid.token")
                        chk_auth_artemis_ad = xbmcaddon.Addon('plugin.video.artemis').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_artemis) or str(chk_auth_artemis) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.artemis")
                                addon.setSetting("premiumize.username", your_username)
                                addon.setSetting("premiumize.token", your_token)
                                
                                enabled_pm = ("true")
                                addon.setSetting("premiumize.enabled", enabled_pm)

                                if str(chk_auth_artemis_rd) != '':
                                        enabled_rd = ("true")
                                        addon.setSetting("realdebrid.enabled", enabled_rd)
                                else:
                                        enabled_rd = ("false")
                                        addon.setSetting("realdebrid.enabled", enabled_rd)
                        
                                if str(chk_auth_artemis_ad) != '':
                                        enabled_ad = ("true")
                                        addon.setSetting("alldebrid.enabled", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("alldebrid.enabled", enabled_ad)
        except:
                pass
        
    #Dynasty RD
        try:
                if xbmcvfs.exists(var.chk_dyna) and xbmcvfs.exists(var.chkset_dyna):
                        chk_auth_dyna = xbmcaddon.Addon('plugin.video.dynasty').getSetting("premiumize.token")
                        chk_auth_dyna_rd = xbmcaddon.Addon('plugin.video.dynasty').getSetting("realdebrid.token")
                        chk_auth_dyna_ad = xbmcaddon.Addon('plugin.video.dynasty').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_dyna) or str(chk_auth_dyna) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.dynasty")
                                addon.setSetting("premiumize.username", your_username)
                                addon.setSetting("premiumize.token", your_token)

                                enabled_rd = ("true")
                                addon.setSetting("realdebrid.enabled", enabled_rd)

                                enabled_pm = ("true")
                                addon.setSetting("premiumize.enabled", enabled_pm)

                                if str(chk_auth_dyna_rd) != '':
                                        enabled_rd = ("true")
                                        addon.setSetting("realdebrid.enabled", enabled_rd)
                                else:
                                        enabled_rd = ("false")
                                        addon.setSetting("realdebrid.enabled", enabled_rd)
                        
                                if str(chk_auth_dyna_ad) != '':
                                        enabled_ad = ("true")
                                        addon.setSetting("alldebrid.enabled", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("alldebrid.enabled", enabled_ad)
        except:
                pass

    #Loonatics Empire
        try:
                if xbmcvfs.exists(var.chk_loon) and xbmcvfs.exists(var.chkset_loon):
                        chk_auth_loon = xbmcaddon.Addon('plugin.video.le').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_loon) or str(chk_auth_loon) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.le")
                                addon.setSetting("premiumize.username", your_username)
                                addon.setSetting("premiumize.token", your_token)
        except:
                pass
        
    #ResolveURL PM
        try:
                if xbmcvfs.exists(var.chk_rurl) and xbmcvfs.exists(var.chkset_rurl):
                        chk_auth_rurl = xbmcaddon.Addon('script.module.resolveurl').getSetting("PremiumizeMeResolver_token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_rurl) or str(chk_auth_rurl) == '':
                        
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("script.module.resolveurl")
                                addon.setSetting("PremiumizeMeResolver_token", your_token)

                                cache_only = ("true")
                                addon.setSetting("PremiumizeMeResolver_cached_only", cache_only)
        except:
                pass

    #My Accounts PM
        try:
                if xbmcvfs.exists(var.chk_myaccounts) and xbmcvfs.exists(var.chkset_myaccounts):
                        chk_auth_myaccounts = xbmcaddon.Addon('script.module.myaccounts').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_myaccounts) or str(chk_auth_myaccounts) == '':
                        
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("script.module.myaccounts")
                                addon.setSetting("premiumize.username", your_username)

                                your_token = accountmgr.getSetting("premiumize.token")
                                addon.setSetting("premiumize.token", your_token)
        except:
                pass

    #Your Accounts PM
        try:
                if xbmcvfs.exists(var.chk_youraccounts) and xbmcvfs.exists(var.chkset_youraccounts):
                        chk_auth_youraccounts = xbmcaddon.Addon('script.module.youraccounts').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_youraccounts) or str(chk_auth_youraccounts) == '':
                        
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("script.module.youraccounts")
                                addon.setSetting("premiumize.username", your_username)

                                your_token = accountmgr.getSetting("premiumize.token")
                                addon.setSetting("premiumize.token", your_token)
        except:
                pass
        
    #Premiumizer PM
        try:
                if xbmcvfs.exists(var.chk_premiumizer) and xbmcvfs.exists(var.chkset_premiumizer):
                        chk_auth_premiumizer = xbmcaddon.Addon('plugin.video.premiumizerx').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_premiumizer) or str(chk_auth_premiumizer) == '':
                        
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("premiumize.username")
                                your_token = accountmgr.getSetting("premiumize.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.premiumizerx")
                                addon.setSetting("premiumize.token", your_token)
        except:
                pass
