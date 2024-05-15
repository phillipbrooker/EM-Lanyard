"""
UNDISCIPLINING THE CONFERENCE
Code by Phillip Brooker

A Rasberry Pi Zero 2 W and Inky pHAT lanyard/badge
which instructs people, visibly, wittnessably, in
conference-doing.

Part of a project being run at The Sociological
Review's "Undisciplining II" conference in Salford,
September 2024, co-authored with Rob Smith, Terry
Au-Yeung, Patrik Dahl, Patricia Jimenez Lugo and
Jonathan Ablitt. Additional code support by
Dipanjan Saha.
"""

"""
CONTENTS:
    1. Imports
    2. Inky pHAT Setup
    3. Inky pHAT Display Engine
    4. Shutdown Routine
"""

#1. Imports

    #1.1. Inky pHAT
from inky.auto import auto
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne

    #1.2. Message data
from undisciplining_msgs import msgs

    #1.3. Other/general
from random import choice
from subprocess import call
from time import sleep

#2. Inky pHAT Setup
inky = auto() #Initialising inky display
inky.set_border(inky.WHITE)

img = Image.new("P", (inky.WIDTH, inky.HEIGHT)) #initialising image
draw = ImageDraw.Draw(img)

font1 = ImageFont.truetype(FredokaOne, 16) #font constants
font2 = ImageFont.truetype(FredokaOne, 24)

#3. Inky pHAT Display Engine
name = "Phil" #For personalisation

    #3.1. "Game over" screen
def displayGameOver():
    line1 = "I'm " + name + ", and I've..." #line text (headline)
    w1, h1 = font1.getsize(line1) #width and height of line
    x1 = 2 #x position in pixels
    y1 = 2 #y position in pixels

    line2 = "Completed the"
    w2, h2 = font2.getsize(line2)
    x2 = (inky.WIDTH/2) - (w2/2) #centre justified
    y2 = 28 #start height of first main line

    line3 = "Undisciplining II"
    w3, h3 = font2.getsize(line3)
    x3 = (inky.WIDTH/2) - (w3/2) 
    y3 = y2 + h2 #start height relative to previous line

    line4 = "Conference!"
    w4, h4 = font2.getsize(line4)
    x4 = (inky.WIDTH/2) - (w4/2)
    y4 = y3 + h3

    #drawing lines to image in right place with correct colour/font
    draw.text((x1, y1), line1, inky.BLACK, font1)
    draw.text((x2, y2), line2, inky.BLACK, font2)
    draw.text((x3, y3), line3, inky.BLACK, font2)
    draw.text((x4, y4), line4, inky.BLACK, font2)
    inky.set_image(img)
    inky.show()
    
    #3.2. Displaying the chosen message
def displayMsg(msg):
    line1 = "I'm " + name + ", and I'm..."
    w1, h1 = font1.getsize(line1)
    x1 = 2
    y1 = 2

    line2 = msg[0] #using the randomly selected new message
    w2, h2 = font2.getsize(line2)
    x2 = (inky.WIDTH/2) - (w2/2)
    y2 = 28

    line3 = msg[1]
    w3, h3 = font2.getsize(line3)
    x3 = (inky.WIDTH/2) - (w3/2)
    y3 = y2 + h2

    line4 = msg[2]
    w4, h4 = font2.getsize(line4)
    x4 = (inky.WIDTH/2) - (w4/2)
    x4 = (inky.WIDTH/2) - (w4/2)
    y4 = y3 + h3

    draw.text((x1, y1), line1, inky.BLACK, font1)
    draw.text((x2, y2), line2, inky.BLACK, font2)
    draw.text((x3, y3), line3, inky.BLACK, font2)
    draw.text((x4, y4), line4, inky.BLACK, font2)
    inky.set_image(img)
    inky.show()

    #3.3. Choosing a new message
read_msgs = open("messages.txt", "r") #read in list of used messages
used_msgs = read_msgs.read()
read_msgs.close()

def count_lines(): #checking how many messages have been used
    read_msgs = open("messages.txt", "r")
    line_count = sum(1 for line in read_msgs)
    return line_count

def msg_select(used_msgs):
    msg = choice(msgs) #choose a random message
    if count_lines() == len(msgs): #if we've used all messages
        displayGameOver()
    elif str(msg) in used_msgs: #if the selected message has been used
        return msg_select(used_msgs)
    else: #if it's a new message
        messages_file = open("messages.txt", "a")
        messages_file.write(str(msg) + "\r")
        messages_file.close()
        return displayMsg(msg)

msg = msg_select(used_msgs) #using the msg_select function on execution

#4. Shutdown Routine
    #NOTE: Comment out unless you are actively using this device as
    #a lanyard in "use mode". Once this executes, you will have to
    #remove the SD card and edit the file on another Linux OS to be
    #able to get back into "dev mode" on the RPi.
"""
sleep(10) #to allow processes to finish
call("sudo shutdown -h now", shell=True) #immediate (non-timed) shutdown
"""
