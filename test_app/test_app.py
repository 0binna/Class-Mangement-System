import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Student, Instructor, Course, Grade
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create dict with Authorization as key and Bearer token as values.
# Later used by test classes as Header

admin_auth_header = {
    "Authorization": os.getenv("ADMIN_TOKEN")
}
instructor_auth_header = {
    "Authorization": os.getenv("INSTRUCTOR_TOKEN")
}
student_auth_header = {
    "Authorization": os.getenv("STUDENT_TOKEN")
}


class CMStestCase(unittest.TestCase):
    # This class represents the CMS test case

    def setUp(self):
        # Define test variables and initialize app
        self.app = create_app()
        self.client = self.app.test_client
        # format database_path:
        # "postgresql://myusername:mypassword@localhost:5432/mydatabase"
        self.database_path = os.getenv("DATABASE_URL_TEST")
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        # Executed after reach test
        pass

    # ----------------------------------------------------------------------#
    # Tests GET/students
    # ----------------------------------------------------------------------#

    def test_200_get_students(self):
        # Test success of endpoint with authentication
        res = self.client().get("/students?page=1", headers=admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(isinstance(data["students"], list))

    def test_404_get_students(self):
        # Test failure of endpoint with authentication beyond valid page
        res = self.client().get("/students?page=1000", headers=admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_401_get_students(self):
        # Test RBAC (Admin role) without authentication
        res = self.client().get("/students?page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "authorization_header_missing")
        self.assertEqual(
            data["description"],
            "Authorization header is expected.")

    # ----------------------------------------------------------------------#
    # Tests GET/instructors
    # ----------------------------------------------------------------------#

    def test_200_get_instructors(self):
        # Test success of endpoint with authentication
        res = self.client().get("/instructors?page=1", headers=instructor_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(isinstance(data["instructors"], list))

    def test_404_get_instructors(self):
        # Test failure of endpoint with authentication beyond valid page
        res = self.client().get("/instructor?page=1000", headers=instructor_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_401_get_instructor(self):
        # Test RBAC (Instructor role) without authentication
        res = self.client().get("/instructors?page=1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "authorization_header_missing")
        self.assertEqual(
            data["description"],
            "Authorization header is expected.")

    # ----------------------------------------------------------------------#
    # Tests GET/students/<int:student_id>
    # ----------------------------------------------------------------------#

    def test_200_get_student_details(self):
        # Test success of endpoint with authentication
        res = self.client().get("/students/22001", headers=student_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["student_details"]["name"])
        self.assertTrue(isinstance(data["student_details"], dict))
        self.assertTrue(isinstance(data["student_details"]["grades"], list))

    def test_404_get_student_details(self):
        # Test failure of endpoint with authentication and unknow student ID
        res = self.client().get("/students/3000", headers=student_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_401_get_student_details(self):
        # Test RBAC (Student role) without authentication
        res = self.client().get("/students/22001")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["code"], "authorization_header_missing")
        self.assertEqual(
            data["description"],
            "Authorization header is expected.")

    # ----------------------------------------------------------------------#
    # Tests GET/instructors/<int:instructor_id>
    # ----------------------------------------------------------------------#

    def test_200_get_instructor_details(self):
        # Test success of endpoint with authentication
        res = self.client().get("/instructors/2203", headers=admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["instructor_details"]["name"])
        self.assertTrue(isinstance(data["instructor_details"], dict))
        self.assertTrue(
            isinstance(
                data["instructor_details"]["courses"],
                list))

    def test_404_get_instructor_details(self):
        # Test failure of endpoint with authentication and unknow instructor ID
        res = self.client().get("/instructor/3000", headers=admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # ----------------------------------------------------------------------#
    # Tests POST/students/search
    # ----------------------------------------------------------------------#

    def test_200_search_students(self):
        # Test success of endpoint with authentication
        searchTerm = {"search_term": "hicks"}
        res = self.client().post(
            "/students/search",
            json=searchTerm,
            headers=instructor_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(isinstance(data["students"], list))

    def test_400_search_students(self):
        # Test failure of endpoint with authentication and no input
        res = self.client().post("/students/search", headers=instructor_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    # ----------------------------------------------------------------------#
    # Tests POST/instructors/search
    # ----------------------------------------------------------------------#

    def test_200_search_instructors(self):
        # Test success of endpoint with authentication
        searchTerm = {"search_term": "harr"}
        res = self.client().post(
            "/instructors/search",
            json=searchTerm,
            headers=admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(isinstance(data["instructors"], list))

    def test_400_search_instructors(self):
        # Test failure of endpoint with authentication and no input
        res = self.client().post("/instructors/search", headers=admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    # ----------------------------------------------------------------------#
    # Tests POST/students/<int:student_id>/create
    # ----------------------------------------------------------------------#

    def test_200_add_student_course(self):
        # Test success of endpoint with authentication
        course = {"course": "mathematics"}
        res = self.client().post(
            "/students/22003/create",
            json=course,
            headers=student_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["course"])

    def test_404_add_student_course(self):
        # Test failure of endpoint with authentication and enrolling student in
        # unknown course
        course = {"course": "unknown"}
        res = self.client().post(
            "/students/22003/create",
            json=course,
            headers=student_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_422_add_student_course(self):
        # Test failure of endpoint with authentication and enrolling student in
        # course that student is already enrolled in.
        course = {"course": "mathematics"}
        res = self.client().post(
            "/students/22001/create",
            json=course,
            headers=student_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_403_search_students(self):
        # Test RBAC (Student role) without authorization
        course = {"course": "English"}
        res = self.client().post(
            "/students/22003/create",
            json=course,
            headers=instructor_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["code"], "unauthorized")
        self.assertEqual(data["description"], "Permission not found.")

    # ----------------------------------------------------------------------#
    # Tests PATCH/students/<int:student_id>/edit
    # ----------------------------------------------------------------------#

    def test_200_update_student_grade(self):
        # Test success of endpoint with authentication
        grade = {
            "course": "mathematics",
            "grade": 100
        }
        res = self.client().patch(
            "/students/22001/edit",
            json=grade,
            headers=instructor_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_422_update_student_grade(self):
        # Test failure of endpoint with authentication and unknown student ID
        grade = {
            "course": "mathematics",
            "grade": 100
        }
        res = self.client().patch(
            "/students/2200/edit",
            json=grade,
            headers=instructor_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_403_update_student_grade(self):
        # Test RBAC (Instructor role) without authorization
        grade = {
            "course": "mathematics",
            "grade": 100
        }
        res = self.client().patch(
            "/students/22001/edit",
            json=grade,
            headers=student_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["code"], "unauthorized")
        self.assertEqual(data["description"], "Permission not found.")

    # ----------------------------------------------------------------------#
    # Tests DELETE/students/<int:student_id>/student_course
    # ----------------------------------------------------------------------#

    def test_200_delete_student_course(self):
        # Test success of endpoint with authentication
        course = {"course": "physical education"}
        res = self.client().delete(
            "/students/22004/student_course",
            json=course,
            headers=student_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_422_delete_student_course(self):
        # Test failure of endpoint with authentication and delete unenrolled
        # course
        course = {"course": "mathematics"}
        res = self.client().delete(
            "/students/22004/student_course",
            json=course,
            headers=student_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_403_delete_student_course(self):
        # Test RBAC (Student role) without authorization
        course = {"course": "Social Studies"}
        res = self.client().delete(
            "/students/22005/student_course",
            json=course,
            headers=instructor_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["code"], "unauthorized")
        self.assertEqual(data["description"], "Permission not found.")

    # ----------------------------------------------------------------------#
    # Tests DELETE/students/<int:student_id>/student
    # ----------------------------------------------------------------------#

    def test_200_delete_student(self):
        # Test success of endpoint with authentication
        res = self.client().delete("/students/22005/student", headers=admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_422_delete_student(self):
        # Test failure of endpoint with authentication and delete student with
        # unknown ID
        res = self.client().delete("/students/220/student", headers=admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_403_delete_student(self):
        # Test RBAC (Admin role) without authorization
        res = self.client().delete(
            "/students/22002/student",
            headers=instructor_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["code"], "unauthorized")
        self.assertEqual(data["description"], "Permission not found.")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
