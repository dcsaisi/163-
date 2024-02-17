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
    cookies = {
        'NMTID': '00OzC-QGyUMtkQA5EX7oHzZaRnrKq4AAAGM5uvgiQ',
        '_iuqxldmzr_': '32',
        '_ntes_nnid': '369262d59dc23cc3d2ac60d86f86bc3a,1704681267356',
        '_ntes_nuid': '369262d59dc23cc3d2ac60d86f86bc3a',
        'WEVNSM': '1.0.0',
        'WNMCID': 'fyjosg.1704681267999.01.0',
        'sDeviceId': 'YD-x%2F5zbAkXmyNFUxBUAFeBoYL4i0YCSHms',
        'WM_TID': 'PiijRwoFrzhBRVQQBVaR4K157I%2Buf5w2',
        '__snaker__id': '88w5UjTNtmMKMepm',
        'ntes_kaola_ad': '1',
        'ntes_utid': 'tid._.g%252FNUtPfWQYtFUgFEAUaEtbls%252FNv%252Fb5Gr._.0',
        '__csrf': '3bba9088ae235bdaa70d04c1835cc123',
        'WM_NI': 'e2LesuPfw%2F1Ynw9tUDzO%2FLCvrFmUZk5lmwSiCAPGpeBiphFkgKftH3o0X6Of2VrYyufzvd4h0OwLbQqdRS8MNWTGQlSRnE7yVQgCfYjtB3ckYQLIenb1zK0qoT5awp6eZHI%3D',
        'WM_NIKE': '9ca17ae2e6ffcda170e2e6eebab853ab93fcd4d774a8b08fa2d44a968b8e83d440b1b7bf8fbb7088999cd6cb2af0fea7c3b92aa7ee8486f27f94bab9d0b453aea9f795d850ba91e1adc27eb29aa3b6d961f7b4a398d263819fa0a8f36f82b7c089c561a595aa95cb39adf098d7ce6ef28abebafc7fa6a6ba85b764f491b9ade15bb3bc9eb4bb478e899ca8d468918ea2a6b673968fa9a4e553aaac8ed4e2619b8f84aae866a2efb6acb37bad8cfb82f67cf6bb96a9cc37e2a3',
        'gdxidpyhxdE': 'lgMVt8kEWqAOncU1QMibYo1sp9L93%2BbCC611x1LpG429Nu4fEjIg%2B9i3d29eSMhGbXyYPgI%2FTixzOeijeVg5Sw%2BIW%2FQIbs8ZfwNk%2BWkeQgJI9vR6gr%5C7tKI%2FBh7%5CbOvjuMEQsZ7Ry7Hyj8eUg0cL%2B%5CyWhQkYiqA%2BmMHM503UACQbSWrc%3A1708051223367',
        'JSESSIONID-WYYY': 'f7c4HuEiq9%2BrnawblMQPua1T5mAgZo8m%5CD47WGp2TNXTu%2Bz0bAAhMH%2BnrEVB0y%2Bt4YK1Jk4S14S0inbiMRqMWx7swN36eCzVVdx8Gdy1f5EFY1sfd%2FVb76H7UtwzOwNDig7%5Cjx5zT81Z4CYhC%2Bv4rNxOuA2%5CVkAvQ%2B620Nd7oUcGueXa%3A1708061167886',
    }

    headers = {
        'authority': 'music.163.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        # 'cookie': 'NMTID=00OzC-QGyUMtkQA5EX7oHzZaRnrKq4AAAGM5uvgiQ; _iuqxldmzr_=32; _ntes_nnid=369262d59dc23cc3d2ac60d86f86bc3a,1704681267356; _ntes_nuid=369262d59dc23cc3d2ac60d86f86bc3a; WEVNSM=1.0.0; WNMCID=fyjosg.1704681267999.01.0; sDeviceId=YD-x%2F5zbAkXmyNFUxBUAFeBoYL4i0YCSHms; WM_TID=PiijRwoFrzhBRVQQBVaR4K157I%2Buf5w2; __snaker__id=88w5UjTNtmMKMepm; ntes_kaola_ad=1; ntes_utid=tid._.g%252FNUtPfWQYtFUgFEAUaEtbls%252FNv%252Fb5Gr._.0; __csrf=3bba9088ae235bdaa70d04c1835cc123; WM_NI=e2LesuPfw%2F1Ynw9tUDzO%2FLCvrFmUZk5lmwSiCAPGpeBiphFkgKftH3o0X6Of2VrYyufzvd4h0OwLbQqdRS8MNWTGQlSRnE7yVQgCfYjtB3ckYQLIenb1zK0qoT5awp6eZHI%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eebab853ab93fcd4d774a8b08fa2d44a968b8e83d440b1b7bf8fbb7088999cd6cb2af0fea7c3b92aa7ee8486f27f94bab9d0b453aea9f795d850ba91e1adc27eb29aa3b6d961f7b4a398d263819fa0a8f36f82b7c089c561a595aa95cb39adf098d7ce6ef28abebafc7fa6a6ba85b764f491b9ade15bb3bc9eb4bb478e899ca8d468918ea2a6b673968fa9a4e553aaac8ed4e2619b8f84aae866a2efb6acb37bad8cfb82f67cf6bb96a9cc37e2a3; gdxidpyhxdE=lgMVt8kEWqAOncU1QMibYo1sp9L93%2BbCC611x1LpG429Nu4fEjIg%2B9i3d29eSMhGbXyYPgI%2FTixzOeijeVg5Sw%2BIW%2FQIbs8ZfwNk%2BWkeQgJI9vR6gr%5C7tKI%2FBh7%5CbOvjuMEQsZ7Ry7Hyj8eUg0cL%2B%5CyWhQkYiqA%2BmMHM503UACQbSWrc%3A1708051223367; JSESSIONID-WYYY=f7c4HuEiq9%2BrnawblMQPua1T5mAgZo8m%5CD47WGp2TNXTu%2Bz0bAAhMH%2BnrEVB0y%2Bt4YK1Jk4S14S0inbiMRqMWx7swN36eCzVVdx8Gdy1f5EFY1sfd%2FVb76H7UtwzOwNDig7%5Cjx5zT81Z4CYhC%2Bv4rNxOuA2%5CVkAvQ%2B620Nd7oUcGueXa%3A1708061167886',
        'referer': 'https://music.163.com/',
        'sec-ch-ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'iframe',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    }

    params = {
        'id': '36893290',
    }

    response = requests.get('https://music.163.com/album', params=params, cookies=cookies, headers=headers).text

    return response


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

    https://music.163.com/#/search/m/?%23%2Fdiscover%2Fplaylist=&s=%E8%8B%97%E6%97%8F&type=1000
    playlist[?]id=(\d+).*?title="(.*?)">
    """

    url = 'https://music.163.com/#/search/m/?%23%2Fdiscover%2Fplaylist=&s=%E8%8B%97%E6%97%8F&type=1000'
    html = get_windows_request(url)
    listid = re.findall(r'/playlist?id=(\d+)"\s+title="([^"]+)">', html)
    print(listid)
    return listid


def playListUrl():
    """
      从 https://music.163.com/discover/playlist 网址获取歌单url
      :return: [歌单url,歌单名]
    """

    listurl = []
    url = 'https://music.163.com/#/search/m/?%23%2Fdiscover%2Fplaylist=&s=%E8%8B%97%E6%97%8F&type=1000'
    html = get_windows_request(url)
    list = re.findall('<a\s+href="\/playlist\?id=(\d+)"\s+title="([^"]+)">', html)
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

    url = 'https://music.163.com/#/album?id=%s'
    # print(url % playListID)
    html = get_windows_request(url % playListID)
    print(html)
    song = re.findall(r'/song[?]id=(\d+)">(.*?)</a>', html)
    print(song)
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
    # p = playListID()
    s = [36893290, 75338376, 86036757, 162221962]
    list = []
    url = ""
    a = []  # 数组格式[[[歌名,评论者名,评论内容,评论时间,点赞数量],...],...]
    # for l in range(len(p)):
    #     list.append(songList(p[l][0]))
    # for o in list:
    #     print("共%s个歌单" % range(len(list)))
    #     for i in o:
    #         print("第%s首歌的评论获取成功" % range(len(i)))
    #         a.append(review(i[0]))
    # for x in a:
    #     for y in x:
    #         print(y[0],y[1],y[2],y[3],y[4])
    #         get_windows_request(url % (y[0],y[1],y[2],y[3],y[4]))

    # print(a)
    for l in range(len(s)):
        list.append(songList(s[l]))
    print(list)
    for o in list:
        print("共%s个歌单" % range(len(list)))
        for i in o:
            print("第%s首歌的评论获取成功" % range(len(i)))
            print(review(i[0]))
            a.append(review(i[0]))

    # 在循环之外打开文件
    with open('../comment.txt', 'a+', encoding='utf-8') as file:
        for x in a:
            for y in x:
                # 写入内容到文件
                print(y[0], y[1], y[2], y[3], y[4])
                file.write(y[2] + '\n')

