'''Info Header Start
Name : geo1_callbacks
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''

def onMoving(Event, PrevEvent, interactionEngine, geoCOMP):
	
	
	delta =  Event.InteractiveComp.localTransform.getInverse() * (  Event.WorldSpaceProjection - PrevEvent.WorldSpaceProjection )
	delta.y = 0
	delta.z = 0

	parent.Gizmo.parGroup.t.val += Event.InteractiveComp.localTransform * delta
	