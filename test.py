from flask import Flask, request, jsonify, session, url_for, redirect
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Table, Column, Integer, String, MetaData, inspect
from flask_oauthlib.client import OAuth
import requests
from authlib.integrations.flask_client import OAuth
from flask_mail import Mail, Message
import random
import sqlite3

app = Flask(__name__)
api = Api(app)
app.secret_key = 'mehul'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'example@gmail.com'  # Use your actual Gmail address
app.config['MAIL_PASSWORD'] =  "password"    # Use your generated App Password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
db = SQLAlchemy(app)

mail = Mail(app)

class AccountModel(db.Model):
    __tablename__ = 'Account'
    
    user_id = db.Column(db.String, primary_key = True)
    user_pwd = db.Column(db.String, nullable = False)
    user_email = db.Column(db.String, nullable = False)
    user_mobile =db.Column(db.Integer, nullable = False)
    pwd_change_code = db.Column(db.Integer, nullable = True)
    
    def __repr__(self):
        return f"Student(id = {id})"


def create_user_ledger_table(user_id): 
    create_table_query = "CREATE TABLE IF NOT EXISTS {} (name TEXT NOT NULL PRIMARY KEY, balance INTEGER ) ".format(user_id)
    conn = sqlite3.connect('database.db')
    conn.execute(create_table_query) 
    conn.commit()
    conn.close()
    return user_id

def add_transaction(user_id, name, data):
    add_entry = """ 
    UPDATE {}
    SET balance = balance + {}
    WHERE name = '{}';
    """.format(user_id, int(data), name)
    conn = sqlite3.connect('database.db')
    conn.execute(add_entry) 
    conn.commit()
    conn.close()
    
def add_user(user_id, name, data):
    add_entry = """
    INSERT INTO {}
    VALUES ('{}', {})
    """.format(user_id, name, data)
    conn = sqlite3.connect('database.db')
    conn.execute(add_entry) 
    conn.commit()
    conn.close()
    

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
        print(code)
        results = AccountModel.query.filter_by(user_id = id).first()
        if not results:
            return jsonify({"message" : "User does not exists", 'status' : 404})
        else:
            if int(code) == int(results.pwd_change_code):
                results.user_pwd = new_pwd
                db.session.commit()
                return jsonify({"message" : "Successful", 'status' : 200})
            else:
                db.session.commit()
                return jsonify({"message" : "Code not right", 'status' : 409})
    
    
@app.route('/api/add_txn', methods = ['PUT'])
def add_txn():
    id = request.json.get('id')
    pwd = request.json.get('pwd')
    
    name = request.json.get('name')
    data = request.json.get('data')
    
    acc = AccountModel.query.filter_by(user_id = id).first()
    if acc.user_pwd == pwd:
        add_transaction(id, name, data)
        return jsonify({'message' : "Successful", 'status' : 200})
    else:
        return jsonify({'message' : "Unsuccessful, Incorrect Password", 'status' : 409})
    
@app.route('/api/send_code', methods = ['GET'])
def send_code():
    id = request.json.get('id')
    acc = AccountModel.query.filter_by(user_id = id).first()
    print(str(acc.user_email))
    msg = Message(
        subject='Hello from the other side!', 
        sender='testflaskapplication@gmail.com',  # Ensure this matches MAIL_USERNAME
        recipients=[str(acc.user_email)]  # Replace with actual recipient's email
        )
    code = random.randint(1111,9999)
    msg.body = "Hey, your code to change your password is {}.".format(code)
    mail.send(msg)
    
    add_entry = """
    UPDATE Account
    SET pwd_change_code = {}
    WHERE user_id = '{}'
    """.format(code, id)
    conn = sqlite3.connect('database.db')
    conn.execute(add_entry) 
    conn.commit()
    conn.close()
    
    return jsonify({'message' : "Successful", 'status' : 200})

@app.route('/api/add_user', methods = ['PUT'])
def add_user_api():
    id = request.json.get('id')
    pwd = request.json.get('pwd')
    
    name = request.json.get('name')
    data = request.json.get('data')
    
    acc = AccountModel.query.filter_by(user_id = id).first()
    if acc.user_pwd == pwd:
        add_user(id, name, data)
        return jsonify({'message' : "Successful", 'status' : 200})
    else:
        return jsonify({'message' : "Unsuccessful, Incorrect Password", 'status' : 409})
    
@app.route('/api/get_data', methods = ['GET'])
def get_data():
    id = request.json.get('id')
    pwd = request.json.get('pwd')
    
    acc = AccountModel.query.filter_by(user_id = id).first()
    if acc.user_pwd == pwd:
        add_entry = """
        SELECT *
        FROM {}
        """.format(id)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(add_entry)
        
        rows = cursor.fetchall()
        result = {row[0]: row[1] for row in rows}
        return jsonify({'message' : "Successful", 'status' : 200, 'data' : result})
    else:
        return jsonify({'message' : "Unsuccessful, Incorrect Password", 'status' : 409})


    

           
api.add_resource(LoginResource, '/api/login')
api.add_resource(RegisterResource, '/api/register')
api.add_resource(PasswordChangeResource, '/api/pwd_reset')

if __name__ == "__main__":
    app.run(debug=True)