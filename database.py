import sqlite3

def create_database():
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL,
            email TEXT,
            course TEXT,
            attendance REAL,
            marks REAL
        )
    """)

    connection.commit()
    connection.close()


def add_student(name, roll_no, email, course, attendance, marks):
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students
        (name, roll_no, email, course, attendance, marks)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, roll_no, email, course, attendance, marks))

    connection.commit()
    connection.close()


def get_students():
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    connection.close()
    return students


def delete_student(student_id):
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    connection.commit()
    connection.close()


def update_student(student_id, name, roll_no, email, course, attendance, marks):
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE students
        SET name = ?, roll_no = ?, email = ?,
            course = ?, attendance = ?, marks = ?
        WHERE id = ?
    """, (name, roll_no, email, course, attendance, marks, student_id))

    connection.commit()
    connection.close()
def get_statistics():
    connection = sqlite3.connect("students.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(marks) FROM students")
    average_marks = cursor.fetchone()[0] or 0

    cursor.execute("SELECT AVG(attendance) FROM students")
    average_attendance = cursor.fetchone()[0] or 0

    cursor.execute(
        "SELECT COUNT(*) FROM students WHERE attendance < 75"
    )
    low_attendance = cursor.fetchone()[0]

    connection.close()

    return (
        total_students,
        round(average_marks, 2),
        round(average_attendance, 2),
        low_attendance
    )