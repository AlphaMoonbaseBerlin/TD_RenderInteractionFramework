'''Info Header Start
Name : interactionEvent
Author : Wieland@AMB-ZEPH15
Saveorigin : RIF_Project.toe
Saveversion : 2022.35320
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


class PropertyFunctions:
    @cached_property
    def Button(self) -> Button:
        return Button( int(self.Event.inValues["aux"] or 0 ))
    
    @cached_property
    def InstanceId(self) -> Button:
        return self.Event.instanceId

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

@dataclass
class InteractionEvent:
    Event           : "RenderPickEvent" = field( repr = False)
    """The RenderpickEvent that is used to evaluate"""
    
    PanelValues     : Panel
    """The panelValue of the panel that triggered this event."""

    Framework       : "extInteractionFramework" = field( repr=False )
    """The Frameework instance. Used for internal stuff."""

    SelectedComp    : "objectCOMP" = field( default = 0 )
    """If this is an event based on selection, this value holds a GeoCOMP."""

    Timestamp       : int = field( default_factory = lambda : int(absTime.seconds * 1000) )
    """TImestamp...."""
    
    #Dynamic properties
    InstanceId              : int           = field( default = PropertyFunctions.InstanceId, init = False)
    Button                  : Button        = field( default = PropertyFunctions.Button , init=False)
    WorldSpaceProjection    : tdu.Position  = field( default = PropertyFunctions.WorldSpaceProjection , init=False)
    CameraProjection        : tdu.Position  = field( default = PropertyFunctions.CameraProjection , init=False)
    PickSop                 : SOP           = field( default = PropertyFunctions.PickSop , init=False)
    HoverComp               : "objectCOMP"  = field( default = PropertyFunctions.HoverComp , init=False)
    InteractiveComp         : "objectCOMP"  = field( default = PropertyFunctions.InteractiveComp , init=False)
    

    

        
    




