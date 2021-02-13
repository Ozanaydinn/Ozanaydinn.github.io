CREATE TABLE user(
    user_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    password VARCHAR(64) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    PRIMARY KEY(user_id)
);

CREATE TABLE student(
    student_id INT,
    PRIMARY KEY(student_id),
    FOREIGN KEY(student_id) REFERENCES user(user_id) ON
    DELETE CASCADE
);

CREATE TABLE instructor(
    instructor_id INT,
    PRIMARY KEY(instructor_id),
    FOREIGN KEY(instructor_id) REFERENCES user(user_id) ON
    DELETE CASCADE
);