from tkinter import ttk, PhotoImage, Scrollbar
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk
import tkinter as tk
import threading
import time
import json
import os






class HomeWindow():
    def __init__(self, root):
        self.root = root
        self.NextWindow = None
        self.MangaData = {
            #<MangaName> : {Chapters : []
            #               CoverImage : <ImageData>
            #           
            #}
        }

        self.MangaCoverScale = 800
        self.RowCapacity = (int(1280*0.95)-55)//((self.MangaCoverScale//3)+10)
        self.MangaCoverCanvases = {}

        self.SearchCanvas = tk.Canvas(self.root,
                                    background="#1E1E1E", 
                                    bd=2,
                                    highlightbackground="#121212",
                                    highlightcolor="#121212",
                                    highlightthickness=5)
                                      


        self.SearchBar = tk.Entry(self.SearchCanvas, font=("Arial", 16))



        self.SearchBar.bind('<FocusIn>', self.OnSearchEntryClick)
        self.SearchBar.bind('<FocusOut>', self.OnSearchEntryFocusout)
        self.SearchBar.bind('<KeyPress>', self.on_key_press_on_searchbar)
        self.SearchBar.bind('<KeyRelease>', self.on_key_release_on_searchbar)
        self.ctrl_pressed = False
        self.OnSearchEntryFocusout(None)

        


        self.ScrollbarCanvasHolder = tk.Canvas(self.root,
                                     background="#000000", 
                                     bd=2,
                                     highlightbackground="#1F1F1F",
                                     highlightcolor="#1F1F1F",
                                     highlightthickness=1)
        


        #Main Canvas for the anime Pictures
        self.MangasHolderCanvas = tk.Canvas(self.ScrollbarCanvasHolder,
                                     background="#1B1B1B", 
                                     bd=2,
                                     highlightbackground="#1F1F1F",
                                     highlightcolor="#1F1F1F",
                                     highlightthickness=1,
                                     )
        
        
        

        
        #self.scrollbar_x = ttk.Scrollbar(self.ScrollbarCanvasHolder, orient='horizontal', command=self.MangasHolderCanvas.xview)
        self.scrollbar_y = ttk.Scrollbar(self.ScrollbarCanvasHolder, orient='vertical', command=self.MangasHolderCanvas.yview)
        self.MangasHolderCanvas.configure(yscrollcommand=self.scrollbar_y.set)
        self.MangasHolderCanvas.bind("<MouseWheel>", self.SmoothCanvasScroller)
        
        self.duration = 0.2
        self.start_time = time.time()
        self.end_time = time.time()
        self.scroll_amount = 0


        

                

        #self.scrollbar_x.pack(side='bottom', fill='x')
        self.scrollbar_y.pack(side='right', fill='y')
        self.MangasHolderCanvas.place(relx=0.5, rely=0.5, anchor='center', relwidth=1, relheight=1)
        self.ScrollbarCanvasHolder.place(relx=0.5, rely=0.55, anchor='center',relwidth=0.95, relheight=0.85)
        self.SearchBar.place(anchor="center",relx=0.75,rely=0.5,relheight=0.5,relwidth=0.20)
        self.SearchCanvas.place(anchor="n",relx=0.5,rely=0.01,relheight=0.1,relwidth=0.95)

        self.MangasHolderCanvasSizeTemp = (self.MangasHolderCanvas.winfo_width(),self.MangasHolderCanvas.winfo_height())        
        self.MangasHolderCanvas.bind("<Configure>", self.on_resize)





        root.bind('<Button-1>', self.OnClick)
        threading.Thread(target=self.InitialiserThread).start()


        self.SmoothCanvasScrollerState = True
        threading.Thread(target=self.SmoothCanvasScrollerThread).start()



    def OnDisplayWindow(self):
        self.SmoothCanvasScrollerState = True
        threading.Thread(target=self.SmoothCanvasScrollerThread).start()


    def DisplayWindow(self):
        self.OnDisplayWindow()
        self.ScrollbarCanvasHolder.place(relx=0.5, rely=0.55, anchor='center',relwidth=0.95, relheight=0.85)
        self.SearchCanvas.place(anchor="n",relx=0.5,rely=0.01,relheight=0.1,relwidth=0.95)


    def HideWindow(self):
        self.ScrollbarCanvasHolder.place_forget()
        self.SearchCanvas.place_forget()
        self.SmoothCanvasScrollerState = False

    def on_resize(self, event=None):
        if str(self.MangasHolderCanvasSizeTemp) != str((event.width,event.height)):
            RowCapacity = (event.width-55)//((self.MangaCoverScale//3)+10)
            if RowCapacity <= 0:
                RowCapacity = 1
            elif RowCapacity != self.RowCapacity:
                self.RowCapacity = RowCapacity
                self.PlaceMangaCoverFrames()
            
    def PlaceMangaCoverFrames(self):
        for index, (key, frame) in enumerate(self.MangaCoverCanvases.items()):
            frame["Object"].grid(row=index // self.RowCapacity, column=index % self.RowCapacity, padx=5, pady=5)
        self.MangasHolderCanvas.update_idletasks()
        self.MangasHolderCanvas.config(scrollregion=self.MangasHolderCanvas.bbox("all"))

    def Object_frame(self, Object):
        for widget in Object.winfo_children():
            widget.destroy()


    def InitialiserThread(self):
        self.GrapAvailableLocalMangaAndDisplay()



    def GrapAvailableLocalMangaAndDisplay(self):
        timer = time.time()

        MangaNmes = self.folders_in_directory("MangaOutput")
        self.MangaCanvasFrame = tk.Frame(self.MangasHolderCanvas, background="#1B1B1B")
        self.MangaCanvasFrame.place(anchor="center",relwidth=0.8, relheight=0.8)
        self.MangasHolderCanvas.create_window((0, 0), window=self.MangaCanvasFrame, anchor='nw')
        self.MangaCanvasFrame.bind("<MouseWheel>", self.SmoothCanvasScroller)

        for index, Name in enumerate(MangaNmes):
            self.MangaData[Name] = {}
            self.MangaData[Name]["Cover"] = Image.open(f"MangaOutput/{Name}/Cover.jpg")
            with open(f'MangaOutput/{Name}/Data.json', 'r') as file:
                self.MangaData[Name]["Names"] = json.load(file)

            manga_Canvas = tk.Canvas(self.MangaCanvasFrame,
                                relief=tk.SOLID,
                                highlightbackground="#000000",
                                highlightcolor="#000000",
                                highlightthickness=3)
            
            manga_Canvas.grid_rowconfigure(0, weight=1)
            manga_Canvas.grid_columnconfigure(0, weight=1)

            manga_image = tk.Label(manga_Canvas, background="#1B1B1B", fg="#1B1B1B", highlightthickness=3, highlightbackground="#0B0B0B")
            temp_image = ImageTk.PhotoImage(self.MangaData[Name]["Cover"].resize(((self.MangaCoverScale)//3,(self.MangaCoverScale)//2)))
            manga_image.grid(row=0, column=0, sticky='ew')
            self.MangaData[Name]["ImageTemp"] = temp_image
            manga_image.config(image=temp_image)
            

            manga_name = tk.Text(manga_Canvas, 
                                background="#373737", 
                                fg="#0075A4", 
                                highlightbackground="#0B0B0B",
                                highlightcolor= "#0B0B0B",
                                highlightthickness=3,
                                bd=0,
                                padx=2,
                                pady=2,
                                wrap=tk.WORD,)
            manga_name.insert(tk.END, self.MangaData[Name]["Names"]["s"],"center")
            manga_name.config(state=tk.DISABLED)  # Make the Text widget read-only
            manga_name.tag_configure("center", justify='center')
            manga_name.place(anchor="center",relheight=0.1,relwidth=1,relx=0.5,rely=1.1)






            manga_image.bind("<Enter>", self.on_enter_image_cover)
            manga_image.bind("<Leave>", self.on_leave_image_cover)
            manga_image.bind("<MouseWheel>", self.SmoothCanvasScroller)
            manga_image.bind("<ButtonRelease-1>", self.on_click_manga_cover)
            self.MangaCoverCanvases[manga_image] = {}
            self.MangaCoverCanvases[manga_image]["Names"] = self.MangaData[Name]["Names"]
            self.MangaCoverCanvases[manga_image]["Object"] = manga_Canvas
            self.MangaCoverCanvases[manga_image]["NameLable"] = manga_name
            self.MangaCoverCanvases[manga_image]["FolderName"] = Name
            self.MangaCoverCanvases[manga_image]["ChaptersData"] = None
            self.MangaCoverCanvases[manga_image]["CoverImage"] = self.MangaData[Name]["Cover"]



            #manga_frame.grid(row=0, column=index, padx=5, pady=5, sticky='w')
            manga_Canvas.grid(row=index//self.RowCapacity, column=index%self.RowCapacity, padx=5, pady=5)
            self.MangasHolderCanvas.update_idletasks()
            self.MangasHolderCanvas.config(scrollregion=self.MangasHolderCanvas.bbox("all"))
            manga_Canvas.grid_propagate(False)
        
        print(time.time()- timer)



    def folders_in_directory(self, directory):
        if not os.path.isdir(directory):
            print(f"The path '{directory}' is not a valid directory.")
            return
        
        Output = []
        try:
            # List all entries in the directory
            entries = os.listdir(directory)
            
            # Iterate over the entries and print only directories
            for entry in entries:
                full_path = os.path.join(directory, entry)
                if os.path.isdir(full_path):
                    Output.append(entry)
            return Output
                    
        except PermissionError:
            print(f"Permission denied: Unable to access '{directory}'.")
        except Exception as e:
            print(f"An error occurred: {e}")



    def GrapAvailableLocalManga(self):
        MangaNmes = self.folders_in_directory("MangaOutput")

        for Name in MangaNmes:
            self.MangaData[Name] = {}
            self.MangaData[Name]["Cover"] = Image.open(f"MangaOutput/{Name}/Cover.jpg")
            with open('Data.json', 'r') as file:
                self.MangaData[Name]["Name"] = json.load(file)


    def on_enter_image_cover(self, event):
        """Change label appearance on hover."""
        #temp_image = ImageTk.PhotoImage(self.MangaData[MangaName]["Cover"].resize((int(((self.MangaCoverScale)//3)*1.2),int(((self.MangaCoverScale)//2)*1.2))))
        #event.widget.config(image=temp_image)
        #self.MangaData[MangaName]["ImageTemp"] = temp_image
        if float(self.MangaCoverCanvases[event.widget]["NameLable"].place_info().get("rely")) == 0.95:
            return

        threading.Thread(target=self.SmoothTranstionMangaCoverThread, args=(event,1.1, 1)).start()
        threading.Thread(target=self.SmoothTranstionNameTextMangaCoverThread, args=(event,0.95)).start()

    def on_leave_image_cover(self, event):
        """Revert label appearance when not hovering."""
        #temp_image = ImageTk.PhotoImage(self.MangaData[MangaName]["Cover"].resize((((self.MangaCoverScale)//3),((self.MangaCoverScale)//2))))
        #event.widget.config(image=temp_image)
        #self.MangaData[MangaName]["ImageTemp"] = temp_image

        getTextBox = self.MangaCoverCanvases[event.widget]["NameLable"]
        x, y = getTextBox.winfo_pointerxy()
        widget_at_cursor = getTextBox.winfo_containing(x, y)
        if widget_at_cursor == getTextBox:
            getTextBox.bind("<Leave>", lambda NameEvent: self.on_leave_image_Name_text(NameEvent, event))
            return
        
        if float(self.MangaCoverCanvases[event.widget]["NameLable"].place_info().get("rely")) == 1.1:
            return
        
        threading.Thread(target=self.SmoothTranstionMangaCoverThread, args=(event,1, 1.1)).start()
        threading.Thread(target=self.SmoothTranstionNameTextMangaCoverThread, args=(event,1.1)).start()

    def on_leave_image_Name_text(self, event, ImageEvent):
        ImageCover = ImageEvent.widget
        x, y = ImageCover.winfo_pointerxy()
        widget_at_cursor = ImageCover.winfo_containing(x, y)
        if widget_at_cursor == ImageCover:
            return
        threading.Thread(target=self.SmoothTranstionMangaCoverThread, args=(ImageEvent,1, 1.1)).start()
        threading.Thread(target=self.SmoothTranstionNameTextMangaCoverThread, args=(ImageEvent,1.1)).start()
        

    def SmoothTranstionMangaCoverThread(self, event, FinalScale, StartScale):
        StartScale = StartScale
        ScaleChange = FinalScale - StartScale
        StartingTime = time.time()
        ElapsedTime = 0.1
        while True:
            DeltaTime = min((time.time() - StartingTime)/ElapsedTime, 1)
            ScaleRatio = StartScale + (DeltaTime * ScaleChange)
            temp_image = ImageTk.PhotoImage(self.MangaData[self.MangaCoverCanvases[event.widget]["FolderName"]]["Cover"].resize((int(((self.MangaCoverScale)//3)*ScaleRatio),int(((self.MangaCoverScale)//2)*ScaleRatio))))
            event.widget.config(image=temp_image)
            self.MangaData[self.MangaCoverCanvases[event.widget]["FolderName"]]["ImageTemp"] = temp_image
            if ScaleRatio == FinalScale:
                break
            time.sleep(1/120)
        
    def SmoothTranstionNameTextMangaCoverThread(self, event, EndPostion):
        StartNamePostion = float(self.MangaCoverCanvases[event.widget]["NameLable"].place_info().get("rely"))
        EndNamePostion = EndPostion
        StartingTime = time.time()
        TotalPostionNameChange = EndNamePostion - StartNamePostion
        ElapsedTime = 0.1
        while True:
            DeltaTime = min((time.time() - StartingTime)/ElapsedTime, 1)
            Postion = (TotalPostionNameChange * DeltaTime) + StartNamePostion
            self.MangaCoverCanvases[event.widget]["NameLable"].place(anchor="center",relheight=0.1,relwidth=1,relx=0.5,rely=Postion)
            if DeltaTime >= 1:
                return
            time.sleep(1/120)
            
    def SmoothCanvasScroller(self, event):
        Width = self.MangasHolderCanvas.cget("scrollregion").split(" ")[-1]
        current_view = self.scrollbar_y.get()

        if int(Width) != 0:

            self.scroll_amount += float((event.delta * -1) / int(Width))
            self.duration = 0.2
            self.start_time = time.time()
            self.end_time = time.time() + self.duration



        #new_view_position = current_view[0] - scroll_amount
        #new_view_position = max(0, min(1, new_view_position))
        

    def SmoothCanvasScrollerThread(self):
        while self.SmoothCanvasScrollerState:
            if time.time() >= self.end_time:
                time.sleep(1/120)
                continue
            current_pos = self.scrollbar_y.get()[0]
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            progress = elapsed_time / self.duration
            target_pos = current_pos + ((self.scroll_amount) * progress)
            self.scroll_amount -= ((self.scroll_amount) * progress)
            self.MangasHolderCanvas.yview_moveto(target_pos)
            self.MangasHolderCanvas.update_idletasks()
            time.sleep(1/120)





    def Search(self, Name, Accuracy=0.5):
        Name = Name.lower().split()
        results = []
        for index, (key, frame) in enumerate(self.MangaCoverCanvases.items()):
            frame["Object"].grid_remove()
            Percentage = self.Compare(Name, frame["Names"]["s"].lower().split())
            if Percentage >= Accuracy:
                frame["Names"]["p"] = Percentage
                results.append(frame["Object"])
            else:
                for Alt in frame["Names"]["a"]:
                    Percentage = self.Compare(Name, Alt.lower().split())
                    if Percentage >= Accuracy:
                        frame["Names"]["p"] = Percentage
                        results.append(frame["Object"])

    
        
        for index, Object in enumerate(results):
            Object.grid(row=index // self.RowCapacity, column=index % self.RowCapacity, padx=5, pady=5)

        if results == []:
            self.MangasHolderCanvas.update_idletasks()
            self.MangasHolderCanvas.config(scrollregion=(0,0,0,0))
            return

        self.MangasHolderCanvas.update_idletasks()
        self.MangasHolderCanvas.config(scrollregion=self.MangasHolderCanvas.bbox("all"))


    def Compare(self, Searched, Data):
        Correct = 0
        for word in Searched:
            if word in Data:
                Correct +=1 
        return Correct/len(Searched)      

    def OnSearchEntryClick(self, event):
        Text = self.SearchBar.get()
        if Text == "Search" and self.SearchBar.cget("fg") == "grey":
            self.SearchBar.delete(0, "end")
            self.SearchBar.config(fg='black')

    def OnSearchEntryFocusout(self, event):
        Text = self.SearchBar.get()
        if Text == "":
            self.SearchBar.insert(0, "Search")
            self.SearchBar.config(fg='grey')

    def on_key_press_on_searchbar(self, event):
        if event.keysym == 'Control_L':
            self.ctrl_pressed = True
        elif event.keysym == 'BackSpace' and self.ctrl_pressed:
            text = self.SearchBar.get()
            new_text = self.delete_until_special_character(text)
            self.SearchBar.delete(0, "end")
            self.SearchBar.insert(0, new_text)
            return "break"


    def delete_until_special_character(self, text):
        words = text.split(" ")
        if words:  # Ensure there are words to delete
            words.pop()  # Remove the last word
        new_text = " ".join(words)
        return new_text
        


    def on_key_release_on_searchbar(self, event):
        if event.keysym == 'Control_L':
            self.ctrl_pressed = False
        
        Text = self.SearchBar.get()
        if len(Text) != 0:
            Words = Text.split(" ")
            accuracy = 1 / len(Words)
            if accuracy > 0.75:
                accuracy = 0.75
            if accuracy < 0.5:
                accuracy = 0.5
            self.Search(Text, Accuracy=accuracy)
        
        if Text == "":
            self.PlaceMangaCoverFrames()
            
        
    def OnClick(self, event):
        widget = event.widget
        widget.focus_set()


    def on_click_manga_cover(self, event):
        x, y = event.widget.winfo_pointerxy()
        widget_at_cursor = event.widget.winfo_containing(x, y)
        if widget_at_cursor == event.widget:
            if self.NextWindow != None:
                if self.MangaCoverCanvases[event.widget]["ChaptersData"] == None:
                    self.MangaCoverCanvases[event.widget]["ChaptersData"] = self.folders_in_directory(f"MangaOutput/{self.MangaCoverCanvases[event.widget]["FolderName"]}")
                self.NextWindow.MangaData = self.MangaCoverCanvases[event.widget]
                self.NextWindow.DisplayWindow()
                self.HideWindow()
            self.HideWindow()