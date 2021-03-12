from django.shortcuts import render,redirect,HttpResponseRedirect
from django.views import View
from django.contrib.auth.models import User
from .models import Student,Recruiter,Job,JobApply
from django.contrib.auth import authenticate,login,logout
from datetime import date
from django.views.generic.list import ListView
from django.db.models import Q
#email import
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

 # Create your views here.
def index(request):
    job = Job.objects.all()[:5]
    return render(request,'index.html',{'jobs':job})

       
    

class StudentRegistrationView(View):
    def get(self,request):
        error = "no"
        return render(request,'student/student_registration.html',{'data':error})
    def post(self,request):
        error =""
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        image = request.FILES['image']
        password = request.POST['password']
        email = request.POST['email']
        mobile = request.POST['mobile']
        gender = request.POST.get('gender',False)  
        try :
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=email,password=password)
            Student.objects.create(user =user,mobile=mobile,image=image,gender=gender,user_type="student")
            error = "no"
        except:
            error ="yes"
        data = {'error':error}
        return render(request,'student/student_registration.html',data)

# -------------------------this is recruiter signup form----------------------------
class RecruiterRegistrationView(View):
    def get(self,request):
        error = "no"
        return render(request,'recruiter/recruiter_signup.html',{'data':error})
    def post(self,request):
        error =""
        company_name = request.POST['company_name']
        company_profile = request.POST['company_profile']
        password = request.POST['password']
        image = request.FILES['image']
        city =  request.POST['city']
        web_address = request.POST['web_address']
        email = request.POST['email']
      
        
        try :
            user = User.objects.create_user(username=email,password=password)
            Recruiter.objects.create(user =user,company_name=company_name,company_profile=company_profile,image=image,web_address=web_address,city=city,user_type="recruiter",status="pending")
            error = "no"
        except:
            error ="yes"
        data = {'error':error}
        return render(request,'recruiter/recruiter_signup.html',data)


# --------------------------------this is job posting  form----------------------------

class  JobPostingView(View):
    def get(self,request):
        error = "no"
        return render(request,'recruiter/job_post.html',{'data':error})
    def post(self,request):
        error =""
        job_title = request.POST['job_title']
        job_type = request.POST['job_type']
        job_location = request.POST['job_location']
        experiance_qualification = request.POST['experiance_qualification']
        skill = request.POST['skill']
        discription = request.POST['discription']
        vacancy = request.POST['vacancy']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        user  =request.user
        recruiter = Recruiter.objects.get(user=user)
        try :
            
            Job.objects.create(recruiter =recruiter,job_title=job_title,job_type=job_type,job_location=job_location,experiance_qualification=experiance_qualification,skill=skill,discription=discription,vacancy=vacancy,creation_date=date.today(),start_date=start_date,end_date=end_date,)
            error = "no"
        except:
            error ="yes"
        data = {'error':error}
        return redirect('recruiter_dashboard')
        return render(request,'recruiter/job_post.html',data)

        

# --------------------this is student or applicant  login form view ------------------------

class UserLoginView(View):
    def get(self,request):
        error  ="no"
        return render(request,'student/student_login.html',{'data':error})
    def post(self,request):
        error  =""
        username =request.POST['email']
        password =request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            try :
                user1 = Student.objects.get(user=user)
                if user1.user_type == "student":
                    login(request,user)
                    error  ="no"
                    student = Student.objects.get(user=request.user)
                    name = student.user.first_name
                    
                else :
                    error = "yes"
            except:
                error = "yes"
        else: 
            error = "yes"
        data  ={"error":error}
        
        
        
        return render(request,'student/student_login.html',data)

# --------------------this is recruiter  login form view ------------------------
class RecruiterLoginView(View):
    def get(self,request):
        error  ="no"
        return render(request,'recruiter/recruiter_login.html',{'data':error})
    def post(self,request):
        error  =""
        username =request.POST['email']
        password =request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            try :
                user1 = Recruiter.objects.get(user=user)
                if user1.user_type == "recruiter" and user1.status != "pending":
                    login(request,user)
                    error  ="no"
                else :
                    error = "yes"
            except:
                error = "yes"
        data  ={"error":error}
        return render(request,'recruiter/recruiter_login.html',data)

# --------------------this is user logout view ------------------------

class UserLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('index')

# --------------------this is recruiter logout view -------------------
class RecruiterLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('index')


# --------------------Update The Jobs-------------------

class UpdateJob(View):
    def get(self,request,id):
        error = "no"
        job  =Job.objects.get(id=id)
        context  ={'error':error,'job':job}
        return render(request,'recruiter/update_job.html',context)
    def post(self,request,id):
        job  =Job.objects.get(id=id)
        error =""
        job_title = request.POST['job_title']
        job_type = request.POST['job_type']
        job_location = request.POST['job_location']
        experiance_qualification = request.POST['experiance_qualification']
        skill = request.POST['skill']
        discription = request.POST['discription']
        vacancy = request.POST['vacancy']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        job.job_title=job_title
        job.job_type=job_type
        job.job_location=job_location
        job.experiance_qualification=experiance_qualification
        job.job_location=job_location
        job.skill=skill
        job.discription=discription
        job.vacancy=vacancy
        job.job_location=job_location
        user  =request.user
        recruiter = Recruiter.objects.get(user=user)
        try :
            job.save()
            error = "no"
        except:
            error ="yes"
        if start_date:
            try :
                job.start_date = start_date
                job.save()
            except:
                pass
        else:
            pass
        if end_date:
            try :
                job.end_date = end_date
                job.save()
            except:
                pass
        else:
            pass
        data = {'error':error}
        return redirect('recruiter_dashboard')
        return render(request,'update_job.html',data)



