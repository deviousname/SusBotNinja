#SusBot -= Ninja Edition ~ ~ ~ ~* ~* ~ ~*
import requests
import crewmate
import os
import json
import keyboard
import socketio #python-socketio[client]==4.6.1
import threading
import math
import random
import time
import urllib.request
import math
import PIL
import numpy as np
import itertools
from itertools import cycle
from numpy import sqrt
from PIL import Image
from ast import literal_eval as make_tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
sio = socketio.Client()

controls = ['',
            "[Controls:                                         ]",
            '[                                                  ]',
            "['shift+insert' # slow down bot                    ]",
            "['shift+delete' # speed up bot                     ]",
            "['shift+w # auto-pathing river spirit              ]",
            "['v' # measures distance                           ]",
            "['s' # drag to draw circle                         ]",
            "['shift+e' # if its flammable, it burns            ]",
            "['a' # single color replacing bucket fill          ]",
            "['d' # draw a bendy river                          ]",
            "['r' # draw single tree, drag/release for forest   ]",
            "['shift+r' # pour water from top to bottom         ]",
            "['shift+a' # every color replacing bucket fill     ]",
            "['o' # bootleg missile                             ]",
            "['f8' # drag it across an area to copy             ]",
            "['f9' # press to paste, centered at mouse location ]",
            '[                                                  ]',
            "['shift+d' # stop key                              ]",
            '',]

###########################
#### Options: #############
autologin = False # True/False - requires Reddit account linked to Pixelplace if True
chart = 7 # map number
stop_key = 'shift+d' # press this hotkey bind to stop the bot while its drawing something
unit_measurement = 'pixels' #change it to whatever you want; miles, feet, bannanas...
###########################
###########################

colors =[(255,255,255),(196,196,196),(136,136,136),(85,85,85),(34,34,34),
        (0,0,0),(0,102,0),(34,177,76),(2,190,1),(81,225,25),(148,224,68),
        (251,255,91),(229,217,0),(230,190,12),(229,149,0),(160,106,66),
        (153,83,13),(99,60,31),(107,0,0),(159,0,0),(229,0,0),(255,57,4),
        (187,79,0),(255,117,95),(255,196,159),(255,223,204),(255,167,209),
        (207,110,228),(236,8,236),(130,0,128),(81,0,255),(2,7,99),(0,0,234),
        (4,75,255),(101,131,207),(54,186,255),(0,131,199),(0,211,221),(69,255,200)]

null = [(204,204,204)]
ocean = [o for o in colors if colors.index(o) in range(30,38+1)]
fire = [f for f in colors if colors.index(f) in (11,12,13,14,20)]
smoke = [s for s in colors if colors.index(s) in range(1,5)]
leaves = [l for l in colors if colors.index(l) in range(6,10+1)]
trunks = [t for t in colors if colors.index(t) in range(15,17+1)]
sand = [sa for sa in colors if colors.index(sa) in (11,12,24,25)]

