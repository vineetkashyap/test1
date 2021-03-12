from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Recruiter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200,null=True)
    company_profile = models.CharField(max_length=1000,null=True)
    city = models.CharField(max_length=100,null=True)
    web_address =models.URLField( max_length=200,null=True) 
    image = models.FileField(null=True)
    user_type = models.CharField(null=True,max_length=50)
    status = models.CharField(max_length=50,null=True)
    def __str__(self):
        return self.user.username
    

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15,null=True)
    image = models.FileField(null=True)
    gender = models.CharField(null=True, max_length=50) 
    user_type = models.CharField(null=True,max_length=50)
    
    

class Job(models.Model):
    recruiter =models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=50)
    job_type = models.CharField(max_length=50)
    job_location = models.CharField(max_length=50)
    experiance_qualification = models.CharField(max_length=1000)
    skill= models.CharField(max_length=1000)
    discription = models.CharField(max_length=1000)
    vacancy =models.CharField(max_length=50)
    creation_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    def __str__(self):
        return self.job_title

class JobApply(models.Model):
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    first_name= models.CharField( max_length=100,null=True)
    last_name= models.CharField( max_length=100,null=True)
    email =models.EmailField(max_length=254,null=True)
    adddress = models.CharField(max_length=500)
    zipcode = models.CharField(max_length=20)
    mobile = models.CharField(max_length=15)
    cv = models.FileField(null=True)
   
   



