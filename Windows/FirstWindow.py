from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
import threading
import time
import json
import os







class HomeWindow():
    def __init__(self, root):
        self.root = root
        self.ActiveWindow = False
        self.NextWindow = None
        self.MangasData = [
            # {Name : f"{NameOfManga}"
            #   Chapters : []
            #   CoverImage : <ImageData>
            #   ReshapedCoverImage: <ImageData>        
            #}
        ]

        self.MangaCoverScale = 800
        self.RowCapacity = (int(1280*0.95)-55)//((self.MangaCoverScale//3)+10)
        self.MangasWidgets = [
            #{
            #   Canvas: <Canvas>,
            #   ImageLabel: <Image>
            #   TextBar: <TextBar>,
            #}
        ]

        self.MangasPages = []# this has the same data is the MangaWidgets

        self.MangasCurrentPage = [
            #[],
            #Index
            ]


        self.SearchCanvas = tk.Canvas(self.root,
                                    background="#1E1E1E", 
                                    bd=2,
                                    highlightbackground="#121212",
                                    highlightcolor="#121212",
                                    highlightthickness=5)
                                      


        self.SearchBar = tk.Entry(self.SearchCanvas, font=("Arial", 16))
        self.SearchTempResults = []


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



        #Create Frame that will hold all the Canvases which contain all the pictures
        self.MangaCanvasFrame = tk.Frame(self.MangasHolderCanvas, background="#1B1B1B")
        self.MangaCanvasFrame.place(anchor="center",relwidth=0.8, relheight=0.8)
        self.MangasHolderCanvas.create_window((0, 0), window=self.MangaCanvasFrame, anchor='nw')
        self.MangaCanvasFrame.bind("<MouseWheel>", self.SmoothCanvasScroller)
        
        
        

        
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
        threading.Thread(target=lambda: self.InitialiserThread(GrapLocalManga=True)).start()
        #self.GrapAvailableLocalManga()

        self.SmoothCanvasScrollerState = True
        threading.Thread(target=self.SmoothCanvasScrollerThread).start()



    def OnDisplayWindow(self):
        self.ActiveWindow = True
        self.SmoothCanvasScrollerState = True
        threading.Thread(target=self.SmoothCanvasScrollerThread).start()
        threading.Thread(target=self.InitialiserThread).start()


    def DisplayWindow(self):
        self.OnDisplayWindow()
        self.ScrollbarCanvasHolder.place(relx=0.5, rely=0.55, anchor='center',relwidth=0.95, relheight=0.85)
        self.SearchCanvas.place(anchor="n",relx=0.5,rely=0.01,relheight=0.1,relwidth=0.95)


    def HideWindow(self):
        self.ActiveWindow = False
        self.DestoryMangasWidgets()

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
        for index, MangaWidgets in enumerate(self.MangasWidgets):
            MangaWidgets["Canvas"].grid(row=index // self.RowCapacity, column=index % self.RowCapacity, padx=5, pady=5)
        self.MangasHolderCanvas.update_idletasks()
        self.MangasHolderCanvas.config(scrollregion=self.MangasHolderCanvas.bbox("all"))
        


    def NextMangasPage(self):
        NumberOfPages = len(self.MangasPages)
        CurrentPageIndex = self.MangasCurrentPage[1]
        NextPageIndex = (CurrentPageIndex + 1) % NumberOfPages
        self.MangasCurrentPage[0] = self.MangasPages[NextPageIndex]
        self.MangasCurrentPage[1] = NextPageIndex
        self.CreateAndDisplayMangaWidgets(self.MangasCurrentPage[0])


    def PreviousMangasPage(self):
        NumberOfPages = len(self.MangasPages)
        CurrentPageIndex = self.MangasCurrentPage[1]
        NextPageIndex = (CurrentPageIndex + (NumberOfPages - 1)) % NumberOfPages # this is over flowing the counter just like subtraction in logic gates
        self.MangasCurrentPage[0] = self.MangasPages[NextPageIndex]
        self.MangasCurrentPage[1] = NextPageIndex
        self.CreateAndDisplayMangaWidgets(self.MangasCurrentPage[0])







    def InitialiserThread(self, GrapLocalManga=False):
        if GrapLocalManga:
            self.GrapAvailableLocalManga()
        self.CreateAndDisplayMangaWidgets(self.MangasCurrentPage[0])


    def DestoryMangasWidgets(self):
        if self.MangasWidgets != []:
            for MangaWidget in self.MangasWidgets:
                MangaWidget["Canvas"].destroy()
                MangaWidget["ImageLabel"].destroy()
                MangaWidget["TextBar"].destroy()
            self.MangasWidgets = []

    def CreateAndDisplayMangaWidgets(self, MangaDataList):

        timer = time.time()
        self.DestoryMangasWidgets()
        for Index, Data in enumerate(MangaDataList):

            #Create the Canvas that will hold the Label Image
            manga_Canvas = tk.Canvas(self.MangaCanvasFrame,
                                relief=tk.SOLID,
                                highlightbackground="#000000",
                                highlightcolor="#000000",
                                highlightthickness=3)
            manga_Canvas.grid_rowconfigure(0, weight=1)
            manga_Canvas.grid_columnconfigure(0, weight=1)
            #==============================================



            #Create the label to hold the image
            manga_image = tk.Label(manga_Canvas, 
                                   background="#1B1B1B", 
                                   fg="#1B1B1B", highlightthickness=3, 
                                   highlightbackground="#0B0B0B")
            manga_image.grid(row=0, column=0, sticky='ew')
            if Data["ReshapedCoverImageSize"] != ((self.MangaCoverScale)//3,(self.MangaCoverScale)//2):
                Data["ReshapedCoverImageSize"] = ((self.MangaCoverScale)//3,(self.MangaCoverScale)//2)
                Data["ReshapedCoverImage"] = ImageTk.PhotoImage(Data["CoverImage"].resize(((self.MangaCoverScale)//3,(self.MangaCoverScale)//2)))
                
            manga_image.config(image=Data["ReshapedCoverImage"]) # attach the image to the label it the image is saved else where so we dont have to 
                                                                 # worry about grabage collection
            #===============================================

            
            #create the Text bar for the name of the image
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
            manga_name.insert(tk.END, Data["Names"]["s"],"center") # attach the name of the manga to the Text Bar
            manga_name.config(state=tk.DISABLED)  # Make the Text widget read-only
            manga_name.tag_configure("center", justify='center')
            manga_name.place(anchor="center",relheight=0.1,relwidth=1,relx=0.5,rely=1.1)
            #==================================================


            # We use a hash map for to increase Proformance Proformance
            index = len(self.MangasWidgets) # we keep track of the index of the weiget this is because we dont want to pass it like
            self.MangasWidgets.append({     # self.MangasWidgets[-1] as this will tell the function to always take the last element
                "Canvas": manga_Canvas,   # in the array which is not true after running the loop more than once
                "ImageLabel": manga_image,
                "TextBar": manga_name,
                "Data": Data
            })
            

            # binds the Labels to the events while attaching the MangaWiget element that we appended as we can Calclate and apply the transtion
            manga_image.bind("<Enter>", lambda event, idx=index: self.on_enter_image_cover(event, self.MangasWidgets[idx]))
            manga_image.bind("<Leave>", lambda event, idx=index: self.on_leave_image_cover(event, self.MangasWidgets[idx]))
            manga_image.bind("<ButtonRelease>", lambda event, idx=index: self.on_click_manga_cover(event, self.MangasWidgets[idx]))
            manga_image.bind("<MouseWheel>", self.SmoothCanvasScroller)






            #Update the scroll bar and the window that holds the CoverCanvases

            #manga_frame.grid(row=0, column=index, padx=5, pady=5, sticky='w')
            manga_Canvas.grid(row=Index//self.RowCapacity, column=Index%self.RowCapacity, padx=5, pady=5)
            self.MangasHolderCanvas.update_idletasks()
            self.MangasHolderCanvas.config(scrollregion=self.MangasHolderCanvas.bbox("all"))
            manga_Canvas.grid_propagate(False)
        
        print(time.time()- timer)


    def GrapAvailableLocalManga(self):
        MangaNmes = self.folders_in_directory("MangaOutput")
        for Index, FolderName in enumerate(MangaNmes):
            CoverImage = Image.open(f"MangaOutput/{FolderName}/Cover.jpg") # lets load it up because we need to use it twice



            Data = {
            "FolderName" : f"{FolderName}",
            "Chapters" : None,
            "CoverImage" : CoverImage,
            "Names" : json.load(open(f'MangaOutput/{FolderName}/Data.json', 'r')),
            "ReshapedCoverImage" : ImageTk.PhotoImage(CoverImage.resize(((self.MangaCoverScale)//3,(self.MangaCoverScale)//2))), #reshape the image of the cover 
                                                                                                                                 #for all covers to be the same size
            "ReshapedCoverImageSize" : ((self.MangaCoverScale)//3,(self.MangaCoverScale)//2)
               }

            self.MangasData.append(Data)


            #this part pagenise the data into 8 manga per page

            if Index % 8 == 0:
                self.MangasPages.append([])

            self.MangasPages[Index//8].append(self.MangasData[-1]) # we use the self.MangasData[-1] methode so we dont recreate the data twice which could lead
                                                                   # to too much memory being used. :)
        self.MangasCurrentPage = [self.MangasPages[0], 0]
        self.SearchTempResults = self.MangasCurrentPage[0]



    def on_enter_image_cover(self, event, WidgetsData):
        """Change label appearance on hover."""
        #temp_image = ImageTk.PhotoImage(self.MangaData[MangaName]["Cover"].resize((int(((self.MangaCoverScale)//3)*1.2),int(((self.MangaCoverScale)//2)*1.2))))
        #event.widget.config(image=temp_image)
        #self.MangaData[MangaName]["ImageTemp"] = temp_image

        if float(WidgetsData["TextBar"].place_info().get("rely")) == 0.95:
            return

        threading.Thread(target=self.SmoothTranstionMangaCoverThread, args=(event,1.1, 1, WidgetsData)).start()
        threading.Thread(target=self.SmoothTranstionNameTextMangaCoverThread, args=(event,0.95, WidgetsData)).start()

    def on_leave_image_cover(self, event, WidgetsData):
        """Revert label appearance when not hovering."""
        #temp_image = ImageTk.PhotoImage(self.MangaData[MangaName]["Cover"].resize((((self.MangaCoverScale)//3),((self.MangaCoverScale)//2))))
        #event.widget.config(image=temp_image)
        #self.MangaData[MangaName]["ImageTemp"] = temp_image

        getTextBox = WidgetsData["TextBar"]
        x, y = getTextBox.winfo_pointerxy()
        widget_at_cursor = getTextBox.winfo_containing(x, y)
        if widget_at_cursor == getTextBox:
            getTextBox.bind("<Leave>", lambda NameEvent: self.on_leave_image_Name_text(NameEvent, event, WidgetsData))
            return
        
        if float(getTextBox.place_info().get("rely")) == 1.1:
            return
        
        threading.Thread(target=self.SmoothTranstionMangaCoverThread, args=(event,1, 1.1, WidgetsData)).start()
        threading.Thread(target=self.SmoothTranstionNameTextMangaCoverThread, args=(event,1.1, WidgetsData)).start()

    def on_leave_image_Name_text(self, event, ImageEvent, WidgetsData):
        ImageCover = ImageEvent.widget
        x, y = ImageCover.winfo_pointerxy()
        widget_at_cursor = ImageCover.winfo_containing(x, y)
        if widget_at_cursor == ImageCover: # this will not allow the image to go down while hovering over the Label as the image is still in the cursor field
            return                         # which makes everything above the image take the focuse but the transtion back to how it was will not happen
        threading.Thread(target=self.SmoothTranstionMangaCoverThread, args=(ImageEvent,1, 1.1, WidgetsData)).start()
        threading.Thread(target=self.SmoothTranstionNameTextMangaCoverThread, args=(ImageEvent,1.1, WidgetsData)).start()
        



    #=====================Animations======================
    def SmoothTranstionMangaCoverThread(self, event, FinalScale, StartScale, WidgetsData):
        StartScale = StartScale
        ScaleChange = FinalScale - StartScale
        StartingTime = time.time()
        ElapsedTime = 0.1
        while True:
            DeltaTime = min((time.time() - StartingTime)/ElapsedTime, 1)
            ScaleRatio = StartScale + (DeltaTime * ScaleChange)
            temp_image = ImageTk.PhotoImage(WidgetsData["Data"]["CoverImage"].resize((int(((self.MangaCoverScale)//3)*ScaleRatio),int(((self.MangaCoverScale)//2)*ScaleRatio))))
            event.widget.config(image=temp_image)
            WidgetsData["Data"]["ReshapedCoverImage"] = temp_image
            WidgetsData["Data"]["ReshapedCoverImageSize"] = (int(((self.MangaCoverScale)//3)*ScaleRatio),int(((self.MangaCoverScale)//2)*ScaleRatio))
            if ScaleRatio == FinalScale:
                return
            time.sleep(1/120)
        
    def SmoothTranstionNameTextMangaCoverThread(self, event, EndPostion, WidgetsData):
        StartNamePostion = float(WidgetsData["TextBar"].place_info().get("rely"))
        EndNamePostion = EndPostion
        StartingTime = time.time()
        TotalPostionNameChange = EndNamePostion - StartNamePostion
        ElapsedTime = 0.1
        while True:
            DeltaTime = min((time.time() - StartingTime)/ElapsedTime, 1)
            Postion = (TotalPostionNameChange * DeltaTime) + StartNamePostion
            WidgetsData["TextBar"].place(anchor="center",relheight=0.1,relwidth=1,relx=0.5,rely=Postion)
            if DeltaTime >= 1:
                return
            time.sleep(1/120)

    #=====================End Of Animations======================



    #Scroll Function this functions are responsible for the smooth scrolling


    # this function will apply the changes when you scroll wheel and will not do anything other than that the thread shuold detect the change 
    # and then apply the scroll on the screen the function is stright down of it
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
                time.sleep(1/60)
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


    #====================================================











        


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


    def on_click_manga_cover(self, event, WidgetsData):
        x, y = event.widget.winfo_pointerxy()
        widget_at_cursor = event.widget.winfo_containing(x, y)
        if widget_at_cursor == event.widget:
            if self.NextWindow != None:
                if WidgetsData["Data"]["Chapters"] == None:
                    WidgetsData["Data"]["Chapters"] = self.folders_in_directory(f"MangaOutput/{WidgetsData["Data"]["FolderName"]}")
                
                WidgetsData["Data"]["ReshapedCoverImage"] = ImageTk.PhotoImage(WidgetsData["Data"]["CoverImage"].resize(((self.MangaCoverScale)//3,(self.MangaCoverScale)//2)))

                self.NextWindow.MangaData = WidgetsData["Data"]
                self.NextWindow.DisplayWindow()
                self.HideWindow()
            self.HideWindow()



    #Search Function This should be rewriten better use the internet to look for better algorithms

    def Search(self, Name, Accuracy=0.5):
        Name = Name.lower().split()
        if len(Name) == 0:
            return
        results = []
        for index, MangaData in enumerate(self.MangasData):
            Percentage = self.Compare(Name, MangaData["Names"]["s"].lower().split())
            if Percentage >= Accuracy:
                MangaData["Names"]["p"] = Percentage
                results.append(MangaData)
            else:
                for Alt in MangaData["Names"]["a"]:
                    Percentage = self.Compare(Name, Alt.lower().split())
                    if Percentage >= Accuracy:
                        MangaData["Names"]["p"] = Percentage
                        results.append(MangaData)

        if self.SearchTempResults != results:
            self.CreateAndDisplayMangaWidgets(results)
            self.SearchTempResults = results
        
            


    def OnSearchEntryClick(self, event):
        Text = self.SearchBar.get()
        if Text == "Search" and self.SearchBar.cget("fg") == "grey":
            self.SearchBar.delete(0, "end")
            self.SearchBar.config(fg='black')

    def OnSearchEntryFocusout(self, event):
        Text = self.SearchBar.get()
        if Text == "":

            if self.MangasCurrentPage != [] and self.SearchTempResults != self.MangasCurrentPage[0]:
                self.CreateAndDisplayMangaWidgets(self.MangasCurrentPage[0])
                self.SearchTempResults = self.MangasCurrentPage[0]

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
        
    #==================================================










    #StaticFunctions

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




    def Compare(self, Searched, Data):
        Correct = 0
        for word in Searched:
            if word in Data:
                Correct +=1 
        return Correct/len(Searched)
    
    def delete_until_special_character(self, text):
        words = text.split(" ")
        if words:  # Ensure there are words to delete
            words.pop()  # Remove the last word
        new_text = " ".join(words)
        return new_text