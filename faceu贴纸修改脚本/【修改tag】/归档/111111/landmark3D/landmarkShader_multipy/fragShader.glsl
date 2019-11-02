precision highp float;
varying vec2 texCoord;
varying vec2 screenCoord;
//原视频
uniform sampler2D inputImageTexture1;

//3d美妆
uniform sampler2D inputImageTexture2;

uniform float intensity;

vec3 blendMultiply(vec3 base, vec3 blend) {
    return base * blend;
}



void main()
{
    vec4 src = texture2D(inputImageTexture1, screenCoord);
    vec4 meVal = texture2D(inputImageTexture2, texCoord);


    if(meVal.a > 0.0)
      meVal.rgb = meVal.rgb / meVal.a;
    vec3 color = blendMultiply(src.rgb, meVal.rgb);
    
    gl_FragColor = vec4(color,meVal.a);

}
