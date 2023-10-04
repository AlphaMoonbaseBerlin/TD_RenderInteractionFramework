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

		self.SelectStartEvent	: InteractionEvent	= None

		self.ClickCount			: int				= 0
		self.ClickTimer			: Run				= run("pass")

		self.frameCache			: int				= 0

		self.Buttons			: Button 			= Button
		self.Utils				: dimensionalUtils	= dimensionalUtils 

	@property
	def PanelComp(self) -> panelCOMP:
		return self.ownerComp.par.Panelcomp.eval()

	@property
	def Camera(self) -> cameraCOMP:
		return self.ownerComp.par.Cameracomp.eval()
	@property 
	def RenderDimensions(self) -> Tuple[int, int]:
		return self.ownerComp.par.Rendertop.eval().width, self.ownerComp.par.Rendertop.eval().height
	 
	def ProjectRay(self, u:float, v: float) -> dimensionalUtils.Ray:
		projectionMatrix:tdu.Matrix 	= self.Camera.projectionInverse( *self.RenderDimensions )
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
				self.SelectStartEvent 	= self.CurrentEvent
				self.SelectedComp 		= self.CurrentEvent.HoverComp
				self.ClickCount 		+= 1
				self._stopClickTimer()
				self.ClickTimer = run("args[0]()", lambda : self._checkClick( self.CurrentEvent ), delayMilliSeconds=self.ownerComp.par.Multitaptiming.eval())
				
				callbackEvents.append( "SelectStart" )
				pass
			if self.PreviousEvent.Button.value:
				self.SelectedComp = None
				callbackEvents.append( "SelectEnd" )

		if self.SelectedComp and not callbackEvents:
			callbackEvents.append("Move")

		self._doCallbacks( callbackEvents )
		self.CurrentEvent.SelectedComp = self.SelectedComp
		pass

	def _stopClickTimer(self):
		try:
			self.ClickTimer.kill()
		except tdError:
			pass

	def ResetClick(self):
		self.ClickCount = 0
		self._stopClickTimer()
		
	def _checkClick(self, Event:InteractionEvent):
		if Event.InteractiveComp == self.SelectedComp: return
		self.ownerComp.op("callbackManager").Do_Callback("onClick", Event, self.ClickCount, self.ownerComp)
		self.ResetClick()
		
	def PushCallback(self, callbackName:str, target:"objectCOMP" = None):
		( target or self.CurrentEvent.InteractiveComp ).op("InteractionEngine_CallbackManager").Do_Callback(
				f"on{callbackName}", self.CurrentEvent, self.PreviousEvent, self.ownerComp, target
			)

	def _doCallbacks(self, callbackList : List[str]):
		for callbackName in callbackList:
				self.ownerComp.op("callbackManager").Do_Callback(
				f"on{callbackName}", self.CurrentEvent, self.PreviousEvent, self.ownerComp
			)
		return

	def Testrun(self):
		return self.ProjectRay(0.5, 0.5).ProjectOnPlane(
			self.GetCompPlane( self.ownerComp.par.Testcomp.eval())
		)