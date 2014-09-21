package com.epicknife.cobaltgamejam1;

import org.lwjgl.input.Keyboard;

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
                this.pos.y += speed;
            }
            if(Keyboard.isKeyDown(Keyboard.KEY_A))
            {
                this.pos.x += speed;
            }
            if(Keyboard.isKeyDown(Keyboard.KEY_S))
            {
                this.pos.y -= speed;
            }
            if(Keyboard.isKeyDown(Keyboard.KEY_D))
            {
                this.pos.x -= speed;
            }
            
            ds = dn;
        }
    }
    
    public void onDraw()
    {
        
    }
}