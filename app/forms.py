from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password

from app.models import Investigation, Patient


class PatientRegistrationForm(UserCreationForm):
    """Override UserCreationForm styles & fields"""

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'name': 'password1',
                'id': 'password1',
                'class': 'form-control',
                "required": True
            }
        )
    )

    class Meta:
        model = Patient
        fields = ('name', 'email', 'password1')
        widgets = {
            'name': forms.TextInput(attrs={
                'name': 'name',
                'id': 'name',
                'class': 'form-control',
                "required": True
            }),
            'email': forms.EmailInput(attrs={
                'name': 'email',
                'id': 'email',
                'class': 'form-control',
                "required": True
            })
        }

    def __init__(self, *args, **kwargs):
        super(PatientRegistrationForm, self).__init__(*args, **kwargs)
        del self.fields['password2']

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        try:
            validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error('password1', error)
        return password1 


class LoginForm(AuthenticationForm):
    """Override AuthenticationForm styles"""

    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'name': 'email',
                'id': 'email',
                'class': 'form-control',
                "required": True
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'name': 'password',
                'id': 'password',
                'class': 'form-control',
                "required": True
            }
        )
    )


class UploadInvestigationForm(forms.ModelForm):
    """Upload investigation form fields with style"""

    class Meta:
        model = Investigation
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={
                'name': 'title',
                'id': 'invest_title',
                'class': 'form-control col-sm-7',
                "required": True
            }),
            'file': forms.FileInput(attrs={
                'name': 'file',
                'id': 'invest_file',
                'class': 'col-sm-7',
                "required": True
            })
        }
