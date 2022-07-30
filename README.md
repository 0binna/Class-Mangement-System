# Class Management System (CMS) API

The Class Management System models a school portal that comprises data management and database storage for effectively managing a class. 

## Motivation for the Project

This is the Capstone project for the Full Stack Web Developer Nanodegree Program by Udacity. It provides an opportunity to combine the skills I’ve learned and developed in this course to construct a database-backed web API with user access control. Concepts from the following technical topics where applied to develope this API:

1. Database modeling with `postgres` & `sqlalchemy` (see `models.py`)
2. API to perform CRUD Operations on database with `Flask` (see `app.py`)
3. Automated testing with `Unittest` (see `test_app`)
4. Authorization & Role based Authentication with `Auth0` (see `auth.py`)
5. Deployment on `Heroku`

## Database Classes

The database comprises the Student, Instructor, Course and Grade classes which all extends the base SQLALchemy Model. The Grade class is a an association object; it establishes a many to many relationship between Course and Student class.

![Database schema diagram](https://i.imgur.com/WZGB1Ex.png)

## User Roles

There are 3 Roles with distinct permission sets:

1. Student:
   - Can see a list of the names of all instructors and email.
   - Can see any instructor profile.
   - Can search for any instructor; the search allows partial string matching and is case-insensitive.
   - Can add or remove course.
   - Can only see their profile.
2. Instructor:
   - Can perform the first three student roles.
   - Can see a list of the names and emails of all students.
   - Can search for any student; the search allows partial string matching and is case-insensitive.
   - Can see any student profile.
   - can edit their student's scores.
3. Admin:
   - Can perform all Instructor and Student roles.
   - Can delete student records. 

## Start Project locally

### Install Dependencies

1. **Python 3.8** - Follow instructions to install the latest version of python for your platform in the [python docs](https://www.python.org/downloads/)

2. **Virtual Environment** - Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PostgreSQL** - Make sure to have PostgreSQL installed, if it is not installed, follow instructions to download PostgreSQL in [PostgreSQL Downloads](https://www.postgresql.org/download/)

4. **PIP Dependencies** - Install the required dependencies by navigating to the project root directory and run:

```bash
pip install -r requirements.txt
```
### Set up the Database

With Postgres running, create a `cms_db` database:

```bash
createdb cms_db
```
Apply Database Schema using Flask-Migrate. Apply the database schema and relationships by executing:

```bash
python manage.py db init  # creates a migration repository
python manage.py db migrate -m "Initial migration."  # generate an initial migration
python manage.py db upgrade # apply the migration to the database
```

Populate the database using the `cms.psql` file. From the root folder in terminal run:

```bash
psql cms_db < cms.psql
```
To run the server, execute:

```bash
python app.py
```

## API Documentation

### Base URL

https://cms-project-obi.herokuapp.com

### Error Handling

HTTP errors are returned as JSON objects in the following format:
```bash
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```
Authentication errors are returned as JSON objects in the following format:
```bash
{
    'error': 401,
    'code': 'invalid_header',
    'description': 'Token not found.'
}
```

The API will return these error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 422: Not Processable

### Endpoints

#### GET '/students?page=${integer}'
- Fetches a paginated list of students.
- Request Arguments: `page` - integer (optional, 10 Students per page, defaults to 1).
- Returns: A success value and an object with paginated students details (id, name, email).
- Requires permission: `get:students`
   ```bash 
   curl https://cms-project-obi.herokuapp.com/students?page=1
   ```
   Sample response

   ```json
   {
      "students": [
         {
            "email": "consectetuer@student.com",
            "id": 22009,
            "name": "Britanni Hooper"
         },
         {
            "email": "vitae.aliquet@student.com",
            "id": 22006,
            "name": "Bryar Gonzales"
         },
         {
            "email": "aenean@student.com",
            "id": 22003,
            "name": "Cecilia Alford"
         },
         .
         .
         .
         .
         {
            "email": "lectus.quis@student.com",
            "id": 22100,
            "name": "Shay Padilla"
         }
      ],
      "success": true
   }
   ```

#### GET '/instructors?page=${integer}'

- Fetches a paginated list of instructors.
- Request Arguments: `page` - integer (optional, 10 instructors per page, defaults to 1).
- Returns: A success value and an object with paginated Instructors details (id, name, email).
- Requires permission: `get:instructors`
   ```bash 
   curl https://cms-project-obi.herokuapp.com/instructors?page=1
   ```
   Sample response

   ```json
   {
      "instructors": [
         {
            "email": "ut.nec.urna@instructor.com",
            "id": 2201,
            "name": "Beau Olson"
         },
         .
         .
         .
         {
            "email": "cras.vehicula@instructor.com",
            "id": 2203,
            "name": "Preston Horne"
         },
         {
            "email": "eros.non@instructor.com",
            "id": 2202,
            "name": "Susan Moreno"
         }
      ],
      "success": true
   }
   ```

#### GET '/students/${id}'

- Fetches a student's information specified by id request argument.
- Request Arguments: `id` - integer.
- Returns: A success value and an object with student information related to the given `id` (id, name, email, courses, scores, image_link).
- Requires permission: `get:student_profile`
   ```bash 
   curl https://cms-project-obi.herokuapp.com/students/22001
   ```
   Sample response

   ```json
   {
      "student_details": {
         "email": "nullam@student.com",
         "grades": [
            {
                  "course": "Mathematics",
                  "score": 85
            },
            {
                  "course": "Science",
                  "score": 100
            }
         ],
         "id": 22001,
         "image_link": "https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png",
         "name": "Lunea Hicks"
      },
      "success": true
   }
   ```

#### GET '/instructors/${id}'

- Fetches an instructor's information specified by id request argument.
- Request Arguments: `id` - integer.
- Returns: A success value and an object with instructor's information related to the given `id` (id, name, email, courses, image_link).
- Requires permission: `get:instructor_profile`
   ```bash 
   curl https://cms-project-obi.herokuapp.com/instructors/2203
   ```
   Sample response

   ```json
   {
      "instructor_details": {
         "courses": [
               {
                  "course": "Science"
               }
         ],
         "email": "cras.vehicula@instructor.com",
         "id": 2203,
         "image_link": "https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png",
         "name": "Preston Horne"
      },
      "success": true
   }
   ```

#### POST '/students'

- Sends a post request in order to return any student for whom the search term is a substring of the student's name (Search is case insensitive).
- Request Arguments: A json body containing, `search_term` - string
- Returns: A success value and an array of students.
- Requires permission: `post:student_search`
   ```bash
   curl -X POST -H "Content-Type: application/json" -d'{"search_term":"br"}' https://cms-project-obi.herokuapp.com/students
   ```
   Sample response

   ```json
   {
      "students": [
         {
            "email": "consectetuer@student.com",
            "id": 22009,
            "name": "Britanni Hooper"
         },
         {
            "email": "vitae.aliquet@student.com",
            "id": 22006,
            "name": "Bryar Gonzales"
         }
      ],
      "success": true
   }
   ```

#### POST '/instructors'

- Sends a post request in order to return any instructor for whom the search term is a substring of the instructor's name (Search is case insensitive).
- Request Arguments: A json body containing, `search_term` - string
- Returns: A success value and an array of instructors.
- Requires permission: `post:instructor_search`
   ```bash
   curl -X POST -H "Content-Type: application/json" -d'{"search_term":"son"}' https://cms-project-obi.herokuapp.com/instructors
   ```
   Sample response

   ```json
   {
    "instructors": [
        {
            "email": "ut.nec.urna@instructor.com",
            "id": 2201,
            "name": "Beau Olson"
        }
    ],
    "success": true
   }
   ```

#### POST '/students/${id}/course'

- Sends a post request to add a course to a student specified by the student id request argument.
- Request Arguments: A json body containing, `id` - integer, `course` - string.
- Returns: Returns a success value and the title of the course added.
- Requires permission: `post:student_create`
   ```bash
   curl -X POST -H "Content-Type: application/json" -d'{"course":"mathematics"}' https://cms-project-obi.herokuapp.com/students/22004/course
   ```
   Sample response
   
   ```json
   {
    "course": "mathematics",
    "success": true
   }
   ```

#### PATCH '/students/${id}/score'

- Sends a patch request to update a student score (Student is specified by student id request argument).
- Request Arguments: A json body containing, `id` - integer, `course` - string, `score` - integer.
- Returns: Returns a success value.
- Requires permission: `patch:student_edit`
   ```bash
   curl -X PATCH -H "Content-Type: application/json" -d'{"course":"mathematics", "score":100}' https://cms-project-obi.herokuapp.com/students/22001/score
   ```
   Sample response
   
   ```json
   {
    "success": true
   }
   ```

#### DELETE '/students/${id}/course'

- Deletes a specified course for a specific student (Student is specified by student id request argument).
- Request Arguments: A json body containing, `id` - integer, `course` - string.
- Returns: Returns a success value and the title of the course deleted.
- Requires permission: `delete:student_course`
  ```bash
   curl -X DELETE -H "Content-Type: application/json" -d'{"course":"science"}' https://cms-project-obi.herokuapp.com/students/22003/course
   ```
   Sample response
   
   ```json
   {
    "student_course": "Science",
    "success": true
   }
   ```

#### DELETE '/students/${id}'

- Deletes a specified student using the student id request argument.
- Request Arguments: `id` - integer.
- Returns: A success value and the name of the deleted student.
- Requires permission: `delete:student_id`
   ```bash 
   curl -X DELETE https://cms-project-obi.herokuapp.com/students/22004
   ```
   Sample response

   ```json
   {
    "student_name": "Paul Freeman",
    "success": true
   }
   ```

## Authentication

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC (Role Based Access Control)
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:students`
   - `get:instructors`
   - `get:student_profile`
   - `get:instructor_profile`
   - `post:student_search`
   - `post:instructor_search`
   - `post:student_create`
   - `patch:student_edit`
   - `delete:student_course`
   - `delete:student_id`
6. Create new roles for:
   - Student
     - can `get:instructors`
     - can `get:instructor_profile`
     - can `post:instructor_search`
     - can `post:student_create`
     - can `get:student_profile`
   - Instructor
     - can perform the first three student roles.
     - can `get:students`
     - can `post:student_search`
     - can `patch:student_edit`
   - Admin
     - can perform all Instructor and Student roles.
     - can `delete:student_id`

In your API Calls, add them as Header, with Authorization as key and the Bearer token as value. Prepend Bearer to the token (see `.env` for header sample).

## Test App Locally (CRUD & RBAC)

Project includes tests to ensure RBAC permissions for CRUD operations are successful and persist accurately in the database for GET, POST, PATCH and DELETE HTTP requests.

Ensure `DATABASE_URL` in `.env` is set to local database path.

To deploy the tests, run
```bash
dropdb cms_db && createdb cms_db # Reset database
python manage.py db migrate 
python manage.py db upgrade
psql cms_db < cms.psql
python test_app.py
```

## Deploy to Heroku

This documentation assumes that the user already:
- Has a heroku account. The free account option would suffice for this project
- Has downloaded and installed the heroku command line interface locally, and
- Is able to login to heroku from the command line

### Login to Heroku

Use the heroku login command to login to heroku via the command line:
```bash
heroku login -i
```
### Procfile and runtime.txt files
Before pushing the project to heroku, ensure that a `runtime.txt` file and a `Procfile` are present in the project's root directory.

The procfile mention using gunicorn (production-ready WSGI server) to run the application:
```bash
web: gunicorn app:app
```

The runtime.txt file specifies the exact runtime environment:
```bash
python-3.8.13
```
### Create the project in Heroku cloud
While still logged in to heroku, create an app in heroku cloud. Ensure that your app has a unique name.
```bash
heroku create cms-project-obi --buildpack heroku/python
```
### Git repository on Heroku
Ensure that a Git remote repository was created on Heroku by the `heroku create` command.
```bash
git remote -v
```
If you cannot see the Heroku `remote` repository URL in the output, you can use the command:
```bash
git remote add heroku [heroku_remote_git_url]
```
### Add a postgreSQL addon for the database
Heroku has an addon for apps for a postgresql database instance. Run the following line of code in order to create the database and connect it to the application:
```bash
heroku addons:create heroku-postgresql:hobby-dev --app cms-project-obi
```
### Configure the application
In order to set up the environment variables in the Heroku cloud specific to the application, run the following command to fix the DATABASE_URL configuration variable:
```bash
heroku config --app cms-project-obi
```
### Update .env file
Copy the DATABASE_URL generated from the step above, and update your local `DATABASE_URL` environment variable in `.env` file.

### Push to Heroku
Commit the changes made to the above files, and then push the project to Heroku.
```bash
git push heroku master
```
### Migrate the database
To migrate your local database to heroku, run:
```bash
heroku run python manage.py db upgrade --app cms-project-obi
```
### Populate postgres database heroku 
Establish a psql session with the remote database:
```bash
heroku pg:psql
```
Populate the database using the `cms.psql` file:
```bash
\i cms.psql
```
### Confirm a successful build
If there were no errors from the above steps, Open the application from your Heroku Dashboard and see it work live!