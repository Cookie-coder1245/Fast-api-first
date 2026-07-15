from fastapi import FastAPI
from fastapi.responses import  JSONResponse,HTMLResponse,RedirectResponse,FileResponse
from pydantic import BaseModel,Field,field_validator,model_validator,computed_field
from typing import List,Dict,Annotated
from enum import Enum

app=FastAPI()

class StudentResponse(BaseModel):
    id:Annotated[str,Field(...,lt=0,gt=0,decription="Hello world",example="ALI")]
    name:str
    age:int
    city:str
    patents:Dict[int,List[str]]

    @field_validator("name")
    @classmethod
    def validate_name(cls,value):
        if not value[0].isupper():
            raise ValueError("Name must be capital letter")
        return value
    
    @model_validator(model='before')
    def check_age(self):
        if self.city =="Lahore"and  self.age> 19:
            raise ValueError("age must be greate then 18")
        return self
    
    @computed_field
    @property 
    def result(self)->str:
        if self.age>18:
            return "Pass"
        else:
            return "Fail"


class city(str,Enum):
    lahore="Lahore"
    karachi="Karachi"


@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: str,student:StudentResponse):
    return student


@app.get('/hello')
def hello():
    return JSONResponse(
        status_code=201,
        content=[
            {'name':'Ahmed'},
            {'city':'Lahore'}
        ]
            
    )
  
@app.get('/html',response_class=HTMLResponse)
def html():
    return HTMLResponse(
        content="""
    <html>
        <head>
            <title>Profile</title>
        </head>

        <body>
            <h1>Muazzam</h1>
            <p>Backend Developer</p>
        </body>
    </html>
    """

    )

@app.get('/google')
def google():
    return RedirectResponse(url='docs')

@app.get('/image')
def image():
    return FileResponse("image.jpg")