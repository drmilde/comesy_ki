import uvicorn
import io
import json
from fastapi import FastAPI, Response, Request
from unified_planning.shortcuts import *
from contextlib import asynccontextmanager
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


#with open('mydata.json', 'w') as f:
#    json.dump(data, f)

#data = {"name": "empty"}


###### setup server
up.shortcuts.get_environment().credits_stream = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    ''' Run at startup '''

    print ("loading blackboard server state")
    global data
    data = loadState()
    print ("Starting up blackboard server")
    yield

    ''' Run at Shutdown '''
    print ("saving blackboard server state")
    saveState(data)
    print ("Shutting blackboard server down");

app = FastAPI(lifespan=lifespan)

############## Dantentypen

class Situation(BaseModel):
    name: str
    description: str | None = None

########

def loadState():
    f = open('mydata.json')
    daten = json.load(f)
    return daten

def saveState(daten):
    with open('mydata.json', 'w') as f:
        json.dump(daten, f)


############# ROUTEN

@app.post("/situation")
async def situation(s: Situation):
    return s

@app.get("/")
async def root(request:Request):
    #data = loadState()

    return templates.TemplateResponse("home.html", 
        {
            "request": request, 
            "name": data["name"],
            "command": data["command"],
            "speech": data["speech"],
            "listening": data["listening"],
            "running": data["running"],
            "object": data["object"],
            "action": data["action"],
            "starting": data["starting"]
        }
    )

@app.get("/info")
async def info():
    return {"message": "BlackboardServer, V1"}

@app.get("/name/")
async def read_name(value:str = "keiner"):
    data["name"] = value
    return {"message": "name set"}

@app.get("/speech/")
async def read_name(value:str = "keiner"):
    data["speech"] = value
    return {"message": "speech set"}

@app.get("/command/")
async def read_name(value:str = "keiner"):
    data["command"] = value
    return {"message": "command set"}

@app.get("/listening/")
async def read_name(value:str = "keiner"):
    data["listening"] = value
    return {"message": "listening set"}

@app.get("/running/")
async def read_name(value:str = "keiner"):
    data["running"] = value
    return {"message": "running set"}

@app.get("/object/")
async def read_name(value:str = "keiner"):
    data["object"] = value
    return {"message": "object set"}

@app.get("/action/")
async def read_name(value:str = "keiner"):
    data["action"] = value
    return {"message": "action set"}


########################


################## MAIN ####################
if __name__ == "__main__":
    uvicorn.run("blackboard_server:app", host="0.0.0.0", port=9000, reload=True)
