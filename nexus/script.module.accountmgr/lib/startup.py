import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon
import os.path
import time
from accountmgr.modules import var

timeout_start = time.time()
timeout = 60*5
        
def startup_sync():
        try:
                if str(var.chk_accountmgr_tk) != '': #Skip sync if Trakt is not authorized
                        from accountmgr.modules import trakt_sync
                        trakt_sync.sync_all() #Sync Trakt
                if str(var.chk_accountmgr_tk_rd) != '': #Skip sync if Real-Debrid is not authorized
                        from accountmgr.modules import debrid_rd
                        debrid_rd.debrid_auth_rd() #Sync Real-Debrid
                if str(var.chk_accountmgr_tk_pm) != '': #Skip sync if Premiumize is not authorized
                        from accountmgr.modules import debrid_pm
                        debrid_pm.debrid_auth_pm() #Sync Premiumize
                if str(var.chk_accountmgr_tk_ad) != '': #Skip sync if All-Debrid is not authorized
                        from accountmgr.modules import debrid_ad 
                        debrid_ad.debrid_auth_ad() #Sync All-Debrid
        except:
                pass
def api_check():

        while True:
                if time.time() > timeout_start + timeout: #Time out after 5min
                        break
              
                if xbmcvfs.exists(var.chk_fen) and xbmcvfs.exists(var.chkset_fen) and str(var.chk_accountmgr_tk) != '': #Check that the addon is installed, settings.xml exists and Account Manager is authorized
                        with open(var.path_fen) as f: #Check add-on for Account Manager API keys. If found, move on to next add-on
                                if var.chk_api in f.read():
                                        pass
                                else:   #Insert Account Mananger API keys into add-on
                                        f = open(var.path_fen,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.fen_client,var.client_am).replace(var.fen_secret,var.secret_am)
                                        f = open(var.path_fen,'w')
                                        f.write(client)
                                        f.close()
                                        continue
         
                if xbmcvfs.exists(var.chk_pov) and xbmcvfs.exists(var.chkset_pov) and str(var.chk_accountmgr_tk) != '':
                        with open(var.path_pov) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.path_pov,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.pov_client,var.client_am).replace(var.pov_client,var.secret_am)
                                        f = open(var.path_pov,'w')
                                        f.write(client)
                                        f.close()
                                        continue
                                                                                
                if xbmcvfs.exists(var.chk_crew) and xbmcvfs.exists(var.chkset_crew) and str(var.chk_accountmgr_tk) != '':
                        with open(var.path_crew) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.path_crew,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.crew_client,var.client_am).replace(var.crew_client,var.secret_am)
                                        f = open(var.path_crew,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_shadow) and xbmcvfs.exists(var.chkset_shadow) and str(var.chk_accountmgr_tk) != '':
                        with open(var.path_shadow) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.path_shadow,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.shadow_client,var.client_am).replace(var.shadow_secret,var.secret_am)
                                        f = open(var.path_shadow,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_ghost) and xbmcvfs.exists(var.chkset_ghost) and str(var.chk_accountmgr_tk) != '':
                        with open(var.path_ghost) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.path_ghost,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.ghost_client,var.client_am).replace(var.ghost_secret,var.secret_am)
                                        f = open(var.path_ghost,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_unleashed) and xbmcvfs.exists(var.chkset_unleashed) and str(var.chk_accountmgr_tk) != '':
                        with open(var.path_unleashed) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.path_unleashed,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.unleashed_client,var.client_am).replace(var.unleashed_secret,var.secret_am)
                                        f = open(var.path_unleashed,'w')
                                        f.write(client)
                                        f.close()
                                        continue
                                        
                if xbmcvfs.exists(var.chk_chains) and xbmcvfs.exists(var.chkset_chains) and str(var.chk_accountmgr_tk) != '':
                        with open(var.path_chains) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.path_chains,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.chains_client,var.client_am).replace(var.chains_secret,var.secret_am)
                                        f = open(var.path_chains,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_md) and xbmcvfs.exists(var.chkset_md) and str(var.chk_accountmgr_tk) != '':
                        with open(var.path_md) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.path_md,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.md_client,var.client_am).replace(var.md_client,var.secret_am)
                                        f = open(var.path_md,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_asgard) and xbmcvfs.exists(var.chkset_asgard) and str(var.chk_accountmgr_tk) != '':
                        with open(var.path_asgard) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.path_asgard,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.asgard_client,var.client_am).replace(var.asgard_secret,var.secret_am)
                                        f = open(var.path_asgard,'w')
                                        f.write(client)
                                        f.close()
                                        continue
                                        
                if xbmcvfs.exists(var.chk_myaccounts) and xbmcvfs.exists(var.chkset_myaccounts) and str(var.chk_accountmgr_tk) != '':
                        with open(var.path_myaccounts) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.path_myaccounts,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.myacts_client,var.client_am).replace(var.myacts_secret,var.secret_am)
                                        f = open(var.path_myaccounts,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_tmdbh) and xbmcvfs.exists(var.chkset_tmdbh) and str(var.chk_accountmgr_tk) != '':
                        with open(var.path_tmdbh) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.path_tmdbh,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.tmdbh_client,var.client_am).replace(var.tmdbh_secret,var.secret_am)
                                        f = open(var.path_tmdbh,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_trakt) and xbmcvfs.exists(var.chkset_trakt) and str(var.chk_accountmgr_tk) != '':
                        with open(var.path_trakt) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.path_trakt,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.trakt_client,var.client_am).replace(var.trakt_secret,var.secret_am)
                                        f = open(var.path_trakt,'w')
                                        f.write(client)
                                        f.close()
                                        pass


                xbmc.sleep(10000) #Pause for 10 seconds

if var.setting('sync.service')=='true': #Check if service is enabled
        startup_sync() #Start service
else:
        pass
if var.setting('trakt.service')=='true': #Check if service is enabled
        api_check() #Start service
else:
        quit()
