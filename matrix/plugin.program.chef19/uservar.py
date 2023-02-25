import xbmcaddon

addon_id = xbmcaddon.Addon().getAddonInfo('id')

'''#####-----Build File-----#####'''
buildfile = 'https://diggz1.me/Wizard/Txts/Matrix_Builds.xml'

'''#####-----Notifications File-----#####'''
notify_url  = 'https://diggz1.me/Wizard/Txts/wizard_notify.txt'

'''#####-----Excludes-----#####'''
excludes  = [addon_id, 'packages', 'backups']
