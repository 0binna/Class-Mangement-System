import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Student, Instructor, Course, Grade
from auth import AuthError, requires_auth


data_per_page = 10


def paginate_data(request, selection):
    # Paginates and formats database queries
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * data_per_page
    end = start + data_per_page

    data = [data.short() for data in selection]
    current_data = data[start:end]

    return current_data


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Basic initialization of CORS
    CORS(app)

    @app.after_request
    # After_request decorator to set Access-Control-Allow
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE"
        )
        return response

    # ----------------------------------------------------------------------#
    # Students
    # ----------------------------------------------------------------------#

    @app.route("/students")
    @requires_auth("get:students")
    # Handles GET requests for all student records including pagination (every
    # 10 students)
    def retrieve_students(payload):
        selection = Student.query.order_by(Student.name).all()
        student_details = paginate_data(request, selection)

        if len(student_details) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "student_details": student_details
            }
        )

    @app.route("/students/<int:student_id>")
    @requires_auth("get:student_profile")
    # Handles GET requests for students using a student ID.
    def retrieve_student_details(payload, student_id):
        try:
            student = Student.query.get(student_id)

            course_score = []
            for grade in student.grades:
                course_score.append(
                    {
                        "course": grade.course.title,
                        "score": grade.score
                    }
                )

            student_details = student.long()
            student_details.update({"grades": course_score})

            return jsonify(
                {
                    "success": True,
                    "student_details": student_details
                }
            )

        except BaseException:
            abort(422)

    @app.route("/students/<int:student_id>/create", methods=['POST'])
    @requires_auth("post:student_create")
    # Handles POST requests to create a new course for a student
    def add_student_course(payload, student_id):

        body = request.get_json()

        course_input = body.get("course", None)
        course = Course.query.filter(
            Course.title.ilike(course_input)).one_or_none()
        if course is None:
            abort(404)

        try:
            add_course = Grade(
                student_id=student_id,
                course_id=course.id)
            add_course.insert()

            return jsonify(
                {
                    "success": True
                }
            )

        except BaseException:
            abort(422)

    @app.route('/students/search', methods=['POST'])
    @requires_auth("post:student_search")
    # Handles POST requests to get student records based on search term.
    # Search allows partial string matching and case-insensitive.
    def search_students(payload):
        try:
            body = request.get_json()

            search_term = body.get("search_term", None)
            formatted_input = '%{0}%'.format(search_term)
            selection = Student.query.filter(
                Student.name.ilike(formatted_input)).all()
            student_details = [student.short() for student in selection]

            return jsonify(
                {
                    "success": True,
                    "student_details": student_details
                }
            )

        except BaseException:
            abort(400)

    @app.route("/students/<int:student_id>/edit", methods=['PATCH'])
    @requires_auth("patch:student_edit")
    # Handles PATCH requests to update students score.
    def update_student_grade(payload, student_id):
        try:
            body = request.get_json()

            grade_input = body.get("grade", None)
            course_input = body.get("course", None)
            course = Course.query.filter(
                Course.title.ilike(course_input)).one()
            grade = Grade.query.filter(
                Grade.course_id == course.id,
                Grade.student_id == student_id).one()
            grade.score = grade_input
            grade.update()

            return jsonify(
                {
                    "success": True
                }
            )

        except BaseException:
            abort(422)

    @app.route("/students/<int:student_id>/student", methods=["DELETE"])
    @requires_auth("delete:student_id")
    # Handles DELETE requests to delete student record.
    def delete_student(payload, student_id):
        try:
            student = Student.query.filter(
                Student.id == student_id).one_or_none()
            student_name = student.name
            student.delete()

            return jsonify(
                {
                    "student_name": student_name,
                    "success": True
                }
            )

        except BaseException:
            abort(422)

    @app.route("/students/<int:student_id>/student_course", methods=["DELETE"])
    @requires_auth("delete:student_course")
    # Handles DELETE requests to unenroll student from course.
    def delete_student_course(payload, student_id):
        try:
            body = request.get_json()

            course_input = body.get("course", None)
            course = Course.query.filter(
                Course.title.ilike(course_input)).one()
            grade = Grade.query.filter(
                Grade.course_id == course.id,
                Grade.student_id == student_id).one()
            student_course = course.title
            grade.delete()

            return jsonify(
                {
                    "student_course": student_course,
                    "success": True
                }
            )

        except BaseException:
            abort(422)

    # ----------------------------------------------------------------------#
    # Instructors
    # ----------------------------------------------------------------------#

    @app.route("/instructors")
    @requires_auth("get:instructors")
    # Handles GET requests for all instructor records including pagination
    # (every 10 instructors)
    def retrieve_instructors(payload):
        selection = Instructor.query.order_by(Instructor.name).all()
        Instructor_details = paginate_data(request, selection)

        if len(Instructor_details) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "student_details": Instructor_details
            }
        )

    @app.route("/instructors/<int:instructor_id>")
    @requires_auth("get:instructor_profile")
    # Handles GET requests for instructors using an instructor ID.
    def retrieve_instructor_details(payload, instructor_id):
        try:
            instructor = Instructor.query.get(instructor_id)

            instructor_course = []
            for course in instructor.courses:
                instructor_course.append(
                    {
                        "course": course.title
                    }
                )

            instructor_details = instructor.long()
            instructor_details.update({"courses": instructor_course})

            return jsonify(
                {
                    "success": True,
                    "instructor_details": instructor_details
                }
            )

        except BaseException:
            abort(422)

    @app.route('/instructors/search', methods=['POST'])
    @requires_auth("post:instructor_search")
    # Handles POST requests to get instructor records based on search term.
    # Search allows partial string matching and case-insensitive.
    def search_instructors(payload):
        try:
            body = request.get_json()

            search_term = body.get("search_term", None)
            formatted_input = '%{0}%'.format(search_term)
            selection = Instructor.query.filter(
                Instructor.name.ilike(formatted_input)).all()
            instructor_details = [instructor.short()
                                  for instructor in selection]

            return jsonify(
                {
                    "success": True,
                    "student_details": instructor_details
                }
            )

        except BaseException:
            abort(400)

    # ----------------------------------------------------------------------#
    # Error handlers for all expected HTTP error
    # ----------------------------------------------------------------------#

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    # Error handlers for all expected Auth error

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        return response, ex.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
