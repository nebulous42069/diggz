# -*- coding: utf-8 -*-
               
#Credit to JewBMX for base code

import threading


class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self, target=self._target, args=self._args)


