import datetime
import os
from dataclasses import dataclass
from typing import Any, List, Mapping, MutableMapping

import cv2
import face_recognition
import numpy
import pytz
from flask import Flask, request, send_from_directory
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor

app: Flask = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
db: Collection[Mapping[str, Any] | Any] = MongoClient("mongodb://127.0.0.1:27017/")[
    "test"
]["face_recognition"]
idp: Collection[Mapping[str, Any] | Any] = MongoClient("mongodb://127.0.0.1:27017/")[
    "test"
]["id"]


@dataclass
class User:
    name: str
    isAdmin: bool
    face_id: str
    login_time: List[str]

    def to_mapping(self) -> MutableMapping:
        return {
            "name": self.name,
            "face_id": self.face_id,
            "isAdmin": self.isAdmin,
            "login_time": [check_time for check_time in self.login_time],
        }


@app.route("/checkFace")
def check_face():
    global user
    face_id = face_id_decoding(request.args.get("face_id"))
    users: Cursor[Mapping[str, Any] | Any] = db.find()
    face_ids = []
    for user in users:
        face_ids.append(face_id_decoding(user["face_id"]))
    face_distances = face_recognition.face_distance(face_ids, face_id)
    best_match_index = numpy.argmin(face_distances)
    if face_distances[best_match_index] < 0.4:
        id1 = face_ids[best_match_index]
        face_id_encoded = ",".join(map(str, id1.tolist()))
        user = db.find_one({"face_id": face_id_encoded})
    else:
        return "Unknown"
    check_time: str = datetime.datetime.now(pytz.timezone("Asia/Shanghai")).strftime(
        "%Y%m%d%H%M%S"
    )
    db.update_one({"face_id": face_id_encoded}, {"$push": {"login_time": check_time}})
    return {"name": user["name"], "isAdmin": user["isAdmin"]}


def cv_imread(filePath):
    cv_img = cv2.imdecode(numpy.fromfile(filePath, dtype=numpy.uint8), -1)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
    return cv_img


def train():
    global recognizer
    idp.drop
    face_list: List[str] = data_needed("./pic")
    images = []
    labels = []
    i = 0
    for a in face_list:
        images.append(cv_imread("./pic/" + a + "/1.jpg"))
        images.append(cv_imread("./pic/" + a + "/2.jpg"))
        labels.append(i)
        labels.append(i)
        idp.insert_one({"id": i, "name": a})
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if not len(images) == 0:
        recognizer.train(images, numpy.array(labels))


@app.route("/checkFace2", methods=["GET", "POST"])
def check_face_2():
    return {"name": "黄安然", "isAdmin": "true"}


@app.route("/addUser")
def add_user():
    return "success"


def change(path):
    img = cv2.imread(path)
    # 要检测cascade文件是否在路径下，最后一般使用绝对路径。
    haar = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    n = 1
    # 将图片进行转灰
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = haar.detectMultiScale(gray_img, 1.3, 2)
    f_x, f_y, f_w, f_h = faces[0]
    face = img[f_y : f_y + f_h, f_x : f_x + f_w]
    face = cv2.resize(face, (96, 96), interpolation=cv2.INTER_AREA)
    # could deal with face to train
    # face = relight(face, random.uniform(0.5, 1.5), random.randint(-50, 50))
    cv2.imwrite(path, face)


@app.route("/deleteUser")
def delete_user():
    return "success"


@app.route("/getCheckInfo")
def get_check_info():
    start_time: str = request.args.get("start_time")
    end_time: str = request.args.get("end_time")
    start_time = start_time.replace("-", "").replace(":", "").replace(" ", "")
    end_time = end_time.replace("-", "").replace(":", "").replace(" ", "")
    result = {}
    users: Cursor[Mapping[str, Any] | Any] = db.find()
    for user in users:
        for checkTime in user["login_time"]:
            if start_time <= checkTime <= end_time:
                result[checkTime] = user["name"]
    info_sorted = sorted(result.items(), key=lambda v: v[0])
    res = dict(info_sorted)
    final = {}
    for key, values in res.items():
        time = (
            key[:4]
            + "."
            + key[4:6]
            + "."
            + key[6:8]
            + " "
            + key[8:10]
            + ":"
            + key[10:12]
            + ":"
            + key[12:]
        )
        final[time] = values
    return final


def face_id_decoding(face_id: str) -> numpy.ndarray:
    code = face_id.split(",")
    return numpy.array(code, dtype="float64")


@app.route("/getFace")
def get_face():
    return send_from_directory("", "1.jpg")


def data_needed(filePath):
    all_data = os.listdir(filePath)
    res = []
    for i in all_data:
        if os.path.isdir(filePath + "/" + i):
            res.append(i)
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
