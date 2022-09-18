from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from peewee import *

db = 'bmc.db'
database = SqliteDatabase(db)

class BaseModel(Model):
	class Meta:
		database=database

class bmc(BaseModel):
	idbmc = AutoField(primary_key=True)
	kodekelompok = TextField()
	type = IntegerField() # 1 for Business, 2 for Users, 3 for Problems, 4 for Motives, 5 for Fears, 6 for Solution, 7 for Alternatives, 8 For Competitive Adventages, 9 for Unique value
	name = CharField()

def create_tables():
	with database:
		database.create_tables([bmc])


app = Flask(__name__)
api = Api(app)

class resourcebmc(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument("kodekelompok", location="args")
		parser.add_argument("idbmc", location="args")
		args = parser.parse_args()

		if args['kodekelompok'] and args['idbmc']:
			return jsonify({"data":None, "message":"Too Many Parameters"})
		elif args['kodekelompok']:
			data_bmc = list(bmc.select().where(bmc.kodekelompok == args['kodekelompok']).dicts())
		elif args['idbmc']:
			data_bmc = list(bmc.select().where(bmc.idbmc == args['idbmc']).dicts())
		else:
			data_bmc = list(bmc.select().dicts())
		return jsonify({"data":data_bmc, "message":"success"})

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("kodekelompok", location="json")
		parser.add_argument("type", location="json")
		parser.add_argument("name", location="json")
		args = parser.parse_args()

		bmc.create(kodekelompok=args['kodekelompok'],type=args['type'],name=args['name'])
		return jsonify({"data":None, "message":"create bmc success"})

	def put(self):
		parser = reqparse.RequestParser()
		parser.add_argument('idbmc', location='json')
		parser.add_argument('name', location='json')

		args =parser.parse_args()

		# cek if bmc exists
		cek = bmc.select().where(bmc.idbmc == args['idbmc'])
		if cek.exists():
			update_bmc = bmc.update(name=args['name']).where(bmc.idbmc==args['idbmc'])
			update_bmc.execute()
			return jsonify({"data":None, "message":"Update bmc success"})
		else:
			return jsonify({"data":None, "message":"Update bmc Failed. bmc not Found"})

	def delete(self):
		parser = reqparse.RequestParser()
		parser.add_argument('idbmc', location="args")
		args = parser.parse_args()
		# cek if bmc exists
		cek = bmc.select().where(bmc.idbmc == args['idbmc'])
		if cek.exists():
			delete_bmc = bmc.delete().where(bmc.idbmc == args['idbmc'])
			delete_bmc.execute()
			return jsonify({"data":None, "message":"Delete bmc success"})
		else:
			return jsonify({"data":None, "message":"Delete bmc Failed. bmc not Found"})

api.add_resource(resourcebmc, '/')

if __name__ == '__main__':
	create_tables()
	app.run(port=5003, debug=True)