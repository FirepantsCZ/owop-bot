import sys
import os
import json
import time
import signal
import pyautogui
import keyboard
import PyQt5
from PIL import Image
from PIL import ImageChops
from PyQt5 import QtWidgets, QtCore, QtWidgets
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Firefox()
driver.get("https://ourworldofpixels.com/fuco")
driver.find_element_by_xpath('//button[normalize-space()="OK"]').click()
#from PyQt5.QtWidgets import *

loadi = int(json.loads(open("pixe.json", "r").read())[0].get("i"))
loadj = int(json.loads(open("pixe.json", "r").read())[0].get("j"))
lastfile = json.loads(open("pixe.json", "r").read())[0].get("lastfile")
customsize = json.loads(open("pixe.json", "r").read())[0].get("customsize")

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
        global fileName
        global lastfile
        global customsize

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        while True:
            if contmode:
                fileName = lastfile
            else:
                fileName = self.openFileNameDialog()
                self.hide()
            lastfile = fileName
            image = Image.open(fileName)
            print(image.size)
            if not contmode:
                cust = input("Vlastní velikost? [Y/N]")
                if cust == "y" or cust == "Y":
                    crust = input("Udržet poměr stran? [Y/N]")
                    if crust == "y" or crust == "Y":
                        usersizewidth = int(
                            input("Image width (owop pixels): "))
                        usersizeheight = int(
                            input("Image height (owop pixels): "))
                        image.thumbnail((usersizewidth, usersizeheight))
                    else:
                        usersizewidth = int(
                            input("Image width (owop pixels): "))
                        usersizeheight = int(
                            input("Image height (owop pixels): "))
                        image.resize(usersizewidth, usersizeheight)
                    customsize = (usersizewidth, usersizeheight)
                else:
                    customsize = "none"
                    image.save("botimage.png")
            else:
                if customsize != "none":
                    custx, custy = tuple(customsize)
                    print(tuple(customsize))
                    botimage = image.resize(tuple(customsize))
                    print("Found previous custom size, resizing to " +
                          str(customsize))
                    botimage.save("botimage.png")
                    botimage.close()
                else:
                    print(
                        "No custom size found, defaulting to original size" + str(image.size))
                    image.save("botimage.png")

            """if image.size > (400, 300):
                print("image too larege, resizing!")
                crust = input("Udržet poměr stran? [Y/N]")
                if crust == "y" or crust == "Y":
                    new_image = image.thumbnail((400, 300))
                else:
                    new_image = image.resize((400, 300))
                new_image.save("botimage.png")
            else:
                print("image size smaller, not resizing...")
                image.save("botimage.png")"""
            # botimage.save("botimage.png")
            print(image.size)
            image.close()
            #global lastfile
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
                i = loadi
                for i in range(loadi, imageheight):
                    pyautogui.moveTo(horpos, vertpos)
                    j = loadj
                    while j < imagewidth:
                        # for j in range(loadj, imagewidth):
                        currentMouseX, currentMouseY = pyautogui.position()
                        reconnect = driver.find_element_by_id('load-options')
                        vis = reconnect.get_attribute("class")
                        print("Class is: " + vis)
                        if vis == "framed":
                            driver.find_element_by_id("reconnect-btn").click()
                            time.sleep(5)
                            pyautogui.click()
                            print("clicked")
                            time.sleep(1)
                            pyautogui.click()
                            print("clicked")
                            #j -= 2
                            #pyautogui.moveTo(currentMouseX - 6, currentMouseY)
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
                        if vis == "framed":
                            try:
                                driver.find_element_by_id(
                                    "reconnect-btn").click()
                                time.sleep(5)
                                pyautogui.click()
                                print("clicked")
                                time.sleep(1)
                                pyautogui.click()
                                print("clicked")
                            except:
                                print("button not on screen")
                        pyautogui.click()
                        if vis == "framed":
                            try:
                                driver.find_element_by_id(
                                    "reconnect-btn").click()
                                time.sleep(5)
                                pyautogui.click()
                                print("clicked")
                                time.sleep(1)
                                pyautogui.click()
                                print("clicked")
                            except:
                                print("button not on screen")
                        oldcol = hexcol
                        oldr = r
                        oldg = g
                        oldb = b
                        jdump = [
                            {"i": i, "j": j, "lastfile": lastfile, "customsize": customsize}]
                        print(jdump)
                        open("pixe.json", "w").write(json.dumps(jdump))
                        # time.sleep(0.5)
                        j += 1
                    loadj = 0
                    horpos = (markx + maxmarkx) + 2
                    vertpos += 3
                    jdump = [{"i": 0, "j": 0, "lastfile": lastfile,
                              "customsize": customsize}]
                    print(jdump)
                    open("pixe.json", "w").write(json.dumps(jdump))
                print("Finished drawing!")
                print("Press s to capture differences")
                keyboard.wait("s")
                keyboard.press_and_release("g")
                image1 = pyautogui.screenshot("finished.png", region=(markx + maxmarkx + 3, marky + maxmarky, imagewidth * 3, imageheight * 3)).convert("RGB").resize((10, 10))
                image2 = Image.open("botimage.png").convert("RGB")
                print(image1.size)
                print(image2.size)
                diff = ImageChops.difference(image1, image2)
                diff.save("diff.png")
                print(diff.mode)
                compwidth, compheight = image1.size
                for i in range(compheight):
                    for j in range(compwidth):
                        print(str(i) + " " + str(j))
                        r1, g1, b1 = image1.getpixel((j,i))
                        r2, g2, b2 = image2.getpixel((j,i))
                        rdif = abs(r1 - r2)
                        gdif = abs(g1 - g2)
                        bdif = abs(b1 - b2)

                        r, g, b = diff.getpixel((j,i))
                        brightness = r + g + b
                        print("red: " + str(r))
                        print("green: " + str(g))
                        print("blue: " + str(b))
                        print(brightness)
                        print("red difference: " + str(rdif))
                        print("green difference: " + str(gdif))
                        print("blue difference: " + str(bdif))
                diff.close()
                image1.close()
                image2.close()
                sys.exit()
            time.sleep(0.05)

    def openFileNameDialog(self):
        options = PyQt5.QtWidgets.QFileDialog.Options()
        options |= PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = PyQt5.QtWidgets.QFileDialog.getOpenFileName(
            self, "Choose file", "", "Image Files (*.png *.jpg);;All Files (*)", options=options)
        if fileName:
            print(fileName)
            return fileName


def mousestat():
    global showmousepos
    if showmousepos == False:
        showmousepos = True
    else:
        showmousepos = False


keyboard.add_hotkey('h', lambda: os.kill(os.getpid(), signal.SIGINT))
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