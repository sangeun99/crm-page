from models.id import Id

class Store:
    def __init__(self, storetype, storelocation, address) :
        self.id = Id().generate()
        self.name = storetype + " " + storelocation
        self.type = storetype
        self.address = address

    def generate(self):
        generatedData = {
            "id" : self.id, 
            "name" : self.name, 
            "type" : self.type, 
            "address" : self.address
        }
        return generatedData