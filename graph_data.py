import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import random
import os

os.listdir()

aVD_file = ""
a_Pos = ""
v_Pos = ""
d_Pos = ""
flow_File = ""

def fileCollect():

    global aVD_file, a_Pos, v_Pos, d_Pos, a_Entry, v_Entry, d_Entry, aVD_File_entry, flow_File

    def files():

        global aVD_file, a_Pos, v_Pos, d_Pos, a_Entry, v_Entry, d_Entry, aVD_File_entry, flow_File

        aVD_file = aVD_File_entry.get()
        a_Pos =  (a_Entry.get())
        v_Pos =  (v_Entry.get())
        d_Pos =  (d_Entry.get())
        flow_File = (flow_File_Entry.get())
        result_label.config(text=f"Thanks!!" + aVD_file + a_Pos + v_Pos + d_Pos)
        root.destroy()

    #start chatgpt paste
    root = tk.Tk()

    # Create and pack the first entry widget
    tk.Label(root, text="Welcome, this program will sync flow readings to Aortic,Ventric, and Differential Sensor Readings.").pack()
    tk.Label(root, text="To Begin, please paste a txt file of your AVD data into the first space").pack()
    tk.Label(root, text="Please ensure all content in your txt file is purely numerical and is seperated by spaces").pack()
    tk.Label(root, text="Note its is recommended to replace all \ in the path with /").pack()
    tk.Label(root, text="Sample File: AVD_data1_70_(run1)").pack()
    #image entry
    image = Image.open("C:/Users/nitin/Downloads/copy_as_path.jpg")
    resized_image = image.resize((200, 200))
    photo = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(root, image=photo)
    image_label.pack()

    #user input
    aVD_File_entry = tk.Entry(root)
    aVD_File_entry.pack()

    # Create and pack the second entry widget
    tk.Label(root, text="Please enter which slot your Aortic readings are in (DNE if you dont have aortic readings)").pack()
    a_Entry = tk.Entry(root)
    a_Entry.pack()

    tk.Label(root, text="Please enter which slot your Ventric readings are in (DNE if you dont have aortic readings)").pack()
    v_Entry = tk.Entry(root)
    v_Entry.pack()

    tk.Label(root, text="Please enter which slot your Differential readings are in (DNE if you dont have aortic readings)").pack()
    d_Entry = tk.Entry(root)
    d_Entry.pack()

    tk.Label(root, text="Please enter the file for the Flow Readings").pack()
    tk.Label(root, text="Sample File: Flow_Run_1").pack()
    flow_File_Entry = tk.Entry(root)
    flow_File_Entry.pack()


    # Create and pack the submit button
    tk.Button(root, text="Submit", command=files).pack()

    # Create and pack the result label
    result_label = tk.Label(root, text="")
    result_label.pack()

    root.mainloop()

fileCollect()

##################################################################################################

#Opening the files
# data_AVD value on local system = AVD_data1_70_(run1)
data_AVD = open( aVD_file,"r")
data_Flow = open(flow_File, "r")

#Setting waveform shift (found by the heartrate waveform)
shiftWaveform = 394

#Opening Arrays for datasets
Aortic = []
Differential = []
Ventric = []
Flow = []
time = []

#For loop indexes from 0 to max times
for i in range(10000):

    #Reads data on a lineByline case
    AVD = data_AVD.readline()
    FloRead = data_Flow.readline()

    #Splits out read data and assigns a variable to it
    #if statement checks if any values are DNE
    if a_Pos.lower() != "dne":
        aNum = AVD.split()[int(a_Pos)] #insert user input values for nums here
        Aortic.append(float(aNum)) # Appends to seperate array/list
    
    if d_Pos.lower() != "dne":
        dNum = AVD.split()[int(d_Pos)]
        Differential.append(float(dNum))
    
    if v_Pos.lower() != "dne":
        vNum = AVD.split()[int(v_Pos)]
        Ventric.append(float(vNum))
    
    fNum = FloRead.split()[1]  
    Flow.append(float(fNum))

    #Time array
    time.append(i)

### Code for tkinter window displaying raw graphs for differential, aortic and ventricular data




# threshold is 20, if 5 greater then 20 keep the value, then finds peak after 25, cuts off at time of 4 to prevent any miscatches
flPeak = 0
tPeakFlo = 0
j = 0 
for j in range(4000):
    if Flow[j] > 25:
        if Flow[j] > flPeak:
            flPeak = Flow[j]
            tPeakFlo = j

#testing the output values
print (tPeakFlo)


# Aortic time shift function

timeAor = []
def aorticShift():
    #reversed for the aortic
    venSPeak = 0
    tSPeakAor = 0
    for k in range(9999, 3500, -1):
        if Aortic[k] > venSPeak:
            venSPeak = Aortic[k]
            tSPeakAor = k

    #shifting time back by diffence in peaks
    for l in range(10000):
        timeAor.append(l - (tSPeakAor - tPeakFlo) + shiftWaveform)

aorticShift()

#Ventric time shift function
timeVen = []
def ventricShift():
    #reversed for ventricular
    venSPeak = 0
    tSPeakVen = 0
    for k in range(9999, 3500, -1):
        if Ventric[k] > venSPeak:
            venSPeak = Ventric[k]
            tSPeakVen = k
    
    #shifting time back by diffence in peaks
    for l in range(10000):
        timeVen.append(l - (tSPeakVen - tPeakFlo) + shiftWaveform)

ventricShift()


#Ventric time shift function
timeDiff = []
def diffShift():
    #reversed for ventricular
    diffSPeak = 0
    tSPeakDiff = 0
    for k in range(3500, 4200):
        if Differential[k] > diffSPeak:
            diffSPeak = Differential[k]
            tSPeakDiff = k
    
    #shifting time back by diffence in peaks
    for l in range(10000):
        timeDiff.append(l - (tSPeakDiff - tPeakFlo) + shiftWaveform)
    print (tSPeakDiff)

diffShift()


#Setting up base graph with Flow meter values
plt.plot(time,Flow,"#aa00ffff" )



# Sub graphs for Aortic,Ventric & Differential
fig, Aorf = plt.subplots()
fig, Ven = plt.subplots()
fig, Diff = plt.subplots()



#Plotting Differential Sub plot
Diff.plot( timeVen, Differential, "b--", linewidth = 1)
Diff.plot(time,Flow,"#aa00ffff" )



#Plotting Aortic Sub Plot
Aorf.plot (timeVen, Aortic, "g--", linewidth = 1)
Aorf.plot(time,Flow,"#aa00ffff")



#Plotting Ventricular Sub Plot
Ven.plot( timeVen, Ventric, "r--", linewidth = 1)
Ven.plot(time,Flow,"#aa00ffff" )




#Showing Graph
plt.show()







#Closing files
data_AVD.close
data_Flow.close
