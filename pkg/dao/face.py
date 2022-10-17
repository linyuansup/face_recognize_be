from typing import List

from pymongo.results import InsertOneResult

from pkg.dao import db
from pkg.model.face import Face


class FaceDao:
    def __init__(self):
        self.face = db['face']

    def insert(self, face: Face) -> InsertOneResult:
        insert_id = self.face.insert_one(face.to_mapping())
        return insert_id

    def delete(self, fid: int) -> None:
        self.face.delete_one({'fid': fid})

    def find(self, fid: int) -> Face:
        face = self.face.find_one({'fid': fid})
        return Face(fid=face['fid'], long_id=face['long_id'])

    def update(self, face: Face) -> None:
        self.face.update_one({'fid': face.fid}, {'$set': face.to_mapping()})

    def find_all(self) -> List[Face]:
        faces = self.face.find()
        return [Face(fid=face['fid'], long_id=face['long_id']) for face in faces]
