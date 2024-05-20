from flask import Flask, request, Response, jsonify, session, redirect
from flask_cors import CORS, cross_origin
import bcrypt
from functools import wraps
import logging
import re
from storage.storage_client import BlobClient
from transformers import AutoTokenizer, T5ForConditionalGeneration
import os
from database.database_client import DBClient
from computer_vision.cv_util import ingredients_from_image
import jwt
import datetime

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
app.config['SECRET_KEY'] = os.env('APP_SECRET_KEY')
CORS(
    app,
    origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    supports_credentials=True
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Preflight request for CORS
@app.before_request
def basic_authentication():
    """Handles preflight requests"""
    if request.method.lower() == "options":
        return Response()

blobclient = BlobClient()
recipeClient = DBClient("recipe")
userClient = DBClient("user")

JWT_SECRET = os.env('APP_JWT_SECRET')

def logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return jsonify({"error": "Unauthorized access"}), 403
        try:
            jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 403
        return f(*args, **kwargs)
    return decorated_function

def hash_password(password):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_value = bcrypt.hashpw(password_bytes, salt)
    return hash_value.decode('utf-8')


def validate_email(email):
    pattern = r'[^@]+@[^@]+\.[^@]+'
    return bool(re.match(pattern, email))

def validate_password(password):
    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return bool(re.match(pattern, password))

############
## ROUTES ##
############

@app.route("/healthz", methods=["GET"])
def health_check():
    return {"msg": "good"}, 200

@app.route("/api/user/signup", methods=["POST", "OPTIONS"])
@cross_origin()
def create_user():
    data = request.get_json()
    email = data.get("user_email")
    password = data.get("user_password")

    if not validate_email(email):
        return jsonify("Error: Invalid email"), 400

    if not validate_password(password):
        return jsonify("Error: Invalid password"), 400

    hashed_password = hash_password(password)

    user_signin = {
        "email": email,
        "password": hashed_password,
    }

    try:
        userClient.insert_document(user_signin)
        return jsonify({"message": "Success: added user to database"}), 200
    except Exception as e:
        app.logger.error(f"Error: Unable to add user to database {str(e)}")
        return jsonify("Error: unable to add user to database"), 500


@app.route("/api/user/login", methods=["POST", "OPTIONS"])
@cross_origin()
def login_user():
    data = request.get_json()
    email = data.get("user_email")
    password = data.get("user_password")

    if not email or not password:
        return jsonify("Error: Invalid email or password"), 400

    user = userClient.get_user(email)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        token = jwt.encode({
            'user_email': email,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }, JWT_SECRET, algorithm="HS256")

        response = jsonify({"message": "Login successful"})
        response.set_cookie('token', token, httponly=True)
        return response, 200
    else:
        return jsonify("Error: Username or Password is not correct"), 401

@app.route("/api/user/dashboard", methods=["GET"])
@cross_origin()
@logged_in
def user_dashboard():
    token = request.cookies.get('token')
    decoded_token = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    user_email = decoded_token['user_email']
    return jsonify({"message": f"Welcome to your dashboard, {user_email}!"}), 200

@app.route("/api/user/logout", methods=["POST", "OPTIONS"])
@cross_origin()
def logout_user():
    response = jsonify({"message": "Logout successful"})
    response.set_cookie('token', '', expires=0)
    return response, 200

@app.route("/api/recipes", methods=["POST", "OPTIONS"])
@cross_origin()
@logged_in
def get_recipe():
    ingredients = request.get_json()
    try:
        recipes = recipeClient.get_document(ingredients["ingredients"])
        recipes.append({"ingredients": ingredients["ingredients"]})
        return recipes, 200
    except:
        return 500
    
@app.route('/api/upload', methods=['POST', 'OPTIONS'])
@cross_origin()
# @logged_in
def upload_file():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Preflight request success'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH,OPTIONS')
        return response
    else:
        if "file" not in request.files:
            return "No file found", 404
        
        file = request.files["file"]
                                
        if file.filename == "":
            return "No file found", 404
        
        temp_path = f"{file.filename}"
        file.save(temp_path)

        try:
            blobclient.upload_blob(temp_path, file.filename)
        except:
            return "Unable to upload to blob", 400
        
        try:
            raw_ingredents = ingredients_from_image(file.filename)
        except:
            return "YOU BLOODY DONKEY!!!", 400
        
        ingredients = set()

        for raw_ingredient in raw_ingredents:
            if isinstance(raw_ingredient, list):
                for ingredient in raw_ingredient:
                    if ingredient:
                        ingredients.add(ingredient)
            elif len(raw_ingredient) != 0:
                ingredients.add(raw_ingredient)

        os.remove(temp_path)

        try:
            ingredients = list(ingredients)
            print("Ingredients: ",ingredients)
            recipes = recipeClient.get_document(ingredients)
            recipes.append({"ingredients": ingredients})
            return recipes, 200
        except:
            return 500

if __name__ == "__main__":
    app.run(debug=True)
