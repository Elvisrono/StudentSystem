# forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Student, Course


class StudentSignUpForm(UserCreationForm):
    course_choices = [
        ('Web_dev', 'Web Development'),
        ('Android_dev', 'Android Development'),
        ('Fullstack', 'Fullstack Engineering'),
    ]
    course = forms.ChoiceField(choices=course_choices, required=True)

    class Meta:
        model = Student
        fields = ('username', 'first_name', 'last_name', 'email', 'contact_number', 'course', 'date_of_birth', 'password1', 'password2', 'image')

    def save(self, commit=True):
        user = super().save(commit=False)  # Call the parent save method
        user.is_student = True  # Ensure the student role is set
        if commit:
            user.save()  # Save the user object
        return user

class LoginForm(AuthenticationForm):
    pass
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['username', 'first_name', 'last_name', 'email', 'image', 'contact_number', 'course']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'date_of_birth': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}),
            'image': forms.ClearableFileInput(
                attrs={'class': 'form-control-file', 'accept': 'image/*', 'title': 'Upload your image here'}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course title'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter course description'}),
        }
User = get_user_model()

class InvitationForm(forms.Form):
    # ModelMultipleChoiceField allows selecting multiple students
    student = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='student'),  # Only fetch students
        widget=forms.CheckboxSelectMultiple,  # Display checkboxes
        required=True,
        label="Select Students to Invite"
    )


class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'image']