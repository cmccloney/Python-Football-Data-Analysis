from tkinter import *
import os

def PickScriptTkinter():
    os.system("nfl-tkinter.py")

def PickScriptDash():
    os.system("nfl-dash.py")

root=Tk()
Label(root, text='Tkinter - Web-Scraped Information and Simple Graph').pack()
Button(root, text='Tkinter', command=lambda:PickScriptTkinter()).pack()
Label(root, text='Dash - WIP').pack()
Button(root, text='Dash', command=lambda:PickScriptDash()).pack()
