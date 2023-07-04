from models.id import Id

class Item:
    def __init__(self, itemname, itemtype, unitprice) :
        self.itemId = Id().generate()
        self.itemName = itemname
        self.itemType = itemtype
        self.unitPrice = unitprice

    def generate(self) :
        generatedData = {
            "id" : self.itemId,
            "name" : self.itemName,
            "type" : self.itemType,
            "unitprice" : self.unitPrice
        }
        return generatedData