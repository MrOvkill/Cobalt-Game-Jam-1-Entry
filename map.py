# map.py
# Author: Samuel "MrOverkill" Meyers
# License: Public domain

"""

 * Author: Samuel "MrOverkil" Meyers
 * License: Public Domain
 * Version: 0.0.1 - Release

"""

# Default tiles are 32 pixels wide and high.

import com.epicknife.cobaltgamejam1.EvilSheepGame as ESG
import com.epicknife.cobaltgamejam1.Point2i as Point
import com.epicknife.cobaltgamejam1.Tile as TileBase
import com.epicknife.cobaltgamejam1.AI as AIBase
import com.epicknife.cobaltgamejam1.NavMesh as NavMesh
import com.epicknife.cobaltgamejam1.Controllable as BaseController
import org.lwjgl.input.Keyboard as Keyboard
import java.lang.System as System
import java.lang.Math as Math

class TileGrass(TileBase):
    def __init__(self, position):
        TileBase.__init__(self, True, True, position)
    def onDraw(self, offset):
        ESG.getImage("grass").draw(offset.x + self.pos.x, offset.y + self.pos.y)

class TileGrassFence(TileBase):
    def __init__(self, position, mode):
        TileBase.__init__(self, False, False, position)
        self.mode = mode
    def onDraw(self, offset):
        ESG.getImage("grass").draw(offset.x + self.pos.x, offset.y + self.pos.y)
        if self.mode == 0:
            ESG.getImage("verticalfence").draw(offset.x + self.pos.x, offset.y + self.pos.y)
        if self.mode == 1:
            ESG.getImage("horizontalfence").draw(offset.x + self.pos.x, offset.y + self.pos.y)
        if self.mode == 2:
            ESG.getImage("verticalfence").draw(offset.x + self.pos.x, offset.y + self.pos.y)
            ESG.getImage("horizontalfence").draw(offset.x + self.pos.x, offset.y + self.pos.y)

class TileVoid(TileBase):
    def __init__(self, position):
        TileBase.__init__(self, False, False, position)
    def onDraw(self, offset):
        ESG.getImage("void").draw(offset.x + self.pos.x, offset.y + self.pos.y)

class EntityCorpse(AIBase):
    def __init__(self, pos):
        AIBase.__init__(self, "corpse")
        self.pos = pos
    def onDraw(self, offset):
        ESG.getImage("corpse").draw(offset.x + (self.pos.x-8), offset.y + (self.pos.y-8))

class EntityShit(AIBase):
    def __init__(self, pos):
        AIBase.__init__(self, "shit")
        self.pos = pos
    def onThink(self, ignoreme):
        ppos = Point(-ESG.player.pos.x, -ESG.player.pos.y)
        if ppos.inRange(16, self.pos):
            ESG.player.shit = ESG.player.shit + 1
            self.destroy = True
    def onDraw(self, offset):
        ESG.getImage("shit").draw(offset.x + (self.pos.x-8), offset.y + (self.pos.y-8))

class AIHappySheep(AIBase):
    def __init__(self, pos):
        AIBase.__init__(self, "happysheep")
        self.pos = pos
        self.dest = pos
        self.direction = Point(0, 0)
        self.lt = System.currentTimeMillis()
        self.ct = System.currentTimeMillis()
        self.speed = 1
        self.positions = []
        self.directions = []
    def onTerrainChange(self):
        self.navmesh = ESG.navmesh
    def onThink(self, ignoreme):
        self.ct = System.currentTimeMillis()
        
        if self.pos.pointEquals(self.dest):
            
            marg = ESG.randInt(0, 43)
            if marg == 42:
                ESG.entities.add(EntityShit(self.pos))
            
            self.positions = []
            self.directions = []
            
            for i in range(0, 4):
                if i == 0:
                    despos = Point(self.pos.x+32, self.pos.y)
                    if ESG.navmesh.legalMove(self.pos, despos):
                        self.positions.append(despos)
                        self.directions.append(Point(1, 0))
                if i == 1:
                    despos = Point(self.pos.x-32, self.pos.y)
                    if ESG.navmesh.legalMove(self.pos, despos):
                        self.positions.append(despos)
                        self.directions.append(Point(-1, 0))
                if i == 2:
                    despos = Point(self.pos.x, self.pos.y+32)
                    if ESG.navmesh.legalMove(self.pos, despos):
                        self.positions.append(despos)
                        self.directions.append(Point(0, 1))
                if i == 3:
                    despos = Point(self.pos.x, self.pos.y-32)
                    if ESG.navmesh.legalMove(self.pos, despos):
                        self.positions.append(despos)
                        self.directions.append(Point(0, -1))
            
            if len(self.directions) >= 1:
                chosen = ESG.randInt(0, (len(self.directions)-1))
                self.dest = self.positions[chosen]
                self.direction = self.directions[chosen]
            else:
                self.dest = self.pos
        
        if self.ct - self.lt >= 25:
            newpos = Point(self.pos.x + (self.direction.x * self.speed), self.pos.y + (self.direction.y * self.speed))
            self.lt = self.ct
            if ESG.navmesh.legalMove(self.pos, newpos):
                self.pos = newpos
        
    def onDraw(self, offset):
        ESG.getImage("happysheep").draw(offset.x + (self.pos.x-8), offset.y + (self.pos.y-32))

