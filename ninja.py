# SusBot
# Requires Firefox
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

chart = 7 #which map to play on
stop_key = 'shift+d' #emergency stop button
autologin = False #requires reddit
unit_measurement = 'pixels' #change to whatever you want

colors = {(255, 255, 255): 0,  (196, 196, 196): 1,
          (136, 136, 136): 2,  (85, 85, 85): 3,
          (34, 34, 34): 4,     (0, 0, 0): 5,
          (0, 54, 56): 39,     (0, 102, 0): 6,
          (27, 116, 0): 49,    (71, 112, 80): 40,
          (34, 177, 76): 7,    (2, 190, 1): 8,
          (81, 225, 25): 9,    (148, 224, 68): 10,
          (152, 251, 152): 41, (251, 255, 91): 11,
          (229, 217, 0): 12,   (230, 190, 12): 13,
          (229, 149, 0): 14,   (255, 112, 0): 42,
          (255, 57, 4): 21,    (229, 0, 0): 20,
          (206, 41, 57): 43,   (255, 65, 106): 44,
          (159, 0, 0): 19,     (107, 0, 0): 18,
          (255, 117, 95): 23,  (160, 106, 66): 15,
          (99, 60, 31): 17,    (153, 83, 13): 16,
          (187, 79, 0): 22,    (255, 196, 159): 24,
          (255, 223, 204): 25, (255, 167, 209): 26,
          (207, 110, 228): 27, (125, 38, 205): 45,
          (236, 8, 236): 28,   (130, 0, 128): 29,
          (51, 0, 119): 46,    (2, 7, 99): 31,
          (81, 0, 255): 30,    (0, 0, 234): 32,
          (4, 75, 255): 33,    (0, 91, 161): 47,
          (101, 131, 207): 34, (54, 186, 255): 35,
          (0, 131, 199): 36,   (0, 211, 221): 37,
          (69, 255, 200): 38,  (181, 232, 238): 48}

colors_reverse = {value: key for key, value in zip(colors.keys(), colors.values())}
color_values = list(colors.values())

null = [(204,204,204)]
ocean = [ (51, 0, 119),    (2, 7, 99),
          (81, 0, 255),    (0, 0, 234),
          (4, 75, 255),    (0, 91, 161),
          (101, 131, 207), (54, 186, 255),
          (0, 131, 199),   (0, 211, 221),
          (69, 255, 200),  (181, 232, 238)]

