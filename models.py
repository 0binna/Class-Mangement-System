import email
import os
from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from flask_sqlalchemy import SQLAlchemy
import json

DATABASE_URL = "postgresql://postgres@localhost:5432/cms_db"
database_path = DATABASE_URL  # os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


# creates student table
class Student(db.Model):
    __tablename__ = 'student'
    __table_args__ = (UniqueConstraint('name'),)

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    image_link = Column(String)
    # creates a one to many relationship with the table Grade(child).
    # If a record in the parent table is deleted, the corresponding records in
    # the child table will automatically be deleted.
    grades = relationship(
        'Grade',
        backref='student',
        lazy='joined',
        cascade="all, delete")

    def __init__(self, name, email, image_link):
        self.name = name
        self.email = email
        self.image_link = image_link

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }

    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'image_link': self.image_link
        }


# creates Instructor table
class Instructor(db.Model):
    __tablename__ = 'instructor'
    __table_args__ = (UniqueConstraint('name'),)

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    image_link = Column(String)
    # creates a one to many relationship with the table Course(child)
    courses = relationship('Course', backref='instructor', lazy='joined')

    def __init__(self, name, email, image_link):
        self.name = name
        self.email = email
        self.image_link = image_link

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }

    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'image_link': self.image_link
        }


# creates Course table
class Course(db.Model):
    __tablename__ = 'course'
    __table_args__ = (
        UniqueConstraint('title'),)

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    credit = Column(String, nullable=False)
    instructor_id = Column(Integer, ForeignKey('instructor.id'), nullable=True)
    # creates a one to many relationship with the table Grade(child).
    # If a record in the parent table is deleted, the corresponding records in
    # the child table will automatically be deleted.
    grades = relationship(
        'Grade',
        backref='course',
        lazy='joined',
        cascade="all, delete")

    def __init__(self, title, credit, instructor_id=None):
        self.title = title
        self.credit = credit
        self.instructor_id = instructor_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'credit': self.credit,
            'instructor_id': self.instructor_id
        }


# creates Grade table
class Grade(db.Model):
    __tablename__ = 'grade'
    __table_args__ = (
        UniqueConstraint('course_id', 'student_id'),)

    id = Column(Integer, primary_key=True)
    score = Column(Integer)
    course_id = Column(Integer, ForeignKey('course.id'))
    student_id = Column(Integer, ForeignKey('student.id'))

    def __init__(self, score=None, course_id=None, student_id=None):
        self.score = score
        self.course_id = course_id
        self.student_id = student_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'score': self.score,
            'course_id': self.course_id,
            'student_id': self.student_id
        }
