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
        print('This is not zip')

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

def listToString(_list):
    s = ""
    for l in _list:
        s += str(l) +"\n        "
    return s


def addStrToEffect(luaString,s):
    index = luaString.find("handleEffectEvent")
    index1 = luaString[index:index+100].find("eventCode")
    newLuaString = luaString[:index+index1+10] + s + luaString[index+index1+10:]
    return newLuaString

def main_process(folder):
    # files = os.listdir(folder)
    # for file in files:
    #     if file[:-4] not in files:
    #         unzip_file(file, file[:-4])
    # print("^^^^^^^^^^^^^^")

    directorys = traversalDir(folder)
    directorys.sort()
    for dire in directorys:
        makeupTypeList_intensity = [[],[],[]]
        makeupTypeList_intensity1 = [[],[],[]]
        makeupTypeList_opacity = [[],[],[]]
        filterPath = []
        filterCounter = 0
        if (os.path.exists(dire + "/config.json")):
            configJSON = {}
            with open(dire + "/config.json",'r',encoding="utf-8") as load_f:
                load_dict = json.load(load_f)
                for index, p in enumerate(load_dict["effect"]["Link"]):
                    if("type" in p):
                        if("Filter" == p["type"]):
                            # print(p["path"][0:-1])
                            filterPath.append(p["path"][0:-1])
                            filterCounter += 1
                        elif("FaceMakeupV2" == p["type"]):
                            load_dict["effect"]["Link"][index]["exclusiveScene"] = [{"sceneKey": "FaceMakeup/Pupil","tagName": [],"priority": 1000},
                                                                                    {"sceneKey": "FaceMakeup/Lips", "tagName": [],"priority": 1000},
                                                                                    {"sceneKey": "FaceMakeup/Blusher","tagName": [],"priority": 1000},
                                                                                    {"sceneKey": "FaceMakeup/EyeShadow","tagName": [],"priority": 1000},
                                                                                    {"sceneKey": "FaceMakeup/EyeLine","tagName": [],"priority": 1000},
                                                                                    {"sceneKey": "FaceMakeup/Normal","tagName": [],"priority": 1000},
                                                                                    {"sceneKey": "FaceMakeup/Facial","tagName": [],"priority": 1000},
                                                                                    {"sceneKey": "FaceMakeup/Teeth","tagName": [],"priority": 1000},
                                                                                    {"sceneKey": "FaceMakeup/NasolabialFolds","tagName": [],"priority": 1000},
                                                                                    {"sceneKey": "FaceMakeup/Brow","tagName": [],"priority": 1000}]
                # print(load_dict)
                configJSON = load_dict
            load_f.close()
            with open(dire + "/config.json",'w',encoding="utf-8") as load_w:
                load_w.write(json.dumps(configJSON, sort_keys=True, indent=4, separators=(',', ': ')))
            load_w.close()
        else:
            filterCounter = -1
        
        makeupPath = []
        subDirectorys = traversalDir(dire)
        for subDire in subDirectorys:
            if("FaceMakeupV" in subDire):
                makeupPath.append(subDire)
        for index, p in enumerate(makeupPath):
            if (os.path.exists(dire + "/" + p + "/makeup.json")):
                with open(dire + "/" + p + "/makeup.json",'r',encoding="utf-8") as load_f:
                    load_dict = json.load(load_f)
                    for makeup in load_dict["filters"]:
                        if ("intensity" in makeup) and (makeup["intensity"] != 1.0):
                            makeupTypeList_intensity1[index].append('_feature:setIntensity("' + makeup["filterType"] + "+" + str(makeup["zPosition"]) + '",' + str(makeup["intensity"]) + ')')
                            makeupTypeList_intensity[index].append('_feature:setIntensity("' + makeup["filterType"] + "+" + str(makeup["zPosition"]) + '",percentage*' + str(makeup["intensity"]) + ')')
                        else:
                            makeupTypeList_intensity[index].append('_feature:setIntensity("' + makeup["filterType"] + "+" + str(makeup["zPosition"]) + '",percentage)')
                        makeupTypeList_opacity[index].append('_feature:setOpacity("' + makeup["filterType"] + "+" + str(makeup["zPosition"]) + '",vals)')
                load_f.close()



        print("*****************************" + dire + "*********************************************")
        if(os.path.exists(dire + "/event.lua")):
            print("+正在处理 " + dire + "...")
            # print(filterPath)
            if(filterCounter == 1 and len(makeupPath) == 1):
                with open(dire + "/event.lua","r",encoding="utf-8") as fr:
                    oldLua = fr.read()
                    if("handleComposerUpdateNodeEvent" not in oldLua):
                        index = -1
                        while(oldLua[index:][0] != "}"):
                            index -= 1
                        indexEventHandles = oldLua.find("EventHandles")
                        newLua = oldLua[0:indexEventHandles-1] + '''
local maleOpacity   = 0.0
local femaleOpacity = 1.0''' + oldLua[indexEventHandles-1:index] + '''
    handleComposerUpdateNodeEvent = function (this, path, tag, percentage)
        local feature = this:getFeature("''' + filterPath[0] + '''")
        -- local _feature = EffectSdk.castFaceMakeupV2Feature(feature)
        if (not feature)  then
            print("Filter is not exist")
            return false
        end
        if tag == "Internal_Filter" then
            feature:setIntensity(percentage)
        end

        
        local feature = this:getFeature("''' + makeupPath[0] + '''")
        local _feature = EffectSdk.castFaceMakeupV2Feature(feature)
        if (not feature) or (not _feature) then
            print("FaceMakeupV2_byTool is not exist")
            return false
        end
        if tag == "Internal_Makeup" then
        ''' + listToString(makeupTypeList_intensity[0]) + '''
        end
    end,
    handleGenderEvent = function(this, genderInfo)
        local feature = this:getFeature("''' + makeupPath[0] + '''")
        local _feature = EffectSdk.castFaceMakeupV2Feature(feature)
        if (not feature) or (not _feature) then
            print("FaceMakeupV2_byTool is not exist")
            return false
        end
        local effect_manager      = this:getEffectManager()
        local isMaleMakeupOpen    = effect_manager:getMaleMakeupState()
        local _maleOpacity        = maleOpacity
        if not isMaleMakeupOpen then
            _maleOpacity = femaleOpacity
        end
        
        local vals = EffectSdk.vectorf()
        for i = 0,4 do
            if genderInfo:isMan(i) > 0.6 then
                vals:push_back(_maleOpacity)
            elseif genderInfo:isMan(i) < 0.4 then
                vals:push_back(femaleOpacity)
            else
                vals:push_back(femaleOpacity)
            end
        end
        ''' + listToString(makeupTypeList_opacity[0]) + '''
    end,
}'''
                        newLua = addStrToEffect(newLua, '''     
        local feature = this:getFeature("''' + makeupPath[0] + '''")
        local _feature = EffectSdk.castFaceMakeupV2Feature(feature)
        ''' + listToString(makeupTypeList_intensity1[0]))
                        with open(dire + "/event.lua","w",encoding="utf-8") as fw:
                            fw.write(newLua)
                        fw.close()
                    else:
                        print(" -该滤镜已包含‘handleComposerUpdateNodeEvent’")

                    #添加 extra.json 文件
                    if("handleTouchEvent" not in oldLua):
                        extraJSON = '''
{ 
    "settings":{
        "disableExtMakeup": 1
    }
}'''
                        with open(dire + "/extra.json","w",encoding="utf-8") as fw:
                            fw.write(extraJSON)
                        fw.close()
                    else:
                        extraJSON = '''
{ 
    "settings":{
        "disableExtMakeup": 1,
        "touchEvent": 1
    }
}'''
                        with open(dire + "/extra.json","w",encoding="utf-8") as fw:
                            fw.write(extraJSON)
                        fw.close()

                fr.close()
            else:########################################################################
                with open(dire + "/event.lua","r",encoding="utf-8") as fr:
                    oldLua = fr.read()
                    #添加 extra.json 文件
                    if("handleTouchEvent" not in oldLua):
                        extraJSON = '''
{ 
    "settings":{
        "disableExtMakeup": 1
    }
}'''
                        with open(dire + "/extra.json","w",encoding="utf-8") as fw:
                            fw.write(extraJSON)
                        fw.close()
                    else:
                        extraJSON = '''
{ 
    "settings":{
        "disableExtMakeup": 1,
        "touchEvent": 1
    }
}'''
                        with open(dire + "/extra.json","w",encoding="utf-8") as fw:
                            fw.write(extraJSON)
                        fw.close()

                fr.close()
                print("需手动修改...")
        else:
            print("该贴纸缺少 event.lua 脚本")

        if(filterCounter == 1):
            print("滤镜个数：1  " + filterPath[0])
        elif(filterCounter == 2):
            print("滤镜个数：2  " + filterPath[0] + "  " + filterPath[1])
        elif(filterCounter == -1):
            pass
        else:
            pass
        
        if(len(makeupPath) == 1):
            print("美妆个数：1  " + makeupPath[0])
            if(filterCounter == 2 or filterCounter == 3):
                print("滑杆：")
                for item in makeupTypeList_intensity[0]:
                    print(item)
                print("男女适配：")
                for item in makeupTypeList_opacity[0]:
                    print(item)

        elif(len(makeupPath) == 2):
            print("美妆个数：2  " + makeupPath[0] + "  " + makeupPath[1])
            print("滑杆1111：")
            for item in makeupTypeList_intensity[0]:
                print(item)
            print("男女适配1111：")
            for item in makeupTypeList_opacity[0]:
                print(item)
            print("滑杆2222：")
            for item in makeupTypeList_intensity[1]:
                print(item)
            print("男女适配2222：")
            for item in makeupTypeList_opacity[1]:
                print(item)
        elif(len(makeupPath) == 3):
            print("美妆个数：3  " + makeupPath[0] + "  " + makeupPath[1] + "  " + makeupPath[2])
            print("滑杆1111：")
            for item in makeupTypeList_intensity[0]:
                print(item)
            print("男女适配1111：")
            for item in makeupTypeList_opacity[0]:
                print(item)
            print("滑杆2222：")
            for item in makeupTypeList_intensity[1]:
                print(item)
            print("男女适配2222：")
            for item in makeupTypeList_opacity[1]:
                print(item)
            print("滑杆3333：")
            for item in makeupTypeList_intensity[2]:
                print(item)
            print("男女适配3333：")
            for item in makeupTypeList_opacity[2]:
                print(item)
        else:
            print("单独看看")


print("---------------Start...----------------")
# folderList = [THISPATH + "/安卓", THISPATH + "/iOS", THISPATH + "/yangxun"]
# folderList = [THISPATH + "/1014郝志君/自信android", THISPATH + "/1014郝志君/自信ios"]
folderList = [THISPATH + "/ve万圣"]
# folderList = [THISPATH + "/1017晚/有问题"]
# folderList = [THISPATH]

for folder in folderList:
    print("###########" + folder + "############")
    os.chdir(folder)
    main_process(folder)

print("----------------End!!!-----------------")