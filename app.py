from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,computed_field
from typing import Annotated,Field,Literal
import json

app=FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description="Id of the patient",example=['1'])]
    name:Annotated[str,Field(...,description="Name of the patient")]
    city:Annotated[str,Field(...,description="City of the patient")]
    age:Annotated[int,Field(...,gt=0,lt=0,description="City of the patient")]
    gender:Annotated[Literal['male','female','other'],Field(...,description="age of the gender")]
    height:Annotated[float,Field(...,gt=0,description="Height of the patient in meters")]
    weight:Annotated[float,Field(...,gt=0,description="Weight of the patient in meters")]

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi


def load_data():
    with open("patient.json", "r") as file:
        data = json.load(file)
    return data
def save_data(data):
    with open('patient.json','w') as f:
        json.dump(data,f)

@app.get("/")
def hello():
    return {"message": "PATIENT management system api!"}

@app.get("/about")
def about():
    return {"message": "This is a patient management system API built with FastAPI."}

@app.get("/view")
def view():
    data = load_data()
    return data



@app.get('/view/{patient_id}')
def view_patient(patient_id:int=Path(...,description="ID of the patient",example="1")):
    data=load_data()
    for patient in data:
     if patient_id ==patient["id"]:
        return patient
    return HTTPException(status_code=404,detail="Patient not found")


@app.get('/sort')
def sort_patient(sort_by:str=Query(...,description="sort on the basis of height,weight and bmi"),
                 order=Query('asc',description="sort in asc and desc")):
    
    valid_fields=['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail='invalid field select from valid {valid_fields}')
    
    if order not in ['asc','desc']:
        raise  HTTPException(status_code=400,detail="Invalid field select from asc and desc")

    data=load_data()
    sort_order=True if order=="desc" else False
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)

    return sorted_data


@app.post('/create')
def create_patient(patient:Patient):

    #load existing data
    data=load_data()

    #check if the pateint already exist
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient already exists")

    #new patient add to the database
    data[patient.id]=patient.model_dump(exclude=['id'])
    save_data(data)
    
    return JSONResponse(status_code=201,content={'message':'patient created successfully'})
    

