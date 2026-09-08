from flask import Flask, render_template, request, redirect, session
from database import (
    create_database,
    add_student,
    get_students,
    delete_student,
    update_student,
    get_statistics
)

app = Flask(__name__)

app.secret_key = "student_management_secret"

create_database()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["logged_in"] = True
            return redirect("/")

        return "Invalid Username or Password"

    return render_template("login.html")


@app.route("/")
def home():
    if not session.get("logged_in"):
        return redirect("/login")

    students = get_students()

    total_students, average_marks, average_attendance, low_attendance = get_statistics()

    return render_template(
        "index.html",
        students=students,
        total_students=total_students,
        average_marks=average_marks,
        average_attendance=average_attendance,
        low_attendance=low_attendance
    )


@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    roll_no = request.form["roll_no"]
    email = request.form["email"]
    course = request.form["course"]
    attendance = request.form["attendance"]
    marks = request.form["marks"]

    add_student(
        name,
        roll_no,
        email,
        course,
        attendance,
        marks
    )

    return redirect("/")


@app.route("/delete/<int:student_id>")
def delete(student_id):
    delete_student(student_id)
    return redirect("/")


@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit(student_id):

    if request.method == "POST":

        name = request.form["name"]
        roll_no = request.form["roll_no"]
        email = request.form["email"]
        course = request.form["course"]
        attendance = request.form["attendance"]
        marks = request.form["marks"]

        update_student(
            student_id,
            name,
            roll_no,
            email,
            course,
            attendance,
            marks
        )

        return redirect("/")

    students = get_students()

    student = next(
        (s for s in students if s[0] == student_id),
        None
    )

    return render_template(
        "edit.html",
        student=student
    )


@app.route("/search")
def search():

    query = request.args.get("q", "").lower()

    students = get_students()

    results = [
        student for student in students
        if query in str(student[1]).lower()
        or query in str(student[2]).lower()
    ]

    return render_template(
        "index.html",
        students=results,
        total_students=len(results),
        average_marks=0,
        average_attendance=0,
        low_attendance=0
    )


@app.route("/logout")
def logout():

    session.pop("logged_in", None)

    return redirect("/login")


@app.route("/id-card/<int:student_id>")
def id_card(student_id):

    students = get_students()

    student = next(
        (s for s in students if s[0] == student_id),
        None
    )

    if student is None:
        return "Student not found"

    return render_template(
        "id_card.html",
        student=student
    )


@app.route("/student/<int:student_id>")
def student_details(student_id):

    students = get_students()

    student = next(
        (s for s in students if s[0] == student_id),
        None
    )

    if student is None:
        return "Student not found"

    return render_template(
        "student_details.html",
        student=student
    )


if __name__ == "__main__":
    app.run(debug=True)