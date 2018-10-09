# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 19:12:20 2018

@author: Deon
"""
from math import pi, sin, cos, acos
import pylab

def plotsdistance(r3, r4, ri): 
    distance = 280.644961
    alpha, beta, gamma = trianglesolver(distance, r3, r4, ri)
    
    print("Angles:", (alpha*180)/pi, (beta*180)/pi, (gamma*180)/pi)
    
    #check error
    calculate = check(r3, r4, ri, alpha, beta)
    print("Error = ", abs(distance - calculate))
    
    #plot gears
    pylab.axes() 
    
    gear3 = pylab.Circle((0, 0), radius = r3, fill=False)
    pylab.gca().add_patch(gear3) 
    
    gear4 = pylab.Circle((0, distance), radius = r4, fill=False)
    pylab.gca().add_patch(gear4) 
    
    idlegear = pylab.Circle((-(r3+ri)*sin(alpha), (r3+ri)*cos(alpha)), 
                            radius = ri, fill=False)
    pylab.gca().add_patch(idlegear)
    
    pylab.axis('scaled')
    pylab.show()
    
def trianglesolver(distance, r3, r4, ri): 
    r3ri = r3 + ri
    r4ri = r4 + ri
    
    try: 
        #bottom angle
        alpha = acos((r3ri**2 + distance**2 - r4ri**2)/(2*r3ri*distance))
    
        #top angle 
        beta = acos((r4ri**2 + distance**2 - r3ri**2)/(2*r4ri*distance))
    
        #side angle 
        gamma = acos((r3ri**2 + r4ri**2 - distance**2)/(2*r3ri*r4ri))
    
        #return (alpha, beta, gamma)
    except ValueError: 
        alpha = 0
        beta = 0
        gamma = 0
    
    return (alpha, beta, gamma)

def check(r3, r4, ri, alpha, beta): 
    return (r3 + ri)*cos(alpha) + (r4 + ri)*cos(beta)

#plotsdistance(47.5, 172.5, 50)



