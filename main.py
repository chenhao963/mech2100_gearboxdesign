# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 16:15:08 2018

@author: Deon
"""
 
from distanceplot import trianglesolver, plotsdistance
from shaft_forces import shaftbendingmoment
from bearings import dynamicload
from gear_stresses import gearstresses
from shaft_stresses import modendurance, bendstress, shearstress, fos, findscf

##############################################################################
    #PARAMETERS
##############################################################################
mod = 5 #mm 
face = 60 #70 
power = 17000 #15000
sdistance = 280.952424
speedin = 2750 #250

uts = 779 #MPa
syield = 600

n1 = 20
n2 = 143 #115
n3 = 26 #19
n4 = 80 #69
ni = 25 #20

bearhours = 30000

d1 = n1*mod
d2 = n2*mod
d3 = n3*mod
d4 = n4*mod
di = ni*mod

r1 = n1*mod/2
r2 = n2*mod/2
r3 = n3*mod/2
r4 = n4*mod/2
ri = ni*mod/2

speedmid = speedin / (n2/n1)
speedidle = speedmid / (ni/n3)
speedout = speedmid / (n4/n3)

alpha, beta, gamma = trianglesolver(sdistance, r3, r4, ri)



print("MECH2100 GEARBOX ASSIGNMENT")
print("~"*70)
print("CHOSEN GEARS:", n1, n2, n3, n4, ni)
print("DIAMETERS:", d1, d2, d3, d4, di)
print("SPEEDS:", speedin, speedmid, speedidle, speedout)
print()
#PLOT
plotsdistance(r3, r4, ri)
##############################################################################

#shaft geometry shaft 1
shoulderwidth1 = 0.030 #free to change
bearingwidth1 = 0.017
dia1_0 = 0.025
dia1_1 = 0.050
dia1_2 = d1 / 1000
dia1_3 = dia1_1
dia1_4 = dia1_0
shaft1_dia = [dia1_0, dia1_1, dia1_2, dia1_3, dia1_4]

#shaft2
bearingwidth2 = 0.033
middlewidth = 0.050 #free to change
dia2_0 = 0.065
dia2_1 = 0.090
dia2_2 = dia2_1
dia2_3 = 0.090
dia2_4 = dia2_3
shaft2_dia = [dia2_0, dia2_1, dia2_2, dia2_3, dia2_4]
middle_dia = 0.09 #free to change

#shaft3
shoulderwidth3 = 0.030 #free to change
bearingwidth3 = 0.023
dia3_0 = 0.040
dia3_1 = 0.070
dia3_2 = d4 / 1000
dia3_3 = dia3_1
dia3_4 = dia3_0
shaft3_dia = [dia3_0, dia3_1, dia3_2, dia3_3, dia3_4]

geometry = (shoulderwidth1, bearingwidth1, bearingwidth2, middlewidth, 
            shoulderwidth3, bearingwidth3)

##############################################################################
    ##Stress in Gears
print()
print("GEARS 1 AND 2")
ft1, fr1 = gearstresses(mod, face, n1, n2, speedin, speedmid, power, False)

print("GEARS 3 AND IDLE")
ft3, fr3 = gearstresses(mod, face, n3, ni, speedmid, speedidle, power, 2)

print("GEARS 3 AND 4")
gearstresses(mod, face, n3, n4, speedmid, speedout, power, False)

print("="*70)
print("="*70)

    ##Shaft Forces

print("SHAFT FORCES")
ft2 = ft1
fr2 = fr1

ft4 = ft3
fr4 = fr3

fti = ft3
fti = ft3

reactions, torq1, bend1, torq2, bend2, torq3, bend3 = shaftbendingmoment(ft1, fr1, ft4, 
                                                              fr4, speedin, 
                                                              speedmid, speedout, 
                                                              alpha, geometry)

print("REQUIRED BEARING LOAD RATINGS")
print("Shaft 1:", dynamicload(reactions[0], speedin, bearhours, 99))
print("Shaft 2 Gear 3 End:", dynamicload(reactions[1], speedmid, bearhours, 99))
print("Shaft 2 Gear 2 End:", dynamicload(reactions[2], speedmid, bearhours, 99))
print("Shaft 3:", dynamicload(reactions[3], speedout, bearhours, 99))

print("="*70)
print("="*70)
##############################################################################
    #SHAFT STRENGTHS
    
filletrad = 5

print("SHAFT STRENGTHS: Shaft 1")
print("D \t ModEndurance \t\t Original \t\t SizeFac")
print("\t BendStress \t\t ShearStress \t\t SCF \t FOS")
print()
for i in range(len(shaft1_dia)):
    
    
    diameter = shaft1_dia[i]
    endure = modendurance(uts, diameter*1000)
    
    bstress = bendstress(bend1[i], (shaft1_dia[i] / 2))
    
    #A and E have no torque 
    if i == 0 or i == 4: 
        tstress = 0.0
    else: 
        tstress = shearstress(torq1, (shaft1_dia[i] / 2))
    
    
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
    
    safety = fos(scf, bstress, tstress, endure, syield)
    
    print(f"\t {bstress} \t {tstress} \t {round(scf, 3)} \t {round(safety, 4)}")
    print("_"*70)

    
print()
print("Shaft 2")
for i in range(len(shaft2_dia)): 
    diameter = shaft2_dia[i]
    endure = modendurance(uts, diameter*1000)
    
    bstress = bendstress(bend2[i], (shaft2_dia[i] / 2))
    
    #A have no torque 
    if i == 0: 
        tstress = 0.0
    else:
        tstress = shearstress(torq2, (shaft2_dia[i] / 2))
    
    if i == 0: 
        scf = findscf(2, fillet=(shaft2_dia[i+1], shaft2_dia[i], filletrad, uts), 
                      bearing=779)
    elif i == 1: 
        scf = 1
    elif i == 2: 
        scf = findscf(0, fillet=(((d3/1000), shaft2_dia[i+1], filletrad, uts)))
    elif i == 3: 
        scf = findscf(2, fillet=(middle_dia, shaft2_dia[i], filletrad, uts), 
                      keyseat=779)
    elif i == 4:
        scf = findscf(2, keyseat=779)
    else: 
        print("Something went wrong")
        scf == 1
    
    safety = fos(scf, bstress, tstress, endure, syield)
    print(f"\t {bstress} \t {tstress} \t {round(scf, 3)} \t {round(safety, 4)}")
    print("_"*70)
    
print()
print("Shaft 3")
for i in range(len(shaft3_dia)): 
    diameter = shaft3_dia[i]
    endure = modendurance(uts, diameter*1000)
    
    bstress = bendstress(bend3[i], (shaft3_dia[i] / 2))
    
    #A and E have no torque 
    if i == 0 or i == 4: 
        tstress = 0.0
    else: 
        tstress = shearstress(torq3, (shaft3_dia[i] / 2))
    
    if i == 0: 
        scf = findscf(2, fillet=(shaft1_dia[i+1], shaft1_dia[i], filletrad, uts), 
                      bearing=779)
    elif i == 1: 
        scf = findscf(2, fillet=((shaft1_dia[i+1], shaft1_dia[i], filletrad, uts)), 
                      gearfit=779)
    elif i == 2: 
        scf = findscf(0, gearfit=779)
    elif i == 3: 
        scf = findscf(2, fillet=((shaft1_dia[i-1], shaft1_dia[i], filletrad, uts)), 
                      gearfit=779)
    elif i == 4:
        scf = findscf(2, fillet=(shaft1_dia[i-1], shaft1_dia[i], filletrad, uts), 
                      bearing=779)
    else: 
        print("Something went wrong")
        scf == 1
    
    safety = fos(scf, bstress, tstress, endure, syield)
    print(f"\t {bstress} \t {tstress} \t {round(scf, 3)} \t {round(safety, 4)}")
    print("_"*70)

print("Reliability = 0.81, Cm = 1, Cst = 1")

print("="*70)
print("="*70)


























