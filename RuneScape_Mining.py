from PIL import ImageGrab
import os
import time
import win32api, win32con
from random import randrange
from array import *
import random

#ScreenGrab Setting
x_pad = 1
y_pad = 31
x_pad2 = 1146
y_pad2 = 1038

def screenGrab():
    box = (x_pad,y_pad,x_pad2,y_pad2)
    im = ImageGrab.grab(box)
    #im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')

    return im
    
def rightClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    #print("Click.")          #completely optional. But nice for debugging purposes.

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    #print("Click.")          #completely optional. But nice for debugging purposes.

def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    print('left Down')
         
def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)
    print('left release')
            
def mousePos(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))
     
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print(x,y)

def dump_pixel():
    #Inventory Coordinates
    inventory_x = [970, 1018, 1066, 1114]
    inventory_y = [570, 606, 642, 678, 714, 750, 786]

    s = screenGrab()
    time.sleep(.2)

    for a in range(7):
        for b in range(4):
            x_t,y_t = (inventory_x, inventory_y)
            print("Mouse: {} | Pixel Value: {}".format((x_t[b],y_t[a]),s.getpixel((x_t[b],y_t[a]))))
            time.sleep(.2)
            
def checkMatch(satu, dua):
    if(satu == dua):
        return(True)
    else:
        return(False)
    
def VerifySpacing(pixel):
    item_desc = [((125, 125, 114),72),((16, 16, 128),54),((152, 152, 116),54),((171, 157, 157),54),((103, 16, 0),54)]

    Task_Match = False
    i = 0
    extra = 0
    for i in range(len(item_desc)):
        if(pixel == item_desc[i][0]):
            extra = item_desc[i][1]
            break
        else:
            extra = 36

    return extra

def clear_inventory():
    s = screenGrab()
    time.sleep(.2)
    
    for a in range(7):
        for b in range(4):
            cor_x = [970, 1018, 1066, 1114]
            cor_y = [570, 606, 642, 678, 714, 750, 786]
            #Analyse Inventory
            extra = VerifySpacing(s.getpixel((cor_x[b], cor_y[a])))
            
            (random_x, random_y) = randomExtra()
            cor_x[b] = cor_x[b] + random_x
            cor_y[a] = cor_y[a] + random_y
            
            #Clicking Begin
            mousePos((cor_x[b], cor_y[a]))
            rightClick()
            time.sleep(.2)
            time.sleep(randomMillisDelay())
            mousePos((cor_x[b], cor_y[a]+extra))
            leftClick()
            time.sleep(randomMillisDelay())
            
        print("{} rows cleared".format(a+1))
        
    print("Clearing completed")
        
def randomMouse():
    print("Moving mouse.... ")
    
    x = randrange(1145)
    y = randrange(1007)
    mousePos((x, y))
    time.sleep(randomMillisDelay())
    
def MiningAdjust():
    x_adjust = randrange(-2,2)
    y_adjust = randrange(-2,2)
    
    return (x_adjust,y_adjust)

def Mining():
    (x, y) = (647, 536)
    
    (x_tra, y_tra) = MiningAdjust()
    #(x_tra, y_tra) = (0, 0)
    x = x + x_tra
    y = y + y_tra
    mousePos((x, y))
    mousePos((x, y))
    time.sleep(.2)
    print("Start mining")
    leftClick()
    time.sleep(randomMillisDelay())
    leftClick()
    time.sleep(randomMillisDelay())

def startGame():
    if(Time >= 240):    
        print("Mining Done --- 4 minutes")
        clear_inventory()
        time.sleep(1)
        Time = 0
    
def ShowPixel(x,y):
    im = screenGrab()
    inventory_1 = (x, y)
    a = im.getpixel(inventory_1)
    print(a)

def checkInventoryFull():
    data = [(152, 152, 116),(125, 125, 114),(58, 80, 90),(203, 193, 169),(131, 152, 116)]

    fixLogin()
    s = screenGrab()
    time.sleep(.2)
    #Rune Ore(32, 48, 53)
    #Others (0, 0, 2)

    Matched = False
    
    for i in range((len(data))):
        if s.getpixel((1114, 786)) == data[i]:
            Matched = True

    if (Matched == True):
        print("Inventory Full")
        return(1)
    else:
        return(0)

def randomExtra():
    xExtra = randrange(-3,3)
    yExtra = randrange(-3,3)

    return(xExtra,yExtra)

def randomMillisDelay():
    a = random.uniform(0.2, 0.6)
    a = round(a, 2)
    return(a)

def fixLogin():
    s = screenGrab()
    time.sleep(0.2)

    if s.getpixel((568, 529)) == (243, 193, 58):
        mousePos((568, 529))
        leftClick()
        time.sleep(randomMillisDelay())
        time.sleep(10)
        
        if s.getpixel((568, 529)) == (0, 0, 0):
            time.sleep(10)
        else:
            print("Account Status : Connected")

def main():
    minutes = 14444 #4 hours + 1 minutes
    bot_start = time.time()
    print("Auto-Mining : ON  |  Time: {}".format(time.strftime("%d-%m-%Y %I:%M %p", time.gmtime(bot_start+28800))))
    miningFlag = False
    
    while((time.time() - bot_start) < 14444):
        if(checkInventoryFull() == 1):
            clear_inventory()
            time.sleep(.5)
        else:

            if(miningFlag == False):
                start_mining = time.time()
                Mining()
                tDelay = randrange(3,6)
                miningFlag = True

            if(miningFlag == True):
                randomMouse()
                
            if(time.time() - start_mining) > tDelay:
                miningFlag = False
                tDelay = 0
                time.sleep(3)
                    
    print("Bot shutdown.....");
    
if __name__ == '__main__':
    #main()
    
    #time.sleep(7200);
    pass
    
