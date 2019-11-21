import tkinter as tk
from tkinter import Tk
from tkinter.filedialog import askopenfilenames

def multfile():
    Tk().withdraw()
    files = askopenfilenames()
    files = list(files)
    finalf = []
    for i in range(len(files)):
        string = files[i]
        ind = 0
        for j in range(len(string)):
            if string[j]=='/':
                ind = j
        string = string[ind+1:len(string)]
        finalf.append(string)
    return finalf