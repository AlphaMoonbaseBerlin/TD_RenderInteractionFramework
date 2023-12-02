'''Info Header Start
Name : geo1_callbacks
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''


def Moving(Event, PrevEvent, interactionEngine, geoCOMP):
	normalized = Event.InteractiveComp.worldTransform.getInverse() * Event.WorldSpaceProjection
	worldToLocal = parent().par.Target.eval().worldTransform * normalized
		
	parent().par.Target.eval().parGroup.t.val = worldToLocal

	