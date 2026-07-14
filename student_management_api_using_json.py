from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import Optional
import json

app=FastAPI()

class Student(BaseModel):
    id:str
    name:str
    age:int
    city:str

class StudentUpdate(BaseModel):
    name:Optional[str]
    age:Optional[int]
    city:Optional[str]

#Helper function
def load_data():
    with open("student.json",'r') as f:
        data=json.load(f)
        return data
    
def save_data(data):
    with open("student.json",'w') as f:
       json.dump(data,f,indent=4)

#Create student
@app.post('/student')
def create_student(student:Student):
    data=load_data()

    if student.id in data:
        raise HTTPException(status_code=400,detail="Student already existed")
    
    data[student.id]=student.model_dump(exclude="id")
    save_data(data)
    return {'message':"Student added successfully ",
            }

#Read student
@app.get('/students')
def get_students():
    data=load_data()
    return data
   
@app.get('/students/{student_id}')
def get_student(student_id:str):
    data=load_data()

    if student_id not in data:
        raise HTTPException(status_code=404,detail="Student not found")
    
    return data[student_id]

#Update student
@app.patch('/students/{student_id}')
def update_students(student_id:str,student:StudentUpdate):
    data=load_data()

    if student_id not in data:
        raise HTTPException(status_code=404,detail="Student Not found")

    if student.name is not None:
        data[student_id]['name']=student.name

    if student.age is not None:
        data[student_id]['age']=student.age

    if student.city is not None:
        data[student_id]['city']=student.city

    save_data(data)
    return {"Message":"Student info updated successfully "}
    
  
@app.put('/students/{student_id}')
def updates_students(student_id:str,student:Student):
    data=load_data()
    
    if student_id not in data:
        raise HTTPException(status_code=404,detail="Student Not found")
    
    data[student_id] = student.model_dump(exclude={"id"})
    save_data(data)
    return {"Message":"Student info updated successfully "}

@app.delete('/students/{student_id}')
def delete_students(student_id:str):
    data=load_data()
    
    if student_id not in data:
        raise HTTPException(status_code=404,detail="Student not found")
    
    del data[student_id]

    save_data(data)
    
    return {"Message":"Student info Deleted successfully "}

@app.delete('/students')
def delete_students_all():
    data={}
    save_data(data)
    
    return {"Message":"Student info Deleted successfully "}

#search by city
@app.get('/students/filter')
def search(city:str="Lahore"):
    results={}
    data=load_data()
    
    for key,val in data.items():
        if val['city']==city:
            results[key]=val
     
    if not results:
     raise HTTPException(
        status_code=404,
        detail="No students found in this city"
    )
    return results

#Search by age 
@app.get('/students/search')
def search(age:int):
    results={}
    data=load_data()
    
    for key,val in data.items():
        if val['age']>age:
            results[key]=val
     
    if not results:
     raise HTTPException(
        status_code=404,
        detail="No students found greater then this age"
    )
    return results


@app.get('/students/count')
def search():
    
    data=load_data()
    return {'student_count':len(data)}
    
    
    
    


    

    


   

   


