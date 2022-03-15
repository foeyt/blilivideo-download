from bilibili.bilibili_video import BilibiliVideo

bvid = input("输入你所需要下载的视频的BV号：")

if __name__ == "__main__":
    bilibili = BilibiliVideo(bvid)
    bilibili.download_bilibili_video()