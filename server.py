from flask import Flask, request, jsonify, session, url_for, redirect
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, inspect
import requests
from flask_mail import Mail, Message
import random
import sqlite3

app = Flask(__name__)
api = Api(app)
app.secret_key = 'mehul'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/test'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'testflaskapplication@gmail.com'  # Use your actual Gmail address
app.config['MAIL_PASSWORD'] =  "kgop xpog hcvd ihhr"    # Use your generated App Password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
db = SQLAlchemy(app)
engine = create_engine('mysql+mysqlconnector://root:root@localhost/test')
Session = sessionmaker(bind=engine) 
session = Session() 
Base = declarative_base()

mail = Mail(app)

class AccountModel(db.Model):
    __tablename__ = 'Account'
    
    user_id = db.Column(db.String(50), primary_key = True)
    user_pwd = db.Column(db.String(50), nullable = False)
    user_email = db.Column(db.String(50), nullable = False)
    user_mobile =db.Column(db.Integer, nullable = False)
    pwd_change_code = db.Column(db.Integer, nullable = True)
    
    def __repr__(self):
        return f"Student(id = {id})"
    
def create_table(table_name, DynamicBase):
    class DynamicTable(DynamicBase):
        __tablename__ = table_name
        __table_args__ = {'extend_existing': True}
        name = Column(String(255), primary_key=True)
        balance = Column(Integer, nullable=False)

    return DynamicTable

def create_user_ledger_table(user_id): 
    engine = create_engine('mysql+mysqlconnector://root:root@localhost/test')
    metadata = MetaData() # Define the table schema 
    user_ledger_table = Table(user_id, metadata, 
                              Column('name', String(255), nullable=False, primary_key=True), 
                              Column('balance', Integer, nullable=False)) 
    metadata.create_all(engine)
    print("test")

def add_user(user_id, name, data):
    DynamicBase = declarative_base(class_registry=dict())
    dynamic_table = create_table(user_id, DynamicBase)
    session = Session()
    
    result = session.query(dynamic_table).filter_by(name=name).first()
    
    if result:
        session.close()
        return False

    txn = dynamic_table(name=name, balance=data)
    session.add(txn)
    session.commit()
    session.close()
    
    return True

def add_transaction(user_id, name, data): 
    DynamicBase = declarative_base(class_registry=dict()) 
    dynamic_table = create_table(user_id, DynamicBase) 
    session = Session() 
    result = session.query(dynamic_table).filter_by(name=name).first() 
    if result: 
        result.balance += int(data) 
        session.commit() 
        session.close() 
        return True 
    else: 
        session.close() 
        return False
    
with app.app_context():
    db.create_all()

class LoginResource(Resource):
    def get(self):
        id = request.json.get('id')
        pwd = request.json.get('pwd')
        
        results = AccountModel.query.filter_by(user_id = id).first()
        if not results:
            return jsonify({"message" : "User does not exists", 'status' : 404})
        
        if pwd == results.user_pwd:
            return jsonify({'message' : "Successful", 'status' : 200})
        else:
            return jsonify({'message' : "Unsuccessful", 'status' : 209})
        
class RegisterResource(Resource):
    def put(self):
        id = request.json.get('id')
        pwd = request.json.get('pwd')
        email = request.json.get('email')
        number = request.json.get('mobile')
        
        results = AccountModel.query.filter_by(user_id = id).first()
        if results:
            return jsonify({"message" : "User already exists", 'status' : 409})
        
        create_user_ledger_table(id)
        acc = AccountModel(user_id = id, user_pwd = pwd, user_email = email, user_mobile = number)
        db.session.add(acc)
        db.session.commit()
        
        return jsonify({'message' : "Successful", 'status' : 200})
    
class PasswordChangeResource(Resource):
    def post(self):
        id = request.json.get('id')
        new_pwd = request.json.get('new_pwd')
        code = request.json.get('code')
        results = AccountModel.query.filter_by(user_id = id).first()
        if not results:
            return jsonify({"message" : "User does not exists", 'status' : 404})
        else:
            if int(code) == int(results.pwd_change_code):
                results.user_pwd = new_pwd
                db.session.commit()
                db.session.close()
                return jsonify({"message" : "Successful", 'status' : 200})
            else:
                db.session.commit()
                db.session.close()
                return jsonify({"message" : "Code not right", 'status' : 409})
    
    
