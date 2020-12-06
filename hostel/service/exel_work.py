import os
import sys
import logging

import django
import openpyxl

wb = openpyxl.load_workbook('./Baza.xlsx')
SHEET = wb['Проживающие']

# project_dir = "/home/roman/hostel/engine"  # Путь до файла settings
# sys.path.append(project_dir)
project_dir = '/home/roman/hostel'
sys.path.append(project_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'engine.settings')  # Добавление переменной окуружения
django.setup()

project_dir = '/home/roman/hostel'
sys.path.append(project_dir)

from hostel.models import Student  # Примечание: импорт не работает, если находться на верху
from hostel.models import Room  # Примечание: импорт не работает, если находться на верху

STATUS_LIST = ('Мужское', 'Женское', 'Пусто', 'Занято')


def get_cell_data(row, column):
    data = SHEET.cell(row=row, column=column).value
    return data


def import_rooms(row_number=2):
    # TODO delete input
    logging.info('Importing rooms...')

    while get_cell_data(row_number, 1) is not None:
        cell_data = get_cell_data(row_number, 1)

        if not Room.objects.filter(room_numb=cell_data):
            hostel = Room()
            hostel.room_numb = cell_data
            hostel.save()
            logging.info(f'Room {cell_data} was imported...')

        row_number += 1


def check_to_empty(row, column):
    data = get_cell_data(row, column)
    if data.capitalize() in STATUS_LIST:
        return True


# TODO Обязательно добавить нормализацию данных
def import_students_data(row_number=2):
    # TODO delete input
    if not row_number:
        row_number = int(input("Start row ="))

    while get_cell_data(row_number, 1) is not None:
        student = Student()
        student.room = Room.objects.get(room_numb=get_cell_data(row_number, 1))

        if check_to_empty(row_number, 2):
            student.name = ''
            student.bed_status = get_cell_data(row_number, 2)
        else:
            student.name = get_cell_data(row_number, 2)
            student.bed_status = get_cell_data(row_number, 6)

        student.faculty = get_cell_data(row_number, 3)
        student.form_studies = get_cell_data(row_number, 4)
        student.group = get_cell_data(row_number, 5)
        student.sex = get_cell_data(row_number, 6)
        student.mobile_number = get_cell_data(row_number, 7)
        student.notation = get_cell_data(row_number, 8)

        if get_cell_data(row_number, 9) != '':
            student.fluorography = True
        else:
            student.fluorography = False

        if get_cell_data(row_number, 10) != '':
            student.pediculosis = True
        else:
            student.pediculosis = False

        student.contract_number = get_cell_data(row_number, 11)
        student.agreement_date = get_cell_data(row_number, 12)
        student.registration = get_cell_data(row_number, 13)
        student.citizenship = get_cell_data(row_number, 14)
        student.date_of_birthday = get_cell_data(row_number, 15)
        student.place_of_birthday = get_cell_data(row_number, 16)
        student.document_number = get_cell_data(row_number, 17)
        student.authority = get_cell_data(row_number, 18)
        student.date_of_issue = get_cell_data(row_number, 19)
        student.save()

        logging.info(f'{row_number} room={student.room} {student.name}')

        row_number += 1
    logging.info('Import completed')


logging.getLogger().setLevel(logging.INFO)
if __name__ == '__main__':
    import_rooms()
    import_students_data()