class AIEvilSheep(AIBase):
    def __init__(self, pos, poses):
        AIBase.__init__(self, "evilsheep")
        self.pos = pos
        self.dest = pos
        self.direction = Point(0, 0)
        self.lt = System.currentTimeMillis()
        self.ct = System.currentTimeMillis()
        self.speed = 1
        self.positions = poses
        self.cdest = 0
        self.lastHit = System.currentTimeMillis()
    def onTerrainChange(self):
        self.navmesh = ESG.navmesh
    
    def onThink(self, ignoreme):
        self.ct = System.currentTimeMillis()
        
        for i in range(0, ESG.entities.size()):
            ent = ESG.entities.get(i)
            if ent.name == "happysheep":
                if (System.currentTimeMillis() - self.lastHit) >= 1000:
                    if ent.pos.inRange(2, self.pos):
                        self.lastHit = System.currentTimeMillis()
                        ESG.entities.get(i).destroy = True
                        ESG.entities.add(AIEvilSheep(ent.pos, [Point(0, 0)]))
        
        ppos = Point(-ESG.player.pos.x, -ESG.player.pos.y)
        
        if ppos.inRange(32, Point(self.pos.x+16, self.pos.y+16)):
            if (System.currentTimeMillis() - self.lastHit) >= 1000:
                self.lastHit = System.currentTimeMillis()
                ESG.player.onDamage(1)
        
        if self.pos.pointEquals(self.dest):
            
            if len(self.positions)-1 >= self.cdest:
                self.dest = self.positions[self.cdest]
                self.direction = Point(0, 0)
                if self.dest.x > self.pos.x:
                    self.direction = Point(1, self.direction.y)
                elif self.dest.x < self.pos.x:
                    self.direction = Point(-1, self.direction.y)
                else:
                    self.direction = Point(0, self.direction.y)
                if self.dest.y > self.pos.y:
                    self.direction = Point(self.direction.x, 1)
                elif self.dest.y < self.pos.y:
                    self.direction = Point(self.direction.x, -1)
                else:
                    self.direction = Point(self.direction.x, 0)
                self.cdest = self.cdest + 1
            else:
                self.positions = []
                self.directions = []
                
                self.cdest = 0
                
                for i in range(0, 4):
                    if i == 0:
                        despos = Point(self.pos.x+32, self.pos.y)
                        if ESG.navmesh.legalMove(self.pos, despos):
                            self.positions.append(despos)
                            self.directions.append(Point(1, 0))
                    if i == 1:
                        despos = Point(self.pos.x-32, self.pos.y)
                        if ESG.navmesh.legalMove(self.pos, despos):
                            self.positions.append(despos)
                            self.directions.append(Point(-1, 0))
                    if i == 2:
                        despos = Point(self.pos.x, self.pos.y+32)
                        if ESG.navmesh.legalMove(self.pos, despos):
                            self.positions.append(despos)
                            self.directions.append(Point(0, 1))
                    if i == 3:
                        despos = Point(self.pos.x, self.pos.y-32)
                        if ESG.navmesh.legalMove(self.pos, despos):
                            self.positions.append(despos)
                            self.directions.append(Point(0, -1))
                
                if len(self.directions) >= 1:
                    chosen = ESG.randInt(0, (len(self.directions)-1))
                    self.dest = self.positions[chosen]
                    self.direction = self.directions[chosen]
                else:
                    self.dest = self.pos
        
        if self.ct - self.lt >= 25:
            self.direction = Point(0, 0)
            if self.dest.x > self.pos.x:
                self.direction = Point(1, self.direction.y)
            elif self.dest.x < self.pos.x:
                self.direction = Point(-1, self.direction.y)
            else:
                self.direction = Point(0, self.direction.y)
            if self.dest.y > self.pos.y:
                self.direction = Point(self.direction.x, 1)
            elif self.dest.y < self.pos.y:
                self.direction = Point(self.direction.x, -1)
            else:
                self.direction = Point(self.direction.x, 0)
            newpos = Point(self.pos.x + (self.direction.x * self.speed), self.pos.y + (self.direction.y * self.speed))
            self.lt = self.ct
            if ESG.navmesh.legalMove(self.pos, newpos):
                self.pos = newpos
        
    def onDraw(self, offset):
        ESG.getImage("evilsheep").draw(offset.x + (self.pos.x-8), offset.y + (self.pos.y-32))

