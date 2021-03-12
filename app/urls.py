from django.urls import path
from app import views 
import pdb
urlpatterns = [
    path('',views.index,name="index"),

    path('student_registration/',views.StudentRegistrationView.as_view(),name="student_registration"),

    path('recruiter_registration/',views.RecruiterRegistrationView.as_view(),name="recruiter_registration"),

    path('job_post/',views.JobPostingView.as_view(),name="job_post"),

    path('student_login/',views.UserLoginView.as_view(),name="student_login"),
    path('recruiter_login/',views.RecruiterLoginView.as_view(),name="recruiter_login"),

    path('student_logout/',views.UserLogoutView.as_view(),name="student_logout"),
    path('recruiter_logout/',views.RecruiterLogoutView.as_view(),name="recruiter_logout"),

    path('update_job/<int:id>',views.UpdateJob.as_view(),name="update_job"),
    path('job_apply/<int:id>',views.JobApplyView.as_view(),name="job_apply"),

    path('post_list/',views.recruiter_posted_job_list,name="post_list"),
    path('applicant_list/',views.recruiter_view_of_applicant,name="applicant_list"),
    path('apply_list/',views.student_apply_list,name="apply_list"),

    path('total_job/',views.total_job,name="total_job"),
    
    path('recruiter_total_job/',views.recruiter_total_job,name="recruiter_total_job"),

    path('student_total_job/',views.student_total_job,name='student_total_job'),

    path('job_detail/<int:id>',views.job_detail,name='job_detail'),

    path('recruiter_job_detail/<int:id>',views.recruiter_job_detail,name="recruiter_job_detail"),

    path('student_job_detail/<int:id>',views.student_job_detail,name="student_job_detail"),

    path('recruiter_dashboard/',views.recruiter_dashboard,name="recruiter_dashboard"),
    path('student_dashboard/',views.student_dashboard,name="student_dashboard"),
    path('student_index',views.student_index,name='student_index'),
    path('recruiter_index',views.recruiter_index,name='recruiter_index'),

    path('delete_job/<int:id>',views.delete_job,name='delete_job'),
    path('search_result/',views.SearchListView.as_view(),name='search_result'),
    path('student_search_result/',views.StudentSearchListView.as_view(),name='student_search_result'),

      


]
