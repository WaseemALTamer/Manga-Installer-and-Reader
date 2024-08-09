from DataAnalyser import Analyser
from bs4 import BeautifulSoup
import threading
import requests
import json
import re
import os



class MangaGraper():

    def __init__(self):
        self.Data = {}
        self.Searcher = Analyser()
        self.Searcher.Data = self.GrapAllMangaNames()
        self.Queue = []
        self.ChaptersFinishedInstalling = 0
        self.Errors = []
        

    def Search(self, Manga, Accuracy = 0.6):
        Results = self.Searcher.Search(Manga,Accuracy)
        for result in Results:
            print(f"Pridction: {int(result["p"]*100)} => Show: {result["s"]}")
        return Results
        


    def GrapAllMangaNames(self):
        url = f"https://mangasee123.com/_search.php"
        response = requests.get(url)
        Data = response.json()
        return Data




    #Note that the MnagaLinkNmae should have the exact name or altirnative name of the manga
    def GrapMangaData(self, Name, Chapter=1, Page=1):
        MangaLinkName = self.Searcher.DataLookUp(Name)
        if MangaLinkName == None:
            print("Manga data was not found in the response or the servers did not response try change the Chapter or page number pramameters to one that exist")
            return None
        script = self.ScriptFromHtml(MangaLinkName,Chapter=Chapter,Page=Page)
        self.ExtractChaptersAndPages(script, MangaLinkName)
        return MangaLinkName
    


    def InstallMangaChaptersMT(self, MangaDataPointer, MangaName, directory= f"MangaOutput", ThreadCount=5):
        response = requests.get(f"https://temp.compsci88.com/cover/{MangaDataPointer}.jpg")

        if not os.path.exists(f"{directory}/{MangaName}"):
            os.makedirs(f"{directory}/{MangaName}")

        with open(f"{directory}/{MangaName}/Cover.jpg", "wb") as f:
            f.write(response.content)

        with open(f"{directory}/{MangaName}/Data.json","w") as f:
            json.dump(self.Searcher.NameDataGrap(MangaDataPointer), f, indent=4)


        self.ChaptersFinishedInstalling = 0

        for Chapter in range(self.Data[MangaDataPointer]["NumberOfChapters"]):
            if self.Data[MangaDataPointer]["Chapters"][Chapter]["ChpaterID"] != None:
                self.Queue.append(Chapter)
            else:
                self.ChaptersFinishedInstalling += 1
        
        Threads = []
        for i in range(ThreadCount):
            Thread = threading.Thread(target=self.ChapterInstallThread, args=(MangaDataPointer, MangaName, directory,))
            Thread.start()
            Threads.append(Thread)
        
        for Thread in Threads:
            Thread.join()
        


    def CheckUpdates(self, MangaFolder, directory="MangaOutput", Chapter=1, Page=1):
        if not os.path.exists(f"{directory}/{MangaFolder}"):
            print("Manga is not installed")
            return    
        with open(f"{directory}/{MangaFolder}/Data.json","r") as f:
            MangaData = json.load(f)
        Pointer = self.GrapMangaData(MangaData["i"], Chapter=Chapter, Page=Page)
        InstalledChapters = self.folders_in_directory(f"{directory}/{MangaFolder}")
        ChaptersID = []
        for Chapter in InstalledChapters:
            ChaptersID.append(Chapter)
        ChaptersFound = []
        for ChapterKey, ChapterData in self.Data[Pointer]["Chapters"].items():
            if str(ChapterData["ChpaterID"]) in ChaptersID:
                ChapterData["ChpaterID"] = None
            else:
                ChaptersFound.append(ChapterData["ChpaterID"])
        print(ChaptersFound)
        print(len(ChaptersFound))
        return Pointer















    #=================================================================
    #========================Private Functions========================
    #=================================================================


    def ChangeNumberFormate(self, number, Format):
        if isinstance(number, float):
            if number.is_integer():
                return f"{int(number):0{Format}d}"
            else:
                integer_part, decimal_part = str(number).split('.')
                integer_part = f"{int(integer_part):0{Format}d}"
                return f"{integer_part}.{decimal_part}"
        else:
            return f"{number:0{Format}d}"
    
    def ChapterInstallThread(self, MangaDataPointer, MangaName, directory):
        while len(self.Queue) != 0:
            Chapter = self.Queue[0]
            self.Queue.pop(0)
            Index = str(self.Data[MangaDataPointer]["Chapters"][Chapter]["ChpaterID"])[0]
            ChapterID = self.Data[MangaDataPointer]["Chapters"][Chapter]["ChpaterID"]
            ChapterNumber = (self.Data[MangaDataPointer]["Chapters"][Chapter]["ChpaterID"] - (int(Index) * 100000))/10
            PagesNum = self.Data[MangaDataPointer]["Chapters"][Chapter]["NumPages"]
            try:
                Domain = self.GrapImageLinkDirctory(MangaDataPointer,Chapter=self.ChangeNumberFormate(ChapterNumber, 0),Index=str(Index))
                FilePath = f"{directory}/{MangaName}/{ChapterID}"
                if not os.path.exists(FilePath):
                    os.makedirs(FilePath)
                for Page in range(1, PagesNum+1):
                    url = self.GrapImageUrl(Domain, MangaDataPointer, ChapterNumber, Page)
                    for i in range(0,3):
                        response = requests.get(url)
                        if response.status_code == 200:
                            break

                    with open(f"{FilePath}/{Page}.png", "wb") as f:
                        f.write(response.content)
                
                self.ChaptersFinishedInstalling +=1
                print(f"Completion => {(self.ChaptersFinishedInstalling / self.Data[MangaDataPointer]["NumberOfChapters"])*100}% ==> {self.ChaptersFinishedInstalling}/{self.Data[MangaDataPointer]["NumberOfChapters"]}")

            except Exception as e:
                self.Errors.append([MangaDataPointer, MangaName, Chapter, e])
                print(e)




    #this function often needs the script that contain the chapters and the pages often used with the ScriptFromHtml function
    def GrapImageUrl(self, Domain, MangaDataPointer, ChapterID, Page, Index=1):
        if Index != 1:
            url = f"https://{Domain}/manga/{MangaDataPointer}/{self.ChangeNumberFormate(ChapterID, 4)}-index-{Index}-{self.ChangeNumberFormate(Page, 3)}.png"
        else:
            url = f"https://{Domain}/manga/{MangaDataPointer}/{self.ChangeNumberFormate(ChapterID, 4)}-{self.ChangeNumberFormate(Page, 3)}.png"
        return url
    
    def GrapChapterUrl(self, Manga, Chapter, Page, Index=1):
        if Index != 1:
            url = f"https://mangasee123.com/read-online/{Manga}-chapter-{Chapter}-index-{Index}-page-{Page}.html"
        else:
            url = f"https://mangasee123.com/read-online/{Manga}-chapter-{Chapter}-page-{Page}.html"
        return url

    def ScriptFromHtml(self, Manga, Chapter=1, Page=1, Index=1):
        try:
            url = self.GrapChapterUrl(Manga, Chapter, Page, Index=Index)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find('script', string=re.compile(r'vm\.CurPage'))
            script_content = script_tag.string
            return script_content
        except Exception as e:
            print("Script was not found in the response or the servers did not response try change the Chapter or page number pramameters to one that exist")
            print(e)
            return None
    def ExtractChaptersAndPages(self, script, Manga):

        match = re.search(r'vm\.CHAPTERS = (\[.*?\]);', script, re.DOTALL)
        #Path = re.search(r'vm\.CurPathName = "(.*?)";', script, re.DOTALL)
        MangaData = json.loads(match.group(1))

        self.Data[Manga] = {}
        self.Data[Manga]["NumberOfChapters"] = len(MangaData)
        #self.Data[Manga]["Path"] = Path.group(1)
        self.Data[Manga]["Chapters"] = {}

        for index, Chapter in enumerate(MangaData):
            self.Data[Manga]["Chapters"][int(index)] = {}
            self.Data[Manga]["Chapters"][int(index)]["ChpaterID"] = int(Chapter["Chapter"])
            self.Data[Manga]["Chapters"][int(index)]["NumPages"] = int(Chapter["Page"])
            self.Data[Manga]["Chapters"][int(index)]["Date"] = Chapter["Date"]

    def GrapImageLinkDirctory(self, Manga, Chapter=1, Page=1, Index=1):
        script = self.ScriptFromHtml(Manga, Chapter=Chapter, Page=Page, Index=Index)
        Path = re.search(r'vm\.CurPathName = "(.*?)";', script, re.DOTALL)
        return Path.group(1)
    

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