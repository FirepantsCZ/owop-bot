import sys
import os
import json
import time
import signal
import pyautogui
import keyboard
import PyQt5
from PIL import Image
from PyQt5 import QtWidgets, QtCore, QtWidgets
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Firefox()
driver.get("https://ourworldofpixels.com/fuco")
driver.find_element_by_xpath('//button[normalize-space()="OK"]').click()
#from PyQt5.QtWidgets import *

loadi = int(json.loads(open("pixe.json", "r").read())[0].get("i"))
loadj = int(json.loads(open("pixe.json", "r").read())[0].get("j"))
print(str(loadi) + " " + str(loadj))
if loadi != 0 or loadj != 0:
    ans = input("Pokračovat? [Y/N]")
    if ans == "Y" or ans == "y":
        contmode = True
    else:
        contmode = False
        loadi = 0
        loadj = 0
else:
    contmode = False
showmousepos = False
scrollmode = True
markMode = True
oldcol = ""
oldr = ""
oldg = ""
oldb = ""

screenWidth, screenHeight = pyautogui.size()


def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


class App(PyQt5.QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        self.hide()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.openFileNameDialog()
        self.show()

    def openFileNameDialog(self):
        options = PyQt5.QtWidgets.QFileDialog.Options()
        options |= PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = PyQt5.QtWidgets.QFileDialog.getOpenFileName(
            self, "Choose file", "", "Image Files (*.png *.jpg);;All Files (*)", options=options)
        if fileName:
            print(fileName)

        image = Image.open(fileName)
        print(image.size)
        cust = input("Vlastní velikost? [Y/N]")
        if cust == "y" or cust == "Y":
            crust = input("Udržet poměr stran? [Y/N]")
            if crust == "y" or crust == "Y":
                usersizewidth = int(input("Image width (owop pixels): "))
                usersizeheight = int(input("Image height (owop pixels): "))
                image.thumbnail((usersizewidth, usersizeheight))
            else:
                usersizewidth = int(input("Image width (owop pixels): "))
                usersizeheight = int(input("Image height (owop pixels): "))
                image.resize(usersizewidth, usersizeheight)
        if image.size > (400, 300):
            print("image too larege, resizing!")
            crust = input("Udržet poměr stran? [Y/N]")
            if crust == "y" or crust == "Y":
                new_image = image.thumbnail((400, 300))
            else:
                new_image = image.resize((400, 300))
            new_image.save("botimage.png")
        else:
            print("image size smaller, not resizing...")
            image.save("botimage.png")
        image.close()

        while True:
            global scrollmode
            global markMode
            global oldcol
            global loadj
            global oldr
            global oldg
            global oldb

            if scrollmode:
                # keyboard.wait("s")
                # keyboard.press_and_release("g")
                # keyboard.press("ctrl")
                # pyautogui.scroll(-13)
                # keyboard.release("ctrl")
                scrollmode = False
                keyboard.wait("s")

            currentMouseX, currentMouseY = pyautogui.position()
            if showmousepos == True:
                print(currentMouseX, currentMouseY)
            if markMode:
                try:
                    print("looking for mark...")
                    markx, marky, maxmarkx, maxmarky = pyautogui.locateOnScreen(
                        "mark1.png")
                except:
                    print("mark not found, exiting...")
                    sys.exit()
                print("found mark at " + str(markx) + " " + str(marky))
                print("end at " + str(markx + maxmarkx) +
                      " " + str(marky + maxmarky))
                print("moving mouse...")
                #pyautogui.moveTo((markx + maxmarkx) + 2, (marky + maxmarky) + 2)
                #pyautogui.moveTo(markx, marky)
                # pyautogui.click()
                markMode = False
                image = Image.open("botimage.png")
                image = image.convert('RGB')
                imagewidth, imageheight = image.size
                print(range(imageheight))
                print(range(imagewidth))
                if contmode:
                    vertpos = ((marky + maxmarky) + 2) + (loadi * 3)
                    horpos = ((markx + maxmarkx) + 2) + (loadj * 3)
                else:
                    vertpos = (marky + maxmarky) + 2
                    horpos = (markx + maxmarkx) + 2
                for i in range(loadi, imageheight):
                    pyautogui.moveTo(horpos, vertpos)
                    for j in range(loadj, imagewidth):
                        reconnect = driver.find_element_by_id('load-options')
                        vis = reconnect.get_attribute("class")
                        print("Class is: " + vis)
                        if vis == "framed":
                            driver.find_element_by_id("reconnect-btn").click()                        
                            time.sleep(1.5)
                        currentMouseX, currentMouseY = pyautogui.position()
                        print(i, j)
                        r, g, b = image.getpixel((j, i))
                        print(r + g + b)
                        hexcol = rgb2hex(r, g, b)
                        print(hexcol)
                        if r != oldr or g != oldg or b != oldb:
                            script = "OWOP.player.selectedColor = [" + str(
                                r) + ", " + str(g) + ", " + str(b) + "]"
                            driver.execute_script(script)
                        """if hexcol != oldcol:
                            keyboard.press_and_release("f")
                            time.sleep(0.08)
                            keyboard.write(hexcol)
                            #time.sleep(1)
                            keyboard.press_and_release("enter")
                            #time.sleep(0.5)"""
                        pyautogui.moveTo(currentMouseX + 3, currentMouseY)
                        pyautogui.click()
                        oldcol = hexcol
                        oldr = r
                        oldg = g
                        oldb = b
                        jdump = [{"i": i, "j": j}]
                        print(jdump)
                        open("pixe.json", "w").write(json.dumps(jdump))
                        # time.sleep(0.5)
                    loadj = 0
                    horpos = (markx + maxmarkx) + 2
                    vertpos += 3
                print("Finished drawing!")
                sys.exit()

            time.sleep(0.05)


def mousestat():
    global showmousepos
    if showmousepos == False:
        showmousepos = True
    else:
        showmousepos = False


keyboard.add_hotkey('g', lambda: os.kill(os.getpid(), signal.SIGINT))
keyboard.add_hotkey('shift', lambda: mousestat())

# scroll 13x
"""while True:
    if scrollmode:
        keyboard.wait("s")
        keyboard.press_and_release("g")
        keyboard.press("ctrl")
        pyautogui.scroll(-13)
        keyboard.release("control")
        scrollmode = False
        keyboard.wait("s")

    currentMouseX, currentMouseY = pyautogui.position()
    if showmousepos == True:
        print(currentMouseX, currentMouseY)
    try:
        markx, marky = pyautogui.locateCenterOnScreen("mark2.png")
    except:
        print("mark not found, exiting...")
        sys.exit()
    print("found mark at " + str(markx) + " " + str(marky))
    time.sleep(0.05)"""


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
