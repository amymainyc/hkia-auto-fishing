# Setup:
- Download Python here: https://www.python.org/downloads/
- Download the file titled "autofisher.zip" here: https://github.com/amymainyc/hkia-auto-fishing/releases/
- Right-click the file in file explorer and click "Extract All"
- Find the folder you just extracted (should be titled "autofisher"), right-click the foler, then click "Open in Terminal"
- Run the following commands: 

```
pip install -r requirements.txt
python fishing.py
```

If you followed the instructions above, the fishing AI should be running. You may need to adjust some things: 

# Adjustments
## Screen Capture Region
Open "fishing.py" and find the lines that say:
```
# Define the screen capture region (x, y, width, height)
CAPTURE_REGION = (1280, 720, 1280, 720) # bottom right
```
This defines the region of the screen that the program captures. My monitor has a resolution of 2560x1440, so the code above captures the bottom right of my screen. You might have to adjust this based on your resolution and how big your game window is. You could make it capture your whole screen but that may slow down your computer. 