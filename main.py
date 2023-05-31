import win32gui, win32con, win32ui
import numpy as np
import cv2 as cv
import pydirectinput as pd

pd.PAUSE = 0 #set pydirectinput delay to 0

#get screenshot
def screenshot():
    w = 130 #change according to resolution
    h = 100 #change according to resolution
    
    hwnd = win32gui.FindWindow(None, 'winnable')

    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (805, 350), win32con.SRCCOPY)

    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (h,w,4)


    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    img = img[...,:3]
    img = np.array(img)
    return img

#find matches
def coords(image, path):
    coordinates = []

    #cc img
    cc_img = cv.imread(path, cv.IMREAD_UNCHANGED)
    
    #do template matching
    result = cv.matchTemplate(image, cc_img, cv.TM_CCORR_NORMED)

    #filter
    threshold = 0.98 #might have to change
    yloc, xloc = np.where(result >= threshold)

    #fill in coordinates
    for x,y in zip(xloc,yloc):
        coordinates.append([x,y])

    #return
    try:
        if coordinates != []:
            return 1
        else:
            return 0
    except:
        return None
clearCC = [True, True, True, True, True] #select which ccs to cleanse

while True:
    img = screenshot() #get screenshot
    blind = coords(img, "CC\\blind.jpg") #blinded?
    charm = coords(img, "CC\\charm.jpg") #charmed?
    root = coords(img, "CC\\root.jpg") #rooted?
    stun = coords(img, "CC\\stun.jpg") #stunned?
    taunt = coords(img, "CC\\taunt.jpg") #tauned?
    cc = [blind, charm, root, stun, taunt] #list of cc to iterate through

    x = 0
    for c in cc:
        if c == 1 and clearCC[x] == True: #if cc'd and cc type is selected as to be cleansed
            pd.keyDown('f') #cleanse on f
            pd.keyUp('f')
        x += 1
