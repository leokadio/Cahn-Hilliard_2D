import numpy as np
import matplotlib.pyplot as plt
import time

tp = 0

Dt = 0.5

tmin = 0

dt = 0.01

coef = np.sqrt(2*Dt)

l = 50

passos = 10**6

array = np.zeros((5, passos + 1))

t = 0

i = 0

while i < passos:
    '''underdamped'''
    '''
    aleatorio = np.random.normal(0, 1)

    array[2][i+1] = array[2][i]*(1 - dt/tp) + coef*aleatorio/tp#VX

    aleatorio = np.random.normal(0, 1)

    array[3][i+1] = array[3][i]*(1 - dt/tp) + coef*aleatorio/tp#VY

    array[0][i+1] = array[0][i] + array[2][i+1]*dt#X

    array[1][i+1] = array[1][i] + array[3][i+1]*dt#Y
    '''

    '''aristotelico ou overdamped'''

    aleatorio = np.random.normal(0, 1)

    array[2][i+1] = coef*aleatorio#VX

    aleatorio = np.random.normal(0, 1)

    array[3][i+1] = coef*aleatorio#VY

    array[0][i+1] = array[0][i] + array[2][i+1]*dt#X

    array[1][i+1] = array[1][i] + array[3][i+1]*dt#Y

    t = round(t + dt, int(-np.log10(dt) + 2))

    array[4][i + 1] = t#TEMPO

    i+=1

print(i)

print("cabou")

np.save(f"tp_{tp}&Dt_{Dt}.npy", array)
