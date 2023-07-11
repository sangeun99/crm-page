import uuid

class Id():
    def __init__(self):
        # sqlite3 uuid type 지원하지 않아 string으로 변환
        self.id = str(uuid.uuid4())
    
    def generate(self):
        return self.id