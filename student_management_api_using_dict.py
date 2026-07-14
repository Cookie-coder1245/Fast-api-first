#Student management system using python dictionary as a storage

from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import Optional

app=FastAPI()

students = {
    "1": {
        "name": "Ali",
        "age": 20,
        "city": "Lahore"
    },
    "2": {
        "name": "Ahmed",
        "age": 22,
        "city": "Karachi"
    },
    "3":{
        "name":"ALi",
        "age":22,
        "city":"Lahore"
    }
}

class Student(BaseModel):
    id:str 
    name:str
    age:int
    city:str

class StudentUpdate(BaseModel):
  
    name:Optional[str]=None
    age:Optional[int]=None
    city:Optional[str]=None


#CREATE operation
@app.post('/add')
def create_student(student:Student):
    if student.id  in students:
        raise HTTPException(status_code=400,detail="Student already found")
    
    students[student.id]=student.model_dump(exclude=['id'])
    return {
        "message": "Student added successfully",
        "student": students[student.id]
    }


#READ OPERATION 
@app.get('/student')
def get_student():
    return students

@app.get('/student/{student_id}')
def retrieve(student_id:str):
    if student_id not in students:
        raise HTTPException(status_code=404,detail="Student deosnt exitst")
    return students[student_id]


#update students
@app.patch('/update/{student_id}')
def update_student(student_id:str,student:StudentUpdate):
    if student_id not in students:
        raise HTTPException(status_code=404,detail="Student deosnt exitst")
    
    if student.name is not None:
        students[student_id]['name']=student.name

    if student.age is not None:
        students[student_id]['age']=student.age

    if student.city is not None:
        students[student_id]['city']=student.city

    return {
        "message": "Student updated successfully",
        "student": students[student_id]
    }

@app.put('/put/{student_id}')
def put_student(student_id:str,student:Student):
    if student_id not in students:
        raise HTTPException(status_code=400,detail="Student deosnt exitst")
    
    students[student_id]={
        "name":student.name,
        "age":student.age,
        "city":student.city

    }
    return {
        "message": "Student updated successfully",
        "student": students[student_id]
    }

    


#DELETE OPERATION 
@app.delete('/delete/{student_id}')
def delete_student(student_id:str):
    if student_id not in students:
        raise HTTPException(status_code=400,detail="Student deosnt exitst")
    
    deleted_student = students.pop(student_id)

    return {
        "message": "Student deleted successfully",
        "student": deleted_student
    }

    
    

    
   