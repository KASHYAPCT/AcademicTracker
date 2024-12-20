# Generated by Django 5.1.3 on 2024-12-20 09:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0028_delete_studentresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_number', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('programme', models.CharField(default='Master of Computer Applications', max_length=100)),
                ('semester', models.CharField(max_length=50)),
                ('college', models.CharField(max_length=255)),
                ('course_code', models.CharField(max_length=10)),
                ('course_title', models.CharField(max_length=255)),
                ('max_mark', models.IntegerField()),
                ('ca_marks', models.IntegerField(verbose_name='Continuous Assessment Marks')),
                ('ese_marks', models.IntegerField(verbose_name='End Semester Evaluation Marks')),
                ('total_marks', models.IntegerField()),
                ('grade_point', models.FloatField()),
                ('grade_sub', models.CharField(blank=True, max_length=3, null=True)),
                ('result', models.CharField(choices=[('P', 'Pass'), ('F', 'Fail')], max_length=1)),
                ('sgpa', models.FloatField(blank=True, null=True)),
                ('grade', models.CharField(blank=True, max_length=2, null=True)),
                ('status', models.CharField(choices=[('Passed', 'Passed'), ('Failed', 'Failed')], max_length=20)),
                ('student', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='results', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]