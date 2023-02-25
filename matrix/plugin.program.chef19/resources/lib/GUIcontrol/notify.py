import xbmcgui
from urllib.request import Request, urlopen
from uservar import notify_url

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

req = Request(notify_url, headers=headers)
response = urlopen(req).read().decode('utf-8')

try:
    split_response = response.split('|||')
    notify_version = int(split_response[0])
    message = split_response[1]

except:
    notify_version = 0
    message = 'Improper Notifications format. Please check the Notifications text.'

def get_notifyversion():
    return notify_version

KEY_NAV_BACK = 92
TEXTBOX = 300
CLOSEBUTTON = 302

class notify(xbmcgui.WindowXMLDialog):
    
    def onInit(self):
        self.getControl(TEXTBOX).setText(message)

    def onAction(self,action):
        if action.getId() == KEY_NAV_BACK:
            self.Close()

    def onClick(self,controlId):
        if controlId == CLOSEBUTTON:
            self.Close()

    def Close(self):
        self.close()