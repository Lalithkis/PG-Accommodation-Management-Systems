from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile, Room, RoomAllocation, Complaint

class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class UserRegistrationForm(BootstrapFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    full_name = forms.CharField(max_length=100)
    department = forms.CharField(max_length=100)
    year = forms.CharField(max_length=20)
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)
    guardian_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                department=self.cleaned_data['department'],
                year=self.cleaned_data['year'],
                phone_number=self.cleaned_data['phone_number'],
                address=self.cleaned_data['address'],
                guardian_name=self.cleaned_data['guardian_name']
            )
        return user

class RoomForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class ComplaintForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'description']

class RoomApplicationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = RoomAllocation
        fields = ['room']
