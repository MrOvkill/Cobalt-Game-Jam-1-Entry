package com.epicknife.cobaltgamejam1;

public class Tile
{
    boolean walkable;
    boolean spawnable;
    public Point2i pos;
    
    public Tile(boolean walkable, boolean spawnable, Point2i pos)
    {
        this.walkable = walkable;
        this.spawnable = (spawnable && walkable);
        this.pos = pos;
    }
    
    public Square getCollisionSquare()
    {
        return new Square(this.pos.x, this.pos.y, this.pos.x + 32, this.pos.y + 32);
    }
    
    public void onDraw(Point2i offset)
    {
        
    }
}