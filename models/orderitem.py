from models.id import Id


class Orderlist():
    # Id,OrderId,ItemId
    def __init__(self, orderid, itemid):
        self.id = Id().generate()
        self.orderId = orderid
        self.itemId = itemid

    def generate(self):
        generatedData = {
            "id" : self.id,
            "orderid" : self.orderId,
            "itemid" : self.itemId
        }
        return generatedData