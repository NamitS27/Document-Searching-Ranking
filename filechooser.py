import tkinter as tk
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
from docx_to_txt import convert_to_txt

def multfile():
    Tk().withdraw()
    files = askopenfilenames(filetypes=(("txt", "*.txt"),("docx", "*.docx")))
    files = list(files)
    finalf = []
    temp = []
    if files[0].endswith(".docx"):
        temp = convert_to_txt(files)
        for i in range(len(temp)):
            string = temp[i]
            ind = 0
            for j in range(len(string)):
                if string[j]=='/':
                    ind = j
            string = string[ind+1:]
            finalf.append(string)
    else :
        for i in range(len(files)):
            string = files[i]
            ind = 0
            for j in range(len(string)):
                if string[j]=='/':
                    ind = j
            string = string[ind+1:len(string)]
            finalf.append(string)
    return finalf