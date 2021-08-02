
import modules.config as cfg
import os
import face_recognition
import numpy as np
from flask_mysqldb import MySQL
from app import mysql

con_str = cfg.CONNECTION_STRING

def GetAllFaceEncodings():
    cur = mysql.connection.cursor()
    cur.execute("CALL GetAllFaceEncodings()")
    result = cur.fetchall();
    cur.close()
    return result

def extract_features(image):
    unknown_face = face_recognition.load_image_file(image)
    try:
        unknown_encoding = face_recognition.face_encodings(unknown_face)[0]
    except IndexError:
        return "Couldn't Detect Face!"

    known_faces = GetAllFaceEncodings()
    known_encodings = [face[1][1:-2] for face in known_faces] #face[0] = cnic , face[1] = face_encoding
    known_encodings_arr = []
    for known_encoding in known_encodings:
        known_encoding_arr = np.fromstring(known_encoding,dtype=np.float64, sep=" ")
        known_encodings_arr.append(known_encoding_arr)
    results = face_recognition.face_distance(known_encodings_arr, unknown_encoding)
    matched_face_ids = []
    for i in range(0, len(results)):
        if(results[i]<=0.5):
            matched_face_ids.append({"CNIC":known_faces[i][0],"Confidence_Score":'{:.2%}'.format(1-results[i])})
    if len(matched_face_ids) == 0:
        return "No similar image found!"
    else:
        return matched_face_ids

