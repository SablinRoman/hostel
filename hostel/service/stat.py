import logging

from hostel.models import Student
from hostel.models import Room
from datetime import datetime
from django.db import OperationalError


class Statistics:

    def __init__(self):
        logging.info('Init statistics attributes...')

        self.all_count = None
        self.male_places = None
        self.female_places = None
        self.empty_places = None
        self.save_places = None
        self.number_of_residents = None
        self.all_free_places = None
        self.flurog_cert = None
        self.pedicul_cert = None
        self.countries = None
        self.faculty = None
        self.form_studies = None
        self.registration = None


    def CreateStatistic(self):
        logging.info('Create statistics...')

        try:
            all_count = Student.objects.all().count()
        except:
            raise OperationalError('DataBase was not fond! Use "make import_data"')

        all_count = Student.objects.all().count()
        male_places = Student.objects.filter(bed_status__icontains='мужское').count()
        female_places = Student.objects.filter(bed_status__icontains='женское').count()
        empty_places = Student.objects.filter(bed_status__icontains='пусто').count()
        save_places = Student.objects.filter(bed_status__icontains='занято').count()
        all_free_places = male_places + female_places + empty_places + save_places
        number_of_residents = all_count - male_places - female_places - empty_places - save_places

        self.all_count = all_count
        self.male_places = male_places
        self.female_places = female_places
        self.empty_places = empty_places
        self.save_places = save_places
        self.number_of_residents = number_of_residents
        self.all_free_places = all_free_places
        self.flurog_cert = number_of_residents - Student.objects.filter(fluorography__contains='+').count()
        self.pedicul_cert = number_of_residents - Student.objects.filter(pediculosis__contains='+').count()
        self.citizenship = self.citizenship_sort()
        self.faculty = self.faculty_sort()
        self.form_studies = self.form_studies_sort()
        self.registration = self.registration_sort()


        return self

    @staticmethod
    def citizenship_sort():
        country_dict = {}
        students = Student.objects.all()

        for student in students:
            if student.name == '':
                continue
            else:
                if student.citizenship in country_dict.keys():
                    country_dict[student.citizenship] += 1
                else:
                    country_dict[student.citizenship] = 1
        return country_dict

    @staticmethod
    def faculty_sort():
        faculty_dict = {}
        students = Student.objects.all()

        for student in students:
            if student.name == '':
                continue
            else:
                if student.faculty in faculty_dict.keys():
                    faculty_dict[student.faculty] += 1
                else:
                    faculty_dict[student.faculty] = 1
        return faculty_dict

    @staticmethod
    def form_studies_sort():
        form_dict = {}
        students = Student.objects.all()

        for student in students:
            if student.form_studies in form_dict:
                form_dict[student.form_studies] += 1
            else:
                form_dict[student.form_studies] = 1
        return form_dict

    @staticmethod
    def registration_sort():
        students = Student.objects.all()
        date_now = datetime.now().date()
        registration_dict = {'Просроченных регистраций': 0, 'Регистрация отсутствует': 0}

        for student in students:
            if student.registration == None:
                registration_dict['Регистрация отсутствует'] += 1
            elif student.registration < date_now:
                registration_dict['Просроченных регистраций'] += 1
        return registration_dict
