# key input monitor
Linux X Window Keyboard Input Monitor 

Usage: 
```python
import key_input_monitor as keyinput
def onKeyEvent(pressed_key,released_key):
    if (1,2) in pressed_key:
        keyinput.stop()
keyinput.start(onKeyEvent)
```
