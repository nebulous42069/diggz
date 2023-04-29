import xbmc
import json
from threading import Thread

class Monitor_Thread(Thread):

    def __init__(self):
        Thread.__init__(self)

    def raise_exc(self, excobj):
        assert self.isAlive(), "thread must be started"
        for tid, tobj in threading._active.items():
            if tobj is self:
                _async_raise(tid, excobj)
                return

    def terminate(self):
        # must raise the SystemExit type, instead of a SystemExit() instance
        # due to a bug in PyThreadState_SetAsyncExc
        self.raise_exc(SystemExit)

    class KodiMonitor(xbmc.Monitor):
        xbmc.log(str('SERVICE2')+'===>OPENINFO', level=xbmc.LOGINFO)
        xbmc.log(str('SERVICE2')+'!!===>OPENINFO', level=xbmc.LOGINFO)
        def __init__(self, **kwargs):
            xbmc.Monitor.__init__(self)
            global window
            window = None

        def terminate_mon(self):
            try: Monitor_Thread.terminate()
            except: pass

        def onNotification(self, sender, method, data):
            from resources.lib.WindowManager import wm
            global window
            try: test_window = wm.global_dialog()
            except: pass
            try:
                if not window and test_window:
                    window = test_window
                    del test_window
                    xbmc.log(str(window)+'===>OPENINFO', level=xbmc.LOGINFO)
                elif window != test_window and test_window:
                    del window
                    window = test_window
                    del test_window
                    xbmc.log(str(window)+'===>OPENINFO', level=xbmc.LOGINFO)
            except:
                pass
            #xbmc.log(str(sender)+'===>OPENINFO', level=xbmc.LOGINFO)
            if sender == 'POP_STACK':
                command_info = json.loads(data)
                #xbmc.log(str(command_info)+'onNotification===>OPENINFO', level=xbmc.LOGINFO)
                container = command_info['command_params']['container']
                position = command_info['command_params']['position']
                window.doModal()
                self.terminate_mon()
                #del window
                #window = None
                try: del wm
                except: self.terminate_mon()
                try: del monitor
                except: self.terminate_mon()
                try: del Thread
                except: self.terminate_mon()
                return
                #xbmc.log(str(wm.global_dialog())+'===>OPENINFO', level=xbmc.LOGINFO)
                for i in range(600):
                    if xbmc.getCondVisibility('Player.HasMedia'):
                        xbmc.sleep(250)
                        while xbmc.getCondVisibility('Player.HasMedia'):
                            xbmc.sleep(250)
                            while xbmc.getCondVisibility('Window.IsActive(10138)'):
                                xbmc.sleep(250)
                        xbmc.sleep(250)
                        window.doModal()
                        del window
                        window = None
                        del wm
                        del monitor
                        del Monitor_Thread
                        return
                    xbmc.sleep(50)

    #player = xbmc.Player()
    #from resources.lib.WindowManager import wm
    monitor = KodiMonitor()