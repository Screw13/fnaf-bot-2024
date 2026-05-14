import pyautogui as pag
import keyboard

a = 1

while not keyboard.is_pressed('x'):
    if keyboard.is_pressed("p"):
        if a == 1:
            a += 1
            x, y = pag.position()
            position =str(x).rjust(4)+str(y).rjust(4)
            print(position + "\n", end="")
    if keyboard.is_pressed('o'):
        a =1