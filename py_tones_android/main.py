#!/usr/bin/env python3
"""Create a recording with arbitrary duration.
The soundfile module (https://PySoundFile.readthedocs.io/) has to be installed!
"""
import argparse
import tempfile
import queue
import sys
import os

import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

import pygame

import time
import random

#from unpythonic.net import server
#server.start(locals={})

import socket

pygame.init()
 
sounds = os.listdir('sounds')

pygame.mixer.init()


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (150, 150, 150)

PI = 3.141592653
 
# Set the height and width of the screen
size = (400, 700)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("pick char")
 
# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

info = pygame.display.Info()

font = pygame.font.SysFont('Source Han Sans CN', int(info.current_w / 13) , True, False)
font1 = pygame.font.SysFont('Source Han Sans CN', 50, True, False)


import json

def read_conf():
    try:
        f = json.loads(open("playdata.json").read())
    except:
        f = {"performance": {}, "maxfreq": 1000, "min_exposure": 1000}
    return f

playdata = read_conf()


try:
 from android import loadingscreen
 loadingscreen.hide_loading_screen()
 # from android.permissions import request_permissions, Permission
 # request_permissions([Permission.INTERNET])
 # request_permissions([Permission.ACCESS_NETWORK_STATE])
 playres = "ok|"
except Exception as e:
    playres = str(e)


try:

    # create an INET, STREAMing socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # now connect to the web server on port 80 - the normal http port
    sock.connect(("192.168.2.5", 9002))
    sock.send(bytes("connected\r\n", "utf-8"))


    #soundObj = pygame.mixer.Sound("sounds/ai2.ogg")
    #soundObj.play()
    playres += "ok"
except Exception as e:
    playres += str(e)

#    sock.send(bytes(str(e)+"\r\n", "utf-8"))


#soundObj = pygame.mixer.Sound(open("sound_effects/error-sound-39539.ogg", "br"))
#soundObj.play()


def render_init():
    global screen, font, word, playres
    

    text = font1.render("开始", True, WHITE)
    screen.blit(text, [info.current_w/2 - 50, info.current_h/2 - 25])
    text = font1.render("%d x %d" % (info.current_w, info.current_h), True, WHITE)
    screen.blit(text, [0, 0])


phase = "init"
start_time = time.time()

def render_showword():
    global screen, font, word
    #text = font1.render(word, True, WHITE)
    mid_h = info.current_h/2
    #screen.blit(text, [info.current_w/2 - 25, mid_h - 25])
    pinyin = word 
    text = font1.render(pinyin, True, WHITE)
    screen.blit(text, [info.current_w/2 - (len(pinyin) * 15), mid_h + 60])


cell_space = 60
cell_per_row = 6

w_10 =  info.current_w / 20

opts = [
            ("q - first", ((w_10, 100), (w_10 * 8, 100)), "1"),
            ("w - second", ((w_10*11, 100), (w_10 * 8, 100)), "2"),
            ("e - third", ((w_10, 300), (w_10 * 8, 100)), "3"),
            ("r - fourth", ((w_10*11, 300), (w_10 * 8, 100)), "4"),
                 ]

opts = [
            ("q - first", ((w_10, 100), (w_10 * 18, 80)), "1"),
            ("w - second", ((w_10, 200), (w_10 * 18, 80)), "2"),
            ("e - third", ((w_10, 300), (w_10 * 18, 80)), "3"),
            ("r - fourth", ((w_10, 400), (w_10 * 18, 80)), "4"),
                 ]



def render_pickword():
    global screen, font, word, playdata, chooses
    #print("---")
    #min_time = playdata["performance"][word] if word in playdata["performance"] else 0 

    for y in range(0, len(opts)):
            color = WHITE 
            (target, (rect_a, rect_b), meaning) = opts[y]

            pygame.draw.rect(screen, GRAY, pygame.Rect(rect_a, rect_b))

            text = font.render(target, True, color)
            x = rect_a[0] + rect_b[0]/2 - (len(target) * 8)
            y = rect_a[1] + rect_b[1]/2 
            screen.blit(text, [x, y])



    mid_w = info.current_w/2
    for a in range(len(chooses)):
        color = RED if chooses[a] != tones[a] else GREEN
        text = font.render(chooses[a], True, color)
        screen.blit(text, [mid_w - len(tones) * 15 + 30 * a, 8 * 60 + 30])

    for a in range(len(chooses)):
        color = WHITE 
        text = font.render(tones[a], True, color)
        screen.blit(text, [mid_w - len(tones) * 15 + 30 * a, 9 * 60 + 30])

    #for x in range(0, cell_per_row):
    #    for y in range(0, 8):
    #        color = WHITE 
    #        target = randomboard[y * cell_per_row + x]
    #        #print(y * 6 + x)
    #        if clicked and (pos == (x, y)):
    #            color = RED
    #        if clicked and (target == word):
    #            color = GREEN 

    #        text = font.render(target, True, color)
    #        screen.blit(text, [30 + x * cell_space, 30 + y * cell_space])

