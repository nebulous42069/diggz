# -*- coding: utf-8 -*-
"""
	Account Manager
"""

from accountmgr.modules.control import addonPath, addonVersion, joinPath
from accountmgr.windows.textviewer import TextViewerXML


def get():
	accountmgr_path = addonPath()
	accountmgr_version = addonVersion()
	changelogfile = joinPath(accountmgr_path, 'changelog.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]Account Manager -  v%s - ChangeLog[/B]' % accountmgr_version
	windows = TextViewerXML('textviewer.xml', accountmgr_path, heading=heading, text=text)
	windows.run()
	del windows

def get_supported():
	accountmgr_path = addonPath()
	accountmgr_version = addonVersion()
	changelogfile = joinPath(accountmgr_path, 'supported.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]Account Manager - Supported Add-ons[/B]'
	windows = TextViewerXML('textviewer.xml', accountmgr_path, heading=heading, text=text)
	windows.run()
	del windows
