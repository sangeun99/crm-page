import uuid

class Id():
    def __init__(self):
        self.id = uuid.uuid4()
    
    def generate(self):
        return self.id