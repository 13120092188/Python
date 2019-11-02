attribute vec3 attPosition;
attribute vec2 attUV;


varying vec2 texCoord;
varying vec2 screenCoord;
void main(void){
    gl_Position = vec4(attPosition,1.0);
    texCoord = attUV;
    screenCoord = gl_Position.xy * 0.5 +0.5;
}