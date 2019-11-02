precision highp float;
varying vec2 texCoord;
varying vec2 sucaiTexCoord;
varying float varOpacity;

uniform sampler2D inputImageTexture;
uniform sampler2D sucaiImageTexture;

uniform float intensity;
uniform int openMouth;

vec3 blendMultiply(vec3 base, vec3 blend) {
    return base * blend;
}

vec3 blendMultiply(vec3 base, vec3 blend, float opacity) {
    return (blendMultiply(base, blend) * opacity + blend * (1.0 - opacity));
}

void main()
{
    vec4 src = texture2D(inputImageTexture, texCoord);
    vec4 meVal = texture2D(sucaiImageTexture, sucaiTexCoord);
    vec3 colorRes = src.rgb;
    if (meVal.a >0.0)
        meVal.rgb = meVal.rgb /meVal.a;
    
    vec3 color = blendMultiply(colorRes, meVal.rgb);

    float alpha = meVal.a * intensity*varOpacity;
    gl_FragColor = vec4(mix(colorRes, color, alpha), 1.0);    
}
