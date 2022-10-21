import time
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
app.config['JSON_AS_ASCII'] = False
db: Collection[Mapping[str, Any] | Any] = MongoClient(
    'mongodb://localhost:27017/')['test']['face_recognition']


@dataclass
class User:
    id: int
    name: str
    face_id: str
    login_time: List[str]

    def to_mapping(self) -> MutableMapping:
        return {
            'id': self.id,
            'name': self.name,
            'face_id': self.face_id,
            'login_time': [check_time for check_time in self.login_time]
        }


@app.route('/checkFace')
def check_face():
    global user
    face_id = face_id_decoding(request.args.get('face_id'))
    users: Cursor[Mapping[str, Any] | Any] = db.find()
    face_ids = []
    for user in users:
        face_ids.append(face_id_decoding(user['face_id']))
    face_distances = face_recognition.face_distance(face_ids, face_id)
    best_match_index = numpy.argmin(face_distances)
    if face_distances[best_match_index] < 0.4:
        id1 = face_ids[best_match_index]
        face_id_encoded = ','.join(map(str, id1.tolist()))
        user = db.find_one({'face_id': face_id_encoded})
    else:
        return 'Unknown'
    year: str = str(time.localtime().tm_year)
    month: str = str(time.localtime().tm_mon)
    day: str = str(time.localtime().tm_mday)
    hour: str = str(time.localtime().tm_hour)
    minute: str = str(time.localtime().tm_min)
    second: str = str(time.localtime().tm_sec)
    check_time: str = year + month + day + hour + minute
    if len(second) == 1:
        check_time += '0' + second
    else:
        check_time += second
    db.update_one({'face_id': face_id_encoded}, {
                  '$push': {'login_time': check_time}})
    return {'name': user['name'], 'id': user['id']}


@app.route('/addUser')
def add_user():
    name: str = request.args.get('name')
    face_id: str = request.args.get('face_id')
    userID: int = db.count_documents({}) + 1
    user: User = User(id=userID, name=name, face_id=face_id, login_time=[])
    db.insert_one(user.to_mapping())
    return 'success'


@app.route('/deleteUser')
def delete_user():
    id: str = request.args.get('id')
    result: DeleteResult = db.delete_one({'id': int(id)})
    if result.deleted_count == 0:
        return 'not found'
    return 'success'


@app.route('/getAllUser')
def get_all_user():
    users: Cursor[Mapping[str, Any] | Any] = db.find()
    return {'users': [User(id=user['id'], name=user['name'], face_id=user['face_id'],
                           login_time=[check_time for check_time in user['login_time']]).to_mapping()
                      for user in users]}


@app.route('/changeUserInfo')
def change_user_info():
    user_id: str = request.args.get('id')
    name: str = request.args.get('name')
    face_id: str = request.args.get('face_id')
    result: UpdateResult = db.update_one({'id': int(user_id)}, {'$set': {
        'name': name,
        'face_id': face_id
    }})
    if result.modified_count == 0:
        return 'not found'
    return 'success'


@app.route('/getCheckInfo')
def get_check_info():
    start_time: str = request.args.get('start_time')
    end_time: str = request.args.get('end_time')
    result = {}
    users: Cursor[Mapping[str, Any] | Any] = db.find()
    for user in users:
        for check_time in user['login_time']:
            if int(start_time) <= int(check_time) <= int(end_time):
                data = check_time[:4]+"."+check_time[4: 6]+"."+check_time[6: 8] + \
                    " "+check_time[8: 10]+":" + \
                    check_time[10: 12]+":"+check_time[12: 14]
                if user['name'] not in result:
                    result[user['name']] = [data]
                else:
                    result[user['name']].append(data)
    return result


def face_id_decoding(face_id: str) -> numpy.ndarray:
    code = face_id.split(',')
    return numpy.array(code, dtype='float64')


if __name__ == '__main__':
    app.run()
