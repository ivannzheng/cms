from db import db
from flask import Flask,request
import json 
from db import Course, Assignment, User

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(message, code=404):
    return json.dumps({"error": message}), code


# your routes here
@app.route("/api/courses/")
def get_all_courses():
    """
    Endpoint for getting all courses
    """
    return success_response({"courses": [c.serialize() for c in Course.query.all()]})

@app.route("/api/courses/", methods=["POST"])
def create_course():
    """
    Endpoint for creating course
    """
    body = json.loads(request.data)

    if not body.get("code") or not body.get("name"):
        return failure_response("Missing class name or code", 400)
    
    new_course = Course(
        code = body.get("code"),
        name = body.get("name")
    )
    db.session.add(new_course)
    db.session.commit() 
    return success_response(new_course.serialize(), 201)

@app.route("/api/courses/<int:course_id>/")
def get_specific_course(course_id):
    """
    Enpoint for getting a specific course
    """
    course = Course.query.filter_by(id=course_id).first() 
    if course is None:
        return failure_response("Course not found")
    return success_response(course.serialize())

@app.route("/api/courses/<int:course_id>/", methods=["DELETE"])
def delete_specific_course(course_id):
    """
    Endpoint for deleting a specific course
    """
    course = Course.query.filter_by(id=course_id).first() 
    if course is None:
        return failure_response("Course not found")
    db.session.delete(course)
    db.session.commit() 
    return success_response(course.serialize())

@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Endpoint for creating user
    """
    body = json.loads(request.data)

    if not body.get("name") or not body.get("netid"):
        return failure_response("Missing user name or netid", 400)
    
    new_user = User(
        name = body.get("name"),
        netid = body.get("netid")
    )

    db.session.add(new_user)
    db.session.commit() 
    return success_response(new_user.serialize(), 201)

@app.route("/api/users/<int:user_id>/")
def get_specific_user(user_id):
    """
    Endpoint for getting a specific user
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    return success_response(user.serialize())

@app.route("/api/courses/<int:course_id>/add/", methods=["POST"])
def add_user_to_course(course_id):
    """
    Endpoint for adding user to course 
    """
    course = Course.query.filter_by(id=course_id).first() 
    if course is None:
        return failure_response("Course not found")
    
    body = json.loads(request.data)
    user_id = body.get("user_id")
    user_type = body.get("type")

    if not user_id or not user_type:
        return failure_response("Missing userid or field", 400)
    
    user = User.query.filter_by(id=user_id).first()
    
    if user is None:
        return failure_response("User not found")
    
    if user_type == "student":
        if user not in course.students:
            course.students.append(user)
        else:
            return failure_response("User is already a studen in this course", 400)
    elif user_type == "instructor":
        if user not in course.instructors:
            course.instructors.append(user)
        else:
            return failure_response("User is already a instructor in this course", 400)
        
    db.session.commit()
    return success_response(course.serialize())

@app.route("/api/courses/<int:course_id>/assignment/", methods=["POST"])
def add_assignment(course_id):
    """
    Endpoint for adding assignment to course
    """
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        return failure_response("Course not found")
    
    body = json.loads(request.data)
    title = body.get("title")
    due_date = body.get("due_date")

    if not title or not due_date:
        return failure_response("Missing title or due date field", 400)
    
    new_assignment = Assignment(
        title = title,
        due_date = due_date,
        course_id = course_id
    )
    
    db.session.add(new_assignment)
    db.session.commit()
    return success_response(new_assignment.serialize(), 201)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True) 
