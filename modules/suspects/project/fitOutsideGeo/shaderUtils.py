/* Info Header Start
Name : shaderUtils
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End */
'''Info Header Start
Name : shaderUtils
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''
/* Info Header Start
Name : shaderUtils
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End */

vec4 calculateFit( sampler2D colorMap, vec2 geometryScaling, vec2 texCoord ){
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
	return texture(colorMap, texCoord0.st);
}