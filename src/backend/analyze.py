from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException, APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import cv2
from flask_cors import cross_origin
import numpy as np
from deepface import DeepFace
from insightface.app import FaceAnalysis
import shutil
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
Base = declarative_base()

#Define Database
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    role = Column(String)

class MeetingRoom(Base):
    __tablename__ = 'meeting_rooms'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    creator_id = Column(Integer, ForeignKey('users.id'))

class UserMeetingRoom(Base):
    __tablename__ = 'user_meeting_room'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    meeting_room_id = Column(Integer, ForeignKey('meeting_rooms.id'), primary_key=True)
    role = Column(String)


engine = create_engine('postgresql://aaa:111@localhost/mydb')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#Meeting Part
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(engine)

@app.on_event("shutdown")
def on_shutdown():
    Base.metadata.drop_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(user_id: int, db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def is_boss(user: User) -> bool:
    return user.role == 'boss'

@app.post("/users/")
def create_user(name: str, role: str, db: Session = Depends(get_db)):
    db_user = User(name=name, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/meeting_rooms/")
def create_meeting_room(name: str, creator_id: int, db: Session = Depends(get_db)):
    db_meeting_room = MeetingRoom(name=name, creator_id=creator_id)
    db.add(db_meeting_room)
    db.commit()
    db.refresh(db_meeting_room)
    return db_meeting_room

@app.post("/join_meeting_room/")
def join_meeting_room(user_id: int, meeting_room_id: int, role: str, db: Session = Depends(get_db)):
    db_join = UserMeetingRoom(user_id=user_id, meeting_room_id=meeting_room_id, role=role)
    db.add(db_join)
    db.commit()
    db.refresh(db_join)
    return db_join

@app.get("/users/", response_model=List[User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/meeting_rooms/", response_model=List[MeetingRoom])
def get_meeting_rooms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    meeting_rooms = db.query(MeetingRoom).offset(skip).limit(limit).all()
    return meeting_rooms

@app.get("/meeting_room_members/{meeting_room_id}", response_model=List[UserMeetingRoom])
def get_meeting_room_members(meeting_room_id: int, db: Session = Depends(get_db)):
    members = db.query(UserMeetingRoom).filter(UserMeetingRoom.meeting_room_id == meeting_room_id).all()
    return members

@app.put("/update_meeting_room_member/")
def update_member_role(user_id: int, meeting_room_id: int, role: str, db: Session = Depends(get_current_user)):
    member = db.query(UserMeetingRoom).filter(
        UserMeetingRoom.user_id == user_id, 
        UserMeetingRoom.meeting_room_id == meeting_room_id
    ).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    if not is_boss(current_user):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    member.role = role
    db.commit()
    return member

#Facial Part
app_analysis = FaceAnalysis(allowed_modules=['detection', 'landmark_2d_106'])
app_analysis.prepare(ctx_id=0, det_size=(640, 640))

def is_eye_closed(eye_points, left_point, right_point):
    bottom_point = np.mean(eye_points[[0, 4, 5]], axis=0)
    top_point = np.mean(eye_points[[7, 8, 9]], axis=0)
    vertical_distance = np.linalg.norm(top_point - bottom_point)
    horizontal_distance = np.linalg.norm(left_point - right_point)
    ear = vertical_distance / horizontal_distance
    threshold = 0.12
    return ear < threshold

async def process_frame(file_path: str):
    emotion_results = DeepFace.analyze(img_path=file_path, actions=['emotion'], enforce_detection=False)
    frame = cv2.imread(file_path)
    faces = app_analysis.get(frame)
    eyes_status = {"left_eye": "open", "right_eye": "open"}
    for face in faces:
            lmk = face.landmark_2d_106
            lmk = np.round(lmk).astype(np.int)
            left_eye = np.append(lmk[33:43], [lmk[75]], axis=0)
            right_eye = np.append(lmk[87:97], [lmk[81]], axis=0)

            if is_eye_closed(left_eye, left_eye[2], left_eye[10]):
                eyes_status["left_eye"] = "closed"
            if is_eye_closed(right_eye, right_eye[6], right_eye[10]):
                eyes_status["right_eye"] = "closed"
    response_data = {
        "emotion": emotion_results[0]['emotion'],
        "eyes_status": eyes_status
    }

    return response_data

@app.post("/process_frame")
async def upload_file(file: UploadFile = File(...)):
    try:
        temp_path = f"temp_frame_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = await process_frame(temp_path)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)

# uvicorn analyze:app --reload