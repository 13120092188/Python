
attribute vec3 attPosition;
attribute vec2 attUV;

// uniform float angle;
// uniform vec2 scale;
// uniform vec2 center;

// uniform float m_display_width;
// uniform float m_display_height;
// uniform vec4 m_srcRect;

 varying vec2 textureCoordinate;
// varying float zPosition;
// varying vec2 frameUV;

void main() {


    vec2 pos = attPosition.xy;
    // float cosAngle = cos(3.14/180.0 * angle);
    // float sinAngle = sin(3.14/180.0 * angle);

    // float width  = m_display_width;
    // float height = m_display_height;


    // mat2 ratio = mat2(720.0, 0.0, 0.0, 1280.0);
    // mat2 ratio_inv = mat2(width, 0.0, 0.0, height);
    // mat2 rotation = mat2(cosAngle, sinAngle, -sinAngle, cosAngle);
    // mat2 scaleMat = mat2(scale.x,0,0,scale.y);
    // pos =  rotation *scaleMat * ( pos) + center;

    // zPosition = attPosition.z;
    gl_Position = vec4(pos, 0.0, 1.0);
  //  textureCoordinate = attUV.xy * m_srcRect.zw + m_srcRect.xy;
    textureCoordinate = attUV.xy ;
    // frameUV = attUV;
}
