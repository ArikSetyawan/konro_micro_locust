from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from peewee import *

db = "fnf.db"
database = SqliteDatabase(db)

class BaseModel(Model):
	class Meta:
		database=database

class fnf(BaseModel):
	idfnf = AutoField(primary_key=True)
	kodekelompok = TextField(null=True)
	type = IntegerField(null=True) # 1 for functional, 2 for non functional
	name = CharField()
	description = TextField(null=True)
	backlog = TextField(null=True)
	assign_to = TextField(null=True)
	target_finish = IntegerField(null=True)
	target_finish_print = CharField(null=True)
	status = CharField(null=True) # status progress fitur

def create_tables():
	with database:
		database.create_tables([fnf])

app = Flask(__name__)
api = Api(app)

class resourceFNF(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('kodekelompok')
		parser.add_argument('idfnf')
		args = parser.parse_args()
		if args['idfnf'] and args['kodekelompok']:
			return jsonify({"data":None, "message":"Too Many Parameters"})
		elif args['idfnf']:
			dataFNF = list(fnf.select().where(fnf.idfnf==args['idfnf']).dicts())
		elif args['kodekelompok']:
			dataFNF = list(fnf.select().where(fnf.kodekelompok==args['kodekelompok']).dicts())
		else:
			dataFNF = list(fnf.select().dicts())
		return jsonify({"data":dataFNF, "message":"success"})

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('kodekelompok', location='json')
		parser.add_argument('type', location='json')
		parser.add_argument('name', location='json')
		parser.add_argument('description', location='json')
		parser.add_argument('backlog', location='json')
		args = parser.parse_args()

		fnf.create(
			kodekelompok=args['kodekelompok'],
			type=args['type'],
			name=args['name'],
			description=args['description'],
			backlog=args['backlog']
		)

		return jsonify({"data":None, "message":"Create FNF Success"})


	def put(self):
		parser = reqparse.RequestParser()
		parser.add_argument('idfnf', location='json')
		parser.add_argument('status', location='json')
		parser.add_argument('description', location='json')
		parser.add_argument('assign_to', location='json')
		args = parser.parse_args()

		# cek if fnf exists
		cek = fnf.select().where(fnf.idfnf == args['idfnf'])
		if cek.exists():
			update_fnf = fnf.update(
					status=args['status'],
					description=args['description'],
					assign_to=args['assign_to']
				).where(fnf.idfnf == args['idfnf'])

			update_fnf.execute()

			return jsonify({"data":None, "message":"Update FNF Success"})
		else:
			return jsonify({"data":None, "message":"Update FNF Failed. FNF not Found"})

	def delete(self):
		parser = reqparse.RequestParser()
		parser.add_argument('idfnf', location='args')
		args = parser.parse_args()

		# cek if fnf exists
		cek = fnf.select().where(fnf.idfnf == args['idfnf'])
		if cek.exists():
			delete_fnf = fnf.delete().where(fnf.idfnf == args['idfnf'])
			delete_fnf.execute()
			return jsonify({"data":None, "message":"Delete FNF Success"})
		else:
			return jsonify({"data":None, "message":"Delete FNF Failed. FNF not Found"})



api.add_resource(resourceFNF, '/')

if __name__ == '__main__':
	create_tables()
	app.run(debug=True)