from flask_pymongo import PyMongo
import flask
import dbObject
import responseObject
import json
import sys
from datetime import timedelta
from datetime import datetime
from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = flask.Flask(__name__)
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/test")
db = mongodb_client.db

app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "test1234"
app.config["JWT_SECRET_KEY"] = "test1234"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

jwt = JWTManager(app)

@app.route('/register', methods=['POST'])
def register():
    
    content = request.json
    first_name = content['first_name']
    last_name = content['last_name']
    phone_number = content['phone_number']
    address = content['address']
    pin = content['pin']
    
    try_find = db.register.find_one({"phone_number": phone_number})

    if (try_find is not None):
        return jsonify(message="Phone Number already registered")
    
    register_object = dbObject.Register(first_name, last_name, phone_number, 
                                        address, pin, 0)

    db.register.insert_one(register_object.__dict__)
    
    register_response = responseObject.RegisterResponse("SUCCESS", register_object.user_id,
                                                        first_name, last_name, phone_number,
                                                        address, register_object.created_date)
    
    return register_response.serialize

@app.route('/login', methods=['POST'])
def login():
    
    content = request.json
    phone_number = content['phone_number']
    pin = content['pin']
    
    try_find = db.register.find_one({"phone_number": phone_number, "pin": pin})

    if (try_find is None):
        return jsonify(message="Phone number and pin doesn’t match.")
    
    access_token = create_access_token(identity=try_find["user_id"])
    refresh_token = create_refresh_token(identity=try_find["user_id"])
        
    login_response = responseObject.LoginResponse("SUCCESS", access_token, refresh_token)
    
    return login_response.serialize

@app.route('/topup', methods=['POST'])
@jwt_required()
def topup():
    
    content = request.json
    topup_amount = content['amount']
    current_user = get_jwt_identity()
    
    try_find = db.register.find_one({"user_id": current_user})

    if (try_find is None):
        return jsonify(message="User ID from JWT invalid")
    
    user_id = try_find["user_id"]
    balance = try_find["balance"]
    balance_after = balance + topup_amount
    
    db.register.update_one({'user_id': user_id}, {"$set": { 'balance': balance_after }})
    
    topup_object = dbObject.Topup(user_id, topup_amount, balance, balance_after)

    db.topup.insert_one(topup_object.__dict__)
    
    topup_response = responseObject.TopupResponse("SUCCESS", topup_object.top_up_id,
                                                  topup_amount, balance, balance_after,
                                                  topup_object.created_date)
    
    return topup_response.serialize
    
@app.route('/pay', methods=['POST'])
@jwt_required()
def pay():
    
    content = request.json
    amount = content['amount']
    remarks = content['remarks']
    current_user = get_jwt_identity()
    
    try_find = db.register.find_one({"user_id": current_user})

    if (try_find is None):
        return jsonify(message="User ID from JWT invalid")
    
    user_id = try_find["user_id"]
    balance = try_find["balance"]
    balance_after = balance - amount
    
    if (balance_after < 0):
        return jsonify(message="Balance is not enough")

    db.register.update_one({'user_id': user_id}, {"$set": { 'balance': balance_after }})
    
    pay_object = dbObject.Pay(user_id, amount, remarks, balance, balance_after)

    db.pay.insert_one(pay_object.__dict__)
    
    pay_response = responseObject.PayResponse("SUCCESS", pay_object.payment_id,
                                                  amount, remarks, balance, balance_after,
                                                  pay_object.created_date)
    
    return pay_response.serialize

@app.route('/transfer', methods=['POST'])
@jwt_required()
def transfer():
    
    content = request.json
    target_user = content['target_user']
    amount = content['amount']
    remarks = content['remarks']
    current_user = get_jwt_identity()
    
    try_find = db.register.find_one({"user_id": current_user})

    if (try_find is None):
        return jsonify(message="User ID from JWT invalid")
    
    try_find_target = db.register.find_one({"user_id": target_user})
    if (try_find_target is None):
        return jsonify(message="Target User ID is invalid")
    
    user_id = try_find["user_id"]
    balance = try_find["balance"]
    balance_after = balance - amount
    
    balance_after_target = try_find_target["balance"] + amount
    
    if (balance_after < 0):
        return jsonify(message="Balance is not enough")

    db.register.update_one({'user_id': user_id}, {"$set": { 'balance': balance_after }})
    db.register.update_one({'user_id': target_user}, {"$set": { 'balance': balance_after_target }})
    
    transfer_object = dbObject.Transfer(user_id, target_user, amount, remarks, balance, balance_after)

    db.transfer.insert_one(transfer_object.__dict__)
    
    transfer_response = responseObject.TransferResponse("SUCCESS", transfer_object.transfer_id,
                                                  amount, remarks, balance, balance_after,
                                                  transfer_object.created_date)
    
    return transfer_response.serialize

@app.route('/transactions', methods=['GET'])
@jwt_required()
def transactions():

    current_user = get_jwt_identity()
    
    try_find = db.register.find_one({"user_id": current_user})

    if (try_find is None):
        return jsonify(message="User ID from JWT invalid")
    
    user_id = try_find["user_id"]

    try_find_topup = db.topup.find({"user_id": user_id})
    
    try_find_pay = db.pay.find({"user_id": user_id})
     
    try_find_transfer = db.transfer.find({"user_id": user_id})
    
    transaction_response = responseObject.TransactionResponse("SUCCESS", try_find_topup, try_find_pay, try_find_transfer)
    
    return transaction_response.serialize

@app.route('/update', methods=['PUT'])
@jwt_required()
def update():

    current_user = get_jwt_identity()
    content = request.json
    first_name_new = content['first_name']
    last_name_new = content['last_name']
    address_new = content['address']
    
    try_find = db.register.find_one({"user_id": current_user})

    if (try_find is None):
        return jsonify(message="User ID from JWT invalid")
    
    user_id = try_find["user_id"]
    
    if (first_name_new is None or first_name_new == ""):
        first_name_new = try_find["first_name"]
        
    if (last_name_new is None or last_name_new == ""):
        last_name_new = try_find["last_name"]
        
    if (address_new is None or address_new == ""):
        address_new = try_find["address"]
        
    updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    db.register.update_one({'user_id': user_id}, {"$set": {'first_name': first_name_new, 
                                                           'last_name': last_name_new,
                                                           'address': address_new,
                                                           'updated_date': updated_date}})

    
    update_response = responseObject.UpdateResponse("SUCCESS", user_id, first_name_new,
                                                    last_name_new, address_new, updated_date)
    
    return update_response.serialize

@jwt.invalid_token_loader
def invalid_token_callback(jwt_header):
    return jsonify(message="Unauthenticated"), 401

def parse_json(data):
    return json.loads(json.dumps(data))

app.run()