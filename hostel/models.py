import logging
import datetime

from django.db import models
from django.db import connection
from django.shortcuts import reverse
from simple_history.models import HistoricalRecords


class Student(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    FORM_STUDIES_CHOICES = (
        ('БЮДЖЕТ', 'Бюджет'),
        ('ПВЗ', 'ПВЗ')
    )

    SEX_CHOICES = (
        ('М', 'Мужской'),
        ('Ж', 'Женский')
    )

    BED_STATUS_CHOICES = (
        ('Студент', 'Студент'),
        ('Заочник', 'Заочник'),
        ('Семейник', 'Семейник'),
        ('Расселитель', 'Расселитель'),
        ('Староста этажа', 'Староста этажа'),
        ('Актив этажа', 'Актив этажа'),
        ('Санитарная комиссия', 'Санитарная комиссия'),
        ('СООПР', 'СООПР'),
        ('Женское', 'Женское'),
        ('Мужское', 'Мужское'),
        ('Занято', 'Занято'),
        ('Пусто', 'Пусто'),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, db_index=True)
    bed_status = models.CharField(max_length=30, db_index=True, choices=BED_STATUS_CHOICES,
                                  blank=True, null=True)
    faculty = models.CharField(max_length=10, db_index=True, blank=True, null=True)
    form_studies = models.CharField(max_length=10, db_index=True, choices=FORM_STUDIES_CHOICES, blank=True, null=True)
    group = models.CharField(max_length=10, db_index=True, blank=True, null=True)
    sex = models.CharField(max_length=2, db_index=True, choices=SEX_CHOICES, blank=True, null=True)
    mobile_number = models.BigIntegerField(db_index=True, blank=True, null=True)
    fluorography = models.BooleanField(db_index=True, default=False)
    pediculosis = models.BooleanField(db_index=True, default=False)
    contract_number = models.CharField(max_length=15, db_index=True, blank=True, null=True)
    agreement_date = models.DateField(blank=True, null=True)
    registration = models.DateField(blank=True, null=True)
    citizenship = models.CharField(max_length=20, db_index=True, blank=True, null=True)
    date_of_birthday = models.DateField(blank=True, null=True)
    place_of_birthday = models.CharField(max_length=70, db_index=True, blank=True, null=True)
    document_number = models.CharField(max_length=20, db_index=True, blank=True, null=True)
    authority = models.CharField(max_length=100, blank=True, null=True)
    date_of_issue = models.DateField(blank=True, null=True)
    notation = models.TextField(db_index=True, blank=True, null=True)

    room = models.ForeignKey('Room', related_name='students', on_delete=models.CASCADE,
                             to_field='room_numb', blank=True, null=True)

    history = HistoricalRecords()

    def save_without_historical_record(self, *args, **kwargs):
        self.skip_history_when_saving = True
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving

        return ret

    def get_absolute_url(self):
        id = self.id
        return reverse('student_detail_url', kwargs={'id': id})

    def room_url(self):
        url = self.room
        return reverse('room_detail_url', kwargs={'room_det': url})

    def __str__(self):
        return self.name


class Room(models.Model):
    room_numb = models.IntegerField(db_index=True, blank=True, null=True, unique=True)


class CardsFilter(models.Model):
    all = models.BooleanField(blank=True, null=True)
    men = models.BooleanField(blank=True, null=True)
    women = models.BooleanField(blank=True, null=True)
    free = models.BooleanField(blank=True, null=True)
    busy = models.BooleanField(blank=True, null=True)


class StudentHistory:
    # TODO Закончить!
    def get_evicted_students(self):
        with connection.cursor() as cursor:
            cursor.execute('''
            SELECT room_id, history_date, history_change_reason, name
                FROM hostel_historicalstudent
                WHERE history_type = '-'
            ''')
            records = cursor.fetchall()

            return records


