import xbmc
import xbmcvfs
import xbmcaddon
import os
import shutil
import json
from .whitelist import add_whitelist
from .addonvar import user_path, data_path, setting, addon_id, packages

user_path = xbmcvfs.translatePath('special://userdata/')
data_path = os.path.join(user_path, 'addon_data/')
text_path = os.path.join(
    xbmcvfs.translatePath(
        xbmcaddon.Addon().getAddonInfo('path')
    ), 'resources/', 'texts/'
)
    
def backup(path, file):
    if os.path.exists(os.path.join(path, file)):
        #shutil.move(os.path.join(path, file), os.path.join(packages, file))
        if os.path.isdir(os.path.join(path, file)):
            shutil.copytree(os.path.join(path, file), os.path.join(packages, file), dirs_exist_ok=True)
        else:
            xbmcvfs.copy(os.path.join(path, file), os.path.join(packages, file))

def restore(path, file):
    if os.path.exists(os.path.join(packages, file)):
        if os.path.exists(os.path.join(path, file)):
            try:
                if os.path.isfile(os.path.join(path, file)) or os.path.islink(os.path.join(path, file)):
                    os.unlink(os.path.join(path, file))
                elif os.path.isdir(os.path.join(path, file)):
                    shutil.rmtree(os.path.join(path, file))
            except Exception as e:
                xbmc.log('Failed to delete %s. Reason: %s' % (os.path.join(path, file), e), xbmc.LOGINFO)
        shutil.move(os.path.join(packages, file), os.path.join(path, file))


def save_backup_restore(_type: str) -> None:
    backup(data_path, addon_id)
    with open(os.path.join(text_path, 'backup_restore.json'), 'r', encoding='utf-8', errors='ignore') as f:
        item_list = json.loads(f.read())
        for item in item_list.keys():
            setting_id = item_list[item]['setting']
            path = item_list[item]['path']
            if path == 'user_path':
                path = user_path
            elif path == 'data_path':
                path = data_path
            try:
                if setting(setting_id)=='true':
                    if _type == 'backup':
                        backup(path, item)
                    elif _type == 'restore':
                        restore(path, item)
            except Exception as e:
                xbmc.log(f'Error= {e}', xbmc.LOGINFO)
                continue
