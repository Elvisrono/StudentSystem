import os
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import StudentSignUpForm, LoginForm, StudentForm, InvitationForm
from django.contrib.auth.decorators import login_required
from .models import Student, Invitation, Course
from .forms import CourseForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import render, redirect



# Create your views here.
def index(request):
    return render(request, 'index.html')

def gallery(request):
    return render(request, 'gallery.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send email
        subject = f"New Message from {name}"
        body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        recipient_email = 'elvisrono90@gmail.com'  # Replace with your recipient email address

        try:
            send_mail(
                subject,
                body,
                'elvisrono90@gmail.com',  # Sender's email address
                [recipient_email],
                fail_silently=False,
            )
            messages.success(request, "Message sent successfully!")  # Success message
        except Exception as e:
            messages.error(request, f"Failed to send message: {str(e)}")  # Error message

        return redirect('contact')  # Redirect to the same page to show message after submission

    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def user_login(request):
    role = request.GET.get('role')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser or user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'student':
                return redirect('student_dashboard')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'role': role})

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Save the new user
            messages.success(request, 'Signup successful! Please log in.')
            return redirect('login')
    else:
        form = StudentSignUpForm()
    return render(request, 'studentpages/student_signup.html', {'form': form})


@login_required
def student_dashboard(request):
    invitations = Invitation.objects.filter(student=request.user)
    enrolled_courses = request.user.courses.all()

    return render(request, 'studentpages/student_dashboard.html', {
        'invitations': invitations,
        'enrolled_courses': enrolled_courses
    })

@login_required
def admin_dashboard(request):
    student_count = Student.objects.count()
    admin_details = {
        'username': request.user.username,
        'email': request.user.email,
        'role': 'admin'
    }
    return render(request, 'adminpages/admin_dashboard.html', {'studentcount': student_count, 'admin': admin_details})

@login_required
def student_list(request):
    if not request.user.is_superuser and request.user.role != 'admin':
        return redirect('index')
    students = Student.objects.filter(role='student')

    return render(request, 'adminpages/admin_student_list.html', {'students': students})

@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'studentpages/student_detail.html', {'student': student})

@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.set_password(form.cleaned_data['password'])  # Hash the password
            student.role = 'student'  # Explicit role assignment
            student.save()
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'adminpages/add_student.html', {'form': form})

@login_required
def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            if 'image' in request.FILES:
                file_name = os.path.basename(request.FILES['image'])
                messages.success(request, f'Student updated succesfully {file_name}) uploaded. ')
            else:
                messages.success(request, 'student updated successfully')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'adminpages/update_student.html', {'form': form})
@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'adminpages/confirm_delete.html', {'student': student})



@login_required
def create_course(request):
    if not request.user.is_superuser and request.user.role != 'admin':
        return redirect('course_list')  # Redirect if user is not admin

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new course
            return redirect('course_list')  # Redirect to the course list after creating a course
    else:
        form = CourseForm()

    return render(request, 'adminpages/create_course.html', {'form': form})

@login_required
def course_list(request):
    courses = Course.objects.all()  # Retrieve all courses from the database
    return render(request, 'course_list.html', {'courses': courses})

@login_required
def student_courses(request):
    student = request.user
    accepted_courses = student.courses.all()
    return render(request, 'studentpages/student_courses.html', {'courses': accepted_courses})




@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.is_superuser or request.user.role == 'admin':
        base_template = 'adminpages/adminbase.html'
    elif request.user.role == 'student':
        if request.user.courses.filter(id=course_id).exists():
            base_template = 'studentpages/studentbase.html'
        else:
            # Deny access if the invitation hasn't been accepted
            messages.error(request, 'You must accept the invitation to view this course.')
            return redirect('student_invites')
    else:
        messages.error(request, 'Access denied.')
        return redirect('course_list')
    return render(request, 'course_detail.html', {'course': course, 'base_template': base_template})


@login_required
def update_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')  # Redirect back to the course list
    else:
        form = CourseForm(instance=course)
    return render(request, 'adminpages/update_course.html', {'form': form, 'course': course})


@login_required
def student_invites(request):
    invitations = Invitation.objects.filter(student=request.user, accepted=False)
    return render(request, 'student_invites.html', {'invitations': invitations})

@login_required
def send_invitation(request, course_id):
    # Fetch the selected course
    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']  # The student selected in the form
            # Create an invitation for the selected student
            Invitation.objects.create(course=course, student=student)
            messages.success(request, 'Invitation sent successfully!')
            return redirect('course_list')
    else:
        form = InvitationForm()  # Empty form for GET request

    return render(request, 'adminpages/send_invitation.html', {'course': course, 'form': form})


@login_required
def view_invitation(request):
    if not request.user.is_superuser and request.user.role != 'admin':
        return redirect('course_list')  # Redirect non-admins to course list or another page

    invitations = Invitation.objects.all()

    return render(request, 'adminpages/admin_view_invitation.html', {'invitations': invitations})



@login_required
def accept_invitation(request, invitation_id):
    invitation = Invitation.objects.get(id=invitation_id)
    if invitation.student == request.user and not invitation.accepted:
        invitation.accepted = True
        invitation.save()
        request.user.courses.add(invitation.course)  # Add the course to the student's courses
        messages.success(request, f'You have successfully enrolled in {invitation.course.title}!')
    else:
        messages.error(request, 'Invalid invitation or already accepted.')

    return redirect('student_invites')


