# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 09:08:52 2018

@author: Deon
"""

from math import pi, cos, sin, tan, sqrt
import numpy as np
import pylab

##############################################################################
    #SHAFT ONE / THREE
##############################################################################
def inoutshaft(tanforce, radforce, rpm, bear, shoulder): 
    T = 15000 / ((rpm * 2*pi)/60)
    
    load = sqrt(tanforce**2 + radforce**2)
    
    breac = load / 2
    areac = load - breac 
    
    print("Torque = ", T)
    print(f"Load = {load}, A = {areac}, B = {breac}")
    
    ##now for bending 
    face = 0.07
    ab = (bear / 2) + shoulder + (face/2)
    
    xvalues = np.linspace(0, 2*ab, 500)
    shearvalues = []
    bendvalues = []
    
    for x in xvalues: 
        if x < ab: 
            shear = areac 
            bend = areac * x 
                        
        elif x < 2*ab: 
            shear = areac - load
            bend = areac*x - load*(x - ab)
        else: 
            shear = areac + breac - load
            bend = areac*x + breac*(x - 2*ab) - load*(x - ab)
            
        shearvalues.append(shear)
        bendvalues.append(bend)
         
    critpoints = [(bear/2), ((bear/2)+shoulder), ((bear/2)+shoulder+(face/2)), 
                  ((bear/2)+shoulder+face), ((bear/2)+(2*shoulder)+face)]
    critbends = []
    
    for x in critpoints: 
        if x < ab: 
            shear = areac 
            bend = areac * x 
                        
        elif x < 2*ab: 
            shear = areac - load
            bend = areac*x - load*(x - ab)
        else: 
            shear = areac + breac - load
            bend = areac*x + breac*(x - 2*ab) - load*(x - ab)
            
        critbends.append(bend)
    
    print()
    print(f"Length: {2*ab}")
    print("Bending Moments at crit points:")
    for i in range(len(critbends)): 
    #for i in range(len(critbends)): 
        print(critbends[i])
    print()
    
    return areac, T, xvalues, bendvalues, critbends


    
##############################################################################
    #INTERMEDIATE SHAFT
##############################################################################
def intershaft(tan2, rad2, tan3, rad3, idlerdeg, rpm, bear, middle): 
    face = 0.07
    a = (bear/2) + (face/2)
    b = (bear/2) + (face*3/2) + middle
    c = bear + (face*2) + middle
    
    T = 15000 / ((rpm * 2*pi)/60)
    angle = (idlerdeg*pi)/180
    
    ct = tan2
    cr = rad2 
    
    dt = tan3*cos(angle) - rad3*sin(angle)
    dr = -tan3*sin(angle) - rad3*cos(angle)
    
    bt = -(dt*a + ct*b)/c
    br = -(dr*a + cr*b)/c
    
    at = -ct - dt - bt
    ar = -dr - cr - br 
    
    print("Reaction Forces at Intermediate Shaft")
    print(f"Torque = {T}")
    print(f"G3Endt = {at}, \t G3Endr = {ar}")
    print(f"G2Endt = {bt}, \t G2Endr = {br}")
    print(f"Gear2t = {ct}, \t Gear2r = {cr}")
    print(f"Gear3t = {dt}, \t Gear3r = {dr}")
    
    areaction = sqrt(at**2 + ar**2)
    breaction = sqrt(bt**2 + br**2)
    
    xvalues = np.linspace(0, c, 500)
    xzshearvalues = []
    xzbendvalues = []
    
    xyshearvalues = []
    xybendvalues = []
    
    shearvalues = []
    bendvalues = []

    for x in xvalues: 
        if x < a: 
            xzshear = ar 
            xzbend = ar * x 
            
            xyshear = at 
            xybend = at * x             
        elif x < b: 
            xzshear = ar + dr 
            xzbend = ar*x + dr*(x - a)
            
            xyshear = at + dt 
            xybend = at*x + dt*(x - a)
        else: 
            xzshear = ar + dr + cr
            xzbend = ar*x + dr*(x - a) + cr*(x - b)
            
            xyshear = at + dt + ct
            xybend = at*x + dt*(x - a) + ct*(x - b)

        xzshearvalues.append(xzshear)
        xzbendvalues.append(xzbend)
        
        xyshearvalues.append(xyshear)
        xybendvalues.append(xybend)
            
        shear = sqrt(xzshear**2 + xyshear**2)
        bend = sqrt(xzbend**2 + xybend**2)
        
        shearvalues.append(shear)
        bendvalues.append(bend)
    
    critpoints = [(bear/2), ((bear/2)+(face/2)), ((bear/2)+face), 
                  ((bear/2)+face+middle), ((bear/2)+face+middle+(face/2)), 
                  ((bear/2)+(2*face)+middle)]
    xzcritbends = []
    xycritbends = []
    critbends = []
    
    for x in critpoints: 
        if x < a: 
            xzshear = ar 
            xzbend = ar * x 
            
            xyshear = at 
            xybend = at * x             
        elif x < b: 
            xzshear = ar + dr 
            xzbend = ar*x + dr*(x - a)
            
            xyshear = at + dt 
            xybend = at*x + dt*(x - a)
        else: 
            xzshear = ar + dr + cr
            xzbend = ar*x + dr*(x - a) + cr*(x - b)
            
            xyshear = at + dt + ct
            xybend = at*x + dt*(x - a) + ct*(x - b)
            
        shear = sqrt(xzshear**2 + xyshear**2)
        bend = sqrt(xzbend**2 + xybend**2)
    
        xzcritbends.append(xzbend)
        xycritbends.append(xybend)
        critbends.append(bend)
    
    print()
    print("Bending Moments at crit points:")
    print("Bend Y \t\t\t Bend Z \t\t Total Magnitude")
    for i in range(len(critbends)): 
        print(xzcritbends[i], "\t", xycritbends[i], "\t", critbends[i])
    print()
    
    return areaction, breaction, T, xvalues, xybendvalues, xzbendvalues, critbends
    
##############################################################################
def shaftbendingmoment(gear1tan, gear1rad, gear4tan, gear4rad, inputspeed, 
                         interspeed, outputspeed, idleangle, geometry): 
    
#    inputshoulder = 0.03
#    bearingin = 0.015
#    interbearing = 0.022
#    intermiddle = 0.05
#    outputshoulder = 0.03
#    bearingout = 0.022
    
    inshoulder, inbearing, midbearing, midmiddle, outshoulder, outbearing = geometry
    
    tanforce1 = gear1tan #1145.9
    radforce1 = gear1rad #417.1
    tanforce4 = gear4tan #6935.8
    radforce4 = gear4rad #2524.4
    
    inspeed = inputspeed #2500
    midspeed = interspeed #434.78
    outspeed = outputspeed #120
    
    
    idlerangle = (idleangle*180) / pi #44.9
    
    
    
    print("INPUT SHAFT")
    reac1, intorque, inx, inbend, critbend1 = inoutshaft(tanforce1, radforce1, inspeed, inbearing, 
                             inshoulder)
    
    print("INTERMEDIATE SHAFT")
    reac23, reac22, midtorque, midx, xybend, xzbend, critbend2 = intershaft(tanforce1, radforce1, 
                                                           tanforce4, 
                                      radforce4, idlerangle, midspeed, 
                                      midbearing, midmiddle)
    
    print("OUTPUT SHAFT")
    reac3, outtorque, outx, outbend, critbend3 = inoutshaft(tanforce4, radforce4, outspeed, outbearing, 
                               outshoulder)
    
    
    #shaft1, shaft2gear3, shaft2gear2, shaft3
    reactions = [reac1, reac23, reac22, reac3]
    
    pylab.figure()
    
    pylab.subplot(221, title = "INPUT")
    pylab.plot(inx, inbend)
    pylab.xlabel("distance")
    pylab.ylabel("bend force")
    
    pylab.subplot(222, title = "OUTPUT")
    pylab.plot(outx, outbend)
    pylab.xlabel("distance")
    pylab.ylabel("bend force")
    
    pylab.subplot(223, title = "XY PLANE")
    pylab.plot(midx, xybend)
    pylab.xlabel("distance")
    pylab.ylabel("bend force")
    
    pylab.subplot(224, title = "XZ PLANE")
    pylab.plot(midx, xzbend)
    pylab.xlabel("distance")
    pylab.ylabel("bend force")
    
    return reactions, intorque, critbend1, midtorque, critbend2, outtorque, critbend3

    
#shaftbendingmoment()