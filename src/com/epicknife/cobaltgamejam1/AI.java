package com.epicknife.cobaltgamejam1;

public class AI
{
    public String name;
    public Point2i pos;
    public NavMesh navmesh;
    public boolean destroy;
    
    public AI(String name)
    {
        this.name = name;
        this.pos = new Point2i();
        this.navmesh = new NavMesh();
        this.destroy = false;
    }
    
    public void onTerrainChange()
    {
        
    }
    
    public void onEntityChange()
    {
        
    }
    
    public void onDraw(Point2i offset)
    {
        
    }
    
    public void onThink(int dt)
    {
        
    }
}