
import json
from datetime import date

class reader:
    #print reflector
    def print_dict(data: dict):
        for item in data:
            print(item, data[item])
    
    def read_json(file_name: str):
        with open(file_name) as json_file:
            data = json.load(json_file)
        return data
    
    def reflector(self, to_ref: str) -> str():
        reflactor = reader.read_json('reflector.json')
        
        return reflactor[to_ref]
    #Read from file and return list of string
    def read_text(filename: str) :
        file = open(filename, "r")
        l=[]
        for line in file:
            l.append(line)
        file.close()
        return l
     
     

    #Write to file and if it doesn't exist we create it
    def write_to_file(text: str, name):
           f = open(f"{name}.txt", "a")
           f.write(text+"\n")
           f.close()
          
        