class AIThrownShit(AIBase):
    def __init__(self, pos, speed, direction):
        AIBase.__init__(self, "thrownshit")
        self.pos = pos
        self.speed = speed
        self.direction = direction
        self.a = System.currentTimeMillis()
        self.b = System.currentTimeMillis()
    def onTerrainChange(self):
        self.navmesh = ESG.navmesh
    def onThink(self, ignoreme):
        for i in range(0, ESG.entities.size()):
            ent = ESG.entities.get(i)
            if ent.name == "happysheep":
                if ent.pos.inRange(42, self.pos):
                    ESG.entities.get(i).destroy = True
                    ESG.entities.add(AIEvilSheep(ent.pos, []))
                    self.destroy = True
            if ent.name == "evilsheep":
                if ent.pos.inRange(42, self.pos):
                    ESG.entities.get(i).destroy = True
                    ESG.entities.add(EntityCorpse(ent.pos))
                    self.destroy = True
        
        oldpos = Point(self.pos.x, self.pos.y)
        self.pos = Point.add(self.pos, self.direction)
        if not ESG.navmesh.legalMove(oldpos, self.pos):
            self.destroy = True
    def onDraw(self, offset):
        ESG.getImage("shit").draw(offset.x + (self.pos.x-8), offset.y + (self.pos.y-8))

class Player(BaseController):
    # I WAS MAKING IT RESET THE TIMER AT THE DRAW FUNCTION INSTEAD OF THE CONSTRUCTOR!!!
    # Edge X: -112
    # Edge Y: -212
    def __init__(self, pos, speed):
        BaseController.__init__(self, pos, speed)
        self.a = True
        self.b = True
        self.c = True
        self.d = True
        self.shit = 0
    def onDraw(self):
        ESG.getImage("player").draw((400-32), (300-32))
    def onUpdate(self):
        BaseController.onUpdate(self)
        if self.health <= 0:
            Systenm.exit(0)
        if Keyboard.isKeyDown(Keyboard.KEY_UP) and self.a and self.shit > 0:
            ESG.addEntity(AIThrownShit(Point(-(self.pos.x+4), -(self.pos.y+40)), 1, Point(0, -1)))
            self.a = False
            self.shit = self.shit - 1
        if not Keyboard.isKeyDown(Keyboard.KEY_UP) and not self.a:
            self.a = True
        if Keyboard.isKeyDown(Keyboard.KEY_DOWN) and self.b and self.shit > 0:
            ESG.addEntity(AIThrownShit(Point(-(self.pos.x+4), -(self.pos.y-40)), 1, Point(0, 1)))
            self.b = False
            self.shit = self.shit - 1
        if not Keyboard.isKeyDown(Keyboard.KEY_DOWN) and not self.b:
            self.b = True
        if Keyboard.isKeyDown(Keyboard.KEY_RIGHT) and self.c and self.shit > 0:
            ESG.addEntity(AIThrownShit(Point(-(self.pos.x-20), -(self.pos.y)), 1, Point(1, 0)))
            self.c = False
            self.shit = self.shit - 1
        if not Keyboard.isKeyDown(Keyboard.KEY_RIGHT) and not self.c:
            self.c = True
        if Keyboard.isKeyDown(Keyboard.KEY_LEFT) and self.d and self.shit > 0:
            ESG.addEntity(AIThrownShit(Point(-(self.pos.x+25), -(self.pos.y)), 1, Point(-1, 0)))
            self.d = False
            self.shit = self.shit - 1
        if not Keyboard.isKeyDown(Keyboard.KEY_LEFT) and not self.d:
            self.d = True

