from tkinter import *
from PIL import ImageGrab
import pyautogui
from datetime import datetime
import ctypes
from pathlib import Path

def endApplication(event):
    root.destroy()

def validate_input(value):
    return value.isdigit() or value == ""

def validate_coordinates(x1, x2, y1, y2):
    valid=True
    if(x1<0 or x1>winWidth):
        x1Label.configure(bg='red')
        valid=False
    if(y1<0 or y1>winHeight):
        y1Label.configure(bg='red')
        valid=False
    if(x2<0 or x2>winWidth or x1==x2):
        x2Label.configure(bg='red')
        valid=False
    if(y2<0 or y2>winHeight or y1==y2):
        y2Label.configure(bg='red')
        valid=False
    return valid

def resetLabelBackground():
    x1Label.configure(bg=originalBackground)
    y1Label.configure(bg=originalBackground)
    x2Label.configure(bg=originalBackground)
    y2Label.configure(bg=originalBackground)

def updateCoords():
    x, y = pyautogui.position()
    liveCoords.config(text=f"X: {x}, Y: {y}")
    miscFrame.after(100, updateCoords)

# event used to detect keypress change despite not using in code block
def setStartingCoords(event = Event):
    global startedView
    x, y = pyautogui.position()
    x1Coord.set(value=x)
    y1Coord.set(value=y)
    if (startedView == 0):
        startedView = 1
    createWindowForPlus('start')

def setEndingCoords(event = Event):
    global startedView
    x, y = pyautogui.position()
    x2Coord.set(value=x)
    y2Coord.set(value=y)
    if (startedView == 1):
        startedView = 2
    createWindowForPlus('end')

def createPlusSign(canvas, x, y, size, color):
    canvas.create_line(x - size, y, x + size, y, fill=color, width=2)
    canvas.create_line(x, y - size, x, y + size, fill=color, width=2)
        
def createBorder():
    x1, y1 = int(x1Coord.get()), int(y1Coord.get())
    x2, y2 = int(x2Coord.get()), int(y2Coord.get())
    w=abs(x1-x2)
    h=abs(y1-y2)
    borderWindow.geometry("%dx%d+%d+%d" % (w,h,min(x1,x2), min(y1,y2)))
    return

def openFileExplorer():
    ctypes.windll.shell32.ShellExecuteW(None, "open", str(directory), None, None, 1)
    return

def infoClicked():
    global showInfo
    if (showInfo):
        infoWindow.withdraw()
    else:
        infoWindow.deiconify()
    showInfo = not showInfo
    return

def snapClicked(event=Event):
    # gets coords, if empty set to opposite corners of screen
    x1 = int(x1Coord.get() if x1Coord.get() != '' else 0) 
    x2 = int(x2Coord.get() if x2Coord.get() != '' else winWidth) 
    y1 = int(y1Coord.get() if y1Coord.get() != '' else 0) 
    y2 = int(y2Coord.get() if y2Coord.get() != '' else winHeight) 

    if(not validate_coordinates(x1, x2, y1, y2)):
        return
    
    # Hides window to take screenshot without this application in the way
    hideAllWindows()
    screenshot(x1=x1, y1=y1, x2=x2, y2=y2)
    showAllWindows()

def hideAllWindows():
    root.withdraw()
    startWindow.withdraw()
    endWindow.withdraw()
    borderWindow.withdraw()

def showAllWindows():
    root.deiconify()
    startWindow.deiconify()
    endWindow.deiconify()
    borderWindow.deiconify()
    toggleVisuals()

def changeVisualView(event = Event):
    global toggleVisual
    if (toggleVisual == 2):
        toggleVisual = 0
    else:
        toggleVisual += 1
    toggleVisuals()

def toggleVisuals():
    createBorder()
    match toggleVisual:
        case 0:
            startWindow.deiconify()
            endWindow.deiconify()
            if (startedView == 2):
                borderWindow.deiconify()
            return
        case 1:
            startWindow.deiconify()
            endWindow.deiconify()
            borderWindow.withdraw()
            return
        case 2:
            startWindow.withdraw()
            endWindow.withdraw()
            borderWindow.withdraw()
            return
    return

def screenshot(x1, y1, x2, y2):
    resetLabelBackground()
    directory.mkdir(parents=True, exist_ok=True)
    today=str(datetime.today().strftime('%Y-%m-%d %H:%M:%S')).replace(":","_").replace(" ","_")
    screenshot = ImageGrab.grab(bbox=(x1 if x1<x2 else x2, y1, x2 if x1<x2 else x1, y2), include_layered_windows=False, all_screens=True)
    screenshot.save(f"{str(directory)}/Snap_{today}.png", format="PNG")

def updatePlusLocation(position, xCord, yCord):
    createWindowForPlus(position, xCord, yCord)

def createWindowForPlus(position, newX=None, newY=None):
    # sets window to where user inputs number
    if(newX and newY):
        x, y = int(newX.get() or 0), int(newY.get() or 0)
    # sets window based on cursor location from shortcuts <F1>, <F2>
    else:
        x, y = pyautogui.position()
    xPos = x-10
    yPos = y-12
    toggleVisuals()
    match position:
        case 'start':
            startWindow.geometry("30x30+%d+%d" % (xPos, yPos))
            return
        case 'end':
            endWindow.geometry("30x30+%d+%d" % (xPos, yPos))
            return

# Keeps window on top
root = Tk()
root.resizable(0,0)
root.focus_force()
root.attributes(toolwindow=1)
root.title("Snap Screen")
root.attributes('-topmost', True)

