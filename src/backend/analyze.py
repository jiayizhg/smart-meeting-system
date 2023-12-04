from datetime import datetime
from operator import or_
import random
from pydantic import BaseModel
import math
from typing import List
from fastapi import FastAPI, Request, UploadFile, File, HTTPException, APIRouter, HTTPException, Depends,Query
from fastapi.responses import JSONResponse
from werkzeug.security import generate_password_hash, check_password_hash
import cv2
import json
from flask_cors import cross_origin
import numpy as np
from deepface import DeepFace

import mediapipe as mp


import shutil
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime, MetaData, Table, VARCHAR, text,Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, Boolean,BigInteger,PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from urllib.parse import quote_plus
Base = declarative_base()


raw_password = ""
encoded_password = quote_plus(raw_password)
# connection_string = f"mysql+pymysql://root:{encoded_password}@localhost:3306/meeting_db"
# engine = create_engine(connection_string)

server_connection_string = f"mysql+pymysql://root:{encoded_password}@localhost:3306/"
engine = create_engine(server_connection_string)

with engine.connect() as connection:
    connection.execute(text("CREATE DATABASE IF NOT EXISTS meeting_db"))
database_connection_string = f"mysql+pymysql://root:{encoded_password}@localhost:3306/meeting_db"
engine.dispose()
engine = create_engine(database_connection_string)


print(engine)

Base = declarative_base()


class UserEmotionData(Base):
    __tablename__ = 'user_emotion_data'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    angry = Column(Float, nullable=False)
    disgust = Column(Float, nullable=False)
    fear = Column(Float, nullable=False)
    happy = Column(Float, nullable=False)
    sad = Column(Float, nullable=False)
    surprise = Column(Float, nullable=False)
    neutral = Column(Float, nullable=False)
    emotion_result = Column(VARCHAR(50), nullable=True)
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_emotion_data_pk'),
    )


class UserDistractedData(Base):
    __tablename__ = 'user_distracted_data'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    distracted_result = Column(VARCHAR(100), nullable=False)
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())
    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_distracted_data_pk'),
    )
    

