from fastapi import FastAPI,Path,HTTPException,Query
import json

app=FastAPI()

def load_data():
    with open("patient.json", "r") as file:
        data = json.load(file)
    return data

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
