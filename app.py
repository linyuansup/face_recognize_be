import datetime
import pytz
from dataclasses import dataclass
from typing import List, MutableMapping, Any, Mapping

import face_recognition
import numpy
from flask import Flask, request
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.results import DeleteResult, UpdateResult

app: Flask = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
db: Collection[Mapping[str, Any] | Any] = MongoClient("mongodb://172.18.0.2:27017/")[
    "test"
]["face_recognition"]


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
    check_time: str = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y%m%d%H%M%S")
    db.update_one({"face_id": face_id_encoded}, {"$push": {"login_time": check_time}})
    return {"name": user["name"], "isAdmin": user["isAdmin"]}


@app.route("/addUser")
def add_user():
    name: str = request.args.get("name")
    face_id: str = request.args.get("face_id")
    isAdmin: bool = request.args.get("isAdmin")
    user: User = User(
        name=name, face_id=face_id, login_time=[], isAdmin=isAdmin
    )
    db.insert_one(user.to_mapping())
    return "success"


@app.route("/deleteUser")
def delete_user():
    name: str = request.args.get("id")
    result: DeleteResult = db.delete_one({"name": name})
    if result.deleted_count == 0:
        return "not found"
    return "success"


# @app.route("/getAllUser")
# def get_all_user():
#     users: Cursor[Mapping[str, Any] | Any] = db.find()
#     return {
#         "users": [
#             User(
#                 id=user["id"],
#                 name=user["name"],
#                 face_id=user["face_id"],
#                 isAdmin=user["isAdmin"],
#                 login_time=[check_time for check_time in user["login_time"]],
#             ).to_mapping()
#             for user in users
#         ]
#     }


# @app.route("/changeUserInfo")
# def change_user_info():
#     user_id: str = request.args.get("id")
#     name: str = request.args.get("name")
#     face_id: str = request.args.get("face_id")
#     isAdmin: str = request.args.get("isAdmin")
#     result: UpdateResult = db.update_one(
#         {"id": int(user_id)},
#         {"$set": {"name": name, "face_id": face_id, "isAdmin": isAdmin}},
#     )
#     if result.modified_count == 0:
#         if result.matched_count == 0:
#             return "not found"
#         return "no change"
#     return "success"


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
    info_sorted = sorted(result.items(), key=lambda v:v[0])
    res = dict(info_sorted)
    final = {}
    for key,values in res.items():
        time = key[:4] + "." + key[4:6] + "." + key[6:8] + " " + key[8:10] + ":" + key[10:12] + ":" + key[12:]
        final[time] = values
    return final


def face_id_decoding(face_id: str) -> numpy.ndarray:
    code = face_id.split(",")
    return numpy.array(code, dtype="float64")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
