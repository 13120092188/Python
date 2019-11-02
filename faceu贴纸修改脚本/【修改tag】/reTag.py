#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import json
import zipfile
import shutil
import random
import time
import hashlib
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
    # files = os.listdir(folder)
    # for file in files:
    #     if file[:-4] not in files:
    #         unzip_file(file, file[:-4])
    # print("^^^^^^^^^^^^^^")

    tags = []
    directorys = traversalDir(folder)
    directorys.sort()
    for dire in directorys:
        print("******" + dire + "******")
        detailFolders = traversalDir(folder + "/" + dire)
        for detailFolder in detailFolders:
            if os.path.exists(dire + "/" + detailFolder + "/content.json") and "ES3DV3" not in detailFolder:
                with open(dire + "/" + detailFolder + "/content.json",'r',encoding="utf-8") as load_f:
                    load_dict = json.load(load_f)
                    nowTime = time.time()
                    myTime = str(nowTime).encode("utf-8")
                    myTimeMD5 = hashlib.md5(myTime).hexdigest()
                    t = time.strftime("%Y_%m_%d_%H_%M_%S_", time.localtime(int(nowTime)))
                    load_dict["tag"] = t + myTimeMD5
                    print(t + myTimeMD5)
                    tags.append(t + myTimeMD5)
                    configJSON = load_dict
                load_f.close()
        
                with open(dire + "/" + detailFolder + "/content.json",'w',encoding="utf-8") as load_w:
                    load_w.write(json.dumps(configJSON, sort_keys=True, indent=4, separators=(',', ': ')))
                load_w.close()
            elif os.path.exists(dire + "/" + detailFolder + "/config.json") and "Filter" in detailFolder:
                with open(dire + "/" + detailFolder + "/config.json",'r',encoding="utf-8") as load_f:
                    load_dict = json.load(load_f)
                    nowTime = time.time()
                    myTime = str(nowTime).encode("utf-8")
                    myTimeMD5 = hashlib.md5(myTime).hexdigest()
                    t = time.strftime("%Y_%m_%d_%H_%M_%S_", time.localtime(int(nowTime)))
                    if "tag" in load_dict:
                        load_dict["tag"] = t + myTimeMD5
                        print(t + myTimeMD5)
                        tags.append(t + myTimeMD5)
                    configJSON = load_dict
                load_f.close()
        
                with open(dire + "/" + detailFolder + "/config.json",'w',encoding="utf-8") as load_w:
                    load_w.write(json.dumps(configJSON, sort_keys=True, indent=4, separators=(',', ': ')))
                load_w.close()

print("---------------Start...----------------")
# folderList = [THISPATH + "/轻颜资源包/ios", THISPATH + "/轻颜资源包/安卓", THISPATH + "/轻颜资源包/其他"]
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