

local CommonFunc = {
setFeatureEnabled = function (this, path, status)
    local feature = this:getFeature(path)
    if (feature) then
        feature:setFeatureStatus(EffectSdk.BEF_FEATURE_STATUS_ENABLED, status)
    end
end,
}

local Sticker2DV3 = {
playClip = function (this, path, entityName, clipName, playTimes)
    local feature = this:getFeature(path)
    local feature_2dv3 = EffectSdk.castSticker2DV3Feature(feature)
    if (feature_2dv3) then
        feature_2dv3:resetClip(entityName, clipName)
        feature_2dv3:playClip(entityName, clipName, -1, playTimes)
    end
end,
stopClip = function (this, path, entityName, clipName)
    local feature = this:getFeature(path)
    local feature_2dv3 = EffectSdk.castSticker2DV3Feature(feature)
    if (feature_2dv3) then
        feature_2dv3:resumeClip(entityName, clipName, false)
        feature_2dv3:appearClip(entityName, clipName, false)
    end
end,
playLastClip = function (this, path, entityName, clipName)
    local feature = this:getFeature(path)
    local feature_2dv3 = EffectSdk.castSticker2DV3Feature(feature)
    if (feature_2dv3) then
        feature_2dv3:resumeClip(entityName, clipName, false)
        feature_2dv3:appearClip(entityName, clipName, true)
    end
end,
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
playClipForegroundHorizontal = function (this, path, entityName, clipName, playTimes)
    local feature = this:getFeature(path)
    local feature_2dv3 = EffectSdk.castSticker2DV3Feature(feature)
    if (feature_2dv3) then
        local effectManager = this:getEffectManager()
        if (effectManager) then
            local aspectRatio = effectManager:getInputAspectRatio()
            if (aspectRatio < 1.0) then
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
stopClipForegroundHorizontal = function (this, path, entityName, clipName)
    local feature = this:getFeature(path)
    local feature_2dv3 = EffectSdk.castSticker2DV3Feature(feature)
    if (feature_2dv3) then
        local effectManager = this:getEffectManager()
        if (effectManager) then
            local aspectRatio = effectManager:getInputAspectRatio()
            if (aspectRatio < 1.0) then
                feature_2dv3:resumeClip(entityName, clipName, false)
                feature_2dv3:appearClip(entityName, clipName, false)
            end
        end
    end
end,
playLastClipForegroundVertical = function (this, path, entityName, clipName)
    local feature = this:getFeature(path)
    local feature_2dv3 = EffectSdk.castSticker2DV3Feature(feature)
    if (feature_2dv3) then
        local effectManager = this:getEffectManager()
        if (effectManager) then
            local aspectRatio = effectManager:getInputAspectRatio()
            if (aspectRatio >= 1.0) then
                feature_2dv3:resumeClip(entityName, clipName, false)
                feature_2dv3:appearClip(entityName, clipName, true)
            end
        end
    end
end,
playLastClipForegroundHorizontal = function (this, path, entityName, clipName)
    local feature = this:getFeature(path)
    local feature_2dv3 = EffectSdk.castSticker2DV3Feature(feature)
    if (feature_2dv3) then
        local effectManager = this:getEffectManager()
        if (effectManager) then
            local aspectRatio = effectManager:getInputAspectRatio()
            if (aspectRatio < 1) then
                feature_2dv3:resumeClip(entityName, clipName, false)
                feature_2dv3:appearClip(entityName, clipName, true)
            end
        end
    end
end,
}



local maleOpacity   = 0.0
local femaleOpacity = 1.0
local init_state = 1
local feature_0 = {
        folder = "ES3DV3Spritea26d4789edfc4ec9a7bcfa5d6f80ce7f",
        clip = { "ProcessorName_0" }, 
        entity = { "scene3d_12f5dad1cfc64ahzjcd89de75d86b7c3b03" }, 
}
EventHandles = {
    handleEffectEvent = function (this, eventCode)
        if (init_state == 1 and eventCode == 1) then
            init_state = 0
            local image2DManager = this:getImage2DManager()
            if (image2DManager) then
                image2DManager:play(feature_0.entity[1], feature_0.clip[1], 0)

            end
        end
        return true
    end,
    handleRecodeVedioEvent = function (this, eventCode)
        if (eventCode == 1) then
            CommonFunc.setFeatureEnabled(this, feature_0.folder, true)
            Sticker2DV3.playClip(this, feature_0.folder, feature_0.entity[1], feature_0.clip[1], 0)
        end
        return true
    end,
    
    handleComposerUpdateNodeEvent = function (this, path, tag, percentage)
        local feature = this:getFeature("Filter_5101")
        -- local _feature = EffectSdk.castFaceMakeupV2Feature(feature)
        if (not feature)  then
            print("Filter is not exist")
            return false
        end
        if tag == "Internal_Filter" then
            feature:setIntensity(percentage)
        end

        
        local feature = this:getFeature("FaceMakeupV2_byTool")
        local _feature = EffectSdk.castFaceMakeupV2Feature(feature)
        if (not feature) or (not _feature) then
            print("FaceMakeupV2_byTool is not exist")
            return false
        end
        if tag == "Internal_Makeup" then
        _feature:setIntensity("pupil_faceu+2994",percentage)
        _feature:setIntensity("lips_keypoint_faceu+2995",percentage)
        _feature:setIntensity("lips_keypoint_faceu+2997",percentage)
        _feature:setIntensity("mask_faceuv2+2998",percentage)
        _feature:setIntensity("mask_faceuv2+2998",percentage)
        _feature:setIntensity("eye_part_faceu+2991",percentage)
        _feature:setIntensity("eye_part_faceu+2992",percentage)
        _feature:setIntensity("eye_part_faceu+2993",percentage)
        _feature:setIntensity("mask_faceuv2+2998",percentage)
        
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
        _feature:setOpacity("pupil_faceu+2994",vals)
        _feature:setOpacity("lips_keypoint_faceu+2995",vals)
        _feature:setOpacity("lips_keypoint_faceu+2997",vals)
        _feature:setOpacity("mask_faceuv2+2998",vals)
        _feature:setOpacity("mask_faceuv2+2998",vals)
        _feature:setOpacity("eye_part_faceu+2991",vals)
        _feature:setOpacity("eye_part_faceu+2992",vals)
        _feature:setOpacity("eye_part_faceu+2993",vals)
        _feature:setOpacity("mask_faceuv2+2998",vals)
        
    end,
}