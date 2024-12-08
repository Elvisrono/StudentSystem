from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Student(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    course_choices = [
        ('Web_dev', 'Web Development'),
        ('Android_dev', 'Android Development'),
        ('Fullstack', 'Fullstack Engineering'),
    ]
    course = models.CharField(max_length=20, choices=course_choices, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    date_of_birth = models.DateField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    courses = models.ManyToManyField('Course', related_name='students', blank=True)
    image = models.ImageField(upload_to='student_images/', blank=True)

    def __str__(self):
        return self.username


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Invitation(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitations')
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invitation to {self.student.username} for {self.course.title}"

    def accept_invitation(self):
        """Accept the invitation and add the course to the student's courses."""
        self.accepted = True
        self.save()
        self.student.courses.add(self.course)  # Add the course to the student's enrolled courses

