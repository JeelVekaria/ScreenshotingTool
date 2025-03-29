from tkinter import * # GUI
import pyautogui # mouse events

# Keeps window on top
root = Tk()
root.attributes('-topmost', True)

# Frame partitions root window into blocks/containers
firstCoordsFrame = Frame(root)
secondCoordsFrame = Frame(root)
miscFrame = Frame(root)

def update_coords():
    x, y = pyautogui.position()
    liveCoords.config(text=f"X: {x}, Y: {y}")
    firstCoordsFrame.after(100, update_coords)

def submit():
    x1 = x1Coord.get()
    x2 = x2Coord.get()
    y1 = y1Coord.get()
    y2 = y2Coord.get()
    print(f"({x1},{y1}), ({x2},{y2})" )
    

x1Label = Label(firstCoordsFrame, text = 'X1:')
y1Label = Label(firstCoordsFrame, text = 'Y1:')
x1Coord=StringVar()
y1Coord=StringVar()
x1Entry = Entry(firstCoordsFrame, textvariable = x1Coord, width=6)
y1Entry = Entry(firstCoordsFrame, textvariable = y1Coord, width=6)

x2Label = Label(secondCoordsFrame, text = 'X2:')
y2Label = Label(secondCoordsFrame, text = 'Y2:')
x2Coord=StringVar()
y2Coord=StringVar()
x2Entry = Entry(secondCoordsFrame, textvariable = x2Coord, width=6)
y2Entry = Entry(secondCoordsFrame, textvariable = y2Coord, width=6)

liveCoords = Label(miscFrame, text = 'X: 0, Y: 0', width=12)
sub_btn=Button(miscFrame,text = 'Snap', command = submit)

x1, x2, y1, y2 = 0, 0, 0, 0


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