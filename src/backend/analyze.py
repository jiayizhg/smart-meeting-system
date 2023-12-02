from datetime import datetime
from typing import List
from fastapi import FastAPI, Request, UploadFile, File, HTTPException, APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import cv2
from flask_cors import cross_origin
import numpy as np
from deepface import DeepFace
from insightface.app import FaceAnalysis
import shutil
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime, MetaData, Table, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine, Column, Integer, Float, DateTime, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
Base = declarative_base()






engine = create_engine('mysql+pymysql://root:admin@localhost:3306/meeting_db')
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

Base.metadata.create_all(bind=engine)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()


# new_user_data = UserEmotionData(
#     angry=0.1,
#     disgust=0.2,
#     fear=0.3,
#     happy=0.4,
#     sad=0.5,
#     surprise=0.6,
#     neutral=0.7,
#     emotion_result=0.8
# )

# db.add(new_user_data)
# db.commit()

# # 关闭会话
# db.close()


#Define Database
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     role = Column(String)
#     is_temporary = Column(bool, default=False)

# class MeetingRoom(Base):
#     __tablename__ = 'meeting_rooms'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     creator_id = Column(Integer, ForeignKey('users.id'))
#     start_time = Column(datetime)
#     end_time = Column(datetime)

# class UserMeetingRoom(Base):
#     __tablename__ = 'user_meeting_room'
#     user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
#     meeting_room_id = Column(Integer, ForeignKey('meeting_rooms.id'), primary_key=True)
#     role = Column(String)


# engine = create_engine('postgresql://aaa:111@localhost/mydb')
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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

# def get_current_user(user_id: int, db: Session = Depends(get_db)) -> User:
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# def is_boss(user: User) -> bool:
#     return user.role == 'boss'

# def cleanup_users(db: Session):
#     current_time = datetime.now()
#     ended_meetings = db.query(MeetingRoom).filter(MeetingRoom.end_time < current_time).all()
    
#     for meeting in ended_meetings:
#         db.query(User).filter(
#             User.id.in_(
#                 db.query(UserMeetingRoom.user_id).filter(UserMeetingRoom.meeting_room_id == meeting.id)
#             ),
#             User.is_temporary == True
#         ).delete()
#         db.commit()

# # def start_scheduler():
# #     scheduler = BackgroundScheduler()
# #     scheduler.add_job(cleanup_users, 'interval', minutes=5) 
# #     scheduler.start()

# @app.on_event("startup")
# async def startup_event():
#     start_scheduler()

# @app.post("/users/")
# def create_user(name: str, role: str, db: Session = Depends(get_db)):
#     db_user = User(name=name, role=role)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# @app.post("/meeting_rooms/")
# def create_meeting_room(name: str, creator_id: int, db: Session = Depends(get_db)):
#     db_meeting_room = MeetingRoom(name=name, creator_id=creator_id)
#     db.add(db_meeting_room)
#     db.commit()
#     db.refresh(db_meeting_room)
#     return db_meeting_room

# @app.post("/join_meeting_room/")
# async def join_meeting_room(request: Request, db: Session = Depends(get_db)):
#     data = await request.json()
#     username = data.get("username")
#     meeting_room_id = data.get("meeting_room_id")

#     if not username or not meeting_room_id:
#         raise HTTPException(status_code=400, detail="Missing username or meeting room ID")
#     user = db.query(User).filter(User.name == username).first()
#     if not user:
#         user = User(name=username, role="employee", is_temporary=True)
#         db.add(user)
#         db.commit()
#         db.refresh(user)
#     user_id = data.get("user_id")
#     role= data.get("role")
#     db_join = UserMeetingRoom(user_id=user_id, meeting_room_id=meeting_room_id, role=role)
#     db.add(db_join)
#     db.commit()
#     db.refresh(db_join)
#     return db_join


# @app.get("/users/", response_model=List[User])
# def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     users = db.query(User).offset(skip).limit(limit).all()
#     return users

# @app.get("/meeting_rooms/", response_model=List[MeetingRoom])
# def get_meeting_rooms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     meeting_rooms = db.query(MeetingRoom).offset(skip).limit(limit).all()
#     return meeting_rooms

# @app.get("/meeting_room_members/{meeting_room_id}", response_model=List[UserMeetingRoom])
# def get_meeting_room_members(meeting_room_id: int, db: Session = Depends(get_db)):
#     members = db.query(UserMeetingRoom).filter(UserMeetingRoom.meeting_room_id == meeting_room_id).all()
#     return members

# @app.put("/update_meeting_room_member/")
# def update_member_role(user_id: int, meeting_room_id: int, role: str, db: Session = Depends(get_current_user)):
#     member = db.query(UserMeetingRoom).filter(
#         UserMeetingRoom.user_id == user_id, 
#         UserMeetingRoom.meeting_room_id == meeting_room_id
#     ).first()
#     if not member:
#         raise HTTPException(status_code=404, detail="Member not found")
#     if not is_boss(get_current_user):
#         raise HTTPException(status_code=403, detail="Insufficient permissions")
#     member.role = role
#     db.commit()
#     return member


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
    # faces = app_analysis.get(frame)
    eyes_status = {"left_eye": "open", "right_eye": "open"}
    # for face in faces:
    #         lmk = face.landmark_2d_106
    #         lmk = np.round(lmk).astype(np.int)
    #         left_eye = np.append(lmk[33:43], [lmk[75]], axis=0)
    #         right_eye = np.append(lmk[87:97], [lmk[81]], axis=0)

    #         if is_eye_closed(left_eye, left_eye[2], left_eye[10]):
    #             eyes_status["left_eye"] = "closed"
    #         if is_eye_closed(right_eye, right_eye[6], right_eye[10]):
    #             eyes_status["right_eye"] = "closed"
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

@app.get("/get_user_emotion_data/{user_id}/{emotion_type}/{start_date}/{end_date}", response_model=list)
def get_user_emotion(user_id: int, emotion_type: str, start_date: datetime, end_date: datetime):
    return get_user_emotion_data(user_id, emotion_type, start_date, end_date)


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

        # 查询数据库
        result = (
            db.query(UserEmotionData)
            .filter(*query_conditions)
            .order_by(UserEmotionData.update_time)
            .all()
        )

        if not result:
            raise HTTPException(status_code=404, detail="Data not found")
        print(result)

        formatted_results = [
            {
                'emotion_data': "{:.6f}".format(getattr(entry, emotion_type)),
                'update_time': entry.update_time
            }
            for entry in result
        ]

        return formatted_results
    
    except Exception as e:
        print(e)


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


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)

# uvicorn analyze:app --reload