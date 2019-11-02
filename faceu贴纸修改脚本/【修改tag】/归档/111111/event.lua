local CommonFunc = { 
setFeatureEnabled = function (this, path, status)
    local feature = this:getFeature(path)
    if (feature) then
        feature:setFeatureStatus(EffectSdk.BEF_FEATURE_STATUS_ENABLED, status)
    end
end,
} 
local init_state = 1
local state_2 = 666
local state_4 = 666
local feature_0 = {
folder = "Filter_5100",
}
local feature_1 = {
folder = "ESScene3DSticker",
}
local feature_2 = {
folder = "ESScene3DSticker1",
}

local maleOpacity   = 0.0
local femaleOpacity = 1.0

local intensityRecord_makeup = -1
EventHandles = {
    handleEffectEvent = function (this, eventCode)     
        if (-1 < intensityRecord_makeup) then
            local feature = this:getFeature("FaceMakeupV2_byTool")
            local _feature = EffectSdk.castFaceMakeupV2Feature(feature)
            _feature:setIntensity("pupil_faceu+2990", intensityRecord_makeup*0.75)
            _feature:setIntensity("mask_faceuv2+2999", intensityRecord_makeup*0.8)
            _feature:setIntensity("mask_faceuv2+2995", intensityRecord_makeup*0.8)
            _feature:setIntensity("eye_part_faceu+2994", intensityRecord_makeup*0.8)
            _feature:setIntensity("eye_part_faceu+2996", intensityRecord_makeup*0.8)
            _feature:setIntensity("mask_faceuv2+2997", intensityRecord_makeup*0.8)
            _feature:setIntensity("eye_part_faceu+2998", intensityRecord_makeup*0.8)
            _feature:setIntensity("lips_keypoint_faceu+2993", intensityRecord_makeup*0.64)
        end
        
        if (init_state == 1 and eventCode == 1) then
            init_state = 0
            CommonFunc.setFeatureEnabled(this, feature_0.folder, true)
            CommonFunc.setFeatureEnabled(this, feature_1.folder, true)
            CommonFunc.setFeatureEnabled(this, feature_2.folder, true)
            state_4 = 0
        end
        return true
    end,
    handleRecodeVedioEvent = function (this, eventCode)
        -- if (eventCode == 1) then
        --     CommonFunc.setFeatureEnabled(this, feature_0.folder, false)
        --     CommonFunc.setFeatureEnabled(this, feature_1.folder, false)
        --     CommonFunc.setFeatureEnabled(this, feature_2.folder, false)
        --     CommonFunc.setFeatureEnabled(this, feature_0.folder, true)
        --     CommonFunc.setFeatureEnabled(this, feature_1.folder, true)
        --     CommonFunc.setFeatureEnabled(this, feature_2.folder, true)
        -- end
        -- return true
    end,
    handleTouchEvent = function (this, eventCode)
        if (eventCode == 1) then
            if (state_2 == 0) then
                state_2 = 1
                CommonFunc.setFeatureEnabled(this, feature_1.folder, true)
                CommonFunc.setFeatureEnabled(this, feature_2.folder, true)
                state_4 = 0

            elseif (state_4 == 0) then
                state_4 = 1
                CommonFunc.setFeatureEnabled(this, feature_1.folder, true)
                CommonFunc.setFeatureEnabled(this, feature_2.folder, false)

                state_2 = 0
            end
        end
        return true
    end,
    handleComposerUpdateNodeEvent = function (this, path, tag, percentage)
        local feature = this:getFeature("Filter_5100")
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