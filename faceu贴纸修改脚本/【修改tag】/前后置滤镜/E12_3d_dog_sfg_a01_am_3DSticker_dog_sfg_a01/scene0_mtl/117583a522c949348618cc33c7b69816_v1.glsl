precision highp float;
attribute vec3 attPosition;
attribute vec2 attUV;
attribute vec3 attNormal;

uniform mat4 g_unif_ModelViewProjMat;

varying vec3 pos0;
varying vec2 uv0;
varying vec2 uv1;
varying vec3 normal0;

void main ()
{
  gl_Position = g_unif_ModelViewProjMat * vec4(attPosition, 1.0);

  pos0 = gl_Position.xyz;
  uv0 = attUV.st;
  normal0 = attNormal.xyz;
  uv1 = pos0.xy * 0.5 + 0.5;   
  uv1.x = uv1.x;
  uv1.y = 1.0 - uv1.y;
}
