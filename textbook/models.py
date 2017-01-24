from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.


class Book(models.Model):
    name = models.CharField(max_length=200)
    isbn = models.CharField(max_length=50, unique=True)
    author = models.CharField(max_length=100, null=True)


class Section(models.Model):
    section = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    professor = models.CharField(max_length=100, null=True)

    def __repr__(self):
        return '{} - {}, Section {} ({})'.format(self.department, self.course, self.section, self.professor)

    class Meta:
        unique_together = ('section', 'course', 'department')


class BookSection(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('book', 'section')


class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    unit_price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)

    def clean(self):
        if self.unit_price < 0:
            raise ValidationError("Unit price must be non-negative")

        if self.quantity < 0:
            raise ValidationError("Quantity must be non-negative")

    class Meta:
        unique_together = ('book', 'user')



