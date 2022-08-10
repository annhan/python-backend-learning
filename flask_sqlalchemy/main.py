# -*- coding: utf-8 -*-

import requests

from dataclasses import dataclass

from flask import Flask, jsonify, abort
#from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

class DbConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///items.db'
    
    SQLALCHEMY_BINDS = {
            'data': 'sqlite:///data.db'
    }
    

app = Flask(__name__)
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config.from_object(DbConfig)
#CORS(app)

db = SQLAlchemy(app)

@dataclass
class paymentinf(db.Model):
    __bind_key__ = 'data'
    name: str
    tmnCode: str
    haskKey: str
    partCode: str
    name = db.Column(db.String(200), primary_key=True)
    tmnCode = db.Column(db.String(200))
    haskKey = db.Column(db.String(200))
    partCode = db.Column(db.String(200))

@dataclass
class QuantityItems(db.Model):
    __tablename__  = "QuantityItems"
    id_item: int
    name: str
    Quantity: int
    id_item = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    Quantity = db.Column(db.Integer)

@dataclass
class glassQuantityItems(db.Model):
    __tablename__  = "glassQuantityItems"
    id_item: int
    name: str
    Quantity: int
    id_item = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    Quantity = db.Column(db.Integer)

@dataclass
class orderList(db.Model):
    __tablename__  = "orderList"
    id_order: int
    id_menu: int
    type: int
    percent: int
    id_order = db.Column(db.Integer, primary_key=True)
    id_menu = db.Column(db.Integer)
    type = db.Column(db.Integer)
    percent = db.Column(db.Integer)

def delete(id, list):
    obj = orderList.query.filter_by(id_order=id,id_menu=list[0],type=list[1],percent=list[2]).one()
    db.session.delete(obj)
    db.session.commit()

@dataclass
class infor(db.Model):
    __tablename__  = "infor"
    paras: str
    value: str
    passw: str
    secre: str
    paras = db.Column(db.String(200), primary_key=True)
    value = db.Column(db.String(200))
    passw = db.Column("pass",db.String(200)) ###################
    secre = db.Column(db.String(200))

@app.route('/api/products')
def index():
    return jsonify(paymentinf.query.all())


@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://docker.for.mac.localhost:8000/api/user')
    json = req.json()
    try:
        product_user = paymentinf(name='1', tmnCode='product_id', haskKey='3', partCode='4')
        db.session.add(product_user)
        db.session.commit()
    except:
        abort(400, 'You already liked this product')

    return jsonify({
        "message": "success"
    })

def query_all():
    print("SDS an nhàn")
    list = infor.query.all()
    for item in list:
        print(item)
        #print("id",item.id_item,item.name.encode("utf-8"),item.Quantity)
    list = paymentinf.query.all()
    for item in list:
        print(item.tmnCode)

def update_data():
    admin = paymentinf.query.filter_by(name='zalo').first()
    admin.partCode = 'my_new_email@example.com'
    db.session.commit()   



def add_data():
    product_user = paymentinf(name='1', tmnCode='product_id', haskKey='3', partCode='4')
    db.session.add(product_user)
    db.session.commit()

if __name__ == '__main__':
    query_all()
    update_data()
    add_data()
    #app.run(debug=True, host='0.0.0.0')