
import json
import os
import pathlib
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs





class main():

	def __init__(self):
		self.dialog           = xbmcgui.Dialog()
		self.__addon__        = xbmcaddon.Addon(sys.argv[1])
		self.__addonPath__    = xbmcvfs.translatePath(self.__addon__.getAddonInfo('path'))
		self.__addonProfile__ = xbmcvfs.translatePath(self.__addon__.getAddonInfo('profile'))
		self.__addonName__    = self.__addon__.getAddonInfo('name')
		self.__addonVerison__ = self.__addon__.getAddonInfo('version')
		self.customiser_json  = os.path.join(self.__addonProfile__,'customiser.json')
		self.tempm3u_json     = os.path.join(self.__addonProfile__,'m3udata.json')
		self.files_json_path  = os.path.join(self.__addonPath__,'resources','data','files.json')
		self.files_json_data  = json.loads(self.OpenFileRead(self.files_json_path))
		self.func             = sys.argv[2]
		if self.func == 'clear_hidden':
			self.ClearHidden()
		elif self.func == 'del_temp':
			self.DelTemp()


	def ClearHidden(self):
		ret = self.dialog.yesno(self.__addonName__,'Do you wish to clear all hidden Categories and Channels?')
		if ret:
			xbmcvfs.delete(self.customiser_json)
			self.NewJsonFile(self.customiser_json,{'hidden_category':{},'hidden_channel':{}})
			self.dialog.notification(self.__addonName__, 'All Hidden cleared successfully',self.__addon__.getAddonInfo('icon'))

	def DelTemp(self):
		ret = self.dialog.yesno(self.__addonName__,'Do you wish to clear temporary and stored data files?')
		if ret:
			filetypes = list(self.files_json_data.keys())
			for filetype in filetypes:
				data = self.files_json_data.get(filetype)
				if filetype == 'json_files':
					alljsfiles = data.get('user_data')+data.get('temp_data')
					for f in alljsfiles:
						path = os.path.join(self.__addonProfile__,f.get('file'))
						a = xbmcvfs.delete(path)
						if not a:
							self.Log(f'unable to delete {path}')
						if f.get('req_start'):
							self.NewJsonFile(path,f.get('headers'))
			self.dialog.notification(self.__addonName__, 'All temporary files cleared successfully',self.__addon__.getAddonInfo('icon'))

	
	def NewJsonFile(self,filepath,headers):
		dirpath = pathlib.Path(filepath).resolve().parent
		if not dirpath.exists():
			dirpath.mkdir(parents=True, exist_ok=True)
		with open(filepath,'w') as f:
			json.dump(headers,f,indent=4)


	def OpenFileRead(self,filepath):
		f = open(filepath,'r')
		txt = f.read()
		f.close()
		return txt


	def Log(self,msg):
		if self.__addon__.getSetting('general.debug'):
			from inspect import getframeinfo, stack
			fileinfo = getframeinfo(stack()[1][0])
			xbmc.log('*__{}__{}*{} Python file name = {} Line Number = {}'.format(self.__addonName__,self.__addonVerison__,msg,fileinfo.filename,fileinfo.lineno), level=xbmc.LOGINFO)

if __name__ == '__main__':
	main()