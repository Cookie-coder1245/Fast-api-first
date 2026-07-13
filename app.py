from fastapi import FastAPI
import json

app=FastAPI()

def load_data():
    with open("data.json", "r") as file:
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