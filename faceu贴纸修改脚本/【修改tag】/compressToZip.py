#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import json
import zipfile
import shutil
THISPATH = sys.path[0]
os.chdir(THISPATH)

def traversalDir(path):
    list = []
    if (os.path.exists(path)):
        files = os.listdir(path)
        for file in files:
            m = os.path.join(path,file)
            if (os.path.isdir(m)):
                h = os.path.split(m)
                # print (h[1])
                list.append(h[1])
        if (list.count(".vscode") > 0):
            list.remove(".vscode")
        return list

def zip_file(src_dir):
    print("正在压缩 " + src_dir + " ...")
    zip_name = src_dir +'.zip'
    z = zipfile.ZipFile(zip_name,'w',zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(src_dir):
        dirnames = dirnames
        fpath = dirpath.replace(src_dir,'')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename),fpath+filename)
    print ('==压缩成功==')
    z.close()




# folderList = [THISPATH + "/滤镜/轻颜滤镜_韩国", THISPATH + "/滤镜/轻颜滤镜_韩国/ios"
#             , THISPATH + "/滤镜/轻颜滤镜_韩国/安卓", THISPATH + "/滤镜/轻颜滤镜_印尼"
#             , THISPATH + "/滤镜/轻颜滤镜_印尼/iOS", THISPATH + "/滤镜/轻颜滤镜_印尼/安卓"
#             , THISPATH + "/滤镜/轻颜滤镜_整个海外、越南、泰国", THISPATH + "/滤镜/轻颜滤镜_整个海外、越南、泰国/ios"
#             , THISPATH + "/滤镜/轻颜滤镜_整个海外、越南、泰国/安卓", THISPATH + "/滤镜/轻颜滤镜_中国"
#             , THISPATH + "/滤镜/轻颜滤镜_中国/ios", THISPATH + "/滤镜/轻颜滤镜_中国/安卓"]
# folderList = [THISPATH + "/1017晚/1017wyx/ios", THISPATH + "/1017晚/1017wyx/安卓"
#             , THISPATH + "/1017晚/1017wxy/ios", THISPATH + "/1017晚/1017wxy/安卓"
#             , THISPATH + "/1017晚/1017hzj/ios", THISPATH + "/1017晚/1017hzj/安卓"
#             , THISPATH + "/1017晚/1017xzx/ios", THISPATH + "/1017晚/1017xzx/安卓"]
# folderList = [THISPATH + "/滤镜/轻颜滤镜_韩国", THISPATH + "/滤镜/轻颜滤镜_韩国/ios", THISPATH + "/滤镜/轻颜滤镜_韩国/安卓", THISPATH + "/滤镜/轻颜滤镜_印尼", THISPATH + "/滤镜/轻颜滤镜_印尼/iOS", THISPATH + "/滤镜/轻颜滤镜_印尼/安卓", THISPATH + "/滤镜/轻颜滤镜_整个海外、越南、泰国", THISPATH + "/滤镜/轻颜滤镜_整个海外、越南、泰国/ios", THISPATH + "/滤镜/轻颜滤镜_整个海外、越南、泰国/安卓", THISPATH + "/滤镜/轻颜滤镜_中国", THISPATH + "/滤镜/轻颜滤镜_中国/ios", THISPATH + "/滤镜/轻颜滤镜_中国/安卓"]
# folderList = [THISPATH + "/安卓", THISPATH + "/iOS", THISPATH + "/yangxun"]
# folderList = [THISPATH + "/轻颜资源包/ios", THISPATH + "/轻颜资源包/安卓", THISPATH + "/轻颜资源包/其他"]
# folderList = [THISPATH]
folderList = [THISPATH + "/万圣节"]

for folder in folderList:
    print("###########" + folder + "############")
    os.chdir(folder)
    directorys = traversalDir(folder)
    for dire in directorys:
        if (os.path.exists(dire + "/__MACOSX")):
            shutil.rmtree(dire + "/__MACOSX")
        if (os.path.exists(dire + "/归档.zip")):
            os.remove(dire + "/归档.zip")  
            print(dire + " 所含归档已删除！")
        if not os.path.exists(dire + ".zip"):
            zip_file(dire)
            if os.path.exists(dire + "/config.json"):
                shutil.rmtree(dire)
        else:
            os.remove(dire + ".zip")
            zip_file(dire)
            if os.path.exists(dire + "/config.json"):
                shutil.rmtree(dire)
