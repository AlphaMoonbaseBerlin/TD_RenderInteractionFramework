'''Info Header Start
Name : geo1_callbacks
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''

def onMoving(Event, PrevEvent, interactionEngine, geoCOMP):
	revertedPosition =  Event.InteractiveComp.localTransform.getInverse() * Event.WorldSpaceProjection
	revertedPosition.y = 0
	revertedPosition.z = 0

	parent.Gizmo.parGroup.t.val = Event.InteractiveComp.localTransform * revertedPosition
	