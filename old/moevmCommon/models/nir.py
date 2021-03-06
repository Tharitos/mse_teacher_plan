# -*- coding: utf-8 -*-
from django.db import models
from moevmCommon.models.userProfile import UserProfile

class NIR(models.Model):
    user = models.ForeignKey(UserProfile)
    workName = models.CharField(max_length=250)
    startDate = models.DateField(null=True)
    finishDate = models.DateField(null=True)
    role = models.CharField(
        max_length=100,
        null=True
    )
    organisation = models.CharField(
        max_length=250,
        null=True
    )
    cipher = models.CharField(
        max_length=100,
        null=True
    )
    year = models.CharField(
        max_length=4,
        null=False
    )
    @staticmethod
    def create(**params):
        nir = NIR.objects.create(
            user=params.get('user'),
            workName=params.get('workName'),
            startDate=params.get('startDate'),
            finishDate=params.get('finishDate'),
            role=params.get('role'),
            organisation=params.get('organisation'),
            cipher=params.get('cipher'),
            year=params.get('year')
        )
        nir.save()
        return nir
    def __str__(self):
        return self.workName + " " + self.organisation + " " + self.cipher
