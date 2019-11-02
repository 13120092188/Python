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
    for file in files:
        if file[:-4] not in files:
            unzip_file(file, file[:-4])
    print("^^^^^^^^^^^^^^")

    directorys = traversalDir(folder)
    directorys.sort()
    for dire in directorys:
        if(os.path.exists(dire + "/event.lua")):
            newLua = ""
            filter_folder = []
            with open(dire + "/event.lua","r",encoding="utf-8") as fr:
                oldLua = fr.read()
                if("handleDeviceOrientedChangedEvent" in oldLua and "-- handleDeviceOrientedChangedEvent" not in oldLua):
                    print("+正在处理 " + dire + "...")
                    fr.seek(0, 0)
                    inIsFront = False
                    newline = fr.readline()
                    while True:
                        if("handleDeviceOrientedChangedEvent" in newline and not inIsFront):
                            inIsFront = True
                        if("end," in newline and inIsFront):
                            inIsFront = False
                        if(inIsFront and "true" in newline):
                            filter_folder.append(newline)
                        if(len(filter_folder) == 2):
                            break
                        newline = fr.readline()

                    newLua = addStrToEffect(oldLua,'''
            ------------------------*#*-----------------------
            local effect_manager = this:getEffectManager()
            local cameraPosition = effect_manager:getCameraPosition()
            if cameraPosition == 0 then--前置
                filter_folder = ''' + filter_folder[1][filter_folder[1].find("feature_"):filter_folder[1].find("feature_")+16] + '''
    ''' + filter_folder[0].replace("true","false",1)[:-1] + '''
    ''' + filter_folder[1][:-1] + '''
            else--后置
                filter_folder = ''' + filter_folder[0][filter_folder[0].find("feature_"):filter_folder[0].find("feature_")+16] + '''
    ''' + filter_folder[1].replace("true","false",1)[:-1] + '''
    ''' + filter_folder[0][:-1] + '''
            end
            if(-1 < intensityRecord_filter) then
                local feature = this:getFeature(filter_folder)
                feature:setIntensity(intensityRecord_filter)
            end
            ------------------------#*#-----------------------
                    ''')
                    with open(dire + "/event.lua","w",encoding="utf-8") as fw:
                        fw.write(newLua)
                    fw.close()
                else:
                    pass
            fr.close()

            if(len(filter_folder) == 2):
                newLua = ""
                with open(dire + "/event.lua","r",encoding="utf-8") as fr:
                    inEffect = False
                    inRecord = False
                    inMyCode = True
                    inIsFront = False
                    newline = fr.readline()
                    while newline != "":
                        if("handleEffectEvent" in newline and not inEffect):
                            inEffect = True
                        if("end," in newline and inEffect):
                            inEffect = False

                        if("handleRecodeVedioEvent" in newline and not inRecord):
                            inRecord = True
                        if("end," in newline and inRecord):
                            inRecord = False

                        if("handleDeviceOrientedChangedEvent" in newline and not inIsFront):
                            inIsFront = True
                        if("end," in newline and inIsFront):
                            inIsFront = False

                        if("-*#*-" in newline):
                            inMyCode = False
                        elif("-#*#-" in newline):
                            inMyCode = True
                        if inMyCode and inEffect and (filter_folder[0][filter_folder[0].find("("):filter_folder[0].find(")")] in newline or filter_folder[1][filter_folder[1].find("("):filter_folder[1].find(")")] in newline):
                            newline = "--" + newline
                        if inRecord and (filter_folder[0][filter_folder[0].find("("):filter_folder[0].find("true")] in newline or filter_folder[1][filter_folder[1].find("("):filter_folder[1].find("true")] in newline):
                            newline = "--" + newline

                        if("EventHandles" in newline):
                            newLua += '''
local intensityRecord_filter = -1
'''

                        if inIsFront and "true" in newline and "setFeatureEnabled" in newline:
                            newLua += "            filter_folder = " + newline[newline.find("feature_"):newline.find("feature_")+16] +"\n"

                        if(inIsFront and "return true" in newline):
                            newLua += '''
        local feature = this:getFeature(filter_folder)
        feature:setIntensity(intensityRecord_filter)
'''

                        newLua += newline#########################################

                        if("feature:setIntensity(percentage)" in newline):
                            newLua += '''
            intensityRecord_filter = percentage
'''
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
folderList = [THISPATH + "/ve万圣"]
# folderList = [THISPATH]

for folder in folderList:
    print("###########" + folder + "############")
    os.chdir(folder)
    main_process(folder)

print("----------------End!!!-----------------")