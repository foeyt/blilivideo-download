import os

class Downloader:
    __direct_url = ""
    __bvid = ""
    __file_name = ""

    def __init__(self, direct_url, bvid, file_name):
        self.__direct_url = direct_url
        self.__bvid = bvid
        self.__file_name = file_name

    def write_aria2_txt(self):
        aria2c_text = "{direct_url}\n  referer=https://www.bilibili.com/video/{bvid}\n  user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0\n  out={file_name}.m4s".format(direct_url = self.__direct_url, bvid = self.__bvid, file_name = self.__file_name)
        txt = open("./{file_name}.txt".format(file_name = self.__file_name), "w", encoding="utf-8")
        txt.write(aria2c_text)

        txt.close()

    def run_aria2c(self):
        cmd = "aria2c -i \"{file_name}.txt\"".format(file_name = self.__file_name)
        os.system(cmd)
