from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

course_instructors = db.Table(
    'course_instructors',
    db.Column("course_id", db.Integer, db.ForeignKey("courses.id", primary_key=True)),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id", primary_key=True))
)

course_students = db.Table(
    'course_students',
    db.Column("course_id", db.Integer, db.ForeignKey("courses.id", primary_key=True)),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id", primary_key=True))
)

# your classes here
class Course(db.Model):
    """
    Course Model
    """
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    assignments = db.relationship('Assignment', backref='course')
    instructors = db.relationship('User', secondary='course_instructors', back_populates='teaching_courses'  )
    students = db.relationship('User', secondary='course_students', back_populates='enrolled_courses')

    def __init__(self, **kwargs):
        """
        Initializes Course Object
        """
        self.code = kwargs.get("code", "")
        self.name = kwargs.get("name", "")

    def serialize(self):
        """
        Serialize course object
        """
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "assignments": [a.serialize() for a in self.assignments],
            "instructors": [i.simple_serialize() for i in self.instructors],
            "students": [s.simple_serialize() for s in self.students]
        }
    
    def simple_serialize(self):
        return {

             "id": self.id,
            "code": self.code,
            "name": self.name

        }


class Assignment(db.Model):
    """
    Assignment Model
    """
    __tablename__ = "assignments"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize Assignmnet object
        """
        self.title = kwargs.get("title", "")
        self.due_date = kwargs.get("due_date", 0)
        self.course_id = kwargs.get("course_id")

    def serialize(self):
        """
        Serializes assignment object
        """

        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date,
            "course": self.course_id
        }
    
class User(db.Model):
    """
    User Model
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    teaching_courses = db.relationship('Course', secondary='course_instructors', back_populates='instructors')
    enrolled_courses = db.relationship('Course', secondary='course_students', back_populates='students')

    def __init__(self, **kwargs):
        """
        Initializes User Object
        """
        self.name = kwargs.get("name", "")
        self.netid = kwargs.get("netid", "")

    def serialize(self):
        """
        Serialize User Object
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "courses": [c.simple_serialize() for c in self.teaching_courses + self.enrolled_courses]
        }
    
    def simple_serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid 
        } 