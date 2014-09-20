# map.py
# Author: Samuel "MrOverkill" Meyers
# License: Public domain

# Default tiles are 32 pixels wide and high.

import com.epicknife.cobaltgamejam1.EvilSheepGame as ESG
import com.epicknife.cobaltgamejam1.Point2i as Point
import com.epicknife.cobaltgamejam1.Tile as TileBase
import com.epicknife.cobaltgamejam1.AI as AIBase
import com.epicknife.cobaltgamejam1.NavMesh as NavMesh
import com.epicknife.cobaltgamejam1.Controllable as BaseController

class TileGrass(TileBase):
    def __init__(self, position):
        TileBase.__init__(self, True, True, position)
    def onDraw(self, offset):
        ESG.getImage("grass").draw(offset.x + self.pos.x, offset.y + self.pos.y)

class TileVoid(TileBase):
    def __init__(self, position):
        TileBase.__init__(self, False, False, position)
    def onDraw(self, offset):
        ESG.getImage("void").draw(offset.x + self.pos.x, offset.y + self.pos.y)

class AIHappySheep(AIBase):
    def __init__(self, pos):
        AIBase.__init__(self, "happysheep")
        self.pos = pos
    def onTerrainChange(self):
        self.navmesh = NavMesh()
        for i in range(0, ESG.world.size()):
            self.navmesh.addRegion(ESG.world.get(i).getCollisionSquare())
    def onDraw(self, offset):
        ESG.getImage("happysheep").draw(offset.x + (self.pos.x-8), offset.y + (self.pos.y-32))

class Player(BaseController):
    def onDraw(self):
        ESG.getImage("player").draw((400-32), (300-32))

ESG.setImage("healthbar", "resources/images/healthbar.png")
ESG.setImage("healthrect", "resources/images/healthrect.png")
ESG.setImage("grass", "resources/images/grass.png")
ESG.setImage("void", "resources/images/void.png")
ESG.setImage("happysheep", "resources/images/happysheep.png")
ESG.setImage("player", "resources/images/farmer.png")

ESG.setPlayer(Player(Point(0, 0), 1))

ESG.addEntity(AIHappySheep(Point(232, 232)))

ESG.addTile(TileGrass(Point(232, 232)))
ESG.addTile(TileGrass(Point(200, 232)))
ESG.addTile(TileGrass(Point(232, 200)))
ESG.addTile(TileGrass(Point(232, 264)))
ESG.addTile(TileGrass(Point(264, 232)))

def onGUI():
    ESG.getImage("healthbar").draw(10, 10)
    i = 19
    num = 0
    while num < ESG.player.health:
        ESG.getImage("healthrect").draw(i, 18)
        i = i + 10
        num = num + 1