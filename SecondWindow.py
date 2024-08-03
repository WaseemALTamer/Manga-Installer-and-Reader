from tkinter import ttk, PhotoImage, Scrollbar
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk
import tkinter as tk
import threading
import time
import json
import os




class MangaHolder():
    def __init__(self, root):
        self.root = root
        self.MangaData = None
        self.NextWindow = None
        self.PreviousWindow = None
        self.TempData = None
        self.BookMarkData = None
        self.MangaCoverScale = 800

        self.ChaptersHashMapListboxElements = {
            #"Chapter 1" : 100010   #this maps Chapters to there chaptersID
        }

        #Main Canvas
        self.MainCanvas = tk.Canvas(self.root,
                                    bg="#000000",
                                    highlightbackground="#1F1F1F",
                                    highlightcolor="#1F1F1F",
                                    highlightthickness=5)
        #Image Cover
        self.ImageFrame = tk.Frame(self.MainCanvas,
                                    bg="#000000",
                                    highlightbackground="#1F1F1F",
                                    highlightcolor="#1F1F1F",
                                    highlightthickness=5)
        self.ImageCanvas = tk.Canvas(self.ImageFrame,
                                    bg="#000000",
                                    highlightbackground="#1F1F1F",
                                    highlightcolor="#1F1F1F",
                                    highlightthickness=5)
        self.ImageCanvas.place(relx=0.01, rely=0.02, anchor="nw")
        self.ImageFrame.place(relx=0,rely=0,relheight=1,relwidth=0.3, anchor="nw")

        #Chapters Holder
        self.ChaptersHolderAndScrollbarFrame = tk.Frame(self.MainCanvas,
                                    bg="#000000",
                                    highlightbackground="#1F1F1F",
                                    highlightcolor="#1F1F1F",
                                    highlightthickness=5)
        self.ChaptersSectionFrame = tk.Frame(self.ChaptersHolderAndScrollbarFrame,
                                    bg="#000000",
                                    highlightbackground="#1F1F1F",
                                    highlightcolor="#1F1F1F",
                                    highlightthickness=0,
                                    bd=0)
        self.ChaptersHolderCanvas = tk.Canvas(self.ChaptersSectionFrame,
                                    bg="#000000",
                                    highlightbackground="#000000",
                                    highlightcolor="#000000",
                                    highlightthickness=0,
                                    bd=5)
        self.ChaptersHolderListbox = tk.Listbox(self.ChaptersHolderCanvas,
                                    bg="#000000",
                                    highlightbackground="#1F1F1F",
                                    highlightcolor="#1E1E1E",
                                    highlightthickness=5,
                                    bd=0,
                                    fg="#0075A4",
                                    font=16)

        self.ChaptersHolderAndScrollbarFrame.place(relx=0.3,rely=0,relheight=1,relwidth=0.7)
        self.ChaptersSectionFrame.place(relx=0.5, rely=1, relheight=0.7, relwidth=1, anchor="s")
        self.ChaptersHolderCanvas.place(relx=0.5, rely=0.5, relheight=1, relwidth=1, anchor="center")
        self.ChaptersHolderListbox.pack(fill="both", expand=True, side=tk.LEFT)



        #ChapterListbox
        self.ChaptersHolderListbox.bind('<Configure>', self.re_size_ChaptersHolderListbox)
        self.ChaptersHolderListbox.bind('<<ListboxSelect>>', self.on_select_chapter_listbox_element)
        self.ChaptersHolderListbox.bind('<Motion>', self.on_hover_ChaptersHolderListboxContent)
        self.ChaptersHolderListbox.bind('<Leave>', self.on_leave_ChapterHolderListbox)
        self.ChapterHolderListboxWidgetInformation = {"Size":(0,0),
                                                    "NumberOfChapter": 0,
                                                    "ElementColors" : ["#000000", "#1F1F1F"],
                                                    "HoveredIndex": None}


        #Scrollbar
        self.scrollbar_y = ttk.Scrollbar(self.ChaptersSectionFrame, orient='vertical', command=self.ChaptersHolderListbox.yview)
        self.ChaptersHolderListbox.configure(yscrollcommand=self.scrollbar_y.set)
        self.ChaptersHolderListbox.config(yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_y.pack(side='right', fill='y')



        self.MainCanvasSizeTemp = (self.MainCanvas.winfo_width(),self.MainCanvas.winfo_height())
        self.MainCanvas.bind("<Configure>", self.on_resize)
        self.BackButton = tk.Button(self.ChaptersHolderAndScrollbarFrame,text="<", background="#2F2F2F", highlightcolor="#2F2F2F",activebackground="#1E1E1E",bd=0,command=self.onclick_back_button)
        self.BackButton.place(relheight=0.02, relwidth=0.02, relx=0.98, rely=0.02, anchor="center")



    def OnDisplayWindow(self):
        #DisplayImage
        CoverImage = ImageTk.PhotoImage(self.MangaData["CoverImage"].resize(((self.MangaCoverScale)//3,(self.MangaCoverScale)//2)))
        self.MangaData["TempImage"] = CoverImage
        ImageLable = tk.Label(self.ImageCanvas, image=CoverImage,background="#1F1F1F", fg="#1F1F1F", highlightthickness=5, highlightbackground="#1F1F1F")
        ImageLable.grid(row=0,column=0)
        #DisplayChaptersHolder

    def AddMangaChapters(self):
            
        BookMarkPath = f"MangaOutput/{self.MangaData["FolderName"]}/BookMark.json"
        self.BookMarkData = None
        if os.path.exists(BookMarkPath):
            # Open and load the existing JSON file
            with open(BookMarkPath, 'r') as file:
                self.BookMarkData = json.load(file)


        if self.MangaData != self.TempData:
            self.ChapterHolderListboxWidgetInformation = {"Size":(0,0),
                                                        "NumberOfChapter": 0,
                                                        "ElementColors" : ["#000000", "#1F1F1F"],
                                                        "HoveredIndex": None}
            
            self.ChaptersHolderListbox.delete(0, tk.END) 
            Chapters = sorted([int(element) for element in self.MangaData["ChaptersData"]])
            for index, Chapter in enumerate(Chapters):            
                if self.BookMarkData != None and Chapter in self.BookMarkData["ReadChapters"]:
                    if self.BookMarkData["Chapter"] == Chapter:
                        Text = f"{self.ChapterID_ToSeasonalChapter(Chapter)} (BookMarked)"
                        self.ChaptersHolderListbox.insert(index, Text)
                        self.ChaptersHolderListbox.itemconfig(index, foreground="#BAA200", background=self.ChapterHolderListboxWidgetInformation["ElementColors"][index%2])
                        self.LoadBookMarkButton = tk.Button(self.MainCanvas,text="Load BookMark", background="#1F1F1F", highlightcolor="#1F1F1F",fg="#626262",activebackground="#1E1E1E",bd=0, font= 16, command=self.onclick_LoadBookMark_button)
                        self.LoadBookMarkButton.place(relx=0.31,rely=0.03)
                    else:
                        Text = f"{self.ChapterID_ToSeasonalChapter(Chapter)} (Read)"
                        self.ChaptersHolderListbox.insert(index, Text)
                        self.ChaptersHolderListbox.itemconfig(index, foreground="#22B14C", background=self.ChapterHolderListboxWidgetInformation["ElementColors"][index%2])
                else:
                    Text = f"{self.ChapterID_ToSeasonalChapter(Chapter)}"
                    self.ChaptersHolderListbox.insert(index, Text)
                    self.ChaptersHolderListbox.itemconfig(index, background=self.ChapterHolderListboxWidgetInformation["ElementColors"][index%2])
                self.ChaptersHashMapListboxElements[Text] = Chapter
                self.ChapterHolderListboxWidgetInformation["NumberOfChapter"] += 1
                self.MangaData["ChaptersData"][index] = Chapters[index]
            self.TempData = self.MangaData


    def ChapterID_ToSeasonalChapter(self, Chapter):
        Index = int(str(Chapter)[0])
        ChapterIDWithoutIndex =  int(str(Chapter)[1:])
        ChapterNumber = self.format_float(ChapterIDWithoutIndex * 0.1) 

        if Index > 1:
            return f"S{Index}  {ChapterNumber}"
        else:
            return f"{ChapterNumber}"



    def onclick_back_button(self):
        self.HideWindow()
        self.PreviousWindow.DisplayWindow()


    def on_select_chapter_listbox_element(self, event):
        # Get the index of the selected item
        selected_index = event.widget.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_item = event.widget.get(selected_index)
            Chapter = self.ChaptersHashMapListboxElements[selected_item] 
            self.MangaData["CurrentChapter"] = Chapter
            self.NextWindow.MangaData = self.MangaData
            self.HideWindow()
            self.NextWindow.DisplayWindow()


    def onclick_LoadBookMark_button(self):
        Chapter = self.BookMarkData["Chapter"]
        Page = self.BookMarkData["Page"]
        self.MangaData["CurrentChapter"] = int(Chapter)
        self.NextWindow.StartingChapterPageIndex = Page
        self.NextWindow.MangaData = self.MangaData
        self.HideWindow()
        self.NextWindow.DisplayWindow()


    def on_hover_ChaptersHolderListboxContent(self, event):
        NumberOfElementsBehind = event.widget.index('@0,0')
        ElementSize = event.widget.bbox(NumberOfElementsBehind)
        if ElementSize == None:
            return
        ContentBoxHeightSize = self.ChapterHolderListboxWidgetInformation["Size"][1] - 10
        NumberOfEelements = self.ChapterHolderListboxWidgetInformation["NumberOfChapter"]
        HoveredOverElementIndex = ((event.y - ElementSize[0])//(ElementSize[3]+1)) + NumberOfElementsBehind # the 19 is font size + 3
        if HoveredOverElementIndex <= NumberOfEelements - 1 and HoveredOverElementIndex >= 0 and HoveredOverElementIndex <= NumberOfEelements - 1:
            for i in range(NumberOfEelements):
                self.ChaptersHolderListbox.itemconfig(i, background=self.ChapterHolderListboxWidgetInformation["ElementColors"][i%2])
            self.ChaptersHolderListbox.itemconfig(HoveredOverElementIndex,background="#323232")
            self.ChapterHolderListboxWidgetInformation["HoveredIndex"] = HoveredOverElementIndex
    
    def on_leave_ChapterHolderListbox(self, event):
        for i in range(self.ChapterHolderListboxWidgetInformation["NumberOfChapter"]):
            self.ChaptersHolderListbox.itemconfig(i, background=self.ChapterHolderListboxWidgetInformation["ElementColors"][i%2])


    def re_size_ChaptersHolderListbox(self, event):
        self.ChapterHolderListboxWidgetInformation["Size"] = (event.width,event.height)


    def on_resize(self, event=None):
        if str(self.MainCanvasSizeTemp) != str((event.width,event.height)):
            self.MainCanvasSizeTemp = (event.width,event.height)










    def DisplayWindow(self):
        self.OnDisplayWindow()
        self.MainCanvas.place(relheight=1, relwidth=1, relx=0.5, rely=0.5, anchor="center")
        self.root.after(100, self.StartLoadeingChapterOnThread)
        
    def StartLoadeingChapterOnThread(self):
        threading.Thread(target=self.AddMangaChapters).start()
    
    def HideWindow(self):
        self.MainCanvas.place_forget()









    def format_float(self, value):
        if isinstance(value, float):
            if value.is_integer():
                return int(value)
            else:
                return value
        return value