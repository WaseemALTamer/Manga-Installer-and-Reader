import json



"""
def extract_array_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        if isinstance(data, list):
            return data
        else:
            print("The JSON file does not contain an array.")


Data = extract_array_from_json("MangaSearcher.json")

TestName = "Attak on tatin full of dawn"
"""


class Analyser():
    def __init__(self):
        self.Data = [{ "i" : "Attak-on-tatin-full-of-dawn",
                       "s" : "Attak on tatin full of dawn",
                       "a" : [],
                       }]

    def Search(self, Name, Accuracy=0.75):
        Results = []
        Name = Name.lower().split()
        for Object in self.Data:
            Percentage = self.Compare(Name, Object["s"].lower().split())
            if Percentage >= Accuracy:
                Object["p"] = Percentage
                Results.append(Object)
            else:
                for Alt in Object["a"]:
                    Percentage = self.Compare(Name, Alt.lower().split())
                    if Percentage >= Accuracy:
                        Object["p"] = Percentage
                        Results.append(Object)
        return Results

    def DataLookUp(self, Name):
        for Object in self.Data:
            if Name == Object["s"]:
                return Object["i"]
            else:
                for Alt in Object["a"]:
                    if Name in Object["a"]:
                        return Object["i"]
        return None
    
    def NameDataGrap(self, Name):
        for Object in self.Data:
            if Name == Object["i"]:
                return Object
            if Name == Object["s"]:
                return Object
            else:
                for Alt in Object["a"]:
                    if Name in Object["a"]:
                        return Object
        return None

    #Private Functions#
    def Compare(self, Searched, Data):
        Correct = 0
        for word in Searched:
            if word in Data:
                Correct +=1 
        return Correct/len(Searched)
    


