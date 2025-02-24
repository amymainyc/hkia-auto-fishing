import time
import pyautogui
import numpy as np
import torch
import warnings
import vgamepad as vg
import keyboard  # For listening to F12 key

# Suppress the specific FutureWarning from torch.cuda.amp.autocast
warnings.filterwarnings("ignore", message=".*torch.cuda.amp.autocast.*")

# Load your trained YOLOv5 model using torch.hub
model = torch.hub.load(
    repo_or_dir='yolov5', 
    model='custom', 
    path=f'best.pt', 
    source='local'
)
model.conf = 0.5  # Set confidence threshold

# Define the screen capture region (x, y, width, height)
CAPTURE_REGION = (1280, 720, 1280, 720) # bottom right
# CAPTURE_REGION = (0, 720, 1280, 720) # bottom left

# Timing parameters
RECAST_DELAY = 2    # If no arrow is detected for this many seconds, recast
TIMEOUT = 15        # Additional delay before another recast can occur
HOLD_BUFFER = 0.4   # Continue holding the stick direction for this many seconds after the arrow disappears
RECAST_TOO_LONG = 60  # If recasting has been active for more than 60 seconds, reposition character

# Initialize the virtual gamepad
gamepad = vg.VX360Gamepad()

# Global state variables to track whether a D-pad button is held down
left_pressed = False
right_pressed = False

# Global pause flag and debounce time for toggling pause
paused = False
last_toggle_time = 0
TOGGLE_DEBOUNCE = 1  # seconds

# We'll use this variable to track how long recasting has been occurring
recast_start_time = None

def press_left():
    """Press (and hold) the D-pad left if not already held."""
    global left_pressed
    if not left_pressed:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        gamepad.update()
        left_pressed = True

def release_left():
    """Release the D-pad left if it is currently held."""
    global left_pressed
    if left_pressed:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        gamepad.update()
        left_pressed = False

def press_right():
    """Press (and hold) the D-pad right if not already held."""
    global right_pressed
    if not right_pressed:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        gamepad.update()
        right_pressed = True

def release_right():
    """Release the D-pad right if it is currently held."""
    global right_pressed
    if right_pressed:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        gamepad.update()
        right_pressed = False

def press_a():
    """Simulate pressing the controller's A button."""
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(0.2)
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()

def press_x():
    """Simulate pressing the controller's X button."""
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    gamepad.update()
    time.sleep(0.2)
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    gamepad.update()

def reposition_character():
    """Reposition the character by nudging the left stick vertically."""
    time.sleep(0.2)
    gamepad.left_joystick(0, 10000)
    gamepad.update()
    time.sleep(0.1)
    gamepad.left_joystick(0, 0)
    gamepad.update()
    time.sleep(0.2)

def main():
    global left_pressed, right_pressed, paused, last_toggle_time, recast_start_time
    print("Starting arrow detection. Press Ctrl+C to stop.")
    # Track the last time any left/right arrow was detected (for recast logic)
    last_arrow_time = time.time()
    # Track the last time we recast the line
    last_recast_time = None
    # Track the last detection times for left and right arrows separately
    last_left_time = time.time()
    last_right_time = time.time()
    
    while True:
        # Check for pause/resume toggle with F10 (debounced)
        if keyboard.is_pressed('F10') and (time.time() - last_toggle_time) > TOGGLE_DEBOUNCE:
            paused = not paused
            last_toggle_time = time.time()
            if paused:
                print("Program paused. Press F10 to resume.")
            else:
                print("Program resumed.")
            time.sleep(0.5)  # debounce
        
        # If paused, wait and do not process detection
        if paused:
            time.sleep(0.2)
            continue

        # Capture a screenshot of the defined region
        screenshot = pyautogui.screenshot(region=CAPTURE_REGION)
        # Convert the screenshot (PIL Image) to a NumPy array (RGB)
        frame = np.array(screenshot)

        # Run object detection with YOLOv5
        results = model(frame)
        
        # Get detections: each detection row is [x1, y1, x2, y2, conf, class]
        detections = results.xyxy[0].cpu().numpy()
        
        # Initialize detection flags for this iteration
        arrow_left_detected = False
        arrow_right_detected = False
        arrow_detected = False
        current_time = time.time()

        if len(detections) > 0:
            # Choose the detection with the highest confidence
            best_detection = detections[np.argmax(detections[:, 4])]
            # Unpack: box = [x1, y1, x2, y2], conf, cls_id
            *box, conf, cls_id = best_detection
            cls_id = int(cls_id)
            # Process based on class
            if cls_id == 0:  # fish_alert
                press_x()
                print("Detected fish_alert, pressed controller X")
                last_arrow_time = current_time
                time.sleep(2.7)  # Wait for the fish to bite
            elif cls_id == 1:  # fish_caught
                press_a()  # Close the fish caught menu
                recast_start_time = current_time
                print("Detected fish_caught, pressed controller A")
            elif cls_id == 2:  # left_arrow
                arrow_left_detected = True
                arrow_detected = True
                last_arrow_time = current_time
                last_left_time = current_time
                print("Detected left_arrow with confidence", conf)
            elif cls_id == 3:  # right_arrow
                arrow_right_detected = True
                arrow_detected = True
                last_arrow_time = current_time
                last_right_time = current_time
                print("Detected right_arrow with confidence", conf)
        else:
            arrow_detected = False

        # For left arrow: if detected OR within HOLD_BUFFER after last detection, hold left
        if arrow_left_detected or (current_time - last_left_time < HOLD_BUFFER):
            # Instead of pressing DPAD left, use stick control in your other code if desired.
            # For now, we simply simulate "holding left" via your existing mechanism.
            press_left()
        else:
            release_left()
        
        # For right arrow: if detected OR within HOLD_BUFFER after last detection, hold right
        if arrow_right_detected or (current_time - last_right_time < HOLD_BUFFER):
            press_right()
        else:
            release_right()

        # Recast logic: if no arrow detected for RECAST_DELAY seconds and enough time has passed since last recast
        if (not arrow_detected and 
            (current_time - last_arrow_time) > RECAST_DELAY and
            (last_recast_time is None or (current_time - last_recast_time) > TIMEOUT)):
            
            # Start or update recasting timer
            if recast_start_time is None:
                recast_start_time = current_time
            elif (current_time - recast_start_time) > RECAST_TOO_LONG:
                reposition_character()
                print("Recasting for too long. Repositioning character.")
                recast_start_time = current_time  # Reset recast timer after repositioning
            
            press_a() 
            time.sleep(0.5)
            press_x()  # Recast line
            print("No arrow detected for", RECAST_DELAY, "seconds. Recasting line with controller X.")
            last_arrow_time = current_time  # Reset arrow time after recast
            last_recast_time = current_time  # Update recast time
    
        # Short delay to reduce CPU usage
        time.sleep(0.2)

if __name__ == "__main__":
    main()
