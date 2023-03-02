import xbmc
from ResolveURL import server as ResolveURL_Server
from ResolveURL import preload as ResolveURL_Preloader
from resources.utils.server import server as Falcon_Server
import threading

if __name__ == '__main__':
    monitor = xbmc.Monitor()
    #threading.Thread(target=ResolveURL_Preloader).start()
    threading.Thread(target=ResolveURL_Server, args=(23569, )).start()
    threading.Thread(target=Falcon_Server, args=(24569, )).start()
    while not monitor.abortRequested():
        if monitor.waitForAbort(1 * 60 * 60): break
