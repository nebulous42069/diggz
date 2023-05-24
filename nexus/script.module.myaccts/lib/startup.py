import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon
import os.path
import time
from myaccts.modules import var

timeout_start = time.time()
timeout = 60*5 #Time out 5min from now

def tmdbh_check():

        if xbmcvfs.exists(var.check_addon_tmdbh) and xbmcvfs.exists(var.check_tmdbh_settings):
                if xbmcvfs.exists(var.first_check) and str(var.check) != '':
                        pass
                if not xbmcvfs.exists(var.backup_file_save) and var.second_check:
                        xbmc.sleep(15000)
                        xbmc.executebuiltin('PlayMedia(plugin://script.module.myauth/?mode=save_tmdbh&name=all)')
                if xbmcvfs.exists(var.backup_file_save):
                        if not var.third_check:
                                xbmc.sleep(15000)
                                xbmc.executebuiltin('PlayMedia(plugin://script.module.myauth/?mode=restore_tmdbh&name=all)')

def api_check():

        while True:
                if time.time() > timeout_start + timeout: #Time out after 5min
                        break
                
                if xbmcvfs.exists(var.check_addon_seren) and xbmcvfs.exists(var.check_seren_settings) and str(var.check_myaccts) != '': #Check that the addon is installed, settings.xml exists and Account Manager is authorized
                        with open(var.client_keys_seren) as f: #Check add-on for Account Manager API keys. If found, move on to next add-on
                                if var.check_api in f.read():
                                        pass
                                else:   #Insert Account Mananger API keys into add-on
                                        f = open(var.client_keys_seren,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.seren_client,var.client_am).replace(var.seren_secret,var.secret_am)
                                        f = open(var.client_keys_seren,'w')
                                        f.write(client)
                                        f.close()
                                        continue
              
                if xbmcvfs.exists(var.check_addon_fen) and xbmcvfs.exists(var.check_fen_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_fen) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_fen,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.fen_client,var.client_am).replace(var.fen_secret,var.secret_am)
                                        f = open(var.client_keys_fen,'w')
                                        f.write(client)
                                        f.close()
                                        continue
         
                if xbmcvfs.exists(var.check_addon_pov) and xbmcvfs.exists(var.check_pov_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_pov) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_pov,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.pov_client,var.client_am).replace(var.pov_client,var.secret_am)
                                        f = open(var.client_keys_pov,'w')
                                        f.write(client)
                                        f.close()
                                        continue
                                        
                if xbmcvfs.exists(var.check_addon_umb) and xbmcvfs.exists(var.check_umb_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_umb) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_umb,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.umb_client,var.client_am).replace(var.umb_secret,var.secret_am)
                                        f = open(var.client_keys_umb,'w')
                                        f.write(client)
                                        f.close()
                                        continue
                                        
                if xbmcvfs.exists(var.check_addon_home) and xbmcvfs.exists(var.check_home_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_home) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_home,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                                        f = open(var.client_keys_home,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.check_addon_genocide) and xbmcvfs.exists(var.check_genocide_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_genocide) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_genocide,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                                        f = open(var.client_keys_genocide,'w')
                                        f.write(client)
                                        f.close()
                                        continue
                                        
                if xbmcvfs.exists(var.check_addon_crew) and xbmcvfs.exists(var.check_crew_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_crew) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_crew,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.crew_client,var.client_am).replace(var.crew_client,var.secret_am)
                                        f = open(var.client_keys_crew,'w')
                                        f.write(client)
                                        f.close()
                                        continue
                                        
                if xbmcvfs.exists(var.check_addon_shazam) and xbmcvfs.exists(var.check_shazam_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_shazam) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_shazam,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                                        f = open(var.client_keys_shazam,'w')
                                        f.write(client)
                                        f.close()
                                        continue
                                        
                if xbmcvfs.exists(var.check_addon_night) and xbmcvfs.exists(var.check_night_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_night) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_night,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.night_client,var.std_client_am).replace(var.night_secret,var.std_secret_am)
                                        f = open(var.client_keys_night,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.check_addon_promise) and xbmcvfs.exists(var.check_promise_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_promise) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_promise,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                                        f = open(var.client_keys_promise,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.check_addon_scrubs) and xbmcvfs.exists(var.check_scrubs_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_scrubs) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_scrubs,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.scrubs_client,var.client_am).replace(var.scrubs_secret,var.secret_am)
                                        f = open(var.client_keys_scrubs,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.check_addon_alvin) and xbmcvfs.exists(var.check_alvin_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_alvin) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_alvin,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                                        f = open(var.client_keys_alvin,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.check_addon_shadow) and xbmcvfs.exists(var.check_shadow_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_shadow) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_shadow,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.shadow_client,var.client_am).replace(var.shadow_secret,var.secret_am)
                                        f = open(var.client_keys_shadow,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.check_addon_ghost) and xbmcvfs.exists(var.check_ghost_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_ghost) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_ghost,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.ghost_client,var.client_am).replace(var.ghost_secret,var.secret_am)
                                        f = open(var.client_keys_ghost,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.check_addon_unleashed) and xbmcvfs.exists(var.check_unleashed_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_unleashed) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_unleashed,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.unleashed_client,var.client_am).replace(var.unleashed_secret,var.secret_am)
                                        f = open(var.client_keys_unleashed,'w')
                                        f.write(client)
                                        f.close()
                                        continue
                                        
                if xbmcvfs.exists(var.check_addon_chains) and xbmcvfs.exists(var.check_chains_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_chains) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_chains,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.chains_client,var.client_am).replace(var.chains_secret,var.secret_am)
                                        f = open(var.client_keys_chains,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.check_addon_md) and xbmcvfs.exists(var.check_md_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_md) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_md,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.md_client,var.client_am).replace(var.md_client,var.secret_am)
                                        f = open(var.client_keys_md,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.check_addon_asgard) and xbmcvfs.exists(var.check_asgard_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_asgard) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_asgard,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.asgard_client,var.client_am).replace(var.asgard_secret,var.secret_am)
                                        f = open(var.client_keys_asgard,'w')
                                        f.write(client)
                                        f.close()
                                        continue
                                        
                if xbmcvfs.exists(var.check_addon_myaccounts) and xbmcvfs.exists(var.check_myaccounts_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_myaccounts) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_myaccounts,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.myacts_client,var.client_am).replace(var.myacts_secret,var.secret_am)
                                        f = open(var.client_keys_myaccounts,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.check_addon_tmdbh) and xbmcvfs.exists(var.check_tmdbh_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_tmdbh) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_tmdbh,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.tmdbh_client,var.client_am).replace(var.tmdbh_secret,var.secret_am)
                                        f = open(var.client_keys_tmdbh,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.check_addon_trakt) and xbmcvfs.exists(var.check_trakt_settings) and str(var.check_myaccts) != '':
                        with open(var.client_keys_trakt) as f:
                                if var.check_api in f.read():
                                        pass
                                else:
                                        f = open(var.client_keys_trakt,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.trakt_client,var.client_am).replace(var.trakt_secret,var.secret_am)
                                        f = open(var.client_keys_trakt,'w')
                                        f.write(client)
                                        f.close()
                                        pass


                xbmc.sleep(10000) #Pause for 10 seconds and then continue API check loop

tmdbh_check()
api_check()
