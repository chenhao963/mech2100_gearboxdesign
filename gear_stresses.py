# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 20:42:25 2018

@author: Deon
"""
from math import sqrt, pi, sin, cos, tan
import numpy as np
from scipy import interpolate

def gearstresses(mod, face, n1, n2, rpm1, rpm2, power, isidler=False): 
    d1 = n1 * mod
    d2 = n2 * mod
    
    #tangential and radial forces
    ft = tanforce(power, rpm1, d1)
    fr = radforce(ft)
    

    print(f"Tangent / Radial Forces: {ft} \t {fr}")
    
    #bend and contact
    bend1 = bending(face, d1, d1, rpm1, n1, n2, mod, ft, 1)
    bend2 = bending(face, d2, d1, rpm2, n1, n2, mod, ft, 2)
    
    
    cont1 = contact(face, d1, d1, rpm1, n1, n2, ft)
    cont2 = contact(face, d2, d1, rpm2, n1, n2, ft)
    
    
    print(f"Bending: \t\t {bend1} \t {bend2}") 
    
    print(f"Contact: \t\t {cont1} \t {cont2}")
    
    #safety factors
    reliability = 0.99 
    life = 30000
    hardness = 400
    grade = 2
     
    cycle1 = life * 60 * rpm1
    cycle2 = life * 60 * rpm2
    if isidler == 1:
        cycle1 *= 2
    elif isidler == 2: 
        cycle2 *= 2
        
    
    safetybend1 = safetyfactor(allowbendstress(hardness, grade), bend1, 
                               findyn(cycle1), reliability)
    safetybend2 = safetyfactor(allowbendstress(hardness, grade), bend2, 
                               findyn(cycle2), reliability)
    
    safetycont1 = safetyfactor(allowcontstress(hardness, grade), cont1, 
                               findzn(cycle1), reliability)
    safetycont2 = safetyfactor(allowcontstress(hardness, grade), cont2, 
                               findzn(cycle2), reliability)
    
    print(f"Safety for Bending: \t {safetybend1} \t {safetybend2}")
    print(f"Safety for Contact: \t {safetycont1} \t {safetycont2}")
    print()
    
    return (ft, fr)
    

def tanforce(power, rpm, dia): 
    ##in m
    diameter= dia / 1000
    omega = (rpm*2*pi)/60
    torque = power / omega
    
    tanforce = torque / (diameter/2)
    return tanforce

def radforce(tanforce): 
    ##20deg
    radforce = tanforce*tan((20*pi)/180)
    return radforce 

def bending(face, dia, pinion, rpm, Np, Ng, mod, force, gear): 
    ft = force
    m = mod /1000
    b = face /1000
    
    if gear == 1: 
        J = findJ(Np, Ng)[0]
    else:
        J = findJ(Np, Ng)[1]
    
    vt = pitchline(rpm, dia/2000)
    ko = findko('uniform', 'moderate')
    ks = 1
    km = findkm(pinion, face)
    kb = 1
    kv = findkv(10, vt )
    
    #print(f"Ft: {ft}, ko: {ko}, ks: {ks}, km: {km}, kb: {kb}, kv: {kv}, vt:{vt}, J: {J}")
    
    return (ft/(m*b*J))*ko*ks*km*kb*kv

def contact(face, dia, pinion, rpm, Np, Ng, force): 
    #cp sqrt(())
    cp = 191e3 
    b = face / 1000
    I = findI(Np, Ng)
    ft = force
    
    vt = pitchline(rpm, dia/2000)
    kv = findkv(10, vt)
    ko = findko('uniform', 'moderate')
    km = findkm(pinion, face)
    ks = 1
    kb = 1
    
    #print(f"Ft: {ft}, ko: {ko}, ks: {ks}, km: {km}, kb: {kb}, kv: {kv}, vt:{vt}, I: {I}")
    
    return cp*sqrt((ft/(b*(pinion/1000)*I))*kv*ko*km*ks)

def findko(source='uniform', driven='uniform'):
    if source == 'uniform': 
        if driven == 'uniform': 
            ko = 1
        elif driven == 'light': 
            ko = 1.25
        elif driven == 'moderate': 
            ko = 1.5 
        else: 
            ko = 1.75
    elif source == 'light': 
        if driven == 'uniform': 
            ko = 1.2
        elif driven == 'light': 
            ko = 1.4
        elif driven == 'moderate': 
            ko = 1.75
        else: 
            ko = 1.25
    else: 
        if driven == 'uniform': 
            ko = 1.3
        elif driven == 'light': 
            ko = 1.7
        elif driven == 'moderate': 
            ko = 2
        else: 
            ko = 2.75
    return ko 

def findkv(grade, pitchline): 
    b = 0.25*((grade - 5.0)**0.667)
    c = 3.5637 + 3.9914*(1.0 - b)
    
    kv = (c / (c + sqrt(pitchline)))**(-b)
    return kv

def pitchline(rpm, radius): 
    omega = (rpm*2*pi)/60
    return omega * radius

def findkm(pinion, face): 
    ##input in mm
    diainch = pinion / 25.4
    faceinch = face / 25.4
    if faceinch < 1: 
        cpf = (faceinch/(10*diainch)) - 0.025
    elif faceinch < 15: 
        cpf = (faceinch/(10*diainch)) - 0.0375 + 0.0125*faceinch
    else: 
        cpf = 0 
        print("Something went wrong")
        
    #assuming commercial enclosed
    cma = 0.127 + 0.0158*faceinch - 1.093*10e-4*faceinch**2
    
    km = 1 + cpf + cma
    return km

def J2(N1, N2):
    
    # The starting point for the following tables are Collins, Mechanical Design
    # I added them points using the Mott Figure 9-15(b)
    x=np.array([17, 19, 21, 26, 29, 35, 55, 135])
    y=np.array([17, 19, 21, 26, 29, 35, 55, 135])
    #a[row,col] is the J for N1=x[col] and N2=y[row]
    a=np.array([ #                                                  N1
    [0.289,  0.315,    0.326, 0.347, 0.356,  0.378, 0.415, 0.447], #17
    [0.289,  0.316,    0.326, 0.348, 0.357,  0.380, 0.417, 0.448], #19
    [0.289,  0.317,    0.327, 0.349, 0.358,  0.381, 0.418, 0.450], #21
    [0.289,  0.319,    0.330, 0.351, 0.360,  0.384, 0.422, 0.454], #26
    [0.289,  0.321,    0.332, 0.353, 0.363,  0.387, 0.425, 0.458], #29
    [0.289,  0.325,    0.336, 0.358, 0.367,  0.392, 0.431, 0.465], #35
    [0.289,  0.333,    0.343, 0.366, 0.376,  0.402, 0.444, 0.480], #55
    [0.289,  0.339,    0.351, 0.376, 0.387,  0.414, 0.460, 0.499]])#135
#N2    7      19         21    26     29       35     55     135

    fp = interpolate.interp2d(x,y,a)
    return fp(N1,N2)[0]

def findJ(Np, Ng):
    Jp = J2(Np, Ng)
    Jg = J2(Ng, Np)
    return (Jp, Jg)

def findI(Np, Ng):
    mG = Ng/Np
    phi = 20.0/180*pi
    Cc = cos(phi)*sin(phi)/2*mG/(mG+1)
    C1 = Np*sin(phi)/2
    C2 = C1*mG
    C3 = pi*cos(phi)
    a = sqrt((Np+2)**2-(Np*cos(phi))**2)
    b = sqrt(Np**2-(Np*cos(phi))**2)
    C4 = (a-b)*0.5
    Cx = ((C1-C3+C4)*(C2+C3-C4))/(C1*C2)
    return Cc*Cx

def findkr(r):
    #input in percentage of 1.0
    import numpy as np
    R=[0.9, 0.99, 0.999, 0.9999]
    K=[0.85,1.0,1.25,1.50]
    # K=0.70 for R=0.50 but I will not allow using R<0.90.  If they do, K will
    # be that for R=0.90
    Kr=np.interp(r/100.0, R, K)
    return Kr

def findyn(cycles): 
    #bend cycle factor
    ##assume hardness of 400HB
    if cycles > 4e6: 
        yn = 1.3558 * (cycles)**(-0.0178)
    else: 
        yn = 9.4518 * (cycles)**(-0.148)
    return yn

def findzn(cycles): 
    #contact cycle factor
    if cycles > 1e7: 
        zn = 1.4488 * (cycles)**(-0.023)
    elif cycles < 1e4: 
        zn = 1.48
    else: 
        zn = 2.466 * (cycles)**(-0.056)
    return zn

def allowbendstress(hardness, grade): 
    if grade == 1: 
        sat = 0.533 * hardness + 88.26
    elif grade == 2: 
        sat = 0.703 * hardness + 113.1
    else: 
        print("grade value not implemented")
    return sat*(10**6)

def allowcontstress(hardness, grade): 
    if grade == 1: 
        sac = 2.22 * hardness + 200.6
    elif grade == 2: 
        sac = 2.41 * hardness + 236.5
    else: 
        print("grade value not implemented")
    return sac*(10**6)

def safetyfactor(allow, design, cyclefactor, rely): 
    corrected = design*(rely / cyclefactor)
    
    safety = allow / corrected 
    
    return safety


#print("GEARS 1 AND 2")
#gearstresses(5, 70, 20, 115, 2500, 434.78, 15000, False)

#print("GEARS 3 AND IDLE")
#gearstresses(5, 70, 19, 20, 434.78, 413, 15000, 2)

#print("GEARS IDLE AND 4")
#gearstresses(5, 70, 19, 69, 434.8, 120, 15000, 1)












