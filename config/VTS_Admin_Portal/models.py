from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import timedelta, date

from django.conf import settings 



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('designer', 'Designer'),
        ('developer', 'Developer'),
        ('designer_trainee', 'Designer Trainee'),
        ('developer_trainee', 'Developer Trainee'),
        ('admin', 'Admin'),
    ]

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
      
    mobile = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'role']

    objects = UserManager()

    def __str__(self):
        return self.email
    
from django.db import models
from django.contrib.auth.models import User

class Trainer(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    EXPERTISE_CHOICES = [
        ('Designing', 'Designing'),
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('fullstack', 'Fullstack'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trainer_profile')

    # Personal Info (in User model: mobile and profile_image)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    dob = models.DateField(verbose_name='Date of Birth', blank=True, null=True)

    # Expertise & Skills
    expertise_area = models.CharField(max_length=20, choices=EXPERTISE_CHOICES)
    experience_years = models.PositiveIntegerField(default=0)

    technical_languages = models.TextField(
        help_text="Enter comma-separated languages like: Python, Angular, React"
    )

    # Address
    address_line1 = models.CharField(max_length=255, verbose_name='Address Line 1', blank=True)
    address_line2 = models.CharField(max_length=255, verbose_name='Address Line 2', blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=100, default='India')

    # Status
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} ({self.get_expertise_area_display()})"

    def get_technical_languages_list(self):
        return [lang.strip() for lang in self.technical_languages.split(',') if lang.strip()]

class Course(models.Model):
    CATEGORY_CHOICES = [
        ('design', 'Design'),
        ('development', 'Development'),
        ('fullstack', 'Fullstack'),
        ('softskills', 'Soft Skills'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    duration_weeks = models.PositiveIntegerField(help_text="Duration in weeks")
    
    
    fee = models.DecimalField(max_digits=8, decimal_places=2, help_text="Course fee in INR")

    trainer = models.ForeignKey('Trainer', on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def duration_display(self):
        return f"{self.duration_weeks} week(s)"      





class Trainee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    CLASS_MODE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]


    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trainee_profile')

    # Personal Info
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    dob = models.DateField(verbose_name='Date of Birth', blank=True, null=True)

    
    class_mode = models.CharField(
        max_length=10,
        choices=CLASS_MODE_CHOICES,
        default='online'
    )

    # Course & Trainer Info (optional foreign keys)
    assigned_course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='trainees')
    assigned_trainer = models.ForeignKey('Trainer', on_delete=models.SET_NULL, null=True, blank=True, related_name='trainees')
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(blank=True, null=True)
    # Address
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=100, default='India')

    # Status
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.start_date and self.assigned_course :
            self.end_date = self.start_date + timedelta(weeks=self.assigned_course.duration_weeks)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.full_name

    def get_full_address(self):
        return f"{self.address_line1}, {self.address_line2}, {self.city}, {self.state} - {self.postal_code}, {self.country}"
