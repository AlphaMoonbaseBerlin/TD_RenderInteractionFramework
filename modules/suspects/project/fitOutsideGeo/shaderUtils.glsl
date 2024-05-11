/* Info Header Start
Name : shaderUtils
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End */

uniform float uBorderWidth;
uniform vec4 uBorderColor;
float udRoundBox( vec2 p, vec2 b, float r )
{
  return length(max(abs(p),b))-r;
}

vec2 map(vec2 value, vec2 min1, vec2 max1, vec2 min2, vec2 max2) {
  return min2 + (value - min1) * (max2 - min2) / (max1 - min1);
}

float sdRoundBox( vec2 position, vec2 bounds, float radius ) 
{
	vec2 p = map( position, vec2(0), bounds, -bounds/2, bounds/2 );
	vec2 b = bounds;
	vec4 r = vec4(radius);
    r.xy = (p.x>0.0)?r.xy : r.zw;
    r.x  = (p.y>0.0)?r.x  : r.y;
    vec2 q = abs(p)-b/2+r.x;
    return min(max(q.x,q.y),0.0) + length(max(q,0.0)) - r.x;
}

vec4 calculateFit( sampler2D colorMap, vec2 geometryScaling, vec2 texCoord, float cornerRadius, float cornerFeather ){
	//vec2 geometryScaling = iVert.instanceScale;

	//Getting and calculating initital textureLookup.
	vec2 textureSize = vec2( textureSize( colorMap, 0 ) ) / geometryScaling;
		
	vec2 textureScalingFitInside = vec2(1/uScale);
	vec2 textureScalingFitOutside = vec2(1/uScale);

	vec2 textureOffsetFitInside = vec2(0);
	vec2 textureOffsetFitOutside = vec2(0);

	float textureRelation = 1;
	
		//Fit Inside
		textureRelation = float(textureSize.x) / float(textureSize.y);
		if ( textureSize.x > textureSize.y) {
			textureScalingFitInside.y *= textureRelation;
			textureOffsetFitInside.y = (1 - textureRelation)/2*uAnchor.y;
		} else {
			textureScalingFitInside.x /= textureRelation;
			textureOffsetFitInside.x = (1 - 1/textureRelation)/2*uAnchor.x;
		}
	
	
		//Fit Inside
		textureRelation = float(textureSize.y) / float(textureSize.x);
		if ( textureSize.x < textureSize.y) {
			textureScalingFitOutside.y /= textureRelation;
			textureOffsetFitOutside.y = (1 - 1/textureRelation)/2*uAnchor.y;
		} else {
			textureScalingFitOutside.x *= textureRelation;
			textureOffsetFitOutside.x = (1 - textureRelation)/2*uAnchor.x;
		}
	
	vec2 textureScaling = mix(textureScalingFitInside, textureScalingFitOutside, uFitMode);
	vec2 textureOffset = mix(textureOffsetFitInside, textureOffsetFitOutside, uFitMode);
	vec2 texCoord0 = texCoord * textureScaling + textureOffset;
	vec4 outputTexture = texture(colorMap, texCoord0.st);

	#ifdef CORNEREDIT
		float distance = -sdRoundBox(  
			min((texCoord + textureOffset * textureRelation )  * geometryScaling, texCoord * geometryScaling)  ,
			min(geometryScaling / textureScaling, geometryScaling) , 
			cornerRadius) ;

		outputTexture = mix( 
			uBorderColor,
			outputTexture,
			smoothstep(
				uBorderWidth, uBorderWidth + cornerFeather, distance
			) );
		//Runding the Edges
		outputTexture *= smoothstep(0, cornerFeather, distance) ;
		//Doing Border
	
	#endif
	//outputTexture.r = textureRelation;
	
	return outputTexture;
}