attribute vec3 attPosition;
attribute vec2 attUV;
uniform mat4 g_unif_ModelViewProjMat;
varying vec2 g_vary_Texcoord;

uniform vec4 mvpVec0;
uniform vec4 mvpVec1;
uniform vec4 mvpVec2;
uniform vec4 mvpVec3;

mat4 transpose(mat4 m) {
  return mat4(m[0][0], m[1][0], m[2][0], m[3][0],
              m[0][1], m[1][1], m[2][1], m[3][1],
              m[0][2], m[1][2], m[2][2], m[3][2],
              m[0][3], m[1][3], m[2][3], m[3][3]);
}

void main ()
{
  vec4 tmpvar_1;
  tmpvar_1.w = 1.0;
  tmpvar_1.xyz = attPosition;
  g_vary_Texcoord.x = attUV.x;
  g_vary_Texcoord.y = 1.0 - attUV.y;
  mat4 ModelViewProjMat = mat4(mvpVec0.x, mvpVec0.y, mvpVec0.z, mvpVec0.w,
                              -mvpVec1.x, -mvpVec1.y, -mvpVec1.z, -mvpVec1.w,
                               mvpVec2.x, mvpVec2.y, mvpVec2.z, mvpVec2.w,
                               mvpVec3.x, mvpVec3.y, mvpVec3.z, mvpVec3.w);
  mat4 trans = transpose(ModelViewProjMat);
  gl_Position = (g_unif_ModelViewProjMat * tmpvar_1);
}