class SusBot():
    def __init__ (self):
        self.load_map_into_cache()
        if autologin == True:
            self.login()
        else:
            driver.get(f"https://pixelplace.io/{chart}")
        self.authid, self.authtoken, self.authkey = None, None, None
        while self.authid == None and self.authtoken == None and self.authkey == None:
            try:
                self.auth_data()
            except:
                pass
        if chart != 7:
            driver.get(f"https://pixelplace.io/{chart}")
        self.connection()
        self.hotkeys()
        self.colorfilter = [None, None, None, None, None, None, None, None, None, None]
        self.color = random.randint(0, len(colors))
        self.borders = False
        
    def login(self):
        driver.get("https://pixelplace.io/api/sso.php?type=2&action=login")
        driver.find_element(By.ID,'loginUsername').send_keys(crewmate.username)
        driver.find_element(By.ID,'loginPassword').send_keys(crewmate.password)
        driver.find_elements(By.XPATH,'/html/body/div/main/div[1]/div/div[2]/form/fieldset')[4].click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div/div[2]/form/div/input'))).click()
        try:
            WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH,'/html/body/div[5]/div[2]/a/img'))).click()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div[8]/a[2]/div[3]/button[2]'))).click()
        except:
            pass
        print('Logged in.')
        return
    
    def load_map_into_cache(self):
        with open(f'{chart}.png', 'wb') as f:
            f.write(requests.get(f'https://pixelplace.io/canvas/{chart}.png?t={random.randint(9999,99999)}').content)
        self.image = PIL.Image.open(f'{chart}.png').convert('RGB')
        self.cache = self.image.load()
                
    def auth_data(self):
        self.authkey = driver.get_cookie("authKey").get('value')
        self.authtoken = driver.get_cookie("authToken").get('value')
        self.authid = driver.get_cookie("authId").get('value')
            
    def connection(self):
        print(f'Connected.')
        sio.connect('https://pixelplace.io', transports=['websocket'])
        @sio.event
        def connect():
            sio.emit("init",{"authKey":f"{self.authkey}","authToken":f"{self.authtoken}","authId":f"{self.authid}","boardId":chart})
            threading.Timer(15, connect).start()
        @sio.on("p")
        def update_pixels(p: tuple):
            try:
                for i in p:        
                    self.cache[i[0], i[1]] = colors[i[2]]
            except:
                pass
        
    def xy(self):
        try:
            self.x, self.y = make_tuple(driver.find_element(By.XPATH,'/html/body/div[3]/div[4]').text)
            return self.x, self.y
        except:
            pass
            
    def get_color_index(self):
        try:
            cid = str(driver.find_element(By.XPATH,'/html/body/div[3]/div[2]').get_attribute("style"))
            a = cid.find('(')
            b = cid.find(')');b+=1
            cid = cid[a:b]
        finally:
            return colors.index(make_tuple(cid))
        
    def return_color(self):
        try:
            self.color = self.get_color_index()
        except:
            self.color = random.randint(0, len(colors)-1)
        return self.color
    
    def visibility_state(self):
        try:
            vis = driver.execute_script("return document.visibilityState") == "visible"
        except:
            driver.switch_to.window(driver.window_handles[0])
            vis = driver.execute_script("return document.visibilityState") == "visible"
        if vis == False:
            p = driver.current_window_handle
            chwd = driver.window_handles
            for w in chwd:
                if(w!=p):
                    driver.switch_to.window(w)
                    
    def primeCheck(self, n): #checks if prime int
        # 0, 1, even numbers greater than 2 are NOT PRIME
        if n==1 or n==0 or (n % 2 == 0 and n > 2):
            return "Not prime"
        else:
            # Not prime if divisable by another number less
            # or equal to the square root of itself.
            # n**(1/2) returns square root of n
            for i in range(3, int(n**(1/2))+1, 2):
                if n%i == 0:
                    return "Not prime"
            return "Prime"
        
    def cy_cols(self, a):
        a += 1
        if a > len(colors):
            a = 0
        self.color = a
        return self.color
    
    def oceaneer(self):
        self.color += 1 if random.random() < .5 else -1
        if self.color < 30:
            self.color = 38
        if self.color > 38:
            self.color = 30
        return self.color

    def emitsleep(self, x, y, color, filters):
        try:
            if self.cache[x,y] not in [colors[color]] + filters + null + self.colorfilter: 
                sio.emit('p',[x, y, color, 1])
                time.sleep(speed - (self.start - time.time()))
                self.start = time.time()
                return True
            else:
                return False
        except:
            return False
        
    def distance(self, xy1, xy2):
        return int(math.sqrt((xy2[0] - xy1[0])**2 + (xy2[1] - xy1[1])**2))
    
    def average(self, xy1, xy2):
        return [(xy1[0] + xy2[0]) / 2, (xy1[1] + xy2[1]) / 2]

    def coordinate_list_average(self, coordinate_list):
        try:
            x_sum = 0
            y_sum = 0
            for coordinate in coordinate_list:
                x_sum += coordinate[0]
                y_sum += coordinate[1]
            return int(x_sum/len(coordinate_list)), int(y_sum/len(coordinate_list))
        except:
            pass
        
    def change_speed(self, opt): #works great
        global speed
        if opt == 'decrease':
            speed += 0.001
            speed = float('%.3f'%speed)
            print("Speed:",speed)
        elif opt == 'increase':
            speed -= 0.001
            speed = float('%.3f'%speed)
            print("Speed:",speed)
        if speed < 0.015:
            print(f"Going too fast now, defaulting to {default_speed} to prevent perma ban.")
            speed = default_speed
        
    def getcurcolorhotkey(self, col): #sets the rgb color to 1-9 slots
        try:
            self.colorfilter[col-1] = colors[self.get_color_index()]
            print(f'Equipped {self.colorfilter[col-1]} to slot {col}')
            return
        except Exception as e:
            print(e)
            pass
        
    def removefilters(self): #removes equipped colors on the 1-9 and 0 slots
        self.colorfilter[0:] = None, None, None, None, None, None, None, None, None, None
        print("Filters dequipped.")
        
    def onkeypress(self, event): #whatever 1-9 key you press will allow you to equip a color to be filtered
        if event.name == '1':
            self.getcurcolorhotkey(1)
        elif event.name == '2':
            self.getcurcolorhotkey(2)
        elif event.name == '3':
            self.getcurcolorhotkey(3)
        elif event.name == '4':
            self.getcurcolorhotkey(4)
        elif event.name == '5':
            self.getcurcolorhotkey(5)
        elif event.name == '6':
            self.getcurcolorhotkey(6)
        elif event.name == '7':
            self.getcurcolorhotkey(7)
        elif event.name == '8':
            self.getcurcolorhotkey(8)
        elif event.name == '9':
            self.getcurcolorhotkey(9)
        elif event.name == '0':
            self.getcurcolorhotkey(0)
        elif event.name in ['`', '~']:
            self.removefilters()
            
    def hotkeys(self):
        keyboard.on_press(self.onkeypress)#1-9 buttons equip currently selected colors
        keyboard.add_hotkey("f8", lambda: self.copypaste('copy', "f8")) #press and hold button, move mouse to right and down, release to copy
        keyboard.add_hotkey("f9", lambda: self.copypaste('paste', "f9")) #press to paste if you have copied
        keyboard.add_hotkey("shift+insert", lambda: self.change_speed('decrease')) #decrease bot speed
        keyboard.add_hotkey("shift+del", lambda: self.change_speed('increase'))#increase bot speed
        keyboard.add_hotkey((key:='s'),lambda:self.circle_outline(key)) #draw a circle
        keyboard.add_hotkey((key1:='shift+w'),lambda:self.bezier_curve(key1)) #auto-pathing
        keyboard.add_hotkey((key2:='v'),lambda:self.bamboo_shaft(key2)) #measures distance
        keyboard.add_hotkey((key3:='shift+e'),lambda:self.way_of_the_dragon(key3)) #if its flammable, it burns
        keyboard.add_hotkey((key4:='a'),lambda:self.mighty_wind_alt(key4))#single color replacing bucket fill
        keyboard.add_hotkey((key5:='d'),lambda:self.river_bend(key5))#draws a bendy river
        keyboard.add_hotkey((key6:='shift+r'),lambda:self.surging_waves(key6)) #pour water from top to bottom
        keyboard.add_hotkey((key7:='shift+a'),lambda:self.mighty_wind(key7)) #every color replacing bucket fill
        keyboard.add_hotkey((keytree:='r'),lambda:self.tree(keytree)) #draw tree
        keyboard.add_hotkey((key9:='['),lambda:self.thick_line(key9)) #2 pixels wide
        keyboard.add_hotkey((key10:='o'),lambda:self.bootleg_missle(key10))#shhh dont tell anyone

    def bootleg_missle(self, key):
        try:
            color = self.return_color()
            x, y = self.xy()
            for bx in range(x-3, x+4):
                for by in range(y-4, y+3):
                    try:
                        sio.emit("p",[bx, by, self.cy_cols(colors.index(self.cache[bx, by])), 1])
                    except:
                        pass
            time.sleep(speed * 55)
        except Exception as e:
            print(e)
            pass
        
    def thick_line(self, key):
        try:
            self.color = self.return_color()
            start, end = (xy:=self.xy()),xy
            while keyboard.is_pressed(key):
                pass
            end = self.xy()
            x1, y1 = start
            x2, y2 = end
            x_difference = x2 - x1
            y_difference = y2 - y1
            x_length = abs(x_difference)
            y_length = abs(y_difference)
            length = max([x_length, y_length])
            if length == 0:
                length = 1
            if x_difference == 0:
                x_difference = 1
            if y_difference == 0:
                y_difference = 1
            slope = y_difference / x_difference
            self.start = time.time()
            for i in range(1, length):
                if keyboard.is_pressed(stop_key):
                    print('Canceling job.')
                    return
                x3 = int(x1 + (i * (x_difference / length)))
                y3 = int(y1 + (i * (y_difference / length)))
                self.emitsleep(x3, y3, self.color, [])
                self.emitsleep(x3+1, y3, self.color, [])
                self.emitsleep(x3, y3+1, self.color, [])
                self.emitsleep(x3+1, y3+1, self.color, [])
        except:
            pass
        
    def copypaste(self, option, key): #this is the copy/paster
        try:
            if option == "copy": #copy
                self.xy()
                x1, y1 = self.x, self.y
                while True: #hold key and drag mouse and release key to set size
                    if not keyboard.is_pressed(key):
                        self.xy()
                        break
                x2, y2 = self.x+1, self.y+1            
                print('Copying...')
                self.work_order = ()
                cx = (x2 - x1) // 2
                cy = (y2 - y1) // 2
                for X in range(x1, x2):
                    for Y in range(y1, y2):
                        if self.cache[X, Y] not in null + self.colorfilter:
                            self.work_order += ((X-x1-cx, Y-y1-cy, colors.index(self.cache[X, Y])),)
                print('Done.')
            elif option == "paste": #paste
                if self.work_order != ():
                    self.xy()
                    self.start = time.time()
                    for i in self.work_order:
                        if keyboard.is_pressed(stop_key):
                            print('Canceling job.')
                            return
                        self.emitsleep(i[0]+self.x, i[1]+self.y, i[2], [None])
        except:
            pass
        
    def tree(self, key):
        try:            
            self.x, self.y = self.xy()
            def tree_data():
                tree_order = ()
                x, y = self.x, self.y
                bark=colors.index(random.choice(trunks))
                for a in range(4):
                    tree_order+=([x,y-a,bark],)
                leaf=colors.index(random.choice(leaves))
                y -= a
                for b in range(3):
                    tree_order+=([x+b-1,y,leaf],)
                y -= 1
                for c in range(3):
                    tree_order+=([x+c-1,y,leaf],)
                y -= 1
                tree_order+=([x,y,leaf],)
                self.start = time.time()
                for Y in tree_order:
                    self.emitsleep(Y[0],Y[1], Y[2], leaves+trunks+null+ocean)
            tree_data()
            tx1, ty1 = self.x, self.y            
            while True:
                if not keyboard.is_pressed(key):
                    tx2, ty2 = self.xy()
                    if self.distance([tx1, ty1],[tx2, ty2]) > 8:
                        loop = True              
                    break
            if loop == True:
                while True:
                    if keyboard.is_pressed(stop_key):
                        return
                    self.x, self.y =  random.randint(tx1, tx2), random.randint(ty1, ty2)
                    tree_data()
        except:
            pass
    
    def circle_outline(self, key):
        try:
            self.xy()
            x2, y2 = self.x, self.y
            while True:
                if not keyboard.is_pressed(key):
                    self.xy()
                    x1, y1 = self.x, self.y
                    break
            r = int((((x2-x1)**2 + (y2-y1)**2))**0.5)
            x = r-1
            y = 0
            dx = 1
            dy = 1
            err = dx - (r << 1)
            self.color = self.return_color()
            def circxy():
                circ = [[x1 + x, y1 + y],[x1 + y, y1 + x],[x1 - y, y1 + x],[x1 - x, y1 + y],
                        [x1 - x, y1 - y],[x1 - y, y1 - x],[x1 + y, y1 - x],[x1 + x, y1 - y]]
                return circ
            self.start = time.time()
            print(f'Omega')
            while x >= y:
                if keyboard.is_pressed(stop_key):
                    print('Canceling...')
                    break
                for c in circxy():
                    self.emitsleep(c[0],c[1], self.color, [None])
                if err > 0:
                    x -= 1
                    dx += 2
                    err += dx - (r << 1)
                if err <= 0:
                    y += 1
                    err += dy
                    dy += 2
        except:
            pass
            
    def river_bend(self, key):#aim and fire a river into the distance
        try:
            river_thickness_fill_list = []
            rotations = [1,-1]
            rotation_cycle = cycle(rotations)
            def r():
                return next(rotation_cycle)
            start, end, control = (xy:=self.xy()),xy,xy
            control_stack = []
            while keyboard.is_pressed(key):
                self.xy()
                control_stack += [[self.x, self.y],]
            end = self.xy()
            control_average = []
            control_average += self.coordinate_list_average(control_stack)
            distance = self.distance(start, end) + self.distance(control_average, end)
            self.start=time.time()
            print(f'River Bend')
            for i in range(distance):
                if keyboard.is_pressed(stop_key):
                    print('Canceling...')
                    return
                t = i / distance
                if self.emitsleep((xfl:=(1-t)**2 * start[0] + (2 * t * (1-t) * control_average[0]) + (t**2 * end[0])), (yfl:=((1-t)**2 * start[1]) + (2 * t * (1-t) * control_average[1]) + (t**2 * end[1])), self.oceaneer(), null+ocean):
                    river_thickness_fill_list.append([xfl+r(),yfl])
                    river_thickness_fill_list.append([xfl+r(),yfl])
                    river_thickness_fill_list.append([xfl,yfl+r()])
                    river_thickness_fill_list.append([xfl,yfl+r()])
            random.shuffle(river_thickness_fill_list)
            self.start=time.time()
            while len(river_thickness_fill_list) > 0:
                if keyboard.is_pressed(stop_key):
                    return
                x, y = river_thickness_fill_list.pop()
                self.emitsleep(x,y,self.oceaneer(), null+ocean)
        except:
            pass
        
    def wyrvern(self, key):#auto tunneling river spirit
        try:
            control_group = []
            eyesight = 32
            start = self.xy()
            self.start=time.time()
            print(f'River Spirit')
            while True:             
                while not self.cache[(rx:=start[0] + random.randint(-eyesight, eyesight)),(ry:=start[1] +random.randint(-eyesight, eyesight+1))] in colors:
                    pass                
                control = rx, ry                
                while not self.cache[(rx1:=control[0]+random.randint(-eyesight, eyesight)),(ry1:=control[1]+random.randint(-eyesight, eyesight+1))] in colors:
                    pass 
                control2 = rx1, ry1                
                while not self.cache[(rx2:=control2[0]+random.randint(-eyesight, eyesight)),(ry2:=control2[1]+random.randint(-eyesight, eyesight+1))] in colors:
                    pass 
                control3 = rx2, ry2                
                while not self.cache[(rx3:=control3[0]+random.randint(-eyesight, eyesight)),(ry3:=control3[1]+random.randint(-eyesight, eyesight+1))] in colors:
                    pass 
                end = rx3, ry3                
                resolution = (self.distance(start, control) + self.distance(control, control2) + self.distance(control2, control3) + self.distance(control3, end))
                for i in range(int(resolution)):
                    if keyboard.is_pressed(stop_key):
                        print('Canceling...')
                        return
                    t = i / resolution
                    x = (1-t)**4 * start[0] + 4 * t * (1-t)**3 * control[0] + 6 * t**2 * (1-t)**2 * control2[0] + 4 * t**3 * (1-t) * control3[0] + t**4 * end[0]
                    y = (1-t)**4 * start[1] + 4 * t * (1-t)**3 * control[1] + 6 * t**2 * (1-t)**2 * control2[1] + 4 * t**3 * (1-t) * control3[1] + t**4 * end[1]
                    if self.emitsleep(int(x), int(y), self.oceaneer(), null + ocean + smoke + trunks + leaves):
                        pass
                    else:
                        try:
                            for a in range(-1,2):
                                for b in range(-1,2):
                                    if abs(a) != abs(b):
                                        if not self.emitsleep(x+a, y+b, self.cy_cols(colors.index(self.cache[x+a, y+b])), null + ocean + smoke + trunks + leaves):
                                            if not self.emitsleep(x-a, y+b, self.cy_cols(colors.index(self.cache[x-a, y+b])), null + ocean + smoke + trunks):
                                                if not self.emitsleep(x-a, y-b, self.cy_cols(colors.index(self.cache[x-a, y-b])), null + ocean + smoke):
                                                    if not self.emitsleep(x+a, y-b, self.cy_cols(colors.index(self.cache[x+a, y-b])), null + ocean):
                                                        start = x+a, y+b
                                                        break
                        except:
                            pass
                start = x, y
        except:
            pass

    def surging_waves(self, key):
        try:
            filters = ocean + leaves + trunks + smoke
            fill_list = []
            self.color = self.oceaneer()
            def locate():
                self.xy()
                fill_list.append([self.x, self.y])
            locate()
            self.start = time.time()
            print(f'Surging Waves')
            while len(fill_list) > 0:
                if keyboard.is_pressed(key):
                    locate()
                elif keyboard.is_pressed(stop_key):
                    print('Canceling...')
                    return
                x, y = fill_list.pop()
                if self.emitsleep(x, y, self.oceaneer(), filters):
                    self.color = self.oceaneer()
                    fill_list.append([x+1, y])
                    fill_list.append([x-1, y])
                    fill_list.append([x, y+1])
                    fill_list.append([x, y-1])
                    if (Ra:=random.randint(-1,1)) > (Rb:=random.randint(-1,1)):
                        fill_list.append([x+Ra, y])
                        fill_list.append([x, y-Rb])
                    elif Ra == Rb:
                        fill_list.append([x+1, y+1])
                        fill_list.append([x-1, y-1])
                        fill_list.append([x+1, y-1])
                        fill_list.append([x-1, y+1])
                    else:
                        fill_list.append([x-Ra, y])
                        fill_list.append([x, y+Rb])
        except:
            pass
        
    def mighty_wind(self, key):#bucket tool
        try:
            filters = [i for i in self.colorfilter]
            fill_list = []
            border_list = []
            self.color = self.return_color()
            border_color = self.color + r if self.color + (r := random.choice([-1,1])) in range(len(colors)) else self.color - r
            def locate():
                self.xy()
                fill_list.append([self.x, self.y])
            locate()
            execoptions = ['self.emitsleep(x+1,y,self.color, filters):fill_list.append([x+1,y])',
                           'self.emitsleep(x-1,y,self.color, filters):fill_list.append([x-1,y])',
                           'self.emitsleep(x,y+1,self.color, filters):fill_list.append([x,y+1])',
                           'self.emitsleep(x,y-1,self.color, filters):fill_list.append([x,y-1])']     
            self.start = time.time()
            print(f'Mighty Wind')
            while len(fill_list) > 0:
                if keyboard.is_pressed(key):
                    locate()
                elif keyboard.is_pressed('shift+o'):
                    self.borders = True if self.borders == False else False
                    print(f'Borders: {self.borders}')
                    time.sleep(speed*2)
                elif keyboard.is_pressed(stop_key):
                    print('Canceling...')
                    return
                x, y = fill_list.pop()
                random.shuffle(execoptions)
                for i in execoptions:
                    try:
                        self.color = colors.index(random.choice(self.colorfilter))
                    except:
                        pass
                    exec(f'if {i}')
                if self.cache[x+1, y] in null and self.cache[x, y] not in null:
                    border_list.append([x,y])
                if self.cache[x-1, y] in null and self.cache[x, y] not in null:
                    border_list.append([x,y])
                if self.cache[x, y+1] in null and self.cache[x, y] not in null:
                    border_list.append([x,y])
                if self.cache[x, y-1] in null and self.cache[x, y] not in null:
                    border_list.append([x,y])
            if self.borders == True:
                self.start = time.time()
                while len(border_list) > 0:
                    if keyboard.is_pressed(stop_key):
                        print('Canceling...')
                        return
                    x, y = border_list.pop() 
                    sio.emit('p', [x,y, border_color, 1])
                    time.sleep(speed - (self.start - time.time()))
                    self.start = time.time()
        except:
            pass
        
    #color replacer variant of bucket tool
    def mighty_wind_alt(self, key):#bucket tool
        try:
            fill_list = []
            border_list =  []
            color = self.return_color()
            oceanstuff = False
            border_color = self.color + r if self.color + (r := random.choice([-1,1])) in range(len(colors)) else self.color - r
            def locate():
                self.xy()
                fill_list.append([self.x, self.y])
            locate()
            filters = [i for i in colors if i != self.cache[self.x, self.y]]
            old_color = self.cache[self.x, self.y]
            execoptions = ['self.emitsleep(x+1,y,color if oceanstuff == False else self.oceaneer(), filters if oceanstuff == False else ocean + leaves + trunks):fill_list.append([x+1,y])',
                           'self.emitsleep(x-1,y,color if oceanstuff == False else self.oceaneer(), filters if oceanstuff == False else ocean + leaves + trunks):fill_list.append([x-1,y])',
                           'self.emitsleep(x,y+1,color if oceanstuff == False else self.oceaneer(), filters if oceanstuff == False else ocean + leaves + trunks):fill_list.append([x,y+1])',
                           'self.emitsleep(x,y-1,color if oceanstuff == False else self.oceaneer(), filters if oceanstuff == False else ocean + leaves + trunks):fill_list.append([x,y-1])']     
            self.start = time.time()
            print(f'Strong Wind')
            while len(fill_list) > 0:
                if keyboard.is_pressed(key):
                    locate()
                elif keyboard.is_pressed('w'):
                    oceanstuff = True if oceanstuff == False else False
                    time.sleep(speed*2)
                elif keyboard.is_pressed('shift+o'):
                    self.borders = True if self.borders == False else False
                    print(f'Borders: {self.borders}')
                    time.sleep(speed*2)
                elif keyboard.is_pressed(stop_key):
                    print('Canceling...')
                    return
                x, y = fill_list.pop()
                try:
                    cachepixel = self.cache[x, y]
                    random.shuffle(execoptions)
                    for i in execoptions:
                        try:
                            color = colors.index(random.choice(self.colorfilter))
                        except:
                            pass
                        exec(f'if {i}')
                    if oceanstuff == False:
                        if self.cache[x+1, y] not in [old_color] + [colors[self.color]]:
                            border_list.append([x,y])
                        if self.cache[x-1, y] not in [old_color] + [colors[self.color]]:
                            border_list.append([x,y])
                        if self.cache[x, y+1] not in [old_color] + [colors[self.color]]:
                            border_list.append([x,y])
                        if self.cache[x, y-1] not in [old_color] + [colors[self.color]]:
                            border_list.append([x,y])
                except:
                    pass
            if self.borders == True and oceanstuff == False:
                self.start = time.time()
                while len(border_list) > 0:
                    if keyboard.is_pressed(stop_key):
                        print('Canceling...')
                        return
                    x, y = border_list.pop() 
                    sio.emit('p', [x,y, border_color, 1])
                    time.sleep(speed - (self.start - time.time()))
                    self.start = time.time()
        except:
            pass
        
    def way_of_the_dragon(self, key): #creates lots of fire that spreads and turns to ashe
        try:
            flame = []
            ashe = []
            def locate():
                self.xy()
                flame.append([self.x, self.y])                
            locate()        
            self.start = time.time()
            print(f'Way of the Dragon')
            while len(flame) > 0:
                if keyboard.is_pressed(key):
                    locate()
                elif keyboard.is_pressed(stop_key):
                    print('Canceling...')
                    return            
                x, y = flame.pop()
                if self.emitsleep(x, y, colors.index(random.choice(fire)), ocean + smoke + fire + null):
                    if (Ra:=random.randint(-1,1)) > (Rb:=random.randint(-1,1)): #backrow                            
                        #knight, 8 possible moves
                        which_knight_move=random.randint(0,7)
                        if which_knight_move == 0:
                            flame.append([x+1, y-2])
                            ashe.append([x+1, y-2-random.randint(0, 9)])
                        elif which_knight_move == 1:    
                            flame.append([x-1, y-2])
                            ashe.append([x-1, y-2-random.randint(0, 9)])
                        elif which_knight_move == 2:
                            flame.append([x+2, y-1])
                            ashe.append([x+2, y-1-random.randint(0, 9)])
                        elif which_knight_move == 3:
                            flame.append([x+2, y+1])
                            ashe.append([x+2, y+1-random.randint(0, 9)])
                        elif which_knight_move == 4:
                            flame.append([x+1, y+2])
                            ashe.append([x+1, y+2-random.randint(0, 9)])
                        elif which_knight_move == 5:
                            flame.append([x-1, y+2])
                            ashe.append([x-1, y+2-random.randint(0, 9)])
                        elif which_knight_move == 6:
                            flame.append([x-2, y+1])
                            ashe.append([x-2, y+1-random.randint(0, 9)])
                        elif which_knight_move == 7:
                            flame.append([x-2, y-1])
                            ashe.append([x-2, y-1-random.randint(0, 9)])
                        
                        #bishop, choice of movements in diagonal directions in range of board size
                        which_bishop_move=random.randint(0,1)
                        if which_bishop_move == 0:
                            flame.append([x+(r1:=random.randint(-3, +4)), y+r1])
                            ashe.append([x+(r1:=random.randint(-3, +4)), y+r1-random.randint(0, 9)])
                        elif which_bishop_move == 1:
                            flame.append([x+(r2:=random.randint(-4, +3)), y+r2])
                            ashe.append([x+(r2:=random.randint(-4, +3)), y+r2-random.randint(0, 9)])

                        #rook, choice of movements in horizontal and vertical directions in range of board size
                        which_rook_move=random.randint(0,3)
                        if which_rook_move == 0:
                            flame.append([x+(r1:=random.randint(-3, +4)), y])
                            ashe.append([x+(r1:=random.randint(-3, +4)), y-random.randint(0, 9)])
                        elif which_rook_move == 1:
                            flame.append([x+(r2:=random.randint(-4, +3)), y])
                            ashe.append([x+(r2:=random.randint(-4, +3)), y-random.randint(0, 9)])
                        elif which_rook_move == 2:
                            flame.append([x, y+(r3:=random.randint(-3, +4))])
                            ashe.append([x, y+(r3:=random.randint(-3, +4))-random.randint(0, 9)])
                        elif which_rook_move == 3:
                            flame.append([x, y+(r4:=random.randint(-4, +3))])
                            ashe.append([x, y+(r4:=random.randint(-4, +3))-random.randint(0, 9)])

                        #queen, choice of movements in horizontal, vertical and diagonal directions in range of board size
                        which_queen_move=random.randint(0,7)
                        if which_queen_move == 0:
                            flame.append([x+(r1:=random.randint(-3, +4)), y+r1])
                            ashe.append([x+(r1:=random.randint(-3, +4)), y+r1-random.randint(0, 9)])
                        elif which_queen_move == 1:
                            flame.append([x+(r2:=random.randint(-4, +3)), y+r2])
                            ashe.append([x+(r2:=random.randint(-4, +3)), y+r2-random.randint(0, 9)])
                        elif which_queen_move == 2:
                            flame.append([x+(r3:=random.randint(-3, +4)), y])
                            ashe.append([x+(r3:=random.randint(-3, +4)), y-random.randint(0, 9)])
                        elif which_queen_move == 3:
                            flame.append([x+(r4:=random.randint(-4, +3)), y])
                            ashe.append([x+(r4:=random.randint(-4, +3)), y-random.randint(0, 9)])
                        elif which_queen_move == 4:
                            flame.append([x, y+(r5:=random.randint(-3, +4))])
                            ashe.append([x, y+(r5:=random.randint(-3, +4))-random.randint(0, 9)])
                        elif which_queen_move == 5:
                            flame.append([x, y+(r6:=random.randint(-4, +3))])
                            ashe.append([x, y+(r6:=random.randint(-4, +3))-random.randint(0, 9)])
                        elif which_queen_move == 6:
                            flame.append([x+(r7:=random.randint(-3, +4)), y-r7])
                            ashe.append([x+(r7:=random.randint(-3, +4)), y-r7-random.randint(0, 9)])
                        elif which_queen_move == 7:
                            flame.append([x+(r8:=random.randint(-4, +3)), y-r8])
                            ashe.append([x+(r8:=random.randint(-4, +3)), y-r8-random.randint(0, 9)])

                        #king, choice of movements in horizontal, vertical and diagonal directions in range of 1
                        which_king_move=random.randint(0,7)
                        if which_king_move == 0:
                            flame.append([x+1, y+1])
                            ashe.append([x+1, y+1-random.randint(0, 9)])
                        elif which_king_move == 1:
                            flame.append([x+1, y])
                            ashe.append([x+1, y-random.randint(0, 9)])
                        elif which_king_move == 2:
                            flame.append([x+1, y-1])
                            ashe.append([x+1, y-1-random.randint(0, 9)])
                        elif which_king_move == 3:
                            flame.append([x, y+1])
                            ashe.append([x, y+1-random.randint(0, 9)])
                        elif which_king_move == 4:
                            flame.append([x, y-1])
                            ashe.append([x, y-1-random.randint(0, 9)])
                        elif which_king_move == 5:
                            flame.append([x-1, y+1])
                            ashe.append([x-1, y+1-random.randint(0, 9)])
                        elif which_king_move == 6:
                            flame.append([x-1, y])
                            ashe.append([x-1, y-random.randint(0, 9)])
                        elif which_king_move == 7:
                            flame.append([x-1, y-1])
                            ashe.append([x-1, y-1-random.randint(0, 9)])

                        #Castling, King + Rook move
                        which_castling_move=random.randint(0,1) #Kingside and Queenside
                        if which_castling_move == 0: #Kingside
                            flame.append([x+Ra+Rb, y])
                            ashe.append([x+Ra+Rb, y-random.randint(0, 9)])
                        elif which_castling_move == 1: #Queenside
                            flame.append([x-Ra-Rb, y])
                            ashe.append([x-Ra-Rb, y-random.randint(0, 9)])
                        
                    else: #pawns
                        #pawn, 6 moves if we account for enemy side pawn moves, and En Passant
                        which_pawn_move=random.randint(0,1)
                        if random.random() > .5:
                            if random.random() > .5:
                                if random.random() > .5:
                                    flame.append([x-1, y-1])
                                    ashe.append([x-1, y-1-random.randint(0, 9)])
                                else:
                                    flame.append([x+1, y-1])
                                    ashe.append([x+1, y-1-random.randint(0, 9)])
                            else:
                                flame.append([x, y-1])
                                ashe.append([x, y-1-random.randint(0, 9)])                         
                        else:
                            if random.random() > .5:
                                if random.random() > .5:
                                    flame.append([x-1, y+1])
                                    ashe.append([x-1, y+1-random.randint(0, 9)])
                                else:
                                    flame.append([x+1, y+1])
                                    ashe.append([x+1, y+1-random.randint(0, 9)])
                            else:
                                flame.append([x, y+1])
                                ashe.append([x, y+1-random.randint(0, 9)])
                if random.random() > .9:
                    for i in ashe:
                        if self.primeCheck(ashe.index(i)) == "Prime":
                            ashe.pop()
                        i[0]+=random.randint(-1, +2)
                        i[1]+=random.randint(-1, +2)
                    while len(ashe) > 0:
                        if keyboard.is_pressed(stop_key):
                            print('Canceling...')
                            return            
                        fx, fy = ashe.pop()
                        self.emitsleep(fx, fy, colors.index(random.choice(smoke)), ocean + smoke + null)
                    if random.random() > .9:
                        random.shuffle(flame)
        except:
            pass
        
    def bamboo_shaft(self, key):
        try:
            self.color = self.return_color()
            start, end = (xy:=self.xy()),xy
            while keyboard.is_pressed(key):
                self.xy()
            end = self.xy()
            distance = self.distance(start, end)
            self.start=time.time()
            print(f'Bamboo Shaft')
            for i in range(distance):
                if keyboard.is_pressed(key):
                    self.color = random.choice([colors.index(i) for i in leaves])
                elif keyboard.is_pressed(stop_key):
                    print('Canceling...')
                    return
                t = i / distance
                self.emitsleep(int((1-t) * start[0] + t * end[0]), int((1-t) * start[1] + t * end[1]), self.color, null)
            print(f'You measure out {distance} {unit_measurement}.')
        except:
            pass
        
speed = 0.02 # default speed
default_speed = speed

susbot = SusBot()
for control in controls:
    print(control)
#end of the line, partner
