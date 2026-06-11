from fastapi import FastAPI, HTTPException, Query, Body
import numpy as np
from scipy.spatial import distance as dist
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

EAR_THRESHOLD = 0.21



app = FastAPI()
origins = [
    #react endpoint url
    "http://localhost:5173"
]
#orgins bellow are the same as above only allow communication with this endpoint, allow all methods and headers can restrict from using delete method

app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True, allow_methods=["*"],allow_headers=["*"])
def calcEAR(eyedataset):
   
    # Calculate the Eye Aspect Ratio (EAR) using the provided eye data
    #examaple data:
#     {
#   "leftEye": [
#     {"x": 0.612, "y": 0.421, "z": -0.015}, 
#     {"x": 0.628, "y": 0.408, "z": -0.018}, 
#     {"x": 0.645, "y": 0.409, "z": -0.017}, 
#     {"x": 0.658, "y": 0.423, "z": -0.012}, 
#     {"x": 0.644, "y": 0.434, "z": -0.013}, 
#     {"x": 0.627, "y": 0.435, "z": -0.014}  
#   ],
#   "rightEye": [
#     {"x": 0.388, "y": 0.422, "z": -0.015}, 
#     {"x": 0.372, "y": 0.409, "z": -0.018}, 
#     {"x": 0.355, "y": 0.408, "z": -0.017}, 
#     {"x": 0.342, "y": 0.424, "z": -0.012}, 
#     {"x": 0.356, "y": 0.435, "z": -0.013}, 
#     {"x": 0.373, "y": 0.434, "z": -0.014}  
#   ]
# }
    #formula = (distance(p2, p6) + distance(p3, p5)) / (2.0 * distance(p1, p4))
    
    points = [(p["x"],p["y"]) for p in eyedataset]
    top = dist.euclidean(points[1], points[5]) + dist.euclidean(points[2], points[4])
    bottom = 2.0 * dist.euclidean(points[0], points[3])
    ear = top / bottom
   
    return ear
    
    
@app.get("/")
def read_root():
    return {"Hello": "World"}



@app.post("/eye")
def get_eye_coordinates(eyedata: dict = Body(...)):
    left = eyedata.get("left")
    right = eyedata.get("right")
    if not left or not right:
        raise HTTPException(status_code=400, detail="Missing 'left' or 'right' eye data")

    try:
        leftEye = calcEAR(left)
        rightEye = calcEAR(right)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid eye coordinates format")

    avrEar = (leftEye + rightEye) / 2
    is_eye_closed = avrEar < EAR_THRESHOLD
    return {"eyeclosed": is_eye_closed}

