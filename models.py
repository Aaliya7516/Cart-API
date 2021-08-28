from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
class EmployeeModel(db.Model):
    __tablename__ = "table"
 
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String())
    name = db.Column(db.String())
    price = db.Column(db.Integer())
    count = db.Column(db.Integer())
 
    def __init__(self, img,name,price,count):
        self.img = img
        self.name = name
        self.price = price
        self.count = count
 
    def __repr__(self):
        return f"{self.name}:{self.price}"