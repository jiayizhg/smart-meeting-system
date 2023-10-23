from flask import Flask, jsonify, request
from flask_cors import CORS,cross_origin
import cv2
import numpy as np
from deepface import DeepFace
import insightface
from insightface.app import FaceAnalysis

app = Flask(__name__)
CORS(app)

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


@app.route('/process_frame', methods=['POST'])
@cross_origin(origin='*')
def process_frame():
    file = request.files['file']
    temp_path = "temp_frame.jpg"
    file.save(temp_path)

    # Use DeepFace to analyze the frame
    emotion_results = DeepFace.analyze(img_path=temp_path, actions=['emotion'], enforce_detection=False)
    print(emotion_results)
    # Use insightface to check eyes status
    frame = cv2.imread(temp_path)
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

    return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug=True)