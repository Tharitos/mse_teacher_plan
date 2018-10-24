from mongoengine.document import Document
from mongoengine.fields import IntField, StringField, ReferenceField, DateTimeField
from app.models.default_params import *

type_conf_choices = ['Конкурс', 'Выставка', 'Конференция', 'Семинар']


class Conference(Document):
    user = ReferenceField('User')
    event_name = StringField(**default_string_params, verbose_name='Название события')
    level = StringField(**default_string_params, verbose_name='Уровень')
    place = StringField(**default_string_params, verbose_name='Место проведения')
    date = DateTimeField(**default_params, verbose_name='Дата проведения')
    type_conf = StringField(**default_string_params, choices=type_conf_choices,
                            verbose_name='Тип')
    meta = {'collection': 'Conferences'}