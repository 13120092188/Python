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
                inEffect = False
                inComposer = False
                inMakeup = False
                newline = fr.readline()
                while newline != "":
                    if("handleEffectEvent" in newline):
                        inEffect = True
                        newline += "        if (-1 < intensityRecord_makeup) then\n"
                    if('getFeature("FaceMakeup' not in newline and 'handleEffectEvent' not in newline and 'EffectSdk.castFaceMakeupV2Feature' not in newline and 'setIntensity("' not in newline and inEffect):
                        inEffect = False
                        newline = "        end\n" + newline
                    if(inEffect):
                        newline = "    " + newline
                        if "setIntensity" in newline:
                            newline = newline[:newline.find(",")+1] +" intensityRecord_makeup*" + newline[newline.find(",")+1:]

                    if("handleComposerUpdateNodeEvent" in newline):
                        inComposer = True
                    if("end," in newline and inComposer):
                        inComposer = False

                    if('if tag == "Internal_Makeup" then' in newline):
                        inMakeup = True
                    if("end" in newline and inMakeup):
                        inMakeup = False
                        newLua += '''        intensityRecord_makeup = percentage
'''

                    
                    if("EventHandles" in newline):
                        newLua += '''
local intensityRecord_makeup = -1
'''
                    newLua += newline
                    newline = fr.readline()
                with open(dire + "/event.lua","w",encoding="utf-8") as fw:
                    fw.write(newLua)
                fw.close()
            fr.close()
                
print("---------------Start...----------------")
# folderList = [THISPATH + "/1017晚/1017wyx/ios", THISPATH + "/1017晚/1017wyx/安卓"
#             , THISPATH + "/1017晚/1017wxy/ios", THISPATH + "/1017晚/1017wxy/安卓"
#             , THISPATH + "/1017晚/1017hzj/ios", THISPATH + "/1017晚/1017hzj/安卓"
#             , THISPATH + "/1017晚/1017xzx/ios", THISPATH + "/1017晚/1017xzx/安卓"]
# folderList = [THISPATH + "/滤镜/轻颜滤镜_韩国", THISPATH + "/滤镜/轻颜滤镜_韩国/ios", THISPATH + "/滤镜/轻颜滤镜_韩国/安卓", THISPATH + "/滤镜/轻颜滤镜_印尼", THISPATH + "/滤镜/轻颜滤镜_印尼/iOS", THISPATH + "/滤镜/轻颜滤镜_印尼/安卓", THISPATH + "/滤镜/轻颜滤镜_整个海外、越南、泰国", THISPATH + "/滤镜/轻颜滤镜_整个海外、越南、泰国/ios", THISPATH + "/滤镜/轻颜滤镜_整个海外、越南、泰国/安卓", THISPATH + "/滤镜/轻颜滤镜_中国", THISPATH + "/滤镜/轻颜滤镜_中国/ios", THISPATH + "/滤镜/轻颜滤镜_中国/安卓"]
# folderList = [THISPATH + "/1014郝志君/自信android", THISPATH + "/1014郝志君/自信ios"]
# folderList = [THISPATH + "/1017晚/有问题"]
folderList = [THISPATH + "/ve万圣"]
# folderList = [THISPATH]

for folder in folderList:
    print("###########" + folder + "############")
    os.chdir(folder)
    main_process(folder)

print("----------------End!!!-----------------")