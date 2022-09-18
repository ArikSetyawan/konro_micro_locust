from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from peewee import * 

db = "ces.db"
database = SqliteDatabase(db)

class BaseModel(Model):
	class Meta:
		database=database

class ces(BaseModel):
	idces = AutoField(primary_key=True)
	kodekelompok = TextField()
	type = IntegerField() # 1 for cause, 2 for efect, 3 for solution
	name = CharField()

def create_tables():
	with database:
		database.create_tables([ces])


app = Flask(__name__)
api = Api(app)

class resourceCes(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument("kodekelompok", location="args")
		parser.add_argument("idces", location="args")
		args = parser.parse_args()

		if args['kodekelompok'] and args['idces']:
			return jsonify({"data":None, "message":"Too Many Parameters"})
		elif args['kodekelompok']:
			data_ces = list(ces.select().where(ces.kodekelompok == args['kodekelompok']).dicts())
		elif args['idces']:
			data_ces = list(ces.select().where(ces.idces == args['idces']).dicts())
		else:
			data_ces = list(ces.select().dicts())
		return jsonify({"data":data_ces, "message":"success"})

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("kodekelompok", location="json")
		parser.add_argument("type", location="json")
		parser.add_argument("name", location="json")
		args = parser.parse_args()

		ces.create(kodekelompok=args['kodekelompok'],type=args['type'],name=args['name'])
		return jsonify({"data":None, "message":"create CES success"})

	def put(self):
		parser = reqparse.RequestParser()
		parser.add_argument('idces', location='json')
		parser.add_argument('name', location='json')

		args =parser.parse_args()

		# cek if ces exists
		cek = ces.select().where(ces.idces == args['idces'])
		if cek.exists():
			update_ces = ces.update(name=args['name']).where(ces.idces==args['idces'])
			update_ces.execute()
			return jsonify({"data":None, "message":"Update CES success"})
		else:
			return jsonify({"data":None, "message":"Update CES Failed. CES not Found"})

	def delete(self):
		parser = reqparse.RequestParser()
		parser.add_argument('idces', location="args")
		args = parser.parse_args()
		# cek if ces exists
		cek = ces.select().where(ces.idces == args['idces'])
		if cek.exists():
			delete_ces = ces.delete().where(ces.idces == args['idces'])
			delete_ces.execute()
			return jsonify({"data":None, "message":"Delete CES success"})
		else:
			return jsonify({"data":None, "message":"Delete CES Failed. CES not Found"})

api.add_resource(resourceCes, '/')

if __name__ == '__main__':
	create_tables()
	app.run(port=5001, debug=True)