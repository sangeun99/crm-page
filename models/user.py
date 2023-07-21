import datetime

from models.id import Id


class User:
    def __init__(self, name, gender, birthdate, address) :
        self.id = Id().generate()
        self.name = name
        self.gender = gender
        self.birthdate = birthdate
        dateToday = datetime.datetime.now()
        if birthdate :
            self.age = dateToday.year - int(birthdate[:4]) + 1
        else :
            self.age = 0
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