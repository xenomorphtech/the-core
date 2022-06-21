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

pygame.init()
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
PI = 3.141592653
 
# Set the height and width of the screen
size = (400, 500)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Rotate Text")
 
# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
 
 
while not done:
 
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
        elif event.type == pygame.KEYDOWN and event.key == 27: 
            #print(event)
            done = True 


     # All drawing code happens after the for loop and but
    # inside the main while not done loop.
 
    # Clear the screen and set the screen background
    screen.fill(WHITE)
 
    # Draw some borders
    #pygame.draw.line(screen, BLACK, [100,50], [200, 50])
    #pygame.draw.line(screen, BLACK, [100,50], [100, 150])
 
    # Select the font to use, size, bold, italics
    font = pygame.font.SysFont('Calibri', 25, True, False)
 
    # Sideways text
    if is_recording: 
      text = font.render("recording", True, BLACK)
      #text = pygame.transform.rotate(text, 90)
      screen.blit(text, [0, 0])
 
    text = font.render("last input: " + lastInput, True, BLACK)
    screen.blit(text, [0, 40])
  
    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()
 
    # This limits the while loop to a max of 60 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(60)
 
# Be IDLE friendly
pygame.quit()
