import requests
import json
import os
from bilibili.downloader import Downloader

class BilibiliVideo:
    __headers = {}
    __video_url = "Hello World"
    __audio_url = "Hello World"
    __bvid = ""
    __cid = ""
    __file_name = ""
    __video_name = __file_name + " (video)"
    __audio_name = __file_name + " (audio)"

    def __init__(self, bvid):
        self.__bvid = bvid
        self.__headers = {
            "referer": "https://www.bilibili.com/video/{bvid}".format(bvid = self.__bvid),
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"
        }

    def search_bilivideo_detail(self, part=0):
        url = "https://api.bilibili.com/x/web-interface/view?bvid={bvid}".format(bvid = self.__bvid)
        
        r = requests.get(url, headers=self.__headers)
        detail = json.loads(r.text)

        self.__file_name = detail["data"]["pages"][part]["part"]
        self.__video_name = self.__file_name + " (video)"
        self.__audio_name = self.__file_name + " (audio)"
        self.__cid = detail["data"]["pages"][part]["cid"]

    def __search_base_json(self):
        url = "https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&qn=120&otype=json&fourk=1&fnever=0&fnval=16".format(bvid = self.__bvid, cid = self.__cid)
        
        r = requests.get(url, headers=self.__headers)
        return json.loads(r.text)

    def search_all_url(self):
        self.__video_url = str(self.__search_base_json()["data"]["dash"]["video"][0]["base_url"])
        self.__audio_url = str(self.__search_base_json()["data"]["dash"]["audio"][0]["base_url"])

    def run_ffmpeg(self):
        cmd = "ffmpeg -i \"{video}.m4s\" -i \"{audio}.m4s\" -codec copy \"{file_name}\".mp4".format(video = self.__video_name, audio = self.__audio_name, file_name = self.__file_name)
        os.system(cmd)

    def remove_fake(self):
        os.remove(self.__video_name + ".m4s")
        os.remove(self.__audio_name + ".m4s")
        os.remove(self.__video_name + ".txt")
        os.remove(self.__audio_name + ".txt")

    def download_bilibili_video(self):


        self.search_bilivideo_detail()
        self.__search_base_json()
        self.search_all_url()
        
        downloader1 = Downloader(self.__video_url, self.__bvid, self.__video_name)
        downloader1.write_aria2_txt()
        downloader1.run_aria2c()

        downloader2 = Downloader(self.__audio_url, self.__bvid, self.__audio_name)
        downloader2.write_aria2_txt()
        downloader2.run_aria2c()

        self.run_ffmpeg()
        self.remove_fake()