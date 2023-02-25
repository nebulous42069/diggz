from http.server import *
from socketserver import ThreadingMixIn
from urllib.parse import parse_qs
from resources.utils.recording import RECORDINGS_FOLDER
from ResolveURL import resolve
from resources.utils.common import getLocalIP, getAllowed
import os
import xbmcaddon
import xbmcvfs
import json

_ADDON = xbmcaddon.Addon()
_USERDATA = 'special://home/userdata/addon_data/'+_ADDON.getAddonInfo('id')

def recordedFile(handler):
    handler.send_response(200)
    query_string = handler.path.split('?')[1]
    query_params = parse_qs(query_string)
    id = query_params.get("id", [''])[0]
    filename = query_params.get("filename", [''])[0]

    if filename.endswith(".ts"):
        handler.send_header('Content-Type', 'video/mp2t')
    elif filename.endswith(".m3u8"):
        handler.send_header('Content-Type', 'application/vnd.apple.mpegurl')
    else:
        handler.send_header('Content-Type', 'text/plain')
    
    
    handler.end_headers()

    return open(os.path.join(RECORDINGS_FOLDER, id, filename), "rb").read()



def play(handler):
    query_string = handler.path.split('?')[1]
    query_params = parse_qs(query_string)

    rmf = resolve(
        module=query_params.get("module", [''])[0],
        channel=query_params.get("stream", [''])[0],
        data_folder=xbmcvfs.translatePath(_USERDATA + "/ResolveURL_data"),
        data_file=xbmcvfs.translatePath(_USERDATA + "/ResolveURL_data.json"),
        server_port=23569
    )

    handler.send_response(302)
    handler.send_header('Location', rmf.urlencoded().replace("127.0.0.1", getLocalIP()))
    handler.end_headers()
    return "".encode()


def playlist(handler):
    handler.send_response(200)
    try:
        query_string = handler.path.split('?')[1]
        query_params = parse_qs(query_string)
    except:
        query_params = {}
    allowed = getAllowed()

    if query_params.get("allowed", [''])[0]:
        a = query_params.get("allowed", [''])[0]
        if "|" in a: allowed = a.split("|")
        else:        allowed = [a]
    
    resp = json.load(open(os.path.join(xbmcvfs.translatePath(_USERDATA), "channels.json"), "r"))

    m3u = "#EXTM3U url-tvg=\"http://falcon-epg.pages.dev/epg.xml.gz\"\n"
    for i in resp:
        title = resp[i]["name"]
        id = resp[i]["tvg-id"]
        country = resp[i]["country"]
        logo = resp[i]["logo"]

        if country not in allowed: continue

        for source in resp[i]["sources"]:
            name = resp[i]["sources"][source]["name"]
            module = resp[i]["sources"][source]["module"]
            channel = resp[i]["sources"][source]["channel"]

            url = f"http://{getLocalIP()}:{handler.server.server_port}/play.m3u8?module={module}&stream={channel}"
            if "cardshare" in module.lower():
                url = url.replace(".m3u8", ".ts")

            m3u += f'#EXTINF:-1 tvg-logo="{logo}" tvg-id="{id}" group-title="{country} Channels" tvg-name="{title} | {name}", {title} | {name} \n'
            m3u += f"{url}\n"
    
    handler.send_header('Content-Type', 'application/vnd.apple.mpegurl')
    handler.end_headers()
    return m3u.encode()



def index(handler):
    handler.send_response(200)
    handler.send_header('Content-Type', 'text/plain')
    handler.end_headers()
    return "Falcon Web Server is running!".encode()

customRoutes = {
    "GET": {
        "/": index,
        "/recordedFile": recordedFile,
        "/recordedFile.m3u8": recordedFile,
        "/play.m3u8": play,
        "/playlist.m3u": playlist
    },
}


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class RequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.0'
    
    def do_GET(self):
        cleanPath = self.path
        if "?" in cleanPath:
            cleanPath = cleanPath.split("?")[0]

        resp = "".encode()
        if cleanPath in customRoutes["GET"]:
            resp = customRoutes["GET"][cleanPath](self)

        self.wfile.write(resp)



def server(port):
    port = ThreadedHTTPServer(('0.0.0.0', port), RequestHandler)
    port.serve_forever()