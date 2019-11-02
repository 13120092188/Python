local CommonFunc = { 
setFeatureEnabled = function (this, path, status)
    local feature = this:getFeature(path)
    if (feature) then
        feature:setFeatureStatus(EffectSdk.BEF_FEATURE_STATUS_ENABLED, status)
    end
end,
} 
local Sticker2DV3 = { 
    playClipForegroundVertical = function (this, path, entityName, clipName, playTimes)
        local feature = this:getFeature(path)
        local feature_2dv3 = EffectSdk.castSticker2DV3Feature(feature)
        if (feature_2dv3) then
            local effectManager = this:getEffectManager()
            if (effectManager) then
                local aspectRatio = effectManager:getInputAspectRatio()
                if (aspectRatio >= 1.0) then
                    feature_2dv3:resetClip(entityName, clipName)
                    feature_2dv3:playClip(entityName, clipName, -1, playTimes)
                end
            end
        end
    end,
    
    stopClipForegroundVertical = function (this, path, entityName, clipName)
        local feature = this:getFeature(path)
        local feature_2dv3 = EffectSdk.castSticker2DV3Feature(feature)
        if (feature_2dv3) then
            local effectManager = this:getEffectManager()
            if (effectManager) then
                local aspectRatio = effectManager:getInputAspectRatio()
                if (aspectRatio >= 1.0) then
                    feature_2dv3:resumeClip(entityName, clipName, false)
                    feature_2dv3:appearClip(entityName, clipName, false)
                end
            end
        end
    end,
} 
local init_state = 1
local feature_1 = {
folder = "Filter_back",
}
local feature_0 = {
folder = "Filter_front",
}
local feature_2 = {
folder = "2DStickerV3_5102",
clip = { "clipname1" }, 
entity = { "entityname6EBA05AAC1E94578944519B57878FB29" }, 
}

local maleOpacity   = 0.0
local femaleOpacity = 1.0
local filter_folder = "Filter_front"
local filterTimer = 6666


local intensityRecord_makeup = -1

