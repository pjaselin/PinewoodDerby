#              .';:cc;.
#            .,',;lol::c.
#            ;';lddddlclo
#            lcloxxoddodxdool:,.
#            cxdddxdodxdkOkkkkkkkd:.
#          .ldxkkOOOOkkOO000Okkxkkkkx:.
#        .lddxkkOkOOO0OOO0000Okxxxxkkkk:
#       'ooddkkkxxkO0000KK00Okxdoodxkkkko
#      .ooodxkkxxxOO000kkkO0KOxolooxkkxxkl
#      lolodxkkxxkOx,.      .lkdolodkkxxxO.
#      doloodxkkkOk           ....   .,cxO;
#      ddoodddxkkkk:         ,oxxxkOdc'..o'
#      :kdddxxxxd,  ,lolccldxxxkkOOOkkkko,
#       lOkxkkk;  :xkkkkkkkkOOO000OOkkOOk.
#        ;00Ok' 'O000OO0000000000OOOO0Od.
#         .l0l.;OOO000000OOOOOO000000x,
#            .'OKKKK00000000000000kc.
#               .:ox0KKKKKKK0kdc,.
#                      ...
#
# Author: peppe8o
# Date: Apr 24th, 2020
# Version: 1.0
# https://peppe8o.com

# Import required libraries
import sys
import RPi.GPIO as GPIO

# display_list = [17,27,22,10,9,11,5] # define GPIO ports to use
display_list = [11, 13, 15, 19, 21, 23, 29]
# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BOARD)
# GPIO.setmode(GPIO.BCM)

# Set all pins as output
GPIO.setwarnings(False)
for pin in display_list:
  GPIO.setup(pin, GPIO.OUT) # setting pins
GPIO.setup(31, GPIO.OUT) # setting dot pin
GPIO.setwarnings(True)

# DIGIT map as array of array
arrSeg = [[1,1,1,1,1,1,0],\
          [0,1,1,0,0,0,0],\
          [1,1,0,1,1,0,1],\
          [1,1,1,1,0,0,1],\
          [0,1,1,0,0,1,1],\
          [1,0,1,1,0,1,1],\
          [1,0,1,1,1,1,1],\
          [1,1,1,0,0,0,0],\
          [1,1,1,1,1,1,1],\
          [1,1,1,1,0,1,1]]

GPIO.output(31,0) # DOT pin

# Check main arguments errors
if len(sys.argv) > 2:
  print("ERROR: too many arguments")
  sys.exit()
elif len(sys.argv) == 1:
  print("ERROR: missing argument")
  sys.exit()
elif int(sys.argv[1].replace(".", "")) > 10 or int(sys.argv[1].replace(".", ""))<0:
  print("ERROR: insert a number between 0 and 10")
  sys.exit()

# Manage DOT activation
if sys.argv[1].count(".") == 1: GPIO.output(31,1)

# Activate number on display with a value cleaned from final dot
numDisplay = int(sys.argv[1].replace(".", ""))

# Display number in argument
if numDisplay == 10:
  GPIO.cleanup()
else:
  GPIO.output(display_list, arrSeg[numDisplay])

sys.exit()
