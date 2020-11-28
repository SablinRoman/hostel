import os
import sys
import logging

import django
import openpyxl

wb = openpyxl.load_workbook('./Baza.xlsx')
SHEET = wb['Проживающие']

project_dir = "/home/firtsdjango/app/engine/engine/"  # Путь до файла settings
sys.path.append(project_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'engine.settings')  # Добавление переменной окуружения
django.setup()
from hostel.models import Student  # Примечание: импорт не работает, если находться на верху
from hostel.models import Room  # Примечание: импорт не работает, если находться на верху


STATUS_LIST = ('Мужское', 'Женское', 'Пусто', 'Занято')


def get_cell_data(row, column):
    data = SHEET.cell(row=row, column=column).value
    return data


def import_rooms():
    # TODO delete input
    i = int(input("Start row ="))
    logging.info('Importing rooms...')

    while get_cell_data(i, 1) is not None:
        cell_data = get_cell_data(i, 1)

        if not Room.objects.filter(room_numb=cell_data):
            hostel = Room()
            hostel.room_numb = cell_data
            hostel.save()
            logging.info(f'Room {cell_data} was imported...')

        i += 1


def check_to_empty(row, column):
    data = get_cell_data(row, column)
    if data.capitalize() in STATUS_LIST:
        return


# TODO Обязательно добавить нормализацию данных
def import_students_data():
    # TODO delete input
    i = int(input("Start row ="))

    while get_cell_data(i, 1) is not None:
        student = Student()
        student.room = Room.objects.get(room_numb=get_cell_data(i, 1))

        if check_to_empty(i, 2):
            student.name = ''
            student.bed_status = get_cell_data(i, 2)
        else:
            student.name = get_cell_data(i, 2)
            student.bed_status = get_cell_data(i, 6)

        student.faculty = get_cell_data(i, 3)
        student.form_studies = get_cell_data(i, 4)
        student.group = get_cell_data(i, 5)
        student.sex = get_cell_data(i, 6)
        student.mobile_number = get_cell_data(i, 7)
        student.notation = get_cell_data(i, 8)

        if get_cell_data(i, 9) != '':
            student.fluorography = True
        else:
            student.fluorography = False

        if get_cell_data(i, 10) != '':
            student.pediculosis = True
        else:
            student.pediculosis = False

        student.contract_number = get_cell_data(i, 11)
        student.agreement_date = get_cell_data(i, 12)
        student.registration = get_cell_data(i, 13)
        student.citizenship = get_cell_data(i, 14)
        student.date_of_birthday = get_cell_data(i, 15)
        student.place_of_birthday = get_cell_data(i, 16)
        student.document_number = get_cell_data(i, 17)
        student.authority = get_cell_data(i, 18)
        student.date_of_issue = get_cell_data(i, 19)
        student.save()

        logging.info(f'{i} room={student.room} {student.name}')

        i += 1
    logging.info('Import completed')