# Get window dimensions & color
user32 = ctypes.windll.user32
winWidth, winHeight = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)

# Variables
originalBackground = root.cget("background")
x1Coord = StringVar(value=1)
y1Coord = StringVar(value=1)
x2Coord = StringVar(value=winWidth)
y2Coord = StringVar(value=winHeight)
green = "#adf0ad"
red = "#f0adad"
toggleVisual=0 # 0 = plus & border, 1 = plus, 2 = none
startedView=0 # 1 = F1 or F2 clicked once, 2 = both clicked and can display border
showInfo = False
home_dir = str(Path.home()).replace("\\","/")
directory = Path(home_dir+"/Pictures/Screenshots_Snap_Screen/")

# Window for plus signs, border, and info
startWindow = Toplevel()
startWindow.attributes('-transparentcolor', startWindow['bg'])
startWindow.overrideredirect(True)
startCanvas = Canvas(startWindow, width=12, height=12)
startCanvas.pack()
startCanvas.place(x=1,y=1)
startWindow.withdraw()

endWindow = Toplevel()
endWindow.attributes('-transparentcolor', endWindow['bg'])
endWindow.overrideredirect(True)
endCanvas = Canvas(endWindow, width=12, height=12)
endCanvas.pack()
endCanvas.place(x=1,y=1)
endWindow.withdraw()

borderWindow = Toplevel(highlightthickness=1, highlightbackground='gray', highlightcolor='gray')
borderWindow.attributes('-transparentcolor', borderWindow['bg'])
borderWindow.overrideredirect(True)
borderWindow.withdraw()

infoWindow = Toplevel()
infoWindow.attributes(toolwindow=1)
infoWindow.geometry("360x150")
infoWindow.overrideredirect(True)
infoWindow.resizable(0,0)
infoWindow.withdraw()

# Frame partitions root window into blocks/containers
firstCoordsFrame = Frame(root)
secondCoordsFrame = Frame(root)
miscFrame = Frame(root)
snapFrame = Frame(root)

# Validation for input
validate_func = root.register(validate_input)

# UI components
x1Label = Label(firstCoordsFrame, text = 'X1:')
y1Label = Label(firstCoordsFrame, text = 'Y1:')
x1Entry = Entry(firstCoordsFrame, textvariable = x1Coord, width=6, validate="key", validatecommand=(validate_func, "%P"))
y1Entry = Entry(firstCoordsFrame, textvariable = y1Coord, width=6, validate="key", validatecommand=(validate_func, "%P"))


x2Label = Label(secondCoordsFrame, text = 'X2:')
y2Label = Label(secondCoordsFrame, text = 'Y2:')
x2Entry = Entry(secondCoordsFrame, textvariable = x2Coord, width=6, validate="key", validatecommand=(validate_func, "%P"))
y2Entry = Entry(secondCoordsFrame, textvariable = y2Coord, width=6, validate="key", validatecommand=(validate_func, "%P"))

infoText = Text(infoWindow)
infoText.insert(INSERT, "How to use:\n")
infoText.insert(INSERT, "<F1> - Starting Corner\n")
infoText.insert(INSERT, "<F2> - Ending Corner\n")
infoText.insert(INSERT, "<F3> or [Snap] button - Screenshot\n")
infoText.insert(INSERT, "<F4> - Toggle Visual Indicators\n")
infoText.insert(INSERT, "<Escape> - End Application\n")
infoText.insert(INSERT, "[?] button - How to use panel \n")
infoText.insert(INSERT, "[O] button - Directory of saved snaps\n")
infoText.insert(INSERT, "** Only works when application is focused **")
infoText.config(state=DISABLED)
infoText.pack()

liveCoords = Label(miscFrame, text = 'X: 0, Y: 0', width=12)
snapBtn=Button(snapFrame, text = 'Snap', command = snapClicked,  width=13)
infoBtn=Button(snapFrame, text = '?', command = infoClicked, width=1)
fileExplorerBtn=Button(snapFrame, text = 'O', command = openFileExplorer, width=1)

# Tracking user input
x1Coord.trace_add("write", lambda var, index, mode:  updatePlusLocation('start', x1Coord, y1Coord))
y1Coord.trace_add("write", lambda *args:  updatePlusLocation('start', x1Coord, y1Coord))
x2Coord.trace_add("write", lambda *args:  updatePlusLocation('end', x2Coord, y2Coord))
y2Coord.trace_add("write", lambda *args:  updatePlusLocation('end', x2Coord, y2Coord))

# Organize frames
firstCoordsFrame.pack(side=TOP)
secondCoordsFrame.pack()
miscFrame.pack()
snapFrame.pack()

x1Label.pack(side=LEFT)
x1Entry.pack(side=LEFT)
y1Label.pack(side=LEFT)
y1Entry.pack(side=LEFT)

x2Label.pack(side=LEFT)
x2Entry.pack(side=LEFT)
y2Label.pack(side=LEFT)
y2Entry.pack(side=LEFT)

infoBtn.pack(side=LEFT)
fileExplorerBtn.pack(side=LEFT)
snapBtn.pack(side=BOTTOM, fill=X, expand=True)
liveCoords.pack()

createPlusSign(startCanvas, x=10, y=10, size=4, color=green)
createPlusSign(endCanvas, x=10, y=10, size=4, color=red)
updateCoords()
root.bind("<F1>", setStartingCoords)
root.bind("<F2>", setEndingCoords)
root.bind("<F3>", snapClicked)
root.bind("<F4>", changeVisualView)
root.bind("<Escape>", endApplication)

try:
    mainloop()
except KeyboardInterrupt:
    print("Interupted")