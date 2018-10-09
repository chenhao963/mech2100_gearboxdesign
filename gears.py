# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 17:09:05 2018

@author: Deon
"""
from math import pi , cos, acos
import pylab

class gears: 
    def __init__(self, inspeed, outspeed, sdistance): 
        #speed ratios
        self.inspeed = inspeed 
        self.outspeed = outspeed
        self.trainvalue = inspeed / outspeed
        self.actvalue = 0 
        
        #possible module numbers
        self.modulelist = [5, 6, 7]
        self.module = 0
        
        self.distance = sdistance
        self.calculate = 0 
        
        #teeth numbers
        self.n1 = 20
        self.n2 = 0
        self.n3 = 0
        self.n4 = 0
        self.ni = 0
        
        #radius values 
        self.r1 = 0 
        self.r2 = 0 
        self.r3 = 0 
        self.r4 = 0 
        self.ri = 0
        
        self.alpha = 0
        self.beta = 0
        self.gamma = 0
        
        #store good values
        self.validvalues = []
        
    def run(self): 
        #for modnum in self.modulelist: 
        #print("Values for module = ", modnum, "mm")
        #modnum = 6
        
        for modnum in self.modulelist: 
            self.module = modnum
            self.teethvalues(self.module) 
        self.writevalues()
        
        
    def teethvalues(self, mod): 
        #gear 2
        for i in range(self.n1, 150):
            self.n2 = i 
            
            #gear 3
            for j in range(10, 50): 
                self.n3 = j 
                
                #round off
                self.n4 = int(round((self.trainvalue * self.n1 * (self.n3 / self.n2)), 0))
                
                #compute actual speed out from gears
                self.actvalue = self.inspeed*((self.n1 * self.n3) / (self.n2 * self.n4))
    
                self.findradius(mod)
               
                #self.ri = self.findri(self.r3, self.r4, 30)
                for k in range(self.n3 - 5, self.n3 + 5): 
                    self.ni = k 
                    self.ri = round((mod * self.ni)/2, 3)
                    
                    self.alpha, self.beta, self.gamma = self.trianglesolver(self.distance, 
                                        (self.r3 + self.ri), 
                                        (self.r4 + self.ri))
                    
                    self.trimvalues()
                
            
    def findradius(self, mod):  
        self.r1 = round((mod * self.n1)/2, 3)
        self.r2 = round((mod * self.n2)/2, 3)
        self.r3 = round((mod * self.n3)/2, 3)
        self.r4 = round((mod * self.n4)/2, 3)
        
    def trimvalues(self): 
        #conditions (adjust error for first condition)
        ACCURATE_SPEED_OUT = abs(self.actvalue - self.outspeed) <= (25e-2)
        GAP_BETWEEN_34 = self.r3 + self.r4 < self.distance 
        NICE_GEAR_SIZE = self.r2 < 400.0 and self.r3 > 30.0 and self.ri > 30.0
        INVALID_ANGLE = self.alpha != 0
        
        #gets rid of inaccurate values for speed ratio
        if ACCURATE_SPEED_OUT and GAP_BETWEEN_34 and NICE_GEAR_SIZE and INVALID_ANGLE: 
        
            
            #optional values 
            HUNTING_TOOTH = self.n3 % 2 != self.ni % 2 and self.ni % 2 != self.n4 % 2

            if HUNTING_TOOTH: 
                self.calculate = self.checkdistance()
                self.validvalues.append((self.n1, self.n2, self.n3, self.n4, 
                                         self.ni, round(self.actvalue, 3), 
                                         self.r1, self.r2, self.r3, 
                                         self.r4, self.ri, round(self.alpha, 8), 
                                         round(self.beta, 8), round(self.gamma, 8), 
                                         self.calculate, self.module))
                        

    def trianglesolver(self, distance, r3ri, r4ri): 
        try: 
            #bottom angle
            alpha = acos((r3ri**2 + distance**2 - r4ri**2)/(2*r3ri*distance))
        
            #top angle 
            beta = acos((r4ri**2 + distance**2 - r3ri**2)/(2*r4ri*distance))
        
            #side angle 
            gamma = acos((r3ri**2 + r4ri**2 - distance**2)/(2*r3ri*r4ri))
        except ValueError: 
            alpha = 0
            beta = 0
            gamma = 0
        
        return ((alpha*180)/pi, (beta*180)/pi, (gamma*180)/pi)
    
    def checkdistance(self): 
        radalpha = (self.alpha * pi)/180
        radbeta = (self.beta * pi)/180
        return (self.r3 + self.ri)*cos(radalpha) + (self.r4 + self.ri)*cos(radbeta)

            
    def writevalues(self): 
        file = open("gear_values.txt", "w")
        file.write("Module  Teeth Numbers \t\t\t Radii Values \t\t\t Angles\n")
        file.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" + 
                   "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        
        for x in self.validvalues:
            file.write(str(x[-1]) + "\t")
            
            file.write(str(x[0]) + " " + str(x[1]) + " " + str(x[2]) + 
                       " " + str(x[3]) + " " + str(x[4]) + "\t" + str(x[5]) + "\t\t")
            
            file.write(str(x[6]) + " " + str(x[7]) + " " + str(x[8]) + 
                       " " + str(x[9]) + " " + str(x[10]) + "\t")
            
            file.write(str(x[11]) + "\t" + str(x[12]) + "\t" + str(x[13]) + 
                       "\t" + str(x[14]))
            
            file.write('\n')
        
        file.close()
        
    
#spur = gears(2750, 125, 280.952424) 
#spur.run()
