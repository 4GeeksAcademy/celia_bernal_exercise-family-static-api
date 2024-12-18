"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body = jsonify(members)
    return response_body, 200


@app.route('/member/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    member = jackson_family.get_member(member_id)
    print(member)
    response_body = jsonify(member)
    return response_body, 200

@app.route('/member', methods=['POST'])
def add_member():
    body= request.get_json(silent=True)
    if body is None:
        return jsonify({'msg':'Debes enviar informacion en el body'}),400
    if "first_name" not in body:
        return jsonify({'msg':'name es obligatorio'}),400
    if "lucky_numbers" not in body:
        return jsonify({'msg':'numbers es obligatorio'}),400
    new_member = {
        "first_name": body ['first_name'],
        "last_name":jackson_family.last_name,
        "age": body['age'],
        "lucky_numbers": body['lucky_numbers']

    }
    if "id" in body:
        new_member['id'] = body['id']
    new_members = jackson_family.add_member(new_member)
    return jsonify({'msg':'ok','members':new_members}),200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_one_member(member_id):
    member = jackson_family.delete_member(member_id)
    response_body = jsonify({'done': True})
    return response_body, 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
