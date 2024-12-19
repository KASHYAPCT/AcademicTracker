from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser): 
    is_fac= models.BooleanField(default=False)
    is_stud = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=12,null=True,blank=True)
    dob=models.DateField(null=True,blank=True)
    place= models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=30,null=True,blank=True)
    image = models.ImageField(upload_to="user/",null=True,blank=True)
    semester=models.CharField(max_length=50,null=True,blank=True)
    address=models.CharField(max_length=150,null=True,blank=True)
    
    
    
class Timetable(models.Model):
    file=models.ImageField(upload_to='table/',null=True,blank=True)
    sem=models.CharField(max_length=50,null=True,blank=True)

    
class Notifications(models.Model):
    description=models.CharField(max_length=150,null=True,blank=True)


class StudentResult(models.Model):
    # Student Information
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="results",default='')
    registration_number = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    programme = models.CharField(max_length=100, default="Master of Computer Applications")
    semester = models.CharField(max_length=50)
    college = models.CharField(max_length=255)

    # Course Details
    course_code = models.CharField(max_length=10)
    course_title = models.CharField(max_length=255)
    credits = models.FloatField()
    ca_marks = models.IntegerField("Continuous Assessment Marks")
    ese_marks = models.IntegerField("End Semester Evaluation Marks")
    total_marks = models.IntegerField()
    grade_point = models.FloatField()
    credit_point = models.FloatField()
    result = models.CharField(max_length=1, choices=[("P", "Pass"), ("F", "Fail")])

    # Additional Information
    sgpa = models.FloatField(null=True, blank=True)
    grade = models.CharField(max_length=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[("Passed", "Passed"), ("Failed", "Failed")])

    def __str__(self):
        return f"{self.name} - {self.course_code} ({self.result})"
