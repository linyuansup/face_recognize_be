import time
from dataclasses import dataclass
from typing import List, MutableMapping, Any, Mapping

from flask import Flask, request
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.results import DeleteResult, UpdateResult

app: Flask = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
db: Collection[Mapping[str, Any] | Any] = MongoClient('mongodb://localhost:27017/')['test']['face_recognition']


@dataclass
class CheckTime:
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int

    def to_str(self) -> str:
        return f'{self.year}-{self.month}-{self.day} {self.hour}:{self.minute}:{self.second}'


def str_to_check_time(check_time: str) -> CheckTime:
    year, month, day, hour, minute, second = map(int, check_time.split('-'))
    return CheckTime(year, month, day, hour, minute, second)


@dataclass
class User:
    id: int
    name: str
    face_id: str
    login_time: List[CheckTime]

    def to_mapping(self) -> MutableMapping:
        return {
            'id': self.id,
            'name': self.name,
            'face_id': self.face_id,
            'login_time': [check_time.to_str() for check_time in self.login_time]
        }


@app.route('/checkFace')
def check_face():
    face_id = request.args.get('face_id')
    user = db.find_one({'face_id': face_id})
    if user is None:
        return 'fail'
    year: int = time.localtime().tm_year
    month: int = time.localtime().tm_mon
    day: int = time.localtime().tm_mday
    hour: int = time.localtime().tm_hour
    minute: int = time.localtime().tm_min
    second: int = time.localtime().tm_sec
    check_time: CheckTime = CheckTime(year, month, day, hour, minute, second)
    db.update_one({'face_id': face_id}, {'$push': {'login_time': check_time.to_str()}})
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
                           login_time=[str_to_check_time(check_time) for check_time in user['login_time']]).to_mapping()
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
    users: Cursor[Mapping[str, Any] | Any] = db.find({'login_time': {
        '$elemMatch': {
            '$gte': start_time,
            '$lte': end_time
        }
    }})
    return {
        'users': [User(**user).to_mapping() for user in users]
    }


if __name__ == '__main__':
    app.run()
