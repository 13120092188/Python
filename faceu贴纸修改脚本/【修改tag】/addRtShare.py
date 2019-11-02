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

def unzip_file(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:
        print("解压 " + zip_src + " 中...")
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)       
    else:
        print('This is not zip')


def main_process(folder):
    files = os.listdir(folder)
    for file in files:
        if file[:-4] not in files:
            unzip_file(file, file[:-4])
    print("^^^^^^^^^^^^^^")

    directorys = traversalDir(folder)
    directorys.sort()
    for dire in directorys:
        print("******" + dire + "******")
        if (os.path.exists(dire + "/config.json")):
            configJSON = {}
            with open(dire + "/config.json",'r',encoding="utf-8") as load_f:
                load_dict = json.load(load_f)
                for index, p in enumerate(load_dict["effect"]["Link"]):
                    if("path" in p):
                        load_dict["effect"]["Link"][index]["rtShare"] = True
                configJSON = load_dict
            load_f.close()
            with open(dire + "/config.json",'w',encoding="utf-8") as load_w:
                load_w.write(json.dumps(configJSON, sort_keys=True, indent=4, separators=(',', ': ')))
            load_w.close()


print("---------------Start...----------------")
# folderList = [THISPATH + "/轻颜资源包/ios", THISPATH + "/轻颜资源包/安卓", THISPATH + "/轻颜资源包/其他"]
# folderList = [THISPATH + "/1012/1012杨迅/ios", THISPATH + "/1012/1012杨迅/安卓"]
# folderList = [THISPATH + "/1017晚/1017wyx/ios", THISPATH + "/1017晚/1017wyx/安卓"
#             , THISPATH + "/1017晚/1017wxy/ios", THISPATH + "/1017晚/1017wxy/安卓"
#             , THISPATH + "/1017晚/1017hzj/ios", THISPATH + "/1017晚/1017hzj/安卓"
#             , THISPATH + "/1017晚/1017xzx/ios", THISPATH + "/1017晚/1017xzx/安卓"]
folderList = [THISPATH + "/归档"]
# folderList = [THISPATH + "/1017晚/有问题"]
# folderList = [THISPATH]
for folder in folderList:
    print("###########" + folder + "############")
    os.chdir(folder)
    main_process(folder)

print("----------------End!!!-----------------")