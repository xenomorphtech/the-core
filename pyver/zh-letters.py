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

pygame.init()
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
PI = 3.141592653
 
# Set the height and width of the screen
size = (400, 700)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("pick char")
 
# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

from cedict_utils.cedict import CedictParser
parser = CedictParser()
parser.read_file("data/cedict_ts.u8")
entries = parser.parse()
e_to_d = {} 
for entry in entries:
   e_to_d[entry.simplified] = entry


font = pygame.font.SysFont('Source Han Sans CN', 30, True, False)
font1 = pygame.font.SysFont('Source Han Sans CN', 50, True, False)

info = pygame.display.Info()

def load_freq():
   freq = open("data/frequency").read().split("\n")
   dic = {}
   for f in freq:
       kv = f.split("\t")
       if len(kv) > 1:
           dic[int(kv[0])] = kv[1]
   return dic 

frequency = load_freq()

#print(frequency)

import json

def read_conf():
    try:
        f = json.loads(open("playdata.json").read())
    except:
        f = {"performance": {}, "maxfreq": 1000, "min_exposure": 1000}
    return f

playdata = read_conf()

def render_init():
    global screen, font, word
    text = font1.render("开始", True, WHITE)
    screen.blit(text, [info.current_w/2 - 50, info.current_h/2 - 25])

phase = "init"
start_time = time.time()

def render_showword():
    global screen, font, word
    text = font1.render(word, True, WHITE)
    mid_h = info.current_h/2
    screen.blit(text, [info.current_w/2 - 25, mid_h - 25])
    pinyin = e_to_d[word].pinyin
    text = font1.render(pinyin, True, WHITE)
    screen.blit(text, [info.current_w/2 - (len(pinyin) * 15), mid_h + 60])


cell_space = 60
cell_per_row = 6

def render_pickword():
    global screen, font, randomboard, word, playdata
    #print("---")
    min_time = playdata["performance"][word] if word in playdata["performance"] else 0 
    text = font.render("min time: "+str(min_time), True, WHITE)
    screen.blit(text, [30, 8 * 60 + 30])

    for x in range(0, cell_per_row):
        for y in range(0, 8):
            color = WHITE 
            target = randomboard[y * cell_per_row + x]
            #print(y * 6 + x)
            if clicked and (pos == (x, y)):
                color = RED
            if clicked and (target == word):
                color = GREEN 

            text = font.render(target, True, color)
            screen.blit(text, [30 + x * cell_space, 30 + y * cell_space])

def next_word():
    global phase, start_time, word, randomboard, clicked, right_pos
    rnd = random.randint(1, playdata["maxfreq"]-1)
    word = frequency[rnd] 
    phase = "showword"
    start_time = time.time()
    nrange = range(1, playdata["maxfreq"])
    randomboard = [frequency[a] for a in random.sample(nrange, len(nrange))]
    randomboard.remove(word)
    inject = random.randint(1, 47)
    #print("inject" + str(inject))
    randomboard[inject] = word
    #print(randomboard)
    clicked = False 
  
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
 
def pickword_proc_event(event):
    global clicked, selected, pos, start_time
    if event.type == pygame.MOUSEBUTTONUP:
        (x, y) = pygame.mouse.get_pos()
        print((x,y))
        pos = (int((x - 30) / cell_space), int((y-30)/cell_space))
        print(pos)
        (pos_x, pos_y) = pos
        cell = pos_x + pos_y * cell_per_row 
        clicked = True
        elapsed = time.time() - start_time
        prev_elapsed = playdata["performance"][word] if word in playdata["performance"] else elapsed
        if (randomboard[cell] == word) and (elapsed <= prev_elapsed): 
          playdata["performance"][word] = elapsed 
        start_time = time.time()
    elif event.type == pygame.KEYDOWN and event.key == 32: 
        done = True 
        clicked = True
        playdata["performance"][word] = time.time() - start_time 
        start_time = time.time()
        pos = (0, 0)
 

while not done:
    events = pygame.event.get()
    for event in events:  # User did something
        if phase == "init":
            init_proc_event(event)
        elif phase == "showword":
            showword_proc_event(event)
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
            if time.time() - start_time > playdata["min_exposure"] / 1000:
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
 
pygame.quit()
