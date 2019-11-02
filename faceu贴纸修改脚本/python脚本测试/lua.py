
import sys
import os
import json
import zipfile
import shutil
import string

def addStrToEffect(luaString,s):
        index = luaString.find("handleEffectEvent")
        index1 = luaString[index:index+100].find("eventCode")
        newLuaString = luaString[:index+index1+10] + s + luaString[index+index1+10:]
        print(newLuaString[index+index1:index+index1+100])


with open("event.lua","r",encoding="utf-8") as fr:
    luaString = fr.read()
    addStrToEffect(luaString, '''
        sss''')