local intensityRecord_filter = -1
EventHandles = {
    handleEffectEvent = function (this, eventCode)
        EffectSdk.LOG_LEVEL(6, "filterTimer test: handleEffectEvent")
        if (-1 < intensityRecord_makeup) then
            local feature = this:getFeature("FaceMakeupV2_byTool")
            local _feature = EffectSdk.castFaceMakeupV2Feature(feature)
            _feature:setIntensity("pupil_faceu+2990", intensityRecord_makeup*0.75)
            _feature:setIntensity("mask_faceuv2+2999", intensityRecord_makeup* 0.8)
            _feature:setIntensity("mask_faceuv2+2995", intensityRecord_makeup* 0.8)
            _feature:setIntensity("eye_part_faceu+2994", intensityRecord_makeup* 0.8)
            _feature:setIntensity("eye_part_faceu+2996", intensityRecord_makeup* 0.8)
            _feature:setIntensity("mask_faceuv2+2997", intensityRecord_makeup* 0.8)
            _feature:setIntensity("eye_part_faceu+2998", intensityRecord_makeup* 0.8)
            _feature:setIntensity("lips_keypoint_faceu+2993", intensityRecord_makeup* 0.64)
        end
        EffectSdk.LOG_LEVEL(6, "filterTimer test: handleEffectEvent1")
        if (init_state == 1 and eventCode == 1) then
            EffectSdk.LOG_LEVEL(6, "filterTimer test: handleEffectEvent2")
            -- ------------------------*#*-----------------------
            -- local effect_manager = this:getEffectManager()
            -- local cameraPosition = effect_manager:getCameraPosition()
            -- if cameraPosition == 0 then--前置
            --     filter_folder = feature_0.folder
            --     CommonFunc.setFeatureEnabled(this, feature_1.folder, false)
            --     CommonFunc.setFeatureEnabled(this, feature_0.folder, true)
            -- else--后置
            --     filter_folder = feature_1.folder
            --     CommonFunc.setFeatureEnabled(this, feature_0.folder, false)
            --     CommonFunc.setFeatureEnabled(this, feature_1.folder, true)
            -- end
            -- if(-1 < intensityRecord_filter) then
            --     local feature = this:getFeature(filter_folder)
            --     feature:setIntensity(intensityRecord_filter)
            -- end
            -- ------------------------#*#-----------------------
            
            EffectSdk.LOG_LEVEL(6, "filterTimer test: handleEffectEvent3")
            init_state = 0
            
            Sticker2DV3.playClipForegroundVertical(this, feature_2.folder, feature_2.entity[1], feature_2.clip[1], 0)

            local effectManager = this:getEffectManager()
            if effectManager then
                local client_state = effectManager:getClientState()
                EffectSdk.LOG_LEVEL(6, "filterTimer test: client_state == "..client_state)
                if client_state == 4 then
                    filter_folder = feature_0.folder
                    local feature = this:getFeature(feature_1.folder)
                    feature:setIntensity(0.0)
                    CommonFunc.setFeatureEnabled(this, feature_1.folder, false)
                    CommonFunc.setFeatureEnabled(this, feature_0.folder, true)
                    if(-1 < intensityRecord_filter) then
                        local feature = this:getFeature(filter_folder)
                        feature:setIntensity(intensityRecord_filter)
                    end
                elseif client_state == 1 then
                    local effect_manager = this:getEffectManager()
                    local cameraPosition = effect_manager:getCameraPosition()
                    if cameraPosition == 0 then--前置
                        filter_folder = feature_0.folder
                        local feature = this:getFeature(feature_1.folder)
                        feature:setIntensity(0.0)
                        CommonFunc.setFeatureEnabled(this, feature_1.folder, false)
                        CommonFunc.setFeatureEnabled(this, feature_0.folder, true)
                    else--后置
                        filter_folder = feature_1.folder
                        local feature = this:getFeature(feature_0.folder)
                        feature:setIntensity(0.0)
                        CommonFunc.setFeatureEnabled(this, feature_0.folder, false)
                        CommonFunc.setFeatureEnabled(this, feature_1.folder, true)
                    end
                    if(-1 < intensityRecord_filter) then
                        local feature = this:getFeature(filter_folder)
                        feature:setIntensity(intensityRecord_filter)
                    end
                end
            end
            EffectSdk.LOG_LEVEL(6, "filterTimer test: handleEffectEvent4")
            EffectSdk.LOG_LEVEL(6, "filterTimer test: handleEffectEvent5")
        end
        return true
    end,
    handleRecodeVedioEvent = function (this, eventCode)
        if (eventCode == 1) then
        
        end
        return true
    end,

    handleDeviceOrientedChangedEvent = function (this,isFront)
        if isFront then
            EffectSdk.LOG_LEVEL(6, "filterTimer test: 后置")
            filter_folder = feature_1.folder
            local feature = this:getFeature(feature_0.folder)
            feature:setIntensity(0.0)
            CommonFunc.setFeatureEnabled(this, feature_0.folder, false)
            CommonFunc.setFeatureEnabled(this, feature_1.folder, true)
        else
            EffectSdk.LOG_LEVEL(6, "filterTimer test: 前置")
            filter_folder = feature_0.folder
            local feature = this:getFeature(feature_1.folder)
            feature:setIntensity(0.0)
            CommonFunc.setFeatureEnabled(this, feature_0.folder, true)
            CommonFunc.setFeatureEnabled(this, feature_1.folder, false)
        end

        local feature = this:getFeature(filter_folder)
        feature:setIntensity(intensityRecord_filter)
        return true
    end,
    handleComposerUpdateNodeEvent = function (this, path, tag, percentage)
        filter_folder = feature_0.folder
        local effectManager = this:getEffectManager()
        -- EffectSdk.LOG_LEVEL(6, "filterTimer test: effectManager == "..effectManager)
        if effectManager then
            local client_state = effectManager:getClientState()
            EffectSdk.LOG_LEVEL(6, "filterTimer test: client_state == "..client_state)
            if client_state == 1 then
                local effect_manager = this:getEffectManager()
                local cameraPosition = effect_manager:getCameraPosition()
                if cameraPosition == 0 then--前置
                    filter_folder = feature_0.folder
                else
                    filter_folder = feature_1.folder
                end
            end
        end
        local feature = this:getFeature(filter_folder)
        -- local _feature = EffectSdk.castFaceMakeupV2Feature(feature)
        if (not feature)  then
            print("Filter is not exist")
            return false
        end
        if tag == "Internal_Filter" then
            feature:setIntensity(percentage)

            intensityRecord_filter = percentage
        end

        
        local feature = this:getFeature("FaceMakeupV2_byTool")
        local _feature = EffectSdk.castFaceMakeupV2Feature(feature)
        if (not feature) or (not _feature) then
            print("FaceMakeupV2_byTool is not exist")
            return false
        end
        if tag == "Internal_Makeup" then
            _feature:setIntensity("pupil_faceu+2990",percentage*0.75)
            _feature:setIntensity("lips_keypoint_faceu+2991",percentage)
            _feature:setIntensity("mask_faceuv2+2999",percentage*0.8)
            _feature:setIntensity("mask_faceuv2+2995",percentage*0.8)
            _feature:setIntensity("eye_part_faceu+2994",percentage*0.8)
            _feature:setIntensity("eye_part_faceu+2996",percentage*0.8)
            _feature:setIntensity("mask_faceuv2+2997",percentage*0.8)
            _feature:setIntensity("eye_part_faceu+2998",percentage*0.8)
            _feature:setIntensity("lips_keypoint_faceu+2993",percentage*0.64)
            intensityRecord_makeup = percentage
        end
    end,
    handleGenderEvent = function(this, genderInfo)
        local feature = this:getFeature("FaceMakeupV2_byTool")
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
        _feature:setOpacity("pupil_faceu+2990",vals)
        _feature:setOpacity("lips_keypoint_faceu+2991",vals)
        _feature:setOpacity("mask_faceuv2+2999",vals)
        _feature:setOpacity("mask_faceuv2+2995",vals)
        _feature:setOpacity("eye_part_faceu+2994",vals)
        _feature:setOpacity("eye_part_faceu+2996",vals)
        _feature:setOpacity("mask_faceuv2+2997",vals)
        _feature:setOpacity("eye_part_faceu+2998",vals)
        _feature:setOpacity("lips_keypoint_faceu+2993",vals)
    end,
}

