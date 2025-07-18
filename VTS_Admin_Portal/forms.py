from django import forms
from exam.models import PracticalQuestion


from .models import Trainee, Trainer
from django.conf import settings
from django.apps import apps

User = apps.get_model(settings.AUTH_USER_MODEL)

# class TrainerForm(forms.ModelForm):
#     class Meta:
#         model = Trainer
#         fields = [  # only fields actually in the Trainer model
#             'user', 'gender', 'dob',
#             'expertise_area', 'experience_years',
#             'technical_languages', 'address_line1', 'address_line2',
#             'city', 'state', 'postal_code', 'country',
#             'is_active'
#         ]
        

#     def __init__(self, *args, **kwargs):
#         super(TrainerForm, self).__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs.update({
#                 'class': 'form-input',
#                 'style': 'width: 100%; height: 36px; font-size: 16px; padding: 5px;',
#             })
from django.core.exceptions import ValidationError

class TrainerUserForm(forms.Form):
    # USER FIELDS
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    mobile = forms.CharField(max_length=10)
    profile_image = forms.ImageField(required=False)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)
    is_staff = forms.BooleanField(required=False, initial=False)
    is_active = forms.BooleanField(required=False, initial=True)

    # TRAINER FIELDS
    gender = forms.ChoiceField(choices=Trainer.GENDER_CHOICES)
    dob = forms.DateField(
    input_formats=['%Y-%m-%d', '%Y/%m/%d'],  # Accept both formats
    error_messages={'invalid': 'Enter a valid date in YYYY/MM/DD or YYYY-MM-DD format.'},
    widget=forms.DateInput(
        attrs={
            'type': 'text',
            'placeholder': 'YYYY/MM/DD',
            'class': 'form-input',
            'style': 'width: 100%; height: 36px; font-size: 16px; padding: 5px;'
        }
    )
)
    expertise_area = forms.ChoiceField(choices=Trainer.EXPERTISE_CHOICES)
    experience_years = forms.IntegerField()
    technical_languages = forms.CharField()
    address_line1 = forms.CharField()
    address_line2 = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    postal_code = forms.CharField()
    country = forms.CharField(initial='India')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-input',
                'style': 'width: 100%; height: 36px; font-size: 16px; padding: 5px;',
            })

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.initial.get('email') != email:
            if User.objects.filter(email=email).exists():
                raise ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        # Only validate if password is being set
        if password or confirm:
            if password != confirm:
                raise ValidationError("Passwords do not match.")
            
from django.db.models import Q



class TraineeUserForm(forms.Form):
    # User fields
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    mobile = forms.CharField(max_length=10)
    profile_image = forms.ImageField(required=False)

    is_staff = forms.BooleanField(required=False, initial=False)
    is_active = forms.BooleanField(required=False, initial=True)

    # Trainee fields
    gender = forms.ChoiceField(choices=Trainee.GENDER_CHOICES)
    dob = forms.DateField(
        input_formats=['%Y/%m/%d'],
        widget=forms.DateInput(attrs={'type': 'text', 'placeholder': 'yyyy/mm/dd'})
    )
    class_mode = forms.ChoiceField(choices=Trainee.CLASS_MODE_CHOICES)
    assigned_course = forms.ModelChoiceField(queryset=None, required=False)
    assigned_trainer = forms.ModelChoiceField(queryset=None, required=False)
    start_date = forms.DateField(
        input_formats=['%Y/%m/%d'],
        widget=forms.DateInput(attrs={'type': 'text', 'placeholder': 'yyyy/mm/dd'})
    )

    address_line1 = forms.CharField()
    address_line2 = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    postal_code = forms.CharField()
    country = forms.CharField(initial='India')

    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



        from .models import Course, Trainer  # import here to avoid circular import


        self.fields['assigned_course'].queryset = Course.objects.all()
        self.fields['assigned_trainer'].queryset = Trainer.objects.all()

        

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-input',
                'style': 'width: 100%; height: 36px; font-size: 16px; padding: 5px;',
            })

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists() and not self.initial.get('email') == email:
            raise ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password or confirm:
            if password != confirm:
                raise ValidationError("Passwords do not match.")


class PracticalQuestionForm(forms.ModelForm):
    class Meta:
        model = PracticalQuestion
        fields = ['course', 'title','question_pdf']

        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter Title'}),
        }