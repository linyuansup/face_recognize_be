from typing import List

from pymongo.results import InsertOneResult

from pkg.dao import db
from pkg.model.user import User


class UserDao:
    def __init__(self):
        self.user = db['user']

    def insert(self, user: User) -> InsertOneResult:
        insert_id = self.user.insert_one(user.to_mapping())
        return insert_id

    def delete(self, uid: int) -> None:
        self.user.delete_one({'id': uid})

    def find(self, uid: int) -> User:
        user = self.user.find_one({'id': uid})
        return User(id=user['id'], name=user['name'], fid=user['fid'], admin=user['admin'])

    def update(self, user: User) -> None:
        self.user.update_one({'id': user.id}, {'$set': user.to_mapping()})

    def find_all(self) -> List[User]:
        users = self.user.find()
        return [User(id=user['id'], name=user['name'], fid=user['fid'], admin=user['admin']) for user in users]