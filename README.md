{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "to install all the libraries used in this project you can navigate to the file directory\n",
    "and run : \n",
    "            pip install -r requirements.txt\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "This code will grap the manga Data Names from the Mangasee123 Servers"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "from MangaSeeAPI import MangaGraper\n",
    "Graper = MangaGraper()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "This allows you to search for certain manga with word to word match of the accuracy you set "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Pridction: 100 => Show: Attack on Titan\n",
      "Pridction: 100 => Show: Attack on Titan - Before the Fall\n",
      "Pridction: 100 => Show: Attack on Titan - Junior High\n",
      "Pridction: 100 => Show: Attack on Titan - Lost Girls\n",
      "Pridction: 100 => Show: Attack on Titan - No Regrets\n",
      "Pridction: 100 => Show: Attack on Titan - No Regrets - Color\n",
      "Pridction: 66 => Show: Spoof on Titan\n",
      "Pridction: 100 => Show: The Best of Attack on Titan - In Color\n",
      "[{'i': 'Shingeki-No-Kyojin', 's': 'Attack on Titan', 'a': ['Shingeki no Kyojin'], 'p': 1.0}, {'i': 'Shingeki-No-Kyojin-Before-The-Fall', 's': 'Attack on Titan - Before the Fall', 'a': ['Shingeki no Kyojin - Before the Fall'], 'p': 1.0}, {'i': 'Shingeki-Kyojin-Chuugakkou', 's': 'Attack on Titan - Junior High', 'a': ['Shingeki! Kyojin Chuugakkou'], 'p': 1.0}, {'i': 'Shingeki-No-Kyojin---Lost-Girls', 's': 'Attack on Titan - Lost Girls', 'a': ['Shingeki no Kyojin - Lost Girls'], 'p': 1.0}, {'i': 'Shingeki-No-Kyojin-Birth-Of-Levi', 's': 'Attack on Titan - No Regrets', 'a': ['Shingeki no Kyojin - Birth of Levi'], 'p': 1.0}, {'i': 'Attack-on-Titan-No-Regrets-Color', 's': 'Attack on Titan - No Regrets - Color', 'a': [], 'p': 1.0}, {'i': 'Spoof-on-Titan', 's': 'Spoof on Titan', 'a': ['Sungeki no Kyojin'], 'p': 0.6666666666666666}, {'i': 'The-Best-of-Attack-on-Titan-In-Color', 's': 'The Best of Attack on Titan - In Color', 'a': [], 'p': 1.0}]\n"
     ]
    }
   ],
   "source": [
    "results = Graper.Search(\"Attack on Titan\", Accuracy=0.60)\n",
    "\n",
    "print(results)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "vscode": {
     "languageId": "bat"
    }
   },
   "source": [
    "This will do a quick requrests and grap all the manga chapters that it can see note that this will not work for mangas\n",
    "that have a seasonal Chapters"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Shingeki-No-Kyojin\n",
      "Chapter Found: 141\n"
     ]
    }
   ],
   "source": [
    "#Write the Exact name or altirnative name\n",
    "MangaName = \"Attack on Titan\"\n",
    "DictionaryPointer = Graper.GrapMangaData(MangaName)\n",
    "if DictionaryPointer != None:\n",
    "    print(DictionaryPointer)\n",
    "    print(f\"Chapter Found: {Graper.Data[DictionaryPointer][\"NumberOfChapters\"]}\")\n",
    "    #print(Graper.Data)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "This will install Chapters in parallel depending on the ThreadCount you set"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "Graper.InstallMangaChaptersMT(DictionaryPointer, \"Attack on Titan\",ThreadCount=10)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "To read the manga you can run the GUI file which will provided you with a interface to select the manga and the chapter and read"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
