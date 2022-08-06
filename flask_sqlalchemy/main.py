import requests

from dataclasses import dataclass

from flask import Flask, jsonify, abort
#from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#CORS(app)

db = SQLAlchemy(app)

@dataclass
class paymentinf(db.Model):
    name: str
    tmnCode: str
    haskKey: str
    partCode: str
    name = db.Column(db.String(200), primary_key=True)
    tmnCode = db.Column(db.String(200))
    haskKey = db.Column(db.String(200))
    partCode = db.Column(db.String(200))

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
    print(paymentinf.query.all())

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