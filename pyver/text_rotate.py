"""
 Simple graphics demo
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
"""
 
# Import a library of functions called 'pygame'
import pygame
 
import argparse
import tempfile
import queue
import sys
import os

import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'filename', nargs='?', metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
parser.add_argument(
    '-c', '--channels', type=int, default=1, help='number of input channels')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args(remaining)

q = queue.Queue()



# Initialize the game engine
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
 
lastInput = ""

text_rotate_degrees = 0
is_recording = False 
# Loop as long as done == False


if args.samplerate is None:
    device_info = sd.query_devices(args.device, 'input')
    # soundfile expects an int, sounddevice provides a float:
    args.samplerate = int(device_info['default_samplerate'])
if args.filename is None:
    args.filename = tempfile.mktemp(prefix='delme_rec_unlimited_',
                                    suffix='.wav', dir='')

def callback(indata, frames, time, status):
    global is_recording
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)

    if is_recording:
      q.put(indata.copy())

import time
import threading
class Foo (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run (self):
        with sd.InputStream(samplerate=args.samplerate, device=args.device,
                channels=args.channels, callback=callback):
            while not(done):
               time.sleep(0.001)


Foo().start()
# Make sure the file is opened before recording anything:

print("samplerate", args.samplerate)


from allosaurus.app import read_recognizer
model = read_recognizer("latest")

def savesound():
    global lastInput
    filename = tempfile.mktemp(prefix='delme_rec_unlimited_',
                                        suffix='.wav', dir='')
    filename = "buff.wav"

    # Make sure the file is opened before recording anything:
    file = sf.SoundFile(filename, mode='x', samplerate=args.samplerate,
                      channels=args.channels, subtype=args.subtype)
    try:
              while True:
                 elem = q.get_nowait()
                 file.write(elem)
                 #print("got frame")
    except Exception as e:
              pass
    file.flush()
    file.close()
    try:
      results = model.recognize(filename, "eng")
      print("text: " + results)
      lastInput = str(results)
    except Exception as e:
      print(e)
      pass
 
 
while not done:
 
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            is_recording = True 
        elif event.type == pygame.MOUSEBUTTONUP:
            is_recording = False 
            savesound()
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
