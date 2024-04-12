from django import forms
from django.contrib.auth import authenticate

from accounts.models import CustomUser
from course.models import Course
from sales.models import Package, EmailTemplates, PAYMENT_DONE,DemoClasses, LiveCourses
from sales.forms import CLASS_STATUS
from pagedown.widgets import PagedownWidget
from s3direct.widgets import S3DirectWidget



class LoginForm(forms.Form):
    email = forms.EmailField(label=(u'User-Email'), widget=forms.TextInput(attrs={'placeholder': 'Email','required':None,'data-parsley-errors-container':'#c-error-username','data-parsley-error-message':'Email is required'}))
    password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False,attrs={'placeholder': 'Password','required':'','data-parsley-errors-container':'#c-error-password','data-parsley-error-message':'Password is required'}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, email Id not registered or user is not active.")
        if user:
            if not user.has_teacherpanel_rights():
                raise forms.ValidationError("Sorry, email ID doesn't have teacher rights.")
            if not user.is_staff and user.is_instructor:
                # changes: teacher-customuser
                # teacher = Teachers.objects.get(email=email)
                teacher = Teachers.objects.get(custom_user_id=user.id)
                print teacher.status.name.lower()
                #if teacher.status.name.lower() != 'active' or teacher.status.name.lower() != 'on leave':
                #    raise forms.ValidationError("Sorry, trainer is not active.")
        return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        return user
