# -*- coding: utf-8 -*-
# Script Name: key_input_monitor.py
# Author: CrazyDog
# Github:https://github.com/icrazydog
# Version: 1.1
# Created: 07/23/2018
# Last Modified: 08/03/2018
# Description: Monitor press and release event of keyboard
# Usage: import key_input_monitor as keyinput
#        def onKeyEvent(pressed_key,released_key):
#           if (1,2) in pressed_key:
#               keyinput.stop()
#        keyinput.start(onKeyEvent)
#
#        Some other Function: close_echo() open_echo() cls()

import ctypes
from ctypes.util import find_library
import sys
import time
import termios
import threading

old_ttyinfo = None
run = True

# close terminal echo
def close_echo():
    global old_ttyinfo
    fd = sys.stdin.fileno()
    old_ttyinfo = termios.tcgetattr(fd)
    new_ttyinfo = old_ttyinfo[:]
    new_ttyinfo[3] &= ~termios.ICANON
    new_ttyinfo[3] &= ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, new_ttyinfo)

# open terminal echo
def open_echo():
    global old_ttyinfo
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSAFLUSH, old_ttyinfo)

# clean screen
def cls():
    print("\033c")

# start monitor
def start(onKeyEvent):
    global run
    run = True
    close_echo()
    threading.Thread(target=__start,args=(onKeyEvent,)).start()

# stop monitor
def stop():
    global run
    open_echo()
    run = False


def __start(onKeyEvent):
    global run
    x11 = ctypes.cdll.LoadLibrary(find_library("X11"))
    display = x11.XOpenDisplay(None)
    keyboard = (ctypes.c_char * 32)()

    print('key input monitor start')
    pressed_key = set()
    last_pressed_key = set()
    released_key = set()
    while run:
        time.sleep(0.05)
        x11.XQueryKeymap(display, keyboard)
        pressed_key.clear()
        for i, byte_str in enumerate(keyboard):
            key = ord(byte_str)
            if(key>0):
                if key & 1 > 0:
                    pressed_key.add((i, 1))
                if key & 2 > 0:
                    pressed_key.add((i, 2))
                if key & 4 > 0:
                    pressed_key.add((i, 4))
                if key & 16 > 0:
                    pressed_key.add((i, 16))
                if key & 32 > 0:
                    pressed_key.add((i, 32))
                if key & 64 > 0:
                    pressed_key.add((i, 64))
                if key & 128 > 0:
                    pressed_key.add((i, 128))

        released_key = last_pressed_key.difference(pressed_key)
        newPressed = pressed_key.difference(last_pressed_key)
        last_pressed_key = set(pressed_key)

        if len(newPressed)>0 or len(released_key)>0:
            onKeyEvent(newPressed,released_key)
    
    print('key input monitor stop')
