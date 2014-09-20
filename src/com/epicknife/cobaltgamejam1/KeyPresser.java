package com.epicknife.cobaltgamejam1;

import org.lwjgl.input.Keyboard;

public class KeyPresser
{
    boolean down;
    int key;
    Runnable onDown;
    
    public KeyPresser(int key, Runnable onDown)
    {
        this.down = false;
        this.key = key;
        this.onDown = onDown;
    }
    
    public void update()
    {
        if(Keyboard.isKeyDown(key) && !down)
        {
            this.down = true;
            onDown.run();
        }
        if(!Keyboard.isKeyDown(key) && down)
        {
            this.down = false;
        }
    }
}