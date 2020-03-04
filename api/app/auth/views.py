from flask import request, make_response, json
from flask_login import login_user, logout_user, login_required
from . import auth
from .. import mongo

@auth.route('/login', methods=['POST'])
def login():
    content = request.json
    
    user_register = mongo.db.users.find_one({
        'email': content['email'],
        'password': content['password'],
    })

    if user_register is None:
        return make_response('¡NO está registrado!')

    return make_response('El usuario está registrado')
