package com.epicknife.cobaltgamejam1;

import org.lwjgl.input.Keyboard;

/*
    * Author: Samuel "MrOverkill" Meyers
    * License: Public Domain
    * Version: 0.0.1
*/

public class Controllable
{
    public Point2i pos;
    public int speed;
    // To allow really small and fine-tined amounts of damage.
    public float health;
    long ds, dn;
    boolean a;
    
    public Controllable(Point2i pos, int speed)
    {
        this.pos = pos;
        this.speed = speed;
        this.health = 20;
        ds = System.currentTimeMillis();
        a = false;
    }
    
    public void onDamage(float amt)
    {
        this.health -= amt;
    }
    
    public void onUpdate()
    {
        dn = System.currentTimeMillis();
        
        if(dn-ds >= 10)
        {
            // Default to WASD controls.
            if(Keyboard.isKeyDown(Keyboard.KEY_W))
            {
                if(EvilSheepGame.navmesh.legalMove(new Point2i(-pos.x, -pos.y), new Point2i(-pos.x, -(pos.y + speed))))
                {
                    this.pos.y += speed;
                }
            }
            if(Keyboard.isKeyDown(Keyboard.KEY_A))
            {
                if(EvilSheepGame.navmesh.legalMove(new Point2i(-pos.x, -pos.y), new Point2i(-(pos.x + speed),- pos.y)))
                {
                    this.pos.x += speed;
                }
            }
            if(Keyboard.isKeyDown(Keyboard.KEY_S))
            {
                if(EvilSheepGame.navmesh.legalMove(new Point2i(-pos.x, -pos.y), new Point2i(-pos.x, -(pos.y - speed))))
                {
                    this.pos.y -= speed;
                }
            }
            if(Keyboard.isKeyDown(Keyboard.KEY_D))
            {
                if(EvilSheepGame.navmesh.legalMove(new Point2i(-pos.x, -pos.y), new Point2i(-(pos.x - speed), -pos.y)))
                {
                    this.pos.x -= speed;
                }
            }
            
            ds = dn;
        }
    }
    
    public void onDraw()
    {
        
    }
}