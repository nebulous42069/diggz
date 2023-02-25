import os
import json
import shutil
import time
import xbmcvfs
import xbmcaddon
import m3u8
import time
import requests
from resources.utils.common import urljoin
import threading

_ADDON = xbmcaddon.Addon()

RECORDINGS_FILE = xbmcvfs.translatePath(f"special://home/userdata/addon_data/{_ADDON.getAddonInfo('id')}/recordings.json")
RECORDINGS_FOLDER = xbmcvfs.translatePath(f"special://home/userdata/addon_data/{_ADDON.getAddonInfo('id')}/recordings")

os.makedirs(RECORDINGS_FOLDER, exist_ok=True)

if not os.path.exists(RECORDINGS_FILE):
    open(RECORDINGS_FILE, "w").write("{}")

def createCommand(url, headers, time, output):
    cmd = f"ffmpeg -t {time} -i \"{url}\" -c copy -bsf:a aac_adtstoasc {output}"
    if headers:
        for k, v in dict(headers).items():
            cmd += f" -headers \"{k}: {v}\""
    return cmd

def addRecording(name, recordingID, channelID):
    loaded = json.load(open(RECORDINGS_FILE, "r"))
    loaded[recordingID] = {
        "name": name,
        "channelID": channelID,
        "recordingID": recordingID,
        "done": False,
        "startedOn": int(time.time())
    }
    open(RECORDINGS_FILE, "w", encoding="utf-8").write(json.dumps(loaded))

def markAsDone(recordingID):
    loaded = json.load(open(RECORDINGS_FILE, "r"))
    loaded[recordingID]["done"] = True
    open(RECORDINGS_FILE, "w", encoding="utf-8").write(json.dumps(loaded))

def removeRecording(recordingID):
    loaded = json.load(open(RECORDINGS_FILE, "r"))
    del loaded[recordingID]
    open(RECORDINGS_FILE, "w", encoding="utf-8").write(json.dumps(loaded))

    if os.path.exists(os.path.join(RECORDINGS_FOLDER, recordingID)):
        shutil.rmtree(os.path.join(RECORDINGS_FOLDER, recordingID))


def getRecordings():
    return json.load(open(RECORDINGS_FILE, "r"))

def getCurrentlyRecording():
    loaded = json.load(open(RECORDINGS_FILE, "r"))

    channels = []
    for k,v in loaded.items():
        if not v["done"]:
            channels.append(v["channelID"])

    return channels




def startRecording(url, headers, length, outFolder, outID):
    os.makedirs(outFolder, exist_ok=True)

    newPlaylist = [
        "#EXTM3U",
        "#EXT-X-VERSION:3",
        "#EXT-X-ALLOW-CACHE:YES",
        "#EXT-X-PLAYLIST-TYPE:VOD",
        "#EXT-X-MEDIA-SEQUENCE:1"
    ]


    totalLen = 0
    i = 1
    while totalLen < length:
        playlist = m3u8.load(url, headers=headers, verify_ssl=False)

        if playlist.is_variant:
            newURL = urljoin(url, playlist.playlists[0].uri)
            playlist = m3u8.load(urljoin(url, newURL), headers=headers, verify_ssl=False)
            url = newURL

        for segment in playlist.segments:
            if totalLen >= length:
                break

            filename = f"chunk_{i}.ts"
            if filename in os.listdir(outFolder):
                continue


            
            if segment.key:
                uri = segment.key.uri
                key_filename = f"KEY_{filename.replace('.ts', '.bin')}"

                if "?" in key_filename:
                    key_filename = key_filename.split("?")[0]

                if uri.startswith("/"):
                    uri = urljoin(url, uri)


                open(os.path.join(outFolder, key_filename), "wb").write(requests.get(uri, headers=headers).content)
                segment.key.uri = f"/recordedFile?id={outID}&filename={key_filename}"


            totalLen += segment.duration
            open(os.path.join(outFolder, filename), "wb").write(requests.get(urljoin(url, segment.uri), headers=headers).content)
            


            # Append to output
            newPlaylist.append(f"#EXTINF:{segment.duration},")
            if segment.key:
                newPlaylist.append(f'#EXT-X-KEY:METHOD={segment.key.method},URI="{segment.key.uri}",IV={segment.key.iv}')
            newPlaylist.append(f"/recordedFile?id={outID}&filename={filename}")
            i += 1
            time.sleep(segment.duration)
        
        


    newPlaylist.append("#EXT-X-ENDLIST")
    open(os.path.join(outFolder, "playlist.m3u8"), "w").write("\n".join(newPlaylist))
    markAsDone(outID)

def record(url, headers, length, outFolder, outID):
    threading.Thread(target=startRecording, args=(url, headers, length, outFolder, outID, )).start()