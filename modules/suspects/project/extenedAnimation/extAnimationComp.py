'''Info Header Start
Name : extAnimationComp
Author : Wieland@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2022.32660
Info Header End'''
from typing import List

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
		for child in self.Keycollection.findChildren( depth = 1):
			child.destroy()

	def Keys(self, channelName:str) -> tableDAT:
		return self.Keycollection.op(channelName) or self.Keycollection.copy( self.ownerComp.op("emptyKeys"), name = channelName )

	def ChannelRow(self, channelName:str) -> List[Cell]:
		return self.Channels.row( channelName )

	def AddChannel(self, channelName:str, defaultValue = 0):
		self.Channels.row( channelName ) or self.Channels.appendRow(
			[ channelName, self.Channels.numRows, "hold", "hold", 0, f"{self.Keycollection.name}/{channelName}", 1,1,1, 0, 1, 0]
		)
		self.AddKeyframe( channelName, 0, defaultValue )
		
		

	def DeleteChannel(self, channelName:str):
		self.Channels.deleteRow( channelName )
		self.Keycollection.op( channelName ).destroy()

	def AddKeyframe(self, targetChannel:str, position:int, value:float):
		id = self.ChannelRow( targetChannel )[1].val
		self.Keys( targetChannel ).appendRow(
			[ id, position, value, 0,0,"linear()",0,0 ]
		)	