def tones(s):
    pinyin_with_tones = s[:-len('.ogg')].split('_')
    tones = ''.join(x[-1] for x in pinyin_with_tones)
    return tones

sounds = [s for s in sounds if len(tones(s)) < 3]
#sounds = [s for s in sounds if tones(s) != "44"]
#sounds = [s for s in sounds if tones(s) == "24" or tones(s) == "42"]
#sounds = [s for s in sounds if tones(s) == "1" or tones(s) == "3"]
#sounds = [s for s in sounds if tones(s) == "2" or tones(s) == "4"]

v = {}
for s in sounds:
    a = tones(s)
    if a in v:
              v[a].append(s)
    else:
              v[a] = [s] 

#for k in v.keys():
# print(k, len(v[k]))

from numpy.random import default_rng
rng = default_rng()
chooses = ""

def next_word():
    global phase, start_time, word, randomboard, clicked, right_pos, tones, chooses, v

    r = rng.choice(list(v.keys()))
    index = int(rng.uniform(0, len(v[r])))
    path = 'sounds/%s' % v[r][index] 
    pinyin_with_tones = path.split('/')[-1][:-len('.ogg')].split('_')
    tones = ''.join(x[-1] for x in pinyin_with_tones)
    pinyin_without_tones = [x[:-1] for x in pinyin_with_tones]

    soundObj = pygame.mixer.Sound(open(path, "br"))
    soundObj.play()

    word = "".join(pinyin_without_tones)
    start_time = time.time()
    phase = "showword"
    clicked = False 
    chooses = ""
  
def show_pick():
    global phase, start_time, playdata
    phase = "pickword"
    start_time = time.time()
 
def init_proc_event(event):
    if event.type == pygame.MOUSEBUTTONUP:
       next_word()
    
 
def showword_proc_event(event):
    global clicked, selected, pos, start_time
    if event.type == pygame.MOUSEBUTTONUP:
        show_pick()
    elif event.type == pygame.KEYDOWN and event.key == 32: 
        show_pick()

keys = [ord(k) for k in "qwert"]

def keypos(key):
   if not(key in keys):
       return None
   return keys.index(key) 

def pickword_proc_event(event):
    global clicked, selected, pos, start_time, tones, chooses
    clicked_before = clicked
    if event.type == pygame.MOUSEBUTTONUP:
        (x, y) = pygame.mouse.get_pos()
        button = None
        for (t, (ra, rb), b) in opts:
            if (x > ra[0] and x < ra[0] + rb[0]) and (y > ra[1] and y < ra[1] + rb[1]):
                   button = b

        if button:
            if len(chooses) < len(tones):
                chooses += button 
            if len(chooses) == len(tones):
                clicked = True
            start_time = time.time()

    if event.type == pygame.KEYDOWN and keypos(event.key) != None: 
        pos = keypos(event.key)
        if len(chooses) < len(tones):
            chooses += "%d" % (pos+1)
        if len(chooses) == len(tones):
            clicked = True
        start_time = time.time()

    if clicked != clicked_before and chooses == tones:

      soundObj = pygame.mixer.Sound(open("sound_effects/sound-effects-finger-snap-without-reverb-113862.ogg", "br"))
      soundObj.play()


try:
 while not done:
    events = pygame.event.get()
    for event in events:  # User did something
        if phase == "init":
            init_proc_event(event)
        #elif phase == "showword":
        #    showword_proc_event(event)
        elif phase == "pickword":
            pickword_proc_event(event)

        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
        elif event.type == pygame.KEYDOWN and event.key == 27: 
            done = True 

    if events == []:
        if phase == "showword":
            if time.time() - start_time > 1000 / 1000:
             show_pick()
        if phase == "pickword":
            if (clicked == True) and (time.time() - start_time > 0.500):
             next_word()
 
    screen.fill(BLACK)
 
    # Draw some borders
    #pygame.draw.line(screen, BLACK, [100,50], [200, 50])
    #pygame.draw.line(screen, BLACK, [100,50], [100, 150])
 
    if phase == "init": 
        render_init()
    elif phase == "showword":
        render_showword()
    else:
        render_pickword()
  
    pygame.display.flip()
 
    clock.tick(60)

except Exception as e:
    sock.send(bytes(str(e)+"\r\n", "utf-8"))

pygame.quit()
