from django.contrib import admin
from django.urls import path

from student import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('about/', views.about, name='about'),
    path('signup/', views.student_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_students/', views.student_list, name='student_list'),
    path('admin-students/add/', views.add_student, name='add_student'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/update/', views.update_course, name='update_course'),
    path('courses/create/', views.create_course, name='create_course'),
    # Remove the duplicate URL pattern here
    path('student/courses/', views.student_courses, name='student_courses'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('send-invitation/<int:course_id>/', views.send_invitation, name='send_invitation'),
    path('invitations/', views.view_invitation, name='view_invitations'),
    path('invitations/accept/<int:invitation_id>/', views.accept_invitation, name='accept_invitation'),
    path('students/', views.student_list, name='student_list'),
    path('student/<int:pk>/', views.student_detail, name='student_detail'),  # View details
    path('student/<int:pk>/update/', views.update_student, name='update_student'),  # Update student
    path('student/<int:pk>/delete/', views.delete_student, name='delete_student'),
    path('invites/', views.student_invites, name='student_invites'),
    path('accept_invite/<int:invitation_id>/', views.accept_invitation, name='accept_invitation'),

]
