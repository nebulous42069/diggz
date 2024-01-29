import os
import shutil
import subprocess
import xbmcgui
import xbmcvfs
import xbmc, xbmcaddon
dialog = xbmcgui.Dialog()
settings_path = xbmcvfs.translatePath('special://userdata/addon_data/skin.xenonxfree/')

def Xenon_Widget_Flavors():
        flavor_list = ['[COLOR chartreuse]Xenon FREE-Restore Default Setup[/COLOR]']
        select = dialog.select('Reset To Defaults',flavor_list)
        if select == None:
            return
   

        if select == 0:
                src_settings = xbmcvfs.translatePath('special://home/addons/script.module.xenonfree/resources/switch/Xenon_Free/settings.xml')
                dst_settings = xbmcvfs.translatePath('special://userdata/addon_data/skin.xenonxfree/settings.xml')
                
                if os.path.exists(os.path.join(settings_path)):
                        try:
                                shutil.copyfile(src_settings, dst_settings)
                                xbmcgui.Dialog().ok('Xenon Plus Switcher', 'To save skin changes, please close Kodi, Press OK to force close Kodi')
                                os._exit(1)
                        except:
                                xbmcgui.Dialog().ok('Xenon Plus Switcher', 'Error switching skin, please contact developer')
                else:
                        xbmcgui.Dialog().ok('Xenon Plus Switcher', 'Error switching skin, please contact developer')                        
                 
