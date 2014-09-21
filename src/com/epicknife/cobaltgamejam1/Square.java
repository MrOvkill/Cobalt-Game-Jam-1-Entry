package com.epicknife.cobaltgamejam1;

/*
    * Author: Samuel "MrOverkill" Meyers
    * License: Public Domain
    * Version: 0.0.1
    * Last Modified: 0.0.1 - Samuel "MrOverkill" Meyers
*/

public class Square
{
    public float x1, x2;
    public float y1, y2;
    
    public Square(float x1, float y1, float x2, float y2)
    {
        this.x1 = x1;
        this.y1 = y1;
        this.x2 = x2;
        this.y2 = y2;
    }
    
    public boolean squareEquals(Square s)
    {
        return (this.x1 == s.x1 && this.y1 == s.y1 && this.x2 == s.x2 && this.y2 == s.y2);
    }
    
    @Override
    public String toString()
    {
        return this.x1 + ":" + this.x2 + "," + this.y1 + ":" + this.y2;
    }
}