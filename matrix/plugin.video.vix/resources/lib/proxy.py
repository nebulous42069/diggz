# -*- coding: utf-8 -*-


import threading

import requests,re


try:  # Python 3
	from http.server import BaseHTTPRequestHandler
except ImportError:  # Python 2
	from BaseHTTPServer import BaseHTTPRequestHandler

try:  # Python 3
	from socketserver import TCPServer
except ImportError:  # Python 2
	from SocketServer import TCPServer


import xbmcaddon, xbmc
addon = xbmcaddon.Addon('plugin.video.vix')

class Proxy(BaseHTTPRequestHandler):

	server_inst = None

	@staticmethod
	def start():
		""" Start the Proxy. """

		def start_proxy():
			""" Start the Proxy. """
			Proxy.server_inst = TCPServer(('127.0.0.1', 0), Proxy)

			port = Proxy.server_inst.socket.getsockname()[1]
			addon.setSetting('proxyport', str(port))

			Proxy.server_inst.serve_forever()

		thread = threading.Thread(target=start_proxy)
		thread.start()

		return thread

	@staticmethod
	def stop():
		""" Stop the Proxy. """
		if Proxy.server_inst:
			Proxy.server_inst.shutdown()
	def do_HEAD(self):

		self.send_response(200)
		self.end_headers()
	def do_GET(self):  
	
		path = self.path 
		if 'manifest=' in path:
			try:
				m3u_url = (path).split('manifest=')[-1]
	
				if 'manifest.mpd' in m3u_url:
	
					result = requests.get(m3u_url, verify=False, timeout = 30).text

				#	xbmc.log('manifest_datamanifest_datamanifest_datamanifest_datamanifest_datamanifest_data', level=xbmc.LOGINFO)
					self.send_response(200)
					self.send_header('Content-type', 'application/xml+dash')
					self.end_headers()

					p1 = re.findall('(<SegmentList[^>].*?<\/SegmentList>)',result,re.DOTALL)[0]
					result = result.replace(p1,'')

					self.wfile.write(result.encode())

				else:
					xbmc.log('redir_redir_redir_redir_redir_redir_redir_: %s'%str(m3u_url), level=xbmc.LOGINFO)
					self.send_response(302)
					self.send_header('Location', m3u_url)
					self.end_headers()

			except Exception as exc: 
				xbmc.log('blad w proxy: %s'%str(exc), level=xbmc.LOGINFO)
				self.send_response(500)
				self.end_headers()

