import requests
import json
import re
import os
import sys
import time
from urllib.parse import urlparse
from urllib.parse import parse_qs
from contextlib import closing


class DouYin(object):
    def __init__(self):
        self.headers = {
            'accept': 'application/json,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        }

    def shareViedo(self, shareUrl, baseDir):
        self.baseDir = baseDir
        print("request: "+shareUrl)
        self.share_url = self.getLocation(shareUrl)
        print("request: "+self.share_url)
        share_url_parse = urlparse(self.share_url)
        shareUrlPath = list(filter(None, share_url_parse.path.split("/")))
        if "user" == shareUrlPath[1]:
            share_url_query = parse_qs(share_url_parse.query, True)
            if share_url_query.get("sec_uid"):
                sec_uid = share_url_query.get("sec_uid")[0]
                userInfo = self.getUserInfo(sec_uid)
                print(userInfo)

        else:
            # 解析视频Id
            videoId = shareUrlPath[2]
            # 获取视频信息
            videoInfo = self.getVideoInfo(videoId)
            # 将地址里的playwm改为play就是无水印播放地址了,头部user-agent需要手机user-agent
            videoInfo["mp4Url"] = videoInfo["mp4Url"].replace("playwm", "play")
            print(videoInfo)
            self.downloadVideoAndAudio(videoInfo)

    def getUserInfo(self, sec_uid):
        # 获取用户信息
        userInfoUrl = "https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid="+sec_uid
        print("request: "+userInfoUrl)
        infoResp = requests.get(userInfoUrl)
        userInfo = {}
        respJson = infoResp.json()
        userInfo["nickname"] = respJson["user_info"]["nickname"]
        userInfo["signature"] = respJson["user_info"]["signature"]
        userInfo["uid"] = respJson["user_info"]["uid"]
        # 获取用户发布的视频
        print(userInfo["uid"])
        signature = self.generateSignature(userInfo["uid"])
        print("signature: "+signature)
        userVideoUrl = "https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=" + \
            sec_uid + "&count=21&max_cursor=0&aid=1128&_signature="+signature

        print("request: "+userVideoUrl)
        userVideoResp = requests.get(userVideoUrl)
        print(json.dumps(userVideoResp.json(), sort_keys=True, indent=4))
        return userInfo

    @staticmethod
    def generateSignature(value):
        p = os.popen('node fuck-byted-acrawler.js %s' % value)
        return (p.readlines()[0]).strip()
    
    def getVideoInfo(self, videoId):
        infoUrl = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids="+videoId
        print("request: "+infoUrl)
        infoResp = requests.get(infoUrl)
        videoInfo = {}
        respJson = infoResp.json()
        itemInfo = respJson["item_list"][0]
        videoInfo["nickname"] = itemInfo["author"]["nickname"]
        videoInfo["desc"] = itemInfo["desc"]
        videoInfo["mp4Url"] = itemInfo["video"]["play_addr"]["url_list"][0]
        videoInfo["mp3Url"] = itemInfo["music"]["play_url"]["url_list"][0]
        return videoInfo

    def getLocation(self, shareUrl):
        response = requests.get(
            shareUrl, headers=self.headers, allow_redirects=False)
        if 'Location' in response.headers.keys():
            return response.headers['Location']
        else:
            print("没有获取到跳转地址")
            return ""

    def downloadVideoAndAudio(self, videoInfo):
        path = os.path.join(self.baseDir, videoInfo["nickname"])
        # 目录不存在，就新建一个
        if not os.path.exists(path):
            os.makedirs(path)

        video = requests.get(url=videoInfo["mp4Url"], headers=self.headers)
        audio = requests.get(url=videoInfo["mp3Url"], headers=self.headers)
        mp4Path = os.path.join(path, videoInfo["desc"]+".mp4")
        mp3Path = os.path.join(path, videoInfo["desc"]+".mp3")
        with open(mp4Path, 'wb') as f, open(mp3Path, 'wb') as f2:
            f.write(video.content)
            f.close()
            f2.write(audio.content)
            f2.close()
            print("===>音频和视频下载完成")


if __name__ == '__main__':
    # 分享链接,视频
    # shareUrl = "https://v.douyin.com/JmenG65/"
    # 用户分享
    shareUrl = "https://v.douyin.com/JmRvpUD/"
    baseDir = "C:\\Users\\Administrator\\Desktop\\douyin"
    douyin = DouYin()
    douyin.shareViedo(shareUrl, baseDir)
