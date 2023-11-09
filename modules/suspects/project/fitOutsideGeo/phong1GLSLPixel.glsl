/* Info Header Start
Name : phong1GLSLPixel
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End */

uniform float uAlphaFront;
uniform sampler2D sColorMap;
uniform int uFitMode;
uniform float uScale;
uniform vec2 uAnchor;


in Vertex
{
	vec4 color;
	vec3 worldSpacePos;
	vec3 worldSpaceNorm;
	vec2 texCoord0;
	flat int cameraIndex;
	mat4 wolrdTransform;
} iVert;

// Output variable for the color
layout(location = 0) out vec4 oFragColor[TD_NUM_COLOR_BUFFERS];
void main()
{
	// This allows things such as order independent transparency
	// and Dual-Paraboloid rendering to work properly
	TDCheckDiscard();
	
	//Calculating the Geometry Scale
	vec4 up 		= iVert.wolrdTransform * vec4(0,1,0,0);
	vec4 right 		= iVert.wolrdTransform * vec4(1,0,0,0);
	vec4 center 	= iVert.wolrdTransform * vec4(0,0,0,0);

	vec2 geometryScaling 	= vec2(length( center - right), length(center - up));

	//Getting and calculating initital textureLookup.
	vec2 textureSize = vec2( textureSize( sColorMap, 0 ) ) / geometryScaling;
		
	vec2 textureScaling = vec2(1/uScale);
	vec2 textureOffset = vec2(0);


	//Doing Fitmode! 
	//TODO: Make them slerpable.
	if(uFitMode == 0) {
		//Fit Inside
		float textureRelation = float(textureSize.x) / float(textureSize.y);
		if ( textureSize.x > textureSize.y) {
			textureScaling.y *= textureRelation;
			textureOffset.y = (1 - textureRelation)/2*uAnchor.y;
		} else {
			textureScaling.x /= textureRelation;
			textureOffset.x = (1 - 1/textureRelation)/2*uAnchor.x;
		}
	}
	if(uFitMode == 1) {
		//Fit Inside
		float textureRelation = float(textureSize.y) / float(textureSize.x);
		if ( textureSize.x < textureSize.y) {
			textureScaling.y /= textureRelation;
			textureOffset.y = (1 - 1/textureRelation)/2*uAnchor.y;
		} else {
			textureScaling.x *= textureRelation;
			textureOffset.x = (1 - textureRelation)/2*uAnchor.x;
		}
	}
	vec2 texCoord0 = iVert.texCoord0.st * textureScaling + textureOffset;
	

	vec4 colorMapColor = texture(sColorMap, texCoord0.st);
	//colorMapColor.rg = vec2(relation);
	
	//colorMapColor.b = 0;
	//colorMapColor.rgb = up.rgb;


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
