from models.id import Id

import datetime


class Order():
    
    def __init__(self, storeid, userid):
        self.orderId = Id().generate()
        self.orderAt = datetime.datetime.now()
        self.storeId = storeid
        self.userId = userid
    
    def generate(self) :
        generatedData = {
            "orderid" : self.orderId,
            "orderat" : self.orderAt,
            "storeid" : self.storeId,
            "userid" : self.userId
        }
        return generatedData
