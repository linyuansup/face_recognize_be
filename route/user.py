from flask import Blueprint, request
from pkg.dao.user import UserDao

user = Blueprint('user', __name__, url_prefix='/user')
dao = UserDao()


@user.route('/login')
def login():
    all_user = dao.find_all()
    fid = request.args.get('fid')
    for user in all_user:
        if


@user.route('/getCheckInfo')
def getCheckInfo():
    return 'getCheckInfo'


@user.route('/add')
def addUser():
    return 'addUser'


@user.route('/delete')
def deleteUser():
    return 'deleteUser'
