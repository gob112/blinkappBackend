from fastapi import FastAPI, HTTPException, Query
import numpy as np
from scipy.spatial import distance as dist

EAR_THRESHOLD = 0.21



app = FastAPI()

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
    print(ear)
    return ear
    
    
@app.get("/")
def home():
    return {"message": "Welcome to the Randomizer API"}

@app.post("/eye")
def get_eye_coordinates(eyedata:dict):
   
    leftEye = calcEAR(eyedata.get("left"))
    rightEye = calcEAR(eyedata.get("right"))
    
    avrEar =(leftEye+rightEye)/2
    open= avrEar < EAR_THRESHOLD
    if open:
        is_eye_open = "true"
    else:
        is_eye_open = "false"
    
    return {"eyeclosed": is_eye_open}