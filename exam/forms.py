from django import forms
from .models import Exam, ExamQuestion
from .models import PracticalAnswer

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['course', 'title', 'description', 'date', 'start_time', 'duration_minutes', 'total_marks']
        widgets = {
             'date': forms.DateInput(
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
        
      self.fields['date'].input_formats = ['%Y/%m/%d']


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