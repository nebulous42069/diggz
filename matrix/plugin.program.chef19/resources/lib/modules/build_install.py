import os
import xbmc
import xbmcvfs
import xbmcaddon
from .downloader import Downloader
import json
import time
from zipfile import ZipFile
from .save_data import save_backup_restore
from .maintenance import fresh_start, truncate_tables
from .addonvar import dp, dialog, zippath, addon_name, home, setting_set, local_string
from xml.etree import ElementTree as ET
from pathlib import Path
import shutil

addons_path = Path(xbmcvfs.translatePath('special://home/addons'))
user_data = Path(xbmcvfs.translatePath('special://userdata'))
binaries_path = Path(xbmcvfs.translatePath(xbmcaddon.Addon().getAddonInfo('profile'))) / 'binaries.json'

def main(name, name2, version, url):
    yesInstall = dialog.yesno(name, local_string(30028), nolabel=local_string(30029), yeslabel=local_string(30030))  # Ready to install, Cancel, Continue
    if yesInstall:
        save_backup_restore('backup')
        fresh_start()
        build_install(name, name2, version, url)
    else:
        return

def build_install(name, name2, version, url):
    if os.path.exists(zippath):
        os.unlink(zippath)
    d = Downloader(url)
    if 'dropbox' in url:
        if not xbmc.getCondVisibility('System.HasAddon(script.module.requests)'):
            xbmc.executebuiltin('InstallAddon(script.module.requests)')
            dialog.ok(name, local_string(30033))  # Installing Requests
            return
        d.download_build(name, zippath, meth='requests')
    else:
        d.download_build(name, zippath, meth='urllib')
    if os.path.exists(zippath):
        dp.create(addon_name, local_string(30034))  # Extracting files
        counter = 1
        with ZipFile(zippath, 'r') as z:
            files = z.infolist()
            for file in files:
                filename = file.filename
                progress_percentage = int(counter/len(files)*100)
                try:
                    z.extract(file, home)
                except Exception as e:
                    xbmc.log(f'Error extracting {filename} - {e}', xbmc.LOGINFO)
                dp.update(progress_percentage, f'{local_string(30034)}...\n{progress_percentage}%\n{filename}')
                counter += 1
        dp.update(100, local_string(30035))  # Done Extracting
        xbmc.sleep(500)
        dp.close()
        os.unlink(zippath)
        save_backup_restore('restore')
        setting_set('buildname', name2)
        setting_set('buildversion', version)
        setting_set('update_passed', 'false')
        setting_set('firstrun', 'true')
        check_binary()
        repo_rollback()
        truncate_tables()
        dialog.ok(addon_name, local_string(30036))  # Install Complete
        os._exit(1)
    else:
        return

def repo_rollback():
        import sqlite3

        db = xbmcvfs.translatePath('special://database/') + 'Addons33.db'
        try:
                con = sqlite3.connect(db)
                cursor = con.cursor()
                cursor.execute(
        """UPDATE repo SET version = 0 WHERE addonID = "repository.xbmc.org";
""",
        )
                con.commit()
        except sqlite3.Error as e:
                xbmc.log(f"Failed to write data to the sqlite table: {e}", xbmc.LOGINFO)
        finally:
            if con:
                xbmc.sleep(1000)
                xbmc.executebuiltin('UpdateAddonRepos')
                xbmc.sleep(5000)

def check_binary():
    binary_list = []
    for folder in addons_path.iterdir():
        if folder.is_dir():
            addon_xml = folder / 'addon.xml'
            if addon_xml.exists():
              with open(addon_xml, 'r', encoding='utf-8', errors='ignore') as f:
                  _xml = f.read()
              if 'kodi.binary' in _xml:
                  try:
                      root = ET.fromstring(_xml)
                      binary_list.append(root.attrib['id'])
                  except:
                      binary_list.append(folder.name)
                  try:
                      shutil.rmtree(folder)
                  except PermissionError as e:
                      xbmc.log(f'Unable to delete binary {folder} - {e}')
    if len(binary_list) > 0:
        with open(binaries_path, 'w', encoding='utf-8') as f:
            json.dump({'items': binary_list}, f, indent = 4)

def restore_binary():
    with open(binaries_path, 'r', encoding='utf-8', errors='ignore') as f:
        binaries_list = json.loads(f.read())['items']
    failed = []
    for plugin_id in binaries_list:
        install = install_addon(plugin_id)
        if install is not True:
            failed.append(plugin_id)
    if len(failed) == 0:
        binaries_path.unlink()
    else:
        with open(binaries_path, 'w', encoding='utf-8') as f:
            json.dump({'items': failed}, f, indent = 4)

def install_addon(plugin_id):
    if xbmc.getCondVisibility(f'System.HasAddon({plugin_id})'):
        return True
    xbmc.executebuiltin(f'InstallAddon({plugin_id})')
    clicked = False
    start = time.time()
    timeout = 20
    while not xbmc.getCondVisibility(f'System.HasAddon({plugin_id})'):
        if time.time() >= start + timeout:
            return False
        xbmc.sleep(500)
        if xbmc.getCondVisibility('Window.IsTopMost(yesnodialog)') and not clicked:
            xbmc.executebuiltin('SendClick(yesnodialog, 11)')
            clicked = True
    return True

# Binaries inspired Dr. Infernoo
