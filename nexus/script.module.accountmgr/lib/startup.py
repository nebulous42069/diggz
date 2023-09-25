import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon
import os.path
import time
from libs.common import var
from accountmgr.modules import control
from accountmgr.modules import log_utils
import _strptime

LOGINFO = 1

timeout_start = time.time()
timeout = 60*5
                                
def startup_sync():
        try:
                if str(var.chk_accountmgr_tk) != '': #Skip sync if Trakt is not authorized
                        from accountmgr.modules import trakt_sync
                        trakt_sync.Auth().trakt_auth() #Sync Trakt
        except:
                pass
        try:
                if str(var.chk_accountmgr_tk_rd) != '': #Skip sync if Real-Debrid is not authorized
                        from accountmgr.modules import debrid_rd
                        debrid_rd.Auth().realdebrid_auth() #Sync Real-Debrid
        except:
                pass
        try:
                if str(var.chk_accountmgr_tk_pm) != '': #Skip sync if Premiumize is not authorized
                        from accountmgr.modules import debrid_pm
                        debrid_pm.Auth().premiumize_auth() #Sync Premiumize
        except:
                pass
        try:
                if str(var.chk_accountmgr_tk_ad) != '': #Skip sync if All-Debrid is not authorized
                        from accountmgr.modules import debrid_ad 
                        debrid_ad.Auth().alldebrid_auth() #Sync All-Debrid
        except:
                pass

def startup_nondebrid_sync():
        try:    #Skip sync if no data is available to sync
                if str(var.chk_accountmgr_furk) != '':
                        from accountmgr.modules import furk_sync
                        furk_sync.Auth().furk_auth() #Sync Data
        except:
                pass
        
        try:    #Skip sync if no data is available to sync
                if str(var.chk_accountmgr_easy) != '':
                        from accountmgr.modules import easy_sync
                        easy_sync.Auth().easy_auth() #Sync Data
        except:
                pass
        
        try:    #Skip sync if no data is available to sync
                if str(var.chk_accountmgr_file) != '':
                        from accountmgr.modules import filepursuit_sync
                        filepursuit_sync.Auth().file_auth() #Sync Data
        except:
                pass
        
def startup_meta_sync():
        try:    #Skip sync if no Metadata is available to sync
                if str(var.chk_accountmgr_fanart) != '' or str(var.chk_accountmgr_omdb) != '' or str(var.chk_accountmgr_mdb) != '' or str(var.chk_accountmgr_imdb) != '' or str(var.chk_accountmgr_tmdb) != '' or str(var.chk_accountmgr_tmdb_user) != '' or str(var.chk_accountmgr_tvdb) != '':
                        from accountmgr.modules import meta_sync
                        meta_sync.Auth().meta_auth() #Sync Metadata
        except:
                pass
        
class AddonCheckUpdate:
	def run(self):
		xbmc.log('[ script.module.accountmgr ]  Addon checking available updates', LOGINFO)
		try:
			import re
			import requests
			repo_xml = requests.get('https://raw.githubusercontent.com/Zaxxon709/nexus/main/zips/script.module.accountmgr/addon.xml')
			if repo_xml.status_code != 200:
				return xbmc.log('[ script.module.accountmgr ]  Could not connect to remote repo XML: status code = %s' % repo_xml.status_code, LOGINFO)
			repo_version = re.search(r'<addon id=\"script.module.accountmgr\".*version=\"(\d*.\d*.\d*)\"', repo_xml.text, re.I).group(1)
			local_version = control.addonVersion()[:5] # 5 char max so pre-releases do try to compare more chars than github version
			def check_version_numbers(current, new): # Compares version numbers and return True if github version is newer
				current = current.split('.')
				new = new.split('.')
				step = 0
				for i in current:
					if int(new[step]) > int(i): return True
					if int(i) > int(new[step]): return False
					if int(i) == int(new[step]):
						step += 1
						continue
				return False
			if check_version_numbers(local_version, repo_version):
				while control.condVisibility('Library.IsScanningVideo'):
					control.sleep(10000)
				xbmc.log('[ script.module.accountmgr ]  A newer version is available. Installed Version: v%s' % (local_version), LOGINFO)
				control.notification(message=control.lang(32072) % repo_version, time=5000)
			return xbmc.log('[ script.module.accountmgr ]  Addon update check complete', LOGINFO)
		except:
			import traceback
			traceback.print_exc()
			
