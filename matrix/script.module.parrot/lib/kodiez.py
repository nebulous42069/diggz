import xbmcplugin
import xbmcgui
import xbmc
import xbmcvfs
import requests
import shutil
import os
import zipfile


class KodiEZ():
    def __init__(self, ADDON, HANDLE):
        self.ADDON = ADDON
        self.HANDLE = HANDLE

    def inpt(self, title, hidden):
        xbmcplugin.setContent(self.HANDLE, 'videos')
        kb = xbmc.Keyboard('', title, hidden)
        kb.doModal()
        query = ""
        if kb.isConfirmed():
            query = kb.getText()
        return query

    def addItemToScreen(self, name, genre, icon, url, isFolder):
        list_item = xbmcgui.ListItem(label=name)
        list_item.setInfo('video', {'title': name,
                                    'genre': genre,
                                    'plot': name,
                                    'mediatype': 'video'})
        list_item.setArt({'thumb': icon, 'icon': icon, 'fanart': icon})
        list_item.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(self.HANDLE, url, list_item, isFolder)

    def updateAddon(self, url):
        pb = xbmcgui.DialogProgress()
        filename = url.split('/')[-1]
        packageDir = xbmcvfs.translatePath("special://home/addons/packages/")
        addonsDir = xbmcvfs.translatePath("special://home/addons/")
        addonDir = xbmcvfs.translatePath("special://home/addons/{id}/".format(id=self.ADDON.getAddonInfo('id')))

        pb.create("Downloading", "Downloading addon zip file")
        with open(packageDir + filename, 'wb') as f:
            f.write(requests.get(url).content)

        pb.update(25, "Removing old addon")
        for file in os.listdir(addonDir):
            if os.path.isdir(addonDir + file):
                shutil.rmtree(addonDir + file)
            else:
                os.remove(addonDir + file)

        pb.update(50, "Extracting zip file")
        with zipfile.ZipFile(packageDir + filename, 'r') as zip_ref:
            zip_ref.extractall(addonsDir)

        pb.update(75, "Removing zip file")
        os.remove(packageDir + filename)
        xbmc.executebuiltin('UpdateLocalAddons')
        xbmc.executebuiltin('UpdateAddonRepos')
        pb.update(100, "Done")
        pb.close()