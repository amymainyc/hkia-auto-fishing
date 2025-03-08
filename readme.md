# Hello Kitty Island Adventure Auto-Fisher
A machine learning object detection model custom-trained to automate fishing in the game Hello Kitty Island Adventure.

## Important Notes
#### Intentions
I created this with the intention to learn more about machine learning and object detection and to have a little fun. I have no intention of ruining the game for other players. If you download this, please use responsibly and don't flood the multiplayer market with sticks. 

#### Best Uses
Another thing, this model is trained mostly with fishing images from the Spooky Swamp dock/lily pads next to the witch hut. Therefore, that is where it will perform best. It may work in other places, just less effectively. I may train it to fish in other areas in the future. 

## Setup:
- Download Terminal: https://apps.microsoft.com/detail/9n0dx20hk701?hl=en-US&gl=US
- Download the file titled "autofisher.zip" here: https://github.com/amymainyc/hkia-auto-fishing/releases/
- Right-click the file in file explorer and click "Extract All"
- Find the folder you just extracted (should be titled "autofisher"), right-click the folder, then click "Open in Terminal"
- If you don't have Python installed, type "python" and hit enter. It will prompt you to install Python. 
- Run the following command: `pip install -r requirements.txt` 

## Running
- To start the fishing AI, run the following command in the same terminal as above: `python fishing.py`
- To pause/resume, press and hold the F10 key for 1 second.
- To stop the program entirely, use `Ctrl-C` in the terminal

If you followed the instructions above, the fishing AI should be running. However, you may need to adjust some things: 

## Adjustments
### Screen Capture Region
Open "fishing.py" in any text editor and find the lines that say:
```
# Define the screen capture region (x, y, width, height)
CAPTURE_REGION = (1280, 720, 1280, 720) # bottom right
```
This defines the region of the screen that the program captures. My monitor has a resolution of 2560x1440, so the code above captures the bottom right of my screen. You might have to adjust this based on your resolution and how big your game window is. You could make it capture your whole screen but that may slow down your computer. 

**Note:** Whenever you change anything in "fishing.py", you must stop and restart the program using `Ctrl-C` and `python fishing.py`.

### Why did it stop fishing?
When you fish in HKIA, the fish sometimes pulls your character so that it faces left or right of where you initially cast your fishing rod. This sometimes makes your fishing line unable to cast. To counter this, if a fish has not been caught for 1 minute, it will nudge the character in the UP direction. This ONLY works if the HKIA window is in focus. 

If you don't want this to happen, you can unfocus the window. 

If you want it to be nudged in a different direction, go to "fishing.py" and find the function below and modify the values. For example, a DOWN nudge would be `gamepad.left_joystick(0, -10000)` and a LEFT nudge would be `gamepad.left_joystick(10000, 0)`.
```
def reposition_character():
    """Reposition the character by nudging the left stick vertically."""
    time.sleep(0.2)
    gamepad.left_joystick(0, 10000) # CHANGE THIS
    gamepad.update()
    time.sleep(0.1)
    gamepad.left_joystick(0, 0)
    gamepad.update()
    time.sleep(0.2)
```

Because of this nudging, if you leave the fishing program on for too long, you might find your character swimming with the fish. 
