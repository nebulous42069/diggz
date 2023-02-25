import xbmc

if __name__ == '__main__':
    monitor = xbmc.Monitor()
    while not monitor.abortRequested():
        if monitor.waitForAbort(1 * 60 * 60): break
