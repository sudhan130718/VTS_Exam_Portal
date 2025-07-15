from django import forms
from exam.models import PracticalQuestion


from .models import Trainee, Trainer
from django.conf import settings
from django.apps import apps

User = apps.get_model(settings.AUTH_USER_MODEL)

class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = [  # only fields actually in the Trainer model
            'user', 'gender', 'dob',
            'expertise_area', 'experience_years',
            'technical_languages', 'address_line1', 'address_line2',
            'city', 'state', 'postal_code', 'country',
            'is_active'
        ]
        

    def __init__(self, *args, **kwargs):
        super(TrainerForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-input',
                'style': 'width: 100%; height: 36px; font-size: 16px; padding: 5px;',
            })

from django.db.models import Q

class TraineeForm(forms.ModelForm):
    class Meta:
        model = Trainee
        exclude = ['end_date'] 
        # fields = '__all__'

        widgets = {
             'start_date': forms.DateInput(
                attrs={
                    'type': 'text',  # important: type text so Flatpickr can override
                    'placeholder': 'yyyy/mm/dd',
                    'class': 'form-control'
                },
                format='%Y/%m/%d'
            ),
            'dob': forms.DateInput(
                attrs={
                    'type': 'text',  # important: type text so Flatpickr can override
                    'placeholder': 'yyyy/mm/dd',
                    'class': 'form-control'
                },
                format='%Y/%m/%d'
            ),
        }


    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

        # Set input formats for initial display values
      self.fields['start_date'].input_formats = ['%Y/%m/%d']
      self.fields['dob'].input_formats = ['%Y/%m/%d']

      assigned_users = Trainee.objects.values_list('user_id', flat=True)


    
      if self.instance and self.instance.pk:
        self.fields['user'].queryset = User.objects.filter(
            Q(id=self.instance.user_id) | ~Q(id__in=assigned_users)
        )
      else:
        self.fields['user'].queryset = User.objects.exclude(id__in=assigned_users)


class PracticalQuestionForm(forms.ModelForm):
    class Meta:
        model = PracticalQuestion
        fields = ['course', 'title','question_pdf']

        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter Title'}),
        }