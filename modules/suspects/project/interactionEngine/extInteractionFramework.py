'''Info Header Start
Name : extInteractionFramework
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''

import dimensionalUtils
from typing import Tuple
class extInteractionFramework:
	"""
	extInteractionFramework description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp:OP = ownerComp
		self.hoverOp:tdu.Dependency[objectCOMP] = tdu.Dependency( None )

	@property
	def Camera(self) -> cameraCOMP:
		return self.ownerComp.par.Cameracomp.eval()
	@property 
	def renderDimensions(self) -> Tuple[int, int]:
		return self.ownerComp.par.Rendertop.eval().width, self.ownerComp.par.Rendertop.eval().height
	 
	def ProjectRay(self, u:float, v: float) -> dimensionalUtils.Ray:
		projectionMatrix:tdu.Matrix 	= self.Camera.projectionInverse( *self.renderDimensions )
		transformationMatrix:tdu.Matrix = self.Camera.transform()
		remappedU 	= tdu.remap( u, 0, 1, -1, 1)
		remappedV 	= tdu.remap( v, 0, 1, -1, 1)
		pointNear 	= projectionMatrix * tdu.Position(remappedU, remappedV, -1)
		pointFar 	= projectionMatrix * tdu.Position(remappedU, remappedV, 1)
		direction 	= tdu.Vector( pointFar - pointNear )
		return dimensionalUtils.Ray( 
			transformationMatrix * pointNear, 
			transformationMatrix * direction)
	
	def GetCompPlane(self, targetComp:COMP):
		return dimensionalUtils.Plane(
			dimensionalUtils.CompPosition( targetComp ),
			targetComp.transform() * tdu.Vector( 0, 0, 1)
		)
	
	def GetCompCameraPlane(self, targetComp:COMP):
		return dimensionalUtils.Plane(
			dimensionalUtils.CompPosition( targetComp ),
			dimensionalUtils.CompPosition( self.Camera ) - dimensionalUtils.CompPosition( targetComp)
		)

	def HandleEvent(self, event:RenderPickEvent):
		self.hoverOp.val = event.pickOp
		
		pass

	def Testrun(self):
		return self.ProjectRay(0.5, 0.5).ProjectOnPlane(self.GetCompPlane( self.ownerComp.par.Testcomp.eval()))