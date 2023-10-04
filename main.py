import json
from lxml import etree as ET
from data import data_

class Person:
    def __init__(self, first_name, last_name, email):
        if not isinstance(first_name, str) or not isinstance(last_name, str) or not isinstance(email, str):
            raise ValueError("Invalid data type for name or email")
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

class Student(Person):
    def __init__(self, first_name, last_name, email, student_id):
        super().__init__(first_name, last_name, email)
        self.student_id = student_id
        self.courses = []

class Teacher(Person):
    def __init__(self, first_name, last_name, email, teacher_id):
        super().__init__(first_name, last_name, email)
        self.teacher_id = teacher_id
        self.courses_taught = []

def save_to_json(filename, data):
    with open(filename, 'w') as json_file:
        json.dump(data_, json_file)

def load_from_json(filename):
    with open(filename, 'r') as json_file:
        loaded_data = json.load(json_file)
    return loaded_data

def save_to_xml(filename, data):
    root = ET.Element("university")
    students = ET.SubElement(root, "students")
    teachers = ET.SubElement(root, "teachers")

    for student in data_["students"]:
        student_element = ET.SubElement(students, "student")
        for key, value in student.items():
            if isinstance(value, list):  # Обработка списков
                courses = ET.SubElement(student_element, "courses")
                for course in value:
                    course_element = ET.SubElement(courses, "course")
                    course_element.text = course
            else:
                field = ET.SubElement(student_element, key)
                field.text = value

    for teacher in data_["teachers"]:
        teacher_element = ET.SubElement(teachers, "teacher")
        for key, value in teacher.items():
            if isinstance(value, list):  # Обработка списков
                courses_taught = ET.SubElement(teacher_element, "courses_taught")
                for course in value:
                    course_element = ET.SubElement(courses_taught, "course")
                    course_element.text = course
            else:
                field = ET.SubElement(teacher_element, key)
                field.text = value

    tree = ET.ElementTree(root)
    tree.write(filename, pretty_print=True, encoding="utf-8")


def load_from_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    data_ = {"students": [], "teachers": []}

    for student_element in root.find("students"):
        student_data = {}
        for field in student_element:
            student_data[field.tag] = field.text
        data_["students"].append(student_data)

    for teacher_element in root.find("teachers"):
        teacher_data = {}
        for field in teacher_element:
            teacher_data[field.tag] = field.text
        data_["teachers"].append(teacher_data)

    return data_


save_to_json("university.json", data_)

load_from_json("university.json")

save_to_xml("university.xml", data_)

load_from_xml("university.xml")
