from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('',views.Login,name="Login"),
    path('home/',views.dashboard,name="dashboard"),
    path('logout/',views.logout_view, name='logout'),
    path('addstaff/',views.Addstaff,name="Addstaff"),
    path('staffdash/',views.staffdashboard, name='staffdashboard'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='admin_app/pages/password_change.html'), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='admin_app/pages/password_change_done.html'), name='password_change_done'),
    path('addstud/',views.add_stud,name="addstud"),
    path('stafflist/',views.staff_list,name="stafflist"),
    path('studlist/',views.stud_list,name="studlist"),
    path('editstaff/<int:faculty_id>/', views.edit_staff, name="editstaff"),
    path('deletefaculty/<int:faculty_id>/', views.faculty_delete, name='facultydelete'),
    path('deletestud/<int:stud_id>/',views.stud_delete,name="studdelete"),
    path('studdashboard/',views.studdashboard,name="studdashboard"),
    path('accounts/password_change/staff/', auth_views.PasswordChangeView.as_view(template_name='admin_app/pages/changestaffpass.html'), name='changestaffpass'),
    path('accounts/password_change/staffdone/', auth_views.PasswordChangeDoneView.as_view(template_name='admin_app/pages/changepassstffdone.html'), name='changepassstffdone'),
    path('accounts/password_change/stud/', auth_views.PasswordChangeView.as_view(template_name='admin_app/pages/changepassstud.html'), name='changestudpass'),
    path('accounts/password_change/studdone/', auth_views.PasswordChangeDoneView.as_view(template_name='admin_app/pages/changepassstuddone.html'), name='changepassstuddone'),
    path('addtimetable/',views.addtimetable,name="addtimetable"),
    path('timetableview/',views.timetable_view,name="timetableview"),
    path('timetablestaff/',views.timetablestaff_view,name="timetablestaff"),
    path('students/update/<int:student_id>/',views.update_student, name='updatestudent'),
    path('addnotification/',views.addnotification,name="addnotification"),
    path("view-notifications/", views.view_notifications, name="viewnotifications"),
    path('timetablestud/',views.timetablestud_view,name="timetablestud"),
    path("view-notificationsstud/", views.view_notificationsstud, name="viewnotificationsstud"),
    path('timetable/edit/<int:pk>/', views.edit_timetable, name='edittimetable'),
    path('timetable/delete/<int:pk>/',views.delete_timetable, name='deletetimetable'),
    path('addresult/',views.add_result,name="addresult"),
    path("results/",views.view_results, name="viewresult"),
     path("allresults/", views.view_all_results, name="allresults"),
     path('edit-result/<int:result_id>/', views.edit_result, name='editresult'),
     path("delete-result/<int:result_id>/",views.delete_result, name="deleteresult"),
    




]   
