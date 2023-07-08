import datetime
from models.id import Id

class User:
    def __init__(self, name, gender, birthdate, address, id="") :
        if id :
            self.id = id
        else :
             self.id = Id().generate()
        self.name = name
        self.gender = gender
        self.birthdate = birthdate
        dateToday = datetime.datetime.now()
        self.age = dateToday.year - int(birthdate[:4]) + 1
        self.address = address

    def generate(self):
        generatedData = {
            "id" : self.id, 
            "name" : self.name, 
            "gender" : self.gender, 
            'age' : self.age, 
            "birthdate" : self.birthdate, 
            'address' : self.address
        }
        return generatedData
    
print(User('김', 'female', '1997-03-21', '주소', "").generate())
print(User('김', 'female', '1997-03-21', '주소', '3242837942').generate())