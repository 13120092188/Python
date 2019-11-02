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




folderList = [THISPATH + "/轻颜滤镜_大海外", THISPATH + "/轻颜滤镜_cn", THISPATH + "/effect韩国/安卓", THISPATH + "/effect韩国/ios", THISPATH + "/effect印尼滤镜/安卓", THISPATH + "/effect印尼滤镜/iOS"]
for folder in folderList:
    print("###########" + folder + "############")
    os.chdir(folder)
    directorys = traversalDir(folder)
    for dire in directorys:
        if (os.path.exists(dire + "/__MACOSX")):
            shutil.rmtree(dire + "/__MACOSX")  
        zip_file(dire)
