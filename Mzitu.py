# coding:utf-8

import os
import requests
import re
from bs4 import BeautifulSoup
import urllib
from time import sleep
import random

id = {'User-Agnet': 'Opera/9.80'}
x = int(input('客官要第几页？\n'))
y = int(input('欲望的尽头是？\n'))
path = 'E:/Mzitu/'
Errorlist = []


# http://www.mzitu.com/136673


def getHtml(url, code='utf-8', id2=id):
    try:
        r = requests.get(url, timeout=30, headers=id2)
        r.encoding = code
        r.raise_for_status()
        return r
    except:
        print('e')
        return 23


def getList(x, y, tplt):
    Page_links = ['http://www.mzitu.com/page/{a}'.format(a=a) for a in range(x, y + 1)]
    img_urls = []
    path2 = path + 'log.txt'
    cnt = 0
    try:
        with open(path2, 'a')as log:
            for link in Page_links:
                cnt = cnt + 1
                log.write('\n第{:4}页\n'.format(cnt))
                r = getHtml(link)
                soup = BeautifulSoup(r.text, 'lxml')
                urls = soup.find('ul', attrs={'id': 'pins'})
                result = re.findall(r'(?<=href=)\S+', str(urls))  # 正则 晕死T T
                result1 = set(result)
                result0 = [eval(i) for i in result1]
                ccc = 0

                for i in result0:
                    ccc = ccc + 1
                    log.write(tplt.format(ccc, i))

                img_urls.extend(result0)
            sleep(1)
        log.close()
        sleep(random.randint(15, 30))
        return img_urls
    except Exception as a:
        print(a)


def Htmlparser(lists, olist):
    try:
        for url in lists:
            r = getHtml(url).text
            soup = BeautifulSoup(r, 'lxml')
            s = soup.find('div', attrs={'class': 'pagenavi'}).find_all('span')[-2].string
            s = int(s)
            mainim = soup.find('div', attrs={'class': 'main-image'})
            getImage(url, s, mainim)
            olist.append(url)
            sleep(random.randint(1, 5))
            print('/r 已完成{:^6.4}%'.format(100 * len(olist) / len(lists)), end='')
    except:  # Exception as b:
        print('')


def makedir(s):
    f = path + s
    isexisted = os.path.exists(f)
    if not isexisted:
        os.mkdir(f)
    return f


def getImage(url, s, mainim):
    try:
        im = mainim.find('img')  # 是名称和地址
        path1 = makedir(im.attrs['alt'])  # 套图文件夹
        pic = im.attrs['src']
        if s >= 100:
            print(url)
            pic_url = pic[0:-7]
            qqq = 3
        else:
            pic_url = pic[0:-6]
            qqq = 2
        img0 = pic_url + '01' + '.jpg'
        img_origin = getHtml(img0, id2=dict(id, **{'Referer': pic}))
        if img_origin == 23:
            Errorlist.append(url)
            getImage2(mainim, s, path1)  # 第二种路线
        else:
            savepic(path1, '01', img_origin)
            for i in range(2, s + 1):
                no = str(i).rjust(qqq, '0')
                img0 = pic_url + no + '.jpg'
                img = getHtml(img0, id2=dict(id, **{'Referer': pic}))
                savepic(path1, no, img)
                sleep(1)
    except Exception as c:
        print(c)


def getImage2(mainim, s, path1):
    for n in range(s):
        no = str(n).rjust(2, '0')
        ia = mainim.find('a').attrs['href']
        pic = mainim.find('img').attrs['src']
        sleep(1.5)
        img = getHtml(pic, id2=dict(id, **{'Referer': pic}))
        savepic(path1, no, img)
        sleep(1)
        r = getHtml(ia).text
        mainim = BeautifulSoup(r, 'lxml').find('div', attrs={'class': 'main-image'})


def savepic(path1, b, img):
    with open(path1 + '/' + b + '.jpg', 'wb') as pbj:
        pbj.write(img.content)
        pbj.close()


def main():
    # pat = re.compile('\/|\.')
    makedir('')
    olist = []
    tplt = '{:^4}\t{}\n'
    img_urls = getList(x, y, tplt)
    Htmlparser(img_urls, olist)
    with open(path + 'ErrorLog.txt', 'a') as comlog:  # 错误文档记录
        cnte = 0
        for i in olist:
            cnte = cnte + 1
            comlog.write(tplt.format(cnte, i))
        comlog.close()
    with open(path + 'Completed log.txt', 'a') as comlog:
        cnt = 0
        for i in olist:
            cnt = cnt + 1
            comlog.write(tplt.format(cnt, i))
        comlog.close()


main()
