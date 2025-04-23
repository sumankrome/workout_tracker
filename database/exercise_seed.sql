INSERT INTO exercise_types(exercise_type) VALUES
    ('Weights'),
    ('Stretches'),
    ('Cardio');

INSERT INTO exercises(exercise_name, exercise_type_id, userID) VALUES
    ('Bench Press', 1, 1),
    ('Running', 3, 1),
    ('Yoga', 2, 1),
    ('Hammer Curl', 1, 1);

INSERT INTO muscle_groups(exercise_id, muscle_group, specific_muscle) VALUES
    (1, 'Chest', 'Upper'),
    (4, 'Arms', NULL);

INSERT INTO users(username, email, passwd) VALUES
    ('admin', 'admin', 'admin'),
    ('suman', 's@g.com', 's123'),
    ('test', 'test@g.com', 't123');

INSERT INTO workouts(userID, workout_name, workout_date, workout_duration) VALUES
    (1, 'sumanTest', '2024-04-16 12:12', '20'),
    (1, 'sumanTest2', '2025-04-16 12:12', '25'),
    (2, 'testtest', '2025-04-16 12:12', '60');

INSERT INTO workout_details(workout_id, exercise_id, exercise_duration, exercise_weight, exercise_reps, exercise_rest) VALUES
    (1, 1, 18, 80, 3, 3),
    (2, 1, 18, 85, 3, 3),
    (3, 2, 18, NULL, NULL, NULL);