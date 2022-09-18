from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from peewee import *

db = 'pdc.db'
database = SqliteDatabase(db)

class BaseModel(Model):
	class Meta:
		database=database

class pdc(BaseModel):
	idpdc = AutoField(primary_key=True)
	kodekelompok = TextField()
	type = IntegerField() # 1 for Business, 2 for Users, 3 for Problems, 4 for Motives, 5 for Fears, 6 for Solution, 7 for Alternatives, 8 For Competitive Adventages, 9 for Unique value
	name = CharField()

def create_tables():
	with database:
		database.create_tables([pdc])


app = Flask(__name__)
api = Api(app)

class resourcepdc(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument("kodekelompok", location="args")
		parser.add_argument("idpdc", location="args")
		args = parser.parse_args()

		if args['kodekelompok'] and args['idpdc']:
			return jsonify({"data":None, "message":"Too Many Parameters"})
		elif args['kodekelompok']:
			data_pdc = list(pdc.select().where(pdc.kodekelompok == args['kodekelompok']).dicts())
		elif args['idpdc']:
			data_pdc = list(pdc.select().where(pdc.idpdc == args['idpdc']).dicts())
		else:
			data_pdc = list(pdc.select().dicts())
		return jsonify({"data":data_pdc, "message":"success"})

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("kodekelompok", location="json")
		parser.add_argument("type", location="json")
		parser.add_argument("name", location="json")
		args = parser.parse_args()

		pdc.create(kodekelompok=args['kodekelompok'],type=args['type'],name=args['name'])
		return jsonify({"data":None, "message":"create pdc success"})

	def put(self):
		parser = reqparse.RequestParser()
		parser.add_argument('idpdc', location='json')
		parser.add_argument('name', location='json')

		args =parser.parse_args()

		# cek if pdc exists
		cek = pdc.select().where(pdc.idpdc == args['idpdc'])
		if cek.exists():
			update_pdc = pdc.update(name=args['name']).where(pdc.idpdc==args['idpdc'])
			update_pdc.execute()
			return jsonify({"data":None, "message":"Update pdc success"})
		else:
			return jsonify({"data":None, "message":"Update pdc Failed. pdc not Found"})

	def delete(self):
		parser = reqparse.RequestParser()
		parser.add_argument('idpdc', location="args")
		args = parser.parse_args()
		# cek if pdc exists
		cek = pdc.select().where(pdc.idpdc == args['idpdc'])
		if cek.exists():
			delete_pdc = pdc.delete().where(pdc.idpdc == args['idpdc'])
			delete_pdc.execute()
			return jsonify({"data":None, "message":"Delete pdc success"})
		else:
			return jsonify({"data":None, "message":"Delete pdc Failed. pdc not Found"})

api.add_resource(resourcepdc, '/')

if __name__ == '__main__':
	create_tables()
	app.run(port=5002, debug=True)