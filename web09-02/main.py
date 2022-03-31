from datetime import datetime

from sqlalchemy import text, or_, and_
from sqlalchemy.orm import joinedload

from connect_db import session
from models import Teacher, Student, TeacherStudent


def get_students():
    students = session.query(Student).options(joinedload('teachers'), joinedload('contacts')).all()
    for s in students:
        print('-----------------')
        print(f"{s.id}: {s.first_name} {s.last_name}")
        for t in s.teachers:
            print(f"Teacher {t.id}: {t.first_name} {t.last_name} - {t.email}")
        print('-----------------')
        if len(list(s.contacts)) == 0:
            print('Not contacts for students')
            continue
        for c in s.contacts:
            print(f"Contact person {c.id}: {c.first_name} {c.last_name} - {c.email}")
        print('=================')


def get_teachers():
    teachers = session.query(Teacher).options(joinedload('students')).filter(
        and_(
            Teacher.start_work > datetime(year=2016, month=1, day=1),
            Teacher.start_work < datetime(year=2020, month=1, day=1)
        )
    )
    # filter(text('teachers.id = :id or teachers.id = :newid')).params(id="3", newid="1")
    for t in teachers:
        print('-----------------')
        print(f"{t.id}: {t.first_name} {t.last_name}")
        if len(list(t.students)) == 0:
            print('Not students')
            continue
        for s in t.students:
            print(f"Student {s.id}: {s.first_name} {s.last_name} - {s.email}")
        print('-----------------')


if __name__ == '__main__':
    get_students()
    # get_teachers()