@app.route('/api/add_txn', methods = ['PUT'])
def add_txn():
    id = request.json.get('id')
    pwd = request.json.get('pwd')
    
    name = request.json.get('name')
    data = request.json.get('data')
    
    acc = AccountModel.query.filter_by(user_id = id).first()
    if not acc:
        return jsonify({'message' : "User does not exists", 'status' : 200})
    if acc.user_pwd == pwd:
        msg = add_transaction(id, name, data)
        if msg:
            return jsonify({'message' : "Successful", 'status' : 200})
        else:
            return jsonify({'message' : "User does not exists", 'status' : 404})
    else:
        return jsonify({'message' : "Unsuccessful, Incorrect Password", 'status' : 409})
    
@app.route('/api/send_code', methods = ['GET'])
def send_code():
    id = request.json.get('id')
    acc = AccountModel.query.filter_by(user_id = id).first()
    
    if not acc:
        db.session.close()
        return jsonify({'message' : "User does not exists", 'status' : 404})
    
    msg = Message(
        subject='Hello from the other side!', 
        sender='testflaskapplication@gmail.com',
        recipients=[str(acc.user_email)]
        )
    code = random.randint(1111,9999)
    msg.body = "Hey, your code to change your password is {}.".format(code)
    mail.send(msg)
    
    acc.pwd_change_code = code
    db.session.commit()
    db.session.close()
    
    return jsonify({'message' : "Successful", 'status' : 200})

@app.route('/api/add_user', methods = ['PUT'])
def add_user_api():
    id = request.json.get('id')
    pwd = request.json.get('pwd')
    
    name = request.json.get('name')
    data = request.json.get('data')
    
    acc = AccountModel.query.filter_by(user_id = id).first()
    if acc.user_pwd == pwd:
        msg = add_user(id, name, data)
        if msg:
            return jsonify({'message' : "Successful", 'status' : 200})
        else:
            return jsonify({'message' : "Name already exists", 'status' : 409})
    else:
        return jsonify({'message' : "Unsuccessful, Incorrect Password", 'status' : 409})
    
@app.route('/api/get_data', methods = ['GET'])
def get_data():
    id = request.json.get('id')
    pwd = request.json.get('pwd')
    
    acc = AccountModel.query.filter_by(user_id = id).first()
    if not acc:
        return jsonify({'message' : "User does not exists", 'status' : 404})
    elif acc.user_pwd == pwd:        
        DynamicBase = declarative_base(class_registry=dict())
        dynamic_table = create_table(id, DynamicBase)
        session = Session()

        rows = session.query(dynamic_table).all()
        
        result = {row.name: row.balance for row in rows}
        
        session.close()
        
        return jsonify({'message': "Successful", 'status': 200, 'data': result})

    else:
        return jsonify({'message' : "Unsuccessful, Incorrect Password", 'status' : 409})
    
    
@app.route('/api/rm_acc', methods = ['DELETE'])
def remove_acc():
    id = request.json.get('id')
    pwd = request.json.get('pwd')

    acc = AccountModel.query.filter_by(user_id=id).first()

    if not acc:
        return jsonify({'message': "Id does not exist", 'status': 404})
    else:
        if acc.user_pwd == pwd:
            db.session.delete(acc)
            db.session.commit()
            return jsonify({'message': "Account Deleted Successfully", 'status': 200})
        else:
            return jsonify({'message': "Wrong Password", 'status': 409})

        
@app.route('/api/rm_user', methods = ['DELETE'])
def remove_user():
    id = request.json.get('id')
    pwd = request.json.get('pwd')
    name = request.json.get('name')
    
    acc = AccountModel.query.filter_by(user_id=id).first()

    if not acc:
        return jsonify({'message': "Id does not exist", 'status': 404})
    elif acc.user_pwd != pwd:
        return jsonify({'message': "Incorrect Password", 'status': 409})
    
    DynamicBase = declarative_base(class_registry=dict())
    dynamic_table = create_table(id, DynamicBase)
    session = Session()
    
    result = session.query(dynamic_table).filter_by(name=name).first()
    
    if result:
        session.delete(result)
        session.commit()
        session.close()
        return jsonify({'message': "Person Removed", 'status': 200})
    else:
        session.close()
        return jsonify({'message': "Person Not Found", 'status': 404})



           
api.add_resource(LoginResource, '/api/login')
api.add_resource(RegisterResource, '/api/register')
api.add_resource(PasswordChangeResource, '/api/pwd_reset')

if __name__ == "__main__":
    app.run(debug=True)