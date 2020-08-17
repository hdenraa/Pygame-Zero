# gameinput Module

from pygame import joystick, key
from pygame.locals import *
import sys, serial, time
from random import randint
import re
import serial.tools.list_ports

ports = list( serial.tools.list_ports.comports(True) )
port = "/dev/ttyACM0"
for p in ports:
	if p.description == 'DAPLink CMSIS-DAP - mbed Serial Port':
	   port = p.device


baud = 115200
sumx = 0
sumy = 0  
count=0  
joystick.init()
joystick_count = joystick.get_count()

if(joystick_count > 0):
    joyin = joystick.Joystick(0)
    joyin.init()


def checkInput(p):
    global joyin, joystick_count, port, baud
    
    s = serial.Serial(port)
    s.baudrate = baud
    #s.parity = serial.PARITY_NONE
    #s.databits = serial.EIGHTBITS
    #s.stopbits = serial.STOPBITS_ONE
    notfound = True
    while notfound:
        data = s.readline()
    #time.sleep(0.1)
        data = str(data)
    #print(data)
        mbit = False
        tr = 200 #treshold 

        if "x, y, z:" in data:
            mbit = True
            #count += 1 
            split = data.split(":")[-1].split()
            print(split)
            if len(split) == 3:
                x = int(split[0])
                y = int(split[1])
                z = int(re.sub('[^-0-9]', '',split[2]))
                notfound = False
            #print("New x, y, z:", x, y, z)
 
    xaxis = yaxis = 0
    
    if p.status == 0:
        if mbit:
            if abs(x) >= abs(y):
                if x > tr:
                    xaxis = 1    
                elif x < -tr:
                    xaxis = -1
                else:
                    xaxis = 0
               
                        
            elif abs(x) < abs(y):    
                if y > tr:
                    yaxis = 1 
                elif y < -tr:
                    yaxis = -1
                else:
                    yaxis = 0
        if joystick_count > 0:
            xaxis = joyin.get_axis(0)
            yaxis = joyin.get_axis(1)
        if key.get_pressed()[K_LEFT] or xaxis < -0.8:
            p.angle = 180
            p.movex = -20
        if key.get_pressed()[K_RIGHT] or xaxis > 0.8:
            p.angle = 0
            p.movex = 20
        if key.get_pressed()[K_UP] or yaxis < -0.8:
            p.angle = 90
            p.movey = -20
        if key.get_pressed()[K_DOWN] or yaxis > 0.8:
            p.angle = 270
            p.movey = 20
    if joystick_count > 0:
        jb = joyin.get_button(1)
    else:
        jb = 0
    if p.status == 1:
        if key.get_pressed()[K_RETURN] or jb:
            return 1
    if p.status == 2:
        if key.get_pressed()[K_RETURN] or jb:
            return 1
        
            
    
