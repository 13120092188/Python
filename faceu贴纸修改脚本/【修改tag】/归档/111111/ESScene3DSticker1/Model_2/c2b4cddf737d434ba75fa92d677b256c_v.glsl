varying vec2 v_texCoord;
varying vec3 v_WorldNormal;
varying vec3 v_WorldTangent;
varying vec3 v_WorldBinormal;
attribute vec3 attPosition;
attribute vec2 attUV;
attribute vec3 attNormal;
attribute vec3 attTangent;
attribute vec3 attBigTangent;
uniform mat4 u_ModelViewProjMat;
uniform mat3 u_NormalWorldMat;
void main ()
{
  v_texCoord.x = attUV.x;
  v_texCoord.y = (1.0 - attUV.y);
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = attPosition;
  gl_Position = (u_ModelViewProjMat * tmpvar_1);
  v_WorldNormal = (u_NormalWorldMat * attNormal);
  v_WorldTangent = (u_NormalWorldMat * attTangent);
  v_WorldBinormal = (u_NormalWorldMat * attBigTangent);
}

