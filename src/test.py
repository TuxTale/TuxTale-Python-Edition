from gmglobal import*
import json

#mapdata = jsonRead("res/map/test_for_PGE.json")

class gMap():
	def __init__(self, _map):
		self.mapdata = jsonRead(_map)
	
	def drawTiles(self):
		dataIterator = 0

		for i in self.mapdata["layers"]:
			if i["type"] == "tilelayer":
				for y in range(1, i["height"]):
					for x in range(1, i["width"]):
						tileID = tileId = i["data"][dataIterator]
						if tileID > 0:
							tileset = self.getTileset(tileID)
							frame = game.loadSprite(tileset)
							drawSprite(tileset, frame[0], self.x - game.camX, self.y - game.camY)
						dataIterator += 1
	
	def getTileset(self, tileGID):
		for i in range(0, self.mapdata["tilesets"]["firstgid"]):
			tilesetGID = self.mapdata["tilesets"][i]["firstgid"]
			tilesetTileCount = self.mapdata["tilesets"][i]["tilecount"]
			if tileGID >= tilesetGID and tileGID < tilesetTileCount + tilesetGID:
				return [pg.image.load(self.mapdata["tilesets"][i]["image"]).convert(), tilesetGID]
			
			return [None, 0]

p = gMap("res/map/test_for_PGE.json")

#p.getTileset()

#print(mapdata["layers"]["name"])

