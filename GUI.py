from tkinter import ttk, PhotoImage, Scrollbar
from ttkthemes import ThemedStyle
from Windows.FirstWindow import HomeWindow
from Windows.SecondWindow import MangaHolder
from Windows.ThridWindow import MangaReader
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk
import tkinter as tk
import threading
import time
import json
import os





class MyTkinterApp:
    def __init__(self):
        #set up the window
        self.root = tk.Tk()
        self.root = self.root 
        self.root.title("GUI")
        self.root.geometry("1280x720")
        self.root.config(bg="#000000")
        
        
        #set theme
        self.style = ThemedStyle()
        self.style.set_theme("black")

        
        #create an instance of a windows
        self.FirstWindow = HomeWindow(self.root)
        self.SecondWindow = MangaHolder(self.root)
        self.ThridWindow = MangaReader(self.root)

        #Link the windows togather so they gain access to each other And Kick start the first window State
        self.FirstWindow.ActiveWindow = True
        self.FirstWindow.NextWindow = self.SecondWindow
        self.SecondWindow.PreviousWindow = self.FirstWindow
        self.SecondWindow.NextWindow = self.ThridWindow
        self.ThridWindow.PreviousWindow = self.SecondWindow

        #Create an instance of empty MangaDataHolder for local manga and give the access to the windows
        self.MangaData = [] #it is an array that will hold hashmaps





        #Bind the keys to commands
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)
        self.root.bind('<Control-minus>', self.on_ctrl_minus)
        self.root.bind('<Control-equal>', self.on_ctrl_plus)
        self.root.bind('<Left>', self.on_left_arrow)
        self.root.bind('<Right>', self.on_right_arrow)



    def on_right_arrow(self, event):
        if self.FirstWindow.ActiveWindow:
            self.FirstWindow.NextMangasPage()
        if self.ThridWindow.SmoothCanvasScrollerState:    #note! that i am checking for scroll wheel instead of checking 
            self.ThridWindow.LoadNextPageToMiddleFrame()  #if the main canvase if if it is visiable this is  because  i want
                                                          # to cut correnrs and it should be done the other way

    def on_left_arrow(self, event):
        if self.FirstWindow.ActiveWindow:
            self.FirstWindow.PreviousMangasPage()
        
        if self.ThridWindow.SmoothCanvasScrollerState:    #note! same comment as the one above it
            self.ThridWindow.LoadPreviousPageToMiddleFrame()
        

    def on_ctrl_minus(self, event):
        self.ThridWindow.PageWidthSizeScaler -= 0.05
        if self.ThridWindow.DispalyedPageIndex != None:
            self.ThridWindow.LoadPageToMiddleFrame(self.ThridWindow.DispalyedPageIndex)


    def on_ctrl_plus(self, event):
        self.ThridWindow.PageWidthSizeScaler += 0.05
        if self.ThridWindow.DispalyedPageIndex != None:
            self.ThridWindow.LoadPageToMiddleFrame(self.ThridWindow.DispalyedPageIndex)


    def toggle_fullscreen(self, event=None):
        # Detect current fullscreen state
        self.is_fullscreen = not self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", self.is_fullscreen)
        return "break"

    def exit_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.root.attributes("-fullscreen", False)
        return "break"

    def on_quit(self):
        self.root.destroy()
        os._exit(0)



x = MyTkinterApp()
x.root.mainloop()