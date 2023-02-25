import datetime
import random
import string
import requests
import xbmcaddon
import xbmc
from urllib.parse import urlparse, urlunparse

def text2hex(text):
    return text.encode("utf-8").hex()

def hex2text(hex):
    return bytes.fromhex(hex).decode('utf-8')

def getTimeshift():
    # https://stackoverflow.com/questions/2720319/python-figure-out-local-timezone
    LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    seconds = LOCAL_TIMEZONE.utcoffset(datetime.datetime.now()).seconds
    if seconds == 0: return "0"
    else: return str(seconds / 60 / 60).split(".")[0]
    
def getPISCTimeShift():
    TS = getTimeshift()
    if TS == "0": return "0"
    else: return str(int(TS) * -1)

def urljoin(base, part2):
    parsed = urlparse(base)

    if part2.startswith("http"):
        return part2

    if part2.startswith("/"):
        return urlunparse(
            (
                parsed.scheme,
                parsed.netloc,
                part2,
                "",
                "",
                "",
            )
        )

    if part2.startswith("/") == False:
        if "." in parsed.path.split("/")[-1]:
            base = base.replace(f'/{parsed.path.split("/")[-1]}', "")

        if parsed.path.endswith("/"):
            return base + part2
        else:
            return base + "/" + part2

def randString(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def getIP():
    return requests.get("https://api.my-ip.io/ip").text

def getCountry():
    data = requests.get(f"https://ipinfo.io/{getIP()}/json")
    return data.json()['country']

def isIPCZSK():
    return getCountry() in ["CZ", "SK"]

def getLocalIP():
    return xbmc.getIPAddress()

def getAllowed():
    allowed = []
    _ADDON = xbmcaddon.Addon()
    if _ADDON.getSettingBool("CSEnabled"): # and isIPCZSK()
        allowed.append("SK"); allowed.append("CZ"); allowed.append("CS")
    if _ADDON.getSettingBool("USEnabled"): allowed.append("US")
    if _ADDON.getSettingBool("USRegionalEnabled"): allowed.append("USRegional")
    if _ADDON.getSettingBool("USLocalEnabled"): allowed.append("USLocal")
    if _ADDON.getSettingBool("UKEnabled"): allowed.append("UK")
    return allowed

def stopifPlaying():
    if xbmc.Player().isPlaying():
        xbmc.Player().stop()