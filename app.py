from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource, reqparse

from models import db, User, Contact

UPLOAD_FOLDER = './upload'
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)
db.init_app(app)
ma = Marshmallow()

db.create_all(app=app)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("name", "phone")


class ContactSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("sender_name", "name", "sender_phone", "phone")


class UserResource(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', type=str, help='Name', required=True)
        parser.add_argument('phone', type=str, help='Phone', required=True)
        args = parser.parse_args()
        user = User.query.filter_by(phone=args['phone']).all()
        if user:
            return "Already Exists", 200
        user = User()
        user.name = args['name']
        user.phone = args['phone']
        db.session.add(user)
        db.session.commit()
        schema = UserSchema()
        return schema.dump(user), 200


class ContactResource(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('name', type=str, help='Name', required=True)
        parser.add_argument('contact', type=dict, help='Name', required=True, action='append')
        parser.add_argument('phone', type=str, help='Phone', required=True)
        args = parser.parse_args()

        contacts = args['contact']
        for data in contacts:
            contact = Contact()
            print(data.get('name'))
            contact.name = data.get('name')
            contact.phone = data.get('phone')
            contact.sender_name = args['name']
            contact.sender_phone = args['phone']
            db.session.add(contact)
        db.session.commit()
        return "Done", 201


@app.route('/api/all/<phone>', methods=['GET'])
def all(phone):
    contacts = Contact.query.filter_by(phone=phone).all()
    schema = ContactSchema(many=True)
    return {'data': schema.dump(contacts)}, 200


@app.route('/api/user_contacts/<phone>', methods=['GET'])
def phon_contacts(phone):
    contacts = Contact.query.filter_by(sender_phone=phone).all()
    schema = ContactSchema(many=True)
    return {'data': schema.dump(contacts)}, 200


if __name__ == '__main__':
    api.add_resource(UserResource, '/api/user/')
    api.add_resource(ContactResource, '/api/contact/')
    app.run(host='0.0.0.0', debug=True)