class UserData(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    name = Column(VARCHAR(100),nullable=False)
    role = Column(VARCHAR(50),nullable=False)
    password = Column(VARCHAR(1024),nullable=False)
    is_online = Column(Boolean, default=False,nullable=False)
    last_active_time = Column(DateTime, server_default=func.now(), onupdate=func.now())

class UserCreate(BaseModel):
    name:str
    passowrd:str

class UserAuthenticate(BaseModel):
    id:int
    passowrd:str

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    sender_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    receiver_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
    sender = relationship('UserData', foreign_keys=[sender_id])
    receiver = relationship('UserData', foreign_keys=[receiver_id])

class MessageCreate(BaseModel):
    sender_id: int
    receiver_id: int
    content: str

class MeetingRoom(Base):
    __tablename__ = 'meeting_rooms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    host_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    title = Column(VARCHAR(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True, nullable=False)

class MeetingRoomParticipant(Base):
    __tablename__ = 'meeting_room_participants'
    id = Column(Integer, primary_key=True, autoincrement=True)
    meeting_room_id = Column(Integer, ForeignKey('meeting_rooms.id'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    role = Column(VARCHAR(50), nullable=False, default='participant') # Roles: 'host', 'participant'
    joined_at = Column(DateTime, server_default=func.now())

class MeetingRoomMessage(Base):
    __tablename__ = 'meeting_room_messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    meeting_room_id = Column(Integer, ForeignKey('meeting_rooms.id'), nullable=False)
    sender_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())

class MeetingRoomCreate(BaseModel):
    host_id: int
    title: str

class MeetingRoomParticipantCreate(BaseModel):
    meeting_room_id: int
    user_id: int
    role: str

class MeetingRoomMessageCreate(BaseModel):
    meeting_room_id: int
    sender_id: int
    content: str


Base.metadata.create_all(bind=engine)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# #Meeting Part
# @app.on_event("startup")
# def on_startup():
#     Base.metadata.create_all(engine)

# @app.on_event("shutdown")
# def on_shutdown():
#     Base.metadata.drop_all(engine)


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# def cleanup_users(db: Session):
#     current_time = datetime.now()
#     ended_meetings = db.query(MeetingRoom).filter(MeetingRoom.end_time < current_time).all()
    
#     for meeting in ended_meetings:
#         db.query(User).filter(
#             User.id.in_(
#                 db.query(UserMeetingRoom.user_id).filter(UserMeetingRoom.meeting_room_id == meeting.id)
#             ),
#             User.is_online == True
#         ).delete()
#         db.commit()

# # def start_scheduler():
# #     scheduler = BackgroundScheduler()
# #     scheduler.add_job(cleanup_users, 'interval', minutes=5) 
# #     scheduler.start()


#Facial Part

LEFT_EYE_INDICES = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE_INDICES = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def calculate_eye_aspect_ratio(landmarks, eye_indices):
    horizontal = euclidean_distance(landmarks[eye_indices[0]], landmarks[eye_indices[8]])
    vertical1 = euclidean_distance(landmarks[eye_indices[12]], landmarks[eye_indices[4]])
    vertical2 = euclidean_distance(landmarks[eye_indices[13]], landmarks[eye_indices[5]])
    ear = (vertical1 + vertical2) / (2 * horizontal)
    return ear

def get_eye_landmarks(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame)
    landmarks = []
    if results.multi_face_landmarks:
        for landmark in results.multi_face_landmarks[0].landmark: 
            x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
            landmarks.append((x, y))
    

    LEFT_EYE_INDICES = [33, 133, 160, 144, 145, 153, 154, 155]
    RIGHT_EYE_INDICES = [362, 263, 466, 388, 387, 386, 385, 384]

    cropped_left_eye, cropped_right_eye = [], []
    if landmarks:
        left_eye_coords = [landmarks[idx] for idx in LEFT_EYE_INDICES]
        lx_coords, ly_coords = zip(*left_eye_coords)
        lx_min, lx_max = min(lx_coords), max(lx_coords)
        ly_min, ly_max = min(ly_coords), max(ly_coords)
        cropped_left_eye = frame[ly_min:ly_max, lx_min:lx_max]

        right_eye_coords = [landmarks[idx] for idx in RIGHT_EYE_INDICES]
        rx_coords, ry_coords = zip(*right_eye_coords)
        rx_min, rx_max = min(rx_coords), max(rx_coords)
        ry_min, ry_max = min(ry_coords), max(ry_coords)
        cropped_right_eye = frame[ry_min:ry_max, rx_min:rx_max]
    return landmarks, cropped_left_eye, cropped_right_eye

def is_left_eye_closed(landmarks, threshold=0.15):
    left_ear = calculate_eye_aspect_ratio(landmarks, LEFT_EYE_INDICES)
    return left_ear < threshold

def is_right_eye_closed(landmarks, threshold=0.15):
    right_ear = calculate_eye_aspect_ratio(landmarks, RIGHT_EYE_INDICES)
    return right_ear < threshold

def get_eye_direction(cropped_eye):
    gray_eye = cv2.cvtColor(cropped_eye, cv2.COLOR_BGR2GRAY)
    blurred_eye = cv2.GaussianBlur(gray_eye, (7, 7), 0)
    _, threshold_eye = cv2.threshold(blurred_eye, 30, 255, cv2.THRESH_BINARY_INV)
    h, w = threshold_eye.shape
    side_piece_width = int(w / 3)
    center_piece_width = w - 2 * side_piece_width
    left_piece = threshold_eye[0:h, 0:side_piece_width]
    center_piece = threshold_eye[0:h, side_piece_width:side_piece_width + center_piece_width]
    right_piece = threshold_eye[0:h, side_piece_width + center_piece_width:w]
    left_part = np.sum(left_piece == 0)
    center_part = np.sum(center_piece == 0)
    right_part = np.sum(right_piece == 0)
    eye_parts = [left_part, center_part, right_part]
    max_index = eye_parts.index(max(eye_parts))
    if max_index == 0:
        return "left"
    elif max_index == 1:
        return "center"
    elif max_index == 2:
        return "right"
    else:
        return "missing"


async def process_frame(file_path: str):
    emotion_results = DeepFace.analyze(img_path=file_path, actions=['emotion'], enforce_detection=False)
    frame = cv2.imread(file_path)
    # faces = app_analysis.get(frame)
    eyes_status = {"left_eye": "open", "right_eye": "open", "left_eye_direction": "center", "right_eye_direction": "center"}
    landmarks, cropped_left_eye, cropped_right_eye = get_eye_landmarks(frame)
    if len(landmarks) < max(LEFT_EYE_INDICES) + 1:
        eyes_status= {"left_eye": "closed", "right_eye": "closed", "left_eye_direction": "missing", "right_eye_direction": "missing"}
        response_data = {
            "emotion": emotion_results[0]['emotion'],
            "eyes_status": eyes_status
        }
        return response_data
    
    eyes_status["left_eye"] = "closed" if is_left_eye_closed(landmarks) else "open"
    eyes_status["right_eye"] = "closed" if is_right_eye_closed(landmarks) else "open"
    eyes_status["left_eye_direction"] = get_eye_direction(cropped_left_eye)
    eyes_status["right_eye_direction"] = get_eye_direction(cropped_right_eye)
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
        print(result)

        angry_value = result['emotion']['angry']
        disgust_value = result['emotion']['disgust']
        fear_value = result['emotion']['fear']
        happy_value = result['emotion']['happy']
        sad_value = result['emotion']['sad']
        surprise_value = result['emotion']['surprise']
        neutral_value = result['emotion']['neutral']

        # for d_data in result['emotion']:
        #     print(d_data)
        e_res = max(zip(result['emotion'].values(),result['emotion'].keys()))[1]

        insert_user_emotion_data(db, 1, angry_value,disgust_value, fear_value,happy_value, sad_value, surprise_value, neutral_value, e_res)

        return JSONResponse(content=result)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/get_emotion_statistics/{user_id}", response_model=dict)
def get_user_emotion_statistics_data(user_id: int):
    return get_user_emotion_statistics(user_id)

# @app.get("/get_user_emotion_data/{user_id}&{emotion_type}&{start_date}&{end_date}", response_model=list)
# def get_user_emotion(user_id: int, emotion_type: str, start_date: datetime, end_date: datetime):
@app.get("/get_user_emotion_data")
def get_user_emotion(user_id: int = Query(...), emotion_type: str = Query(...), start_date: datetime = Query(...), end_date: datetime = Query(...)):
    print(f"Received request with user_id: {user_id}, emotion_type: {emotion_type}, start_date: {start_date}, end_date: {end_date}")
    return get_user_emotion_data(user_id, emotion_type, start_date, end_date)




@app.get("/get_distraction_data/{user_id}",response_model=list)
def get_user_distraction(user_id:int):
    return get_user_distraction_data(user_id)


#return distraction_type count (int)
#distraction type:  Yawning , Talking , Eyes look elsewhere , Drowsiness , Sleeping , Looking at another direction
@app.get("/get_distraction_count/{user_id}/{distraction_type}/{start_date}/{end_date}", response_model=int)
def get_user_distraction_count(user_id: int, distraction_type: str, start_date: datetime, end_date: datetime):
    print(get_user_distraction_type_count(user_id, distraction_type, start_date, end_date))
    return get_user_distraction_type_count(user_id, distraction_type, start_date, end_date)

def generate_user_id():
    while True:
        user_id = str(random.randint(100000, 999999))
        query_conditions = [
            UserData.id == user_id
        ]
        result = (
            db.query(UserData)
            .filter(*query_conditions)
            .all()
        )
        if not result:
            return user_id

@app.post("/add_user")
def add_user(user:UserCreate):
    user_id = generate_user_id()
    print(user_id)
    hashed_password = generate_password_hash(user.passowrd)
    # insert_user_data(db, user.id,user.name,user.role,user.is_online,user.password)
    insert_user_data(db, user_id,user.name,"Participant",False,hashed_password)
    return {
        "id":{user_id}
    }


@app.post("/user_login")
def user_login(user:UserAuthenticate):
    db_user = db.query(UserData).filter(UserData.id == user.id).first()
    if db_user and check_password_hash(db_user.password, user.passowrd):
        db_user.is_online = True
        db.commit()
        return {
            "message":"Login successful"
        }
    else:
        raise HTTPException(status_code=400,detail="Wrong ID or Password.")

@app.post("/user_logout")
def user_login(user:UserAuthenticate):
    db_user = db.query(UserData).filter(UserData.id == user.id).first()
    if db_user and check_password_hash(db_user.password, user.passowrd):
        db_user.is_online = False
        db.commit()
        return {
            "message":"Logout successful"
        }
    else:
        raise HTTPException(status_code=400,detail="Wrong Status, Login and then logout again.")

@app.get("/get_user_status")
def get_current_user(user_id:int):
    user = db.query(UserData).filter(UserData.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.password=""
    return user

@app.get("/get_user_status")
def get_user_status(username: str):
    users = db.query(UserData).filter(UserData.name == username).all()
    user_statuses = []
    for user in users:
        user_status = {
            "id": user.id,
            "name": user.name,
            "is_online": user.is_online
        }
        user_statuses.append(user_status)
    return user_statuses

@app.post('/send_message')
async def send_message(message: MessageCreate):
    try:
        db_message = Message(sender_id=message.sender_id, receiver_id=message.receiver_id, content=message.content)
        db.add(db_message)
        db.commit()
        return {"message": "Message sent successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400,detail="Wrong Message Status.")

@app.get('/get_messages')
async def get_messages(user_id: int):
    messages = db.query(Message).filter(or_(Message.sender_id == user_id, Message.receiver_id == user_id)).all()
    return messages

@app.post("/create_meeting_room")
def create_meeting_room(meeting_room: MeetingRoomCreate):
    try:
        new_meeting_room = MeetingRoom(host_id=meeting_room.host_id, title=meeting_room.title)
        db.add(new_meeting_room)
        db.commit()
        new_participant = MeetingRoomParticipant(meeting_room_id=new_meeting_room.id, user_id=meeting_room.host_id, role="host")
        db.add(new_participant)
        db.commit()
        return {"message": "Meeting room created successfully", "meeting_room_id": new_meeting_room.id}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400,detail="Create meeting room failed")

@app.post("/add_user_to_meeting_room")
def add_user_to_meeting_room(participant: MeetingRoomParticipantCreate):
    try:
        new_participant = MeetingRoomParticipant(meeting_room_id=participant.meeting_room_id, user_id=participant.user_id, role=participant.role)
        db.add(new_participant)
        db.commit()
        return {"message": "User added to meeting room successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400,detail="Add user "+str(participant.user_id)+" to meeting room failed")
    
@app.post("change_role_in_meeting_room")
def change_role_in_meeting_room(participant: MeetingRoomParticipantCreate):
    meeting_user = db.query(MeetingRoomParticipant).filter(MeetingRoomParticipant.user_id == participant.user_id).first()
    if meeting_user:
        meeting_user.role = participant.role
        db.commit()
        return {
            "message":"Change Role successful"
        }
    else:
        raise HTTPException(status_code=400,detail="Change Role Failed")
    


@app.get("/meeting_room_participants")
def get_meeting_room_participants(meeting_room_id: int):
    participants = db.query(MeetingRoomParticipant).filter(MeetingRoomParticipant.meeting_room_id == meeting_room_id).all()
    return participants
   
@app.post("/send_room_message")
def send_message(message: MeetingRoomMessageCreate):
    try:
        new_message = MeetingRoomMessage(meeting_room_id=message.meeting_room_id, sender_id=message.sender_id, content=message.content)
        db.add(new_message)
        db.commit()
        return {"message": "Message sent successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400,detail="Send message in meeting room failed")


@app.get("/get_room_messages")
def get_room_messages(meeting_room_id: int):
    messages = db.query(MeetingRoomMessage).filter(MeetingRoomMessage.meeting_room_id == meeting_room_id).all()
    return messages

@app.post("/leave_meeting_room")
def leave_meeting_room(meeting_room_id: int, user_id: int):
    try:
        db.query(MeetingRoomParticipant).filter(MeetingRoomParticipant.meeting_room_id == meeting_room_id, MeetingRoomParticipant.user_id == user_id).delete()
        db.commit()
        remaining_hosts = db.query(MeetingRoomParticipant).filter(MeetingRoomParticipant.meeting_room_id == meeting_room_id, MeetingRoomParticipant.role == 'host').count()
        if remaining_hosts == 0:
            meeting_room = db.query(MeetingRoom).filter(MeetingRoom.id == meeting_room_id).first()
            meeting_room.is_active = False
            db.commit()
        return {"message": "Left meeting room successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400,detail="Leave meeting room failed")

#get user statistics data using user_id from db
def get_user_emotion_statistics(user_id: int):
    try:
        result = (
            db.query(
                func.avg(UserEmotionData.angry).label('avg_angry'),
                func.avg(UserEmotionData.disgust).label('avg_disgust'),
                func.avg(UserEmotionData.fear).label('avg_fear'),
                func.avg(UserEmotionData.happy).label('avg_happy'),
                func.avg(UserEmotionData.sad).label('avg_sad'),
                func.avg(UserEmotionData.surprise).label('avg_surprise'),
                func.avg(UserEmotionData.neutral).label('avg_neutral')
            )
            .filter(UserEmotionData.user_id == user_id)
            .one_or_none()
        )

        if not result:
            raise HTTPException(status_code=404, detail="User not found")

        avg_angry = result.avg_angry
        avg_disgust = result.avg_disgust
        avg_fear = result.avg_fear
        avg_happy = result.avg_happy
        avg_sad = result.avg_sad
        avg_surprise = result.avg_surprise
        avg_neutral = result.avg_neutral

        return {'avg_angry': avg_angry, 
                'avg_disgust': avg_disgust, 
                'avg_fear':avg_fear, 
                'avg_happy':avg_happy, 
                'avg_sad':avg_sad, 
                'avg_surprise':avg_surprise,
                'avg_neutral':avg_neutral}

    except Exception as e:
        print(e)


#get user emotion data using id, type, start time and end time
def get_user_emotion_data(user_id: int, emotion_type: str, start_date: datetime, end_date: datetime):
    try:
        if emotion_type not in UserEmotionData.__table__.columns:
            raise HTTPException(status_code=400, detail=f"Invalid emotion_type: {emotion_type}")

        query_conditions = [
            UserEmotionData.user_id == user_id,
            getattr(UserEmotionData, emotion_type) is not None,
            UserEmotionData.update_time >= start_date,
            UserEmotionData.update_time <= end_date
        ]

        result = (
            db.query(UserEmotionData)
            .filter(*query_conditions)
            .order_by(UserEmotionData.update_time)
            .all()
        )
        
    except Exception as e:
        print(e)
    if not result:
        raise HTTPException(status_code=404, detail="Data not found")

    formatted_results = [
        {
            'emotion_data': "{:.6f}".format(getattr(entry, emotion_type)),
            'update_time': entry.update_time
        }
        for entry in result
    ]
    print(formatted_results)
    return formatted_results
    



#get user distracted data using id
def get_user_distraction_data(user_id: int):
    try:
        result = (
            db.query(UserDistractedData)
            .filter(UserDistractedData.user_id == user_id)
            .order_by(UserDistractedData.update_time.desc())
            .all()
        )
        
        formatted_results = [
            {
                'distracted_result': entry.distracted_result,
                'update_time':entry.update_time

            }
            for entry in result
        ]
        return formatted_results
    
    except Exception as e:
        print(e)


#get distracted count using id ,distracted_type, start time and end time
def get_user_distraction_type_count(user_id: int, distracted_result: str, start_date: datetime, end_date: datetime):
    count =  (
        db.query(func.count(UserDistractedData.distracted_result))
        .filter(
            UserDistractedData.user_id == user_id,
            UserDistractedData.distracted_result == distracted_result,
            UserDistractedData.update_time >= start_date,
            UserDistractedData.update_time <= end_date
        )
        .scalar()
    )
    return count



#Insert emotion to db
def insert_user_emotion_data(db, user_id ,angry, disgust, fear, happy, sad, surprise, neutral, emotion_result):
    new_user_data = UserEmotionData(
        user_id = user_id,
        angry=angry,
        disgust=disgust,
        fear=fear,
        happy=happy,
        sad=sad,
        surprise=surprise,
        neutral=neutral,
        emotion_result=emotion_result
    )
    try:
        db.add(new_user_data)
        db.commit()
    except Exception as e:
        print(e)


#Insert distracted data to distracted table
def insert_user_distracted_data(db, user_id,distracted_result):
    #Test 
    test_distracted_data = UserDistractedData(
    user_id = user_id,
    distracted_result = distracted_result
    )
    try:        
        db.add(test_distracted_data)
        db.commit()
    except Exception as e:
        print(e)

def insert_user_data(db, id, name, role, is_online,password):
    user_data = UserData(
        id = id,
        name = name,
        role = role,
        is_online = is_online,
        password = password
    )
    try:
        db.add(user_data)
        db.commit()
    except Exception as e:
        print(e)






print(get_user_distraction_data(1))
print(get_user_distraction_type_count(2,'Normal','2023-11-30T12:23:23','2023-12-02T12:23:23'))

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)

# uvicorn analyze:app --reload