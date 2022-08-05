import requests

from dataclasses import dataclass

from flask import Flask, jsonify, abort
#from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://data.db'
#CORS(app)

db = SQLAlchemy(app)

@dataclass
class paymentinf(db.Model):
    name: str
    tmnCode: str
    haskKey: str
    partCode: str
    name = db.Column(db.String(200), primary_key=True, autoincrement=True)
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
        product_id = id
        product_user = ProductUser(user_id=json['id'], product_id=product_id)
        db.session.add(product_user)
        db.session.commit()
    except:
        abort(400, 'You already liked this product')

    return jsonify({
        "message": "success"
    })

def test():
    print(paymentinf.query.all())
if __name__ == '__main__':
    test()
    #app.run(debug=True, host='0.0.0.0')