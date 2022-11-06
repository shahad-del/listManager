from flask import Flask,request,jsonify
from sqlalchemy.sql import func
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import BadRequest
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///listmanager.db"
db =SQLAlchemy(app)


class Lists(db.Model):
	__tablename__ = 'tblLists'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100),nullable=False)
	created_on = db.Column(db.DateTime(timezone=True),server_default=func.now())
	edited_on = db.Column(db.DateTime(timezone=false),server_default=func.now(),onupdate=func.now())
	
	def __repr__(self):
		return  f'{self.id} - {self.name}'

class Items(db.Model):
	__tablename__ = 'tblItems'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100),nullable=False)
	created_on = db.Column(db.DateTime(timezone=True),server_default=func.now())
	edited_on = db.Column(db.DateTime(timezone=false),server_default=func.now(),onupdate=func.now())
	list_id = db.Column(db.Integer, db.ForeignKey('tblLists.id'), nullable=False)	
	def __repr__(self):
		return  f'{self.id} - {self.items}'
# endpoints
@app.route('/')
def index():
	return 'Your api is working'
@app.route('/lists',methods=['GET'])
def lists():
	try:
		name_list = Lists.query.all()
		all_list_json = []
		for l in name_list:
			all_list_json.append({'id': l.id,'name': l.name,'created_on': l.created_on,'edited_on': l.edited_on})
		return jsonify(all_list_json)
	except BadRequest as bre:
		return jsonify({"error": str(bre)}), 400
	except Exception as e:
		return jsonify({"error": str(e)}), 400

@app.route('/lists/addlist',methods=['POST'])
def new_list():
	try:
		list_name_from_user= request.json['name']
		if len(list_name_from_user) < 1:
			return jsonify({"error":'List name is required'}),400
		li= Lists(name=list_name_from_user)
		db.session.add(li)
		db.session.commit()
		return jsonify({'id': li.id,'name': li.name,'created_on': li.created_on,'edited_on': li.edited_on}),201
	except Exception as e:
		return jsonify({"error": str(e)}), 400
@app.route('/delete_list',methods=['DELETE'])
def delete_list():
	try:
		list_name_from_user =request.json['name']
		if len(list_name_from_user) < 1:
			return jsonify({"error":'List to delete must be specified.'}),400
		Lists.query.filter_by(name= list_name_from_user).delete()
		db.session.commit()
		name_list = Lists.query.all()
		all_list_json = []
		for l in name_list:
			all_list_json.append({'id': l.id,'name': l.name,'created_on': l.created_on,'edited_on': l.edited_on})
		return jsonify(all_list_json)
	except Exception as e:
		return jsonify({"error": str(e)}), 400
@app.route('/update_list',methods=['PUT'])
def update_list():
	try:
		list_name_from_user =request.json['name']
		edited_name_from_user =request.json['edited']
		li =Lists.query.filter_by(name=list_name_from_user).first()
		li.name= edited_name_from_user
		db.session.commit()
		return jsonify({'id':li.id,'name':li.name,'created_on':li.created_on})
	except Exception as e:
		return jsonify({"error":str(e)}),400
if __name__=='__main__':
		app.run(debug = True)



