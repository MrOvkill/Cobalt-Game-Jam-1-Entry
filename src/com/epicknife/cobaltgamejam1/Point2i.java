package com.epicknife.cobaltgamejam1;

public class Point2i
{
    public int x, y;
    
    public Point2i()
    {
        this.x = 0;
        this.y = 0;
    }

    public Point2i(int x, int y)
    {
        this.x = x;
        this.y = y;
    }
    
    public boolean pointEquals(Point2i p)
    {
        return ((this.x == p.x) && (this.y == p.y));
    }
    
    public boolean pointInRange(int range, Point2i p)
    {
        boolean a = (this.x+range >= p.x);
        boolean b = (this.x-range <= p.x);
        boolean c = (this.y+range >= p.y);
        boolean d = (this.x-range <= p.y);
        
        return ((a || b) && (c || d));
    }
    
    public static Point2i add(Point2i a, Point2i b)
    {
        return new Point2i(a.x + b.x, a.y + b.y);
    }
    
    public static Point2i muli(Point2i a, int b)
    {
        return new Point2i(a.x * b, a.y * b);
    }
    
    public static int distance(Point2i a, Point2i b)
    {
        int ad = Math.abs(a.x) - Math.abs(b.x);
        int bd = Math.abs(a.y) - Math.abs(b.y);
        return ad+bd;
    }
    
    public boolean inRange(int range, Point2i dest)
    {
        return (Point2i.distance(this, dest) <= range);
    }
}