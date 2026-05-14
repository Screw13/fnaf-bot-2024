import keyboard
import time
import pyautogui as pp

print(pp.FAILSAFE)  # Make sure failsafe is on
"""
USE THIS TO PRINT COORDS OF MOUSE
try:
     while True:
        time.sleep(1)

        x, y = pp.position()
        position = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(position + "\n", end="")
#         if keyboard.is_pressed('q'):
#             break
except KeyboardInterrupt:
     print("\n")
"""

"""
FNAF coords:
Top Left: 0, 0
Bottom Left: 0, 719
Top Right: 1279, 0
Bottom Right: 1279, 719
So 1280 x 720

Regular screen res is 1920 x 1080
"""
BON = 1
CHI = 0
facingLeft = True
bonnie = False
chica = False
eyes = False

#cam
def toggleCam():
    pp.moveTo(640, 640)
    pp.moveTo(640, 670, 0.1)
    pp.moveTo(640, 640, 0.1)

def pirateCove():
    # Switch to pirate's cove
    pp.moveTo(930, 490)
    pp.click()

def westHall():
    # fox run animation
    pp.moveTo(980, 600)
    pp.click()

def lookLeft():
    global facingLeft
    if not facingLeft:
        pp.moveTo(0, 360)
        time.sleep(0.4)
        facingLeft = True

def lookRight():
    global facingLeft
    if facingLeft:
        pp.moveTo(1279, 360)
        time.sleep(0.4)
        facingLeft = False

def leftDoor():
    lookLeft()
    pp.moveTo(56, 336)
    pp.click()

def leftLightOn():
    lookLeft()
    pp.moveTo(56, 447)
    pp.click()

def leftlightOff():
    pp.moveTo(56, 459)
    pp.click()

def rightDoor():
    lookRight()
    pp.moveTo(1212, 336)
    pp.click()

def rightLightOn():
    lookRight()
    pp.moveTo(1212, 447)
    pp.click()

def rightLightOff():
    pp.moveTo(1212, 459)
    pp.click()

def checkTronic(tronic):
    # Check if tronic is at door.
    # Double checks and lower confidence compensate for flashing lights or errors
    if tronic:
        global bonnie
        if bonnie:  # If Bonnie is already there before, check if still there
            while True:
                bonnieAtDoor = pp.locateOnScreen("bonnieOutside.png", grayscale=True, confidence=0.8) is not None
                if not bonnieAtDoor:
                    bonnieAtDoor = pp.locateOnScreen("bonnieOutside.png", grayscale=True, confidence=0.8) is not None
                    if not bonnieAtDoor:
                        break
                leftlightOff()
                time.sleep(0.2)
                leftLightOn()
                time.sleep(0.1)

        else:  # Check if Bonnie has just arrived at the door
            bonnieAtDoor = pp.locateOnScreen("bonnieAtDoor.png", grayscale=True, confidence=0.6) is not None
            if not bonnieAtDoor:
                bonnieAtDoor = pp.locateOnScreen("bonnieAtDoor.png", grayscale=True, confidence=0.6) is not None
        bonnie = bonnieAtDoor
        return bonnieAtDoor
    else:
        global chica
        if chica:  # If Chica is already there before, check if still there
            while True:
                chicaAtDoor = pp.locateOnScreen("chicaAtDoor.png", grayscale=True, confidence=0.6) is not None  # True is STILL THERE
                if not chicaAtDoor:
                    chicaAtDoor = pp.locateOnScreen("chicaAtDoor.png", grayscale=True, confidence=0.5) is not None
                    if not chicaAtDoor:
                        break
                rightLightOff()
                time.sleep(0.2)
                rightLightOn()
        else:  # Check if Chica has just arrived at the door
            chicaAtDoor = pp.locateOnScreen("chicaAtDoor.png", grayscale=True, confidence=0.6) is not None
            if not chicaAtDoor:
                chicaAtDoor = pp.locateOnScreen("chicaAtDoor.png", grayscale=True, confidence=0.6) is not None
        chica = chicaAtDoor
        time.sleep(0.1)  # Delay, the game doesn't like responses too fast for right door
        return chicaAtDoor


def checkBonnie():
    leftLightOn()
    if bonnie != checkTronic(BON):
        leftDoor()
    leftlightOff()

def checkChica():
    rightLightOn()
    if chica != checkTronic(CHI):
        rightDoor()
    rightLightOff()

def checkFoxy():
    # Foxy is there
    global eyes
    if eyes:
        # Check if Foxy is gone, after already seeing his second stage
        if pp.locateOnScreen("foxyEye.png", grayscale=True, confidence=0.6) is None:
            if pp.locateOnScreen("foxyEye.png", grayscale=True, confidence=0.6) is None:
                eyes = False
                return True
    else:
        # Check for Foxy's second stage, one before he's gone
        if pp.locateOnScreen("foxyEye.png", grayscale=True, confidence=0.6) is not None:
            if pp.locateOnScreen("foxyEye.png", grayscale=True, confidence=0.5) is not None:
                eyes = True
    return False

def stopFoxy():
    # Change to west hall
    westHall()
    pirateCove()

# Bot plays
def autoPlay():
    global bonnie
    global chica
    global eyes
    stopped = False
    while True:
        bonnie = False
        chica = False
        eyes = False
        pp.moveTo(312, 631)  # Custom night button
        pp.click()
        time.sleep(2)
        pp.moveTo(1140, 656)  # Ready button
        pp.click()
        time.sleep(9)  # Wait for game to load
        # Stalling at the beginning
        time.sleep(3)
        lookRight()
        toggleCam()  # up
        time.sleep(0.3)
        pirateCove()
        time.sleep(0.3)
        toggleCam()  # down
        time.sleep(3)
        toggleCam()  # up
        time.sleep(0.3)
        toggleCam()  # down
        time.sleep(3)
        toggleCam()  # up
        time.sleep(0.3)
        toggleCam()  # down
        time.sleep(3)
        toggleCam()  # up
        time.sleep(0.3)
        toggleCam()  # down
        time.sleep(3)

        timeout = 435  # 7 min 15 s
        start = time.time()
        while time.time() < start + timeout:
            if not chica:
                rightDoor()
                if stopped:  # If foxy attacked, check Chica
                    chica = True
                    stopped = False
            toggleCam()
            time.sleep(0.4)
            # If Foxy left cove, change to west hall and close left door (if open)
            if checkFoxy():
                stopFoxy()
                toggleCam()
                if not chica:
                    rightDoor()
                    stopped = True
                if not bonnie:
                    leftDoor()
                    bonnie = True
                time.sleep(0.5)
            else:
                toggleCam()
                if not chica:
                    rightDoor()
                checkChica()
            checkBonnie()
            if not bonnie:
                time.sleep(0.6)
            if pp.locateOnScreen("stars.png", grayscale=True, confidence=0.5) is not None:  # We are on the title screen
                break
        # Stop everything
        time.sleep(0.1)
        if bonnie:
            leftDoor()
        if chica:
            leftDoor()
        # Restart game
        while True:
            if pp.locateOnScreen("stars.png", grayscale=True, confidence=0.5) is not None:  # We are on the title screen
                break
            time.sleep(3)
        # time.sleep(130)  # 130 + 430 is 9min 20s. Wait until game is definitely over


# Other controls for playing/testing
while not keyboard.is_pressed('x'):
    if keyboard.is_pressed('p'):
        autoPlay()
