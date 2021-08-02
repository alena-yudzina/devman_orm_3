from datacenter.models import Schoolkid, Lesson, Mark, Commendation, Chastisement
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import random


def get_schoolkid(schoolkid_name):
    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except ObjectDoesNotExist:
        print('Такого ученика нет')
    except MultipleObjectsReturned:
        print('По такому имени найдено несколько совпадений. Конкретизируйте запрос')


def fix_marks(schoolkid_name):

    schoolkid = get_schoolkid(schoolkid_name)
    if not schoolkid:
        return

    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    for mark in bad_marks:
        mark.points = 5
        mark.save()

    print('Оценки исправлены на 5')


def remove_chastisements(schoolkid_name):
    
    schoolkid = get_schoolkid(schoolkid_name)
    if not schoolkid:
        return

    comments = Chastisement.objects.filter(schoolkid=schoolkid)
    comments.delete()

    print('Комментарии удалены')


def create_commendation(schoolkid_name, subject):

    schoolkid = get_schoolkid(schoolkid_name)
    if not schoolkid:
        return

    commendations = [
        'Молодец!',
        'Ты сегодня прыгнул выше головы!',
        'С каждым разом у тебя получается всё лучше!',
        'Ты многое сделал, я это вижу!',
        'Хвалю',
    ]

    last_lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study, 
        group_letter=schoolkid.group_letter, 
        subject__title__contains=subject,
        ).order_by('-date').first()

    Commendation.objects.create(
        text=random.choice(commendations),
        created=last_lesson.date,
        schoolkid=schoolkid,
        subject=last_lesson.subject,
        teacher=last_lesson.teacher
        )

    print('Похвала добавлена')
