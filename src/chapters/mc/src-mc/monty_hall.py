#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 14:43:55 2019

@author: ah
"""
import random as r

def monty_hall(N,switch=False):
    won=0
    for i in range(N):
        prize = r.randint(1,3)
        guess = r.randint(1,3)
        if (guess == prize and not(switch)):
            won += 1
        if (guess != prize and switch):
            won+=1
    if(switch):
        sw = 'switching'
    else:
        sw = 'not switching'
    print('Probability of winning when '+str(sw)+' is: {0:.5f}'.format(won/N))

monty_hall(100000,False)
    

    