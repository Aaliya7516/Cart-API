from flask import Flask, request

import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cart.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


class cart(db.Model):
 
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


class cartSchema(ma.Schema):
    class Meta:
        fields = ("id", "img", "name", "price", "count")


cart_schema = cartSchema()
carts_schema = cartSchema(many=True)


class cartListResource(Resource):
    def get(self):
        carts = cart.query.all()
        return carts_schema.dump(carts)

    def post(self):
        new_cart = cart(
            img=request.json['img'],
            name=request.json['name'],
            price=request.json['price'],
            count=request.json['count'],
        )
        db.session.add(new_cart)
        db.session.commit()
        return cart_schema.dump(new_cart)


class cartResource(Resource):
    def get(self, cart_id):
        cart = cart.query.get_or_404(cart_id)
        return cart_schema.dump(cart)

    def patch(self, cart_id):
        cart = cart.query.get_or_404(cart_id)

        if 'img' in request.json:
            cart.title = request.json['img']
        if 'name' in request.json:
            cart.content = request.json['name']
        if 'price' in request.json:
            cart.content = request.json['price']
        if 'count' in request.json:
            cart.content = request.json['count']
        

        db.session.commit()
        return cart_schema.dump(cart)

    def delete(self, cart_id):
        cart = cart.query.get_or_404(cart_id)
        db.session.delete(cart)
        db.session.commit()
        return 'Data deleted Successfully', 204


api.add_resource(cartListResource, '/carts')
api.add_resource(cartResource, '/carts/<int:cart_id>')


if __name__ == '__main__':
    app.run(debug=True)