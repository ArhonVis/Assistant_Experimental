import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[0].absolute()))

from api_db import Client


class BaseClass:
    def __init__(self):
        self.client = Client()


class Teacher(BaseClass):
    def set(self, teacher_id: int, teacher_name: str):
        self.client.get_connect().teacher.insert_one({'id': teacher_id, 'name': teacher_name})

    def get_by_name(self, name: str) -> dict or None:
        teacher = self.client.get_connect().teacher.find_one({'name': name})
        if isinstance(teacher, dict):
            return teacher
        else:
            return None


class Group(BaseClass):
    def set(self, group_id: int, group_name: str) -> None:
        self.client.group.get_connect().insert_one({'id': group_id, 'name': group_name})

    def get_by_name(self, group_name: str) -> dict:
        group = self.client.get_connect().group.find_one({'name': group_name})
        if isinstance(group, dict):
            return group


class Lesson(BaseClass):
    def set(self, group_id: int, day: str, time: str, name: str, location: str, teacher: str):
        self.client.get_connect().lessons.insert_one({
            'group_id': group_id,
            'day': day,
            'time': time,
            'name': name,
            'location': location,
            'teacher': teacher
        })

    def get_lessons_by_date(self, date1: str, date2: str):
        self.client.get_connect().lessons.find_all()
