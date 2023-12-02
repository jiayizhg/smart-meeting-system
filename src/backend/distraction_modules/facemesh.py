import os
import time

import cv2
import numpy as np
import mediapipe as mp


from distraction_modules import utils, config
mp_face_mesh = mp.solutions.face_mesh


class Distraction():
    def __init__(self):
        self.facemesh = mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)
        self.i_non = 0
        self.i_h = 0
        self.i_hd = 0
        self.i_ear = 0
        self.i_ed = 0
        self.i_lip_y = 0
        self.i_lip_t = 0
        self.i_a = 0

    @staticmethod
    def lip_dist_vs_face(lm_coords):
        """Ratio of distance between upper lip and lower lip to the length of face"""
        lip_dist = utils.dist(
            lm_coords[config.LIP[0]], lm_coords[config.LIP[1]])
        len_face = utils.dist(
            lm_coords[config.FACE[0]], lm_coords[config.FACE[1]])
        return lip_dist/len_face

    @staticmethod
    def eye_aspect_ratio(lm_coords):
        """Eye aspect ratio for detecting the openess of eyes"""
        l = [lm_coords[p] for p in config.LEFT_EYE]
        r = [lm_coords[p] for p in config.RIGHT_EYE]
        ear_l = (utils.dist(l[1], l[5]) + utils.dist(l[2],
                 l[4])) / (2 * utils.dist(l[0], l[3]))
        ear_r = (utils.dist(r[1], r[5]) + utils.dist(r[2],
                 r[4])) / (2 * utils.dist(r[0], r[3]))
        return (ear_l + ear_r)/2

    @staticmethod
    def eye_direction(lm_coords, image):
        """Ratio for the white region of the left eye to the right eye to detect the direction of eyes"""
        cropped_r = image[lm_coords[159][1]: lm_coords[145][1],
                          lm_coords[33][0]: lm_coords[133][0]]

        cropped_l = image[lm_coords[386][1]: lm_coords[374][1],
                          lm_coords[362][0]: lm_coords[263][0]]

        cropped_l = utils.binary(cropped_l)
        cropped_r = utils.binary(cropped_r)
        try:
            cropped_l_1 = cropped_l[:, :int((cropped_l.shape)[1]*0.5)]
            cropped_l_2 = cropped_l[:, int((cropped_l.shape)[1]*0.5):]

            cropped_r_1 = cropped_r[:, :int(cropped_r.shape[1]*0.5)]
            cropped_r_2 = cropped_r[:, int(cropped_r.shape[1]*0.5):]

            if np.count_nonzero(cropped_l_2) > 0 and np.count_nonzero(cropped_r_2) > 0:
                white_ratio_l = np.count_nonzero(
                    cropped_l_1) / np.count_nonzero(cropped_l_2)
                white_ratio_r = np.count_nonzero(
                    cropped_r_1) / np.count_nonzero(cropped_r_2)
                return (white_ratio_l + white_ratio_r)/2
            else:
                return 1
        except Exception as error:
            print(f"[ERROR] eye_direction: {error}")
            return 0

    @staticmethod
    def head_pose(landmarks, img_shape, dist_coeffs=np.zeros((4, 1), dtype=np.float64)):
        """Estimation of headpose using Perspective-n-Point  algorithm"""
        face_2d = []
        face_3d = []

        for idx, lm in enumerate(landmarks):
            if idx in config.FOCUS_POINTS:
                x, y = int(lm.x * img_shape[1]), int(lm.y * img_shape[0])
                face_2d.append([x, y])
                face_3d.append([x, y, lm.z])

        face_2d = np.array(face_2d, dtype=np.float64)
        face_3d = np.array(face_3d, dtype=np.float64)

        focal_length = 1 * img_shape[1]
        cam_mat = np.array([[focal_length, 0, img_shape[1]/2],
                            [0, focal_length, img_shape[0]/2],
                            [0, 0, 1]])

        success, rvec, tvec = cv2.solvePnP(
            face_3d, face_2d, cam_mat, dist_coeffs)

        rmat, jac = cv2.Rodrigues(rvec)
        angles, mtxQ, mtxR, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

        x_angle = angles[0] * 360
        y_angle = angles[1] * 360
        z_angle = angles[2] * 360

        if (y_angle > config.THRESHOLD_RIGHT_Y) or (z_angle > config.THRESHOLD_RIGHT_Z):
            text = "Looking Right"
        elif (y_angle < config.THRESHOLD_LEFT_Y) or (z_angle < config.THRESHOLD_LEFT_Z):
            text = "Looking Left"
        elif x_angle > config.THRESHOLD_UP_X:
            text = "Looking Up"
        elif x_angle < config.THRESHOLD_DOWN_X:
            text = "Looking Down"
        else:
            text = "Looking Forward"
        return text
    
    def draw_eyes(self, img, landmarks, img_width, img_height):
        left_eye_ids = list(range(362, 382))  # Landmarks for left eye
        right_eye_ids = list(range(133, 153)) # Landmarks for right eye

        # Draw circles for each landmark in both eyes
        for id in left_eye_ids + right_eye_ids:
            x, y = int(landmarks[id].x * img_width), int(landmarks[id].y * img_height)
            cv2.circle(img, (x, y), 1, (0, 255, 0), -1)

    def distract_detection(self, v_cap=None, save_video=config.FILE_OUTPUT):

        if not v_cap:
            v_cap = cv2.VideoCapture(0)
        else:
            v_cap = cv2.VideoCapture(v_cap)

        if save_video:
            if os.path.isfile(save_video):
                os.remove(save_video)
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            videoWriter = cv2.VideoWriter(
                save_video, fourcc, 30, (int(v_cap.get(3)), int(v_cap.get(4))))

        while v_cap.isOpened():
            start = time.time()
            success, img = v_cap.read()
            if not success:
                break
    
            # img = cv2.flip(img, 1)
            img_height, img_width = img.shape[:2]
            img.flags.writeable = False
            results = self.facemesh.process(
                cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            img.flags.writeable = True

            if results.multi_face_landmarks:
                self.i_non = 0
                landmarks = results.multi_face_landmarks[0].landmark
                lm_coords = [[int(lm.x * img_width), int(lm.y * img_height)]
                             for lm in landmarks]
                status = ""
                self.draw_eyes(img, landmarks, img_width, img_height)
                
                # Lip detection
                if self.lip_dist_vs_face(lm_coords) > config.THRESHOLD_YAWN:
                    self.i_lip_y += 1
                    if self.i_lip_y > config.THRESHOLD_YAWN_TIME*config.FPS:
                        status = "Distracted: Yawning!"
                else:
                    self.i_lip_y = 0

                if (self.lip_dist_vs_face(lm_coords) > config.THRESHOLD_TALKING_MIN) and (self.lip_dist_vs_face(lm_coords) < config.THRESHOLD_TALKING_MAX):
                    self.i_a = 0
                    self.i_lip_t += 1
                    if self.i_lip_t > config.THRESHOLD_TALKING_TIME*config.FPS:
                        status = "Distracted: Talking!"
                elif self.i_lip_t > config.THRESHOLD_TALKING_TIME*config.FPS:
                    self.i_lip_t += 1
                    self.i_a += 1
                    status = "Distracted: Talking!"
                    # Because the mouth opens and closes consecutively, I define the delay
                    # time for talking detection at about 1 second
                    if self.i_a == int(1*config.FPS):
                        self.i_lip_t = 0

                # Eye direction detection
                if (self.eye_direction(lm_coords, img) > config.THRESHOLD_EYE_DIRECTION_MAX) or (self.eye_direction(lm_coords, img) < config.THRESHOLD_EYE_DIRECTION_MIN):
                    self.i_ed += 1
                    if self.i_ed > config.THRESHOLD_EYE_DIRECTION_TIME*config.FPS:
                        status = "Distracted: Eyes look elsewhere!"
                else:
                    self.i_ed = 0

                # Eye openness detection
                if (self.eye_aspect_ratio(lm_coords) < config.THRESHOLD_EYE_OPENNESS):
                    if self.head_pose(landmarks, (img_height, img_width)) != "Looking Down":
                        self.i_ear += 1
                        if self.i_ear > config.THRESHOLD_EYE_OPENNESS_DROWSINESS_TIME*config.FPS:
                            status = "Distracted: Drowsiness!"
                        if self.i_ear > config.THRESHOLD_EYE_OPENNESS_SLEEPING_TIME*config.FPS:
                            status = "Distracted: Sleeping!"
                    else:
                        self.i_ear = 0
                else:
                    self.i_ear = 0

                # Head pose estimation
                if self.head_pose(landmarks, (img_height, img_width)) != "Looking Forward":
                    if self.head_pose(landmarks, (img_height, img_width)) == "Looking Down":
                        self.i_hd += 1
                    else:
                        self.i_h += 1
                    if (self.i_h > config.THRESHOLD_HEAD_LOOKING_AWAY_TIME_1*config.FPS) or (self.i_hd > config.THRESHOLD_HEAD_LOOKING_AWAY_TIME_2*config.FPS):
                        status = "Distracted: Looking at another direction!"
                else:
                    self.i_hd = 0
                    self.i_h = 0

                # Write the detected status each frame:
                if status == "":
                    cv2.putText(img, "Normal", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 225, 0), 2, cv2.LINE_AA)
                else:
                    cv2.putText(img, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 0, 225), 2, cv2.LINE_AA)

            else:
                self.i_non += 1
                self.i_h = 0
                self.i_hd = 0
                self.i_ear = 0
                self.i_ed = 0
                self.i_lip_y = 0
                self.i_lip_t = 0
                self.i_a = 0
                if self.i_non > config.THRESHOLD_NO_FACE_TIME*config.FPS:
                    cv2.putText(img, "No face detected", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 225, 0), 2, cv2.LINE_AA)

            duration = time.time() - start
            fps_cap = int(1/duration)
            # Show the FPS at each frame to taking the average fps to initialize "fps"
            cv2.putText(img, "FPS = " + str(fps_cap), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (225, 0, 0),
                        1, cv2.LINE_AA)
            if save_video:
                videoWriter.write(img)
        
            # Show the output window
            cv2.imshow("MediaPipe FaceMesh", img)
            if cv2.waitKey(5) & 0xFF == 27:
                break
            
            

            
