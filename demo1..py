# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 11:24:17 2024

@author: Administrator
"""
import time
import requests
import re

proxies = {'https': '192.168.3.83:7890'}
TIMESLEEP = 0.002


def get_windows_request(url):
    hd = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'ssxmod_itna2=QqjhYKBIxmx0OCDzxAOfD0iCUqh1B=rpDnFoitQWDlgDWq03rq2f6qqWuX525tY04cNOt763KqKVe9BH+IjAilDKAjlQqkh7D8Ov5mHZ3TrFsppbnkcejYlaxF5sTzI=qu468X9gBl+hBtd3xLSA8lSGVzxEX4wXX+SQIeeLn/MYRlgD5ueddVuEX/M6D==dR4M6i3PTPydL7pRiFhMcu9xQEBCIFYwEuYkWFUnLVi27dPUPzrKdAHQ8sUbjd6/6EvFhbD7jqWxqawoxd+hmS4vh21cCsbsKWD7=DeqqxD==; ssxmod_itna=WqGxB7iQEx9DzxAoZbGkY=WeQT4mu5haaPDsoqNDSxGKidDqxBnukmx2qGQeMPKj7fDv3qBn0mwYAtIeq5TXbYpRU5DU4i8DCwuaqNDenQD5xGoDPxDeDADYoUDAqiOD7qDdLwHyzkDbxi3LxDbDin8pxGCDeKD0c+FDQKDu6FqCiGkeDDzeloxqlr4DYnGKfp+noECC7B4LxG1W40HqiLItFM6eAvhUUiGIWKDXrQDvO51M2pmDB+kl1HGl0ntrlGtMe9DABhxsexxYh1eM72DMGn5qi455ZhqYcToSixx4D===; tfstk=eViM3xMKeVz_DdsSpfE6vfKaVqLKC1Zb8jIYMoF28WPC61It3S2mFW0tXxRsimVE_5U9ClWsRbHPXcL_Diq_coRJw3KRCAZb0036MWksgbdxYQKJ2Ak_coRJwd1rbljhHdI7TtmkIzVlE06_F7tY-7kaTAHtYRf8aAPh0iP3IPYnQWjV0Djzbw7PAYSbLKnFlZaadJV-OEf6P8xq8GvHKaJb7Jw_wmphuZ550iQMKpby-PyQC75..; acw_tc=2760777a17068884375607807e89650a4bdc260b9a5c4e0c2a8f5cf295e05d',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    }

    time.sleep(TIMESLEEP)
    rst = requests.get(url, headers=hd)
    rst.encoding = "utf-8"

    return rst.text


def get_phone_request(url):
    hd = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.36"}
    time.sleep(TIMESLEEP)
    rst = requests.get(url, headers=hd)
    rst.encoding = "utf-8"
    # f = open('./hhh.html', 'w')
    # f.write(rst.text)
    # f.close()

    return rst.text


def playListID():
    """
    从 https://music.163.com/discover/playlist 网址获取歌单id
    :return: [歌单id,歌单名]
    """

    url = 'https://music.163.com/discover/playlist'
    html = get_windows_request(url)
    print(html)
    listid = re.findall(r'playlist[?]id=(\d+).*?tit.*?>(.*?)</a', html)

    print("歌单id获取成功")
    return listid


def playListUrl():
    """
      从 https://music.163.com/discover/playlist 网址获取歌单url
      :return: [歌单url,歌单名]
    """

    listurl = []
    url = 'https://music.163.com/discover/playlist'
    html = get_windows_request(url)
    list = re.findall(r'playlist[?]id=(\d+).*?tit.*?>(.*?)</a', html)
    # print(list)
    for i in range(len(list)):
        lp = 'https://music.163.com/#/playlist?id=' + list[i][0]
        listurl.append([lp, list[i][1]])
    return listurl


def songList(playListID):
    """
    :param playListID: 歌单id
    :return: [歌曲id,歌曲名称]
    """

    url = 'https://music.163.com/playlist?id=%s'
    # print(url % playListID)
    html = get_windows_request(url % playListID)
    song = re.findall(r'/song[?]id=(\d+).*?>(.*?)</a', html)
    print("歌曲获取成功")
    return song


def review(songID):
    """
    :param songID : 歌曲id
    :return: data:歌名，评论者名，评论内容，评论时间，点赞数量
    """
    url = "https://y.music.163.com/m/song?id=%s"
    data = []
    html = get_phone_request(url % songID)
    songname = re.findall(r':[{]"name":"(.*?)"', html)
    pin = re.findall(r'"nickname":"(.*?)".*?"content":"(.*?)".*?time":(\d+).*?likedCount":(\d+)', html)
    for i in pin:
        e = re.sub(r'\\n', "", i[1])
        p = re.sub(r'\\r', "", e)
        data.append([songname[0], i[0], p, i[2], i[3]])
    return data


if __name__ == '__main__':
    p = playListID()
    list = []
    url = ""
    a = []  # 数组格式[[[歌名,评论者名,评论内容,评论时间,点赞数量],...],...]
    for l in range(len(p)):
        list.append(songList(p[l][0]))
    for o in list:
        print("共%s个歌单" % range(len(list)))
        for i in o:
            print("第%s首歌的评论获取成功" % range(len(i)))
            a.append(review(i[0]))
    for x in a:
        for y in x:
            print(y[0], y[1], y[2], y[3], y[4])
            get_windows_request(url % (y[0], y[1], y[2], y[3], y[4]))

    print(a)



