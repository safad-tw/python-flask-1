from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity



app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)
jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type=float,
    required=True,
    help="This field cant be left blank")

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404

    def post(self,name):



        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message':"An item with name '{}' already exist".format(name)},400

        request_data = Item.parser.parse_args()
        item = {'name': name, 'price':request_data['price']}
        items.append(item)
        return item, 201

    def put(self,name):

        request_data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            new_item = {'name': name, 'price':request_data['price']}
            items.append(new_item)
        else:
            item.update(request_data)
        return item

    def delete(self,name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted'}

class ItemsList(Resource):
    def get(self):
        return items

api.add_resource(Item, '/item/<string:name>')

api.add_resource(ItemsList, '/items')


app.run(port=5000, debug=True)
