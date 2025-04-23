import mysql.connector

mydb = mysql.connector.connect(
        host = "localhost",
        user="root",
        password="root",
        database="workout"
    )

cursor = mydb.cursor(dictionary=True)

def get_user_password(username):
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    users = cursor.fetchall()
    if len(users) == 0:
        return False
    else:
        return(users[0]["passwd"])

def get_exercise(username):
    cursor.execute(f"SELECT userID FROM users WHERE username = '{username}'")
    userID = cursor.fetchall()[0]["userID"]
    cursor.execute(f"SELECT exercise_name FROM exercises WHERE userID IN ('1','{userID}')")
    exercise_list = []
    for i in cursor.fetchall():
        exercise_list.append(i.get("exercise_name"))
    return exercise_list

def create_exercise(username, exercise_name, exercise_type):
    cursor.execute(f"SELECT userID FROM users WHERE username = '{username}'")
    userID = cursor.fetchall()[0]["userID"]

    cursor.execute(f"SELECT exercise_type_id FROM exercise_types WHERE exercise_type = '{exercise_type}'")
    exercise_type_IDs = cursor.fetchall()

    if len(exercise_type_IDs) == 0:
        print("Invalid exercise type name")
        return False
    else:
        exercise_type_ID = exercise_type_IDs[0]["exercise_type_id"]

    cursor.execute(f"INSERT INTO exercises(exercise_name, exercise_type_id, userID) VALUES ('{exercise_name}', '{exercise_type_ID}', '{userID}')")
    mydb.commit()
    print("record inserted")

def delete_exercise(username, exercise_name):
    cursor.execute(f"SELECT userID FROM users WHERE username = '{username}'")
    userID = cursor.fetchall()[0]["userID"]

    cursor.execute(f"SELECT exercise_id FROM exercises WHERE exercise_name = '{exercise_name}' AND userID = '{userID}'")
    exercise_IDs = cursor.fetchall()

    if len(exercise_IDs) == 0:
        print("Exercise does not exist / you cannot delete this exercise.")
        return False
    else:
        exercise_ID = exercise_IDs[0]["exercise_id"]

    cursor.execute(f"DELETE FROM exercises WHERE exercise_id = '{exercise_ID}'")
    mydb.commit()
    print("record removed")


# create_exercise("suman", "sTest", "Weights")

delete_exercise("suman", "sTest")