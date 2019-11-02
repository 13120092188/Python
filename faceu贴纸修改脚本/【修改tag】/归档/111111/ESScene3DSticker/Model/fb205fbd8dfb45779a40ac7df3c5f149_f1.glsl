
    precision highp float;
    precision highp sampler2D;
varying highp vec2 v_texCoord;
varying highp vec3 v_WorldNormal;
varying highp vec3 v_WorldTangent;
varying highp vec3 v_WorldBinormal;
uniform sampler2D u_colorTexture;
uniform sampler2D u_normalTexture;
void main ()
{
  vec3 viewN_1;
  highp mat3 tmpvar_2;
  tmpvar_2[0] = v_WorldTangent;
  tmpvar_2[1] = v_WorldBinormal;
  tmpvar_2[2] = v_WorldNormal;
  vec3 tmpvar_3;
  tmpvar_3 = ((normalize(
    (tmpvar_2 * ((texture2D (u_normalTexture, v_texCoord).xyz * 2.0) - 1.0))
  ) * 0.5) + 0.5);
  viewN_1.xz = tmpvar_3.xz;
  viewN_1.y = (1.0 - tmpvar_3.y);
  vec4 tmpvar_4;
  tmpvar_4.w = 1.0;
  tmpvar_4.xyz = texture2D (u_colorTexture, viewN_1.xy).xyz;
  gl_FragColor = tmpvar_4;
}

