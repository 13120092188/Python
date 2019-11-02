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
        print("解压 " + zip_src + " 中...")
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)       
    else:
        print(zip_src + ' is not zip')

def zip_file(src_dir):
    zip_name = src_dir +'.zip'
    z = zipfile.ZipFile(zip_name,'w',zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(src_dir):
        dirnames = dirnames # unused
        fpath = dirpath.replace(src_dir,'')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename),fpath+filename)
    print ('==压缩成功==' + src_dir)
    z.close()


def addStrToEffect(luaString,s):
    index = luaString.find("handleEffectEvent")
    index1 = luaString[index:index+100].find("eventCode")
    newLuaString = luaString[:index+index1+10] + s + luaString[index+index1+10:]
    return newLuaString


def main_process(folder):
    files = os.listdir(folder)
    for file in files:
        if file[:-4] not in files:
            unzip_file(file, file[:-4])
    print("^^^^^^^^^^^^^^")

    directorys = traversalDir(folder)

    needEditByHandlist = []
    differentfilter = []
    maybePI = []
    for dire in directorys:
        filterPath = ""
        filterCounter = 0
        if (os.path.exists(dire + "/config.json")):
            with open(dire + "/config.json",'r') as load_f:
                load_dict = json.load(load_f)
                for p in load_dict["effect"]["Link"]:
                    if(p["path"][0:6] == "Filter"):
                        # print(p["path"][0:-1])
                        filterPath = p["path"][0:-1]
                        filterCounter += 1
            load_f.close()
        else:
            filterCounter = -1
        if(filterCounter == 1):
            print("+正在处理 " + dire + "...")
            # print(filterPath)
            with open(dire + "/event.lua","r",encoding="utf-8") as fr:
                oldLua = fr.read()
                if("handleComposerUpdateNodeEvent" not in oldLua):
                    index = -1
                    while(oldLua[index:][0] != "}"):
                        index -= 1
                    newLua = oldLua[0:index] + '''handleComposerUpdateNodeEvent = function (this, path, tag, percentage)
        local feature = this:getFeature("''' + filterPath + '''")
        -- local _feature = EffectSdk.castFaceMakeupV2Feature(feature)
        if (not feature)  then
            print("Filter is not exist")
            return false
        end
        if tag == "Internal_Filter" then
            feature:setIntensity(percentage)
        end
    end,
}'''
                    with open(dire + "/event.lua","w",encoding="utf-8") as fw:
                        fw.write(newLua)
                    fw.close()
                else:
                    print(" -该滤镜已包含‘handleComposerUpdateNodeEvent’")
            fr.close()

        elif(filterCounter == 2):
            needEditByHandlist.append(dire)
            print("+正在处理 " + dire + "...")
            # print(filterPath)
            with open(dire + "/event.lua","r",encoding="utf-8") as fr:
                oldLua = fr.read()
                if("handleComposerUpdateNodeEvent" not in oldLua):
                    index = -1
                    while(oldLua[index:][0] != "}"):
                        index -= 1
                    indexEventHandles = oldLua.find("EventHandles")
                    newLua = oldLua[0:indexEventHandles-1] + '''
                    
local filter_folder = "xxxxxx"
filter_folder = feature_0.folder
''' + oldLua[indexEventHandles-1:index] + '''
    handleComposerUpdateNodeEvent = function (this, path, tag, percentage)
        local feature = this:getFeature(filter_folder)
        -- local _feature = EffectSdk.castFaceMakeupV2Feature(feature)
        if (not feature)  then
            print("Filter is not exist")
            return false
        end
        if tag == "Internal_Filter" then
            feature:setIntensity(percentage)
        end
    end,
}'''
                    with open(dire + "/event.lua","w",encoding="utf-8") as fw:
                        fw.write(newLua)
                    fw.close()
                else:
                    print(" -该滤镜已包含‘handleComposerUpdateNodeEvent’")
            fr.close()
        elif(filterCounter == -1):
            maybePI.append(dire)
        else:
            differentfilter.append(dire)

        if (os.path.exists(dire + "/__MACOSX")):
            shutil.rmtree(dire + "/__MACOSX")  
        zip_file(dire)

    print("* * * * * *") 
    print("需要手动修改的贴纸为：")
    print(needEditByHandlist)
    print("需要检查的贴纸为")
    print(differentfilter)
    print("可能是PI包的贴纸为")
    print(maybePI)



print("---------------Start...----------------")
folderList = [THISPATH + "/effect韩国", THISPATH + "/effect韩国/ios", THISPATH + "/effect韩国/安卓", THISPATH + "/effect印尼滤镜", THISPATH + "/effect印尼滤镜/iOS", THISPATH + "/effect印尼滤镜/安卓"]
for folder in folderList:
    print("###########" + folder + "############")
    os.chdir(folder)
    main_process(folder)


print("----------------End!!!-----------------")