/* Info Header Start
Name : phong1GLSLPixel
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End */

uniform float uAlphaFront;
uniform sampler2D sColorMapA;
uniform sampler2D sColorMapB;
uniform float uFitMode;
uniform float uScale;
uniform vec2 uAnchor;
uniform float uCross;

in Vertex
{
	vec4 color;
	vec3 worldSpacePos;
	vec3 worldSpaceNorm;
	vec2 texCoord0;
	flat int cameraIndex;
	vec2 instanceScale;
} iVert;

// Output variable for the color
layout(location = 0) out vec4 oFragColor[TD_NUM_COLOR_BUFFERS];


vec4 calculateFit( sampler2D colorMap ){
	vec2 geometryScaling = iVert.instanceScale;

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
	vec2 texCoord0 = iVert.texCoord0.st * textureScaling + textureOffset;
	return texture(colorMap, texCoord0.st);
}

void main()
{
	// This allows things such as order independent transparency
	// and Dual-Paraboloid rendering to work properly
	TDCheckDiscard();
	


	vec4 colorMapColor = calculateFit( sColorMapA );


	// Flip the normals on backfaces
	// On most GPUs this function just return gl_FrontFacing.
	// However, some Intel GPUs on macOS have broken gl_FrontFacing behavior.
	// When one of those GPUs is detected, an alternative way
	// of determing front-facing is done using the position
	// and normal for this pixel.
	vec3 worldSpaceNorm = normalize(iVert.worldSpaceNorm.xyz);
	vec3 normal = normalize(worldSpaceNorm.xyz);
	if (!TDFrontFacing(iVert.worldSpacePos.xyz, worldSpaceNorm.xyz))
	{
		normal = -normal;
	}


	// Modern GL removed the implicit alpha test, so we need to apply
	// it manually here. This function does nothing if alpha test is disabled.
	vec4 finalColor = vec4( colorMapColor );
	finalColor *= uAlphaFront;
	TDAlphaTest(finalColor.a);

	oFragColor[0] = TDOutputSwizzle(finalColor);


	// TD_NUM_COLOR_BUFFERS will be set to the number of color buffers
	// active in the render. By default we want to output zero to every
	// buffer except the first one.
	for (int i = 1; i < TD_NUM_COLOR_BUFFERS; i++)
	{
		oFragColor[i] = vec4(0.0);
	}
}
