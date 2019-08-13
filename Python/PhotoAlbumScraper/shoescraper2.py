#IMPORTS PHOTOS FROM AN SHOW PHOTO ALBUM AND SAVES THEM TO A DIRECTORY


import sys
import requests
from bs4 import BeautifulSoup
from lxml import etree
import itertools
import re
from urllib.request import urlopen
import os
from pathlib import Path
from selenium import webdriver

home="http://x.yupoo.com"
page=requests.get('http://boost.x.yupoo.com/albums?tab=gallery')
page2="http://boost.x.yupoo.com/albums?tab=gallery"



def CreateDirectory(dirname):
    pathname=dirname
    if not os.path.exists(pathname):
        os.makedirs(pathname)

def CheckDirectory(dirname):
    pathname=dirname
    if os.path.exists(pathname):
        return True
    else:
        return False



def download(url,file_name):
    url = url

    #file_name = url.split('/')[-1]
    u = urlopen("http:"+url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.get_all("Content-Length")[0])
    print ("Downloading: %s Bytes: %s" % (file_name, file_size))

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        print (status),

    f.close()

def CreateTitle(string):
    pattern=re.compile(r'[a-zA-Z0-9-.]+')
    newtitles=re.finditer(pattern,string)

    endstring=" "
    for newtitle in newtitles:
        #print(newtitle.group(0))
        endstring+=" "+newtitle.group(0)
    #print (endstring)
    return endstring

def CustomSoup(page):
    dataurl=requests.get(page)
    data=BeautifulSoup(dataurl.text,'html.parser')
    return data

def CustomDriver(page):
    driver=webdriver.Chrome()
    driver.get(page)
    html=driver.execute_script("return document.documentElement.outerHTML")
    driversoup=BeautifulSoup(html,'html.parser')
    return driversoup


def GetAlbumUrls(home,soup):
    print(soup)
    #sys.exit()
    albums=[]
    album_name_list=soup.find(class_="showindex__parent")
    #print (album_name_list)
    album_name_list_items=album_name_list.find_all('a',href=True)
    number=len(album_name_list_items)
    for i,album_name_list in enumerate(album_name_list_items,1):
        albumurl=home+album_name_list['href'].replace(" ","")
        print("Found Album Urls:", i, "/", number, albumurl)
        albums.append(albumurl)
    return albums

def GetMaxPageUrls(soup):
    maxpages=[]
    pages_links=soup.find(class_="pagination__jumpwrap")
    input_pages=pages_links.find('input',type="number")
    print (input_pages['max'])
    return int(input_pages['max'])

def GetPageLinks(home,soup):
    pages=[]

    page_name_list = soup.find(class_="none_select pagination__buttons")
    page_name_list_items = page_name_list.find_all('a', href=True)
    number = len(page_name_list_items)
    for i, page_name_list in enumerate(page_name_list_items, 1):
        pageurl = home + page_name_list['href'].replace(" ", "")
        #print("Found Page Urls:", i, "/", number, pageurl)
        pages.append(pageurl)

    del pages[-1]
    return pages



def GetAllAlbums(home,soup):
    pages=GetPageLinks(home,soup)
    print(len(pages))
    lists=[]
    for i,page in enumerate(pages,1):
        result=GetAlbumUrls(home,CustomSoup(page))
        lists.extend(result)
    for i, list in enumerate(lists, 1):
        print(i, "These are the album urls", list)
    return lists

def GetAllImages(imageurl):
    #titlereg="[a-zA-z\d]"
    titlereg="[a-zA-Z0-9][a-zA-Z]\S*[a-zA-Z0-9]"
    #titlereg="([a-zA-Z\s\d.-.-])"
    maxtag="&tab=max"
    #imageurl="http://x.yupoo.com/photos/afanda/albums/25046963?uid=1"
    fullurl=imageurl+maxtag
    imagedata=CustomSoup(fullurl)
    #print(imagedata)
    title=imagedata.find(class_="showalbumheader__gallerytitle")

    image_album_list = imagedata.find(class_="showalbum__parent showalbum__max max")
    images_list=imagedata.find_all(class_="autocover image__img image__blur")
    #print (images_list)
    print (title.contents[0])
    dir=CreateTitle(title.contents[0])

    if CheckDirectory(dir)==True:
        print("Directory Exists")
        return
    else:
        CreateDirectory(dir)


    for i,images in enumerate(images_list,1):
        print (i,images['data-src'])
        filename="big{}.jpeg".format(i)
        data_folder =Path(dir+"/"+filename)
        download(images['data-src'],data_folder)






soup=CustomDriver(page2)


albums=GetAllAlbums(home,soup)
#print(albums[0])

for i ,album in enumerate(albums,1):
    print("Downloading Albums")
    #.format(i, album)
    #print(i,album)
    GetAllImages(album)