ESG.setImage("healthbar", "resources/images/healthbar.png")
ESG.setImage("healthrect", "resources/images/healthrect.png")
ESG.setImage("grass", "resources/images/grass.png")
ESG.setImage("void", "resources/images/void.png")
ESG.setImage("happysheep", "resources/images/happysheep.png")
ESG.setImage("player", "resources/images/farmer.png")
ESG.setImage("shit", "resources/images/shit.png")
ESG.setImage("bigshit", "resources/images/bigshit.png")
ESG.setImage("evilsheep", "resources/images/angrysheep.png")
ESG.setImage("corpse", "resources/images/corpse.png")
ESG.setImage("verticalfence", "resources/images/verticalfence.png")
ESG.setImage("horizontalfence", "resources/images/horizontalfence.png")

ESG.setPlayer(Player(Point(-64, -64), 1))

ESG.addEntity(AIHappySheep(Point(-128, -128)))
ESG.addEntity(AIHappySheep(Point(-256, -128)))
ESG.addEntity(AIHappySheep(Point(-128, -256)))
ESG.addEntity(AIHappySheep(Point(-256, -256)))

ESG.addEntity(AIEvilSheep(Point(-95, 282), [
Point(267, 229),
Point(138, -34),
Point(396, -418),
Point(-147, -405),
Point(-237, -179),
]))

ESG.addEntity(AIEvilSheep(Point(-200, 282), [
Point(267, 229),
Point(138, -34),
Point(396, -418),
Point(-147, -405),
Point(-237, -179),
]))

ESG.addEntity(AIEvilSheep(Point(-55, 282), [
Point(267, 229),
Point(138, -34),
Point(396, -418),
Point(-147, -405),
Point(-237, -179),
]))

ESG.addEntity(AIEvilSheep(Point(100, 382), [
Point(267, 229),
Point(138, -34),
Point(396, -418),
Point(-147, -405),
Point(-237, -179),
]))

ESG.addEntity(AIEvilSheep(Point(10, 382), [
Point(367, 229),
Point(238, -80),
Point(396, -418),
Point(-147, -405),
Point(-237, -179),
]))

"""
ESG.addEntity(AIEvilSheep(Point(232, 264), [
Point(200, 264),

Point(200, 232),

Point(200, 200),

Point(168, 200),

Point(168, 168),

Point(168, 136),

Point(168, 104),

Point(168, 72),

Point(168, 40),

Point(168, 8),

Point(168, -24),

Point(168, -56),

Point(168, -88),

Point(168, -120),

Point(168, -152),

Point(168, -184),

Point(168, -216),

Point(168, -248),

Point(168, -280),

Point(168, -312),

Point(168, -344),

Point(168, -376),

Point(168, -408),

Point(136, -408),

Point(104, -408),

Point(0, -408),

Point(0, -376),

Point(-200, -300),
]))

"""

cx = (-16)*32
cy = (-16)*32

for x in range(-16, 16):
    for y in range(-16, 16):
        ESG.addTile(TileGrass(Point(cx, cy)))
        cy = cy + 32
    cy = -16*32
    cx = cx + 32

cx = (-14)*32
cy = (-14)*32

for x in range(0, 15):
    ESG.removeTile(TileGrass(Point(cx, cy)))
    ESG.addTile(TileGrassFence(Point(cx, cy), 2))
    cx = cx + 32

cx = (-14)*32

for y in range(0, 15):
    ESG.removeTile(TileGrass(Point(cx, cy)))
    ESG.addTile(TileGrassFence(Point(cx, cy), 2))
    cy = cy + 32

for x in range(0, 15):
    ESG.removeTile(TileGrass(Point(cx, cy)))
    ESG.addTile(TileGrassFence(Point(cx, cy), 2))
    cx = cx + 32

for y in range(0, 16):
    ESG.removeTile(TileGrass(Point(cx, cy)))
    ESG.addTile(TileGrassFence(Point(cx, cy), 2))
    cy = cy - 32

ESG.removeTile(TileGrass(Point(cx, cy + 64)))
ESG.addTile(TileGrass(Point(cx, cy + 64)))

def onGUI(graphics):
    ESG.getImage("healthbar").draw(10, 10)
    i = 19
    num = 0
    while num < ESG.player.health:
        ESG.getImage("healthrect").draw(i, 18)
        i = i + 10
        num = num + 1
    ESG.getImage("bigshit").draw(10, 65)
    graphics.drawString("x " + str(ESG.player.shit), 52, 70)
    graphics.drawString("Player: x" + str(-ESG.player.pos.x) + " y" + str(-ESG.player.pos.y), 10, 100)
    arg = 130
    for i in range(0, ESG.entities.size()):
        ent = ESG.entities.get(i)
        if ent.name == "evilsheep":
            graphics.drawString("evilsheep: x" + str(ESG.entities.get(i).pos.x) + " y" + str(ESG.entities.get(i).pos.y), 10, arg)
            arg = arg + 30