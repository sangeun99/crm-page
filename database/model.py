from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    Id = db.Column(db.String(64), primary_key=True)
    Name = db.Column(db.String(16))
    Gender = db.Column(db.String(16))
    Age = db.Column(db.Integer())
    Birthdate = db.Column(db.String(32))
    Address = db.Column(db.String(64))
    OrderR = db.relationship('Order', backref='users')

    def __repr__(self): # 파이썬 내장함수
        return f'<User {self.Id}, {self.Name}, {self.Gender}, {self.Age}, {self.Address}>'

class Store(db.Model):
    __tablename__ = 'stores'
    Id = db.Column(db.String(64), primary_key=True)
    Name = db.Column(db.String(32))
    Type = db.Column(db.String(32))
    Address = db.Column(db.String(64))
    OrderR = db.relationship('Order', backref='stores')

    def __repr__(self):
        return f'<Store {self.Id}, {self.Name}, {self.Type}, {self.Address}>'

class Item(db.Model):
    __tablename__ = 'items'
    Id = db.Column(db.String(64), primary_key=True)
    Name = db.Column(db.String(32))
    Type = db.Column(db.String(16))
    UnitPrice = db.Column(db.Integer())
    OrderItemR = db.relationship('OrderItem', backref='items')

    def __repr__(self):
        return f'<Item {self.Id}, {self.Name}, {self.Type}, {self.UnitPrice}>'

class Order(db.Model):
    __tablename__ = 'orders'
    Id = db.Column(db.String(64), primary_key=True)
    OrderAt = db.Column(db.String(64))
    StoreId = db.Column(db.String(64), db.ForeignKey('stores.Id'))
    UserId = db.Column(db.String(64), db.ForeignKey('users.Id'))
    OrderItemR = db.relationship('OrderItem', backref="orders")

    def __repr__(self):
        return f'<Order {self.Id}, {self.OrderAt}, {self.StoreId}, {self.UserId}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    Id = db.Column(db.String(64), primary_key=True)
    OrderId = db.Column(db.String(64), db.ForeignKey('orders.Id'))
    ItemId = db.Column(db.String(64), db.ForeignKey('items.Id'))

    def __repr__(self):
        return f'<OrderItem {self.Id}, {self.OrderId}, {self.ItemId}>'
        