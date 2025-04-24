import mysql.connector
import tabulate

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
        return (users[0]["userID"]), (users[0]["passwd"])

def get_exercise(userID, exerciseID=''):
    if userID == 1:
        cursor.execute(f"SELECT * FROM exercises WHERE exercise_id LIKE '{exerciseID}%'")
    else:
        cursor.execute(f"SELECT * FROM exercises WHERE userID IN ('1','{userID}') AND exercise_id LIKE '{exerciseID}%'")
    exercise_list = []
    values = cursor.fetchall()
    return tabulate.tabulate(values, headers = "keys", tablefmt="github")

def create_exercise(userID, exercise_name, exercise_type_ID):
    cursor.execute(f"SELECT * FROM exercise_types WHERE exercise_type_id = '{exercise_type_ID}'")
    exercise_type_IDs = cursor.fetchall()

    if len(exercise_type_IDs) == 0:
        print("Invalid exercise type name")
        return False

    cursor.execute(f"INSERT INTO exercises(exercise_name, exercise_type_id, userID) VALUES ('{exercise_name}', '{exercise_type_ID}', '{userID}')")
    mydb.commit()
    cursor.execute(f"SELECT * FROM exercises WHERE userID IN ('1','{userID}') AND exercise_name = '{exercise_name}'")
    values = cursor.fetchall()
    return tabulate.tabulate(values, headers = "keys", tablefmt="github")

def delete_exercise(userID, exercise_ID):
    cursor.execute(f"SELECT * FROM exercises WHERE exercise_ID = '{exercise_ID}' AND userID = '{userID}'")
    exercise_IDs = cursor.fetchall()

    if len(exercise_IDs) == 0:
        print("Exercise does not exist / you cannot delete this exercise.")
        return False

    cursor.execute(f"DELETE FROM exercises WHERE exercise_id = '{exercise_ID}'")
    mydb.commit()
    print("record removed")
    return "record removed"

# print(create_exercise(2, "STest", 1))

print(get_exercise(1))