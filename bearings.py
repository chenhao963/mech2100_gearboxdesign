# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 12:10:30 2018

@author: Deon
"""

def dynamicload(load, rpm ,hours, rely): 
    k = 3 
    
    if rely == 99: 
        cr = 0.21 #99% 
    elif rely == 98: 
        cr = 0.33
    elif rely == 97: 
        cr = 0.44 
    elif rely == 96:
        cr = 0.53
    elif rely == 95: 
        cr = 0.62
    else: 
        cr = 1
        
    L10 = hours * rpm * 60
    
    c = load*((L10 / (cr * (10**6)))**(1/k))
    
    return c
    

print(dynamicload(3690, 120, 30000, 99))
    
    