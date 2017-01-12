# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-11 04:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('isbn', models.CharField(max_length=50, unique=True)),
                ('author', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='textbook.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(max_length=200)),
                ('course', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=200)),
                ('professor', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='section',
            unique_together=set([('section', 'course', 'department')]),
        ),
        migrations.AddField(
            model_name='booksection',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='textbook.Section'),
        ),
        migrations.AlterUniqueTogether(
            name='booksection',
            unique_together=set([('book', 'section')]),
        ),
    ]
