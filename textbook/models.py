from __future__ import unicode_literals

from django.db import models

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

    class Meta:
        unique_together = ('section', 'course', 'department')


class BookSection(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('book', 'section')


