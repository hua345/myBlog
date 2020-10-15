import os
from urllib import request

# 把图片下载到本地

requestHeader = {
    'User-Agent':  r'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
    }


def downloadImgs(dirName, imgUrls):
    baseDir = "C:\\Users\\Administrator\\Desktop\\zhihu"
    path = os.path.join(baseDir, dirName)
    # 目录不存在，就新建一个
    if not os.path.exists(path):
        os.makedirs(path)

    # imgUrls = [
    #     'https://pic1.zhimg.com/80/v2-ee7c2940fec007c867c984dd1223f871_720w.jpg?source=1940ef5c']
    for imgUrl in imgUrls:
        # 这里要取图片地址的最后一个，以便之后获取图片的格式，保存的时候就按照本来的格式保存
        start = imgUrl.rfind('/', 0, len(imgUrl))
        end = imgUrl.find('?', 0, len(imgUrl))
        imgName = imgUrl[start+1:end]
        # 组装图片的绝对路径，用isbn来命名
        img_path = os.path.join(path, imgName)
        req = request.Request(imgUrl, headers=requestHeader)
        data = request.urlopen(req, timeout=300).read()
        f = open(img_path, 'wb')
        f.write(data)
        f.close()
