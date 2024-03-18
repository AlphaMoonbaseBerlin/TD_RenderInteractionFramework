/* Info Header Start
Name : Pixel
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End */
/* Info Header Start
Name : AB_Pixel
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

uniform vec2 uCorner;

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


#include <shaderUtils>

void main()
{
	// This allows things such as order independent transparency
	// and Dual-Paraboloid rendering to work properly
	TDCheckDiscard();
	

	#if (TEXTUREMODE == AB)
		vec4 colorMapColor = mix(
			calculateFit( sColorMapA, iVert.instanceScale, iVert.texCoord0, uCorner.x, uCorner.y ),
			calculateFit( sColorMapB, iVert.instanceScale, iVert.texCoord0, uCorner.x, uCorner.y ),
			uCross
		);
	#endif
	#if (TEXTUREMODE == Single)
		vec4 colorMapColor = calculateFit( sColorMapA, iVert.instanceScale, iVert.texCoord0, uCorner.x, uCorner.y );
	#endif

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
