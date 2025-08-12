from django import forms
from exam.models import PracticalQuestion


from .models import Course, Trainee, Trainer
from django.conf import settings
from django.apps import apps
from django.forms import HiddenInput


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
import re


            

class TrainerUserForm(forms.Form):
    # USER FIELDS
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    mobile = forms.CharField(max_length=10)
    # profile_image = forms.ImageField(
    # required=True,
    # error_messages={'required': 'Profile photo is required.'})

    profile_image = forms.ImageField(required=False)
    # role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    role = forms.CharField(max_length=100, required=True)

    # password = forms.CharField(widget=forms.PasswordInput, required=False, readonly=True)
    # confirm_password = forms.CharField(widget=forms.PasswordInput, required=False, readonly=True)
    password = forms.CharField(
    widget=forms.PasswordInput(attrs={'readonly': 'readonly'}),
    required=False
)
    confirm_password = forms.CharField(
    widget=forms.PasswordInput(attrs={'readonly': 'readonly'}),
    required=False
)
        
    # password = forms.CharField(
    # widget=forms.PasswordInput,
    # required=True,
    # min_length=6,
    # error_messages={'required': 'Password is required.'})
    # confirm_password = forms.CharField(
    # widget=forms.PasswordInput,
    # required=True,
    # error_messages={'required': 'Confirm password is required.'})




    is_staff = forms.BooleanField(required=False, initial=False)
    is_active = forms.BooleanField(required=False, initial=True)

    # TRAINER FIELDS
    gender = forms.ChoiceField(choices=Trainer.GENDER_CHOICES)
    dob = forms.DateField(
        input_formats=['%Y-%m-%d', '%Y/%m/%d'],
        error_messages={'invalid': 'Enter a valid date in YYYY/MM/DD or YYYY-MM-DD format.'},
        widget=forms.DateInput(
            attrs={
                'type': 'text',
                'placeholder': 'YYYY/MM/DD',
                'class': 'form-input',
                'style': 'width: 100%; height: 36px; font-size: 16px; padding: 5px;',
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
    postal_code = forms.CharField(max_length=6)
    country = forms.CharField(initial='India')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['role'].widget.attrs['readonly'] = True

        if not kwargs.get('initial') or not kwargs['initial'].get('email'):
         self.fields['password'].required = True
         self.fields['confirm_password'].required = True
         self.fields['profile_image'].required = True
         self.fields['password'].widget.attrs['readonly'] = False
         self.fields['confirm_password'].widget.attrs['readonly'] = False



        #  self.fields['password'].widget = HiddenInput()

        #  self.fields['confirm_password'].widget = HiddenInput()




        

        
            
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-input',
                'style': 'width: 100%; height: 36px; font-size: 16px; padding: 5px;',
            })

    def clean_email(self):
     email = self.cleaned_data['email']
     common_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']
    
     if not re.fullmatch(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', email):
        raise ValidationError("Enter a valid email address.")
    
     domain = email.split('@')[-1]
     if self.initial.get('email') != email:
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")
    
     if domain not in common_domains:
        raise ValidationError("Please enter an email with a valid domain (e.g., gmail.com).")

     return email
    
    


    # ✅ Mobile validation (10-digit numeric only)
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if not re.fullmatch(r'[6-9]\d{9}', mobile):
            raise ValidationError("Enter a valid 10-digit mobile number starting with 6-9.")
        return mobile

    # ✅ Postal code validation (6-digit Indian format)
    def clean_postal_code(self):
        postal = self.cleaned_data['postal_code']
        if not re.fullmatch(r'\d{6}', postal):
            raise ValidationError("Enter a valid 6-digit postal code.")
        return postal

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if city and not re.fullmatch(r'[A-Za-z ]+', city):
            raise ValidationError("City name should contain only letters and spaces.")
        return city

    def clean_state(self):
        state = self.cleaned_data.get('state')
        if state and not re.fullmatch(r'[A-Za-z ]+', state):
            raise ValidationError("State name should contain only letters and spaces.")
        return state

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if country and not re.fullmatch(r'[A-Za-z ]+', country):
            raise ValidationError("Country name should contain only letters and spaces.")
        return country

    # ✅ Password confirmation validation
    def clean(self):
     cleaned_data = super().clean()
     password = cleaned_data.get("password")
     confirm = cleaned_data.get("confirm_password")
     

     if password and confirm and password != confirm:
        self.add_error('confirm_password', "Passwords do not match.") 

     if password:
      if len(password) < 6:
            self.add_error('password', 'Password must be at least 6 characters long.')
      elif not re.search(r'[A-Z]', password):
            self.add_error('password', 'Password must include at least one uppercase letter.')
      elif not re.search(r'[a-z]', password):
            self.add_error('password', 'Password must include at least one lowercase letter.')
      elif not re.search(r'\d', password):
            self.add_error('password', 'Password must include at least one digit.')    
            
from django.db.models import Q



class TraineeUserForm(forms.Form):
    # User fields
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)
    role = forms.CharField(max_length=100, required=True)
    mobile = forms.CharField(max_length=10)
    profile_image = forms.ImageField(required=False)

    # is_staff = forms.BooleanField(required=False, initial=False)
    # is_active = forms.BooleanField(required=False, initial=True)

    # Trainee fields
    gender = forms.ChoiceField(choices=Trainee.GENDER_CHOICES)
    dob = forms.DateField(
        input_formats=['%Y/%m/%d'],
        widget=forms.DateInput(attrs={'type': 'text', 'placeholder': 'yyyy/mm/dd'})
    )
    class_mode = forms.ChoiceField(choices=Trainee.CLASS_MODE_CHOICES)
    assigned_course = forms.ModelChoiceField(queryset=None, required=False)
    # assigned_trainer = forms.ModelChoiceField(queryset=None, required=False)
    # start_date = forms.DateField(
    #     input_formats=['%Y/%m/%d'],
    #     widget=forms.DateInput(attrs={'type': 'text', 'placeholder': 'yyyy/mm/dd'})
    # )

    address_line1 = forms.CharField()
    address_line2 = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    postal_code = forms.CharField(max_length=6)
    country = forms.CharField(initial='India')

    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.fields['role'].widget.attrs['readonly'] = True

        from .models import Course, Trainer  # import here to avoid circular import


        self.fields['assigned_course'].queryset = Course.objects.all()
        # self.fields['assigned_trainer'].queryset = Trainer.objects.all()

        

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-input',
                'style': 'width: 100%; height: 36px; font-size: 16px; padding: 5px;',
            })

    def clean_email(self):
        email = self.cleaned_data['email']

        # ✅ Regex for basic email format validation
        if not re.fullmatch(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$', email):
            raise ValidationError("Enter a valid email address.")

        # ✅ Check if email already exists (only if it changed)
        if self.initial.get('email') != email:
            if User.objects.filter(email=email).exists():
                raise ValidationError("Email already exists.")

        return email

    # ✅ Mobile validation (10-digit numeric only)
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if not re.fullmatch(r'[6-9]\d{9}', mobile):
            raise ValidationError("Enter a valid 10-digit mobile number starting with 6-9.")
        return mobile

    # ✅ Postal code validation (6-digit Indian format)
    def clean_postal_code(self):
        postal = self.cleaned_data['postal_code']
        if not re.fullmatch(r'\d{6}', postal):
            raise ValidationError("Enter a valid 6-digit postal code.")
        return postal

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if city and not re.fullmatch(r'[A-Za-z ]+', city):
            raise ValidationError("City name should contain only letters and spaces.")
        return city

    def clean_state(self):
        state = self.cleaned_data.get('state')
        if state and not re.fullmatch(r'[A-Za-z ]+', state):
            raise ValidationError("State name should contain only letters and spaces.")
        return state

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if country and not re.fullmatch(r'[A-Za-z ]+', country):
            raise ValidationError("Country name should contain only letters and spaces.")
        return country

    # ✅ Password confirmation validation
    def clean(self):
      cleaned_data = super().clean()
      password = cleaned_data.get("password")
      confirm = cleaned_data.get("confirm_password")
    

      if password and confirm and password != confirm:
        self.add_error('confirm_password', "Passwords do not match.")   


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'name', 'description', 'category', 'duration_weeks',
            'start_date', 'fee', 'trainer', 'is_active'
        ]
        widgets = {
            'start_date': forms.DateInput(
                attrs={
                    'type': 'text',  # important: type text so Flatpickr can override
                    'placeholder': 'yyyy/mm/dd',
                    'class': 'form-control',
                    'readonly': 'readonly',
                },
                format='%Y/%m/%d'
            ),
             'description': forms.TextInput(  
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter course description'
                }
            ),
            'duration_weeks': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '2',     # Allows 2 digits, like 12 weeks
                'min': '1'
            }),
            'fee': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '6',     # Allows 6 digits, like 500000
                'min': '1'
            }),
         }
        
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
        
      self.fields['start_date'].input_formats = ['%Y/%m/%d']
    


class PracticalQuestionForm(forms.ModelForm):
    class Meta:
        model = PracticalQuestion
        fields = ['course', 'title','question_pdf']

        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter Title'}),
        }