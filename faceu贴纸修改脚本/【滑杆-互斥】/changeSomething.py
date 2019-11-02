#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import json
import zipfile
import shutil
THISPATH = sys.path[0]
print(THISPATH)
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
        # print("解压 " + zip_src + " 中...")
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)       
    else:
        # print('This is not zip')
        pass



def addStrToEffect(luaString,s):
    index = luaString.find("handleEffectEvent")
    index1 = index + luaString[index: ].find("end,")
    index2 = index + luaString[index:index1].find("eventCode == 1") + 14
    index3 = index2 + luaString[index2:index2 + 20].find("then") + 4
    newLuaString = luaString[:index3] + s + luaString[index3:]
    return newLuaString

def main_process(folder):
    files = os.listdir(folder)
    for f in files:
        if f[:-4] not in files:
            unzip_file(f, f[:-4])
    print("^^^^^^^^^^^^^^")

    directorys = traversalDir(folder)
    directorys.sort()
    for dire in directorys:
        if(os.path.exists(dire + "/event.lua")):
            newLua = ""
            with open(dire + "/event.lua","r",encoding="utf-8") as fr:
                oldLua = fr.read()
                fr.seek(0, 0)
                newline = fr.readline()
                while newline != "":
                    if("handleComposerUpdateNodeEvent" in newline and "handleDeviceOrientedChangedEvent" not in oldLua):
                        newLua += newline
                        newline = fr.readline()
                        newline = fr.readline()
                    newLua += newline
                    newline = fr.readline()
                with open(dire + "/event.lua","w",encoding="utf-8") as fw:
                    fw.write(newLua)
                fw.close()
            fr.close()
                
print("---------------Start...----------------")
# folderList = [THISPATH + "/1017/1017wyx/ios", THISPATH + "/1017/1017wyx/安卓"
#             , THISPATH + "/1017/1017wxy/ios", THISPATH + "/1017/1017wxy/安卓"
#             , THISPATH + "/1017/1017hzj/ios", THISPATH + "/1017/1017hzj/安卓"
#             , THISPATH + "/1017/1017xzx/ios", THISPATH + "/1017/1017xzx/安卓"]
folderList = [THISPATH + "/滤镜/轻颜滤镜_韩国", THISPATH + "/滤镜/轻颜滤镜_韩国/ios", THISPATH + "/滤镜/轻颜滤镜_韩国/安卓", THISPATH + "/滤镜/轻颜滤镜_印尼", THISPATH + "/滤镜/轻颜滤镜_印尼/iOS", THISPATH + "/滤镜/轻颜滤镜_印尼/安卓", THISPATH + "/滤镜/轻颜滤镜_整个海外、越南、泰国", THISPATH + "/滤镜/轻颜滤镜_整个海外、越南、泰国/ios", THISPATH + "/滤镜/轻颜滤镜_整个海外、越南、泰国/安卓", THISPATH + "/滤镜/轻颜滤镜_中国", THISPATH + "/滤镜/轻颜滤镜_中国/ios", THISPATH + "/滤镜/轻颜滤镜_中国/安卓"]
# folderList = [THISPATH + "/1014郝志君/自信android", THISPATH + "/1014郝志君/自信ios"]
# folderList = [THISPATH + "/测试"]
# folderList = [THISPATH]

for folder in folderList:
    print("###########" + folder + "############")
    os.chdir(folder)
    main_process(folder)

print("----------------End!!!-----------------")