class SusBot():
    ##################
    # Hotkey Section: 
    def hotkey_preload(self):
        self.river_bend_key = 'd' # river bend tool
        self.linekey = 'v' # line tool
        self.piekey = 's' # circle tool
        self.mine = 'e' # mining tool
        self.reverse = 'q' # reverse mining tool
        self.copykey = 'f8' # copy a region by swiping right and down
        self.pastekey = 'f9' # paste the copied region at mouse location
        self.windkey = 'shift+v' # large bucket fill tool
        self.oceankey = 'o' # ocean
        self.downspeed = 'shift+insert' # decrease bot speed
        self.upspeed = 'shift+delete' # increase bot speed
        self.fillborderskey = 'f4'# fill borders toggle key
        
     # SET YOUR HOTKEY DESCRIPTIONS HERE:
        controls = ['',
            "Controls:",
            '',
            '# mining tools',
            f'{self.mine} # mining tool',
            f'{self.reverse} # reverse mining tool',
            '',
            '# fill tools',     
            f'{self.windkey} # large bucket fill tool',
            f'{self.oceankey} # ocean',
            '',
            '# shape tools',    
            f'{self.linekey} # line tool',
            f'{self.piekey} # circle tool',
            '',
            '# extras',
            f'{self.fillborderskey} # fill borders toggle key',
            f'{self.river_bend_key} # river bend tool'
            '',
            f'{self.copykey} # copy a region by swiping right and down',
            f'{self.pastekey} # paste the copied region at mouse location',
            '',
            f'{self.downspeed} # decrease bot speed',
            f'{self.upspeed} # increase bot speed',
            '',
            '# Equip your colors with the 1 key and press ` or ~ to clear them out.',
            "# Copy doesn't copy equipped colors, and paste doesn't paste on equipped colors.",
            '',
            f'stop key = {stop_key}',
            '',
            '# ~ ~ ~ ~ ~* ~* ~ ~*','']   
        for control in controls:
            print(control)
            
    def hotkeys(self):
        keyboard.add_hotkey(self.river_bend_key,lambda:self.river_bend(self.river_bend_key)) # river bend tool
        keyboard.add_hotkey(self.linekey,lambda:self.thick_line(self.linekey, 2)) # line tool, second parameter is line thickness
        keyboard.add_hotkey(self.piekey,lambda:self.circle_outline(self.piekey)) # circle tool
        keyboard.add_hotkey(self.mine,lambda:self.prototype_mining_tool(self.mine)) # mining tool
        keyboard.add_hotkey(self.reverse,lambda:self.prototype_mining_tool(self.reverse)) # reverse mining tool
        keyboard.add_hotkey(self.copykey,lambda:self.copypaste('copy','f8')) # copy a region by swiping right and down
        keyboard.add_hotkey(self.pastekey,lambda:self.copypaste('paste','f9')) # paste the copied region at mouse location
        keyboard.add_hotkey(self.windkey,lambda:self.mighty_wind(self.windkey)) # large bucket fill tool
        keyboard.add_hotkey(self.oceankey,lambda:self.ocean(self.oceankey)) # water bucket
        keyboard.add_hotkey(self.downspeed, lambda: self.change_speed('decrease')) # decrease bot speed
        keyboard.add_hotkey(self.upspeed, lambda: self.change_speed('increase')) # increase bot speed
        keyboard.on_press(self.onkeypress)  # equips your colors to the 0-9 slots press ` or ~ to clear the filters
        keyboard.add_hotkey(self.fillborderskey,lambda:self.fillborderstoggle(self.fillborderskey)) # fill borders toggle key

    ##################
    # Gameplay Section:
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
                if self.emitsleep((xfl:=(1-t)**2 * start[0] + (2 * t * (1-t) * control_average[0]) + (t**2 * end[0])), (yfl:=((1-t)**2 * start[1]) + (2 * t * (1-t) * control_average[1]) + (t**2 * end[1])), colors[random.choice(ocean)], ocean):
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
                self.emitsleep(x,y,colors[random.choice(ocean)], null + ocean)
        except Exception as e:
            print(e)
            pass

    def thick_line(self, key, width):
        try:
            color=self.return_color()
            start, end = self.zone(key)
            x2, y2 = end
            x1, y1 = start
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
                for j in range(-width // 2, width // 2 + 1):
                    self.emitsleep(x3 + j, y3, color, [])
                    self.emitsleep(x3, y3 + j, color, [])
            print(f'Drew a {length} {unit_measurement} line.')
        except Exception as e:
            print(e)
            pass

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

    def prototype_mining_tool(self, key):        
        try:            
            self.start = time.time()            
            x, y = self.xy()          
            if key == self.mine:
                drill_bit = [[a+x, b+y, self.cy_cols(colors[self.cache[a+x, b+y]]) if self.cache[a+x, b+y] in colors else self.return_color()] for a in range(-1,2) for b in range(-1,2)]           
            elif key == self.reverse:
                drill_bit = [[a+x, b+y, self.reverse_cy_cols(colors[self.cache[a+x, b+y]]) if self.cache[a+x, b+y] in colors else self.return_color()] for a in range(-1,2) for b in range(-1,2)]
            for i in list(drill_bit):
                if [i[0]-x, i[1]-y] in [[-1,-1],[1,-1],[1,1],[-1,1]]:
                    drill_bit.remove(i)
            self.emit_block_sleep(drill_bit)
        except Exception as e:
            print(e)
            pass

    def copypaste(self, option, key):
        try:
            if option == "copy":
                self.work_order=()
                self.xy()
                start, end = self.zone(key)
                x1, y1 = start
                x2, y2 = end           
                print('Copying...')
                cx = (x2 - x1) // 2
                cy = (y2 - y1) // 2
                for X in range(x1, x2):
                    for Y in range(y1, y2):
                        if self.cache[X, Y] not in null + self.colorfilter:
                            self.work_order += ((X-x1-cx, Y-y1-cy, colors[self.cache[X, Y]]),)
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

    def mighty_wind(self, key):
        try:
            self.start = time.time()
            color=self.return_color()
            border_list =  []
            filters = [i for i in self.colorfilter]
            locs = []
            def locate():
                locs.append(self.xy())
            locate()
            while len(locs) > 0:
                x, y = locs.pop(locs.index(random.choice(locs)))
                ic = 0
                for i in ((x, y),(x+1, y),(x-1, y),(x, y-1),(x, y+1)):
                    for ap in [(i[0]+1, i[1]), (i[0]-1, i[1]), (i[0], i[1]+1), (i[0], i[1]-1)]:
                        if self.cache[ap[0], ap[1]] in [(204,204,204)] and self.cache[i[0], i[1]] not in [(204,204,204)]:
                            border_list.append([i[0], i[1]])                   
                    if self.cache[i[0], i[1]] not in [colors_reverse[color]] + [(204,204,204)] + filters:
                        sio.emit('p',[i[0], i[1], color, 1])
                        try:
                            color = colors[random.choice(self.colorfilter)]
                        except:
                            pass
                        locs.append([i[0], i[1]])
                        ic+=1
                    if keyboard.is_pressed(key):
                        locate()
                    elif keyboard.is_pressed(stop_key):
                        return                    
                time.sleep(speed*ic - (self.start - time.time()))
                self.start = time.time()
            if self.borders == True:
                ic = 0
                newlist = []
                for i in border_list: 
                    if i not in newlist: 
                        newlist.append(i)
                for i in newlist:
                    sio.emit('p', [i[0], i[1], self.border_color, 1])
                    ic += 1
                    if ic >= 20:
                        time.sleep(speed*ic - (self.start - time.time()))
                        self.start = time.time()
                        ic = 0            
        except Exception as e:
            print(e)
            pass
                        
    def ocean(self, key):
        try:
            self.start = time.time()
            locs = []
            def locate():
                locs.append(self.xy())
            locate()
            while len(locs) > 0:
                if keyboard.is_pressed(key):
                    locate()
                elif keyboard.is_pressed(stop_key):
                    return
                x, y = locs.pop(locs.index(random.choice(locs)))
                ic = 0
                for i in ((x-1,y-2),(x,y-2),(x+1,y-2),(x-2,y-1),(x-1,y-1),(x,y-1),(x+1,y-1),(x-2,y),(x-1,y),(x,y),(x+1,y),(x-1,y+1),(x+1,y+1)):
                    if self.cache[i[0], i[1]] not in ocean +[(204,204,204)]:
                        sio.emit('p',[i[0], i[1], colors[random.choice(ocean)], 1])
                        locs.append([i[0], i[1]])
                        ic+=1
                time.sleep(speed*ic - (self.start - time.time()))
                self.start = time.time()
        except:
            pass

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
        self.emit_counter = 0
        self.hotkey_preload()
        self.hotkeys()
        self.borders = True
        self.colorfilter = []
        self.return_color()
        self.border_color = self.color
        self.connection()

    def load_map_into_cache(self):
        with open(f'{chart}.png', 'wb') as f:
            f.write(requests.get(f'https://pixelplace.io/canvas/{chart}.png?t={random.randint(9999,99999)}').content)
        self.image = PIL.Image.open(f'{chart}.png').convert('RGB')
        self.cache = self.image.load()
        
    def clear_cookies(self, url):
        driver.get(url)
        driver.delete_all_cookies()

    def login(self):
        if autologin == True:
            self.clear_cookies('https://reddit.com')
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
                    self.cache[i[0], i[1]] = colors_reverse[i[2]]
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

    def change_speed(self, opt):
        global speed
        try:
            if opt == 'decrease':
                speed += 0.001
                speed = float('%.3f'%speed)
            elif opt == 'increase':
                speed -= 0.001
                speed = float('%.3f'%speed)
            if speed < 0.015:
                print(f"Going too fast now, defaulting to {regular_speed} to prevent perma ban.")
                speed = regular_speed
            if speed == 0.015:
                print(f"Warning: You are in speed throttling territory.")
            if speed > 0.014:
                    print("Speed:",speed)
        except Exception as e:
            print(e)
            pass
            
    def xy(self):
        try:
            self.x, self.y = make_tuple(driver.find_element(By.XPATH,'/html/body/div[3]/div[4]').text)
            return [self.x, self.y]
        except:
            pass

    def distance(self, xy1, xy2):
        return int(math.sqrt((xy2[0] - xy1[0])**2 + (xy2[1] - xy1[1])**2))
    
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

    def ifsioemit(self, x, y, color):
        if self.cache[x,y] not in [colors_reverse[color]] + null + self.colorfilter:
            sio.emit('p',[x, y, color, 1])
            return True
        
    def emit_block_sleep(self, block_list):
        if len(block_list) > 32:
            pass
        else:
            for i in block_list:
                try:
                    x, y, color = i                  
                    if self.ifsioemit(x, y, color):
                        self.emit_counter += 1
                except:
                    pass
            time.sleep(speed * self.emit_counter)
            self.start = time.time()
            self.emit_counter = 0
            
    def cy_cols(self, color):
        color_index = color_values.index(color)
        if color_index == len(color_values) - 1:
            return 0
        else:
            return color_values[color_index + 1]
        
    def reverse_cy_cols(self, color):
        color_index = color_values.index(color)
        if color_index == 0:
            return color_values[-1]
        else:
            return color_values[color_index - 1]
    
        
    def emitsleep(self, x, y, color, filters):
        try:
            if self.cache[x,y] not in [colors_reverse[color]] + filters + null + self.colorfilter: 
                sio.emit('p',[x, y, color, 1])
                time.sleep(speed - (self.start - time.time()))
                self.start = time.time()
                return True
            else:
                return False
        except:
            return False
        
    def zone(self, key):
        x1, y1 = self.xy()
        while True:
            if not keyboard.is_pressed(key):
                break
        x2, y2 = self.xy()
        return [x1, y1], [x2, y2]
    
        
    def fillborderstoggle(self, key):
        self.border_color = self.return_color()
        self.borders = True if self.borders == False else False
        print('borders on' if self.borders == True else 'borders off')
        time.sleep(speed*3)
        
    def getcurcolorhotkey(self, col):
        try:
            self.colorfilter.append(colors_reverse[self.get_color_index()])
            print(f'Equipped {self.colorfilter[-1]} Press ` or ~ to clear filters.')
            return
        except Exception as e:
            print(e)
            pass
        
    def onkeypress(self, event):
        try:
            if event.name in ['1']:
                self.getcurcolorhotkey(int(event.name))
            elif event.name in ['`', '~']:
                self.removefilters()
        except Exception as e:
            print(e)
            pass
        
    def removefilters(self):
        try:
            self.colorfilter = []
            print("Filters dequipped.")
        except Exception as e:
            print(e)
            pass
        
    def get_color_index(self):
        try:
            cid = str(driver.find_element(By.XPATH,'/html/body/div[3]/div[2]').get_attribute("style"))
            a = cid.find('(')
            b = cid.find(')');b+=1
            cid = cid[a:b]
        finally:
            return self.get_color(make_tuple(cid))

    def return_color(self):
        try:
            self.color = self.get_color_index()
        except:
            self.color = random.choice(colors_reverse.keys())
        return self.color
    
    def get_color(self, input):
        if type(input) == int:
            return colors_reverse[(input)]
        elif type(input) == tuple:
            return colors[(input)]
        else:
            return None

SusBot()
