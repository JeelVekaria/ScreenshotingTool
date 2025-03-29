from tkinter import *
from PIL import ImageGrab
import pyautogui
from datetime import datetime
import ctypes

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
    if(x2>winWidth or x2<=x1):
        x2Label.configure(bg='red')
        valid=False
    if(y2>winHeight or y2<=y1):
        y2Label.configure(bg='red')
        valid=False
    return valid

def update_coords():
    x, y = pyautogui.position()
    liveCoords.config(text=f"X: {x}, Y: {y}")
    firstCoordsFrame.after(100, update_coords)

def submit():
    today=str(datetime.today().strftime('%Y-%m-%d %H:%M:%S')).replace(":","_").replace(" ","_")
    x1 = int(x1Coord.get() if x1Coord.get() != '' else 0) 
    x2 = int(x2Coord.get() if x2Coord.get() != '' else winWidth) 
    y1 = int(y1Coord.get() if y1Coord.get() != '' else 0) 
    y2 = int(y2Coord.get() if y2Coord.get() != '' else winHeight) 

    if(not validate_coordinates(x1, x2, y1, y2)):
        return
    
    # Hides window to take screenshot without this application in the way
    root.withdraw()
    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2), include_layered_windows=False, all_screens=True)
    screenshot.save("Snap_"+today+".png", format="PNG")
    root.deiconify()

# Keeps window on top
root = Tk()
root.resizable(0,0)
root.attributes(toolwindow=1)
root.title("Snap Screen")
root.attributes('-topmost', True)

# Get window dimensions
user32 = ctypes.windll.user32
winWidth, winHeight = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)

# Frame partitions root window into blocks/containers
firstCoordsFrame = Frame(root)
secondCoordsFrame = Frame(root)
miscFrame = Frame(root)

# Validation for input
validate_func = root.register(validate_input)

# UI components
x1Label = Label(firstCoordsFrame, text = 'X1:')
y1Label = Label(firstCoordsFrame, text = 'Y1:')
x1Coord = StringVar(value=1)
y1Coord = StringVar(value=1)
x1Entry = Entry(firstCoordsFrame, textvariable = x1Coord, width=6, validate="key", validatecommand=(validate_func, "%P"))
y1Entry = Entry(firstCoordsFrame, textvariable = y1Coord, width=6, validate="key", validatecommand=(validate_func, "%P"))

x2Label = Label(secondCoordsFrame, text = 'X2:')
y2Label = Label(secondCoordsFrame, text = 'Y2:')
x2Coord = StringVar(value=winWidth)
y2Coord = StringVar(value=winHeight)
x2Entry = Entry(secondCoordsFrame, textvariable = x2Coord, width=6, validate="key", validatecommand=(validate_func, "%P"))
y2Entry = Entry(secondCoordsFrame, textvariable = y2Coord, width=6, validate="key", validatecommand=(validate_func, "%P"))

liveCoords = Label(miscFrame, text = 'X: 0, Y: 0', width=12)
sub_btn=Button(miscFrame,text = 'Snap', command = submit)

x1, x2, y1, y2 = 1, 1, 500, 500

# Organize frames
firstCoordsFrame.pack(side=TOP)
secondCoordsFrame.pack()
miscFrame.pack(side=BOTTOM)

x1Label.pack(side=LEFT)
x1Entry.pack(side=LEFT)
y1Label.pack(side=LEFT)
y1Entry.pack(side=LEFT)

x2Label.pack(side=LEFT)
x2Entry.pack(side=LEFT)
y2Label.pack(side=LEFT)
y2Entry.pack(side=LEFT)

sub_btn.pack(side=RIGHT)
liveCoords.pack()

update_coords()
mainloop()