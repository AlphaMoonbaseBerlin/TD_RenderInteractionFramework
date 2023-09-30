'''Info Header Start
Name : extInteractionFramework
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''

from interactionEvent import InteractionEvent, Button
import dimensionalUtils
from typing import Tuple, List

class extInteractionFramework:
	"""
	extInteractionFramework description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp 			: OP 				= ownerComp
		self.CurrentEvent		: InteractionEvent 	= None
		self.PreviousEvent		: InteractionEvent 	= None
		self.SelectedComp		: "objectCOMP"		= None
		self.frameCache			: int				= 0

		self.Buttons		: Button 			= Button
		self.Utils				: dimensionalUtils	= dimensionalUtils 

	@property
	def PanelComp(self) -> panelCOMP:
		return self.ownerComp.par.Panelcomp.eval()

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

	def HandleEvent(self, event:"RenderPickEvent"):

		if self.frameCache == absTime.frame: return
		self.frameCache = absTime.frame


		callbackEvents = []
		self.PreviousEvent = self.CurrentEvent
		self.CurrentEvent = InteractionEvent( 
			event, 
			self.PanelComp.panel, 
			self, 
			SelectedComp = self.SelectedComp )
		if self.PreviousEvent.HoverComp != self.CurrentEvent.HoverComp:
			if self.PreviousEvent.HoverComp:	
				#Hover End
				callbackEvents.append( "HoverEnd" )
				pass
			if self.CurrentEvent.HoverComp:
				callbackEvents.append( "HoverStart" )
				pass
		
		if self.CurrentEvent.Button != self.PreviousEvent.Button:
			if self.CurrentEvent.Button.value:
				self.SelectedComp = self.CurrentEvent.HoverComp
				callbackEvents.append( "SelectStart" )
				pass
			if self.PreviousEvent.Button.value:
				self.SelectedComp = None
				callbackEvents.append( "SelectEnd" )

		if self.SelectedComp and not callbackEvents:
			callbackEvents.append("Move")

		self.CurrentEvent.SelectedComp = self.SelectedComp
		self.DoCallbacks( callbackEvents )
		pass

	def DoCallbacks(self, callbackList : List[str]):
		for callbackName in callbackList:
			self.ownerComp.op("callbackManager").Do_Callback(
				f"on{callbackName}", self.CurrentEvent, self.PreviousEvent, self.ownerComp
			)
		return

	def Testrun(self):
		return self.ProjectRay(0.5, 0.5).ProjectOnPlane(
			self.GetCompPlane( self.ownerComp.par.Testcomp.eval())
		)