# --------------------Apply For The Job View-------------------

class JobApplyView(View):
    def get(self,request,id):
        if request.user.is_authenticated:
            job = Job.objects.get(id=id)
            return render(request,'student/apply.html',{'job':job})
        else :
            return redirect('student_login')
    def post(self,request,id):
       if request.user.is_authenticated:
            error =""
            first_name  =request.POST['first_name']
            last_name  =request.POST['last_name']
            email1  =request.POST['email']
            address  =request.POST['address']
            mobile  =request.POST['mobile']
            zipcode  =request.POST['zipcode']
            cv = request.FILES['cv']
            # import pdb ; pdb.set_trace()
            try:
                job =Job.objects.get(id=id)
                student = Student.objects.get(user=request.user)
                if JobApply.objects.get(job=job,student=student):
                    return HttpResponseRedirect('/student_dashboard/')
                elif not JobApply.objects.get(job=job,student=student):
                    JobApply.objects.create(job=job,student=student,first_name=first_name,last_name=last_name,email=email1,adddress=address,mobile=mobile,zipcode=zipcode,cv=cv)
                    error = "no"
            except:
                JobApply.objects.create(job=job,student=student,first_name=first_name,last_name=last_name,email=email1,adddress=address,mobile=mobile,zipcode=zipcode,cv=cv)
                job_apply =JobApply.objects.get(student=student,job=job)
                template = render_to_string('student_email.html',{'job':job_apply})
                email = EmailMessage(
                    'Thanks for Applying',
                    template,
                    settings.EMAIL_HOST_USER,
                    [email1],
                )
                email.fail_silently=False
                email.send()
                template = render_to_string('recruiter_email.html',{'job':job_apply})
                email = EmailMessage(
                    'Thanks for Applying',
                    template,
                    settings.EMAIL_HOST_USER,
                    [job_apply.job.recruiter.user.username],
                )
                email.fail_silently=False

                email.send()
                
                error = "no"
            data = {'error':error}
            return redirect('student_dashboard')
       else : 
            return redirect('student_login')

# --------------------Filter By  Specific Recruiter-------------------

def recruiter_posted_job_list(request):
    recruiter = Recruiter.objects.get(user=request.user)
    data = Job.objects.filter(recruiter=recruiter).order_by('-creation_date')[0]
    return render(request,'job_listing.html',{'data':data})


# -----------Filter By  Specific Recruiter For Job Application Of  Applicant--

def  recruiter_view_of_applicant(request):
    user = request.user
    recruiter  =Recruiter.objects.get(user=user)
    job1= Job.objects.get(recruiter=recruiter)
    job = JobApply.objects.filter(job=job1)
    return render(request,'recruiter/recruiter_dashboard.html',{'jobs':job})

# --------Filter By  Specific Student Or Applicant For Job Application Of  Applicant------

def  student_apply_list(request):
    user = request.user
    student  =Student.objects.get(user=user)
    data= Job.objects.filter(student=student)
    return render(request,'student_dashboard.html',{'data':data})

# ------------------------------- total jobs--------------------------
def total_job(request):
    job = Job.objects.all()
    return render(request,'job_listing.html',{'jobs':job})
def recruiter_total_job(request):
    job = Job.objects.all()
    d = "recruiter"
    return render(request,'recruiter/recruiter_total_job.html',{'jobs':job,'d':d})

def student_total_job(request):
    job = Job.objects.all()
    d = "student"
    return render(request,'student/student_total_job.html',{'jobs':job,'d':d})
#----------------------------------job detals-------------------------
def  job_detail(request,id):
    job=Job.objects.get(id=id)
    return render(request,"job_detail.html",{'job':job})

def recruiter_job_detail(request,id):
    job=Job.objects.get(id=id)
    return render(request,"recruiter_job_detail.html",{'job':job})

def  student_job_detail(request,id):
    job=Job.objects.get(id=id)
    return render(request,"student_job_detail.html",{'job':job})

def  recruiter_dashboard(request):
    recruiter = Recruiter.objects.get(user=request.user)
    job = Job.objects.filter(recruiter=recruiter)
    return render(request,'recruiter/recruiter_dashboard.html',{'jobs':job,'recruiter':recruiter})
def  student_dashboard(request):
    student = Student.objects.get(user=request.user)
    job = JobApply.objects.filter(student=student)
    return render(request,'student/student_dashboard.html',{'jobs':job,'student':student})

def student_index(request):
    d = "student"
    return render(request,'index.html',{'d':d})

def recruiter_index(request):
    d = "recruiter"
    return render(request,'index.html',{'d':d})

def delete_job(request,id):
    pass


def email_send(request):
        student =Student.objects.get(user=request.user)
        job=Job.objects.get(id=6)
        job_apply =JobApply.objects.get(student=student,job=job)
        template = render_to_string('student_email.html',{'job':job_apply})
        email = EmailMessage(
            'Thanks for Applying',
            template,
            settings.EMAIL_HOST_USER,
            [job_apply.email],
        )
        email.fail_silently=False
        email.send()
    
class SearchListView(ListView):
        model = Job
        template_name = 'search_result.html'
        context_object_name = 'jobs'
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            search_result = self.request.GET.get('search')
            context["jobs"] = Job.objects.filter(Q(job_title__icontains=search_result)|Q(discription__icontains=search_result))
            return context
        
class StudentSearchListView(ListView):
        model = Job
        template_name = 'student_search_result.html'
        context_object_name = 'jobs'
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            search_result = self.request.GET.get('search')
            context["jobs"] = Job.objects.filter(Q(job_title__icontains=search_result)|Q(discription__icontains=search_result))
            return context
        
        
          
