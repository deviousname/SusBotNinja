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

#options:
#Bot speed suggestions:
slow_speed = 0.04 # good for leaving on low energy botting all night
regular_speed = 0.02 # good speed for using the brush tools
max_speed = 0.016  # this is the max speed you should go before rate limiting occurs
# Rate limiting is when the server detects you pixeling too fast and auto nerfs your speed
# Warning: It's possible to go so fast your account gets permantly disabled.
# 
# Suggestion: Only ever do that on a test account you don't mind losing.

#--|###############|--# Bot global speed:
speed = regular_speed # Set speed here
#--|###############|--# Recommend: speed = regular_speed

chart = 7
unit_measurement = 'pixels'
stop_key = 'shift+d'
autologin = False

colors =[(255,255,255),(196,196,196),(136,136,136),(85,85,85),(34,34,34),
        (0,0,0),(0,102,0),(34,177,76),(2,190,1),(81,225,25),(148,224,68),
        (251,255,91),(229,217,0),(230,190,12),(229,149,0),(160,106,66),
        (153,83,13),(99,60,31),(107,0,0),(159,0,0),(229,0,0),(255,57,4),
        (187,79,0),(255,117,95),(255,196,159),(255,223,204),(255,167,209),
        (207,110,228),(236,8,236),(130,0,128),(81,0,255),(2,7,99),(0,0,234),
        (4,75,255),(101,131,207),(54,186,255),(0,131,199),(0,211,221),(69,255,200)]

paint = {"white":(255,255,255), "grey1":(196,196,196), "grey2":(136,136,136), "grey3":(85,85,85), "grey4":(34,34,34), "black":(0,0,0), "green1":(0,102,0), "green2":(34,177,76), "green3":(2,190,1),
          "green4":(81,225,25), "green5":(148,224,68), "yellow1":(251,255,91), "yellow2":(229,217,0), "yellow3":(230,190,12), "yellow4":(229,149,0), "brown1":(160,106,66), "brown2":(153,90,26), "brown3":(99,60,31),
          "red1":(107,0,0), "red2":(159,0,0), "red3":(229,0,0), "orange":(255,57,4), "brown4":(187,79,0), "peach1":(255,117,95), "peach2":(255,196,159), "peach3":(255,223,204), "pink1":(255,167,209),
          "pink2":(207,110,228), "pink3":(236,8,236), "pink4":(130,0,128), "purple":(81,0,255), "blue1":(2,7,99), "blue2":(0,0,234), "blue3":(4,75,255), "blue4":(101,131,207), "blue5":(54,186,255),
          "blue6":(0,131,199), "blue7":(0,211,221), "cyan":(69,255,200)
          }

paintnames = [i for i in paint.keys()]

null = [(204,204,204)]
ocean = [o for o in colors if colors.index(o) in range(30,38+1)]
fire = [f for f in colors if colors.index(f) in (11,12,13,14,20)]
smoke = [s for s in colors if colors.index(s) in range(2,5)]
leaves = [l for l in colors if colors.index(l) in range(6,10+1)]
trunks = [t for t in colors if colors.index(t) in range(15,17+1)]
sand = [sa for sa in colors if colors.index(sa) in (11,12,24,25)]

