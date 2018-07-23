import key_input_monitor as keyinput

def onKeyEvent(pressed_key,released_key):
    if (1,2) in pressed_key:
        keyinput.stop()

    for (i,key) in pressed_key:
        print "(%d,%d) pressed" % (i, key) 

    for (i,key) in released_key:
        print "(%d,%d) released" % (i, key)

if __name__ == '__main__':
    keyinput.start(onKeyEvent)
