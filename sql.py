from flask import jsonify
import mysql.connector

mydb = mysql.connector.connect(
        host = "localhost",
        user="root",
        password="root",
        database="workout"
    )

cursor = mydb.cursor(dictionary=True)

def create_user(username, password, email):
    
    validation = validate_creation_data(username, password, email)
    
    if isinstance(validation, bool):
        cursor.execute(f"INSERT INTO users(username, email, passwd) VALUES ('{username}','{email}','{password}')")
        mydb.commit()

        return jsonify({"message": f"Account creation successful. Please use your username '{username}' to login."})
    else:
        return validation

def get_user_details(username):
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    users = cursor.fetchall()
    if len(users) == 0:
        return False
    else:
        return (users[0]["userID"]), (users[0]["passwd"])

def get_exercise(userID, exerciseID=''):
    if userID == 1:
        cursor.execute(f"SELECT * FROM exercises WHERE exercise_id LIKE '{exerciseID}%'")
    else:
        cursor.execute(f"SELECT * FROM exercises WHERE userID IN ('1','{userID}') AND exercise_id LIKE '{exerciseID}%'")
    exercises = cursor.fetchall()
    
    return jsonify({"exercises": exercises})

def create_exercise(userID, exercise_name, exercise_type_ID):
    cursor.execute(f"SELECT * FROM exercise_types WHERE exercise_type_id = '{exercise_type_ID}'")
    exercise_type_IDs = cursor.fetchall()

    if len(exercise_type_IDs) == 0:
        print("Invalid exercise type name")
        return False

    cursor.execute(f"INSERT INTO exercises(exercise_name, exercise_type_id, userID) VALUES ('{exercise_name}', '{exercise_type_ID}', '{userID}')")
    mydb.commit()
    cursor.execute(f"SELECT * FROM exercises WHERE userID IN ('1','{userID}') AND exercise_name = '{exercise_name}' ORDER BY exercise_id DESC")
    values = cursor.fetchall()
    return jsonify(values[0])

def delete_exercise(userID, exercise_ID):
    cursor.execute(f"SELECT * FROM exercises WHERE exercise_ID = '{exercise_ID}' AND userID = '{userID}'")
    exercise_IDs = cursor.fetchall()

    if len(exercise_IDs) == 0:
        return jsonify({"message": "Exercise does not exist / you cannot delete this exercise."})

    cursor.execute(f"DELETE FROM exercises WHERE exercise_id = '{exercise_ID}'")
    mydb.commit()
    return jsonify({"message": "record removed"})

def validate_creation_data(username, password, email):
    valid_details = True
    username_error = {"username error": "The username is too short. Please choose another."}
    password_error = {"password error": "The password is too short. Please choose another."}
    email_error = {"email error": "The email is not valid. Please choose another."}
    username_dupe_error = {"message": "The username provided already exists, please choose another."}
    email_dupe_error = {"message": "The email is already linked to an existing user, please choose another."}
    errors = {}
    if len(username) < 5:
        errors = errors | username_error
        valid_details = False
    if len(password) < 5:
        errors = errors | password_error
        valid_details = False
    if len(email) < 5:
        errors = errors | email_error
        valid_details = False

    if not valid_details:
        return jsonify(errors)

    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    users = cursor.fetchall()
    if len(users) != 0:
        errors = errors | username_dupe_error
        valid_details = False

    cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
    users = cursor.fetchall()
    if len(users) != 0:
        errors = errors | email_dupe_error
        valid_details = False

    if not valid_details:
        return jsonify(errors)
    
    return True