from django.db import models
from django.conf import settings
from django.utils import timezone
class Exam(models.Model):
    trainer = models.ForeignKey(
    'VTS_Admin_Portal.Trainer',
    on_delete=models.SET_NULL,   # If trainer is deleted, set NULL instead of deleting Exam
    null=True,                   # Allow NULL in database
    blank=True,                  # Allow empty in Django forms/admin
    default=None                 # Default value is None
)


    course = models.ForeignKey('VTS_Admin_Portal.Course', on_delete=models.CASCADE, related_name='exams')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField(default=0)
    # ✅ New fields
    isActivate = models.BooleanField(default=False)   
    isExpired = models.BooleanField(default=False)    


    def __str__(self):
        return f"{self.title} - {self.course.name}"


class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])

    def __str__(self):
        return self.question_text[:50]
    
    def save(self, *args, **kwargs):
        # Check existing question count for this exam
        if self.exam.questions.count() >= self.exam.total_marks:
            from django.core.exceptions import ValidationError
            raise ValidationError(f"Cannot add more than {self.exam.total_marks} questions for this exam.")
        
        super().save(*args, **kwargs)


class TraineeExam(models.Model):
    trainee = models.ForeignKey('VTS_Admin_Portal.Trainee', on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)
    score = models.PositiveIntegerField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='trainee_exam_images/', default='images/default.jpg')
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('trainee', 'exam')


class TraineeAnswer(models.Model):
    trainee_exam = models.ForeignKey(TraineeExam, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')], null=True)

    def __str__(self):
        return f"{self.trainee_exam.trainee} - {self.question}"

class PracticalQuestion(models.Model):
    course = models.ForeignKey('VTS_Admin_Portal.Course', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    question_pdf = models.FileField(upload_to='practical_questions/')
    created_at = models.DateTimeField(auto_now_add=True)
    isActivate = models.BooleanField(default=True)   


    def __str__(self):
        return f"{self.title} ({self.course.name})"    

class PracticalAnswer(models.Model):
    question = models.ForeignKey(PracticalQuestion, on_delete=models.CASCADE)
    trainee = models.ForeignKey('VTS_Admin_Portal.Trainee', on_delete=models.CASCADE)
    answer_pdf = models.FileField(upload_to='practical_answers/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trainee.user}'s Answer - {self.question.title}"    
