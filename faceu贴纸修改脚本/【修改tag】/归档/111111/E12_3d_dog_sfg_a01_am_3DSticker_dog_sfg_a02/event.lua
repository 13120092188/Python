
local FaceEntityID = {
    '6', '7', '8', '9', '10'
}

local g_FaceGuid = { }
local isFirstTime = true

g_GuidFaceIdTable = {}

CommonFunc = {
    bindEntityToFaceID = function ( guid, faceid )
        g_GuidFaceIdTable[guid] = faceid
        -- print(string.format('Bind [GUID=%d FaceID=%d]\n', guid, faceid))
    end,
    unbindEntityToAnyFaceID = function ( guid )
        local faceid = g_GuidFaceIdTable[guid]
        if (faceid ~= nil) then
            -- print(string.format('UnBind [GUID=%s FaceID=%d]\n', guid, faceid))
            g_GuidFaceIdTable[guid] = nil
        end
    end,
    getBindedFaceID = function ( guid )
        local faceid = g_GuidFaceIdTable[guid]
        if (faceid ~= nil) then
            return faceid
        else
            return nil
        end
    end
}
local feature_0 = {
    folder = "E12_3d_dog_sfg_a01_am_3DSticker_dog_sfg_a01",
    }
EventHandles = {

    handleFaceFittingEvent = function (this, eventContent)
        feature3d = this
        if( not feature3d ) then 
            return false
        end

        local scene0 = feature3d:getLuaScene(0)
        if( not scene0 ) then
            return false
        end

        if( isFirstTime ) then
            for i,v in ipairs(FaceEntityID) do
                local guid = scene0:getEntityGUIDWithName(v)
                g_FaceGuid[i] = guid
                -- print(string.format('[GUID=%d]\n', guid))
            end
            isFirstTime = false
        end

        local camera0GUID = scene0:getEntityGUIDWithName("1")
        if( not camera0GUID) then
            return
        end

        face_mesh_st = eventContent.faceFittingInfo
        faceCount = face_mesh_st.face_mesh_info_count

        display_height = face_mesh_st.view_height
        display_width = face_mesh_st.view_width

        scene0:setScaleGUID(camera0GUID, display_height, display_height, 2)

        if(faceCount <= 0) then
            return false
        end

        faceMeshInfo_ptr = EffectSdk.faceFittingMeshInfoArray.frompointer(face_mesh_st.face_mesh_info)
        -- faceMeshConfig_ptr = EffectSdk.faceFittingMeshCfgArray.frompointer(face_mesh_st.face_mesh_cfg)

        -- 局部变量, 统计所有实时的Face ID
        local l_FaceId = { }
        for i = 0, faceCount-1 do
            -- key: 算法的faceid, value: 结果数组索引值
            l_FaceId[faceMeshInfo_ptr[i].id] = i 
            -- print(string.format('[l_FaceId=%d, index=%d]\n', faceMeshInfo_ptr[i].id, i))
        end

        -- 局部变量, 统计所有实时的已绑定好的Face ID
        local l_FaceIdGuidTable = { }
        -- 计算哪些Face ID未变, 哪些旧Face ID应该删除
        for i,v in pairs(g_FaceGuid) do
            local faceid = CommonFunc.getBindedFaceID(v)
            if (faceid) then
                local faceindex = l_FaceId[faceid]
                if (not faceindex) then
                    CommonFunc.unbindEntityToAnyFaceID(v)
                    scene0:setVisibleWithGUID(v, false)
                else
                    l_FaceIdGuidTable[faceid] = v
                end
            end
        end

        -- 统计所有实时的未绑定好的Face ID, 添加新增Face ID
        for faceid,v in pairs(l_FaceId) do
            local guid = l_FaceIdGuidTable[faceid]
            if( not guid ) then
                for i,faceguid in pairs(g_FaceGuid) do
                    local face_id = CommonFunc.getBindedFaceID(faceguid)
                    if (not face_id) then
                        CommonFunc.bindEntityToFaceID(faceguid, faceid)
                        -- print(faceguid, faceid)
                        l_FaceIdGuidTable[faceid] = faceguid
                        break
                    end
                end
            end
        end

        -- for k,v in pairs(l_FaceIdGuidTable) do
        --     print(k,v)
        -- end

        -- for k,v in pairs(l_FaceId) do
        --     print(k,v)
        -- end
        for faceid,v in pairs(l_FaceId) do
            if (faceid) then
                local guid = l_FaceIdGuidTable[faceid]
                if (guid) then
                    -- print(string.format('[GUID=%d]\n', guid))
                    
                    local data0 = EffectSdk.MetaDataST(faceMeshInfo_ptr[v].vertex_count/3, face_mesh_st.face_mesh_cfg.flist_count, faceMeshInfo_ptr[v].vertex_count/3)
                    local vertex_ptr = EffectSdk.floatArray.frompointer(faceMeshInfo_ptr[v].vertex) 
                    local uv_ptr = EffectSdk.floatArray.frompointer(face_mesh_st.face_mesh_cfg.uv)
                    local param_ptr = EffectSdk.floatArray.frompointer(faceMeshInfo_ptr[v].param)
                    local mvp_ptr = EffectSdk.floatArray.frompointer(faceMeshInfo_ptr[v].mvp)
                    data0:setVertexListPos(vertex_ptr)
                    data0:setVertexListUV(uv_ptr)
                    
                    -- for i = 0, 15 do
                    --     print("yk: mvp[" .. i .. "]", mvp_ptr[i])
                    -- end
                    -- 传uniformVec4组装mvp给shader
                    scene0:setUniformVec4(guid, "mvpVec0", mvp_ptr[0], mvp_ptr[1], mvp_ptr[2], mvp_ptr[3], true)
                    scene0:setUniformVec4(guid, "mvpVec1", mvp_ptr[4], mvp_ptr[5], mvp_ptr[6], mvp_ptr[7], true)
                    scene0:setUniformVec4(guid, "mvpVec2", mvp_ptr[8], mvp_ptr[9], mvp_ptr[10], mvp_ptr[11], true)
                    scene0:setUniformVec4(guid, "mvpVec3", mvp_ptr[12], mvp_ptr[13], mvp_ptr[14], mvp_ptr[15], true)

                    scene0:setOrientationGUID(guid, param_ptr[1], param_ptr[2], param_ptr[3])
                    scene0:setPositionGUID(guid, param_ptr[4]-display_width/2, param_ptr[5]-display_height/2, 0)
                    scene0:setScaleGUID(guid, param_ptr[0], param_ptr[0], param_ptr[0])
             
                    local index0_ptr = EffectSdk.ushortArray.frompointer(face_mesh_st.face_mesh_cfg.flist)
                    data0:setIndiceList(index0_ptr)

                    scene0:updateMeshCooking(guid, data0)
                    scene0:setVisibleWithGUID(guid, true)
                end
            end
        end

        -- print(faceMeshInfo_ptr[face_idx])
        -- print(string.format('Index=%d, FaceID=%d\n', face_idx, faceMeshInfo_ptr[face_idx].id))
        -- print(faceMeshConfig_ptr[face_idx].flist_count)
        -- print(faceMeshInfo_ptr[face_idx].param_count)

    end
}