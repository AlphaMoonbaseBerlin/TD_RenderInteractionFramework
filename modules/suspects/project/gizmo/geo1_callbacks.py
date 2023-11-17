'''Info Header Start
Name : geo1_callbacks
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''

def calculate( Event ):
	normalized = Event.InteractiveComp.worldTransform.getInverse() *  Event.WorldSpaceProjection
	normalized.y = 0
	normalized.z = 0
	return Event.InteractiveComp.worldTransform * normalized

def Moving(Event, PrevEvent, interactionEngine, geoCOMP):
	
	
	delta = calculate( Event ) - calculate( PrevEvent )
	
	parent().par.Target.eval().parGroup.t.val += delta

	