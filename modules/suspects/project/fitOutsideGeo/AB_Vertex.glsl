/* Info Header Start
Name : AB_Vertex
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End */


uniform float uAlphaFront;
out Vertex
{
	vec4 color;
	vec3 worldSpacePos;
	vec3 worldSpaceNorm;
	vec2 texCoord0;
	flat int cameraIndex;
	

	vec2 instanceScale;
} oVert;

void main()
{	

	vec3 xScaleVector = TDDeformVec( vec3(1,0,0));
	vec3 yScaleVector = TDDeformVec( vec3(0,1,0));
	oVert.instanceScale = vec2( length( xScaleVector ), length( yScaleVector ));

	
	gl_PointSize = 1.0;
	{ // Avoid duplicate variable defs
		vec3 texcoord = TDInstanceTexCoord(uv[0]);
		oVert.texCoord0.st = texcoord.st;
	}
	// First deform the vertex and normal
	// TDDeform always returns values in world space
	vec4 worldSpacePos = TDDeform(P);
	vec3 uvUnwrapCoord = TDInstanceTexCoord(TDUVUnwrapCoord());
	gl_Position = TDWorldToProj(worldSpacePos, uvUnwrapCoord);


	// This is here to ensure we only execute lighting etc. code
	// when we need it. If picking is active we don't need lighting, so
	// this entire block of code will be ommited from the compile.
	// The TD_PICKING_ACTIVE define will be set automatically when
	// picking is active.
#ifndef TD_PICKING_ACTIVE

	int cameraIndex = TDCameraIndex();
	oVert.cameraIndex = cameraIndex;
	oVert.worldSpacePos.xyz = worldSpacePos.xyz;
	oVert.color = TDInstanceColor(TDPointColor());
	vec3 worldSpaceNorm = normalize(TDDeformNorm(N));
	oVert.worldSpaceNorm.xyz = worldSpaceNorm;

#else // TD_PICKING_ACTIVE

	// This will automatically write out the nessessary values
	// for this shader to work with picking.
	// See the documentation if you want to write custom values for picking.
	TDWritePickingValues();

#endif // TD_PICKING_ACTIVE
}
