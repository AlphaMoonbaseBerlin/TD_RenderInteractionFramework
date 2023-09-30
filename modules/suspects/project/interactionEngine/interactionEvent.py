'''Info Header Start
Name : interactionEvent
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''
from dataclasses import dataclass, field
import enum
from functools import cached_property
from typing import TYPE_CHECKING
if TYPE_CHECKING:
   from extInteractionFramework import extInteractionFramework

class Button(enum.Enum):
    Null    = 0
    Left    = 1
    Middle  = enum.auto()
    Right   = 4

@dataclass
class InteractionEvent:
    Event           : "RenderPickEvent"
    PanelValues     : Panel
    Framework       : "extInteractionFramework"
    SelectedComp    : "objectCOMP" = field( default = 0 )

    @cached_property
    def Button(self) -> Button:
        return Button( int(self.Event.inValues["aux"] ))

    @cached_property
    def WorldSpaceProjection(self) -> tdu.Position:
        return self.Framework.ProjectRay( 
            self.Event.u, self.Event.v
        ).ProjectOnPlane(
            self.Framework.GetCompPlane( self.InteractiveComp )
        )
    
    @cached_property
    def CameraProjection(self) -> tdu.Position:
        return self.Framework.ProjectRay( 
            self.Event.u, self.Event.v
        ).ProjectOnPlane(
            self.Framework.GetCompCameraPlane( self.InteractiveComp )
        )
    
    @cached_property
    def PickSop(self) -> SOP:
        return self.Event.pickOp
    
    @cached_property
    def HoverComp(self) -> "objectCOMP":
        try:
            return getattr( self.PickSop.parent, "InteractiveOP", None)
        except AttributeError:
            return None
    
    @property
    def InteractiveComp(self) -> "objectCOMP":
        return self.SelectedComp or self.HoverComp

        
    




