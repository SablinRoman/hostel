from hostel.models import Student
from hostel.models import Room
from datetime import datetime


class Statistics:

    all_count = Student.objects.all().count()
    male_places = Student.objects.filter(bed_status__icontains='мужское').count()
    female_places = Student.objects.filter(bed_status__icontains='женское').count()
    empty_places = Student.objects.filter(bed_status__icontains='пусто').count()
    save_places = Student.objects.filter(bed_status__icontains='занято').count()
    num_of_residents = all_count - male_places - female_places - empty_places - save_places
    all_free_places = male_places + female_places + empty_places + save_places
    flurog_cert = num_of_residents - Student.objects.filter(fluorography__contains='+').count()
    pedicul_cert = num_of_residents - Student.objects.filter(pediculosis__contains='+').count()


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


    def form_studies_sort():
        form_dict = {}
        students = Student.objects.all()

        for student in students:
            if student.form_studies in form_dict:
                form_dict[student.form_studies] += 1
            else:
                form_dict[student.form_studies] = 1
        return form_dict


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
