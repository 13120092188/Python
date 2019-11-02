precision highp float;

uniform sampler2D inputImageTexture1;
// uniform sampler2D inputImageTexture2;
varying vec2 textureCoordinate;

void main() 
{
    vec4 color = texture2D(inputImageTexture1,textureCoordinate);
    gl_FragColor = vec4(color.rgb,1.0);
}
