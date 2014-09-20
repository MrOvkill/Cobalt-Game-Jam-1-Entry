package com.epicknife.cobaltgamejam1;

import java.util.ArrayList;

/**
 * This class handles navigation meshes.
 */

public class NavMesh
{
    private ArrayList<Square> regions;
    
    public NavMesh()
    {
        this.regions = new ArrayList<>();
    }
    
    /**
     * s is the Square you're trying to add to the regions.
     * Returns true if square is valid.
     * Returns false if square is invalid.
     */
    
    public boolean addRegion(Square s)
    {
        if((s.x1 <= s.x2) && (s.y1 <= s.y2))
        {
            this.regions.add(s);
            return true;
        }
        else
        {
            return false;
        }
    }
    
    /**
     * a is the AI's origin.
     * b is the AI's desired destination.
     * Warning: If a is illegal, the AI will NEVER MOVE.
     *
    **/
    
    public boolean legalMove(Point2i a, Point2i b)
    {
        boolean at = false;
        boolean bt = false;
        
        for(int i = 0; i < regions.size(); i++)
        {
            Square s = regions.get(i);
            
            if(a.x <= s.x1 && a.x >= s.x2 && a.y <= s.y1 && a.y >= s.y2)
            {
                at = true;
            }
            if(b.x <= s.x1 && b.x >= s.x2 && b.y <= s.y1 && b.y >= s.y2)
            {
                bt = true;
            }
            
            if (at && bt)
            {
                return true;
            }
            else
            {
                at = false;
                bt = false;
            }
        }
        
        return false;
    }
}