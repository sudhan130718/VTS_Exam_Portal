from django import forms
from .models import Exam, ExamQuestion
from .models import PracticalAnswer

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['course', 'title', 'description', 'date', 'start_time', 'duration_minutes', 'total_marks', 'isActivate']
        widgets = {
             'date': forms.DateInput(
                attrs={
                    'type': 'text',  # important: type text so Flatpickr can override
                    'placeholder': 'yyyy/mm/dd',
                    'class': 'form-control',

                    'readonly': 'readonly',
                },
                format='%Y/%m/%d'
            ),
         }
        
    def __init__(self, *args, **kwargs):
      user = kwargs.pop('user', None)

      super().__init__(*args, **kwargs)
      # ✅ Initially disable isActivate
      self.fields['isActivate'].disabled = True

       # Filter course dropdown based on logged-in trainer
      if user:
            print("user", user)

            trainer = getattr(user, 'trainer_profile', None)
            if trainer:
                self.fields['course'].queryset = trainer.courses.all()
        
      self.fields['date'].input_formats = ['%Y/%m/%d']

      # Disable isActivate if total_marks != questions.count
      if self.instance and self.instance.pk:  # editing existing exam
            if self.instance.total_marks != self.instance.questions.count():
                self.fields['isActivate'].disabled = True
            if self.instance.total_marks == self.instance.questions.count():
                                self.fields['isActivate'].disabled = False


    

class ExamQuestionForm(forms.ModelForm):
    class Meta:
        model = ExamQuestion
        fields = ['exam', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option']
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter question text'}),
            'correct_option': forms.Select(attrs={'class': 'select-input'}),
        }







class PracticalAnswerForm(forms.ModelForm):
    class Meta:
        model = PracticalAnswer
        fields = ['answer_pdf']
        widgets = {
            'answer_pdf': forms.FileInput(attrs={'class': 'form-control'}),
        }