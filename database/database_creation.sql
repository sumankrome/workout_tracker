CREATE DATABASE workout;

USE workout;

CREATE TABLE users(
    userID INT AUTO_INCREMENT,
    username varchar(255) NOT NULL UNIQUE,
    email varchar(255) NOT NULL UNIQUE,
    passwd varchar(255) NOT NULL,
    PRIMARY KEY (userID)
);

CREATE TABLE workouts(
    workout_id INT AUTO_INCREMENT,
    userID INT NOT NULL,
    workout_name varchar(255),
    workout_date datetime NOT NULL,
    workout_duration int NULL,
    PRIMARY KEY (workout_id),
    FOREIGN KEY (userID) REFERENCES users(userID)
);

CREATE TABLE exercise_types(
    exercise_type_id INT AUTO_INCREMENT,
    exercise_type varchar(255),
    PRIMARY KEY (exercise_type_id)
);

CREATE TABLE exercises(
    exercise_id INT AUTO_INCREMENT,
    exercise_type_id INT NOT NULL,
    exercise_name varchar(255) NOT NULL,
    details text NULL,
    userID INT,
    PRIMARY KEY (exercise_id),
    FOREIGN KEY (exercise_type_id) REFERENCES exercise_types(exercise_type_id)
);


CREATE TABLE muscle_groups(
    muscle_group_id INT AUTO_INCREMENT,
    exercise_id INT NOT NULL,
    muscle_group varchar(255),
    specific_muscle varchar(255),
    PRIMARY KEY (muscle_group_id),
    FOREIGN KEY (exercise_id) REFERENCES exercises(exercise_id)
);

CREATE TABLE workout_details(
    workout_detail_id INT AUTO_INCREMENT,
    workout_id INT,
    exercise_id INT,
    exercise_duration int NULL,
    exercise_weight int NULL,
    exercise_reps int NULL,
    exercise_rest int NULL,
    PRIMARY KEY (workout_detail_id),
    FOREIGN KEY (exercise_id) REFERENCES exercises(exercise_id),
    FOREIGN KEY (workout_id) REFERENCES workouts(workout_id)
);
