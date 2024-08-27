to install all the libraries used in this project you can navigate to the file directory
and run : 
            pip install -r requirements.txt




This code will grap the manga Data Names from the Mangasee123 Servers


```python
from MangaSeeAPI import MangaGraper
Graper = MangaGraper()
```

This allows you to search for certain manga with word to word match of the accuracy you set 


```python
results = Graper.Search("Attack on Titan", Accuracy=0.60)

print(results)
```

    Pridction: 100 => Show: Attack on Titan
    Pridction: 100 => Show: Attack on Titan - Before the Fall
    Pridction: 100 => Show: Attack on Titan - Junior High
    Pridction: 100 => Show: Attack on Titan - Lost Girls
    Pridction: 100 => Show: Attack on Titan - No Regrets
    Pridction: 100 => Show: Attack on Titan - No Regrets - Color
    Pridction: 66 => Show: Spoof on Titan
    Pridction: 100 => Show: The Best of Attack on Titan - In Color
    [{'i': 'Shingeki-No-Kyojin', 's': 'Attack on Titan', 'a': ['Shingeki no Kyojin'], 'p': 1.0}, {'i': 'Shingeki-No-Kyojin-Before-The-Fall', 's': 'Attack on Titan - Before the Fall', 'a': ['Shingeki no Kyojin - Before the Fall'], 'p': 1.0}, {'i': 'Shingeki-Kyojin-Chuugakkou', 's': 'Attack on Titan - Junior High', 'a': ['Shingeki! Kyojin Chuugakkou'], 'p': 1.0}, {'i': 'Shingeki-No-Kyojin---Lost-Girls', 's': 'Attack on Titan - Lost Girls', 'a': ['Shingeki no Kyojin - Lost Girls'], 'p': 1.0}, {'i': 'Shingeki-No-Kyojin-Birth-Of-Levi', 's': 'Attack on Titan - No Regrets', 'a': ['Shingeki no Kyojin - Birth of Levi'], 'p': 1.0}, {'i': 'Attack-on-Titan-No-Regrets-Color', 's': 'Attack on Titan - No Regrets - Color', 'a': [], 'p': 1.0}, {'i': 'Spoof-on-Titan', 's': 'Spoof on Titan', 'a': ['Sungeki no Kyojin'], 'p': 0.6666666666666666}, {'i': 'The-Best-of-Attack-on-Titan-In-Color', 's': 'The Best of Attack on Titan - In Color', 'a': [], 'p': 1.0}]
    

This will do a quick requrests and grap all the manga chapters that it can see note that this will not work for mangas
that have a seasonal Chapters


```python
#Write the Exact name or altirnative name
MangaName = "Attack on Titan"
DictionaryPointer = Graper.GrapMangaData(MangaName)
if DictionaryPointer != None:
    print(DictionaryPointer)
    print(f"Chapter Found: {Graper.Data[DictionaryPointer]["NumberOfChapters"]}")
    #print(Graper.Data)
```

    Shingeki-No-Kyojin
    Chapter Found: 141
    

This will install Chapters in parallel depending on the ThreadCount you set


```python
Graper.InstallMangaChaptersMT(DictionaryPointer, "Attack on Titan",ThreadCount=10)
```

To read the manga you can run the GUI file which will provided you with a interface to select the manga and the chapter and read


later on you want to update the Manga Chapters to get the new chapters and for
you can reinstall the manga again or you can use the update function to check 
for new chapters and then run the installation function. 


```python
from MangaSeeAPI import MangaGraper
Graper = MangaGraper()

direcotry = "One Piece"
DictionaryPointer = Graper.CheckUpdates(direcotry) # this will check the chapters you have 
                                                   # and filter out the ones you have from 
                                                   # the ones you dont have
```


```python
Graper.InstallMangaChaptersMT(DictionaryPointer, "One Piece", ThreadCount=10) #this will start installing the chapters
```

If you want to install more than one manga at the same time it is recommended that you use the class MangaGraper for each installation
