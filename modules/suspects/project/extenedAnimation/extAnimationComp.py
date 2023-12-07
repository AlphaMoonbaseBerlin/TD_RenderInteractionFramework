'''Info Header Start
Name : extAnimationComp
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''
from typing import List
import uuid

KeyframeId = str

class extAnimationComp:
	"""
	extAnimationComp description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	@property
	def Channels(self) -> tableDAT:
		return self.ownerComp.par.channels.eval()
	
	@property
	def Keycollection(self) -> COMP:
		return self.ownerComp.op("keyCollection")
	
	def Clear(self):
		self.Channels.clear(keepFirstRow = True)
		self.Keys.clear( keepFirstRow = True)
	@property
	def Keys(self) -> tableDAT:
		return self.ownerComp.op("keys")

	def ChannelRow(self, channelName:str) -> List[Cell]:
		return self.Channels.row( channelName )

	def AddChannel(self, channelName:str, defaultValue = 0):
		self.Channels.row( channelName ) or self.Channels.appendRow(
			[ channelName, self.Channels.numRows, "hold", "hold", 0, f"keys", 1,1,1, 0, 1, 0]
		) and self.AddKeyframe( channelName, 0, defaultValue )
		
	def DeleteChannel(self, channelName:str):
		channelId = self.ChannelRow( channelName )[1].val
		channelKeyRows = [
			row[0].row for row in self.Keys.rows()[1:] if row[1].val == channelId
		]
		self.Keys.deleteRows( channelKeyRows )
		self.Channels.deleteRow( channelName )

	def AddKeyframe(self, targetChannel:str, position:int, value:float) -> KeyframeId:
		keyframeId = str( uuid.uuid4() )
		channelId = self.ChannelRow( targetChannel )[1].val
		self.Keys.appendRow(
			[ keyframeId, channelId, position, value, 0,0,"linear()",0,0 ]
		)	
		return keyframeId
	
	def RemoveKeyframe(self, keyframeId:str):
		self.Keys.deleteRow( keyframeId )
	
	def UpdateKeyframePosition(self, keyframeId:str, value:int):
		self.Keys[keyframeId, "x"].val = value

	def UpdateKeyframeValue(self, keyframeId:str, value:float):
		self.Keys[keyframeId, "y"].val = value