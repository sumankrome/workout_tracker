from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import Flask, jsonify, request, session, make_response
import jwt
import sql

app = Flask(__name__)
app.config['SECRET_KEY'] = "753e55a1cf494a9780836ab6a8b04cbd"

def authenticate(token):
    try:
        return jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError, jwt.exceptions.InvalidSignatureError, jwt.exceptions.InvalidTokenError) as error:
        print(f'Unable to decode the token, error: {error}')
        return False


## NEED A FUNCTION TO CREATE EXERCISE DATA
## NEED AUTHENTICATION

## WORKOUT MANAGEMENT : CREATE, UPDATE, DELETE, SCHEDULE (specific date and time), LIST and GENERATE REPORTS

@app.route("/")
def home():
    return jsonify({"message": "logged in"})

@app.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    password = sql.get_user_password(data["username"])
    if data["password"] == password:
        session['login'] = True
        now = datetime.now(timezone.utc)
        token = jwt.encode({
            'user':data["username"],
            "iat": now.timestamp(),
            "exp": (now + timedelta(hours=24)).timestamp()
        }, app.config['SECRET_KEY'])

        return jsonify({'token': token})
    else:
        return make_response("Unable to verify", 403, {'WWW-Authenticate': 'Basic realm:"Authentication Failed."'})

@app.route("/exercise", methods = ["GET", "POST"])
def exercise():
    data = request.get_json()
    decoded_token = authenticate(data["token"])
    if decoded_token == False:
        return make_response("Invalid Token", 401, {'WWW-Authenticate': 'Basic realm:"Invalid JWT Token."'})
    else:
        user = decoded_token["user"]

    if request.method == "POST":
        return jsonify({"message": f"POST {user}"})
    elif request.method == "GET":
        exercises = sql.get_exercise(user)
        return jsonify({"message": f"{exercises}"})

if __name__ == "__main__":
    app.run(debug=True)