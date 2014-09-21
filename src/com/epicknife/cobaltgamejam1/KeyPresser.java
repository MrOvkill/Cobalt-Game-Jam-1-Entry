package com.epicknife.cobaltgamejam1;

import org.lwjgl.input.Keyboard;

/*
    * Author: Samuel "MrOverkill" Meyers
    * License: Public Domain
    * Version: 0.0.1
    * Last Modified: 0.0.1 - Samuel "MrOverkill" Meyers
*/

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