from flask import Flask, escape, request
from marshmallow import Schema, fields, pprint #, ValidationError

app = Flask(__name__)

stu_db = {
    "id":[], 
    "name":[]
}

class_db = {
    "id":[],
    "name":[],
    "students": []
}

stu_id = 1000000
class_id = 8000


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'
# http://localhost:5000/?name=Foo the un-RESTful way



####################################################
###################students#########################
####################################################
@app.route('/students', methods=['POST'])
def create_student():
    req = request.json
    stu_name = req["name"]
    global stu_id #must be here?
    stu_id = stu_id + 1
    stu_db['id'].append(stu_id)
    stu_db['name'].append(stu_name)
    print(stu_db)
    return{"id": str(stu_id), "name": stu_name}, 201

@app.route('/students/<id>', methods=['GET'])
def get_student(id):
    my_stu_id = id
    index = stu_db['id'].index(int(my_stu_id))
    my_stu_name = stu_db['name'][index]
    return {"id": my_stu_id, "name": my_stu_name}



####################################################
###################classes##########################
####################################################
@app.route('/classes', methods=['POST'])
def create_class():
    req = request.json
    class_name = req["name"]
    global class_id
    class_id += 1
    class_student = []
    class_db['id'].append(class_id)
    class_db['name'].append(class_name)
    class_db['students'].append(class_student)
    print(class_db)
    return{"id": str(class_id), "name": class_name, "students": class_student}

@app.route('/classes/<id>', methods=['GET'])
def get_class(id):
    my_class_id = id
    class_index = class_db['id'].index(int(my_class_id))
    my_class_name = class_db['name'][class_index]
    my_class_student = class_db['students'][class_index]
    return {"id": my_class_id, "name": my_class_name, "students": my_class_student}

@app.route('/classes/<id>', methods=['PATCH'])
def add_student(id):
    #look up in stu_db
    req = request.json
    my_stu_id = req['student_id']
    index = stu_db['id'].index(int(my_stu_id))
    my_stu_name = stu_db['name'][index]
    new_class_student = {"id": my_stu_id, "name": my_stu_name}
    print(new_class_student)
    #add new students to class_db
    my_class_id = id
    class_index = class_db['id'].index(int(my_class_id))
    my_class_name = class_db['name'][class_index]
    class_db['students'][class_index].append(new_class_student)
    my_class_student = class_db['students'][class_index]
    
    return {"id": my_class_id, "name": my_class_name, "students": my_class_student}