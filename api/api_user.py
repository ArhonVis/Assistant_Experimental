import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[0].absolute()))

import api_timetable
from api_db import Client
from api_exception import UserException

UserTypeIncorrect = UserException(code=3030, message='The user type is incorrect')
UserGroupIncorrect = UserException(code=3030, message='The user group is incorrect')
TeacherNotFound = UserException(code=3030, message='Teacher not found')
UserNotFound = UserException(code=6060, message='User not found')


Group = api_timetable.Group()
Teacher = api_timetable.Teacher()


class User:
    def __init__(self):
        self.UserTypeStudent = 0
        self.UserTypeTeacher = 1
        self.UserTypeAll = [0, 1]
        self.client = Client()

    def set(self, user_id: int, username: str, user_type: int, group: str, teacher: str) -> None:
        if user_type and user_type not in self.UserTypeAll:
            raise UserTypeIncorrect

        if group and user_type == self.UserTypeStudent:
            group = Group.get_by_name(group)
            if not group:
                raise UserGroupIncorrect

        if teacher and user_type == self.UserTypeTeacher:
            teacher = Teacher.get_by_name(teacher)
            if not teacher:
                raise TeacherNotFound

        self.client.get_connect().users.insert_one({
            'user_id': user_id,
            'username': username,
            'user_type': user_type,
            'group': group,
            'teacher_id': teacher
        })

    def get_by_id(self, user_id: int) -> dict:
        user = self.client.get_connect().users.find_one({'user_id': user_id})
        if user:
            return user
        else:
            raise UserNotFound