print('*~ SusBot -*= Ninja Edition ~ ~ ~ ~*')
class SusBot():
    ##################
    # Hotkey Section:          
    def hotkey_preload(self):
        # SET YOUR HOTKEYS HERE:
        
        # brushes
        self.firekey='a' # fire brush
        self.waterkey='w' # water brush
        self.fire_and_water_key='z' # water and fire brush

        # mining tools
        self.mine='e' # mining tool
        self.bigmine='shift+e' # big mining tool
        self.dump='q' # unmining tool
        self.bigdump='shift+q' # big unmining tool
        
        # fill tools
        self.windkey='shift+v' # large bucket fill tool
        self.breezekey='shift+x' # small bucket tool
        self.breezekey2='o' # small lake generator

        # shape tools
        self.linekey='v' # line tool
        self.piekey='s' # circle tool

        # extras
        self.fillborderskey ='['# fill borders toggle key
        self.keytree='r' # tree tool
        self.river_bend_key='d' # river bend tool
        
        self.copykey = 'f8' # copy a region by swiping right and down
        self.pastekey = 'f9' # paste the copied region at mouse location
        
        self.downspeed = 'shift+insert' # decrease bot speed
        self.upspeed = 'shift+delete' # increase bot speed
        
        # SET YOUR HOTKEY DESCRIPTIONS HERE:
        controls = ['',
            "Controls:",
            '',
            '# brushes',
            f'{self.firekey} # fire brush',
            f'{self.waterkey} # water brush',
            f'{self.fire_and_water_key} # water and fire brush',
            '',
            '# mining tools',
            f'{self.mine} # mining tool',
            f'{self.bigmine} # big mining tool',
            f'{self.dump} # reverse mining tool',
            f'{self.bigdump} # reverse big mining tool',
            '',
            '# fill tools',     
            f'{self.windkey} # large bucket fill tool',
            f'{self.breezekey} # small bucket tool',
            f'{self.breezekey2} # small lake generator',
            '',
            '# shape tools',    
            f'{self.linekey} # line tool',
            f'{self.piekey} # circle tool',
            '',
            '# extras',
            f'{self.fillborderskey} # fill borders toggle key',
            f'{self.keytree} # tree tool',
            f'{self.river_bend_key} # river bend tool'
            '',
            f'{self.copykey} # copy a region by swiping right and down',
            f'{self.pastekey} # paste the copied region at mouse location',
            '',
            f'{self.downspeed} # decrease bot speed',
            f'{self.upspeed} # increase bot speed',
            '',
            '# Equip your colors with the 0-9 keys and press ` or ~ to clear them out.',
            "# Copy doesn't copy equipped colors, and paste doesn't paste on equipped colors.",
            '',
            'stop key = {stop_key}',
            '',
            '# ~ ~ ~ ~ ~* ~* ~ ~*','']   
        for control in controls:
            print(control)
            
    def hotkeys(self):
        # ADD NEW HOTKEYS HERE:
        
        # brushes
        keyboard.add_hotkey(self.firekey,lambda:self.way_of_the_dragon(self.firekey)) # fire brush 
        keyboard.add_hotkey(self.waterkey,lambda:self.surging_waves(self.waterkey)) # water brush
        keyboard.add_hotkey(self.fire_and_water_key,lambda:self.fire_and_water(self.fire_and_water_key)) # water and fire brush

        # mining tools
        keyboard.add_hotkey(self.mine,lambda:self.mining_tool(self.mine)) # jackhammer tool, mines at a rate of {speed} {unit_measurement}s per second'
        keyboard.add_hotkey(self.bigmine,lambda:self.mining_tool(self.bigmine))
        keyboard.add_hotkey(self.dump,lambda:self.mining_tool(self.dump)) # reverse jackhammer tool, unmines at a rate of {speed} {unit_measurement}s per second' 
        keyboard.add_hotkey(self.bigdump,lambda:self.mining_tool(self.bigdump))
        
        # fill tools
        keyboard.add_hotkey(self.windkey,lambda:self.mighty_wind(self.windkey)) # large bucket fill tool
        keyboard.add_hotkey(self.breezekey,lambda:self.mighty_wind_alt(self.breezekey)) # small bucket tool
        keyboard.add_hotkey(self.breezekey2,lambda:self.gentle_breeze2(self.breezekey2)) # small lake generator

        # shape tools
        keyboard.add_hotkey(self.linekey,lambda:self.thick_line(self.linekey)) # line tool
        keyboard.add_hotkey(self.piekey,lambda:self.circle_outline(self.piekey)) # circle tool

        # extras
        keyboard.add_hotkey(self.fillborderskey,lambda:self.fillborderstoggle(self.fillborderskey)) # fill borders toggle key
        keyboard.add_hotkey(self.keytree,lambda:self.tree(self.keytree)) # tree tool
        keyboard.add_hotkey(self.river_bend_key,lambda:self.river_bend(self.river_bend_key)) # river bend tool
        
        keyboard.add_hotkey(self.copykey,lambda:self.copypaste('copy','f8')) # copy a region by swiping right and down
        keyboard.add_hotkey(self.pastekey,lambda:self.copypaste('paste','f9')) # paste the copied region at mouse location
        
        keyboard.add_hotkey(self.downspeed, lambda: self.change_speed('decrease')) # decrease bot speed
        keyboard.add_hotkey(self.upspeed, lambda: self.change_speed('increase')) # increase bot speed
        keyboard.on_press(self.onkeypress) # equips your colors to the 0-9 slots press ` or ~ to clear the filters
        
    #############################
    # Bot Initialization Section:    
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
        self.hotkey_preload()
        self.hotkeys()
        self.pn = 1
        self.emit_counter = 0
        self.tree_counter = 0
        self.z = -1
        self.color = random.randint(0, len(colors)-1)
        self.border_color = self.color + r if self.color + (r := random.choice([-1,1])) in range(len(colors)-1) else self.color - r
        self.colorfilter = [None, None, None, None, None, None, None, None, None, None]
        self.borders = False
        
    def load_map_into_cache(self):
        with open(f'{chart}.png', 'wb') as f:
            f.write(requests.get(f'https://pixelplace.io/canvas/{chart}.png?t={random.randint(9999,99999)}').content)
        self.image = PIL.Image.open(f'{chart}.png').convert('RGB')
        self.cache = self.image.load()
        
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
        
    def xy(self):
        try:
            self.x, self.y = make_tuple(driver.find_element(By.XPATH,'/html/body/div[3]/div[4]').text)
            return [self.x, self.y]
        except:
            pass       
                    
    def primeCheck(self, n):
        if n==1 or n==0 or (n % 2 == 0 and n > 2):
            return "Not prime"
        else:
            for i in range(3, int(n**(1/2))+1, 2):
                if n%i == 0:
                    return "Not prime"
            self.pn = n
            return "Prime"
        
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
        
    def zone(self, key):
        x1, y1 = self.xy()
        while True:
            if not keyboard.is_pressed(key):
                break
        x2, y2 = self.xy()
        return [x1, y1], [x2, y2]
        
    def cy_cols(self, a):
        a += 1
        if a > len(colors)-1:
            a = 0
        self.color = a
        return self.color
    
    def reverse_cy_cols(self, color):
        color -= 1
        if color < 0:
            color = len(colors)-1
        self.color = color
        return self.color
    
    def oceaneer(self, c):
        return len(colors) - 1 - random.randint((ln:=len(ocean))-ln, ln)
        
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

    def ifsioemit(self, x, y, color):
        if self.cache[x,y] not in [colors[color]] + null + self.colorfilter:
            sio.emit('p',[x, y, color, 1])
            return True
        
    def emit_block_sleep(self, block_list, filters):
        if len(block_list) > 32:
            pass
        else:
            for i in block_list:
                x, y, color = i                  
                if self.ifsioemit(x, y, color):
                    self.emit_counter += 1
            time.sleep(speed * self.emit_counter)
            self.start = time.time()
            self.emit_counter = 0  
        
    def getcurcolorhotkey(self, col):
        try:
            self.colorfilter[col-1] = colors[self.get_color_index()]
            print(f'Equipped {self.colorfilter[col-1]} to slot {col}')
            return
        except Exception as e:
            print(e)
            pass
        
    def removefilters(self):
        try:
            self.colorfilter[0:] = None, None, None, None, None, None, None, None, None, None
            print("Filters dequipped.")
        except Exception as e:
            print(e)
            pass
        
    def onkeypress(self, event):
        try:
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
        except Exception as e:
            print(e)
            pass
            
    def change_speed(self, opt): #works good
        global speed
        try:
            if opt == 'decrease':
                speed += 0.001
                speed = float('%.3f'%speed)
                print("Speed:",speed)
            elif opt == 'increase':
                speed -= 0.001
                speed = float('%.3f'%speed)
                print("Speed:",speed)
            if speed < 0.015:
                print(f"Going too fast now, defaulting to {regular_speed} to prevent perma ban.")
                speed = regular_speed
        except Exception as e:
            print(e)
            pass
            
    ###################
    # Gameplay Section-
    # Copy Paster, works good, needs a save/load system still
    def copypaste(self, option, key):
        try:
            if option == "copy":
                self.xy()
                x1, y1 = self.x, self.y
                while True:
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
            elif option == "paste":
                if self.work_order != ():
                    self.xy()
                    self.start = time.time()
                    for i in self.work_order:
                        if keyboard.is_pressed(stop_key):
                            print('Canceling job.')
                            return
                        self.emitsleep(i[0]+self.x, i[1]+self.y, i[2], [None])
        except Exception as e:
            print(e)
            pass
        
    # Fire Brush, works good
    # hold the hotkey and spread fire
    # it plays a minigame until is burns out
    # see how big you can spread the fire
    # based on Chess move logic to move
    def way_of_the_dragon(self, key):
        try:
            flame = [] 
            def locate():
                flame.append(self.xy())        
            locate()        
            ashe = []
            def nap():
                try:
                    time.sleep(speed -(self.start - time.time()))
                    self.start = time.time()
                except:
                    pass
            def move(here):
                a, b = here
                flame.append([a, b])
                if self.cache[a+random.randint(-1,1), b+random.randint(-1,1)] in trunks + leaves + [(255,255,255)]:
                    flame.append([a+(fx:=random.randint(-1,1)), b+(fy:=random.randint(-1,1))])
                    ashe.append([a+random.randint(-2,2), b-random.randint(-1,self.pn % 10)])
                    if self.cache[a+fx+fy, b-int(fy*fx)] not in null + ocean + sand:
                        flame.append([a+fx+fy, b-int(fy*fx)])
                        ashe.append([a+random.randint(-2,2), b-random.randint(-1,self.pn % 10)])
                        if self.cache[a-fx-fy, b-int(fy*fx) - 1] not in null + ocean + sand:
                            flame.append([a-fx-fy, b-int(fy*fx) - 1])
                if self.cache[a, b] in ocean + sand:
                    if self.ifsioemit(a+(ar:=random.choice((-1,1))), b - (br:=random.randint(1, self.pn % 10)), colors.index(random.choice(ocean))):
                        nap()
                        flame.append([a+random.randint(-1,1), b+random.randint(-1,1)])
                    if self.ifsioemit(a, b, colors.index(random.choice(sand+ocean+smoke))):
                        nap()
                        try:
                            if self.ifsioemit(a+ar+random.randint(-1,1), b+br+random.randint(-1,1), self.cy_cols(colors.index(self.cache[a+ar+random.randint(-1,1), b+br+random.randint(-1,1)]))):
                                nap()
                        except:
                            pass
                        try:
                            if self.ifsioemit(a-ar+random.randint(-1,1), b+br+random.randint(-1,1), self.cy_cols(colors.index(self.cache[a+ar+random.randint(-1,1), b+br+random.randint(-1,1)]))):
                                nap()
                                ashe.append([a+random.randint(-2,2), b-random.randint(-1,self.pn % 10)])
                        except:
                            pass
                    if self.ifsioemit(a+ar, b-br, colors.index(random.choice(fire+smoke))):
                        nap()
                        flame.append([a+random.randint(-1,1), b+random.randint(-1,1)])
                    if self.ifsioemit(a+ar+random.randint(-1,1), b+br+random.randint(-1,1), colors.index(random.choice(fire+smoke))):
                        sio.emit('p', [a+ar+random.randint(-1,1), b+br+random.randint(-1,1), self.cy_cols(colors.index(self.cache[a+ar+random.randint(-1,1), b+br+random.randint(-1,1)]))])                        
                        nap()
                        ashe.append([a+random.randint(-2,2), b-random.randint(-1,self.pn % 10)])
                ashe.append([a, b])
            move([self.x, self.y])        
            def move_sets():
                knight_moves = [[x+1, y-2], [x-1, y-2], [x+2, y-1], [x+2, y+1], [x+1, y+2], [x-1, y+2], [x-2, y+1], [x-2, y-1]]    
                bishop_moves = [[x+(b1:=random.randint(-3, +4)), y+b1], [x+(b2:=random.randint(-4, +3)), y+b2]]    
                rook_moves = [[x+random.randint(-3, +4), y], [x, y+random.randint(-3, +4)]]    
                queen_moves = bishop_moves + rook_moves    
                king_moves = [[x+1, y],[x-1, y],[x, y+1],[x, y-1],[x+1, y+1],[x-1, y-1],[x+1, y-1],[x-1, y+1]]
                pawn_moves = [[x, y+1], [x, y-1], [x-1, y+1], [x-1, y-1], [x, y+2], [x, y-2]]
                return knight_moves + bishop_moves + rook_moves + queen_moves + king_moves + pawn_moves        
            self.start = time.time()
            print(f'Fire Brush')
            while len(flame) > 0:
                if keyboard.is_pressed(key):
                    locate()
                elif keyboard.is_pressed(stop_key):
                    print('Canceling...')
                    return
                x, y = flame.pop()
                if self.emitsleep(x, y, colors.index(random.choice(fire)), [None]):
                    move(random.choice(move_sets()))
                for i in ashe:
                    if self.primeCheck(ashe.index(i)) == "Prime":
                        ashe.pop()
                    i[0]+=random.randint(-self.pn, +self.pn)
                    i[1]+=random.randint(-1, +self.pn)
                while len(ashe) > 0:
                    if keyboard.is_pressed(stop_key):
                        print('Canceling...')
                        return            
                    hi, fi = ashe.pop()
                    self.emitsleep(hi, fi, colors.index(random.choice(smoke)), trunks)
                if (rand := random.random()) > self.pn / lf if (lf := len(flame)) != 0 else self.pn:
                    random.shuffle(flame)
        except Exception as e:
            print(e)
            pass
        
    # Water Brush, works good
    # self.surging_waves(hotkey) works pretty good, you can hold the hotkey and spread circles of water that fill like bubbles
    def surging_waves(self, key): #creates lots of water that spreads and evaporates
        try:
            water = []
            def locate():
                water.append(self.xy())        
            locate()
            def nap():
                try:
                    time.sleep(speed -(self.start - time.time()))
                    self.start = time.time()
                except:
                    pass
            def move(here):
                a, b = here
                water.append([a, b])
                if self.cache[a+random.randint(-1,1), b+random.randint(-1,1)] in ocean + [(0,0,0)]:
                    water.append([a+random.randint(-1,1), b+random.randint(-1,1)])
                if self.cache[a, b] in fire:
                    if self.ifsioemit(a+(ar:=random.choice((-1,1))), b - (br:=random.randint(1, self.pn % 10)), colors.index(random.choice(fire))):
                        nap()
                    if self.ifsioemit(a, b, colors.index(random.choice(sand+ocean+smoke+fire))):
                        nap()
                    if self.ifsioemit(a+ar, b-br, colors.index(random.choice(smoke))):
                        nap()
                    if self.ifsioemit(a+ar+random.randint(-1,1), b+br+random.randint(-1,1), colors.index(random.choice(smoke))):
                        nap()
            move([self.x, self.y])        
            def move_sets():
                knight_moves = [[x+1, y-2], [x-1, y-2], [x+2, y-1], [x+2, y+1], [x+1, y+2], [x-1, y+2], [x-2, y+1], [x-2, y-1]]    
                bishop_moves = [[x+(b1:=random.randint(-3, +4)), y+b1], [x+(b2:=random.randint(-4, +3)), y+b2]]    
                rook_moves = [[x+random.randint(-3, +4), y], [x, y+random.randint(-3, +4)]]    
                queen_moves = bishop_moves + rook_moves    
                king_moves = [[x+1, y],[x-1, y],[x, y+1],[x, y-1],[x+1, y+1],[x-1, y-1],[x+1, y-1],[x-1, y+1]]
                pawn_moves = [[x, y+1], [x, y-1], [x-1, y+1], [x-1, y-1], [x, y+2], [x, y-2]]
                return knight_moves + bishop_moves + rook_moves + queen_moves + king_moves + pawn_moves        
            self.start = time.time()
            print(f'Water Brush')
            while len(water) > 0:
                if keyboard.is_pressed(key):
                    locate()
                elif keyboard.is_pressed(stop_key):
                    print('Canceling...')
                    return
                x, y = water.pop()
                if self.emitsleep(x, y, colors.index(random.choice(ocean)), [None]):
                    move(random.choice(move_sets()))                
                if (rand := random.random()) > self.pn / lw if (lw := len(water)) != 0 else self.pn:
                    random.shuffle(water)
        except Exception as e:
            print(e)
            pass
        
    # Fire and Water Brush, works good, can still be improved of course
    def fire_and_water(self, key):
        try:
            water = []
            flame = []
            def locate():
                flame.append(self.xy())
                water.append(self.xy()) 
            locate()        
            ashe = []
            def nap():
                try:
                    time.sleep(speed -(self.start - time.time()))
                    self.start = time.time()
                except:
                    pass
            def move_flame(here):
                a, b = here
                flame.append([a, b])
                if self.cache[a+random.randint(-1,1), b+random.randint(-1,1)] in trunks + leaves + [(255,255,255)]:
                    flame.append([a+random.randint(-1,1), b+random.randint(-1,1)])
                    ashe.append([a+random.randint(-2,2), b-random.randint(-1,self.pn % 10)])
                if self.cache[a, b] in ocean + sand:
                    if self.ifsioemit(a+(ar:=random.choice((-1,1))), b - (br:=random.randint(1, self.pn % 10)), colors.index(random.choice(ocean))):
                        nap()
                        flame.append([a+random.randint(-1,1), b+random.randint(-1,1)])
                    if self.ifsioemit(a, b, colors.index(random.choice(sand+ocean+smoke))):
                        nap()
                        ashe.append([a+random.randint(-2,2), b-random.randint(-1,self.pn % 10)])
                    if self.ifsioemit(a+ar, b-br, colors.index(random.choice(fire+smoke))):
                        nap()
                        flame.append([a+random.randint(-1,1), b+random.randint(-1,1)])
                    if self.ifsioemit(a+ar+random.randint(-1,1), b+br+random.randint(-1,1), colors.index(random.choice(fire+smoke))):
                        nap()
                        ashe.append([a+random.randint(-2,2), b-random.randint(-1,self.pn % 10)])
                ashe.append([a, b])
            move_flame([self.x, self.y])
            def move_water(here):
                a, b = here
                water.append([a, b])
                if self.cache[a+random.randint(-1,1), b+random.randint(-1,1)] in ocean + [(0,0,0)]:
                    water.append([a+random.randint(-1,1), b+random.randint(-1,1)])
                if self.cache[a, b] in fire:
                    if self.ifsioemit(a+(ar:=random.choice((-1,1))), b - (br:=random.randint(1, self.pn % 10)), colors.index(random.choice(fire))):
                        nap()
                    if self.ifsioemit(a, b, colors.index(random.choice(sand+ocean+smoke+fire))):
                        nap()
                    if self.ifsioemit(a+ar, b-br, colors.index(random.choice(smoke))):
                        nap()
                    if self.ifsioemit(a+ar+random.randint(-1,1), b+br+random.randint(-1,1), colors.index(random.choice(smoke))):
                        nap()
            move_water([self.x, self.y])        
            def move_sets():
                knight_moves = [[x+1, y-2], [x-1, y-2], [x+2, y-1], [x+2, y+1], [x+1, y+2], [x-1, y+2], [x-2, y+1], [x-2, y-1]]    
                bishop_moves = [[x+(b1:=random.randint(-3, +4)), y+b1], [x+(b2:=random.randint(-4, +3)), y+b2]]    
                rook_moves = [[x+random.randint(-3, +4), y], [x, y+random.randint(-3, +4)]]    
                queen_moves = bishop_moves + rook_moves    
                king_moves = [[x+1, y],[x-1, y],[x, y+1],[x, y-1],[x+1, y+1],[x-1, y-1],[x+1, y-1],[x-1, y+1]]
                pawn_moves = [[x, y+1], [x, y-1], [x-1, y+1], [x-1, y-1], [x, y+2], [x, y-2]]
                return knight_moves + bishop_moves + rook_moves + queen_moves + king_moves + pawn_moves        
            self.start = time.time()
            print(f'Fire and Water Brush')
            while len(water) > 0 or len(flame) > 0:
                if keyboard.is_pressed(key):
                    locate()
                elif keyboard.is_pressed(stop_key):
                    print('Canceling...')
                    return
                if len(water) > 0:
                    x, y = water.pop()
                    if self.emitsleep(x, y, colors.index(random.choice(ocean)), smoke + trunks):
                        move_water(random.choice(move_sets()))                
                    if (rand := random.random()) > self.pn / lw if (lw := len(water)) != 0 else self.pn:
                        random.shuffle(water)
                counter = 0
                if len(flame) > 0 and len(flame) < len(colors):
                    counter += 1
                    x, y = flame.pop()
                    if self.cache[x, y] not in  ocean + sand + null:
                        sio.emit('p', [x, y, colors.index(random.choice(fire)), 1])
                        time.sleep((speed * counter) - (self.start - time.time()))
                        self.start = time.time()
                        move_flame(random.choice(move_sets()))                
                    for i in ashe:
                        if self.primeCheck(ashe.index(i)) == "Prime":
                            ashe.pop()
                        i[0]+=random.randint(-self.pn, +self.pn)
                        i[1]+=random.randint(-1, +self.pn)
                    while len(ashe) > 0:
                        if keyboard.is_pressed(stop_key):
                            print('Canceling...')
                            return            
                        hi, fi = ashe.pop()
                        if self.cache[hi, fi] not in null + sand + leaves:
                            sio.emit('p',[hi, fi, colors.index(random.choice(smoke)), 1])
                            time.sleep(speed - (self.start - time.time()))
                            self.start = time.time()
                    if (rand := random.random()) > self.pn / lf if (lf := len(flame)) != 0 else self.pn:
                        random.shuffle(flame)
                else:
                    counter = 0
        except Exception as e:
            print(e)
            pass
        
    # Circle tool, works good
    def circle_outline(self, key):
        try:
            start, end = self.zone(key)
            x2, y2 = start
            x1, y1 = end
            r = int((((x2-x1)**2 + (y2-y1)**2))**0.5)
            x = r-1
            y = 0
            dx = 1
            dy = 1
            err = dx - (r << 1)
            color = self.return_color()
            def circxy():
                circ = [[x1 + x, y1 + y],[x1 + y, y1 + x],[x1 - y, y1 + x],[x1 - x, y1 + y],
                        [x1 - x, y1 - y],[x1 - y, y1 - x],[x1 + y, y1 - x],[x1 + x, y1 - y]]
                return circ
            self.start = time.time()
            print(f'Drawing a circle.')
            while x >= y:
                if keyboard.is_pressed(stop_key):
                    print('Canceling...')
                    break
                for c in circxy():
                    self.emitsleep(c[0],c[1], color, [None])
                if err > 0:
                    x -= 1
                    dx += 2
                    err += dx - (r << 1)
                if err <= 0:
                    y += 1
                    err += dy
                    dy += 2
        except Exception as e:
            print(e)
            pass

    # toggle borders on or off for the fill tool, works good
    def fillborderstoggle(self, key):
        self.border_color = self.return_color()
        self.borders = True if self.borders == False else False
        print('borders on' if self.borders == True else 'borders off')
        print(f'{paintnames[self.border_color]}')
        time.sleep(speed*3)
        
    # Mining Tool, works good
    def mining_tool(self, key):
        self.start = time.time()
        try:
            x, y = self.xy()
            if key == self.bigmine:
                large_bit=[[x-1,y-2, self.cy_cols(colors.index(self.cache[x-1,y-2]))],
                           [x+1,y-2, self.cy_cols(colors.index(self.cache[x+1,y-2]))],
                           [x-2,y-1, self.cy_cols(colors.index(self.cache[x-2,y-1]))],
                           [x-1,y-1, self.cy_cols(colors.index(self.cache[x-1,y-1]))],
                           [x,y-1, self.cy_cols(colors.index(self.cache[x,y-1]))],
                           [x+1,y-1, self.cy_cols(colors.index(self.cache[x+1,y-1]))],
                           [x+2,y-1, self.cy_cols(colors.index(self.cache[x+2,y-1]))],
                           [x-2,y, self.cy_cols(colors.index(self.cache[x-2,y]))],
                           [x-1,y, self.cy_cols(colors.index(self.cache[x-1,y]))],
                           [x,y, self.cy_cols(colors.index(self.cache[x,y]))],
                           [x+1,y, self.cy_cols(colors.index(self.cache[x+1,y]))],
                           [x+2,y, self.cy_cols(colors.index(self.cache[x+2,y]))],
                           [x-1,y+1, self.cy_cols(colors.index(self.cache[x-1,y+1]))],
                           [x,y+1, self.cy_cols(colors.index(self.cache[x,y+1]))],
                           [x+1,y+1, self.cy_cols(colors.index(self.cache[x+1,y+1]))],
                           [x,y+2, self.cy_cols(colors.index(self.cache[x,y+2]))],]
                self.emit_block_sleep(large_bit, [None])
            elif key == self.bigdump:
                large_bit_reverse=[[x-1,y-2, self.reverse_cy_cols(colors.index(self.cache[x-1,y-2]))],
                           [x+1,y-2, self.reverse_cy_cols(colors.index(self.cache[x+1,y-2]))],
                           [x-2,y-1, self.reverse_cy_cols(colors.index(self.cache[x-2,y-1]))],
                           [x-1,y-1, self.reverse_cy_cols(colors.index(self.cache[x-1,y-1]))],
                           [x,y-1, self.reverse_cy_cols(colors.index(self.cache[x,y-1]))],
                           [x+1,y-1, self.reverse_cy_cols(colors.index(self.cache[x+1,y-1]))],
                           [x+2,y-1, self.reverse_cy_cols(colors.index(self.cache[x+2,y-1]))],
                           [x-2,y, self.reverse_cy_cols(colors.index(self.cache[x-2,y]))],
                           [x-1,y, self.reverse_cy_cols(colors.index(self.cache[x-1,y]))],
                           [x,y, self.reverse_cy_cols(colors.index(self.cache[x,y]))],
                           [x+1,y, self.reverse_cy_cols(colors.index(self.cache[x+1,y]))],
                           [x+2,y, self.reverse_cy_cols(colors.index(self.cache[x+2,y]))],
                           [x-1,y+1, self.reverse_cy_cols(colors.index(self.cache[x-1,y+1]))],
                           [x,y+1, self.reverse_cy_cols(colors.index(self.cache[x,y+1]))],
                           [x+1,y+1, self.reverse_cy_cols(colors.index(self.cache[x+1,y+1]))],
                           [x,y+2, self.reverse_cy_cols(colors.index(self.cache[x,y+2]))],]
                self.emit_block_sleep(large_bit_reverse, [None])
            elif key == self.mine:
                small_bit= [[x-1,y-1,self.cy_cols(colors.index(self.cache[x-1,y-1]))],
                            [x+1,y-1,self.cy_cols(colors.index(self.cache[x+1,y-1]))],
                            [x-1,y,self.cy_cols(colors.index(self.cache[x-1,y]))],
                            [x,y,self.cy_cols(colors.index(self.cache[x,y]))],
                            [x+1,y,self.cy_cols(colors.index(self.cache[x+1,y]))],
                            [x,y+1,self.cy_cols(colors.index(self.cache[x,y+1]))]]
                self.emit_block_sleep(small_bit, [None])
            elif key == self.dump:
                small_bit_reverse=[[x-1,y-1,self.reverse_cy_cols(colors.index(self.cache[x-1,y-1]))],
                            [x+1,y-1,self.reverse_cy_cols(colors.index(self.cache[x+1,y-1]))],
                            [x-1,y,self.reverse_cy_cols(colors.index(self.cache[x-1,y]))],
                            [x,y,self.reverse_cy_cols(colors.index(self.cache[x,y]))],
                            [x+1,y,self.reverse_cy_cols(colors.index(self.cache[x+1,y]))],
                            [x,y+1,self.reverse_cy_cols(colors.index(self.cache[x,y+1]))]]
                self.emit_block_sleep(small_bit_reverse, [None])  
        except:
            pass
        
    #Bucket tool, works good
    def mighty_wind(self, key):
        try:
            self.start = time.time()
            oceanstuff = False
            filters = [i for i in self.colorfilter]
            fill_list = []
            border_list = []
            self.color = self.return_color()
            def locate():
                self.xy()
                fill_list.append([self.x, self.y])
            locate()
            execoptions = ['self.emitsleep(x+1,y,self.color if oceanstuff == False else self.oceaneer(color), filters if oceanstuff == False else ocean + leaves + trunks + smoke):fill_list.append([x+1,y])',
                           'self.emitsleep(x-1,y,self.color if oceanstuff == False else self.oceaneer(color), filters if oceanstuff == False else ocean + leaves + trunks + smoke):fill_list.append([x-1,y])',
                           'self.emitsleep(x,y+1,self.color if oceanstuff == False else self.oceaneer(color), filters if oceanstuff == False else ocean + leaves + trunks + smoke):fill_list.append([x,y+1])',
                           'self.emitsleep(x,y-1,self.color if oceanstuff == False else self.oceaneer(color), filters if oceanstuff == False else ocean + leaves + trunks + smoke):fill_list.append([x,y-1])']
            print(f'Mighty Wind')
            while len(fill_list) > 0:
                if keyboard.is_pressed(key):
                    locate()
                elif keyboard.is_pressed('w'):
                    oceanstuff = True if oceanstuff == False else False
                    time.sleep(speed*3)
                elif keyboard.is_pressed(stop_key):
                    print('Canceling...')
                    return
                elif keyboard.is_pressed(self.fillborderskey):
                    self.fillborderstoggle(key)
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
                    elif keyboard.is_pressed(self.fillborderskey):
                        self.fillborderstoggle(key)
                    x, y = border_list.pop() 
                    sio.emit('p', [x,y, self.border_color, 1])
                    time.sleep(speed - (self.start - time.time()))
                    self.start = time.time()
        except:
            pass
                
    # Small bucket tool, works good
    def mighty_wind_alt(self, key):
        try:
            fill_list = []
            border_list =  []
            color = self.return_color()
            oceanstuff = False
            def locate():
                self.xy()
                fill_list.append([self.x, self.y])
            locate()
            filters = [i for i in colors if i != self.cache[self.x, self.y]]
            old_color = self.cache[self.x, self.y]
            execoptions = ['self.emitsleep(x+1,y,color if oceanstuff == False else self.oceaneer(color), filters if oceanstuff == False else ocean + leaves + trunks + smoke):fill_list.append([x+1,y])',
                           'self.emitsleep(x-1,y,color if oceanstuff == False else self.oceaneer(color), filters if oceanstuff == False else ocean + leaves + trunks + smoke):fill_list.append([x-1,y])',
                           'self.emitsleep(x,y+1,color if oceanstuff == False else self.oceaneer(color), filters if oceanstuff == False else ocean + leaves + trunks + smoke):fill_list.append([x,y+1])',
                           'self.emitsleep(x,y-1,color if oceanstuff == False else self.oceaneer(color), filters if oceanstuff == False else ocean + leaves + trunks + smoke):fill_list.append([x,y-1])']     
            self.start = time.time()
            print(f'Wind')
            while len(fill_list) > 0:
                if keyboard.is_pressed(key):
                    locate()
                elif keyboard.is_pressed('w'):
                    oceanstuff = True if oceanstuff == False else False
                    time.sleep(speed*3)
                elif keyboard.is_pressed(stop_key):
                    print('Canceling...')
                    return
                elif keyboard.is_pressed(self.fillborderskey):
                    self.fillborderstoggle(key)
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
            if self.borders == True:
                self.start = time.time()
                while len(border_list) > 0:
                    if keyboard.is_pressed(stop_key):
                        print('Canceling...')
                        return
                    elif keyboard.is_pressed(self.fillborderskey):
                        self.fillborderstoggle(key)
                    x, y = border_list.pop() 
                    sio.emit('p', [x,y, self.border_color, 1])
                    time.sleep(speed - (self.start - time.time()))
                    self.start = time.time()
        except:
            pass

    # Line tool, works good
    def thick_line(self, key):
        color=self.return_color()
        try:
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
                self.emitsleep(x3, y3, color, [])
                self.emitsleep(x3+1, y3, color, [])
                self.emitsleep(x3, y3+1, color, [])
                self.emitsleep(x3+1, y3+1, color, [])
            print(f'Drew a {length} {unit_measurement} line.')
        except Exception as e:
            print(e)
            pass
        
    # Tree tool, needs fine tuning, works pretty good
    def tree(self, key):
        self.start = time.time()
        try:
            self.primegrowth = self.primegrowth
        except:
            self.primegrowth = 1
            self.primegrowth += 1
            pass
        try:            
            self.x, self.y = self.xy()
            def tree_data():
                self.z = -self.z
                tree_order = ()
                x, y = self.x, self.y
                if self.primeCheck(self.tree_counter) == "Prime":                    
                    self.primegrowth = self.pn % 10
                    tree_order+=([x-self.z,y+1,colors.index(random.choice(trunks))],)
                    tree_order+=([x+self.z,y+2,colors.index(random.choice(trunks))],)
                shadebark = random.choice((16,17))
                for a in range(int(self.primegrowth * float(f"1.{self.primegrowth}"))):
                    tree_order+=([x+self.z,y-a,colors.index(random.choice(trunks))],)
                    tree_order+=([x-self.z,y-a,colors.index(random.choice(trunks))],)
                    tree_order+=([x,y-a,shadebark],)
                    if random.random() >  1-(1 /self.primegrowth):
                        rchoice = random.choice((6,7))
                        for special_y in range(random.randint(0, self.primegrowth//2)):
                            tree_order+=([x+special_y+a+self.z,y+special_y,rchoice],)
                            if random.random() >  1-(1 /self.primegrowth):
                                leaf = random.choice((8,9))
                                tree_order+=([x+special_y+a+self.z-1,y+special_y-1+self.z,leaf],)
                                self.z = -self.z
                y -= a
                leaf=colors.index(random.choice(leaves))
                for b in range(-(self.primegrowth-1)+3, (self.primegrowth-1)+3):
                    tree_order+=([x+self.z+b-1,y,leaf],)
                    if random.random() >  1-(1 /self.primegrowth):
                        rchoice = random.choice((6,7))
                        for special_y in range(random.randint(0, self.primegrowth-1)):
                            tree_order+=([x+b+self.z-1,y+special_y,rchoice],)
                tree_order+=([x+self.z, y, colors.index(random.choice(trunks))],)
                self.z = -self.z
                y -= 1
                leaf=colors.index(random.choice(leaves))
                for c in range(-(self.primegrowth-2)+3, (self.primegrowth-2)+3):
                    tree_order+=([x+self.z+c-1,y,leaf],)
                    if random.random() >  1-(1 /self.primegrowth):
                        for special_y in range(random.randint(0, self.primegrowth-1)):
                            tree_order+=([x+c+self.z+1,y+special_y,random.choice((8,9))],)
                self.z = -self.z
                y -= 1
                if self.primeCheck(self.tree_counter) == "Prime":
                    for c in range(-3, 3):
                        tree_order+=([x+self.z+c-1,y,colors.index(random.choice(leaves))],)
                y -= 1
                tree_order+=([x+self.z,y,colors.index(random.choice(leaves))],)
                if self.cache[self.x, self.y] not in ocean + trunks + leaves + smoke + null + fire + self.colorfilter:
                    for Y in tree_order:
                        sio.emit('p',[Y[0],Y[1], Y[2], 1])
                        try:
                            time.sleep(speed - (self.start - time.time()))
                            self.start = time.time()
                        except:
                            time.sleep(speed)
                            self.start = time.time()
                            pass
                    self.tree_counter+=1                    
            tree_data()
            tx1, ty1 = self.x, self.y       
            while True:
                if not keyboard.is_pressed(key):
                    tx2, ty2 = self.xy()
                    tree_data()
                    if self.distance([tx1, ty1],[tx2, ty2]) > 16:
                        loop = True
                    else:
                        loop = False
                    break
            if loop == True:
                print('Planting Forest.')
                while True:
                    self.x, self.y =  random.randint(tx1, tx2), random.randint(ty1, ty2)
                    tree_data()
                    if keyboard.is_pressed(stop_key):
                        print(f'Planted {self.tree_counter} trees so far. {f"Tree {self.pn} was prime."}')
                        return
        except Exception as e:
            print(e)
            pass        
        
    # Small Bucket tool2, works good
    def gentle_breeze2(self, key):
        try:
            locs = []
            def locate():
                locs.append(self.xy())
            locate()
            print(f'The ocean swells...')
            while len(locs) > 0:
                try:
                    if keyboard.is_pressed(key):
                        locate()
                    elif keyboard.is_pressed(stop_key):
                        print('Canceling...')
                        return
                    x, y = locs.pop(locs.index(random.choice(locs)))
                    ic = 0
                    self.start = time.time()
                    for i in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                        x0, y0 = i
                        try:
                            if keyboard.is_pressed(key):
                                locate()
                            elif keyboard.is_pressed(stop_key):
                                print(f'The ocean sways...')
                                return
                            if self.cache[x0, y0] not in null + self.colorfilter + ocean: 
                                sio.emit('p',[x0, y0, self.oceaneer(self.color), 1])
                                locs.append([x0, y0])
                                ic+=1
                        except Exception as e:
                            print(e)
                            pass
                    time.sleep(speed*ic - (self.start - time.time()))
                    self.start = time.time()
                except:
                    pass
        except Exception as e:
            print(e)
            pass
        
    # River Bend tool, works good
    def river_bend(self, key):
        try:
            color=self.return_color()
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
                if self.emitsleep((xfl:=(1-t)**2 * start[0] + (2 * t * (1-t) * control_average[0]) + (t**2 * end[0])), (yfl:=((1-t)**2 * start[1]) + (2 * t * (1-t) * control_average[1]) + (t**2 * end[1])), self.oceaneer(color), [None]):
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
                self.emitsleep(x,y,self.oceaneer(color), null+ocean)
        except Exception as e:
            print(e)
            pass
        
susbot = SusBot()
#end of the line, partner
