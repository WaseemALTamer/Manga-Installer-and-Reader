from tkinter import ttk, PhotoImage, Scrollbar
from ttkthemes import ThemedStyle
from FirstWindow import HomeWindow
from SecondWindow import MangaHolder
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk
import tkinter as tk
import threading
import time
import json
import os





class MyTkinterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root = self.root 
        self.root.title("GUI")
        self.style = ThemedStyle()
        self.root.geometry("1280x720")
        self.root.config(bg="#000000")
        self.window_width = self.root.winfo_reqwidth()
        self.window_height = self.root.winfo_reqheight()
        self.style.set_theme("black")
        self.FirstWindow = HomeWindow(self.root)
        self.SecondWindow = MangaHolder(self.root)
        self.ThridWindow = MangaReader(self.root)
        self.FirstWindow.NextWindow = self.SecondWindow
        self.SecondWindow.PreviousWindow = self.FirstWindow
        self.SecondWindow.NextWindow = self.ThridWindow
        self.ThridWindow.PreviousWindow = self.SecondWindow




        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.root.protocol("WM_DELETE_WINDOW", self.on_quit)
        self.root.bind('<Control-minus>', self.on_ctrl_minus)
        self.root.bind('<Control-equal>', self.on_ctrl_plus)


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






class MangaReader():
    def __init__(self, root):
        self.root = root
        self.PreviousWindow = None
        self.MangaData = None
        self.CurrentChapterPages = []
        self.DispalyedPageIndex = None
        self.StartingChapterPageIndex = 0


        self.PageDimentions = (1200, 1800)
        self.PageWidthSizeScaler = 1

        
        self.MainCanvas = tk.Canvas(self.root,
                                    bg="#000000",
                                    highlightbackground="#1F1F1F",
                                    highlightcolor="#1F1F1F",
                                    highlightthickness=5)


        self.RightCanvas = tk.Canvas(self.MainCanvas,
                                    bg="#000000",
                                    highlightbackground="#1F1F1F",
                                    highlightcolor="#1F1F1F",
                                    highlightthickness=5)
        

        self.LeftCanvas = tk.Canvas(self.MainCanvas,
                                    bg="#000000",
                                    highlightbackground="#1F1F1F",
                                    highlightcolor="#1F1F1F",
                                    highlightthickness=5)




        #=========================================
        self.MiddleCanvas = tk.Canvas(self.MainCanvas,
                            bg="#000000",
                            highlightbackground="#1F1F1F",
                            highlightcolor="#1F1F1F",
                            highlightthickness=0)

        self.MiddleFrame = tk.Frame(self.MiddleCanvas,
                            bg="#000000",
                            highlightbackground="#1F1F1F",
                            highlightcolor="#1F1F1F",
                            highlightthickness=0)
        self.MiddleFrame.grid_columnconfigure(0,weight=1)
        self.MiddleFrame.grid_rowconfigure(0,weight=1)



        self.scrollbar_y = ttk.Scrollbar(self.RightCanvas, orient='vertical', command=self.MiddleCanvas.yview)
        self.MiddleCanvas.configure(yscrollcommand=self.scrollbar_y.set)
        self.MiddleCanvas.create_window((0, 0), window=self.MiddleFrame, anchor="n")
        self.scrollbar_y.pack(fill="y", side="right")
        self.duration = 0.2
        self.start_time = time.time()
        self.end_time = time.time()
        self.scroll_amount = 0
        self.SmoothCanvasScrollerState = False


        self.BlankSpace = tk.Label(self.MiddleFrame, bd=0, background="#000000",highlightcolor="#000000")
        self.BlankSpace.bind("<MouseWheel>", self.SmoothCanvasScroller) 
        self.BlankSpace.grid(row=1, column=0, pady=150)

        self.RightCanvas.bind("<MouseWheel>", self.SmoothCanvasScroller)
        self.RightCanvas.bind("<ButtonRelease-1>", self.LoadNextPageToMiddleFrame)
        self.LeftCanvas.bind("<MouseWheel>", self.SmoothCanvasScroller)
        self.LeftCanvas.bind("<ButtonRelease-1>", self.LoadPreviousPageToMiddleFrame)
        self.MiddleFrame.bind("<MouseWheel>", self.SmoothCanvasScroller)


        #PopUpButtons
        self.ChapterButtonPOPUP = tk.Button(self.LeftCanvas,text="Chapter: 0", background="#1F1F1F", highlightcolor="#1F1F1F",fg="#626262",activebackground="#1E1E1E",bd=0, font= 16)
        self.ChapterButtonPOPUP.place(rely= 0.02, relx=0.1)

        self.PageButtonPOPUP = tk.Button(self.LeftCanvas,text="Page: 0", background="#1F1F1F", highlightcolor="#1F1F1F",fg="#626262",activebackground="#1E1E1E",bd=0, font= 16)
        self.PageButtonPOPUP.place(rely= 0.07, relx=0.1)

        #BookMarkButton
        self.BookMark = tk.Button(self.LeftCanvas,text="BookMark", background="#1F1F1F", highlightcolor="#1F1F1F",fg="#626262",activebackground="#1E1E1E",bd=0, font= 16,command=self.on_press_book_mark)
        self.BookMark.place(rely= 0.92, relx=0.1)




        self.FullScreenWindowButton = tk.Button(self.MainCanvas,text="⛶", background="#2F2F2F", highlightcolor="#2F2F2F",activebackground="#1E1E1E",bd=0,command=self.onclick_fullscreen_button, font= 16)
        self.FullScreenWindowButton.place(height=20, width=20, relx=0.98, rely=0.03, anchor="center")
        self.BackButton = tk.Button(self.MainCanvas,text="<", background="#2F2F2F", highlightcolor="#2F2F2F",activebackground="#1E1E1E",bd=0,command=self.onclick_back_button)
        self.BackButton.place(height=20, width=20, relx=0.96, rely=0.03, anchor="center")
        self.MainCanvasSizeTemp = (self.MainCanvas.winfo_width(),self.MainCanvas.winfo_height())
        self.MainCanvas.bind("<Configure>", self.on_resize)




        



    def OnDisplayWindow(self):
        self.SmoothCanvasScrollerState = True
        threading.Thread(target=self.SmoothCanvasScrollerThread).start()


    def CallAnUpdate(self):
        self.RightCanvasAndLeftCanvasWidth = max(0, min(1, ((self.MainCanvasSizeTemp[0] - (self.PageDimentions[0] * self.PageWidthSizeScaler))/self.MainCanvasSizeTemp[0])/2))
        self.RightCanvas.place(anchor="e", relx=1, rely=0.5, relheight=1, relwidth=self.RightCanvasAndLeftCanvasWidth)
        self.LeftCanvas.place(anchor="w", relx=0, rely=0.5, relheight=1, relwidth=self.RightCanvasAndLeftCanvasWidth)
        self.MiddleCanvas.place(anchor="n",relx=0.5,relheight=1,width=(self.PageDimentions[0]*self.PageWidthSizeScaler))

    def LoadPageToMiddleFrame(self, PageIndex):
        self.PageDimentions = self.CurrentChapterPages[PageIndex]["ImageSize"]

        if self.DispalyedPageIndex != None:
            self.CurrentChapterPages[self.DispalyedPageIndex]["TempImage"] = None
            self.CurrentChapterPages[self.DispalyedPageIndex]["ImageLableHolder"].destroy()


        self.CurrentChapterPages[PageIndex]["ImageLableHolder"] = tk.Label(self.MiddleFrame, highlightbackground="#1F1F1F", highlightthickness=0, bd=0)
        self.CurrentChapterPages[PageIndex]["ImageLableHolder"].bind("<MouseWheel>", self.SmoothCanvasScroller) 
        self.CurrentChapterPages[PageIndex]["ImageLableHolder"].bind("<ButtonRelease-1>", self.onclick_onpage_label)
        
        if self.PageDimentions[0] * self.PageWidthSizeScaler > self.MainCanvasSizeTemp[0]:
            CustemScale = self.MainCanvasSizeTemp[0] / self.PageDimentions[0]
            self.CurrentChapterPages[PageIndex]["TempImage"] = ImageTk.PhotoImage(self.CurrentChapterPages[PageIndex]["ImagePage"].resize(((int(self.PageDimentions[0]*self.PageWidthSizeScaler * CustemScale)),(int(self.PageDimentions[1] * self.PageWidthSizeScaler * CustemScale)))))
            self.PageDimentions = ((int(self.PageDimentions[0] * CustemScale)),(int(self.PageDimentions[1] * CustemScale)))
        else:
            self.CurrentChapterPages[PageIndex]["TempImage"] = ImageTk.PhotoImage(self.CurrentChapterPages[PageIndex]["ImagePage"].resize(((int(self.PageDimentions[0]*self.PageWidthSizeScaler)),(int(self.PageDimentions[1] * self.PageWidthSizeScaler)))))
        
        self.CurrentChapterPages[PageIndex]["ImageLableHolder"].config(image=self.CurrentChapterPages[PageIndex]["TempImage"])
        self.CurrentChapterPages[PageIndex]["ImageLableHolder"].grid(row=0, column=0, sticky='w')





        self.CallAnUpdate()
        self.DispalyedPageIndex = PageIndex
        self.ChapterButtonPOPUP.config(text=f"Chapter: {self.ChapterID_ToSeasonalChapter(self.MangaData["CurrentChapter"])}")
        self.PageButtonPOPUP.config(text=f"Page: {self.DispalyedPageIndex + 1}")
        self.MiddleCanvas.yview_moveto(0)
        self.MiddleCanvas.update_idletasks()
        self.MiddleCanvas.config(scrollregion=self.MiddleCanvas.bbox("all"))



    def LoadChapterContent(self, directory):
        entries = sorted([int(element[:-4]) for element in os.listdir(directory) if element.endswith('.png')])
        for i, entry in enumerate(entries):
            page_path = f"{directory}/{entry}.png"
            image_page = Image.open(page_path)
            image_size = (image_page.width, image_page.height)

            self.CurrentChapterPages.append({
                "ImagePage": image_page,
                "ImageSize": image_size,
                "TempImage" : None,
                "ImageLableHolder" : None
            })

            if i == self.StartingChapterPageIndex:
                self.LoadPageToMiddleFrame(self.StartingChapterPageIndex)
                self.StartingChapterPageIndex = 0

        if self.StartingChapterPageIndex == -1:
            self.LoadPageToMiddleFrame(len(entries) - 1)



        BookMarkData = {
            "Chapter" : None,
            "Page" : None,
            "ReadChapters": []
        }

        try:
            BookMarkPath = f"MangaOutput/{self.MangaData["FolderName"]}/BookMark.json"
            if not os.path.exists(BookMarkPath):
                with open(BookMarkPath, 'w') as file:
                    json.dump(BookMarkData, file, indent=4)
            with open(BookMarkPath, 'r') as file:
                data = json.load(file)
                BookMarkData["Page"] = data["Page"]
                BookMarkData["Chapter"] = data["Chapter"]
                BookMarkData["ReadChapters"] = data["ReadChapters"]
                if self.MangaData["CurrentChapter"] not in BookMarkData["ReadChapters"]:
                    BookMarkData["ReadChapters"].append(self.MangaData["CurrentChapter"])
        except Exception as e:
            print(e)


        with open(BookMarkPath, 'w') as file:
            json.dump(BookMarkData, file, indent=4)


        

    def LoadNextPageToMiddleFrame(self, event=None):
        TotalNumberOfPages = len(self.CurrentChapterPages)
        if self.DispalyedPageIndex < TotalNumberOfPages - 1:
            self.LoadPageToMiddleFrame(self.DispalyedPageIndex + 1)
        else:
            index = self.MangaData["ChaptersData"].index(self.MangaData["CurrentChapter"])
            NumberOfChapters = len(self.MangaData["ChaptersData"])
            if index < NumberOfChapters - 1:
                self.MangaData["CurrentChapter"] = self.MangaData["ChaptersData"][index + 1]
                self.StartingChapterPageIndex = 0
                self.LoadAChapterOnThread()


    def LoadPreviousPageToMiddleFrame(self, event=None):
        if self.DispalyedPageIndex > 0:
            self.LoadPageToMiddleFrame(self.DispalyedPageIndex - 1)
        else:
            index = self.MangaData["ChaptersData"].index(self.MangaData["CurrentChapter"])
            if index > 0:
                self.MangaData["CurrentChapter"] = self.MangaData["ChaptersData"][index - 1]
                self.StartingChapterPageIndex = -1
                self.LoadAChapterOnThread()



    def LoadAChapterOnThread(self):
        for index, Page in enumerate(self.CurrentChapterPages):
            if Page["ImageLableHolder"] != None:
                Page["ImageLableHolder"].destroy()
            del Page
            pass

        
        self.CurrentChapterPages = []
        self.DispalyedPageIndex = None
            
        directory = f"MangaOutput/{self.MangaData["FolderName"]}/{self.MangaData["CurrentChapter"]}"
        threading.Thread(target=self.LoadChapterContent, args=(directory,)).start()




    def SmoothCanvasScroller(self, event):
        Width = self.MiddleCanvas.cget("scrollregion").split(" ")[-1]
        current_view = self.scrollbar_y.get()

        if int(Width) != 0:
            self.scroll_amount += float((event.delta * -1) / int(Width))
            self.duration = 0.2
            self.start_time = time.time()
            self.end_time = time.time() + self.duration


    def SmoothCanvasScrollerThread(self):
        while self.SmoothCanvasScrollerState:
            if time.time() >= self.end_time:
                time.sleep(1/60)
                continue
            current_pos = self.scrollbar_y.get()[0]
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            progress = elapsed_time / self.duration
            target_pos = current_pos + ((self.scroll_amount) * progress)
            self.scroll_amount -= ((self.scroll_amount) * progress)
            self.MiddleCanvas.yview_moveto(target_pos)
            #self.MiddleCanvas.update_idletasks()
            time.sleep(1/60)





    def on_press_book_mark(self):
        BookMarkPath = f"MangaOutput/{self.MangaData["FolderName"]}/BookMark.json"

        
        

        BookMarkData = {
            "Chapter" : self.MangaData["CurrentChapter"],
            "Page" : self.DispalyedPageIndex,
            "ReadChapters": []
        }

        if os.path.exists(BookMarkPath):
            with open(BookMarkPath, "r") as file:
                data = json.load(file)
                BookMarkData["ReadChapters"] = data.get("ReadChapters", [])


        with open(BookMarkPath, 'w') as file:
            json.dump(BookMarkData, file, indent=4)


    def onclick_onpage_label(self, event):
        LeftSide = event.widget.winfo_width() / 2
        if event.x <= LeftSide:
            self.LoadPreviousPageToMiddleFrame()
        else:
            self.LoadNextPageToMiddleFrame()


    def onclick_fullscreen_button(self):
        # Detect current fullscreen state
        self.is_fullscreen = not self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", self.is_fullscreen)
        return "break"

    def onclick_back_button(self):
        self.HideWindow()
        self.PreviousWindow.TempData = None
        self.PreviousWindow.DisplayWindow()

    def on_resize(self, event=None):
        if str(self.MainCanvasSizeTemp) != str((event.width,event.height)):
            self.MainCanvasSizeTemp = (event.width,event.height)
            if self.DispalyedPageIndex != None:
                self.LoadPageToMiddleFrame(self.DispalyedPageIndex)

    def DisplayWindow(self):
        self.OnDisplayWindow()
        self.MainCanvas.place(relheight=1, relwidth=1, relx=0.5, rely=0.5, anchor="center")
        self.root.after(100, self.LoadAChapterOnThread)

    def HideWindow(self):
        self.MainCanvas.place_forget()
        self.SmoothCanvasScrollerState = False



    def ChapterID_ToSeasonalChapter(self, Chapter):
        Index = int(str(Chapter)[0])
        ChapterIDWithoutIndex =  int(str(Chapter)[1:])
        ChapterNumber = self.format_float(ChapterIDWithoutIndex * 0.1) 

        if Index > 1:
            return f"S{Index}  {ChapterNumber}"
        else:
            return f"{ChapterNumber}"




    def format_float(self, value):
        if isinstance(value, float):
            if value.is_integer():
                return int(value)
            else:
                return value
        return value


x = MyTkinterApp()
x.root.mainloop()