def api_check():

        while True:
                if time.time() > timeout_start + timeout: #Time out after 5min
                        break

                if xbmcvfs.exists(var.chk_seren) and xbmcvfs.exists(var.chkset_seren) and str(var.chk_accountmgr_tk) != '' and var.setting('traktuserkey.enabled') == 'true': #Check that the addon is installed, settings.xml exists and Account Manager is authorized
                        with open(var.path_seren) as f: #Check add-on for Account Manager API keys. If found, move on to next add-on
                                if var.chk_api in f.read():
                                        pass
                                else:   #Insert Account Mananger API keys into add-on
                                        f = open(var.path_seren,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.seren_client,var.client_am).replace(var.seren_secret,var.secret_am)
                                        f = open(var.path_seren,'w')
                                        f.write(client)
                                        f.close()
                                        continue
                                
                if xbmcvfs.exists(var.chk_fen) and xbmcvfs.exists(var.chkset_fen) and str(var.chk_accountmgr_tk) != '':
                        with open(var.path_fen) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:   
                                        f = open(var.path_fen,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.fen_client,var.client_am).replace(var.fen_secret,var.secret_am)
                                        f = open(var.path_fen,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_coal) and xbmcvfs.exists(var.chkset_coal) and str(var.chk_accountmgr_tk) != '':
                        with open(var.path_coal) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:   
                                        f = open(var.path_coal,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.coal_client,var.client_am).replace(var.coal_secret,var.secret_am)
                                        f = open(var.path_coal,'w')
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

                if xbmcvfs.exists(var.chk_base) and xbmcvfs.exists(var.chkset_base) and str(var.chk_accountmgr_tk) != '':
                        with open(var.path_base) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.path_base,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.base_client,var.client_am).replace(var.base_secret,var.secret_am)
                                        f = open(var.path_base,'w')
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

                if xbmcvfs.exists(var.chk_patriot) and xbmcvfs.exists(var.chkset_patriot) and str(var.chk_accountmgr_tk) != '':
                        with open(var.path_patriot) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.path_patriot,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.patriot_client,var.client_am).replace(var.patriot_secret,var.secret_am)
                                        f = open(var.path_patriot,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_blackl) and xbmcvfs.exists(var.chkset_blackl) and str(var.chk_accountmgr_tk) != '':
                        with open(var.path_blackl) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.path_blackl,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.blackl_client,var.client_am).replace(var.blackl_secret,var.secret_am)
                                        f = open(var.path_blackl,'w')
                                        f.write(client)
                                        f.close()
                                        continue
                                
                if xbmcvfs.exists(var.chk_aliunde) and xbmcvfs.exists(var.chkset_aliunde) and str(var.chk_accountmgr_tk) != '':
                        with open(var.path_aliunde) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.path_aliunde,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.aliunde_client,var.client_am).replace(var.aliunde_secret,var.secret_am)
                                        f = open(var.path_aliunde,'w')
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
                                
                if xbmcvfs.exists(var.chk_scrubs) and xbmcvfs.exists(var.chkset_scrubs) and str(var.chk_accountmgr_tk) != '':
                        with open(var.path_scrubs) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.path_scrubs,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.scrubs_client,var.client_am).replace(var.scrubs_secret,var.secret_am)
                                        f = open(var.path_scrubs,'w')
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

if var.setting('sync.nondebrid.service')=='true': #Check if service is enabled
        startup_nondebrid_sync() #Start service
else:
        pass

if var.setting('sync.metaservice')=='true': #Check if service is enabled
        startup_meta_sync() #Start service
else:
        pass

if var.setting('checkAddonUpdates') == 'true': #Check if service is enabled
	AddonCheckUpdate().run() #Start service
else:
        pass

if var.setting('trakt.service')=='true': #Check if service is enabled
        api_check() #Start service
else:
        quit()
