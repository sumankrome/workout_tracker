from datetime import datetime, timedelta, timezone
from flask import Flask, jsonify, request, session, make_response
import jwt
import sql

app = Flask(__name__)
app.config['SECRET_KEY'] = "753e55a1cf494a9780836ab6a8b04cbd"

def authenticate(token):
    if token:
        auth_token = token.split(" ")[1]
    else:
        auth_token = ''
    try:
        return jwt.decode(auth_token, app.config['SECRET_KEY'], algorithms=["HS256"])
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
    userID, password = sql.get_user_password(data["username"])
    if data["password"] == password:
        session['login'] = True
        now = datetime.now(timezone.utc)
        token = jwt.encode({
            'userID': userID,
            "iat": now.timestamp(),
            "exp": (now + timedelta(hours=24)).timestamp()
        }, app.config['SECRET_KEY'])

        return jsonify({'token': token})
    else:
        return make_response("Unable to verify", 403, {'WWW-Authenticate': 'Basic realm:"Authentication Failed."'})

@app.route("/exercise/<exerciseID>", methods = ["GET", "DELETE"])
def exercise(exerciseID):
    data = request.headers.get('Authorization')
    decoded_token = authenticate(data)
    if decoded_token == False:
        return make_response("Invalid Token", 401, {'WWW-Authenticate': 'Basic realm:"Invalid JWT Token."'})
    else:
        userID = decoded_token["userID"]

    if request.method == "DELETE":
        return sql.delete_exercise(userID, exerciseID)
    elif request.method == "GET":
        if exerciseID == "all":
            return sql.get_exercise(userID)
        else:
            return sql.get_exercise(userID, exerciseID)

@app.route("/exercise", methods = ["POST"])
def create_exercise():
    data = request.headers.get('Authorization')
    decoded_token = authenticate(data)
    if decoded_token == False:
        return make_response("Invalid Token", 401, {'WWW-Authenticate': 'Basic realm:"Invalid JWT Token."'})
    else:
        userID = decoded_token["userID"]

    body = request.get_json()

    return sql.create_exercise(userID, body["exercise_name"], body["exercise_type_ID"])

if __name__ == "__main__":
    app.run(debug=True)