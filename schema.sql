CREATE DATABASE IF NOT EXISTS skill_course_db;
USE skill_course_db;

CREATE TABLE IF NOT EXISTS users (
 id INT AUTO_INCREMENT PRIMARY KEY,
 name VARCHAR(100) NOT NULL,
 email VARCHAR(150) NOT NULL UNIQUE,
 password_hash VARCHAR(255) NOT NULL,
 target_role VARCHAR(100) DEFAULT 'Data Analyst',
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS courses (
 id INT AUTO_INCREMENT PRIMARY KEY,
 title VARCHAR(180) NOT NULL,
 provider VARCHAR(100) NOT NULL,
 url VARCHAR(500) NOT NULL,
 description TEXT,
 skill_name VARCHAR(100),
 difficulty VARCHAR(50) DEFAULT 'Beginner'
);
CREATE TABLE IF NOT EXISTS progress (
 id INT AUTO_INCREMENT PRIMARY KEY,
 user_id INT NOT NULL,
 task_name VARCHAR(200) NOT NULL,
 completed BOOLEAN DEFAULT FALSE,
 completed_at TIMESTAMP NULL DEFAULT NULL,
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 CONSTRAINT fk_progress_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

INSERT INTO courses(title,provider,url,description,skill_name,difficulty)
SELECT 'Python for Everybody','University of Michigan','https://www.py4e.com/','Build a practical foundation in Python programming.','Python','Beginner'
WHERE NOT EXISTS (SELECT 1 FROM courses WHERE title='Python for Everybody');
INSERT INTO courses(title,provider,url,description,skill_name,difficulty)
SELECT 'Python Tutorial','Python.org','https://docs.python.org/3/tutorial/','Learn Python syntax and core language features.','Python','Beginner'
WHERE NOT EXISTS (SELECT 1 FROM courses WHERE title='Python Tutorial');
INSERT INTO courses(title,provider,url,description,skill_name,difficulty)
SELECT 'Problem Solving','HackerRank','https://www.hackerrank.com/domains/algorithms','Practise coding and algorithmic thinking.','DSA','Beginner'
WHERE NOT EXISTS (SELECT 1 FROM courses WHERE title='Problem Solving');
INSERT INTO courses(title,provider,url,description,skill_name,difficulty)
SELECT 'Data Structures and Algorithms','GeeksforGeeks','https://www.geeksforgeeks.org/data-structures/','Explore common data structures and algorithms.','DSA','Intermediate'
WHERE NOT EXISTS (SELECT 1 FROM courses WHERE title='Data Structures and Algorithms');
INSERT INTO courses(title,provider,url,description,skill_name,difficulty)
SELECT 'SQL Tutorial','W3Schools','https://www.w3schools.com/sql/','Learn SELECT, filtering, joins and grouping.','SQL','Beginner'
WHERE NOT EXISTS (SELECT 1 FROM courses WHERE title='SQL Tutorial');
INSERT INTO courses(title,provider,url,description,skill_name,difficulty)
SELECT 'Statistics and Probability','Khan Academy','https://www.khanacademy.org/math/statistics-probability','Study statistics and probability foundations.','Statistics','Beginner'
WHERE NOT EXISTS (SELECT 1 FROM courses WHERE title='Statistics and Probability');
INSERT INTO courses(title,provider,url,description,skill_name,difficulty)
SELECT 'Git and GitHub','GitHub Docs','https://docs.github.com/en/get-started','Learn version control and GitHub basics.','Git and GitHub','Beginner'
WHERE NOT EXISTS (SELECT 1 FROM courses WHERE title='Git and GitHub');
INSERT INTO courses(title,provider,url,description,skill_name,difficulty)
SELECT 'Machine Learning Crash Course','Google','https://developers.google.com/machine-learning/crash-course','Study machine learning fundamentals.','Machine Learning','Beginner'
WHERE NOT EXISTS (SELECT 1 FROM courses WHERE title='Machine Learning Crash Course');
