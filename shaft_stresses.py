# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 15:38:17 2018

@author: Deon
"""
from math import pi, sqrt
import numpy as np
from scipy import interpolate

def endurance(uts, condition="ground"):
    if condition=="ground":
        su=np.array([350, 475, 650, 875, 1050, 1250, 1450, 1500])
        sn=np.array([137, 203, 297, 400, 478,  553,  600,  612])
        return np.interp(uts, su, sn)
    elif condition=="polished":
        return 0.50*uts
    elif condition=="cold drawn" or condition=="machined":
        su=np.array([350,525,650,900,1075,1162,1275,1450,1500])
        sn=np.array([137,200,249,325,375,  400, 425, 450, 429])
        return np.interp(uts, su, sn)
    elif condition=="hot rolled":
        su=np.array([350,450,600,800,1000,1250,1400,1500])
        sn=np.array([137,150,175,200, 225, 247, 238, 237.5])
        return np.interp(uts, su, sn)
    else:
        print("TOOLS.SURFACEFINISH : Surface condition not recognised")
           
def modendurance(uts, diameter): 
    sn = endurance(uts)
    cm = 1.0 
    cst = 1.0 
    
    if diameter<8.00:
        return 1.0
    DA=np.array([12.5, 25.0, 50.0, 75.0, 100.0, 150.0, 203.0, 250.0])
    CS=np.array([0.94, 0.875,0.81, 0.776,0.755, 0.720, 0.695, 0.68])
    cs=np.interp(diameter, DA, CS)
    
    cr = 0.81 #99%
    modendure = sn * cm * cst * cs * cr 
    

    print(f"{diameter} \t {modendure} \t {sn} \t {round(cs, 4)}")
    return modendure

def bendstress(moment, radius): 
    bstress = (moment * radius)/((pi*radius**4)/4)
    return bstress

def shearstress(torsion, radius): 
    tstress = (torsion * radius)/((pi*radius**4)/2)
    return tstress

def fos(scf, bend, shear, endure, syield): 
    safety = 1 / sqrt((scf*bend/(endure*10**6))**2 + 3*((shear/(syield*10**6))**2))
    return safety

##############################################################################
    #SCF CALCS

def findscf(combine, fillet=None, bearing=None, keyseat=None, gearfit=None): 
    allscf = {}
    scflist = []
    
    #provide (largeD, smalld, radius, uts) if not None
    if fillet != None: 
        bigmm, smallmm, fillet, uts = fillet
        largeD = bigmm * 1000
        smalld = smallmm * 1000
        scf1 = shoulderscf(largeD, smalld, fillet, uts)
        allscf['fillet'] = scf1
        scflist.append(scf1)
        
    #provide tensile strength
    if bearing != None: 
        uts = bearing
        scf2 = bearingscf(uts)
        allscf['bearing'] = scf2
        scflist.append(scf2)
        
     #provide tensile strength
    if keyseat != None: 
        uts = keyseat
        scf3 = keyscf(uts)
        allscf['keyseat'] = scf3
        scflist.append(scf3)
        
    #provide tensile strength
    if gearfit != None: 
        uts = gearfit
        scf4 = gearscf(uts)
        allscf['gearfit'] = scf4
        scflist.append(scf4)
        
    """
    print("Fillet:", allscf.get('fillet', 'None'), 
          "Bearing:", allscf.get('bearing', 'None'), 
          "Keyseat:", allscf.get('keyseat', 'None'), 
          "Gearfit:", allscf.get('gearfit', 'None'), )"""
    
    #combine logic
    if combine == 0: 
        return max(scflist)
    elif combine == 1: 
        maxscf = max(scflist) 
        scflist.remove(maxscf)
        
        for scf in scflist: 
            maxscf += scf * 0.1
        return maxscf
    elif combine == 2: 
        maxscf = max(scflist) 
        scflist.remove(maxscf)
        
        for scf in scflist: 
            maxscf += scf * 0.2
        return maxscf
    else: 
        print("Something went wrong")
    
    
def scfdelta(D, d): 
    x = D/d 
    if x > 2.0: 
        x = 2.0 
    deltafit =+ ((33.78826 * x**8) + (-428.02758 * x**7) + (2360.48676 * x**6)
                + (-7400.99264 * x**5) + (14428.18588 * x**4) + (-17907.43776 * x**3) 
                + (13817.79262 * x**2) + (-6060.73737 * x) + (1157.17958)) 
    return deltafit

def shoulderscf(D, d, R, uts): 
    
    x = [400, 500, 600, 800, 900]
    y = [0.5, 0.2, 0.05, 0]
    z = [[1.11, 1.075, 1.05, 1.1, 1.15], 
         [1.4, 1.3, 1.3, 1.38, 1.45], 
         [1.88, 1.86, 1.87, 2.1, 2.3], 
         [2.52, 2.7, 2.9, 3.4, 3.7]] 
    
    f = interpolate.interp2d(x, y, z, kind='linear') 
    delta = scfdelta(D, d)
    Z = R / d + delta
    K = f(uts, Z)[0]
    
    #print(K)
    return K
    
def bearingscf(uts): 
    K = -2.4074071e-9*(uts**3) + 6.01587302e-6*(uts**2) - 3.05767196e-03*(uts) + 1.91753968
    return K

def gearscf(uts): 
    K = -3.61111111e-9*(uts**3) + 8.27380952e-6*(uts**2) - 3.95079365e-03*(uts) + 2.10809524
    return K

def keyscf(uts):
    x = uts / 1000
    K = 16.667*(x**5)-50*(x**4) + 57.5*(x**3) - 30*(x**2) + 7.6733*x + 0.54
    return K



#modendurance(779, 100)
    
#print(bendstress(63.92, 0.03))
#print(shearstress(57.3, 0.027))


#total = findscf(2, fillet=(150, 100, 5, 779), bearing=779, keyseat=779, gearfit=779)
#print(total)       
      
"""  
filletrad = 5
uts = 779
shaft1_dia = [40, 54, 100, 54, 40]
for i in range(len(shaft1_dia)): 
    if i == 0: 
        scf = findscf(2, fillet=(shaft1_dia[i+1], shaft1_dia[i], filletrad, uts), 
                      bearing=779)
    elif i == 1: 
        scf = findscf(0, fillet=((shaft1_dia[i+1], shaft1_dia[i], filletrad, uts)))
    elif i == 2: 
        scf = 1 
    elif i == 3: 
        scf = findscf(0, fillet=((shaft1_dia[i-1], shaft1_dia[i], filletrad, uts)))
    elif i == 4:
        scf = findscf(2, fillet=(shaft1_dia[i-1], shaft1_dia[i], filletrad, uts), 
                      bearing=779)
    else: 
        print("Something went wrong")
        scf == 1
        
    print(scf)
"""
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        